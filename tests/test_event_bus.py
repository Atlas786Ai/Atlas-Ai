"""EventBus deterministic behavior tests."""

from atlas.core.models import Event
from atlas.event_bus import DeliveryFailure, EventBus, EventValidationError, SubscriptionError


def test_event_bus_delivers_by_priority_then_repository() -> None:
    delivered: list[str] = []
    bus = EventBus()
    bus.subscribe("Example", "BRepository", lambda event: delivered.append("B"), priority=20)
    bus.subscribe("Example", "ARepository", lambda event: delivered.append("A"), priority=20)
    bus.subscribe("Example", "CriticalRepository", lambda event: delivered.append("Critical"), priority=10)
    event = bus.publish(Event(event_type="Example", publisher="Test", payload={}))

    assert delivered == ["Critical", "A", "B"]
    assert [status.subscriber for status in bus.get_delivery_status(event.event_id)] == [
        "CriticalRepository",
        "ARepository",
        "BRepository",
    ]
    assert all(status.status == "DELIVERED" for status in bus.get_delivery_status(event.event_id))


def test_event_replay_is_side_effect_free_and_ordered() -> None:
    bus = EventBus()
    first = bus.publish(Event(event_type="Example", publisher="Test", payload={"n": 1}))
    second = bus.publish(Event(event_type="Example", publisher="Test", payload={"n": 2}))

    assert [event.event_id for event in bus.replay_events("Example")] == [first.event_id, second.event_id]
    assert bus.get_delivery_status() == ()


def test_event_bus_records_failed_delivery_status() -> None:
    bus = EventBus()

    def fail(_: Event) -> None:
        raise RuntimeError("subscriber failed")

    bus.subscribe("Example", "BrokenRepository", fail)
    event = Event(event_type="Example", publisher="Test", payload={})

    try:
        bus.publish(event)
    except DeliveryFailure as exc:
        assert exc.context["subscriber"] == "BrokenRepository"
    else:
        raise AssertionError("delivery failure was not raised")

    statuses = bus.get_delivery_status(event.event_id)
    assert len(statuses) == 1
    assert statuses[0].status == "FAILED"
    assert statuses[0].error == "subscriber failed"


def test_event_bus_validates_unsubscribe_and_duplicate_events() -> None:
    bus = EventBus()
    subscription = bus.subscribe("Example", "Repository", lambda event: None)
    bus.unsubscribe(subscription)

    try:
        bus.unsubscribe(subscription)
    except SubscriptionError:
        pass
    else:
        raise AssertionError("missing subscription was accepted")

    event = Event(event_type="Example", publisher="Test", payload={})
    bus.publish(event)
    try:
        bus.publish(event)
    except EventValidationError as exc:
        assert exc.context["event_id"] == event.event_id
    else:
        raise AssertionError("duplicate event was accepted")


def test_event_bus_metrics_health_and_replay_dispatch() -> None:
    delivered: list[int] = []
    bus = EventBus()
    bus.subscribe("Example", "Repository", lambda event: delivered.append(int(event.payload["n"])))
    bus.publish(Event(event_type="Example", publisher="Test", payload={"n": 1}))
    bus.publish(Event(event_type="Example", publisher="Test", payload={"n": 2}))

    replayed = bus.replay_events("Example", dispatch=True)
    metrics = bus.metrics()
    health = bus.health()

    assert [event.payload["n"] for event in replayed] == [1, 2]
    assert delivered == [1, 2, 1, 2]
    assert metrics.metrics["events_published"] == 2.0
    assert metrics.metrics["events_delivered"] == 4.0
    assert metrics.metrics["replay_count"] == 2.0
    assert health.repository == "EventBus"
