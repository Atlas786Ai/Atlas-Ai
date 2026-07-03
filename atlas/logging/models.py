"""Domain models for LoggingRepository.

Module Name: atlas.logging.models
Purpose: Define immutable, structured log records for Atlas operations.
Owner: Atlas Governance
Version: 1.0.0
Dependencies: dataclasses, atlas.core.models
Architecture Layer: Repository
"""

from dataclasses import dataclass, field
from uuid import uuid4

from atlas.core.models import stable_checksum, utc_now


@dataclass(frozen=True)
class LogEntry:
    """Immutable structured log entry owned by LoggingRepository."""

    repository: str
    level: str
    message: str
    context: dict[str, object] = field(default_factory=dict)
    trace_id: str = ""
    log_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: str = field(default_factory=utc_now)
    version: str = "1.0.0"
    integrity_hash: str = ""

    def to_payload(self) -> dict[str, object]:
        """Return a deterministic payload representation."""
        return {
            "log_id": self.log_id,
            "timestamp": self.timestamp,
            "repository": self.repository,
            "level": self.level,
            "message": self.message,
            "context": self.context,
            "trace_id": self.trace_id,
            "version": self.version,
            "integrity_hash": self.integrity_hash,
        }

    def with_integrity_hash(self) -> "LogEntry":
        """Return a copy with an integrity hash over immutable log content."""
        payload = self.to_payload()
        payload["integrity_hash"] = ""
        return LogEntry(
            log_id=self.log_id,
            timestamp=self.timestamp,
            repository=self.repository,
            level=self.level,
            message=self.message,
            context=self.context,
            trace_id=self.trace_id,
            version=self.version,
            integrity_hash=stable_checksum(payload),
        )
