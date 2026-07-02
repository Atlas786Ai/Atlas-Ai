"""Public interface contracts for MissionRepository."""

from typing import Protocol


class MissionRepositoryInterface(Protocol):
    def create_mission(self, *args: object, **kwargs: object) -> object:
        """create_mission contract."""
        ...

    def load_mission(self, *args: object, **kwargs: object) -> object:
        """load_mission contract."""
        ...

    def save_mission(self, *args: object, **kwargs: object) -> object:
        """save_mission contract."""
        ...

    def validate_mission(self, *args: object, **kwargs: object) -> object:
        """validate_mission contract."""
        ...

    def archive_mission(self, *args: object, **kwargs: object) -> object:
        """archive_mission contract."""
        ...

    def get_current_mission(self, *args: object, **kwargs: object) -> object:
        """get_current_mission contract."""
        ...

    def mission_exists(self, *args: object, **kwargs: object) -> object:
        """mission_exists contract."""
        ...

    def get_mission_version(self, *args: object, **kwargs: object) -> object:
        """get_mission_version contract."""
        ...

