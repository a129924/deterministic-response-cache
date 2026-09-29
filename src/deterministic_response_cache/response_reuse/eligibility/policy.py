# Copyright (c) 2026 deterministic-response-cache contributors
# ruff: noqa: INP001

"""Eligibility contracts for safely reusing stored responses."""

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class ReuseAllowed:
    """A stored response is safe to return as a cache hit."""


@dataclass(frozen=True, slots=True)
class ReuseDenied:
    """A stored response must not be returned as a cache hit."""


type ReuseEligibilityDecision = ReuseAllowed | ReuseDenied


class ReuseEligibilityPolicy[ResponseT](Protocol):
    """Evaluate whether a stored response is eligible for reuse."""

    def evaluate(self, response: ResponseT, /) -> ReuseEligibilityDecision:
        """Return the explicit reuse decision for the supplied response."""
        ...
