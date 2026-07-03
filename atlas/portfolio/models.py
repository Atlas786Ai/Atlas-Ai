"""Domain models for PortfolioRepository."""

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass(frozen=True)
class PortfolioRecord:
    """Immutable domain record owned by PortfolioRepository."""

    record_id: str = field(default_factory=lambda: str(uuid4()))
    status: str = "Created"
    version: str = "1.0.0"
