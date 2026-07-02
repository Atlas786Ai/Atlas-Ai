"""Typed repository exceptions."""

from atlas.core.exceptions import AtlasException, AtlasValidationError, AtlasStorageError

class PortfolioError(AtlasException):
    """Typed PortfolioError."""

class PortfolioValidationError(AtlasException):
    """Typed PortfolioValidationError."""

class PortfolioStorageError(AtlasException):
    """Typed PortfolioStorageError."""

class PortfolioNotFound(AtlasException):
    """Typed PortfolioNotFound."""
