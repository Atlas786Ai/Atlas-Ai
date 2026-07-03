"""Serialization helpers."""

import json

def to_json(payload: dict[str, object]) -> str:
    """Serialize payload deterministically."""
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))
