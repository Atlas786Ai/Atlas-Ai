"""Typed repository exceptions."""

from atlas.core.exceptions import AtlasException, AtlasValidationError, AtlasStorageError

class MonitoringError(AtlasException):
    """Typed MonitoringError."""

class MonitoringValidationError(AtlasException):
    """Typed MonitoringValidationError."""

class MonitoringStorageError(AtlasException):
    """Typed MonitoringStorageError."""

class MonitoringNotFound(AtlasException):
    """Typed MonitoringNotFound."""
