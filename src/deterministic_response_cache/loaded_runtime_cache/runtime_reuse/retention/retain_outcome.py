# Copyright (c) 2026 deterministic-response-cache contributors
# ruff: noqa: INP001

"""Semantic retention outcomes owned by the Loaded Runtime Cache boundary."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Retained[RuntimeT]:
    """The runtime remains available after successful retention."""

    runtime: RuntimeT


@dataclass(frozen=True, slots=True)
class NotRetained[RuntimeT]:
    """The runtime remains available even though retention did not succeed."""

    runtime: RuntimeT


type RetentionOutcome[RuntimeT] = Retained[RuntimeT] | NotRetained[RuntimeT]
