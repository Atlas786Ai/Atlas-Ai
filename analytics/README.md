# AnalyticsRepository

This top-level directory is the architecture-visible home for `AnalyticsRepository` in the hybrid Atlas repository layout.

## Implementation Location

Runtime Python implementation lives in:

```text
atlas/analytics/
```

## Purpose

Keep the Atlas v1.0 frozen repository set visible at the repository root while preserving the importable Python package namespace under `atlas/`.

## Canonical Rule

- Architecture-visible repository path: `analytics/`
- Importable Python implementation path: `atlas/analytics/`
- Public interface definitions: `atlas/analytics/interfaces.py`
- Service implementation boundary: `atlas/analytics/services.py`
- Version metadata: `atlas/analytics/version.py`

This directory SHALL NOT introduce a second implementation. It documents and anchors repository ownership while the implementation remains centralized in the `atlas` Python package.
