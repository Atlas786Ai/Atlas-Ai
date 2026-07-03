"""Public interface contracts for AnalyticsRepository."""

from typing import Protocol


class AnalyticsRepositoryInterface(Protocol):
    def calculate_metrics(self, *args: object, **kwargs: object) -> object:
        """calculate_metrics contract."""
        ...

    def generate_report(self, *args: object, **kwargs: object) -> object:
        """generate_report contract."""
        ...

    def generate_dashboard(self, *args: object, **kwargs: object) -> object:
        """generate_dashboard contract."""
        ...

    def load_analytics(self, *args: object, **kwargs: object) -> object:
        """load_analytics contract."""
        ...

    def archive_analytics(self, *args: object, **kwargs: object) -> object:
        """archive_analytics contract."""
        ...

    def validate_analytics(self, *args: object, **kwargs: object) -> object:
        """validate_analytics contract."""
        ...

    def get_statistics(self, *args: object, **kwargs: object) -> object:
        """get_statistics contract."""
        ...

