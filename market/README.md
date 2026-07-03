# MarketRepository

This top-level directory is the architecture-visible home for `MarketRepository` in the hybrid Atlas repository layout.

## Implementation Location

Runtime Python implementation lives in:

```text
atlas/market/
```

## Purpose

Keep the Atlas v1.0 frozen repository set visible at the repository root while preserving the importable Python package namespace under `atlas/`.

## Canonical Rule

- Architecture-visible repository path: `market/`
- Importable Python implementation path: `atlas/market/`
- Public interface definitions: `atlas/market/interfaces.py`
- Service implementation boundary: `atlas/market/services.py`
- Version metadata: `atlas/market/version.py`

This directory SHALL NOT introduce a second implementation. It documents and anchors repository ownership while the implementation remains centralized in the `atlas` Python package.
