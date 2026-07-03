"""RuntimeRepository service tests for Atlas v1.0."""

from atlas.core.exceptions import AtlasValidationError
from atlas.runtime.constants import RUNTIME_RUNNING, RUNTIME_STOPPED
from atlas.runtime.services import RuntimeRepository


def test_runtime_repository_starts_and_validates_state(tmp_path) -> None:
    repository = RuntimeRepository(storage_root=tmp_path)

    record = repository.start_runtime(trace_id="trace-runtime-001", key="runtime-start")
    state = repository.get_runtime_state()

    assert record["payload"] == state
    assert state["status"] == RUNTIME_RUNNING
    assert state["trace_id"] == "trace-runtime-001"
    assert state["integrity_hash"]
    assert repository.validate_runtime(state) is True


def test_runtime_repository_schedules_tasks_only_when_running(tmp_path) -> None:
    repository = RuntimeRepository(storage_root=tmp_path)

    try:
        repository.schedule_task("collect-health", {"component": "Runtime"})
    except AtlasValidationError as exc:
        assert exc.context["status"] == RUNTIME_STOPPED
    else:
        raise AssertionError("task scheduled while runtime was stopped")

    repository.start_runtime(trace_id="trace-runtime-002")
    task_record = repository.schedule_task("collect-health", {"component": "Runtime"}, trace_id="trace-runtime-002", key="task-001")
    state = repository.get_runtime_state()

    assert task_record["payload"]["task_name"] == "collect-health"
    assert task_record["payload"]["status"] == "Scheduled"
    assert state["active_tasks"] == ("task-001",)


def test_runtime_repository_restarts_shutdowns_and_archives(tmp_path) -> None:
    repository = RuntimeRepository(storage_root=tmp_path)
    repository.start_runtime(trace_id="trace-runtime-003")
    restarted = repository.restart_runtime(trace_id="trace-runtime-003")

    assert restarted["payload"]["status"] == RUNTIME_RUNNING

    stopped = repository.shutdown_runtime(trace_id="trace-runtime-003")
    archive = repository.archive_runtime_state(archive_id="runtime-daily")

    assert stopped["payload"]["status"] == RUNTIME_STOPPED
    assert archive["payload"]["archive_id"] == "runtime-daily"
    assert archive["payload"]["state"]["status"] == RUNTIME_STOPPED
    assert archive["payload"]["integrity_hash"]


def test_runtime_repository_rejects_tampered_state(tmp_path) -> None:
    repository = RuntimeRepository(storage_root=tmp_path)
    repository.start_runtime()
    state = repository.get_runtime_state()
    tampered = dict(state)
    tampered["status"] = RUNTIME_STOPPED

    try:
        repository.validate_runtime(tampered)
    except AtlasValidationError:
        pass
    else:
        raise AssertionError("tampered runtime state was accepted")
