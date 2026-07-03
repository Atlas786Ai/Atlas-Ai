# PredictionRepository

This top-level directory is the architecture-visible home for `PredictionRepository` in the hybrid Atlas repository layout.

## Implementation Location

Runtime Python implementation lives in:

```text
atlas/prediction/
```

## Purpose

Keep the Atlas v1.0 frozen repository set visible at the repository root while preserving the importable Python package namespace under `atlas/`.

## Canonical Rule

- Architecture-visible repository path: `prediction/`
- Importable Python implementation path: `atlas/prediction/`
- Public interface definitions: `atlas/prediction/interfaces.py`
- Service implementation boundary: `atlas/prediction/services.py`
- Version metadata: `atlas/prediction/version.py`

This directory SHALL NOT introduce a second implementation. It documents and anchors repository ownership while the implementation remains centralized in the `atlas` Python package.
