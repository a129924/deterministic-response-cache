# Copyright (c) 2026 deterministic-response-cache contributors
# ruff: noqa: INP001

"""Synchronous orchestration at the Model Execution boundary."""

from deterministic_response_cache.model_execution.outcomes import (
    Executed,
    ExecutionFailed,
    ExecutionFailureReason,
    ExecutionOutcome,
    InvocationFailed,
    InvocationSucceeded,
    RuntimeMissing,
    RuntimePreparationFailed,
    RuntimeReady,
    RuntimeUnavailable,
)
from deterministic_response_cache.model_execution.ports import ModelInvoker, RuntimeAccess


class ModelExecutionProtocol[RuntimeRequestT, RuntimeT, InvocationT, ResponseT]:
    """Coordinate runtime access and one model invocation."""

    def __init__(
        self,
        runtime_access: RuntimeAccess[RuntimeRequestT, RuntimeT],
        invoker: ModelInvoker[RuntimeT, InvocationT, ResponseT],
    ) -> None:
        """Create the protocol with injected runtime and invocation ports."""
        self._runtime_access = runtime_access
        self._invoker = invoker

    def execute(
        self,
        runtime_request: RuntimeRequestT,
        invocation: InvocationT,
    ) -> ExecutionOutcome[ResponseT]:
        """Resolve a runtime and execute one invocation when possible."""
        match self._runtime_access.resolve(runtime_request):
            case RuntimeReady(runtime):
                return self._invoke(runtime, invocation)
            case RuntimeMissing():
                return self._prepare_and_invoke(runtime_request, invocation)
            case RuntimeUnavailable():
                return ExecutionFailed(ExecutionFailureReason.RUNTIME_UNAVAILABLE)
            case _:
                message = "RuntimeAccess.resolve must return a runtime resolution outcome"
                raise TypeError(message)

    def _prepare_and_invoke(
        self,
        runtime_request: RuntimeRequestT,
        invocation: InvocationT,
    ) -> ExecutionOutcome[ResponseT]:
        """Prepare an explicitly missing runtime and invoke when ready."""
        match self._runtime_access.prepare(runtime_request):
            case RuntimeReady(runtime):
                return self._invoke(runtime, invocation)
            case RuntimePreparationFailed():
                return ExecutionFailed(ExecutionFailureReason.RUNTIME_PREPARATION_FAILED)
            case _:
                message = "RuntimeAccess.prepare must return a runtime preparation outcome"
                raise TypeError(message)

    def _invoke(
        self,
        runtime: RuntimeT,
        invocation: InvocationT,
    ) -> ExecutionOutcome[ResponseT]:
        """Invoke once and map its value channel to an execution outcome."""
        match self._invoker.invoke(runtime, invocation):
            case InvocationSucceeded(response):
                return Executed(response)
            case InvocationFailed():
                return ExecutionFailed(ExecutionFailureReason.INVOCATION_FAILED)
            case _:
                message = "ModelInvoker.invoke must return an invocation outcome"
                raise TypeError(message)
