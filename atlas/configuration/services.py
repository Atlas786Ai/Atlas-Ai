"""Business service boundary for ConfigurationRepository.

Module Name: atlas.configuration.services
Purpose: Implement the frozen public service API for ConfigurationRepository.
Owner: Atlas Governance
Version: 1.0.0
Dependencies: atlas.repository_base, atlas.configuration.models, atlas.configuration.validators
Architecture Layer: Repository
"""

from pathlib import Path
from typing import Any

from atlas.configuration.models import Configuration, ConfigurationSection
from atlas.configuration.validators import validate_configuration_payload
from atlas.core.exceptions import AtlasStorageError, AtlasValidationError
from atlas.core.models import stable_checksum, utc_now
from atlas.repository_base import RepositoryBase


class ConfigurationRepository(RepositoryBase):
    """Frozen Atlas v1.0 repository implementation for ConfigurationRepository."""

    repository_name = "ConfigurationRepository"
    public_interfaces = (
        "load_configuration",
        "save_configuration",
        "validate_configuration",
        "get_configuration",
        "reload_configuration",
        "archive_configuration",
        "configuration_exists",
    )
    event_types = (
        "ConfigurationLoaded",
        "ConfigurationUpdated",
        "ConfigurationValidated",
        "ConfigurationArchived",
        "ConfigurationReloaded",
    )

    def __init__(self, storage_root: Path | None = None) -> None:
        super().__init__(storage_root)
        self._current_configuration_id: str | None = None

    def load_configuration(self, configuration_id: str | None = None, **_: object) -> dict[str, Any]:
        """Load a stored configuration by id, defaulting to the current configuration."""
        key = configuration_id or self._current_configuration_id
        if key is None:
            raise AtlasValidationError("No current configuration is available")
        record = self.storage.read(key)
        payload = record["payload"]
        if not isinstance(payload, dict):
            raise AtlasValidationError("Stored configuration payload is invalid")
        validate_configuration_payload(payload)
        self.emit_event("ConfigurationLoaded", {"configuration_id": key})
        return payload

    def save_configuration(self, payload: dict[str, object] | None = None, **kwargs: object) -> dict[str, Any]:
        """Validate and persist an immutable configuration version."""
        configuration = self._coerce_configuration(payload or kwargs)
        configuration_payload = configuration.with_integrity_hash().to_payload()
        validate_configuration_payload(configuration_payload)
        self._verify_integrity(configuration_payload)
        configuration_id = str(configuration_payload["configuration_id"])
        record = self.archive_record(configuration_id, configuration_payload)
        self._current_configuration_id = configuration_id
        self.emit_event("ConfigurationUpdated", {"configuration_id": configuration_id})
        return record

    def validate_configuration(self, payload: dict[str, object] | None = None, **kwargs: object) -> bool:
        """Validate a configuration payload and integrity hash."""
        configuration_payload = payload or kwargs
        validate_configuration_payload(configuration_payload)
        self._verify_integrity(configuration_payload)
        self.emit_event("ConfigurationValidated", {"configuration_id": configuration_payload["configuration_id"]})
        return True

    def get_configuration(self, configuration_id: str | None = None, **kwargs: object) -> dict[str, Any]:
        """Return a stored configuration without changing it."""
        return self.load_configuration(configuration_id, **kwargs)

    def reload_configuration(self, configuration_id: str | None = None, **kwargs: object) -> dict[str, Any]:
        """Reload a validated configuration and mark it current."""
        payload = self.load_configuration(configuration_id, **kwargs)
        self._current_configuration_id = str(payload["configuration_id"])
        self.emit_event("ConfigurationReloaded", {"configuration_id": self._current_configuration_id})
        return payload

    def archive_configuration(self, configuration_id: str | None = None, **kwargs: object) -> dict[str, Any]:
        """Archive a configuration by creating an archive record."""
        payload = self.load_configuration(configuration_id, **kwargs)
        archived_payload = dict(payload)
        archived_payload["status"] = "Archived"
        archived_payload["updated_at"] = utc_now()
        archived_payload["integrity_hash"] = ""
        archived_payload["integrity_hash"] = stable_checksum(archived_payload)
        key = f"{archived_payload['configuration_id']}.archive"
        record = self.archive_record(key, archived_payload)
        self.emit_event("ConfigurationArchived", {"configuration_id": archived_payload["configuration_id"]})
        return record

    def configuration_exists(self, configuration_id: str | None = None, **_: object) -> bool:
        """Return whether a configuration exists in storage."""
        key = configuration_id or self._current_configuration_id
        if key is None:
            return False
        try:
            self.storage.read(key)
        except AtlasStorageError:
            return False
        return True

    def _coerce_configuration(self, payload: dict[str, object]) -> Configuration:
        if "sections" not in payload:
            raise AtlasValidationError("Configuration input requires sections")
        sections_input = payload["sections"]
        if isinstance(sections_input, dict):
            sections = tuple(
                ConfigurationSection(name=name, values=values if isinstance(values, dict) else {"value": values})
                for name, values in sorted(sections_input.items())
            )
        elif isinstance(sections_input, list):
            sections = tuple(
                ConfigurationSection(
                    name=str(section["name"]),
                    values=section["values"],
                    version=str(section.get("version", "1.0.0")),
                )
                for section in sections_input
                if isinstance(section, dict)
            )
        else:
            raise AtlasValidationError("Configuration sections must be a dictionary or list")
        return Configuration(
            configuration_id=self._configuration_id_from_payload(payload, sections),
            name=str(payload.get("name", "AtlasConfiguration")),
            version=str(payload.get("version", "1.0.0")),
            sections=sections,
            created_at=str(payload.get("created_at", utc_now())),
            updated_at=str(payload.get("updated_at", utc_now())),
            status=str(payload.get("status", "Active")),
        )

    def _configuration_id_from_payload(
        self,
        payload: dict[str, object],
        sections: tuple[ConfigurationSection, ...],
    ) -> str:
        if payload.get("configuration_id"):
            return str(payload["configuration_id"])
        return Configuration(name="temporary", sections=sections).configuration_id

    def _verify_integrity(self, payload: dict[str, object]) -> None:
        expected_payload = dict(payload)
        expected_hash = str(expected_payload.get("integrity_hash", ""))
        expected_payload["integrity_hash"] = ""
        actual_hash = stable_checksum(expected_payload)
        if expected_hash != actual_hash:
            raise AtlasValidationError("Configuration integrity hash mismatch")
