"""Public interface contracts for PlanningRepository."""

from typing import Protocol


class PlanningRepositoryInterface(Protocol):
    def create_plan(self, *args: object, **kwargs: object) -> object:
        """create_plan contract."""
        ...

    def load_plan(self, *args: object, **kwargs: object) -> object:
        """load_plan contract."""
        ...

    def validate_plan(self, *args: object, **kwargs: object) -> object:
        """validate_plan contract."""
        ...

    def optimize_plan(self, *args: object, **kwargs: object) -> object:
        """optimize_plan contract."""
        ...

    def estimate_resources(self, *args: object, **kwargs: object) -> object:
        """estimate_resources contract."""
        ...

    def archive_plan(self, *args: object, **kwargs: object) -> object:
        """archive_plan contract."""
        ...

    def get_plan(self, *args: object, **kwargs: object) -> object:
        """get_plan contract."""
        ...

