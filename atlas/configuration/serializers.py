"""Serialization helpers for ConfigurationRepository.

Module Name: atlas.configuration.serializers
Purpose: Serialize configuration payloads deterministically.
Owner: Atlas Governance
Version: 1.0.0
Dependencies: json
Architecture Layer: Repository
"""

import json


def to_json(payload: dict[str, object]) -> str:
    """Serialize payload deterministically."""
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def from_json(content: str) -> dict[str, object]:
    """Deserialize a JSON configuration payload."""
    payload = json.loads(content)
    if not isinstance(payload, dict):
        raise ValueError("Configuration JSON must decode to an object")
    return payload
