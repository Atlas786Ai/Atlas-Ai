"""Validators for IdentityRepository."""

from atlas.core.exceptions import AtlasValidationError
from atlas.core.models import stable_checksum

IDENTITY_STATUSES = ("Active", "Archived")
REQUIRED_IDENTITY_FIELDS = (
    "identity_id",
    "name",
    "purpose",
    "traits",
    "capabilities",
    "status",
    "created_at",
    "updated_at",
    "version",
    "integrity_hash",
)


def validate_payload(payload: dict[str, object]) -> None:
    """Validate a generic immutable repository payload."""
    if not isinstance(payload, dict):
        raise AtlasValidationError("Payload must be a dictionary")


def validate_identity_payload(payload: dict[str, object]) -> None:
    """Validate canonical identity payload shape."""
    validate_payload(payload)
    missing = [field for field in REQUIRED_IDENTITY_FIELDS if field not in payload]
    if missing:
        raise AtlasValidationError("identity payload is missing required fields", context={"missing": missing})
    for field in ("identity_id", "name", "purpose", "status", "created_at", "updated_at", "version", "integrity_hash"):
        if not isinstance(payload[field], str):
            raise AtlasValidationError("identity field must be a string", context={"field": field})
    if not payload["identity_id"] or not payload["name"] or not payload["purpose"]:
        raise AtlasValidationError("identity_id, name, and purpose must be non-empty")
    if payload["status"] not in IDENTITY_STATUSES:
        raise AtlasValidationError("invalid identity status", context={"status": payload["status"]})
    for field in ("traits", "capabilities"):
        if not isinstance(payload[field], (tuple, list)) or not all(isinstance(item, str) for item in payload[field]):
            raise AtlasValidationError("identity collection field must contain strings", context={"field": field})


def verify_identity_integrity(payload: dict[str, object]) -> None:
    """Verify deterministic identity integrity hash."""
    validate_identity_payload(payload)
    expected_payload = dict(payload)
    expected_hash = str(expected_payload["integrity_hash"])
    expected_payload["integrity_hash"] = ""
    actual_hash = stable_checksum(expected_payload)
    if expected_hash != actual_hash:
        raise AtlasValidationError("identity integrity hash mismatch", context={"identity_id": payload["identity_id"]})
