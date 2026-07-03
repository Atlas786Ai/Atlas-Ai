"""Public interface contracts for RuntimeRepository."""

from typing import Protocol


class RuntimeRepositoryInterface(Protocol):
    def start_runtime(self, *args: object, **kwargs: object) -> object:
        """start_runtime contract."""
        ...

    def shutdown_runtime(self, *args: object, **kwargs: object) -> object:
        """shutdown_runtime contract."""
        ...

    def restart_runtime(self, *args: object, **kwargs: object) -> object:
        """restart_runtime contract."""
        ...

    def get_runtime_state(self, *args: object, **kwargs: object) -> object:
        """get_runtime_state contract."""
        ...

    def schedule_task(self, *args: object, **kwargs: object) -> object:
        """schedule_task contract."""
        ...

    def validate_runtime(self, *args: object, **kwargs: object) -> object:
        """validate_runtime contract."""
        ...

    def archive_runtime_state(self, *args: object, **kwargs: object) -> object:
        """archive_runtime_state contract."""
        ...

