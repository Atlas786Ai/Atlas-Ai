# DecisionRepository

This top-level directory is the architecture-visible home for `DecisionRepository` in the hybrid Atlas repository layout.

## Implementation Location

Runtime Python implementation lives in:

```text
atlas/decision/
```

## Purpose

Keep the Atlas v1.0 frozen repository set visible at the repository root while preserving the importable Python package namespace under `atlas/`.

## Canonical Rule

- Architecture-visible repository path: `decision/`
- Importable Python implementation path: `atlas/decision/`
- Public interface definitions: `atlas/decision/interfaces.py`
- Service implementation boundary: `atlas/decision/services.py`
- Version metadata: `atlas/decision/version.py`

This directory SHALL NOT introduce a second implementation. It documents and anchors repository ownership while the implementation remains centralized in the `atlas` Python package.
