from atlas.core.exceptions import AtlasValidationError
from atlas.logging.constants import REDACTED_VALUE
from atlas.logging.services import LoggingRepository


def test_logging_repository_creates_structured_immutable_log() -> None:
    repository = LoggingRepository()

    payload = repository.info(
        "configuration loaded",
        repository="ConfigurationRepository",
        context={"path": "runtime", "token": "secret-value"},
        trace_id="trace-001",
    )

    assert payload["level"] == "INFO"
    assert payload["repository"] == "ConfigurationRepository"
    assert payload["context"]["token"] == REDACTED_VALUE
    assert payload["trace_id"] == "trace-001"
    assert payload["integrity_hash"]
    assert repository.load_logs() == (payload,)
    assert repository._events[-1].event_type == "LogCreated"
    assert repository._events[-1].payload["payload"]["level"] == "INFO"


def test_logging_repository_filters_and_archives_logs() -> None:
    repository = LoggingRepository()
    info = repository.info("started", repository="RuntimeRepository")
    error = repository.error("failed", repository="RuntimeRepository")
    repository.debug("noise", repository="MonitoringRepository")

    assert repository.load_logs(level="ERROR") == (error,)
    assert repository.load_logs(repository="RuntimeRepository") == (info, error)

    archive = repository.archive_logs(archive_id="daily-logs")

    assert archive["archive_id"] == "daily-logs"
    assert archive["log_count"] == 3
    assert archive["integrity_hash"]


def test_logging_repository_rejects_invalid_payloads() -> None:
    repository = LoggingRepository()

    try:
        repository.log("bad level", level="VERBOSE")
    except AtlasValidationError as exc:
        assert exc.context["level"] == "VERBOSE"
    else:
        raise AssertionError("invalid log level was accepted")

    try:
        repository.info("bad context", context="not-a-dict")
    except AtlasValidationError:
        pass
    else:
        raise AssertionError("invalid log context was accepted")
