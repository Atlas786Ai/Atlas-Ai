# Atlas Hybrid Repository Layout

Atlas uses a hybrid layout to satisfy both architecture visibility and Python import determinism.

## Architecture-visible root directories

Each frozen Atlas repository has a top-level directory (`identity/`, `mission/`, `knowledge/`, etc.) so the repository set is visible at the root of `Atlas-Ai`.

## Importable implementation package

Executable Python implementation lives under `atlas/` so imports remain stable and namespaced:

```python
from atlas.identity.services import IdentityRepository
```

## No duplicate implementation

Root-level directories are ownership and documentation anchors. The canonical implementation for each repository remains under `atlas/<repository>/`.
