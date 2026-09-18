# Copyright (c) 2026 deterministic-response-cache contributors
# ruff: noqa: INP001

"""Outcome-facing retention protocol for the Loaded Runtime Cache."""

from typing import Protocol

from ..registry.runtime_reuse_key import RuntimeReuseKey  # noqa: TID252
from .retain_outcome import NotRetained, Retained


class RuntimeRetention[RuntimeT](Protocol):
    """Attempt to retain a runtime while preserving it in either outcome."""

    def retain(
        self,
        key: RuntimeReuseKey,
        runtime: RuntimeT,
    ) -> Retained[RuntimeT] | NotRetained[RuntimeT]:
        """Return a retention outcome containing the supplied runtime."""
        ...
