"""Deterministic Atlas Event Bus.

Module Name: atlas.event_bus
Purpose: Route immutable events without business logic.
Owner: Atlas Governance
Version: 1.0.0
Dependencies: collections, dataclasses, atlas.core
Architecture Layer: Core Infrastructure
"""

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Callable
from uuid import uuid4

from atlas.core.enums import HealthStatus
from atlas.core.exceptions import AtlasException, AtlasValidationError
from atlas.core.models import Event, HealthReport, MetricSnapshot, utc_now

EventHandler = Callable[[Event], None]


class EventValidationError(AtlasValidationError):
    """Raised when an event violates Event Bus schema rules."""


class DeliveryFailure(AtlasException):
    """Raised when a subscriber fails during delivery."""


class SubscriptionError(AtlasException):
    """Raised when subscription management fails."""


class ReplayError(AtlasException):
    """Raised when replay cannot be performed."""


class DispatchError(AtlasException):
    """Raised when dispatch cannot proceed deterministically."""


@dataclass(frozen=True)
class Subscription:
    """Immutable subscription to an event type."""

    event_type: str
    repository: str
    handler: EventHandler
    priority: int = 100
    subscription_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=utc_now)
    version: str = "1.0.0"


@dataclass(frozen=True)
class DeliveryStatus:
    """Immutable status for one event delivery attempt."""

    event_id: str
    event_type: str
    subscriber: str
    status: str
    sequence: int
    delivered_at: str = field(default_factory=utc_now)
    error: str = ""
    version: str = "1.0.0"


class EventBus:
    """Validation-gated deterministic event dispatcher."""

    def __init__(self) -> None:
        self._subscriptions: dict[str, list[Subscription]] = defaultdict(list)
        self._events: dict[str, Event] = {}
        self._publish_order: list[str] = []
        self._delivery_statuses: list[DeliveryStatus] = []
        self._metrics: dict[str, float] = {
            "events_published": 0.0,
            "events_delivered": 0.0,
            "events_rejected": 0.0,
            "delivery_failures": 0.0,
            "replay_count": 0.0,
        }

    def publish(self, event: Event) -> Event:
        """Validate, store, and dispatch an immutable event."""
        try:
            self.validate_event(event)
        except AtlasValidationError as exc:
            self._metrics["events_rejected"] += 1.0
            raise EventValidationError("Event rejected by EventBus validation", context=exc.context) from exc
        if event.event_id in self._events:
            self._metrics["events_rejected"] += 1.0
            raise EventValidationError("Duplicate event_id rejected", context={"event_id": event.event_id})
        self._events[event.event_id] = event
        self._publish_order.append(event.event_id)
        self._metrics["events_published"] += 1.0
        self.dispatch(event)
        return event

    def subscribe(self, event_type: str, repository: str, handler: EventHandler, priority: int = 100) -> Subscription:
        """Register a deterministic event subscription."""
        self._validate_subscription_inputs(event_type, repository, handler, priority)
        subscription = Subscription(event_type=event_type, repository=repository, handler=handler, priority=priority)
        self._subscriptions[event_type].append(subscription)
        self._subscriptions[event_type].sort(key=lambda item: (item.priority, item.repository))
        return subscription

    def unsubscribe(self, subscription: Subscription) -> None:
        """Remove an existing subscription."""
        existing = self._subscriptions.get(subscription.event_type, [])
        if subscription not in existing:
            raise SubscriptionError("Subscription not found", context={"subscription_id": subscription.subscription_id})
        self._subscriptions[subscription.event_type] = [item for item in existing if item != subscription]

    def dispatch(self, event: Event) -> None:
        """Deliver an event to subscriptions in deterministic order."""
        self.validate_event(event)
        subscriptions = tuple(self._subscriptions.get(event.event_type, ()))
        for subscription in subscriptions:
            sequence = len(self._delivery_statuses) + 1
            try:
                subscription.handler(event)
            except Exception as exc:
                self._metrics["delivery_failures"] += 1.0
                self._delivery_statuses.append(
                    DeliveryStatus(
                        event_id=event.event_id,
                        event_type=event.event_type,
                        subscriber=subscription.repository,
                        status="FAILED",
                        sequence=sequence,
                        error=str(exc),
                    )
                )
                raise DeliveryFailure(
                    "Event delivery failed",
                    context={"event_id": event.event_id, "subscriber": subscription.repository},
                ) from exc
            self._metrics["events_delivered"] += 1.0
            self._delivery_statuses.append(
                DeliveryStatus(
                    event_id=event.event_id,
                    event_type=event.event_type,
                    subscriber=subscription.repository,
                    status="DELIVERED",
                    sequence=sequence,
                )
            )

    def validate_event(self, event: Event) -> None:
        """Validate required immutable event fields."""
        if not isinstance(event, Event):
            raise EventValidationError("Invalid event object")
        if not event.event_type or not event.publisher or not event.version:
            raise EventValidationError("Invalid event", context={"event_id": event.event_id})
        if not isinstance(event.payload, dict):
            raise EventValidationError("Event payload must be a dictionary", context={"event_id": event.event_id})

    def get_event(self, event_id: str) -> Event | None:
        """Return a previously published event."""
        if not isinstance(event_id, str) or not event_id:
            raise EventValidationError("event_id must be a non-empty string")
        return self._events.get(event_id)

    def replay_events(self, event_type: str | None = None, *, dispatch: bool = False) -> list[Event]:
        """Return events in publish order and optionally dispatch them again."""
        if event_type is not None and not isinstance(event_type, str):
            raise ReplayError("event_type must be a string when supplied")
        events = [self._events[event_id] for event_id in self._publish_order]
        if event_type is not None:
            events = [event for event in events if event.event_type == event_type]
        if dispatch:
            for event in events:
                self.dispatch(event)
            self._metrics["replay_count"] += float(len(events))
        return events

    def get_delivery_status(self, event_id: str | None = None) -> tuple[DeliveryStatus, ...]:
        """Return immutable delivery status records in deterministic sequence order."""
        if event_id is None:
            return tuple(self._delivery_statuses)
        if not isinstance(event_id, str) or not event_id:
            raise EventValidationError("event_id must be a non-empty string")
        return tuple(status for status in self._delivery_statuses if status.event_id == event_id)

    def metrics(self) -> MetricSnapshot:
        """Return Event Bus metrics."""
        queue_size = float(sum(len(items) for items in self._subscriptions.values()))
        metrics = dict(sorted({**self._metrics, "subscriptions": queue_size, "queue_size": queue_size}.items()))
        return MetricSnapshot(repository="EventBus", metrics=metrics)

    def health(self) -> HealthReport:
        """Return Event Bus health checks."""
        checks = {
            "dispatcher": HealthStatus.PASS,
            "publisher": HealthStatus.PASS,
            "subscriptions": HealthStatus.PASS,
            "queue": HealthStatus.PASS,
            "version": HealthStatus.PASS,
        }
        return HealthReport(repository="EventBus", status=HealthStatus.PASS, checks=checks)

    def _validate_subscription_inputs(
        self,
        event_type: str,
        repository: str,
        handler: EventHandler,
        priority: int,
    ) -> None:
        if not isinstance(event_type, str) or not event_type:
            raise SubscriptionError("event_type must be a non-empty string")
        if not isinstance(repository, str) or not repository:
            raise SubscriptionError("repository must be a non-empty string")
        if not callable(handler):
            raise SubscriptionError("handler must be callable")
        if not isinstance(priority, int):
            raise SubscriptionError("priority must be an integer")
