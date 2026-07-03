"""Typed repository exceptions."""

from atlas.core.exceptions import AtlasException, AtlasValidationError, AtlasStorageError

class CognitiveContextError(AtlasException):
    """Typed CognitiveContextError."""

class CognitiveContextValidationError(AtlasException):
    """Typed CognitiveContextValidationError."""

class CognitiveContextStorageError(AtlasException):
    """Typed CognitiveContextStorageError."""

class CognitiveContextNotFound(AtlasException):
    """Typed CognitiveContextNotFound."""
