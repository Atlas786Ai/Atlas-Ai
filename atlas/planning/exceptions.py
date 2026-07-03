"""Typed repository exceptions."""

from atlas.core.exceptions import AtlasException, AtlasValidationError, AtlasStorageError

class PlanningError(AtlasException):
    """Typed PlanningError."""

class PlanningValidationError(AtlasException):
    """Typed PlanningValidationError."""

class PlanningStorageError(AtlasException):
    """Typed PlanningStorageError."""

class PlanningNotFound(AtlasException):
    """Typed PlanningNotFound."""
