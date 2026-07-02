"""Mapping helpers between schemas and models."""

def identity_map(payload: dict[str, object]) -> dict[str, object]:
    """Return a defensive copy of payload."""
    return dict(payload)
