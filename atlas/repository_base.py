"""Base classes for frozen Atlas repository implementations.

Module Name: atlas.repository_base
Purpose: Provide shared deterministic repository behavior without owning domains.
Owner: Atlas Governance
Version: 1.0.0
Dependencies: dataclasses, pathlib, typing, atlas.core
Architecture Layer: Repository Support
"""

from pathlib import Path
from typing import Any

from atlas.core.enums import HealthStatus
from atlas.core.models import Event, HealthReport, MetricSnapshot, stable_checksum, utc_now
from atlas.core.storage import JsonStorage


class RepositoryBase:
    """Reusable infrastructure for one-domain Atlas repositories."""

    repository_name: str = "RepositoryBase"
    public_interfaces: tuple[str, ...] = ()
    event_types: tuple[str, ...] = ()

    def __init__(self, storage_root: Path | None = None) -> None:
        self.storage = JsonStorage(storage_root or Path(".atlas_data") / self.repository_name)
        self._events: list[Event] = []
        self._metrics: dict[str, float] = {"requests": 0.0, "errors": 0.0}

    def emit_event(self, event_type: str, payload: dict[str, Any], *, trace_id: str | None = None) -> Event:
        """Create and retain an immutable repository event."""
        event = Event(event_type=event_type, publisher=self.repository_name, payload=payload, trace_id=trace_id or "")
        self._events.append(event)
        return event

    def health(self) -> HealthReport:
        """Return a deterministic PASS health report for initialized scaffolds."""
        checks = {
            "storage": HealthStatus.PASS,
            "schema": HealthStatus.PASS,
            "configuration": HealthStatus.PASS,
            "version": HealthStatus.PASS,
        }
        return HealthReport(repository=self.repository_name, status=HealthStatus.PASS, checks=checks)

    def metrics(self) -> MetricSnapshot:
        """Return repository metrics."""
        return MetricSnapshot(repository=self.repository_name, metrics=dict(sorted(self._metrics.items())))

    def archive_record(self, key: str, payload: dict[str, Any]) -> dict[str, Any]:
        """Persist a versioned immutable record with checksum metadata."""
        record = {
            "key": key,
            "repository": self.repository_name,
            "payload": payload,
            "timestamp": utc_now(),
            "version": "1.0.0",
        }
        record["integrity_hash"] = stable_checksum(record)
        self.storage.write(key, record)
        return record

    def as_registration(self) -> dict[str, Any]:
        """Return Runtime registration metadata."""
        return {
            "repository": self.repository_name,
            "version": "1.0.0",
            "interfaces": list(self.public_interfaces),
            "health_endpoint": "health",
            "events": list(self.event_types),
        }

    def _record_request(self) -> None:
        self._metrics["requests"] = self._metrics.get("requests", 0.0) + 1.0

    def _store_and_event(self, action: str, key: str, payload: dict[str, Any]) -> dict[str, Any]:
        self._record_request()
        record = self.archive_record(key, payload)
        self.emit_event(action, {"key": key, "integrity_hash": record["integrity_hash"]})
        return record
