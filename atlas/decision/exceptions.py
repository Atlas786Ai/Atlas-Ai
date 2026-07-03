"""Typed repository exceptions."""

from atlas.core.exceptions import AtlasException, AtlasValidationError, AtlasStorageError

class DecisionError(AtlasException):
    """Typed DecisionError."""

class DecisionValidationError(AtlasException):
    """Typed DecisionValidationError."""

class DecisionStorageError(AtlasException):
    """Typed DecisionStorageError."""

class DecisionNotFound(AtlasException):
    """Typed DecisionNotFound."""
