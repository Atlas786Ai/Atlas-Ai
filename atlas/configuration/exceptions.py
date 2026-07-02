"""Typed repository exceptions."""

from atlas.core.exceptions import AtlasException, AtlasValidationError, AtlasStorageError

class ConfigurationError(AtlasException):
    """Typed ConfigurationError."""

class ConfigurationValidationError(AtlasException):
    """Typed ConfigurationValidationError."""

class ConfigurationStorageError(AtlasException):
    """Typed ConfigurationStorageError."""

class ConfigurationNotFound(AtlasException):
    """Typed ConfigurationNotFound."""
