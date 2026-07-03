"""Canonical immutable models for Atlas.

Module Name: atlas.core.models
Purpose: Define base object, event, metric, and health models.
Owner: Atlas Governance
Version: 1.0.0
Dependencies: dataclasses, datetime, hashlib, json, uuid
Architecture Layer: Core
"""

from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
import hashlib
import json
from uuid import uuid4

from atlas.core.enums import HealthStatus


def utc_now() -> str:
    """Return an ISO-8601 UTC timestamp."""
    return datetime.now(timezone.utc).isoformat()


def stable_checksum(payload: object) -> str:
    """Return deterministic SHA-256 checksum for JSON-serializable payload."""
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True)
class AtlasObject:
    """Base immutable Atlas object with required identity metadata."""

    object_id: str = field(default_factory=lambda: str(uuid4()))
    object_type: str = "AtlasObject"
    version: str = "1.0.0"
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)
    trace_id: str = field(default_factory=lambda: str(uuid4()))
    checksum: str = ""
    owner: str = "Atlas"
    status: str = "Created"

    def with_checksum(self) -> "AtlasObject":
        """Return a copy with a deterministic checksum over public fields."""
        payload = {k: v for k, v in self.__dict__.items() if k != "checksum"}
        return replace(self, checksum=stable_checksum(payload))


@dataclass(frozen=True)
class Event:
    """Immutable event exchanged through the Atlas Event Bus."""

    event_type: str
    publisher: str
    payload: dict[str, object]
    event_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: str = field(default_factory=utc_now)
    trace_id: str = field(default_factory=lambda: str(uuid4()))
    version: str = "1.0.0"


@dataclass(frozen=True)
class HealthReport:
    """Repository health response consumed by Runtime and Monitoring."""

    repository: str
    status: HealthStatus
    checks: dict[str, HealthStatus]
    timestamp: str = field(default_factory=utc_now)
    version: str = "1.0.0"


@dataclass(frozen=True)
class MetricSnapshot:
    """Repository metric snapshot."""

    repository: str
    metrics: dict[str, float]
    timestamp: str = field(default_factory=utc_now)
    version: str = "1.0.0"
