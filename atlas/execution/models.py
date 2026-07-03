"""Domain models for ExecutionRepository."""

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass(frozen=True)
class ExecutionRecord:
    """Immutable domain record owned by ExecutionRepository."""

    record_id: str = field(default_factory=lambda: str(uuid4()))
    status: str = "Created"
    version: str = "1.0.0"
