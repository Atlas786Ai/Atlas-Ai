"""Public interface contracts for LoggingRepository."""

from typing import Protocol


class LoggingRepositoryInterface(Protocol):
    def log(self, *args: object, **kwargs: object) -> object:
        """log contract."""
        ...

    def debug(self, *args: object, **kwargs: object) -> object:
        """debug contract."""
        ...

    def info(self, *args: object, **kwargs: object) -> object:
        """info contract."""
        ...

    def warning(self, *args: object, **kwargs: object) -> object:
        """warning contract."""
        ...

    def error(self, *args: object, **kwargs: object) -> object:
        """error contract."""
        ...

    def critical(self, *args: object, **kwargs: object) -> object:
        """critical contract."""
        ...

    def archive_logs(self, *args: object, **kwargs: object) -> object:
        """archive_logs contract."""
        ...

    def load_logs(self, *args: object, **kwargs: object) -> object:
        """load_logs contract."""
        ...

