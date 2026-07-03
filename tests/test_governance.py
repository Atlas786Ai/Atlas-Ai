"""Governance validation tests for the frozen Atlas v1.0 constitution."""

import json

from atlas.architecture import FROZEN_REPOSITORIES
from atlas.governance import architecture_manifest, frozen_contracts, repository_slug, validate_workspace, write_manifest


def test_repository_slug_is_deterministic() -> None:
    assert repository_slug("IdentityRepository") == "identity"
    assert repository_slug("CognitiveContextRepository") == "cognitive_context"
    assert repository_slug("RuntimeRepository") == "runtime"


def test_frozen_contracts_match_architecture_order() -> None:
    contracts = frozen_contracts()
    assert tuple(contract.name for contract in contracts) == tuple(FROZEN_REPOSITORIES)
    assert all(contract.public_interfaces for contract in contracts)
    assert all(contract.package.startswith("atlas.") for contract in contracts)


def test_workspace_has_no_governance_violations() -> None:
    assert validate_workspace(".") == []


def test_architecture_manifest_is_json_serializable() -> None:
    manifest = architecture_manifest()
    assert manifest["architecture"] == "Atlas"
    assert manifest["status"] == "frozen"
    assert manifest["repository_count"] == len(FROZEN_REPOSITORIES)
    assert json.loads(json.dumps(manifest, sort_keys=True))["repository_count"] == len(FROZEN_REPOSITORIES)


def test_write_manifest_outputs_deterministic_json(tmp_path) -> None:
    output = write_manifest(tmp_path / "manifest.json", ".")
    manifest = json.loads(output.read_text(encoding="utf-8"))
    assert manifest["repository_count"] == len(FROZEN_REPOSITORIES)
    assert [repository["name"] for repository in manifest["repositories"]] == FROZEN_REPOSITORIES
