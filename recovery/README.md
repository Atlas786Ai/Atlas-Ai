# RecoveryRepository

This top-level directory is the architecture-visible home for `RecoveryRepository` in the hybrid Atlas repository layout.

## Implementation Location

Runtime Python implementation lives in:

```text
atlas/recovery/
```

## Purpose

Keep the Atlas v1.0 frozen repository set visible at the repository root while preserving the importable Python package namespace under `atlas/`.

## Canonical Rule

- Architecture-visible repository path: `recovery/`
- Importable Python implementation path: `atlas/recovery/`
- Public interface definitions: `atlas/recovery/interfaces.py`
- Service implementation boundary: `atlas/recovery/services.py`
- Version metadata: `atlas/recovery/version.py`

This directory SHALL NOT introduce a second implementation. It documents and anchors repository ownership while the implementation remains centralized in the `atlas` Python package.
