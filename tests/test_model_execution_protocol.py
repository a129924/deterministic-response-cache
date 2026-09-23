# Copyright (c) 2026 deterministic-response-cache contributors

"""Behavior tests for the synchronous Model Execution Protocol."""

import pytest

from deterministic_response_cache.model_execution.outcomes import (
    Executed,
    ExecutionFailed,
    ExecutionFailureReason,
    InvocationFailed,
    InvocationSucceeded,
    RuntimeMissing,
    RuntimePreparationFailed,
    RuntimeReady,
    RuntimeUnavailable,
)
from deterministic_response_cache.model_execution.ports import ModelInvoker, RuntimeAccess
from deterministic_response_cache.model_execution.protocol import ModelExecutionProtocol


class RecordingRuntimeAccess[RuntimeT]:
    """Return configured runtime channels while recording calls and inputs."""

    def __init__(
        self,
        *,
        resolve_result: RuntimeReady[RuntimeT] | RuntimeMissing | RuntimeUnavailable,
        prepare_result: RuntimeReady[RuntimeT] | RuntimePreparationFailed,
        events: list[str],
        resolve_exception: Exception | None = None,
        prepare_exception: Exception | None = None,
    ) -> None:
        """Configure value channels or exact exceptions for both runtime operations."""
        self.resolve_result = resolve_result
        self.prepare_result = prepare_result
        self.events = events
        self.resolve_exception = resolve_exception
        self.prepare_exception = prepare_exception
        self.resolve_requests: list[object] = []
        self.prepare_requests: list[object] = []

    def resolve(
        self,
        request: object,
    ) -> RuntimeReady[RuntimeT] | RuntimeMissing | RuntimeUnavailable:
        """Record and resolve the caller's opaque runtime request."""
        self.events.append("resolve")
        self.resolve_requests.append(request)
        if self.resolve_exception is not None:
            raise self.resolve_exception
        return self.resolve_result

    def prepare(
        self,
        request: object,
    ) -> RuntimeReady[RuntimeT] | RuntimePreparationFailed:
        """Record and prepare the caller's opaque runtime request."""
        self.events.append("prepare")
        self.prepare_requests.append(request)
        if self.prepare_exception is not None:
            raise self.prepare_exception
        return self.prepare_result


class RecordingInvoker[RuntimeT, ResponseT]:
    """Return a configured invocation channel while recording calls and inputs."""

    def __init__(
        self,
        result: InvocationSucceeded[ResponseT] | InvocationFailed,
        *,
        events: list[str],
        exception: Exception | None = None,
    ) -> None:
        """Configure one value channel or the exact exception to propagate."""
        self.result = result
        self.events = events
        self.exception = exception
        self.calls: list[tuple[RuntimeT, object]] = []

    def invoke(
        self,
        runtime: RuntimeT,
        invocation: object,
    ) -> InvocationSucceeded[ResponseT] | InvocationFailed:
        """Record the exact runtime and invocation before returning."""
        self.events.append("invoke")
        self.calls.append((runtime, invocation))
        if self.exception is not None:
            raise self.exception
        return self.result


class InvalidResolveAccess:
    """Return a non-contract value from resolve and expose any later calls."""

    def __init__(self, result: object) -> None:
        """Keep the invalid result and initialize call observations."""
        self.result = result
        self.resolve_requests: list[object] = []
        self.prepare_requests: list[object] = []

    def resolve(self, request: object) -> object:
        """Violate the resolve return contract."""
        self.resolve_requests.append(request)
        return self.result

    def prepare(self, request: object) -> RuntimePreparationFailed:
        """Expose an erroneous continuation after invalid resolve."""
        self.prepare_requests.append(request)
        return RuntimePreparationFailed()


class InvalidPrepareAccess:
    """Reach prepare and return a configured non-contract value."""

    def __init__(self, result: object) -> None:
        """Keep the invalid result and initialize call observations."""
        self.result = result
        self.resolve_requests: list[object] = []
        self.prepare_requests: list[object] = []

    def resolve(self, request: object) -> RuntimeMissing:
        """Require the protocol to enter its prepare branch."""
        self.resolve_requests.append(request)
        return RuntimeMissing()

    def prepare(self, request: object) -> object:
        """Violate the prepare return contract."""
        self.prepare_requests.append(request)
        return self.result


class InvalidInvoker:
    """Return a configured non-contract value from invoke."""

    def __init__(self, result: object) -> None:
        """Keep the invalid result and initialize call observations."""
        self.result = result
        self.calls: list[tuple[object, object]] = []

    def invoke(self, runtime: object, invocation: object) -> object:
        """Violate the invocation return contract."""
        self.calls.append((runtime, invocation))
        return self.result


def runtime_access[RuntimeT](
    resolve_result: RuntimeReady[RuntimeT] | RuntimeMissing | RuntimeUnavailable,
    *,
    events: list[str],
    prepare_result: RuntimeReady[RuntimeT] | RuntimePreparationFailed | None = None,
    resolve_exception: Exception | None = None,
    prepare_exception: Exception | None = None,
) -> RecordingRuntimeAccess[RuntimeT]:
    """Build a typed runtime fake with an unused preparation failure default."""
    return RecordingRuntimeAccess(
        resolve_result=resolve_result,
        prepare_result=(RuntimePreparationFailed() if prepare_result is None else prepare_result),
        events=events,
        resolve_exception=resolve_exception,
        prepare_exception=prepare_exception,
    )


def test_port_protocols_are_available_from_their_defining_module() -> None:
    """The synchronous port methods remain directly importable without a facade."""
    assert RuntimeAccess.__module__ == "deterministic_response_cache.model_execution.ports"
    assert RuntimeAccess.__name__ == "RuntimeAccess"
    assert ModelInvoker.__module__ == "deterministic_response_cache.model_execution.ports"
    assert ModelInvoker.__name__ == "ModelInvoker"


def test_execute_invokes_once_with_an_existing_runtime() -> None:
    """A ready runtime bypasses preparation and preserves every opaque object."""
    events: list[str] = []
    runtime_request = object()
    runtime = object()
    invocation = object()
    response = object()
    access = runtime_access(RuntimeReady(runtime), events=events)
    invoker = RecordingInvoker[object, object](InvocationSucceeded(response), events=events)
    runtime_port: RuntimeAccess[object, object] = access
    invocation_port: ModelInvoker[object, object, object] = invoker

    outcome = ModelExecutionProtocol(runtime_port, invocation_port).execute(
        runtime_request,
        invocation,
    )

    assert outcome == Executed(response)
    assert isinstance(outcome, Executed)
    assert outcome.response is response
    assert events == ["resolve", "invoke"]
    assert access.resolve_requests == [runtime_request]
    assert access.resolve_requests[0] is runtime_request
    assert access.prepare_requests == []
    assert invoker.calls == [(runtime, invocation)]
    assert invoker.calls[0][0] is runtime
    assert invoker.calls[0][1] is invocation


def test_execute_prepares_a_missing_runtime_then_invokes_once() -> None:
    """Only an explicit missing channel enters prepare before invoking."""
    events: list[str] = []
    runtime_request = object()
    runtime = object()
    invocation = object()
    response = object()
    access = runtime_access(
        RuntimeMissing(),
        events=events,
        prepare_result=RuntimeReady(runtime),
    )
    invoker = RecordingInvoker[object, object](InvocationSucceeded(response), events=events)

    outcome = ModelExecutionProtocol(access, invoker).execute(runtime_request, invocation)

    assert outcome == Executed(response)
    assert isinstance(outcome, Executed)
    assert outcome.response is response
    assert events == ["resolve", "prepare", "invoke"]
    assert access.resolve_requests == [runtime_request]
    assert access.prepare_requests == [runtime_request]
    assert access.resolve_requests[0] is runtime_request
    assert access.prepare_requests[0] is runtime_request
    assert invoker.calls == [(runtime, invocation)]
    assert invoker.calls[0][0] is runtime
    assert invoker.calls[0][1] is invocation


def test_execute_maps_runtime_unavailable_without_preparing_or_invoking() -> None:
    """Runtime unavailability remains distinct from runtime absence."""
    events: list[str] = []
    access: RecordingRuntimeAccess[object] = runtime_access(RuntimeUnavailable(), events=events)
    invoker = RecordingInvoker[object, object](InvocationFailed(), events=events)

    outcome = ModelExecutionProtocol(access, invoker).execute(object(), object())

    assert outcome == ExecutionFailed(ExecutionFailureReason.RUNTIME_UNAVAILABLE)
    assert not hasattr(outcome, "response")
    assert events == ["resolve"]
    assert len(access.resolve_requests) == 1
    assert access.prepare_requests == []
    assert invoker.calls == []


def test_execute_maps_preparation_failure_without_invoking() -> None:
    """A declared preparation failure stops before model invocation."""
    events: list[str] = []
    access: RecordingRuntimeAccess[object] = runtime_access(
        RuntimeMissing(),
        events=events,
        prepare_result=RuntimePreparationFailed(),
    )
    invoker = RecordingInvoker[object, object](InvocationFailed(), events=events)

    outcome = ModelExecutionProtocol(access, invoker).execute(object(), object())

    assert outcome == ExecutionFailed(ExecutionFailureReason.RUNTIME_PREPARATION_FAILED)
    assert not hasattr(outcome, "response")
    assert events == ["resolve", "prepare"]
    assert len(access.resolve_requests) == 1
    assert len(access.prepare_requests) == 1
    assert invoker.calls == []


def test_execute_maps_invocation_failure_without_a_response() -> None:
    """A declared invocation failure produces no successful response field."""
    events: list[str] = []
    runtime = object()
    invocation = object()
    access = runtime_access(RuntimeReady(runtime), events=events)
    invoker = RecordingInvoker[object, object](InvocationFailed(), events=events)

    outcome = ModelExecutionProtocol(access, invoker).execute(object(), invocation)

    assert outcome == ExecutionFailed(ExecutionFailureReason.INVOCATION_FAILED)
    assert not hasattr(outcome, "response")
    assert events == ["resolve", "invoke"]
    assert len(access.resolve_requests) == 1
    assert access.prepare_requests == []
    assert invoker.calls == [(runtime, invocation)]


@pytest.mark.parametrize("invalid_result", [None, object()])
def test_execute_rejects_invalid_resolve_results_before_later_calls(
    invalid_result: object,
) -> None:
    """None and foreign resolve results cannot be interpreted as runtime state."""
    request = object()
    access = InvalidResolveAccess(invalid_result)
    invoker = RecordingInvoker[object, object](InvocationFailed(), events=[])

    with pytest.raises(TypeError):
        ModelExecutionProtocol[object, object, object, object](
            access,  # pyright: ignore[reportArgumentType]
            invoker,
        ).execute(request, object())

    assert access.resolve_requests == [request]
    assert access.prepare_requests == []
    assert invoker.calls == []


@pytest.mark.parametrize("invalid_result", [None, object()])
def test_execute_rejects_invalid_prepare_results_before_invoke(
    invalid_result: object,
) -> None:
    """None and foreign prepare results cannot become ready runtimes."""
    request = object()
    access = InvalidPrepareAccess(invalid_result)
    invoker = RecordingInvoker[object, object](InvocationFailed(), events=[])

    with pytest.raises(TypeError):
        ModelExecutionProtocol[object, object, object, object](
            access,  # pyright: ignore[reportArgumentType]
            invoker,
        ).execute(request, object())

    assert access.resolve_requests == [request]
    assert access.prepare_requests == [request]
    assert invoker.calls == []


@pytest.mark.parametrize("invalid_result", [None, object()])
def test_execute_rejects_invalid_invoke_results_after_one_invoke(
    invalid_result: object,
) -> None:
    """None and foreign invocation results cannot become execution outcomes."""
    runtime = object()
    invocation = object()
    access = runtime_access(RuntimeReady(runtime), events=[])
    invoker = InvalidInvoker(invalid_result)

    with pytest.raises(TypeError):
        ModelExecutionProtocol[object, object, object, object](
            access,
            invoker,  # pyright: ignore[reportArgumentType]
        ).execute(object(), invocation)

    assert len(access.resolve_requests) == 1
    assert access.prepare_requests == []
    assert invoker.calls == [(runtime, invocation)]


@pytest.mark.parametrize(
    ("stage", "expected_events"),
    [
        ("resolve", ["resolve"]),
        ("prepare", ["resolve", "prepare"]),
        ("invoke", ["resolve", "invoke"]),
    ],
)
def test_execute_propagates_each_port_exception_object_unchanged(
    stage: str,
    expected_events: list[str],
) -> None:
    """Exceptions remain transport failures and never become business outcomes."""
    events: list[str] = []
    error = RuntimeError(f"{stage} failed")
    runtime = object()
    resolve_result = RuntimeMissing() if stage == "prepare" else RuntimeReady(runtime)
    access = runtime_access(
        resolve_result,
        events=events,
        prepare_result=RuntimeReady(runtime),
        resolve_exception=error if stage == "resolve" else None,
        prepare_exception=error if stage == "prepare" else None,
    )
    invoker = RecordingInvoker[object, object](
        InvocationSucceeded(object()),
        events=events,
        exception=error if stage == "invoke" else None,
    )

    with pytest.raises(RuntimeError, match=f"{stage} failed") as error_info:
        ModelExecutionProtocol(access, invoker).execute(object(), object())

    assert error_info.value is error
    assert events == expected_events
    assert len(access.resolve_requests) == 1
    assert len(access.prepare_requests) == (1 if stage == "prepare" else 0)
    assert len(invoker.calls) == (1 if stage == "invoke" else 0)


def test_declared_failure_outcomes_never_expose_a_response() -> None:
    """Every public failure reason uses the response-free failure shape."""
    failures: tuple[ExecutionFailed, ...] = tuple(
        ExecutionFailed(reason)
        for reason in (
            ExecutionFailureReason.RUNTIME_UNAVAILABLE,
            ExecutionFailureReason.RUNTIME_PREPARATION_FAILED,
            ExecutionFailureReason.INVOCATION_FAILED,
        )
    )

    assert all(not hasattr(failure, "response") for failure in failures)
