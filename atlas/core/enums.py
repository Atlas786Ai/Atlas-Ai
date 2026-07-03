"""Core enumerations shared by Atlas repositories.

Module Name: atlas.core.enums
Purpose: Define stable status and health enumerations.
Owner: Atlas Governance
Version: 1.0.0
Dependencies: enum
Architecture Layer: Core
"""

from enum import Enum


class HealthStatus(str, Enum):
    """Canonical repository health states."""

    PASS = "PASS"
    WARNING = "WARNING"
    DEGRADED = "DEGRADED"
    FAIL = "FAIL"
    CRITICAL = "CRITICAL"


class ObjectStatus(str, Enum):
    """Generic immutable object lifecycle states."""

    CREATED = "Created"
    VALIDATED = "Validated"
    ACTIVE = "Active"
    ARCHIVED = "Archived"
    FAILED = "Failed"
