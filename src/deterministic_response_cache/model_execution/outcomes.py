# Copyright (c) 2026 deterministic-response-cache contributors
# ruff: noqa: INP001

"""Deterministic value channels for the Model Execution boundary."""

from dataclasses import dataclass
from enum import Enum, auto


@dataclass(frozen=True, slots=True)
class RuntimeReady[RuntimeT]:
    """A runtime is available for model invocation."""

    runtime: RuntimeT


@dataclass(frozen=True, slots=True)
class RuntimeMissing:
    """No reusable runtime currently exists."""


@dataclass(frozen=True, slots=True)
class RuntimeUnavailable:
    """A runtime cannot be supplied for this execution."""


@dataclass(frozen=True, slots=True)
class RuntimePreparationFailed:
    """A missing runtime could not be prepared."""


@dataclass(frozen=True, slots=True)
class InvocationSucceeded[ResponseT]:
    """A model invocation produced a response."""

    response: ResponseT


@dataclass(frozen=True, slots=True)
class InvocationFailed:
    """A model invocation completed with a declared failure."""


class ExecutionFailureReason(Enum):
    """The declared reason an execution produced no response."""

    RUNTIME_UNAVAILABLE = auto()
    RUNTIME_PREPARATION_FAILED = auto()
    INVOCATION_FAILED = auto()


@dataclass(frozen=True, slots=True)
class Executed[ResponseT]:
    """A model execution completed with a response."""

    response: ResponseT


@dataclass(frozen=True, slots=True)
class ExecutionFailed:
    """A model execution produced no response for a declared reason."""

    reason: ExecutionFailureReason


type RuntimeResolutionOutcome[RuntimeT] = (
    RuntimeReady[RuntimeT] | RuntimeMissing | RuntimeUnavailable
)
type RuntimePreparationOutcome[RuntimeT] = RuntimeReady[RuntimeT] | RuntimePreparationFailed
type InvocationOutcome[ResponseT] = InvocationSucceeded[ResponseT] | InvocationFailed
type ExecutionOutcome[ResponseT] = Executed[ResponseT] | ExecutionFailed
