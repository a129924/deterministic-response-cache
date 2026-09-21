# Copyright (c) 2026 deterministic-response-cache contributors
# ruff: noqa: INP001

"""Outcome-facing protocol for retaining initialized runtimes."""

from typing import Protocol

from deterministic_response_cache.loaded_runtime_cache.runtime_reuse.registry.runtime_reuse_key import (  # noqa: E501
    RuntimeReuseKey,
)

from .retain_outcome import NotRetained, Retained


class RuntimeRetention[RuntimeT](Protocol):
    """Attempt retention while preserving the runtime in every outcome."""

    def retain(
        self,
        key: RuntimeReuseKey,
        runtime: RuntimeT,
    ) -> Retained[RuntimeT] | NotRetained[RuntimeT]:
        """Return a retention outcome without creating or managing the runtime."""
        ...
