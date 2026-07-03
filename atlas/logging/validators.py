"""Validation helpers for LoggingRepository."""

from atlas.core.exceptions import AtlasValidationError
from atlas.logging.constants import ALLOWED_LOG_LEVELS

REQUIRED_LOG_FIELDS = ("log_id", "timestamp", "repository", "level", "message", "context", "trace_id", "version")


def validate_payload(payload: dict[str, object]) -> None:
    """Validate a generic repository payload dictionary."""
    if not isinstance(payload, dict):
        raise AtlasValidationError("payload must be a dictionary")


def validate_log_payload(payload: dict[str, object]) -> None:
    """Validate a structured log payload against Atlas logging invariants."""
    validate_payload(payload)
    missing = [field for field in REQUIRED_LOG_FIELDS if field not in payload]
    if missing:
        raise AtlasValidationError("log payload is missing required fields", context={"missing": missing})
    level = payload["level"]
    if not isinstance(level, str) or level.upper() not in ALLOWED_LOG_LEVELS:
        raise AtlasValidationError("invalid log level", context={"level": level, "allowed": ALLOWED_LOG_LEVELS})
    for field in ("log_id", "timestamp", "repository", "message", "trace_id", "version"):
        if not isinstance(payload[field], str):
            raise AtlasValidationError("log field must be a string", context={"field": field})
    if not isinstance(payload["context"], dict):
        raise AtlasValidationError("log context must be a dictionary")
