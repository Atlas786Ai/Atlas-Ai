"""Business service boundary for SecurityRepository.

Module Name: atlas.security.services
Purpose: Implement deterministic authentication, authorization, and policy validation.
Owner: Atlas Governance
Version: 1.0.0
Dependencies: atlas.repository_base, atlas.security.models
Architecture Layer: Repository
"""

from typing import Any

from atlas.core.exceptions import AtlasValidationError
from atlas.core.models import stable_checksum, utc_now
from atlas.repository_base import RepositoryBase
from atlas.security.constants import SECURITY_DECISION_ALLOWED, SECURITY_DECISION_DENIED, SENSITIVE_AUTH_FIELDS
from atlas.security.models import SecurityDecision, SecurityPrincipal
from atlas.security.validators import validate_payload, validate_policy_payload, validate_principal_payload


class SecurityRepository(RepositoryBase):
    """Frozen Atlas v1.0 repository implementation for security checks."""

    repository_name = "SecurityRepository"
    public_interfaces = (
        "authenticate",
        "authorize",
        "verify_signature",
        "validate_permission",
        "validate_policy",
        "archive_security_event",
        "get_security_status",
    )
    event_types = (
        "AuthenticationValidated",
        "AuthorizationEvaluated",
        "SignatureVerified",
        "PermissionValidated",
        "PolicyValidated",
        "SecurityEventArchived",
    )

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        self._principal_ids: list[str] = []
        self._decision_ids: list[str] = []
        self._security_event_ids: list[str] = []

    def authenticate(
        self,
        principal_id: str,
        *,
        roles: tuple[str, ...] | list[str] = (),
        credential_reference: str = "external",
        trace_id: str = "",
        key: str | None = None,
        **credentials: object,
    ) -> dict[str, object]:
        """Authenticate a principal without accepting or storing raw secrets."""
        self._reject_raw_secrets(credentials)
        if not isinstance(credential_reference, str) or not credential_reference:
            raise AtlasValidationError("credential_reference must be a non-empty external reference")
        normalized_roles = self._normalize_roles(roles)
        principal = SecurityPrincipal(
            principal_id=self._require_text(principal_id, "principal_id"),
            roles=normalized_roles,
            trace_id=self._require_optional_text(trace_id, "trace_id"),
        ).with_integrity_hash()
        payload = principal.to_payload()
        validate_principal_payload(payload)
        storage_key = key or principal.principal_record_id
        record = self.archive_record(storage_key, payload)
        self._principal_ids.append(storage_key)
        self.emit_event(
            "AuthenticationValidated",
            {"principal_id": principal.principal_id, "key": storage_key, "integrity_hash": record["integrity_hash"]},
            trace_id=trace_id,
        )
        return payload

    def authorize(
        self,
        principal: dict[str, object],
        permission: str,
        policy: dict[str, object],
        *,
        trace_id: str = "",
        key: str | None = None,
    ) -> dict[str, object]:
        """Authorize a permission for an authenticated principal under a validated policy."""
        allowed = self.validate_permission(principal, permission, policy)
        reason = SECURITY_DECISION_ALLOWED if allowed else SECURITY_DECISION_DENIED
        decision = SecurityDecision(
            principal_id=str(principal["principal_id"]),
            permission=self._require_text(permission, "permission"),
            allowed=allowed,
            reason=reason,
            trace_id=self._require_optional_text(trace_id, "trace_id"),
        ).with_integrity_hash()
        payload = decision.to_payload()
        storage_key = key or decision.decision_id
        record = self.archive_record(storage_key, payload)
        self._decision_ids.append(storage_key)
        self.emit_event(
            "AuthorizationEvaluated",
            {"decision_id": decision.decision_id, "allowed": allowed, "integrity_hash": record["integrity_hash"]},
            trace_id=trace_id,
        )
        return payload

    def verify_signature(self, payload: dict[str, object], signature: str, *, trace_id: str = "") -> bool:
        """Verify a deterministic SHA-256 style stable checksum signature."""
        validate_payload(payload)
        expected = stable_checksum(payload)
        verified = expected == self._require_text(signature, "signature")
        self.emit_event(
            "SignatureVerified",
            {"verified": verified, "expected_hash": expected},
            trace_id=trace_id,
        )
        return verified

    def validate_permission(self, principal: dict[str, object], permission: str, policy: dict[str, object]) -> bool:
        """Validate whether principal roles grant a permission in the supplied policy."""
        validate_principal_payload(principal)
        validate_policy_payload(policy)
        permission_name = self._require_text(permission, "permission")
        if not principal["authenticated"]:
            return False
        role_permissions = policy["role_permissions"]
        allowed_permissions: set[str] = set()
        if not isinstance(role_permissions, dict):
            raise AtlasValidationError("role_permissions must be a dictionary")
        for role in principal["roles"]:
            permissions = role_permissions.get(role, ())
            if isinstance(permissions, (tuple, list)):
                allowed_permissions.update(str(item) for item in permissions)
        allowed = permission_name in allowed_permissions or "*" in allowed_permissions
        self.emit_event("PermissionValidated", {"principal_id": principal["principal_id"], "permission": permission_name, "allowed": allowed})
        return allowed

    def validate_policy(self, payload: dict[str, object]) -> bool:
        """Validate a role-permission policy payload."""
        validate_policy_payload(payload)
        self.emit_event("PolicyValidated", {"policy_id": payload["policy_id"], "version": payload["version"]})
        return True

    def archive_security_event(
        self,
        event_type: str,
        payload: dict[str, object],
        *,
        trace_id: str = "",
        key: str | None = None,
    ) -> dict[str, Any]:
        """Archive an immutable security event without changing its meaning."""
        validate_payload(payload)
        security_event = {
            "event_type": self._require_text(event_type, "event_type"),
            "payload": payload,
            "trace_id": self._require_optional_text(trace_id, "trace_id"),
            "created_at": utc_now(),
            "version": "1.0.0",
        }
        storage_key = key or stable_checksum(security_event)
        record = self.archive_record(storage_key, security_event)
        self._security_event_ids.append(storage_key)
        self.emit_event("SecurityEventArchived", {"key": storage_key, "integrity_hash": record["integrity_hash"]}, trace_id=trace_id)
        return record

    def get_security_status(self) -> dict[str, object]:
        """Return deterministic SecurityRepository status and counters."""
        return {
            "repository": self.repository_name,
            "version": "1.0.0",
            "principals": len(self._principal_ids),
            "decisions": len(self._decision_ids),
            "security_events": len(self._security_event_ids),
            "events_emitted": len(self._events),
        }

    def _normalize_roles(self, roles: tuple[str, ...] | list[str]) -> tuple[str, ...]:
        if not isinstance(roles, (tuple, list)) or not all(isinstance(role, str) and role for role in roles):
            raise AtlasValidationError("roles must be a tuple or list of non-empty strings")
        return tuple(sorted(roles))

    def _reject_raw_secrets(self, credentials: dict[str, object]) -> None:
        for field in credentials:
            if any(marker in field.lower() for marker in SENSITIVE_AUTH_FIELDS):
                raise AtlasValidationError("raw secrets must not be passed to SecurityRepository", context={"field": field})

    def _require_text(self, value: str, field: str) -> str:
        if not isinstance(value, str) or not value:
            raise AtlasValidationError(f"{field} must be a non-empty string")
        return value

    def _require_optional_text(self, value: str, field: str) -> str:
        if not isinstance(value, str):
            raise AtlasValidationError(f"{field} must be a string")
        return value
