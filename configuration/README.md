# ConfigurationRepository

This top-level directory is the architecture-visible home for `ConfigurationRepository` in the hybrid Atlas repository layout.

## Implementation Location

Runtime Python implementation lives in:

```text
atlas/configuration/
```

## Purpose

Keep the Atlas v1.0 frozen repository set visible at the repository root while preserving the importable Python package namespace under `atlas/`.

## Canonical Rule

- Architecture-visible repository path: `configuration/`
- Importable Python implementation path: `atlas/configuration/`
- Public interface definitions: `atlas/configuration/interfaces.py`
- Service implementation boundary: `atlas/configuration/services.py`
- Version metadata: `atlas/configuration/version.py`

This directory SHALL NOT introduce a second implementation. It documents and anchors repository ownership while the implementation remains centralized in the `atlas` Python package.
