"""Deterministic workspace handoff archive utilities.

Module Name: atlas.handoff
Purpose: Create reproducible ZIP archives for manual GitHub transfer when direct
network operations are unavailable.
Owner: Atlas Governance
Version: 1.0.0
Dependencies: dataclasses, hashlib, json, pathlib, zipfile
Architecture Layer: Governance / Transfer
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

DEFAULT_EXCLUDE_PARTS = frozenset({".git", ".venv", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"})
DEFAULT_EXCLUDE_SUFFIXES = (".pyc", ".pyo", ".zip")
FIXED_ZIP_TIMESTAMP = (2026, 1, 1, 0, 0, 0)


@dataclass(frozen=True)
class HandoffFile:
    """Immutable manifest entry for one archived file."""

    path: str
    size: int
    sha256: str


@dataclass(frozen=True)
class HandoffManifest:
    """Immutable manifest for one handoff archive."""

    project: str
    version: str
    file_count: int
    total_bytes: int
    archive_sha256: str
    files: tuple[HandoffFile, ...]

    def to_json(self) -> str:
        """Serialize the manifest deterministically."""
        return json.dumps(asdict(self), indent=2, sort_keys=True) + "\n"


def should_include(path: Path, root: Path) -> bool:
    """Return whether a path should be included in a handoff archive."""
    relative = path.relative_to(root)
    if any(part in DEFAULT_EXCLUDE_PARTS for part in relative.parts):
        return False
    if path.suffix in DEFAULT_EXCLUDE_SUFFIXES:
        return False
    if not path.is_file():
        return False
    return True


def iter_handoff_files(root: Path | str) -> tuple[Path, ...]:
    """Return archiveable files in deterministic relative-path order."""
    workspace_root = Path(root).resolve()
    files = [path for path in workspace_root.rglob("*") if should_include(path, workspace_root)]
    return tuple(sorted(files, key=lambda path: path.relative_to(workspace_root).as_posix()))


def file_sha256(path: Path) -> str:
    """Return the SHA-256 digest for a file."""
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_file_manifest(root: Path | str) -> tuple[HandoffFile, ...]:
    """Build deterministic file manifest entries for the workspace."""
    workspace_root = Path(root).resolve()
    entries: list[HandoffFile] = []
    for path in iter_handoff_files(workspace_root):
        entries.append(
            HandoffFile(
                path=path.relative_to(workspace_root).as_posix(),
                size=path.stat().st_size,
                sha256=file_sha256(path),
            )
        )
    return tuple(entries)


def create_handoff_archive(root: Path | str, output_path: Path | str, *, project: str = "Atlas-Ai") -> HandoffManifest:
    """Create a deterministic ZIP handoff archive and return its manifest."""
    workspace_root = Path(root).resolve()
    archive_path = Path(output_path).resolve()
    archive_path.parent.mkdir(parents=True, exist_ok=True)

    files = build_file_manifest(workspace_root)
    with ZipFile(archive_path, "w", compression=ZIP_DEFLATED) as archive:
        for entry in files:
            source = workspace_root / entry.path
            zip_info = ZipInfo(filename=f"{project}/{entry.path}", date_time=FIXED_ZIP_TIMESTAMP)
            zip_info.compress_type = ZIP_DEFLATED
            zip_info.external_attr = 0o644 << 16
            archive.writestr(zip_info, source.read_bytes())

    archive_digest = file_sha256(archive_path)
    manifest = HandoffManifest(
        project=project,
        version="1.0.0",
        file_count=len(files),
        total_bytes=sum(entry.size for entry in files),
        archive_sha256=archive_digest,
        files=files,
    )
    manifest_path = archive_path.with_suffix(archive_path.suffix + ".manifest.json")
    manifest_path.write_text(manifest.to_json(), encoding="utf-8")
    return manifest
