# Copyright (c) 2026 deterministic-response-cache contributors
# ruff: noqa: INP001

"""Semantic lookup outcomes owned by the Loaded Runtime Cache boundary."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Available[RuntimeT]:
    """A reusable runtime is available."""

    runtime: RuntimeT


@dataclass(frozen=True, slots=True)
class Missing:
    """No reusable runtime is available for the local key."""


@dataclass(frozen=True, slots=True)
class Unavailable:
    """A future boundary consumer may report an unavailable lookup."""


type LookupOutcome[RuntimeT] = Available[RuntimeT] | Missing | Unavailable
