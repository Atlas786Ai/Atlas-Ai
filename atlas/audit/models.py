"""Domain models for AuditRepository.

Module Name: atlas.audit.models
Purpose: Define immutable, append-only audit events and archive summaries.
Owner: Atlas Governance
Version: 1.0.0
Dependencies: dataclasses, atlas.core.models
Architecture Layer: Repository
"""

from dataclasses import dataclass, field
from uuid import uuid4

from atlas.core.models import stable_checksum, utc_now


@dataclass(frozen=True)
class AuditEvent:
    """Immutable audit event for cross-repository reconstruction."""

    event_type: str
    actor: str
    action: str
    source_repository: str
    payload: dict[str, object]
    trace_id: str
    audit_id: str = field(default_factory=lambda: str(uuid4()))
    recorded_at: str = field(default_factory=utc_now)
    version: str = "1.0.0"
    integrity_hash: str = ""

    def to_payload(self) -> dict[str, object]:
        """Return a deterministic audit event payload."""
        return {
            "audit_id": self.audit_id,
            "event_type": self.event_type,
            "actor": self.actor,
            "action": self.action,
            "source_repository": self.source_repository,
            "payload": self.payload,
            "trace_id": self.trace_id,
            "recorded_at": self.recorded_at,
            "version": self.version,
            "integrity_hash": self.integrity_hash,
        }

    def with_integrity_hash(self) -> "AuditEvent":
        """Return an audit event with integrity hash over immutable content."""
        payload = self.to_payload()
        payload["integrity_hash"] = ""
        return AuditEvent(
            audit_id=self.audit_id,
            event_type=self.event_type,
            actor=self.actor,
            action=self.action,
            source_repository=self.source_repository,
            payload=self.payload,
            trace_id=self.trace_id,
            recorded_at=self.recorded_at,
            version=self.version,
            integrity_hash=stable_checksum(payload),
        )
