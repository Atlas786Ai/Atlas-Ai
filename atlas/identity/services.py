"""Business service boundary for IdentityRepository.

Module Name: atlas.identity.services
Purpose: Implement deterministic identity ownership and retrieval.
Owner: Atlas Governance
Version: 1.0.0
Dependencies: atlas.repository_base, atlas.identity.models
Architecture Layer: Repository
"""

from pathlib import Path
from typing import Any

from atlas.core.exceptions import AtlasStorageError, AtlasValidationError
from atlas.core.models import stable_checksum, utc_now
from atlas.identity.constants import IDENTITY_ACTIVE, IDENTITY_ARCHIVED
from atlas.identity.models import IdentityProfile
from atlas.identity.validators import validate_identity_payload, verify_identity_integrity
from atlas.repository_base import RepositoryBase


class IdentityRepository(RepositoryBase):
    """Frozen Atlas v1.0 repository implementation for Atlas identity."""

    repository_name = "IdentityRepository"
    public_interfaces = (
        "create_identity",
        "load_identity",
        "save_identity",
        "validate_identity",
        "archive_identity",
        "get_identity",
        "identity_exists",
    )
    event_types = (
        "IdentityCreated",
        "IdentityLoaded",
        "IdentitySaved",
        "IdentityValidated",
        "IdentityArchived",
    )

    def __init__(self, storage_root: Path | None = None) -> None:
        super().__init__(storage_root)
        self._current_identity_id: str | None = None

    def create_identity(
        self,
        name: str,
        purpose: str,
        *,
        traits: tuple[str, ...] | list[str] = (),
        capabilities: tuple[str, ...] | list[str] = (),
        key: str | None = None,
    ) -> dict[str, Any]:
        """Create and persist a new immutable Atlas identity profile."""
        identity = IdentityProfile(
            name=self._require_text(name, "name"),
            purpose=self._require_text(purpose, "purpose"),
            traits=self._normalize_collection(traits, "traits"),
            capabilities=self._normalize_collection(capabilities, "capabilities"),
            status=IDENTITY_ACTIVE,
        ).with_integrity_hash()
        record = self._save_identity_payload(identity.to_payload(), key=key)
        self.emit_event("IdentityCreated", {"identity_id": identity.identity_id})
        return record

    def load_identity(self, identity_id: str | None = None) -> dict[str, object]:
        """Load an identity payload by id, defaulting to current identity."""
        key = identity_id or self._current_identity_id
        if key is None:
            raise AtlasValidationError("No current identity is available")
        record = self.storage.read(key)
        payload = record["payload"]
        if not isinstance(payload, dict):
            raise AtlasValidationError("stored identity payload is invalid")
        verify_identity_integrity(payload)
        normalized = self._normalize_identity_payload(payload)
        self.emit_event("IdentityLoaded", {"identity_id": key})
        return normalized

    def save_identity(self, payload: dict[str, object]) -> dict[str, Any]:
        """Validate and persist an identity payload without changing its meaning."""
        verify_identity_integrity(payload)
        return self._save_identity_payload(payload, key=str(payload["identity_id"]))

    def validate_identity(self, payload: dict[str, object] | None = None) -> bool:
        """Validate supplied or current identity payload."""
        identity_payload = payload or self.load_identity()
        verify_identity_integrity(identity_payload)
        self.emit_event("IdentityValidated", {"identity_id": identity_payload["identity_id"]})
        return True

    def archive_identity(self, identity_id: str | None = None) -> dict[str, Any]:
        """Archive an identity profile by creating a new immutable archive record."""
        payload = dict(self.load_identity(identity_id))
        payload["status"] = IDENTITY_ARCHIVED
        payload["updated_at"] = utc_now()
        payload["integrity_hash"] = ""
        payload["integrity_hash"] = stable_checksum(payload)
        verify_identity_integrity(payload)
        key = f"{payload['identity_id']}.archive"
        record = self.archive_record(key, payload)
        self.emit_event("IdentityArchived", {"identity_id": payload["identity_id"]})
        return record

    def get_identity(self, identity_id: str | None = None) -> dict[str, object]:
        """Return an identity payload without mutation."""
        return self.load_identity(identity_id)

    def identity_exists(self, identity_id: str | None = None) -> bool:
        """Return whether an identity exists in storage."""
        key = identity_id or self._current_identity_id
        if key is None:
            return False
        try:
            self.storage.read(key)
        except AtlasStorageError:
            return False
        return True

    def _normalize_identity_payload(self, payload: dict[str, object]) -> dict[str, object]:
        normalized = dict(payload)
        normalized["traits"] = tuple(normalized["traits"])
        normalized["capabilities"] = tuple(normalized["capabilities"])
        return normalized

    def _save_identity_payload(self, payload: dict[str, object], *, key: str | None = None) -> dict[str, Any]:
        validate_identity_payload(payload)
        verify_identity_integrity(payload)
        identity_id = str(payload["identity_id"])
        record = self.archive_record(key or identity_id, payload)
        self._current_identity_id = key or identity_id
        self.emit_event("IdentitySaved", {"identity_id": identity_id})
        return record

    def _normalize_collection(self, values: tuple[str, ...] | list[str], field: str) -> tuple[str, ...]:
        if not isinstance(values, (tuple, list)) or not all(isinstance(item, str) and item for item in values):
            raise AtlasValidationError(f"{field} must be a tuple or list of non-empty strings")
        return tuple(sorted(values))

    def _require_text(self, value: str, field: str) -> str:
        if not isinstance(value, str) or not value:
            raise AtlasValidationError(f"{field} must be a non-empty string")
        return value
