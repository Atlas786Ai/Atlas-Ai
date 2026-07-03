# LoggingRepository

This top-level directory is the architecture-visible home for `LoggingRepository` in the hybrid Atlas repository layout.

## Implementation Location

Runtime Python implementation lives in:

```text
atlas/logging/
```

## Purpose

Keep the Atlas v1.0 frozen repository set visible at the repository root while preserving the importable Python package namespace under `atlas/`.

## Canonical Rule

- Architecture-visible repository path: `logging/`
- Importable Python implementation path: `atlas/logging/`
- Public interface definitions: `atlas/logging/interfaces.py`
- Service implementation boundary: `atlas/logging/services.py`
- Version metadata: `atlas/logging/version.py`

This directory SHALL NOT introduce a second implementation. It documents and anchors repository ownership while the implementation remains centralized in the `atlas` Python package.
