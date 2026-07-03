# RuntimeRepository

This top-level directory is the architecture-visible home for `RuntimeRepository` in the hybrid Atlas repository layout.

## Implementation Location

Runtime Python implementation lives in:

```text
atlas/runtime/
```

## Purpose

Keep the Atlas v1.0 frozen repository set visible at the repository root while preserving the importable Python package namespace under `atlas/`.

## Canonical Rule

- Architecture-visible repository path: `runtime/`
- Importable Python implementation path: `atlas/runtime/`
- Public interface definitions: `atlas/runtime/interfaces.py`
- Service implementation boundary: `atlas/runtime/services.py`
- Version metadata: `atlas/runtime/version.py`

This directory SHALL NOT introduce a second implementation. It documents and anchors repository ownership while the implementation remains centralized in the `atlas` Python package.
