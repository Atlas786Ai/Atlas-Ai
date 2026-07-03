# MemoryRepository

This top-level directory is the architecture-visible home for `MemoryRepository` in the hybrid Atlas repository layout.

## Implementation Location

Runtime Python implementation lives in:

```text
atlas/memory/
```

## Purpose

Keep the Atlas v1.0 frozen repository set visible at the repository root while preserving the importable Python package namespace under `atlas/`.

## Canonical Rule

- Architecture-visible repository path: `memory/`
- Importable Python implementation path: `atlas/memory/`
- Public interface definitions: `atlas/memory/interfaces.py`
- Service implementation boundary: `atlas/memory/services.py`
- Version metadata: `atlas/memory/version.py`

This directory SHALL NOT introduce a second implementation. It documents and anchors repository ownership while the implementation remains centralized in the `atlas` Python package.
