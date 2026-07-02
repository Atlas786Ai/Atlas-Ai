"""Simple deterministic JSON storage adapter.

Module Name: atlas.core.storage
Purpose: Provide append-only and keyed JSON persistence for repository scaffolds.
Owner: Atlas Governance
Version: 1.0.0
Dependencies: json, pathlib
Architecture Layer: Core Infrastructure
"""

import json
from pathlib import Path
from typing import Any

from atlas.core.exceptions import AtlasStorageError


class JsonStorage:
    """Small file-backed storage abstraction used by repositories."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def write(self, key: str, payload: dict[str, Any]) -> None:
        """Write a JSON object under a stable key."""
        path = self.root / f"{key}.json"
        try:
            path.write_text(json.dumps(payload, sort_keys=True, indent=2), encoding="utf-8")
        except OSError as exc:
            raise AtlasStorageError("Unable to write storage object", context={"key": key}) from exc

    def read(self, key: str) -> dict[str, Any]:
        """Read a JSON object by key."""
        path = self.root / f"{key}.json"
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except OSError as exc:
            raise AtlasStorageError("Unable to read storage object", context={"key": key}) from exc
