"""Validators for MemoryRepository."""

from atlas.core.exceptions import AtlasValidationError


def validate_payload(payload: dict[str, object]) -> None:
    """Validate a generic immutable repository payload."""
    if not isinstance(payload, dict):
        raise AtlasValidationError("Payload must be a dictionary")
