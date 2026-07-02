"""Typed repository exceptions."""

from atlas.core.exceptions import AtlasException, AtlasValidationError, AtlasStorageError

class RiskError(AtlasException):
    """Typed RiskError."""

class RiskValidationError(AtlasException):
    """Typed RiskValidationError."""

class RiskStorageError(AtlasException):
    """Typed RiskStorageError."""

class RiskNotFound(AtlasException):
    """Typed RiskNotFound."""
