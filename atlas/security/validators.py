"""Validators for SecurityRepository."""

from atlas.core.exceptions import AtlasValidationError

REQUIRED_POLICY_FIELDS = ("policy_id", "role_permissions", "version")
REQUIRED_PRINCIPAL_FIELDS = ("principal_id", "roles", "authenticated")


def validate_payload(payload: dict[str, object]) -> None:
    """Validate a generic immutable repository payload."""
    if not isinstance(payload, dict):
        raise AtlasValidationError("Payload must be a dictionary")


def validate_principal_payload(payload: dict[str, object]) -> None:
    """Validate a principal payload used for authentication and authorization."""
    validate_payload(payload)
    missing = [field for field in REQUIRED_PRINCIPAL_FIELDS if field not in payload]
    if missing:
        raise AtlasValidationError("principal payload is missing required fields", context={"missing": missing})
    if not isinstance(payload["principal_id"], str) or not payload["principal_id"]:
        raise AtlasValidationError("principal_id must be a non-empty string")
    if not isinstance(payload["roles"], (tuple, list)) or not all(isinstance(role, str) for role in payload["roles"]):
        raise AtlasValidationError("roles must be a tuple or list of strings")
    if not isinstance(payload["authenticated"], bool):
        raise AtlasValidationError("authenticated must be a boolean")


def validate_policy_payload(payload: dict[str, object]) -> None:
    """Validate deterministic role-to-permission policy payloads."""
    validate_payload(payload)
    missing = [field for field in REQUIRED_POLICY_FIELDS if field not in payload]
    if missing:
        raise AtlasValidationError("policy payload is missing required fields", context={"missing": missing})
    role_permissions = payload["role_permissions"]
    if not isinstance(role_permissions, dict):
        raise AtlasValidationError("role_permissions must be a dictionary")
    for role, permissions in role_permissions.items():
        if not isinstance(role, str) or not role:
            raise AtlasValidationError("policy role must be a non-empty string")
        if not isinstance(permissions, (tuple, list)) or not all(isinstance(item, str) for item in permissions):
            raise AtlasValidationError("policy permissions must be a tuple or list of strings", context={"role": role})
    if not isinstance(payload["version"], str) or not payload["version"]:
        raise AtlasValidationError("policy version must be a non-empty string")
