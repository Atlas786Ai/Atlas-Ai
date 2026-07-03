"""Validators for ConfigurationRepository.

Module Name: atlas.configuration.validators
Purpose: Validate Atlas configuration payloads before storage or distribution.
Owner: Atlas Governance
Version: 1.0.0
Dependencies: atlas.core.exceptions
Architecture Layer: Repository
"""

from atlas.core.exceptions import AtlasValidationError

REQUIRED_CONFIGURATION_FIELDS = (
    "configuration_id",
    "name",
    "version",
    "sections",
    "created_at",
    "updated_at",
    "status",
    "integrity_hash",
)


def validate_payload(payload: dict[str, object]) -> None:
    """Validate a generic immutable repository payload."""
    if not isinstance(payload, dict):
        raise AtlasValidationError("Payload must be a dictionary")


def validate_configuration_payload(payload: dict[str, object]) -> None:
    """Validate canonical Configuration payload fields and sections."""
    validate_payload(payload)
    missing = [field for field in REQUIRED_CONFIGURATION_FIELDS if field not in payload]
    if missing:
        raise AtlasValidationError("Configuration payload is missing required fields", context={"missing": missing})
    sections = payload["sections"]
    if not isinstance(sections, list) or not sections:
        raise AtlasValidationError("Configuration must contain at least one section")
    for section in sections:
        if not isinstance(section, dict):
            raise AtlasValidationError("Configuration section must be a dictionary")
        if not section.get("name") or not isinstance(section.get("values"), dict):
            raise AtlasValidationError("Configuration section requires name and values")
