"""Public interface contracts for MarketRepository."""

from typing import Protocol


class MarketRepositoryInterface(Protocol):
    def load_market_snapshot(self, *args: object, **kwargs: object) -> object:
        """load_market_snapshot contract."""
        ...

    def save_market_snapshot(self, *args: object, **kwargs: object) -> object:
        """save_market_snapshot contract."""
        ...

    def get_market_data(self, *args: object, **kwargs: object) -> object:
        """get_market_data contract."""
        ...

    def list_assets(self, *args: object, **kwargs: object) -> object:
        """list_assets contract."""
        ...

    def validate_market_data(self, *args: object, **kwargs: object) -> object:
        """validate_market_data contract."""
        ...

    def archive_market_snapshot(self, *args: object, **kwargs: object) -> object:
        """archive_market_snapshot contract."""
        ...

    def market_available(self, *args: object, **kwargs: object) -> object:
        """market_available contract."""
        ...

