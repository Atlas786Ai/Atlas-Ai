"""Public interface contracts for KnowledgeRepository."""

from typing import Protocol


class KnowledgeRepositoryInterface(Protocol):
    def add_knowledge(self, *args: object, **kwargs: object) -> object:
        """add_knowledge contract."""
        ...

    def update_knowledge(self, *args: object, **kwargs: object) -> object:
        """update_knowledge contract."""
        ...

    def remove_knowledge(self, *args: object, **kwargs: object) -> object:
        """remove_knowledge contract."""
        ...

    def get_knowledge(self, *args: object, **kwargs: object) -> object:
        """get_knowledge contract."""
        ...

    def search(self, *args: object, **kwargs: object) -> object:
        """search contract."""
        ...

    def semantic_search(self, *args: object, **kwargs: object) -> object:
        """semantic_search contract."""
        ...

    def list_related(self, *args: object, **kwargs: object) -> object:
        """list_related contract."""
        ...

    def validate_knowledge(self, *args: object, **kwargs: object) -> object:
        """validate_knowledge contract."""
        ...

    def archive_knowledge(self, *args: object, **kwargs: object) -> object:
        """archive_knowledge contract."""
        ...

