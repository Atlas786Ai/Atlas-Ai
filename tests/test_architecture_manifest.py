"""Architecture compliance tests for Atlas v1.0."""

import importlib

from atlas.architecture import BOOT_SEQUENCE, FROZEN_REPOSITORIES


def test_frozen_repository_count() -> None:
    assert len(FROZEN_REPOSITORIES) == 22


def test_boot_sequence_starts_with_infrastructure() -> None:
    assert BOOT_SEQUENCE[0] == ["ConfigurationRepository", "LoggingRepository", "SecurityRepository", "AuditRepository"]


def test_repository_public_interfaces_are_declared() -> None:
    for repository in FROZEN_REPOSITORIES:
        slug = repository.removesuffix("Repository")
        slug = "cognitive_context" if slug == "CognitiveContext" else ''.join(['_'+c.lower() if c.isupper() else c for c in slug]).lstrip('_')
        module = importlib.import_module(f"atlas.{slug}.services")
        cls = getattr(module, repository)
        assert cls.public_interfaces
        instance = cls()
        registration = instance.as_registration()
        assert registration["repository"] == repository
        assert registration["interfaces"] == list(cls.public_interfaces)
