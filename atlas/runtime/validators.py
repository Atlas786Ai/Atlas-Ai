"""Validators for RuntimeRepository."""

from atlas.core.exceptions import AtlasValidationError
from atlas.core.models import stable_checksum

RUNTIME_STATUSES = ("Stopped", "Running", "Restarting", "ShuttingDown")
TASK_STATUSES = ("Pending", "Scheduled")
REQUIRED_STATE_FIELDS = ("state_id", "status", "generation", "active_tasks", "trace_id", "updated_at", "version", "integrity_hash")
REQUIRED_TASK_FIELDS = ("task_id", "task_name", "payload", "trace_id", "status", "scheduled_at", "version", "integrity_hash")


def validate_payload(payload: dict[str, object]) -> None:
    """Validate a generic immutable repository payload."""
    if not isinstance(payload, dict):
        raise AtlasValidationError("Payload must be a dictionary")


def validate_runtime_state_payload(payload: dict[str, object]) -> None:
    """Validate a runtime state payload."""
    validate_payload(payload)
    missing = [field for field in REQUIRED_STATE_FIELDS if field not in payload]
    if missing:
        raise AtlasValidationError("runtime state is missing required fields", context={"missing": missing})
    if payload["status"] not in RUNTIME_STATUSES:
        raise AtlasValidationError("invalid runtime status", context={"status": payload["status"]})
    if not isinstance(payload["generation"], int) or payload["generation"] < 0:
        raise AtlasValidationError("runtime generation must be a non-negative integer")
    if not isinstance(payload["active_tasks"], (tuple, list)):
        raise AtlasValidationError("active_tasks must be a tuple or list")
    for field in ("state_id", "trace_id", "updated_at", "version", "integrity_hash"):
        if not isinstance(payload[field], str):
            raise AtlasValidationError("runtime state field must be a string", context={"field": field})


def validate_task_payload(payload: dict[str, object]) -> None:
    """Validate a scheduled task payload."""
    validate_payload(payload)
    missing = [field for field in REQUIRED_TASK_FIELDS if field not in payload]
    if missing:
        raise AtlasValidationError("task payload is missing required fields", context={"missing": missing})
    if not isinstance(payload["task_name"], str) or not payload["task_name"]:
        raise AtlasValidationError("task_name must be a non-empty string")
    if not isinstance(payload["payload"], dict):
        raise AtlasValidationError("task payload field must be a dictionary")
    if payload["status"] not in TASK_STATUSES:
        raise AtlasValidationError("invalid task status", context={"status": payload["status"]})
    for field in ("task_id", "trace_id", "scheduled_at", "version", "integrity_hash"):
        if not isinstance(payload[field], str):
            raise AtlasValidationError("task field must be a string", context={"field": field})


def verify_integrity(payload: dict[str, object]) -> None:
    """Verify deterministic payload integrity hash."""
    validate_payload(payload)
    expected_payload = dict(payload)
    expected_hash = str(expected_payload.get("integrity_hash", ""))
    expected_payload["integrity_hash"] = ""
    actual_hash = stable_checksum(expected_payload)
    if expected_hash != actual_hash:
        raise AtlasValidationError("runtime payload integrity hash mismatch")
