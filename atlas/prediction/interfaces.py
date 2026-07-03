"""Public interface contracts for PredictionRepository."""

from typing import Protocol


class PredictionRepositoryInterface(Protocol):
    def create_prediction(self, *args: object, **kwargs: object) -> object:
        """create_prediction contract."""
        ...

    def load_prediction(self, *args: object, **kwargs: object) -> object:
        """load_prediction contract."""
        ...

    def validate_prediction(self, *args: object, **kwargs: object) -> object:
        """validate_prediction contract."""
        ...

    def compare_prediction(self, *args: object, **kwargs: object) -> object:
        """compare_prediction contract."""
        ...

    def archive_prediction(self, *args: object, **kwargs: object) -> object:
        """archive_prediction contract."""
        ...

    def get_prediction(self, *args: object, **kwargs: object) -> object:
        """get_prediction contract."""
        ...

    def list_predictions(self, *args: object, **kwargs: object) -> object:
        """list_predictions contract."""
        ...

