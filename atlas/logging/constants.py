"""Constants for LoggingRepository."""

ALLOWED_LOG_LEVELS = ("DEBUG", "INFO", "NOTICE", "WARNING", "ERROR", "CRITICAL")
SENSITIVE_CONTEXT_KEYS = (
    "api_key",
    "authorization",
    "credential",
    "password",
    "private_key",
    "secret",
    "token",
)
REDACTED_VALUE = "[REDACTED]"
