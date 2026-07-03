"""Business service boundary for RuntimeRepository.

Module Name: atlas.runtime.services
Purpose: Implement deterministic runtime lifecycle and task scheduling state.
Owner: Atlas Governance
Version: 1.0.0
Dependencies: atlas.repository_base, atlas.runtime.models
Architecture Layer: Repository
"""

from pathlib import Path
from typing import Any

from atlas.core.exceptions import AtlasValidationError
from atlas.core.models import stable_checksum, utc_now
from atlas.repository_base import RepositoryBase
from atlas.runtime.constants import RUNTIME_RESTARTING, RUNTIME_RUNNING, RUNTIME_SHUTTING_DOWN, RUNTIME_STOPPED, TASK_SCHEDULED
from atlas.runtime.models import RuntimeState, RuntimeTask
from atlas.runtime.validators import validate_runtime_state_payload, validate_task_payload, verify_integrity


class RuntimeRepository(RepositoryBase):
    """Frozen Atlas v1.0 repository implementation for runtime lifecycle control."""

    repository_name = "RuntimeRepository"
    public_interfaces = (
        "start_runtime",
        "shutdown_runtime",
        "restart_runtime",
        "get_runtime_state",
        "schedule_task",
        "validate_runtime",
        "archive_runtime_state",
    )
    event_types = (
        "RuntimeStarted",
        "RuntimeShutdown",
        "RuntimeRestarted",
        "RuntimeValidated",
        "RuntimeStateArchived",
        "TaskScheduled",
    )

    def __init__(self, storage_root: Path | None = None) -> None:
        super().__init__(storage_root)
        self._state = RuntimeState().with_integrity_hash()
        self._state_ids: list[str] = []
        self._task_ids: list[str] = []

    def start_runtime(self, *, trace_id: str = "", key: str | None = None) -> dict[str, Any]:
        """Transition runtime into Running state and archive the new snapshot."""
        state = self._transition(RUNTIME_RUNNING, trace_id=trace_id)
        record = self._archive_state(state, key=key)
        self.emit_event("RuntimeStarted", {"state_id": state.state_id, "status": state.status}, trace_id=trace_id)
        return record

    def shutdown_runtime(self, *, trace_id: str = "", key: str | None = None) -> dict[str, Any]:
        """Transition runtime through shutdown into Stopped state."""
        self._state = self._transition(RUNTIME_SHUTTING_DOWN, trace_id=trace_id)
        state = self._transition(RUNTIME_STOPPED, trace_id=trace_id)
        record = self._archive_state(state, key=key)
        self.emit_event("RuntimeShutdown", {"state_id": state.state_id, "status": state.status}, trace_id=trace_id)
        return record

    def restart_runtime(self, *, trace_id: str = "", key: str | None = None) -> dict[str, Any]:
        """Perform deterministic restart and return the Running state archive."""
        self._state = self._transition(RUNTIME_RESTARTING, trace_id=trace_id)
        state = self._transition(RUNTIME_RUNNING, trace_id=trace_id)
        record = self._archive_state(state, key=key)
        self.emit_event("RuntimeRestarted", {"state_id": state.state_id, "status": state.status}, trace_id=trace_id)
        return record

    def get_runtime_state(self) -> dict[str, object]:
        """Return the current immutable runtime state payload."""
        payload = self._state.to_payload()
        validate_runtime_state_payload(payload)
        verify_integrity(payload)
        return payload

    def schedule_task(
        self,
        task_name: str,
        payload: dict[str, object] | None = None,
        *,
        trace_id: str = "",
        key: str | None = None,
    ) -> dict[str, Any]:
        """Schedule an immutable runtime task without executing business logic."""
        if self._state.status != RUNTIME_RUNNING:
            raise AtlasValidationError("runtime must be Running before scheduling tasks", context={"status": self._state.status})
        if not isinstance(payload or {}, dict):
            raise AtlasValidationError("task payload must be a dictionary")
        task = RuntimeTask(
            task_name=self._require_text(task_name, "task_name"),
            payload=payload or {},
            trace_id=self._require_optional_text(trace_id, "trace_id"),
            status=TASK_SCHEDULED,
        ).with_integrity_hash()
        task_payload = task.to_payload()
        validate_task_payload(task_payload)
        verify_integrity(task_payload)
        storage_key = key or task.task_id
        record = self.archive_record(storage_key, task_payload)
        self._task_ids.append(storage_key)
        self._state = RuntimeState(
            status=self._state.status,
            generation=self._state.generation + 1,
            active_tasks=tuple(self._task_ids),
            trace_id=trace_id,
        ).with_integrity_hash()
        self.emit_event("TaskScheduled", {"task_id": task.task_id, "task_name": task.task_name}, trace_id=trace_id)
        return record

    def validate_runtime(self, payload: dict[str, object] | None = None) -> bool:
        """Validate supplied or current runtime state integrity."""
        runtime_payload = payload or self.get_runtime_state()
        validate_runtime_state_payload(runtime_payload)
        verify_integrity(runtime_payload)
        self.emit_event("RuntimeValidated", {"state_id": runtime_payload["state_id"], "status": runtime_payload["status"]})
        return True

    def archive_runtime_state(self, *, archive_id: str | None = None) -> dict[str, Any]:
        """Archive the current runtime state with task references."""
        state_payload = self.get_runtime_state()
        archive_payload = {
            "archive_id": archive_id or f"runtime-{len(self._state_ids) + 1:06d}",
            "state": state_payload,
            "task_ids": tuple(self._task_ids),
            "created_at": utc_now(),
            "version": "1.0.0",
            "integrity_hash": stable_checksum({"state": state_payload, "task_ids": tuple(self._task_ids)}),
        }
        key = str(archive_payload["archive_id"])
        record = self.archive_record(key, archive_payload)
        self.emit_event("RuntimeStateArchived", {"archive_id": key, "state_id": state_payload["state_id"]})
        return record

    def _transition(self, status: str, *, trace_id: str) -> RuntimeState:
        return RuntimeState(
            status=status,
            generation=self._state.generation + 1,
            active_tasks=self._state.active_tasks,
            trace_id=self._require_optional_text(trace_id, "trace_id"),
        ).with_integrity_hash()

    def _archive_state(self, state: RuntimeState, *, key: str | None = None) -> dict[str, Any]:
        payload = state.to_payload()
        validate_runtime_state_payload(payload)
        verify_integrity(payload)
        storage_key = key or state.state_id
        record = self.archive_record(storage_key, payload)
        self._state = state
        self._state_ids.append(storage_key)
        return record

    def _require_text(self, value: str, field: str) -> str:
        if not isinstance(value, str) or not value:
            raise AtlasValidationError(f"{field} must be a non-empty string")
        return value

    def _require_optional_text(self, value: str, field: str) -> str:
        if not isinstance(value, str):
            raise AtlasValidationError(f"{field} must be a string")
        return value
