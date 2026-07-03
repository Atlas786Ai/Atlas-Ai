"""Typed repository exceptions."""

from atlas.core.exceptions import AtlasException, AtlasValidationError, AtlasStorageError

class RuntimeError(AtlasException):
    """Typed RuntimeError."""

class RuntimeValidationError(AtlasException):
    """Typed RuntimeValidationError."""

class RuntimeStorageError(AtlasException):
    """Typed RuntimeStorageError."""

class RuntimeNotFound(AtlasException):
    """Typed RuntimeNotFound."""
