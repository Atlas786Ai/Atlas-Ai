"""Deterministic Atlas Event Bus.

Module Name: atlas.event_bus
Purpose: Route immutable events without business logic.
Owner: Atlas Governance
Version: 1.0.0
Dependencies: collections, atlas.core
Architecture Layer: Core Infrastructure
"""

from collections import defaultdict
from dataclasses import dataclass
from typing import Callable

from atlas.core.exceptions import AtlasValidationError
from atlas.core.models import Event

EventHandler = Callable[[Event], None]


@dataclass(frozen=True)
class Subscription:
    """Immutable subscription to an event type."""

    event_type: str
    repository: str
    handler: EventHandler
    priority: int = 100


class EventBus:
    """Validation-gated deterministic event dispatcher."""

    def __init__(self) -> None:
        self._subscriptions: dict[str, list[Subscription]] = defaultdict(list)
        self._events: dict[str, Event] = {}

    def publish(self, event: Event) -> Event:
        """Validate, store, and dispatch an immutable event."""
        self.validate_event(event)
        self._events[event.event_id] = event
        self.dispatch(event)
        return event

    def subscribe(self, event_type: str, repository: str, handler: EventHandler, priority: int = 100) -> Subscription:
        """Register a deterministic event subscription."""
        subscription = Subscription(event_type, repository, handler, priority)
        self._subscriptions[event_type].append(subscription)
        self._subscriptions[event_type].sort(key=lambda item: (item.priority, item.repository))
        return subscription

    def unsubscribe(self, subscription: Subscription) -> None:
        """Remove an existing subscription."""
        self._subscriptions[subscription.event_type] = [item for item in self._subscriptions[subscription.event_type] if item != subscription]

    def dispatch(self, event: Event) -> None:
        """Deliver an event to subscriptions in deterministic order."""
        for subscription in self._subscriptions.get(event.event_type, []):
            subscription.handler(event)

    def validate_event(self, event: Event) -> None:
        """Validate required immutable event fields."""
        if not event.event_type or not event.publisher or not event.version:
            raise AtlasValidationError("Invalid event", context={"event_id": event.event_id})

    def get_event(self, event_id: str) -> Event | None:
        """Return a previously published event."""
        return self._events.get(event_id)

    def replay_events(self, event_type: str | None = None) -> list[Event]:
        """Return events in deterministic timestamp/event-id order without side effects."""
        events = list(self._events.values())
        if event_type is not None:
            events = [event for event in events if event.event_type == event_type]
        return sorted(events, key=lambda event: (event.timestamp, event.event_id))
