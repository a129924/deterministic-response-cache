# Copyright (c) 2026 deterministic-response-cache contributors
# ruff: noqa: INP001

"""Semantic retention outcome contracts for reusable runtimes."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Retained[RuntimeT]:
    """The caller's runtime was retained and remains available to that caller."""

    runtime: RuntimeT


@dataclass(frozen=True, slots=True)
class NotRetained[RuntimeT]:
    """The caller keeps its runtime after an unsuccessful retention attempt."""

    runtime: RuntimeT


type RetentionOutcome[RuntimeT] = Retained[RuntimeT] | NotRetained[RuntimeT]
