"""Domain models for RuntimeRepository."""

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass(frozen=True)
class RuntimeRecord:
    """Immutable domain record owned by RuntimeRepository."""

    record_id: str = field(default_factory=lambda: str(uuid4()))
    status: str = "Created"
    version: str = "1.0.0"
