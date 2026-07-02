"""Public interface contracts for SecurityRepository."""

from typing import Protocol


class SecurityRepositoryInterface(Protocol):
    def authenticate(self, *args: object, **kwargs: object) -> object:
        """authenticate contract."""
        ...

    def authorize(self, *args: object, **kwargs: object) -> object:
        """authorize contract."""
        ...

    def verify_signature(self, *args: object, **kwargs: object) -> object:
        """verify_signature contract."""
        ...

    def validate_permission(self, *args: object, **kwargs: object) -> object:
        """validate_permission contract."""
        ...

    def validate_policy(self, *args: object, **kwargs: object) -> object:
        """validate_policy contract."""
        ...

    def archive_security_event(self, *args: object, **kwargs: object) -> object:
        """archive_security_event contract."""
        ...

    def get_security_status(self, *args: object, **kwargs: object) -> object:
        """get_security_status contract."""
        ...

