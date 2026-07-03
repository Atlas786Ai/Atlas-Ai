"""Typed repository exceptions."""

from atlas.core.exceptions import AtlasException, AtlasValidationError, AtlasStorageError

class MarketError(AtlasException):
    """Typed MarketError."""

class MarketValidationError(AtlasException):
    """Typed MarketValidationError."""

class MarketStorageError(AtlasException):
    """Typed MarketStorageError."""

class MarketNotFound(AtlasException):
    """Typed MarketNotFound."""
