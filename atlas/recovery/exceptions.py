"""Typed repository exceptions."""

from atlas.core.exceptions import AtlasException, AtlasValidationError, AtlasStorageError

class RecoveryError(AtlasException):
    """Typed RecoveryError."""

class RecoveryValidationError(AtlasException):
    """Typed RecoveryValidationError."""

class RecoveryStorageError(AtlasException):
    """Typed RecoveryStorageError."""

class RecoveryNotFound(AtlasException):
    """Typed RecoveryNotFound."""
