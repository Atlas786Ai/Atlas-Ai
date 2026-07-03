"""Public interface contracts for ReasoningRepository."""

from typing import Protocol


class ReasoningRepositoryInterface(Protocol):
    def reason(self, *args: object, **kwargs: object) -> object:
        """reason contract."""
        ...

    def generate_hypotheses(self, *args: object, **kwargs: object) -> object:
        """generate_hypotheses contract."""
        ...

    def evaluate_hypotheses(self, *args: object, **kwargs: object) -> object:
        """evaluate_hypotheses contract."""
        ...

    def rank_candidates(self, *args: object, **kwargs: object) -> object:
        """rank_candidates contract."""
        ...

    def validate_reasoning(self, *args: object, **kwargs: object) -> object:
        """validate_reasoning contract."""
        ...

    def archive_reasoning(self, *args: object, **kwargs: object) -> object:
        """archive_reasoning contract."""
        ...

    def load_reasoning(self, *args: object, **kwargs: object) -> object:
        """load_reasoning contract."""
        ...

