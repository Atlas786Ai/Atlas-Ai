"""Governance utilities for the frozen Atlas v1.0 architecture.

Module Name: atlas.governance
Purpose: Validate constitutional repository boundaries and produce a deterministic
architecture manifest for handoff, audit, and runtime registration.
Owner: Atlas Governance
Version: 1.0.0
Dependencies: dataclasses, importlib, json, pathlib, atlas.architecture
Architecture Layer: Governance
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import importlib
import json
from pathlib import Path
from typing import Any

from atlas.architecture import BOOT_SEQUENCE, FROZEN_REPOSITORIES

REQUIRED_REPOSITORY_MODULES = (
    "__init__",
    "config",
    "constants",
    "events",
    "exceptions",
    "health",
    "interfaces",
    "mappers",
    "metrics",
    "models",
    "schemas",
    "serializers",
    "services",
    "validators",
    "version",
)

REQUIRED_ROOT_ANCHORS = ("README.md", "IMPLEMENTATION.md")


@dataclass(frozen=True)
class RepositoryContract:
    """Immutable constitutional contract for one frozen Atlas repository."""

    name: str
    slug: str
    package: str
    root_anchor: str
    public_interfaces: tuple[str, ...]
    event_types: tuple[str, ...]
    required_modules: tuple[str, ...] = REQUIRED_REPOSITORY_MODULES


def repository_slug(repository_name: str) -> str:
    """Convert a frozen repository class name into its deterministic package slug."""
    base_name = repository_name.removesuffix("Repository")
    if base_name == "CognitiveContext":
        return "cognitive_context"
    return "".join([f"_{char.lower()}" if char.isupper() else char for char in base_name]).lstrip("_")


def load_contract(repository_name: str) -> RepositoryContract:
    """Load one repository contract from its implementation package."""
    slug = repository_slug(repository_name)
    module = importlib.import_module(f"atlas.{slug}.services")
    repository_cls = getattr(module, repository_name)
    return RepositoryContract(
        name=repository_name,
        slug=slug,
        package=f"atlas.{slug}",
        root_anchor=slug,
        public_interfaces=tuple(repository_cls.public_interfaces),
        event_types=tuple(repository_cls.event_types),
    )


def frozen_contracts() -> tuple[RepositoryContract, ...]:
    """Return all frozen repository contracts in canonical architecture order."""
    return tuple(load_contract(repository_name) for repository_name in FROZEN_REPOSITORIES)


def architecture_manifest() -> dict[str, Any]:
    """Build a deterministic JSON-serializable architecture manifest."""
    contracts = frozen_contracts()
    return {
        "architecture": "Atlas",
        "version": "1.0.0",
        "status": "frozen",
        "repository_count": len(contracts),
        "repositories": [asdict(contract) for contract in contracts],
        "boot_sequence": BOOT_SEQUENCE,
        "rules": [
            "one_repository_owns_one_domain",
            "public_interfaces_or_event_bus_only",
            "immutable_boundary_objects",
            "deterministic_import_paths",
            "runtime_registration_required",
        ],
    }


def validate_workspace(root: Path | str = Path(".")) -> list[str]:
    """Return deterministic governance violations for the workspace, if any."""
    workspace_root = Path(root)
    violations: list[str] = []

    for contract in frozen_contracts():
        package_root = workspace_root / "atlas" / contract.slug
        root_anchor = workspace_root / contract.root_anchor

        for anchor_file in REQUIRED_ROOT_ANCHORS:
            if not (root_anchor / anchor_file).is_file():
                violations.append(f"missing_root_anchor:{contract.slug}/{anchor_file}")

        for module_name in contract.required_modules:
            module_path = package_root / f"{module_name}.py"
            if module_name == "__init__":
                module_path = package_root / "__init__.py"
            if not module_path.is_file():
                violations.append(f"missing_module:atlas/{contract.slug}/{module_path.name}")

        if not contract.public_interfaces:
            violations.append(f"missing_public_interfaces:{contract.name}")

    return sorted(violations)


def write_manifest(path: Path | str, root: Path | str = Path(".")) -> Path:
    """Write the deterministic governance manifest to disk after validation."""
    violations = validate_workspace(root)
    if violations:
        raise ValueError("Atlas governance violations: " + ", ".join(violations))

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = architecture_manifest()
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output_path
