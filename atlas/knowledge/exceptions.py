"""Typed repository exceptions."""

from atlas.core.exceptions import AtlasException, AtlasValidationError, AtlasStorageError

class KnowledgeError(AtlasException):
    """Typed KnowledgeError."""

class KnowledgeValidationError(AtlasException):
    """Typed KnowledgeValidationError."""

class KnowledgeStorageError(AtlasException):
    """Typed KnowledgeStorageError."""

class KnowledgeNotFound(AtlasException):
    """Typed KnowledgeNotFound."""
