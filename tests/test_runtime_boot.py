"""Runtime boot sequence tests for Atlas v1.0."""

import pytest

from atlas.architecture import BOOT_SEQUENCE, FROZEN_REPOSITORIES
from atlas.core.exceptions import AtlasValidationError
from atlas.core.registry import RepositoryRegistration, RepositoryRegistry
from atlas.runtime.boot import AtlasBootManager


def test_repository_registry_rejects_duplicate_registration() -> None:
    registry = RepositoryRegistry()
    registration = RepositoryRegistration(
        repository="IdentityRepository",
        version="1.0.0",
        interfaces=("get_identity",),
        health_endpoint="health",
        events=(),
    )
    registry.register(registration)
    with pytest.raises(AtlasValidationError):
        registry.register(registration)


def test_runtime_boot_initializes_all_frozen_repositories() -> None:
    manager = AtlasBootManager()
    result = manager.boot()
    assert result.status == "Running"
    assert set(result.repositories) == set(FROZEN_REPOSITORIES)
    assert [phase.components for phase in result.phases] == [tuple(phase) for phase in BOOT_SEQUENCE]


def test_runtime_boot_emits_required_lifecycle_events() -> None:
    manager = AtlasBootManager()
    result = manager.boot()
    event_types = [event.event_type for event in result.events]
    assert event_types[0] == "BootStarted"
    assert "BootValidated" in event_types
    assert event_types[-1] == "RuntimeReady"


def test_shutdown_order_is_reverse_boot_order() -> None:
    manager = AtlasBootManager()
    manager.boot()
    assert manager.shutdown() == tuple(
        component for phase in reversed(BOOT_SEQUENCE) for component in reversed(phase)
    )
