"""Typed repository exceptions."""

from atlas.core.exceptions import AtlasException, AtlasValidationError, AtlasStorageError

class MemoryError(AtlasException):
    """Typed MemoryError."""

class MemoryValidationError(AtlasException):
    """Typed MemoryValidationError."""

class MemoryStorageError(AtlasException):
    """Typed MemoryStorageError."""

class MemoryNotFound(AtlasException):
    """Typed MemoryNotFound."""
