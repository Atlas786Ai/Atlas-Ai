"""Typed repository exceptions."""

from atlas.core.exceptions import AtlasException, AtlasValidationError, AtlasStorageError

class ExecutionError(AtlasException):
    """Typed ExecutionError."""

class ExecutionValidationError(AtlasException):
    """Typed ExecutionValidationError."""

class ExecutionStorageError(AtlasException):
    """Typed ExecutionStorageError."""

class ExecutionNotFound(AtlasException):
    """Typed ExecutionNotFound."""
