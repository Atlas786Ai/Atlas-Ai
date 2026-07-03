"""Domain models for MissionRepository.

Module Name: atlas.mission.models
Purpose: Define immutable Atlas mission directives.
Owner: Atlas Governance
Version: 1.0.0
Dependencies: dataclasses, atlas.core.models
Architecture Layer: Repository
"""

from dataclasses import dataclass, field
from uuid import uuid4

from atlas.core.models import stable_checksum, utc_now
from atlas.mission.constants import MISSION_ACTIVE


@dataclass(frozen=True)
class MissionDirective:
    """Immutable mission directive owned exclusively by MissionRepository."""

    title: str
    objective: str
    constraints: tuple[str, ...] = ()
    success_criteria: tuple[str, ...] = ()
    priority: str = "medium"
    mission_id: str = field(default_factory=lambda: str(uuid4()))
    status: str = MISSION_ACTIVE
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)
    version: str = "1.0.0"
    integrity_hash: str = ""

    def to_payload(self) -> dict[str, object]:
        """Return deterministic mission payload."""
        return {
            "mission_id": self.mission_id,
            "title": self.title,
            "objective": self.objective,
            "constraints": self.constraints,
            "success_criteria": self.success_criteria,
            "priority": self.priority,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "version": self.version,
            "integrity_hash": self.integrity_hash,
        }

    def with_integrity_hash(self) -> "MissionDirective":
        """Return directive with deterministic integrity hash."""
        payload = self.to_payload()
        payload["integrity_hash"] = ""
        return MissionDirective(
            mission_id=self.mission_id,
            title=self.title,
            objective=self.objective,
            constraints=self.constraints,
            success_criteria=self.success_criteria,
            priority=self.priority,
            status=self.status,
            created_at=self.created_at,
            updated_at=self.updated_at,
            version=self.version,
            integrity_hash=stable_checksum(payload),
        )
