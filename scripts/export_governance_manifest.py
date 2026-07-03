#!/usr/bin/env python3
"""Write the Atlas governance manifest to a deterministic JSON file."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from atlas.governance import write_manifest


if __name__ == "__main__":
    output = write_manifest(Path("docs") / "architecture_manifest.json")
    print(output)
