"""Atlas Runtime boot sequence implementation.

Module Name: atlas.runtime.boot
Purpose: Execute the frozen Atlas v1.0 runtime boot sequence deterministically.
Owner: Atlas Governance
Version: 1.0.0
Dependencies: importlib, dataclasses, atlas.architecture, atlas.core, atlas.event_bus
Architecture Layer: Runtime
"""

from dataclasses import dataclass, field
import importlib
from typing import Any

from atlas.architecture import BOOT_SEQUENCE, FROZEN_REPOSITORIES
from atlas.core.enums import HealthStatus
from atlas.core.exceptions import AtlasValidationError
from atlas.core.models import Event, utc_now
from atlas.core.registry import RepositoryRegistration, RepositoryRegistry
from atlas.event_bus import EventBus


@dataclass(frozen=True)
class BootPhaseResult:
    """Immutable result for one boot phase."""

    phase_index: int
    components: tuple[str, ...]
    initialized_at: str


@dataclass(frozen=True)
class BootResult:
    """Immutable result of a completed Atlas boot."""

    status: str
    phases: tuple[BootPhaseResult, ...]
    repositories: tuple[str, ...]
    events: tuple[Event, ...] = field(default_factory=tuple)


class AtlasBootManager:
    """Deterministic boot manager for the frozen Atlas v1.0 architecture."""

    def __init__(self) -> None:
        self.registry = RepositoryRegistry()
        self.event_bus = EventBus()
        self._instances: dict[str, Any] = {}
        self._events: list[Event] = []

    def boot(self) -> BootResult:
        """Initialize all frozen repositories according to the canonical boot sequence."""
        self._emit("BootStarted", {"phase_count": len(BOOT_SEQUENCE)})
        phase_results: list[BootPhaseResult] = []
        for index, phase in enumerate(BOOT_SEQUENCE, start=1):
            for component in phase:
                self._initialize_component(component)
            phase_results.append(
                BootPhaseResult(
                    phase_index=index,
                    components=tuple(phase),
                    initialized_at=utc_now(),
                )
            )
        self.registry.validate_required(FROZEN_REPOSITORIES)
        self._verify_health()
        self._emit("BootValidated", {"repositories": len(FROZEN_REPOSITORIES)})
        self._emit("RuntimeReady", {"status": "Running"})
        return BootResult(
            status="Running",
            phases=tuple(phase_results),
            repositories=self.registry.names(),
            events=tuple(self._events),
        )

    def shutdown(self) -> tuple[str, ...]:
        """Return deterministic shutdown order without mutating repository internals."""
        ordered: list[str] = []
        for phase in reversed(BOOT_SEQUENCE):
            ordered.extend(reversed(phase))
        self._emit("ShutdownCompleted", {"components": ordered})
        return tuple(ordered)

    def get_component(self, name: str) -> Any:
        """Return an initialized component by name."""
        try:
            return self._instances[name]
        except KeyError as exc:
            raise AtlasValidationError("Component is not initialized", context={"component": name}) from exc

    def _initialize_component(self, component: str) -> None:
        if component == "EventBus":
            self._instances[component] = self.event_bus
            self._emit("RepositoryInitialized", {"repository": component})
            return
        instance = self._load_repository(component)
        registration = instance.as_registration()
        self.registry.register(
            RepositoryRegistration(
                repository=registration["repository"],
                version=registration["version"],
                interfaces=tuple(registration["interfaces"]),
                health_endpoint=registration["health_endpoint"],
                events=tuple(registration["events"]),
            )
        )
        self._instances[component] = instance
        self._emit("RepositoryInitialized", {"repository": component})

    def _load_repository(self, repository: str) -> Any:
        slug = self._repository_slug(repository)
        module = importlib.import_module(f"atlas.{slug}.services")
        cls = getattr(module, repository)
        return cls()

    def _verify_health(self) -> None:
        for repository in FROZEN_REPOSITORIES:
            health = self.get_component(repository).health()
            if health.status is not HealthStatus.PASS:
                raise AtlasValidationError("Repository health check failed", context={"repository": repository})

    def _emit(self, event_type: str, payload: dict[str, object]) -> Event:
        event = Event(event_type=event_type, publisher="RuntimeRepository", payload=payload)
        self._events.append(event)
        return event

    @staticmethod
    def _repository_slug(repository: str) -> str:
        name = repository.removesuffix("Repository")
        if name == "CognitiveContext":
            return "cognitive_context"
        return ''.join(['_' + char.lower() if char.isupper() else char for char in name]).lstrip('_')
