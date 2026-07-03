"""Handoff archive tests for manual Atlas transfer."""

import json
from zipfile import ZipFile

from atlas.handoff import build_file_manifest, create_handoff_archive, iter_handoff_files, should_include


def test_should_include_excludes_git_and_cache(tmp_path) -> None:
    root = tmp_path
    source = root / "atlas" / "module.py"
    source.parent.mkdir(parents=True)
    source.write_text("print('atlas')\n", encoding="utf-8")
    git_file = root / ".git" / "config"
    git_file.parent.mkdir()
    git_file.write_text("ignored", encoding="utf-8")
    pycache_file = root / "atlas" / "__pycache__" / "module.pyc"
    pycache_file.parent.mkdir()
    pycache_file.write_bytes(b"ignored")

    assert should_include(source, root)
    assert not should_include(git_file, root)
    assert not should_include(pycache_file, root)


def test_iter_handoff_files_is_deterministic(tmp_path) -> None:
    root = tmp_path
    for relative_path in ("b.txt", "a.txt", "nested/c.txt"):
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(relative_path, encoding="utf-8")

    assert [path.relative_to(root).as_posix() for path in iter_handoff_files(root)] == ["a.txt", "b.txt", "nested/c.txt"]


def test_build_file_manifest_includes_checksum(tmp_path) -> None:
    source = tmp_path / "README.md"
    source.write_text("Atlas\n", encoding="utf-8")

    manifest = build_file_manifest(tmp_path)
    assert manifest[0].path == "README.md"
    assert manifest[0].size == len("Atlas\n")
    assert len(manifest[0].sha256) == 64


def test_create_handoff_archive_writes_zip_and_manifest(tmp_path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    (root / "README.md").write_text("Atlas\n", encoding="utf-8")
    (root / "atlas").mkdir()
    (root / "atlas" / "__init__.py").write_text("\n", encoding="utf-8")

    output = tmp_path / "handoff.zip"
    manifest = create_handoff_archive(root, output, project="Atlas-Test")

    assert output.is_file()
    assert output.with_suffix(".zip.manifest.json").is_file()
    assert manifest.file_count == 2
    assert len(manifest.archive_sha256) == 64
    with ZipFile(output) as archive:
        assert archive.namelist() == ["Atlas-Test/README.md", "Atlas-Test/atlas/__init__.py"]
    persisted = json.loads(output.with_suffix(".zip.manifest.json").read_text(encoding="utf-8"))
    assert persisted["archive_sha256"] == manifest.archive_sha256
