# Copyright (c) 2026 deterministic-response-cache contributors
# ruff: noqa: INP001

"""Caller-facing native model response value object."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ModelResponse[PayloadT]:
    """Hold a native payload without changing its representation."""

    value: PayloadT
