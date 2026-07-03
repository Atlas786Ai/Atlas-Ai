# IdentityRepository

This top-level directory is the architecture-visible home for `IdentityRepository` in the hybrid Atlas repository layout.

## Implementation Location

Runtime Python implementation lives in:

```text
atlas/identity/
```

## Purpose

Keep the Atlas v1.0 frozen repository set visible at the repository root while preserving the importable Python package namespace under `atlas/`.

## Canonical Rule

- Architecture-visible repository path: `identity/`
- Importable Python implementation path: `atlas/identity/`
- Public interface definitions: `atlas/identity/interfaces.py`
- Service implementation boundary: `atlas/identity/services.py`
- Version metadata: `atlas/identity/version.py`

This directory SHALL NOT introduce a second implementation. It documents and anchors repository ownership while the implementation remains centralized in the `atlas` Python package.
