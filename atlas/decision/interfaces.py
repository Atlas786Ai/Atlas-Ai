"""Public interface contracts for DecisionRepository."""

from typing import Protocol


class DecisionRepositoryInterface(Protocol):
    def evaluate_decision(self, *args: object, **kwargs: object) -> object:
        """evaluate_decision contract."""
        ...

    def select_plan(self, *args: object, **kwargs: object) -> object:
        """select_plan contract."""
        ...

    def validate_decision(self, *args: object, **kwargs: object) -> object:
        """validate_decision contract."""
        ...

    def archive_decision(self, *args: object, **kwargs: object) -> object:
        """archive_decision contract."""
        ...

    def load_decision(self, *args: object, **kwargs: object) -> object:
        """load_decision contract."""
        ...

    def get_decision(self, *args: object, **kwargs: object) -> object:
        """get_decision contract."""
        ...

