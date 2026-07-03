# PortfolioRepository

This top-level directory is the architecture-visible home for `PortfolioRepository` in the hybrid Atlas repository layout.

## Implementation Location

Runtime Python implementation lives in:

```text
atlas/portfolio/
```

## Purpose

Keep the Atlas v1.0 frozen repository set visible at the repository root while preserving the importable Python package namespace under `atlas/`.

## Canonical Rule

- Architecture-visible repository path: `portfolio/`
- Importable Python implementation path: `atlas/portfolio/`
- Public interface definitions: `atlas/portfolio/interfaces.py`
- Service implementation boundary: `atlas/portfolio/services.py`
- Version metadata: `atlas/portfolio/version.py`

This directory SHALL NOT introduce a second implementation. It documents and anchors repository ownership while the implementation remains centralized in the `atlas` Python package.
