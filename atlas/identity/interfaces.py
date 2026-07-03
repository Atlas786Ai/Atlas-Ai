"""Public interface contracts for IdentityRepository."""

from typing import Protocol


class IdentityRepositoryInterface(Protocol):
    def create_identity(self, *args: object, **kwargs: object) -> object:
        """create_identity contract."""
        ...

    def load_identity(self, *args: object, **kwargs: object) -> object:
        """load_identity contract."""
        ...

    def save_identity(self, *args: object, **kwargs: object) -> object:
        """save_identity contract."""
        ...

    def validate_identity(self, *args: object, **kwargs: object) -> object:
        """validate_identity contract."""
        ...

    def archive_identity(self, *args: object, **kwargs: object) -> object:
        """archive_identity contract."""
        ...

    def get_identity(self, *args: object, **kwargs: object) -> object:
        """get_identity contract."""
        ...

    def identity_exists(self, *args: object, **kwargs: object) -> object:
        """identity_exists contract."""
        ...

