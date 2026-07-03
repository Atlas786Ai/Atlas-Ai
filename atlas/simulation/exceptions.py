"""Typed repository exceptions."""

from atlas.core.exceptions import AtlasException, AtlasValidationError, AtlasStorageError

class SimulationError(AtlasException):
    """Typed SimulationError."""

class SimulationValidationError(AtlasException):
    """Typed SimulationValidationError."""

class SimulationStorageError(AtlasException):
    """Typed SimulationStorageError."""

class SimulationNotFound(AtlasException):
    """Typed SimulationNotFound."""
