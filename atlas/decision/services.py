"""Business service boundary for DecisionRepository.

Module Name: atlas.decision.services
Purpose: Implement the frozen public service API for DecisionRepository.
Owner: Atlas Governance
Version: 1.0.0
Dependencies: atlas.repository_base
Architecture Layer: Repository
"""

from atlas.repository_base import RepositoryBase
from atlas.decision.validators import validate_payload


class DecisionRepository(RepositoryBase):
    """Frozen Atlas v1.0 repository implementation for DecisionRepository."""

    repository_name = "DecisionRepository"
    public_interfaces = ('evaluate_decision', 'select_plan', 'validate_decision', 'archive_decision', 'load_decision', 'get_decision')
    event_types = ('EvaluateDecision', 'SelectPlan', 'ValidateDecision', 'ArchiveDecision', 'LoadDecision')

    def evaluate_decision(self, *args: object, **kwargs: object) -> object:
        """Implement the frozen `evaluate_decision` public interface."""
        return self._store_and_event("EvaluateDecision", kwargs.get("key", "evaluate_decision"), {"operation": "evaluate_decision", "args": list(args), "kwargs": kwargs})

    def select_plan(self, *args: object, **kwargs: object) -> object:
        """Implement the frozen `select_plan` public interface."""
        return self._store_and_event("SelectPlan", kwargs.get("key", "select_plan"), {"operation": "select_plan", "args": list(args), "kwargs": kwargs})

    def validate_decision(self, *args: object, **kwargs: object) -> object:
        """Implement the frozen `validate_decision` public interface."""
        validate_payload(kwargs.get("payload", {}))
        return True

    def archive_decision(self, *args: object, **kwargs: object) -> object:
        """Implement the frozen `archive_decision` public interface."""
        return self._store_and_event("ArchiveDecision", kwargs.get("key", "archive_decision"), {"operation": "archive_decision", "args": list(args), "kwargs": kwargs})

    def load_decision(self, *args: object, **kwargs: object) -> object:
        """Implement the frozen `load_decision` public interface."""
        return {"repository": self.repository_name, "operation": "load_decision", "args": args, "kwargs": kwargs}

    def get_decision(self, *args: object, **kwargs: object) -> object:
        """Implement the frozen `get_decision` public interface."""
        return {"repository": self.repository_name, "operation": "get_decision", "args": args, "kwargs": kwargs}

