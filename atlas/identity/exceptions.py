"""Typed repository exceptions."""

from atlas.core.exceptions import AtlasException, AtlasValidationError, AtlasStorageError

class IdentityError(AtlasException):
    """Typed IdentityError."""

class IdentityValidationError(AtlasException):
    """Typed IdentityValidationError."""

class IdentityStorageError(AtlasException):
    """Typed IdentityStorageError."""

class IdentityNotFound(AtlasException):
    """Typed IdentityNotFound."""
