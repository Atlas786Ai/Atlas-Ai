"""AuditRepository tests for Atlas v1.0."""

from atlas.audit.services import AuditRepository
from atlas.core.exceptions import AtlasValidationError


def test_audit_repository_records_and_loads_immutable_event(tmp_path) -> None:
    repository = AuditRepository(storage_root=tmp_path)

    event = repository.record_event(
        "ConfigurationUpdated",
        "ConfigurationRepository",
        "save_configuration",
        "ConfigurationRepository",
        {"configuration_id": "cfg-001"},
        trace_id="trace-audit-001",
        key="audit-001",
    )

    loaded = repository.load_event("audit-001")

    assert loaded == event
    assert loaded["trace_id"] == "trace-audit-001"
    assert loaded["integrity_hash"]
    assert repository.audit_available()["audit_count"] == 1


def test_audit_repository_searches_and_reconstructs_trace(tmp_path) -> None:
    repository = AuditRepository(storage_root=tmp_path)
    first = repository.record_event("BootStarted", "RuntimeRepository", "boot", "RuntimeRepository", {}, trace_id="trace-boot", key="audit-001")
    second = repository.record_event("RuntimeReady", "RuntimeRepository", "ready", "RuntimeRepository", {}, trace_id="trace-boot", key="audit-002")
    repository.record_event("LogCreated", "LoggingRepository", "log", "LoggingRepository", {}, trace_id="trace-log", key="audit-003")

    assert repository.search_events(source_repository="RuntimeRepository") == (first, second)
    assert repository.get_trace("trace-boot") == (first, second)


def test_audit_repository_validates_and_archives_history(tmp_path) -> None:
    repository = AuditRepository(storage_root=tmp_path)
    event = repository.record_event("SecurityEvent", "SecurityRepository", "authorize", "SecurityRepository", {"allowed": True}, trace_id="trace-sec", key="audit-001")

    assert repository.validate_audit(event) is True
    assert repository.validate_audit() is True

    archive = repository.archive_audit(archive_id="audit-daily")

    assert archive["payload"]["archive_id"] == "audit-daily"
    assert archive["payload"]["audit_count"] == 1
    assert archive["payload"]["integrity_hash"]


def test_audit_repository_rejects_tampered_event(tmp_path) -> None:
    repository = AuditRepository(storage_root=tmp_path)
    event = repository.record_event("RiskChecked", "RiskRepository", "check", "RiskRepository", {"risk": "low"}, trace_id="trace-risk", key="audit-001")
    tampered = dict(event)
    tampered["payload"] = {"risk": "high"}

    try:
        repository.validate_audit(tampered)
    except AtlasValidationError as exc:
        assert exc.context["audit_id"] == event["audit_id"]
    else:
        raise AssertionError("tampered audit event was accepted")
