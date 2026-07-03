# SimulationRepository

This top-level directory is the architecture-visible home for `SimulationRepository` in the hybrid Atlas repository layout.

## Implementation Location

Runtime Python implementation lives in:

```text
atlas/simulation/
```

## Purpose

Keep the Atlas v1.0 frozen repository set visible at the repository root while preserving the importable Python package namespace under `atlas/`.

## Canonical Rule

- Architecture-visible repository path: `simulation/`
- Importable Python implementation path: `atlas/simulation/`
- Public interface definitions: `atlas/simulation/interfaces.py`
- Service implementation boundary: `atlas/simulation/services.py`
- Version metadata: `atlas/simulation/version.py`

This directory SHALL NOT introduce a second implementation. It documents and anchors repository ownership while the implementation remains centralized in the `atlas` Python package.
