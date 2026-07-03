"""Validators for AuditRepository."""

from atlas.core.exceptions import AtlasValidationError
from atlas.core.models import stable_checksum

REQUIRED_AUDIT_FIELDS = (
    "audit_id",
    "event_type",
    "actor",
    "action",
    "source_repository",
    "payload",
    "trace_id",
    "recorded_at",
    "version",
    "integrity_hash",
)


def validate_payload(payload: dict[str, object]) -> None:
    """Validate a generic immutable repository payload."""
    if not isinstance(payload, dict):
        raise AtlasValidationError("Payload must be a dictionary")


def validate_audit_payload(payload: dict[str, object]) -> None:
    """Validate a canonical audit event payload."""
    validate_payload(payload)
    missing = [field for field in REQUIRED_AUDIT_FIELDS if field not in payload]
    if missing:
        raise AtlasValidationError("audit payload is missing required fields", context={"missing": missing})
    for field in ("audit_id", "event_type", "actor", "action", "source_repository", "trace_id", "recorded_at", "version", "integrity_hash"):
        if not isinstance(payload[field], str):
            raise AtlasValidationError("audit field must be a string", context={"field": field})
    if not payload["audit_id"] or not payload["event_type"] or not payload["trace_id"]:
        raise AtlasValidationError("audit_id, event_type, and trace_id must be non-empty")
    if not isinstance(payload["payload"], dict):
        raise AtlasValidationError("audit payload field must be a dictionary")


def verify_audit_integrity(payload: dict[str, object]) -> None:
    """Verify deterministic integrity hash for an audit event."""
    validate_audit_payload(payload)
    expected_payload = dict(payload)
    expected_hash = str(expected_payload["integrity_hash"])
    expected_payload["integrity_hash"] = ""
    actual_hash = stable_checksum(expected_payload)
    if expected_hash != actual_hash:
        raise AtlasValidationError("audit integrity hash mismatch", context={"audit_id": payload["audit_id"]})
