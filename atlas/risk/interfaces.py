"""Public interface contracts for RiskRepository."""

from typing import Protocol


class RiskRepositoryInterface(Protocol):
    def calculate_risk(self, *args: object, **kwargs: object) -> object:
        """calculate_risk contract."""
        ...

    def get_risk(self, *args: object, **kwargs: object) -> object:
        """get_risk contract."""
        ...

    def validate_risk(self, *args: object, **kwargs: object) -> object:
        """validate_risk contract."""
        ...

    def archive_risk(self, *args: object, **kwargs: object) -> object:
        """archive_risk contract."""
        ...

    def risk_available(self, *args: object, **kwargs: object) -> object:
        """risk_available contract."""
        ...

    def load_risk_snapshot(self, *args: object, **kwargs: object) -> object:
        """load_risk_snapshot contract."""
        ...

