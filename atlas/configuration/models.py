"""Domain models for ConfigurationRepository.

Module Name: atlas.configuration.models
Purpose: Define immutable configuration objects and sections.
Owner: Atlas Governance
Version: 1.0.0
Dependencies: dataclasses, atlas.core.models
Architecture Layer: Repository
"""

from dataclasses import dataclass, field
from uuid import uuid4

from atlas.core.models import stable_checksum, utc_now


@dataclass(frozen=True)
class ConfigurationSection:
    """Immutable named configuration section."""

    name: str
    values: dict[str, object]
    version: str = "1.0.0"


@dataclass(frozen=True)
class Configuration:
    """Immutable Atlas configuration object."""

    name: str
    sections: tuple[ConfigurationSection, ...]
    configuration_id: str = field(default_factory=lambda: str(uuid4()))
    version: str = "1.0.0"
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)
    status: str = "Active"
    integrity_hash: str = ""

    def to_payload(self) -> dict[str, object]:
        """Return deterministic payload representation."""
        return {
            "configuration_id": self.configuration_id,
            "name": self.name,
            "version": self.version,
            "sections": [
                {"name": section.name, "values": section.values, "version": section.version}
                for section in self.sections
            ],
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "status": self.status,
            "integrity_hash": self.integrity_hash,
        }

    def with_integrity_hash(self) -> "Configuration":
        """Return a copy with an integrity hash over the configuration content."""
        payload = self.to_payload()
        payload["integrity_hash"] = ""
        return Configuration(
            configuration_id=self.configuration_id,
            name=self.name,
            version=self.version,
            sections=self.sections,
            created_at=self.created_at,
            updated_at=self.updated_at,
            status=self.status,
            integrity_hash=stable_checksum(payload),
        )
