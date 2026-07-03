"""Deterministic serializers for LoggingRepository."""

import json

from atlas.core.exceptions import AtlasValidationError
from atlas.logging.validators import validate_log_payload


def to_json(payload: dict[str, object]) -> str:
    """Serialize a log payload with deterministic key ordering."""
    validate_log_payload(payload)
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def from_json(raw: str) -> dict[str, object]:
    """Deserialize and validate a deterministic log payload."""
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise AtlasValidationError("serialized log payload must decode to a dictionary")
    validate_log_payload(payload)
    return payload
