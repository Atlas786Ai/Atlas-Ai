# MissionRepository

This top-level directory is the architecture-visible home for `MissionRepository` in the hybrid Atlas repository layout.

## Implementation Location

Runtime Python implementation lives in:

```text
atlas/mission/
```

## Purpose

Keep the Atlas v1.0 frozen repository set visible at the repository root while preserving the importable Python package namespace under `atlas/`.

## Canonical Rule

- Architecture-visible repository path: `mission/`
- Importable Python implementation path: `atlas/mission/`
- Public interface definitions: `atlas/mission/interfaces.py`
- Service implementation boundary: `atlas/mission/services.py`
- Version metadata: `atlas/mission/version.py`

This directory SHALL NOT introduce a second implementation. It documents and anchors repository ownership while the implementation remains centralized in the `atlas` Python package.
