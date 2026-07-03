"""Typed repository exceptions."""

from atlas.core.exceptions import AtlasException, AtlasValidationError, AtlasStorageError

class PredictionError(AtlasException):
    """Typed PredictionError."""

class PredictionValidationError(AtlasException):
    """Typed PredictionValidationError."""

class PredictionStorageError(AtlasException):
    """Typed PredictionStorageError."""

class PredictionNotFound(AtlasException):
    """Typed PredictionNotFound."""
