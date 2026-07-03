# SecurityRepository

This top-level directory is the architecture-visible home for `SecurityRepository` in the hybrid Atlas repository layout.

## Implementation Location

Runtime Python implementation lives in:

```text
atlas/security/
```

## Purpose

Keep the Atlas v1.0 frozen repository set visible at the repository root while preserving the importable Python package namespace under `atlas/`.

## Canonical Rule

- Architecture-visible repository path: `security/`
- Importable Python implementation path: `atlas/security/`
- Public interface definitions: `atlas/security/interfaces.py`
- Service implementation boundary: `atlas/security/services.py`
- Version metadata: `atlas/security/version.py`

This directory SHALL NOT introduce a second implementation. It documents and anchors repository ownership while the implementation remains centralized in the `atlas` Python package.
