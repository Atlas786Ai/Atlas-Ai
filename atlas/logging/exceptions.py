"""Typed repository exceptions."""

from atlas.core.exceptions import AtlasException, AtlasValidationError, AtlasStorageError

class LoggingError(AtlasException):
    """Typed LoggingError."""

class LoggingValidationError(AtlasException):
    """Typed LoggingValidationError."""

class LoggingStorageError(AtlasException):
    """Typed LoggingStorageError."""

class LoggingNotFound(AtlasException):
    """Typed LoggingNotFound."""
