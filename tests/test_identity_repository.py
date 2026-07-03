"""IdentityRepository service tests for Atlas v1.0."""

from atlas.core.exceptions import AtlasValidationError
from atlas.identity.constants import IDENTITY_ACTIVE, IDENTITY_ARCHIVED
from atlas.identity.services import IdentityRepository


def test_identity_repository_creates_loads_and_validates_identity(tmp_path) -> None:
    repository = IdentityRepository(storage_root=tmp_path)

    record = repository.create_identity(
        "Atlas",
        "Deterministic repository-oriented intelligence",
        traits=("auditable", "deterministic"),
        capabilities=("reasoning", "planning"),
    )
    identity = repository.load_identity()

    assert record["payload"] == identity
    assert identity["name"] == "Atlas"
    assert identity["status"] == IDENTITY_ACTIVE
    assert identity["traits"] == ("auditable", "deterministic")
    assert identity["capabilities"] == ("planning", "reasoning")
    assert identity["integrity_hash"]
    assert repository.validate_identity(identity) is True
    assert repository.identity_exists(identity["identity_id"]) is True


def test_identity_repository_saves_and_gets_identity_payload(tmp_path) -> None:
    repository = IdentityRepository(storage_root=tmp_path)
    record = repository.create_identity("Atlas", "Own identity")
    payload = dict(record["payload"])

    saved = repository.save_identity(payload)
    fetched = repository.get_identity(payload["identity_id"])

    assert saved["payload"] == fetched
    assert fetched["identity_id"] == payload["identity_id"]


def test_identity_repository_archives_identity_without_mutating_original(tmp_path) -> None:
    repository = IdentityRepository(storage_root=tmp_path)
    record = repository.create_identity("Atlas", "Own identity")
    original = record["payload"]

    archive = repository.archive_identity(original["identity_id"])
    loaded = repository.load_identity(original["identity_id"])

    assert archive["payload"]["identity_id"] == original["identity_id"]
    assert archive["payload"]["status"] == IDENTITY_ARCHIVED
    assert loaded["status"] == IDENTITY_ACTIVE


def test_identity_repository_rejects_tampered_identity(tmp_path) -> None:
    repository = IdentityRepository(storage_root=tmp_path)
    record = repository.create_identity("Atlas", "Own identity")
    tampered = dict(record["payload"])
    tampered["purpose"] = "Changed"

    try:
        repository.validate_identity(tampered)
    except AtlasValidationError as exc:
        assert exc.context["identity_id"] == record["payload"]["identity_id"]
    else:
        raise AssertionError("tampered identity was accepted")
