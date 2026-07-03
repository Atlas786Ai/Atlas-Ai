# MonitoringRepository

This top-level directory is the architecture-visible home for `MonitoringRepository` in the hybrid Atlas repository layout.

## Implementation Location

Runtime Python implementation lives in:

```text
atlas/monitoring/
```

## Purpose

Keep the Atlas v1.0 frozen repository set visible at the repository root while preserving the importable Python package namespace under `atlas/`.

## Canonical Rule

- Architecture-visible repository path: `monitoring/`
- Importable Python implementation path: `atlas/monitoring/`
- Public interface definitions: `atlas/monitoring/interfaces.py`
- Service implementation boundary: `atlas/monitoring/services.py`
- Version metadata: `atlas/monitoring/version.py`

This directory SHALL NOT introduce a second implementation. It documents and anchors repository ownership while the implementation remains centralized in the `atlas` Python package.
