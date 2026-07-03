"""Domain models for SecurityRepository.

Module Name: atlas.security.models
Purpose: Define immutable security principals, policies, and decisions.
Owner: Atlas Governance
Version: 1.0.0
Dependencies: dataclasses, atlas.core.models
Architecture Layer: Repository
"""

from dataclasses import dataclass, field
from uuid import uuid4

from atlas.core.models import stable_checksum, utc_now


@dataclass(frozen=True)
class SecurityPrincipal:
    """Authenticated security principal for cross-repository interactions."""

    principal_id: str
    roles: tuple[str, ...]
    authenticated: bool = True
    trace_id: str = ""
    principal_record_id: str = field(default_factory=lambda: str(uuid4()))
    issued_at: str = field(default_factory=utc_now)
    version: str = "1.0.0"
    integrity_hash: str = ""

    def to_payload(self) -> dict[str, object]:
        """Return a deterministic principal payload."""
        return {
            "principal_record_id": self.principal_record_id,
            "principal_id": self.principal_id,
            "roles": self.roles,
            "authenticated": self.authenticated,
            "trace_id": self.trace_id,
            "issued_at": self.issued_at,
            "version": self.version,
            "integrity_hash": self.integrity_hash,
        }

    def with_integrity_hash(self) -> "SecurityPrincipal":
        """Return a principal with an integrity hash over its immutable content."""
        payload = self.to_payload()
        payload["integrity_hash"] = ""
        return SecurityPrincipal(
            principal_record_id=self.principal_record_id,
            principal_id=self.principal_id,
            roles=self.roles,
            authenticated=self.authenticated,
            trace_id=self.trace_id,
            issued_at=self.issued_at,
            version=self.version,
            integrity_hash=stable_checksum(payload),
        )


@dataclass(frozen=True)
class SecurityDecision:
    """Immutable authorization decision produced by SecurityRepository."""

    principal_id: str
    permission: str
    allowed: bool
    reason: str
    trace_id: str = ""
    decision_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=utc_now)
    version: str = "1.0.0"
    integrity_hash: str = ""

    def to_payload(self) -> dict[str, object]:
        """Return a deterministic authorization decision payload."""
        return {
            "decision_id": self.decision_id,
            "principal_id": self.principal_id,
            "permission": self.permission,
            "allowed": self.allowed,
            "reason": self.reason,
            "trace_id": self.trace_id,
            "created_at": self.created_at,
            "version": self.version,
            "integrity_hash": self.integrity_hash,
        }

    def with_integrity_hash(self) -> "SecurityDecision":
        """Return a decision with an integrity hash over its immutable content."""
        payload = self.to_payload()
        payload["integrity_hash"] = ""
        return SecurityDecision(
            decision_id=self.decision_id,
            principal_id=self.principal_id,
            permission=self.permission,
            allowed=self.allowed,
            reason=self.reason,
            trace_id=self.trace_id,
            created_at=self.created_at,
            version=self.version,
            integrity_hash=stable_checksum(payload),
        )
