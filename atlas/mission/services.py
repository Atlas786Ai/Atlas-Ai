"""Business service boundary for MissionRepository.

Module Name: atlas.mission.services
Purpose: Implement deterministic mission ownership and retrieval.
Owner: Atlas Governance
Version: 1.0.0
Dependencies: atlas.repository_base, atlas.mission.models
Architecture Layer: Repository
"""

from pathlib import Path
from typing import Any

from atlas.core.exceptions import AtlasStorageError, AtlasValidationError
from atlas.core.models import stable_checksum, utc_now
from atlas.mission.constants import MISSION_ACTIVE, MISSION_ARCHIVED, REPOSITORY_VERSION, VALID_MISSION_PRIORITIES
from atlas.mission.events import MISSION_ARCHIVED as MISSION_ARCHIVED_EVENT
from atlas.mission.events import MISSION_CREATED, MISSION_LOADED, MISSION_SAVED, MISSION_VALIDATED
from atlas.mission.models import MissionDirective
from atlas.mission.validators import validate_payload, verify_mission_integrity
from atlas.repository_base import RepositoryBase


class MissionRepository(RepositoryBase):
    """Frozen Atlas v1.0 repository implementation for Atlas mission directives."""

    repository_name = "MissionRepository"
    public_interfaces = (
        "create_mission",
        "load_mission",
        "save_mission",
        "validate_mission",
        "archive_mission",
        "get_current_mission",
        "mission_exists",
        "get_mission_version",
    )
    event_types = (MISSION_CREATED, MISSION_LOADED, MISSION_SAVED, MISSION_VALIDATED, MISSION_ARCHIVED_EVENT)

    def __init__(self, storage_root: Path | None = None) -> None:
        super().__init__(storage_root)
        self._current_mission_id: str | None = None

    def create_mission(
        self,
        title: str,
        objective: str,
        *,
        constraints: tuple[str, ...] | list[str] = (),
        success_criteria: tuple[str, ...] | list[str] = (),
        priority: str = "medium",
        key: str | None = None,
    ) -> dict[str, Any]:
        """Create and persist a new immutable mission directive."""
        mission = MissionDirective(
            title=self._require_text(title, "title"),
            objective=self._require_text(objective, "objective"),
            constraints=self._normalize_collection(constraints, "constraints"),
            success_criteria=self._normalize_collection(success_criteria, "success_criteria"),
            priority=self._normalize_priority(priority),
            status=MISSION_ACTIVE,
        ).with_integrity_hash()
        record = self._save_mission_payload(mission.to_payload(), key=key)
        self.emit_event(MISSION_CREATED, {"mission_id": mission.mission_id})
        return record

    def load_mission(self, mission_id: str | None = None) -> dict[str, object]:
        """Load a mission payload by id, defaulting to current mission."""
        key = mission_id or self._current_mission_id
        if key is None:
            raise AtlasValidationError("No current mission is available")
        record = self.storage.read(key)
        payload = record["payload"]
        if not isinstance(payload, dict):
            raise AtlasValidationError("stored mission payload is invalid")
        verify_mission_integrity(payload)
        normalized = self._normalize_mission_payload(payload)
        self.emit_event(MISSION_LOADED, {"mission_id": key})
        return normalized

    def save_mission(self, payload: dict[str, object]) -> dict[str, Any]:
        """Validate and persist a mission payload without changing its meaning."""
        verify_mission_integrity(payload)
        return self._save_mission_payload(payload, key=str(payload["mission_id"]))

    def validate_mission(self, payload: dict[str, object] | None = None) -> bool:
        """Validate supplied or current mission payload."""
        mission_payload = payload or self.load_mission()
        verify_mission_integrity(mission_payload)
        self.emit_event(MISSION_VALIDATED, {"mission_id": mission_payload["mission_id"]})
        return True

    def archive_mission(self, mission_id: str | None = None) -> dict[str, Any]:
        """Archive a mission by creating a new immutable archive record."""
        payload = dict(self.load_mission(mission_id))
        payload["status"] = MISSION_ARCHIVED
        payload["updated_at"] = utc_now()
        payload["integrity_hash"] = ""
        payload["integrity_hash"] = stable_checksum(payload)
        verify_mission_integrity(payload)
        key = f"{payload['mission_id']}.archive"
        record = self.archive_record(key, payload)
        self.emit_event(MISSION_ARCHIVED_EVENT, {"mission_id": payload["mission_id"]})
        return record

    def get_current_mission(self) -> dict[str, object]:
        """Return the current mission payload without mutation."""
        return self.load_mission()

    def mission_exists(self, mission_id: str | None = None) -> bool:
        """Return whether a mission exists in storage."""
        key = mission_id or self._current_mission_id
        if key is None:
            return False
        try:
            self.storage.read(key)
        except AtlasStorageError:
            return False
        return True

    def get_mission_version(self) -> str:
        """Return MissionRepository frozen version."""
        return REPOSITORY_VERSION

    def _normalize_mission_payload(self, payload: dict[str, object]) -> dict[str, object]:
        normalized = dict(payload)
        normalized["constraints"] = tuple(normalized["constraints"])
        normalized["success_criteria"] = tuple(normalized["success_criteria"])
        return normalized

    def _save_mission_payload(self, payload: dict[str, object], *, key: str | None = None) -> dict[str, Any]:
        validate_payload(payload)
        verify_mission_integrity(payload)
        mission_id = str(payload["mission_id"])
        record = self.archive_record(key or mission_id, payload)
        self._current_mission_id = key or mission_id
        self.emit_event(MISSION_SAVED, {"mission_id": mission_id})
        return record

    def _normalize_collection(self, values: tuple[str, ...] | list[str], field: str) -> tuple[str, ...]:
        if not isinstance(values, (tuple, list)) or not all(isinstance(item, str) and item for item in values):
            raise AtlasValidationError(f"{field} must be a tuple or list of non-empty strings")
        return tuple(sorted(values))

    def _normalize_priority(self, priority: str) -> str:
        if not isinstance(priority, str) or priority not in VALID_MISSION_PRIORITIES:
            raise AtlasValidationError("priority is invalid", context={"priority": priority})
        return priority

    def _require_text(self, value: str, field: str) -> str:
        if not isinstance(value, str) or not value:
            raise AtlasValidationError(f"{field} must be a non-empty string")
        return value
