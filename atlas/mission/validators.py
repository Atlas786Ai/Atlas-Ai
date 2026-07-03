"""Validators for MissionRepository."""

from atlas.core.exceptions import AtlasValidationError
from atlas.core.models import stable_checksum
from atlas.mission.constants import MISSION_ACTIVE, MISSION_ARCHIVED, VALID_MISSION_PRIORITIES

_REQUIRED_FIELDS = (
    "mission_id",
    "title",
    "objective",
    "constraints",
    "success_criteria",
    "priority",
    "status",
    "created_at",
    "updated_at",
    "version",
    "integrity_hash",
)


def validate_payload(payload: dict[str, object]) -> None:
    """Validate a mission payload shape without recomputing integrity."""
    if not isinstance(payload, dict):
        raise AtlasValidationError("Payload must be a dictionary")
    missing = [field for field in _REQUIRED_FIELDS if field not in payload]
    if missing:
        raise AtlasValidationError("Mission payload is missing required fields", context={"missing": tuple(missing)})
    for field in ("mission_id", "title", "objective", "created_at", "updated_at", "version", "integrity_hash"):
        if not isinstance(payload[field], str) or not payload[field]:
            raise AtlasValidationError(f"{field} must be a non-empty string")
    for field in ("constraints", "success_criteria"):
        if not isinstance(payload[field], (tuple, list)):
            raise AtlasValidationError(f"{field} must be a tuple or list")
        if not all(isinstance(item, str) and item for item in payload[field]):
            raise AtlasValidationError(f"{field} must contain non-empty strings")
    if payload["priority"] not in VALID_MISSION_PRIORITIES:
        raise AtlasValidationError("priority is invalid", context={"priority": payload["priority"]})
    if payload["status"] not in (MISSION_ACTIVE, MISSION_ARCHIVED):
        raise AtlasValidationError("status is invalid", context={"status": payload["status"]})


def verify_mission_integrity(payload: dict[str, object]) -> None:
    """Validate mission payload and deterministic integrity hash."""
    validate_payload(payload)
    checksum_payload = dict(payload)
    expected_hash = str(checksum_payload["integrity_hash"])
    checksum_payload["integrity_hash"] = ""
    actual_hash = stable_checksum(checksum_payload)
    if actual_hash != expected_hash:
        raise AtlasValidationError(
            "Mission integrity hash mismatch",
            context={"mission_id": payload.get("mission_id"), "expected": expected_hash, "actual": actual_hash},
        )
