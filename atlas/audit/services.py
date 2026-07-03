"""Business service boundary for AuditRepository.

Module Name: atlas.audit.services
Purpose: Implement deterministic, append-only audit recording and trace reconstruction.
Owner: Atlas Governance
Version: 1.0.0
Dependencies: atlas.repository_base, atlas.audit.models
Architecture Layer: Repository
"""

from typing import Any

from atlas.audit.constants import AUDIT_STATUS_AVAILABLE, AUDIT_STATUS_ARCHIVED
from atlas.audit.models import AuditEvent
from atlas.audit.validators import validate_audit_payload, validate_payload, verify_audit_integrity
from atlas.core.exceptions import AtlasValidationError
from atlas.core.models import stable_checksum, utc_now
from atlas.repository_base import RepositoryBase


class AuditRepository(RepositoryBase):
    """Frozen Atlas v1.0 repository implementation for immutable audit history."""

    repository_name = "AuditRepository"
    public_interfaces = (
        "record_event",
        "load_event",
        "search_events",
        "validate_audit",
        "archive_audit",
        "get_trace",
        "audit_available",
    )
    event_types = (
        "AuditEventRecorded",
        "AuditEventLoaded",
        "AuditValidated",
        "AuditArchived",
        "AuditTraceLoaded",
    )

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        self._audit_ids: list[str] = []
        self._archive_ids: list[str] = []

    def record_event(
        self,
        event_type: str,
        actor: str,
        action: str,
        source_repository: str,
        payload: dict[str, object],
        *,
        trace_id: str,
        key: str | None = None,
    ) -> dict[str, object]:
        """Record an immutable audit event in deterministic append order."""
        validate_payload(payload)
        audit_event = AuditEvent(
            event_type=self._require_text(event_type, "event_type"),
            actor=self._require_text(actor, "actor"),
            action=self._require_text(action, "action"),
            source_repository=self._require_text(source_repository, "source_repository"),
            payload=payload,
            trace_id=self._require_text(trace_id, "trace_id"),
        ).with_integrity_hash()
        audit_payload = audit_event.to_payload()
        verify_audit_integrity(audit_payload)
        storage_key = key or audit_event.audit_id
        record = self.archive_record(storage_key, audit_payload)
        if storage_key not in self._audit_ids:
            self._audit_ids.append(storage_key)
        self.emit_event(
            "AuditEventRecorded",
            {"audit_id": audit_event.audit_id, "trace_id": trace_id, "integrity_hash": record["integrity_hash"]},
            trace_id=trace_id,
        )
        return audit_payload

    def load_event(self, audit_id: str) -> dict[str, object]:
        """Load an immutable audit event by id."""
        record = self.storage.read(self._require_text(audit_id, "audit_id"))
        payload = record["payload"]
        if not isinstance(payload, dict):
            raise AtlasValidationError("stored audit event payload is invalid")
        verify_audit_integrity(payload)
        self.emit_event("AuditEventLoaded", {"audit_id": audit_id}, trace_id=str(payload["trace_id"]))
        return payload

    def search_events(
        self,
        *,
        trace_id: str | None = None,
        source_repository: str | None = None,
        event_type: str | None = None,
        actor: str | None = None,
    ) -> tuple[dict[str, object], ...]:
        """Search recorded audit events without mutating audit history."""
        results: list[dict[str, object]] = []
        for audit_id in self._audit_ids:
            payload = self.load_event(audit_id)
            if trace_id is not None and payload["trace_id"] != trace_id:
                continue
            if source_repository is not None and payload["source_repository"] != source_repository:
                continue
            if event_type is not None and payload["event_type"] != event_type:
                continue
            if actor is not None and payload["actor"] != actor:
                continue
            results.append(payload)
        return tuple(results)

    def validate_audit(self, payload: dict[str, object] | None = None) -> bool:
        """Validate one audit payload or the full tracked audit history."""
        if payload is not None:
            verify_audit_integrity(payload)
        else:
            for audit_id in self._audit_ids:
                self.load_event(audit_id)
        self.emit_event("AuditValidated", {"audit_count": len(self._audit_ids)})
        return True

    def archive_audit(self, *, archive_id: str | None = None) -> dict[str, Any]:
        """Create an immutable archive summary over current audit events."""
        events = tuple(self.load_event(audit_id) for audit_id in self._audit_ids)
        archive_payload: dict[str, object] = {
            "archive_id": archive_id or f"audit-{len(self._archive_ids) + 1:06d}",
            "status": AUDIT_STATUS_ARCHIVED,
            "repository": self.repository_name,
            "audit_count": len(events),
            "audit_ids": tuple(self._audit_ids),
            "created_at": utc_now(),
            "integrity_hash": stable_checksum(events),
            "version": "1.0.0",
        }
        validate_payload(archive_payload)
        key = str(archive_payload["archive_id"])
        record = self.archive_record(key, archive_payload)
        self._archive_ids.append(key)
        self.emit_event("AuditArchived", {"archive_id": key, "integrity_hash": record["integrity_hash"]})
        return record

    def get_trace(self, trace_id: str) -> tuple[dict[str, object], ...]:
        """Return all audit events for a trace id in append order."""
        trace = self.search_events(trace_id=self._require_text(trace_id, "trace_id"))
        self.emit_event("AuditTraceLoaded", {"trace_id": trace_id, "event_count": len(trace)}, trace_id=trace_id)
        return trace

    def audit_available(self) -> dict[str, object]:
        """Return deterministic audit availability status and counts."""
        return {
            "repository": self.repository_name,
            "status": AUDIT_STATUS_AVAILABLE,
            "audit_count": len(self._audit_ids),
            "archive_count": len(self._archive_ids),
            "events_emitted": len(self._events),
            "version": "1.0.0",
        }

    def _require_text(self, value: str, field: str) -> str:
        if not isinstance(value, str) or not value:
            raise AtlasValidationError(f"{field} must be a non-empty string")
        return value
