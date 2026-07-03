"""Typed base exceptions for Atlas.

Module Name: atlas.core.exceptions
Purpose: Provide typed, contextual exception base classes.
Owner: Atlas Governance
Version: 1.0.0
Dependencies: None
Architecture Layer: Core
"""

class AtlasException(Exception):
    """Base exception carrying machine-readable context."""

    def __init__(self, message: str, *, context: dict[str, object] | None = None) -> None:
        super().__init__(message)
        self.context = context or {}


class AtlasValidationError(AtlasException):
    """Raised when an Atlas object violates a frozen schema or invariant."""


class AtlasStorageError(AtlasException):
    """Raised when a storage operation fails."""
