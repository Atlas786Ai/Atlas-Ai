# CognitiveContextRepository

This top-level directory is the architecture-visible home for `CognitiveContextRepository` in the hybrid Atlas repository layout.

## Implementation Location

Runtime Python implementation lives in:

```text
atlas/cognitive_context/
```

## Purpose

Keep the Atlas v1.0 frozen repository set visible at the repository root while preserving the importable Python package namespace under `atlas/`.

## Canonical Rule

- Architecture-visible repository path: `cognitive_context/`
- Importable Python implementation path: `atlas/cognitive_context/`
- Public interface definitions: `atlas/cognitive_context/interfaces.py`
- Service implementation boundary: `atlas/cognitive_context/services.py`
- Version metadata: `atlas/cognitive_context/version.py`

This directory SHALL NOT introduce a second implementation. It documents and anchors repository ownership while the implementation remains centralized in the `atlas` Python package.
