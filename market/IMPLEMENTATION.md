# MarketRepository Implementation Mapping

`MarketRepository` is implemented under `atlas/market/` to keep imports deterministic and package-scoped.

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

This top-level directory owns the architecture identity of `MarketRepository`. Code changes must be made in `atlas/market/` unless a governance-approved future version changes the repository layout.
