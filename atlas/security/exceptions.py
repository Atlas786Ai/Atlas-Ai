"""Typed repository exceptions."""

from atlas.core.exceptions import AtlasException, AtlasValidationError, AtlasStorageError

class SecurityError(AtlasException):
    """Typed SecurityError."""

class SecurityValidationError(AtlasException):
    """Typed SecurityValidationError."""

class SecurityStorageError(AtlasException):
    """Typed SecurityStorageError."""

class SecurityNotFound(AtlasException):
    """Typed SecurityNotFound."""
