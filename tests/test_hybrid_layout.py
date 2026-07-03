"""Hybrid layout compliance tests for Atlas v1.0."""

from pathlib import Path

from atlas.architecture import FROZEN_REPOSITORIES


ROOT = Path(__file__).resolve().parents[1]


def _slug(repository: str) -> str:
    name = repository.removesuffix("Repository")
    if name == "CognitiveContext":
        return "cognitive_context"
    return ''.join(['_' + char.lower() if char.isupper() else char for char in name]).lstrip('_')


def test_each_frozen_repository_has_root_architecture_anchor() -> None:
    for repository in FROZEN_REPOSITORIES:
        slug = _slug(repository)
        assert (ROOT / slug / "README.md").is_file()
        assert (ROOT / slug / "IMPLEMENTATION.md").is_file()
        assert (ROOT / slug / "docs").is_dir()
        assert (ROOT / slug / "tests").is_dir()


def test_each_root_anchor_points_to_importable_package() -> None:
    for repository in FROZEN_REPOSITORIES:
        slug = _slug(repository)
        readme = (ROOT / slug / "README.md").read_text(encoding="utf-8")
        assert f"atlas/{slug}/" in readme
        assert (ROOT / "atlas" / slug / "services.py").is_file()
