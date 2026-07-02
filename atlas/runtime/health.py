"""Health endpoint for RuntimeRepository."""

from atlas.core.enums import HealthStatus

def health_status() -> HealthStatus:
    """Return baseline health status."""
    return HealthStatus.PASS
