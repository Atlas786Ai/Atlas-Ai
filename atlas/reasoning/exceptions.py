"""Typed repository exceptions."""

from atlas.core.exceptions import AtlasException, AtlasValidationError, AtlasStorageError

class ReasoningError(AtlasException):
    """Typed ReasoningError."""

class ReasoningValidationError(AtlasException):
    """Typed ReasoningValidationError."""

class ReasoningStorageError(AtlasException):
    """Typed ReasoningStorageError."""

class ReasoningNotFound(AtlasException):
    """Typed ReasoningNotFound."""
