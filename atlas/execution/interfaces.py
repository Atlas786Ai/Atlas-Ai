"""Public interface contracts for ExecutionRepository."""

from typing import Protocol


class ExecutionRepositoryInterface(Protocol):
    def execute(self, *args: object, **kwargs: object) -> object:
        """execute contract."""
        ...

    def pause_execution(self, *args: object, **kwargs: object) -> object:
        """pause_execution contract."""
        ...

    def resume_execution(self, *args: object, **kwargs: object) -> object:
        """resume_execution contract."""
        ...

    def cancel_execution(self, *args: object, **kwargs: object) -> object:
        """cancel_execution contract."""
        ...

    def rollback_execution(self, *args: object, **kwargs: object) -> object:
        """rollback_execution contract."""
        ...

    def get_execution(self, *args: object, **kwargs: object) -> object:
        """get_execution contract."""
        ...

    def validate_execution(self, *args: object, **kwargs: object) -> object:
        """validate_execution contract."""
        ...

