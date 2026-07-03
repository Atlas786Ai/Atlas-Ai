# PlanningRepository

This top-level directory is the architecture-visible home for `PlanningRepository` in the hybrid Atlas repository layout.

## Implementation Location

Runtime Python implementation lives in:

```text
atlas/planning/
```

## Purpose

Keep the Atlas v1.0 frozen repository set visible at the repository root while preserving the importable Python package namespace under `atlas/`.

## Canonical Rule

- Architecture-visible repository path: `planning/`
- Importable Python implementation path: `atlas/planning/`
- Public interface definitions: `atlas/planning/interfaces.py`
- Service implementation boundary: `atlas/planning/services.py`
- Version metadata: `atlas/planning/version.py`

This directory SHALL NOT introduce a second implementation. It documents and anchors repository ownership while the implementation remains centralized in the `atlas` Python package.
