"""Public interface contracts for CognitiveContextRepository."""

from typing import Protocol


class CognitiveContextRepositoryInterface(Protocol):
    def build_context(self, *args: object, **kwargs: object) -> object:
        """build_context contract."""
        ...

    def load_context(self, *args: object, **kwargs: object) -> object:
        """load_context contract."""
        ...

    def validate_context(self, *args: object, **kwargs: object) -> object:
        """validate_context contract."""
        ...

    def archive_context(self, *args: object, **kwargs: object) -> object:
        """archive_context contract."""
        ...

    def get_context(self, *args: object, **kwargs: object) -> object:
        """get_context contract."""
        ...

    def context_exists(self, *args: object, **kwargs: object) -> object:
        """context_exists contract."""
        ...

