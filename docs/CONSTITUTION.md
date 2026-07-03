# Atlas v1.0 Constitutional Execution Rules

Atlas v1.0 is frozen around deterministic repository boundaries. This document captures the execution rules that every future implementation step must preserve.

## Non-Negotiable Rules

1. **One repository owns one domain.** Domain behavior must remain inside the repository that owns it.
2. **Cross-repository communication is explicit.** Repositories may communicate only through declared public interfaces or the Event Bus.
3. **Boundary objects are immutable.** Events, health reports, metric snapshots, and archived records must be deterministic and immutable after creation.
4. **Runtime registration is mandatory.** Every repository must expose registration metadata through `as_registration()`.
5. **Imports are deterministic.** Executable Python implementations live under `atlas/<repository_slug>/`; root-level directories are ownership anchors.
6. **Infrastructure repositories boot first.** Configuration, Logging, Security, and Audit must initialize before Runtime and domain repositories.

## Workspace Validation

The `atlas.governance` module provides a deterministic validation layer for this constitution. It verifies root ownership anchors, implementation package modules, public interfaces, event declarations, and manifest generation.

## Manual Handoff Rule

When direct GitHub access is unavailable, the workspace may be transferred as a ZIP archive. The handoff archive must exclude `.git/`, virtual environments, caches, and generated Python bytecode.
