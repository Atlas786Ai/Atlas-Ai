"""Domain models for IdentityRepository.

Module Name: atlas.identity.models
Purpose: Define immutable Atlas identity profiles.
Owner: Atlas Governance
Version: 1.0.0
Dependencies: dataclasses, atlas.core.models
Architecture Layer: Repository
"""

from dataclasses import dataclass, field
from uuid import uuid4

from atlas.core.models import stable_checksum, utc_now
from atlas.identity.constants import IDENTITY_ACTIVE


@dataclass(frozen=True)
class IdentityProfile:
    """Immutable identity profile owned exclusively by IdentityRepository."""

    name: str
    purpose: str
    traits: tuple[str, ...] = ()
    capabilities: tuple[str, ...] = ()
    identity_id: str = field(default_factory=lambda: str(uuid4()))
    status: str = IDENTITY_ACTIVE
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)
    version: str = "1.0.0"
    integrity_hash: str = ""

    def to_payload(self) -> dict[str, object]:
        """Return deterministic identity payload."""
        return {
            "identity_id": self.identity_id,
            "name": self.name,
            "purpose": self.purpose,
            "traits": self.traits,
            "capabilities": self.capabilities,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "version": self.version,
            "integrity_hash": self.integrity_hash,
        }

    def with_integrity_hash(self) -> "IdentityProfile":
        """Return profile with deterministic integrity hash."""
        payload = self.to_payload()
        payload["integrity_hash"] = ""
        return IdentityProfile(
            identity_id=self.identity_id,
            name=self.name,
            purpose=self.purpose,
            traits=self.traits,
            capabilities=self.capabilities,
            status=self.status,
            created_at=self.created_at,
            updated_at=self.updated_at,
            version=self.version,
            integrity_hash=stable_checksum(payload),
        )
