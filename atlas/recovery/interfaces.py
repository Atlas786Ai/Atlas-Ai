"""Public interface contracts for RecoveryRepository."""

from typing import Protocol


class RecoveryRepositoryInterface(Protocol):
    def recover(self, *args: object, **kwargs: object) -> object:
        """recover contract."""
        ...

    def rollback(self, *args: object, **kwargs: object) -> object:
        """rollback contract."""
        ...

    def restore_snapshot(self, *args: object, **kwargs: object) -> object:
        """restore_snapshot contract."""
        ...

    def restart_workflow(self, *args: object, **kwargs: object) -> object:
        """restart_workflow contract."""
        ...

    def validate_recovery(self, *args: object, **kwargs: object) -> object:
        """validate_recovery contract."""
        ...

    def archive_recovery(self, *args: object, **kwargs: object) -> object:
        """archive_recovery contract."""
        ...

    def get_recovery(self, *args: object, **kwargs: object) -> object:
        """get_recovery contract."""
        ...

