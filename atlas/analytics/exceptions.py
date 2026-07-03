"""Typed repository exceptions."""

from atlas.core.exceptions import AtlasException, AtlasValidationError, AtlasStorageError

class AnalyticsError(AtlasException):
    """Typed AnalyticsError."""

class AnalyticsValidationError(AtlasException):
    """Typed AnalyticsValidationError."""

class AnalyticsStorageError(AtlasException):
    """Typed AnalyticsStorageError."""

class AnalyticsNotFound(AtlasException):
    """Typed AnalyticsNotFound."""
