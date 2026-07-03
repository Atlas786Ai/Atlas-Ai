"""Public interface contracts for SimulationRepository."""

from typing import Protocol


class SimulationRepositoryInterface(Protocol):
    def create_simulation(self, *args: object, **kwargs: object) -> object:
        """create_simulation contract."""
        ...

    def run_simulation(self, *args: object, **kwargs: object) -> object:
        """run_simulation contract."""
        ...

    def stop_simulation(self, *args: object, **kwargs: object) -> object:
        """stop_simulation contract."""
        ...

    def archive_simulation(self, *args: object, **kwargs: object) -> object:
        """archive_simulation contract."""
        ...

    def get_simulation(self, *args: object, **kwargs: object) -> object:
        """get_simulation contract."""
        ...

    def compare_simulations(self, *args: object, **kwargs: object) -> object:
        """compare_simulations contract."""
        ...

    def validate_simulation(self, *args: object, **kwargs: object) -> object:
        """validate_simulation contract."""
        ...

