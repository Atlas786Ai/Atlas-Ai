"""Business service boundary for LoggingRepository.

Module Name: atlas.logging.services
Purpose: Implement deterministic, structured logging for Atlas repositories.
Owner: Atlas Governance
Version: 1.0.0
Dependencies: atlas.repository_base, atlas.logging.models
Architecture Layer: Repository
"""

from atlas.core.exceptions import AtlasValidationError
from atlas.core.models import stable_checksum, utc_now
from atlas.logging.constants import ALLOWED_LOG_LEVELS, REDACTED_VALUE, SENSITIVE_CONTEXT_KEYS
from atlas.logging.models import LogEntry
from atlas.logging.validators import validate_log_payload, validate_payload
from atlas.repository_base import RepositoryBase


class LoggingRepository(RepositoryBase):
    """Frozen Atlas v1.0 repository implementation for structured logs."""

    repository_name = "LoggingRepository"
    public_interfaces = ("log", "debug", "info", "warning", "error", "critical", "archive_logs", "load_logs")
    event_types = ("LogCreated", "LogArchived", "LogRejected")

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        self._log_ids: list[str] = []
        self._archive_ids: list[str] = []

    def log(
        self,
        message: str,
        *,
        level: str = "INFO",
        repository: str = "Atlas",
        context: dict[str, object] | None = None,
        trace_id: str = "",
        key: str | None = None,
    ) -> dict[str, object]:
        """Create, validate, store, and emit a deterministic structured log entry."""
        log_entry = self._coerce_log_entry(
            message=message,
            level=level,
            repository=repository,
            context=context,
            trace_id=trace_id,
        )
        payload = log_entry.to_payload()
        validate_log_payload(payload)
        storage_key = key or log_entry.log_id
        self.archive_record(storage_key, payload)
        if storage_key not in self._log_ids:
            self._log_ids.append(storage_key)
        self.emit_event("LogCreated", {"key": storage_key, "payload": payload}, trace_id=trace_id)
        return payload

    def debug(self, message: str, **kwargs: object) -> dict[str, object]:
        """Record a DEBUG log entry."""
        return self.log(message, level="DEBUG", **kwargs)

    def info(self, message: str, **kwargs: object) -> dict[str, object]:
        """Record an INFO log entry."""
        return self.log(message, level="INFO", **kwargs)

    def warning(self, message: str, **kwargs: object) -> dict[str, object]:
        """Record a WARNING log entry."""
        return self.log(message, level="WARNING", **kwargs)

    def error(self, message: str, **kwargs: object) -> dict[str, object]:
        """Record an ERROR log entry."""
        return self.log(message, level="ERROR", **kwargs)

    def critical(self, message: str, **kwargs: object) -> dict[str, object]:
        """Record a CRITICAL log entry."""
        return self.log(message, level="CRITICAL", **kwargs)

    def archive_logs(self, *, archive_id: str | None = None) -> dict[str, object]:
        """Create a deterministic archive summary for currently tracked logs."""
        logs = self.load_logs()
        payload: dict[str, object] = {
            "archive_id": archive_id or f"logs-{len(self._archive_ids) + 1:06d}",
            "created_at": utc_now(),
            "repository": self.repository_name,
            "log_count": len(logs),
            "log_ids": tuple(self._log_ids),
            "integrity_hash": stable_checksum(logs),
            "version": "1.0.0",
        }
        validate_payload(payload)
        self.archive_record(str(payload["archive_id"]), payload)
        self._archive_ids.append(str(payload["archive_id"]))
        self.emit_event("LogArchived", {"key": str(payload["archive_id"]), "payload": payload})
        return payload

    def load_logs(self, *, level: str | None = None, repository: str | None = None) -> tuple[dict[str, object], ...]:
        """Load tracked log entries in their deterministic creation order."""
        normalized_level = level.upper() if level else None
        if normalized_level is not None and normalized_level not in ALLOWED_LOG_LEVELS:
            raise AtlasValidationError("invalid log level", context={"level": level, "allowed": ALLOWED_LOG_LEVELS})
        logs: list[dict[str, object]] = []
        for log_id in self._log_ids:
            record = self.storage.read(log_id)
            payload = record["payload"]
            validate_log_payload(payload)
            if normalized_level is not None and payload["level"] != normalized_level:
                continue
            if repository is not None and payload["repository"] != repository:
                continue
            logs.append(payload)
        return tuple(logs)

    def _coerce_log_entry(
        self,
        *,
        message: str,
        level: str,
        repository: str,
        context: dict[str, object] | None,
        trace_id: str,
    ) -> LogEntry:
        if not isinstance(message, str) or not message:
            raise AtlasValidationError("log message must be a non-empty string")
        if not isinstance(repository, str) or not repository:
            raise AtlasValidationError("log repository must be a non-empty string")
        if not isinstance(trace_id, str):
            raise AtlasValidationError("trace_id must be a string")
        normalized_level = level.upper()
        if normalized_level not in ALLOWED_LOG_LEVELS:
            raise AtlasValidationError("invalid log level", context={"level": level, "allowed": ALLOWED_LOG_LEVELS})
        redacted_context = self._redact_context(context or {})
        return LogEntry(
            repository=repository,
            level=normalized_level,
            message=message,
            context=redacted_context,
            trace_id=trace_id,
        ).with_integrity_hash()

    def _redact_context(self, context: dict[str, object]) -> dict[str, object]:
        if not isinstance(context, dict):
            raise AtlasValidationError("log context must be a dictionary")
        redacted: dict[str, object] = {}
        for key in sorted(context):
            value = context[key]
            if any(marker in key.lower() for marker in SENSITIVE_CONTEXT_KEYS):
                redacted[key] = REDACTED_VALUE
            elif isinstance(value, dict):
                redacted[key] = self._redact_context(value)
            else:
                redacted[key] = value
        return redacted
