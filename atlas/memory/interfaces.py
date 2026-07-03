"""Public interface contracts for MemoryRepository."""

from typing import Protocol


class MemoryRepositoryInterface(Protocol):
    def store_memory(self, *args: object, **kwargs: object) -> object:
        """store_memory contract."""
        ...

    def update_memory(self, *args: object, **kwargs: object) -> object:
        """update_memory contract."""
        ...

    def get_memory(self, *args: object, **kwargs: object) -> object:
        """get_memory contract."""
        ...

    def search_memory(self, *args: object, **kwargs: object) -> object:
        """search_memory contract."""
        ...

    def contextual_recall(self, *args: object, **kwargs: object) -> object:
        """contextual_recall contract."""
        ...

    def archive_memory(self, *args: object, **kwargs: object) -> object:
        """archive_memory contract."""
        ...

    def delete_memory(self, *args: object, **kwargs: object) -> object:
        """delete_memory contract."""
        ...

    def validate_memory(self, *args: object, **kwargs: object) -> object:
        """validate_memory contract."""
        ...

