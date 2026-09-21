# Copyright (c) 2026 deterministic-response-cache contributors
# ruff: noqa: INP001

"""Semantic lookup outcome contracts for reusable runtimes."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Available[RuntimeT]:
    """A reusable runtime is available to a future consumer."""

    runtime: RuntimeT


@dataclass(frozen=True, slots=True)
class Missing:
    """No reusable runtime is retained for the supplied local key."""


@dataclass(frozen=True, slots=True)
class Unavailable:
    """A future consumer may report that lookup could not be completed."""


type LookupOutcome[RuntimeT] = Available[RuntimeT] | Missing | Unavailable
