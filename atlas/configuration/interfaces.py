"""Public interface contracts for ConfigurationRepository."""

from typing import Protocol


class ConfigurationRepositoryInterface(Protocol):
    def load_configuration(self, *args: object, **kwargs: object) -> object:
        """load_configuration contract."""
        ...

    def save_configuration(self, *args: object, **kwargs: object) -> object:
        """save_configuration contract."""
        ...

    def validate_configuration(self, *args: object, **kwargs: object) -> object:
        """validate_configuration contract."""
        ...

    def get_configuration(self, *args: object, **kwargs: object) -> object:
        """get_configuration contract."""
        ...

    def reload_configuration(self, *args: object, **kwargs: object) -> object:
        """reload_configuration contract."""
        ...

    def archive_configuration(self, *args: object, **kwargs: object) -> object:
        """archive_configuration contract."""
        ...

    def configuration_exists(self, *args: object, **kwargs: object) -> object:
        """configuration_exists contract."""
        ...

