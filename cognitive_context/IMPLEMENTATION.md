# CognitiveContextRepository Implementation Mapping

`CognitiveContextRepository` is implemented under `atlas/cognitive_context/` to keep imports deterministic and package-scoped.

## Required Canonical Modules

The implementation package includes:

- `README.md`
- `config.py`
- `constants.py`
- `interfaces.py`
- `models.py`
- `schemas.py`
- `services.py`
- `validators.py`
- `serializers.py`
- `mappers.py`
- `events.py`
- `exceptions.py`
- `metrics.py`
- `health.py`
- `version.py`
- `tests/`
- `docs/`

## Ownership

This top-level directory owns the architecture identity of `CognitiveContextRepository`. Code changes must be made in `atlas/cognitive_context/` unless a governance-approved future version changes the repository layout.
