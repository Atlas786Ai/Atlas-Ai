"""Repository registry for Atlas runtime boot.

Module Name: atlas.core.registry
Purpose: Register frozen repositories exactly once and validate architecture metadata.
Owner: Atlas Governance
Version: 1.0.0
Dependencies: dataclasses, atlas.core.exceptions
Architecture Layer: Core Infrastructure
"""

from dataclasses import dataclass

from atlas.core.exceptions import AtlasValidationError


@dataclass(frozen=True)
class RepositoryRegistration:
    """Immutable Runtime registration metadata for one repository."""

    repository: str
    version: str
    interfaces: tuple[str, ...]
    health_endpoint: str
    events: tuple[str, ...]


class RepositoryRegistry:
    """Deterministic registry enforcing one registration per repository."""

    def __init__(self) -> None:
        self._registrations: dict[str, RepositoryRegistration] = {}

    def register(self, registration: RepositoryRegistration) -> None:
        """Register a repository once.

        Raises:
            AtlasValidationError: If the registration is incomplete or duplicated.
        """
        if not registration.repository or not registration.version:
            raise AtlasValidationError("Repository registration is incomplete")
        if registration.repository in self._registrations:
            raise AtlasValidationError(
                "Repository already registered",
                context={"repository": registration.repository},
            )
        self._registrations[registration.repository] = registration

    def get(self, repository: str) -> RepositoryRegistration:
        """Return a repository registration by name."""
        try:
            return self._registrations[repository]
        except KeyError as exc:
            raise AtlasValidationError(
                "Repository is not registered",
                context={"repository": repository},
            ) from exc

    def names(self) -> tuple[str, ...]:
        """Return registered repository names in deterministic order."""
        return tuple(sorted(self._registrations))

    def validate_required(self, required: list[str]) -> None:
        """Validate that all required repositories are registered."""
        missing = [repository for repository in required if repository not in self._registrations]
        if missing:
            raise AtlasValidationError("Missing required repositories", context={"missing": missing})

    def as_dict(self) -> dict[str, dict[str, object]]:
        """Return deterministic dictionary representation."""
        return {
            name: {
                "repository": registration.repository,
                "version": registration.version,
                "interfaces": list(registration.interfaces),
                "health_endpoint": registration.health_endpoint,
                "events": list(registration.events),
            }
            for name, registration in sorted(self._registrations.items())
        }
