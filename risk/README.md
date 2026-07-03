# RiskRepository

This top-level directory is the architecture-visible home for `RiskRepository` in the hybrid Atlas repository layout.

## Implementation Location

Runtime Python implementation lives in:

```text
atlas/risk/
```

## Purpose

Keep the Atlas v1.0 frozen repository set visible at the repository root while preserving the importable Python package namespace under `atlas/`.

## Canonical Rule

- Architecture-visible repository path: `risk/`
- Importable Python implementation path: `atlas/risk/`
- Public interface definitions: `atlas/risk/interfaces.py`
- Service implementation boundary: `atlas/risk/services.py`
- Version metadata: `atlas/risk/version.py`

This directory SHALL NOT introduce a second implementation. It documents and anchors repository ownership while the implementation remains centralized in the `atlas` Python package.
