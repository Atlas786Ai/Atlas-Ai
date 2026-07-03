"""EventBus deterministic behavior tests."""

from atlas.core.models import Event
from atlas.event_bus import EventBus


def test_event_bus_delivers_by_priority_then_repository() -> None:
    delivered: list[str] = []
    bus = EventBus()
    bus.subscribe("Example", "BRepository", lambda event: delivered.append("B"), priority=20)
    bus.subscribe("Example", "ARepository", lambda event: delivered.append("A"), priority=20)
    bus.subscribe("Example", "CriticalRepository", lambda event: delivered.append("Critical"), priority=10)
    bus.publish(Event(event_type="Example", publisher="Test", payload={}))
    assert delivered == ["Critical", "A", "B"]


def test_event_replay_is_side_effect_free_and_ordered() -> None:
    bus = EventBus()
    first = bus.publish(Event(event_type="Example", publisher="Test", payload={"n": 1}))
    second = bus.publish(Event(event_type="Example", publisher="Test", payload={"n": 2}))
    assert [event.event_id for event in bus.replay_events("Example")] == [first.event_id, second.event_id]
