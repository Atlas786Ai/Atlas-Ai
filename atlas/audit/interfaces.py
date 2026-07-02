"""Public interface contracts for AuditRepository."""

from typing import Protocol


class AuditRepositoryInterface(Protocol):
    def record_event(self, *args: object, **kwargs: object) -> object:
        """record_event contract."""
        ...

    def load_event(self, *args: object, **kwargs: object) -> object:
        """load_event contract."""
        ...

    def search_events(self, *args: object, **kwargs: object) -> object:
        """search_events contract."""
        ...

    def validate_audit(self, *args: object, **kwargs: object) -> object:
        """validate_audit contract."""
        ...

    def archive_audit(self, *args: object, **kwargs: object) -> object:
        """archive_audit contract."""
        ...

    def get_trace(self, *args: object, **kwargs: object) -> object:
        """get_trace contract."""
        ...

    def audit_available(self, *args: object, **kwargs: object) -> object:
        """audit_available contract."""
        ...

