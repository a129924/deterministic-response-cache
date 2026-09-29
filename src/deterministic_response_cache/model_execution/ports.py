# Copyright (c) 2026 deterministic-response-cache contributors
# ruff: noqa: INP001

"""Synchronous ports required by the Model Execution boundary."""

from typing import Protocol

from deterministic_response_cache.model_execution.outcomes import (
    InvocationOutcome,
    RuntimePreparationOutcome,
    RuntimeResolutionOutcome,
)


class RuntimeAccess[RuntimeRequestT, RuntimeT](Protocol):
    """Resolve or prepare runtimes for opaque execution requests."""

    def resolve(self, request: RuntimeRequestT) -> RuntimeResolutionOutcome[RuntimeT]:
        """Return the current runtime state for a request."""
        ...

    def prepare(self, request: RuntimeRequestT) -> RuntimePreparationOutcome[RuntimeT]:
        """Prepare a runtime that was explicitly reported missing."""
        ...


class ModelInvoker[RuntimeT, InvocationT, ResponseT](Protocol):
    """Invoke a model through an opaque runtime and request."""

    def invoke(
        self,
        runtime: RuntimeT,
        invocation: InvocationT,
    ) -> InvocationOutcome[ResponseT]:
        """Run one model invocation and return its declared value channel."""
        ...
