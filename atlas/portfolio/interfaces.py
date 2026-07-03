"""Public interface contracts for PortfolioRepository."""

from typing import Protocol


class PortfolioRepositoryInterface(Protocol):
    def create_portfolio(self, *args: object, **kwargs: object) -> object:
        """create_portfolio contract."""
        ...

    def load_portfolio(self, *args: object, **kwargs: object) -> object:
        """load_portfolio contract."""
        ...

    def save_portfolio(self, *args: object, **kwargs: object) -> object:
        """save_portfolio contract."""
        ...

    def update_position(self, *args: object, **kwargs: object) -> object:
        """update_position contract."""
        ...

    def remove_position(self, *args: object, **kwargs: object) -> object:
        """remove_position contract."""
        ...

    def validate_portfolio(self, *args: object, **kwargs: object) -> object:
        """validate_portfolio contract."""
        ...

    def archive_portfolio(self, *args: object, **kwargs: object) -> object:
        """archive_portfolio contract."""
        ...

    def get_portfolio(self, *args: object, **kwargs: object) -> object:
        """get_portfolio contract."""
        ...

    def portfolio_exists(self, *args: object, **kwargs: object) -> object:
        """portfolio_exists contract."""
        ...

