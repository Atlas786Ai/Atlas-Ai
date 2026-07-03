"""Domain models for RuntimeRepository.

Module Name: atlas.runtime.models
Purpose: Define immutable runtime state and task scheduling records.
Owner: Atlas Governance
Version: 1.0.0
Dependencies: dataclasses, atlas.core.models
Architecture Layer: Repository
"""

from dataclasses import dataclass, field
from uuid import uuid4

from atlas.core.models import stable_checksum, utc_now
from atlas.runtime.constants import RUNTIME_STOPPED, TASK_PENDING


@dataclass(frozen=True)
class RuntimeState:
    """Immutable runtime lifecycle state snapshot."""

    status: str = RUNTIME_STOPPED
    generation: int = 0
    active_tasks: tuple[str, ...] = ()
    trace_id: str = ""
    state_id: str = field(default_factory=lambda: str(uuid4()))
    updated_at: str = field(default_factory=utc_now)
    version: str = "1.0.0"
    integrity_hash: str = ""

    def to_payload(self) -> dict[str, object]:
        """Return deterministic runtime state payload."""
        return {
            "state_id": self.state_id,
            "status": self.status,
            "generation": self.generation,
            "active_tasks": self.active_tasks,
            "trace_id": self.trace_id,
            "updated_at": self.updated_at,
            "version": self.version,
            "integrity_hash": self.integrity_hash,
        }

    def with_integrity_hash(self) -> "RuntimeState":
        """Return a state snapshot with deterministic integrity hash."""
        payload = self.to_payload()
        payload["integrity_hash"] = ""
        return RuntimeState(
            state_id=self.state_id,
            status=self.status,
            generation=self.generation,
            active_tasks=self.active_tasks,
            trace_id=self.trace_id,
            updated_at=self.updated_at,
            version=self.version,
            integrity_hash=stable_checksum(payload),
        )


@dataclass(frozen=True)
class RuntimeTask:
    """Immutable scheduled runtime task."""

    task_name: str
    payload: dict[str, object]
    trace_id: str = ""
    status: str = TASK_PENDING
    task_id: str = field(default_factory=lambda: str(uuid4()))
    scheduled_at: str = field(default_factory=utc_now)
    version: str = "1.0.0"
    integrity_hash: str = ""

    def to_payload(self) -> dict[str, object]:
        """Return deterministic task payload."""
        return {
            "task_id": self.task_id,
            "task_name": self.task_name,
            "payload": self.payload,
            "trace_id": self.trace_id,
            "status": self.status,
            "scheduled_at": self.scheduled_at,
            "version": self.version,
            "integrity_hash": self.integrity_hash,
        }

    def with_integrity_hash(self) -> "RuntimeTask":
        """Return a task with deterministic integrity hash."""
        payload = self.to_payload()
        payload["integrity_hash"] = ""
        return RuntimeTask(
            task_id=self.task_id,
            task_name=self.task_name,
            payload=self.payload,
            trace_id=self.trace_id,
            status=self.status,
            scheduled_at=self.scheduled_at,
            version=self.version,
            integrity_hash=stable_checksum(payload),
        )
