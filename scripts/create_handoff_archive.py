#!/usr/bin/env python3
"""Create a deterministic Atlas handoff ZIP archive outside the repository."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from atlas.handoff import create_handoff_archive


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[1]
    output_path = Path("/workspace") / "Atlas-Ai-final-handoff.zip"
    manifest = create_handoff_archive(repo_root, output_path)
    print(output_path)
    print(manifest.archive_sha256)
