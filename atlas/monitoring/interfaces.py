"""Public interface contracts for MonitoringRepository."""

from typing import Protocol


class MonitoringRepositoryInterface(Protocol):
    def collect_metrics(self, *args: object, **kwargs: object) -> object:
        """collect_metrics contract."""
        ...

    def get_health(self, *args: object, **kwargs: object) -> object:
        """get_health contract."""
        ...

    def get_status(self, *args: object, **kwargs: object) -> object:
        """get_status contract."""
        ...

    def generate_alert(self, *args: object, **kwargs: object) -> object:
        """generate_alert contract."""
        ...

    def archive_monitoring(self, *args: object, **kwargs: object) -> object:
        """archive_monitoring contract."""
        ...

    def validate_monitoring(self, *args: object, **kwargs: object) -> object:
        """validate_monitoring contract."""
        ...

    def load_snapshot(self, *args: object, **kwargs: object) -> object:
        """load_snapshot contract."""
        ...

