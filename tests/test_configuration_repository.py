"""ConfigurationRepository tests for Atlas v1.0."""

import pytest

from atlas.configuration.services import ConfigurationRepository
from atlas.core.exceptions import AtlasValidationError


def test_save_and_load_configuration_round_trip(tmp_path) -> None:
    repository = ConfigurationRepository(storage_root=tmp_path)
    record = repository.save_configuration(
        payload={
            "configuration_id": "config-001",
            "name": "Atlas Test Configuration",
            "sections": {"runtime": {"workers": 1}, "logging": {"level": "INFO"}},
        }
    )
    loaded = repository.load_configuration("config-001")
    assert record["payload"] == loaded
    assert loaded["integrity_hash"]
    assert repository.configuration_exists("config-001") is True


def test_validate_configuration_rejects_tampered_hash(tmp_path) -> None:
    repository = ConfigurationRepository(storage_root=tmp_path)
    repository.save_configuration(
        payload={
            "configuration_id": "config-002",
            "name": "Config",
            "sections": {"runtime": {"workers": 1}},
        }
    )
    payload = repository.load_configuration("config-002")
    payload["name"] = "Tampered"
    with pytest.raises(AtlasValidationError):
        repository.validate_configuration(payload=payload)


def test_archive_configuration_creates_archived_copy(tmp_path) -> None:
    repository = ConfigurationRepository(storage_root=tmp_path)
    repository.save_configuration(
        payload={
            "configuration_id": "config-003",
            "name": "Config",
            "sections": {"runtime": {"workers": 1}},
        }
    )
    archive = repository.archive_configuration("config-003")
    assert archive["payload"]["status"] == "Archived"
    assert archive["key"] == "config-003.archive"


def test_reload_configuration_marks_current(tmp_path) -> None:
    repository = ConfigurationRepository(storage_root=tmp_path)
    repository.save_configuration(
        payload={
            "configuration_id": "config-004",
            "name": "Config",
            "sections": {"runtime": {"workers": 1}},
        }
    )
    reloaded = repository.reload_configuration("config-004")
    assert reloaded["configuration_id"] == "config-004"
    assert repository.load_configuration()["configuration_id"] == "config-004"
