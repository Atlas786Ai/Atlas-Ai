"""Typed repository exceptions."""

from atlas.core.exceptions import AtlasException, AtlasValidationError, AtlasStorageError

class MissionError(AtlasException):
    """Typed MissionError."""

class MissionValidationError(AtlasException):
    """Typed MissionValidationError."""

class MissionStorageError(AtlasException):
    """Typed MissionStorageError."""

class MissionNotFound(AtlasException):
    """Typed MissionNotFound."""
