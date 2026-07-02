"""Typed repository exceptions."""

from atlas.core.exceptions import AtlasException, AtlasValidationError, AtlasStorageError

class AuditError(AtlasException):
    """Typed AuditError."""

class AuditValidationError(AtlasException):
    """Typed AuditValidationError."""

class AuditStorageError(AtlasException):
    """Typed AuditStorageError."""

class AuditNotFound(AtlasException):
    """Typed AuditNotFound."""
