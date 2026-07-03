"""Domain models for ReasoningRepository."""

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass(frozen=True)
class ReasoningRecord:
    """Immutable domain record owned by ReasoningRepository."""

    record_id: str = field(default_factory=lambda: str(uuid4()))
    status: str = "Created"
    version: str = "1.0.0"
