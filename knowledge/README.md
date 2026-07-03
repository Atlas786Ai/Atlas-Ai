# KnowledgeRepository

This top-level directory is the architecture-visible home for `KnowledgeRepository` in the hybrid Atlas repository layout.

## Implementation Location

Runtime Python implementation lives in:

```text
atlas/knowledge/
```

## Purpose

Keep the Atlas v1.0 frozen repository set visible at the repository root while preserving the importable Python package namespace under `atlas/`.

## Canonical Rule

- Architecture-visible repository path: `knowledge/`
- Importable Python implementation path: `atlas/knowledge/`
- Public interface definitions: `atlas/knowledge/interfaces.py`
- Service implementation boundary: `atlas/knowledge/services.py`
- Version metadata: `atlas/knowledge/version.py`

This directory SHALL NOT introduce a second implementation. It documents and anchors repository ownership while the implementation remains centralized in the `atlas` Python package.
