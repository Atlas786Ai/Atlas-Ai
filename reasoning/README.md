# ReasoningRepository

This top-level directory is the architecture-visible home for `ReasoningRepository` in the hybrid Atlas repository layout.

## Implementation Location

Runtime Python implementation lives in:

```text
atlas/reasoning/
```

## Purpose

Keep the Atlas v1.0 frozen repository set visible at the repository root while preserving the importable Python package namespace under `atlas/`.

## Canonical Rule

- Architecture-visible repository path: `reasoning/`
- Importable Python implementation path: `atlas/reasoning/`
- Public interface definitions: `atlas/reasoning/interfaces.py`
- Service implementation boundary: `atlas/reasoning/services.py`
- Version metadata: `atlas/reasoning/version.py`

This directory SHALL NOT introduce a second implementation. It documents and anchors repository ownership while the implementation remains centralized in the `atlas` Python package.
