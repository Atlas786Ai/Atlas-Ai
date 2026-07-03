"""MissionRepository service tests for Atlas v1.0."""

from atlas.core.exceptions import AtlasValidationError
from atlas.mission.constants import MISSION_ACTIVE, MISSION_ARCHIVED, REPOSITORY_VERSION
from atlas.mission.services import MissionRepository


def test_mission_repository_creates_loads_and_validates_mission(tmp_path) -> None:
    repository = MissionRepository(storage_root=tmp_path)

    record = repository.create_mission(
        "Protect capital",
        "Maintain deterministic capital preservation mandate",
        constraints=("no leverage", "auditable decisions"),
        success_criteria=("drawdown controlled", "all actions logged"),
        priority="high",
    )
    mission = repository.load_mission()

    assert record["payload"] == mission
    assert mission["title"] == "Protect capital"
    assert mission["status"] == MISSION_ACTIVE
    assert mission["constraints"] == ("auditable decisions", "no leverage")
    assert mission["success_criteria"] == ("all actions logged", "drawdown controlled")
    assert mission["integrity_hash"]
    assert repository.validate_mission(mission) is True
    assert repository.mission_exists(mission["mission_id"]) is True
    assert repository.get_mission_version() == REPOSITORY_VERSION


def test_mission_repository_saves_and_gets_current_mission(tmp_path) -> None:
    repository = MissionRepository(storage_root=tmp_path)
    record = repository.create_mission("Atlas mandate", "Own the operating mission")
    payload = dict(record["payload"])

    saved = repository.save_mission(payload)
    current = repository.get_current_mission()

    assert saved["payload"] == current
    assert current["mission_id"] == payload["mission_id"]


def test_mission_repository_archives_without_mutating_original(tmp_path) -> None:
    repository = MissionRepository(storage_root=tmp_path)
    record = repository.create_mission("Atlas mandate", "Own the operating mission")
    original = record["payload"]

    archive = repository.archive_mission(original["mission_id"])
    loaded = repository.load_mission(original["mission_id"])

    assert archive["payload"]["mission_id"] == original["mission_id"]
    assert archive["payload"]["status"] == MISSION_ARCHIVED
    assert loaded["status"] == MISSION_ACTIVE


def test_mission_repository_rejects_invalid_or_tampered_mission(tmp_path) -> None:
    repository = MissionRepository(storage_root=tmp_path)
    record = repository.create_mission("Atlas mandate", "Own the operating mission")
    tampered = dict(record["payload"])
    tampered["objective"] = "Changed"

    try:
        repository.validate_mission(tampered)
    except AtlasValidationError as exc:
        assert exc.context["mission_id"] == record["payload"]["mission_id"]
    else:
        raise AssertionError("tampered mission was accepted")

    try:
        repository.create_mission("Invalid", "Bad priority", priority="urgent")
    except AtlasValidationError as exc:
        assert exc.context["priority"] == "urgent"
    else:
        raise AssertionError("invalid mission priority was accepted")
