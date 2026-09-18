# Copyright (c) 2026 deterministic-response-cache contributors

"""Branch mapping tests for the synchronous Response Reuse Protocol."""

from inspect import Parameter, signature

import pytest

from deterministic_response_cache.response_reuse._cache_store import (
    CacheStoreFailure,
    CacheStoreWriteFailure,
    NotFound,
    TokenWritten,
)
from deterministic_response_cache.response_reuse.eligibility.policy import (
    ReuseAllowed,
    ReuseDenied,
    ReuseEligibilityDecision,
)
from deterministic_response_cache.response_reuse.outcomes import (
    Cached,
    Hit,
    Miss,
    NotCached,
    Unavailable,
)
from deterministic_response_cache.response_reuse.protocol import ResponseReuseProtocol

DEFAULT_WRITE_RESULT = TokenWritten()


class FakeStore[ResponseT]:
    """A typed in-memory test double for the internal CacheStore port."""

    def __init__(
        self,
        read_result: ResponseT | NotFound | CacheStoreFailure,
        write_result: TokenWritten | CacheStoreWriteFailure = DEFAULT_WRITE_RESULT,
        read_exception: Exception | None = None,
        write_exception: Exception | None = None,
    ) -> None:
        """Configure value channels and optional propagated exceptions."""
        self.read_result = read_result
        self.write_result = write_result
        self.read_exception = read_exception
        self.write_exception = write_exception
        self.read_identities: list[object] = []
        self.writes: list[tuple[object, ResponseT]] = []

    def read(self, confirmed_identity: object) -> ResponseT | NotFound | CacheStoreFailure:
        """Return the configured read channel or raise an unchanged exception."""
        self.read_identities.append(confirmed_identity)
        if self.read_exception is not None:
            raise self.read_exception
        return self.read_result

    def write(
        self,
        confirmed_identity: object,
        response: ResponseT,
    ) -> TokenWritten | CacheStoreWriteFailure:
        """Return the configured write channel or raise an unchanged exception."""
        self.writes.append((confirmed_identity, response))
        if self.write_exception is not None:
            raise self.write_exception
        return self.write_result


class RecordingEligibilityPolicy[ResponseT]:
    """Return a configured eligibility decision and retain observed responses."""

    def __init__(
        self,
        decision: ReuseEligibilityDecision,
        exception: Exception | None = None,
    ) -> None:
        """Configure a decision or an exception that must be propagated unchanged."""
        self.decision = decision
        self.exception = exception
        self.evaluated_responses: list[ResponseT] = []

    def evaluate(self, response: ResponseT, /) -> ReuseEligibilityDecision:
        """Record the exact response before returning its configured behavior."""
        self.evaluated_responses.append(response)
        if self.exception is not None:
            raise self.exception
        return self.decision


class InvalidDecisionPolicy:
    """Deliberately violate the eligibility decision contract at runtime."""

    def __init__(self, result: object) -> None:
        """Keep the invalid result and each supplied response observable to the test."""
        self.result = result
        self.evaluated_responses: list[object] = []

    def evaluate(self, response: object, /) -> object:
        """Return a foreign decision that a protocol implementation must reject."""
        self.evaluated_responses.append(response)
        return self.result


class NoneReadStore:
    """A deliberate CacheStore contract violator for runtime-boundary testing."""

    def __init__(self) -> None:
        """Create a store that intentionally returns an invalid read channel."""
        self.read_identities: list[object] = []

    def read(self, confirmed_identity: object) -> None:
        """Violate the read channel contract with ``None``."""
        self.read_identities.append(confirmed_identity)

    def write(self, confirmed_identity: object, response: object) -> TokenWritten:
        """Supply an otherwise valid write channel for structural completeness."""
        del confirmed_identity, response
        return TokenWritten()


class ForeignWriteStore:
    """A deliberate CacheStore contract violator for write-channel testing."""

    def __init__(self) -> None:
        """Create a store that intentionally returns an invalid write channel."""
        self.writes: list[tuple[object, object]] = []

    def read(self, confirmed_identity: object) -> NotFound:
        """Supply an otherwise valid read channel for structural completeness."""
        del confirmed_identity
        return NotFound()

    def write(self, confirmed_identity: object, response: object) -> object:
        """Violate the write channel contract with a foreign value."""
        self.writes.append((confirmed_identity, response))
        return object()


@pytest.mark.parametrize(
    "channel_type",
    [NotFound, CacheStoreFailure, TokenWritten, CacheStoreWriteFailure],
)
def test_cache_store_channels_are_immutable_slotted_value_objects(
    channel_type: type[NotFound]
    | type[CacheStoreFailure]
    | type[TokenWritten]
    | type[CacheStoreWriteFailure],
) -> None:
    """Every CacheStore channel is an immutable value object, not an exception."""
    channel = channel_type()
    assert not isinstance(channel, Exception)
    assert not hasattr(channel, "__dict__")
    assert channel == channel_type()


def test_lookup_returns_hit_and_forwards_opaque_identity_once() -> None:
    """A policy-approved response becomes Hit without inspecting its identity."""
    identity = object()
    response = object()
    store = FakeStore(read_result=response)
    policy = RecordingEligibilityPolicy[object](ReuseAllowed())

    outcome = ResponseReuseProtocol(store, eligibility_policy=policy).lookup(identity)

    assert outcome == Hit(response)
    assert isinstance(outcome, Hit)
    assert outcome.response is response
    assert store.read_identities == [identity]
    assert store.writes == []
    assert policy.evaluated_responses == [response]


def test_lookup_returns_miss_without_leaking_a_policy_denied_response() -> None:
    """A policy-denied response cannot become a Hit or trigger a retention write."""
    response = object()
    store = FakeStore(read_result=response)
    policy = RecordingEligibilityPolicy[object](ReuseDenied())

    outcome = ResponseReuseProtocol(store, eligibility_policy=policy).lookup(object())

    assert outcome == Miss()
    assert not isinstance(outcome, Hit)
    assert store.writes == []
    assert policy.evaluated_responses == [response]


def test_lookup_returns_miss_for_not_found_channel() -> None:
    """An explicit absent-entry value channel becomes Miss."""
    store = FakeStore[object](NotFound())
    policy = RecordingEligibilityPolicy[object](ReuseAllowed())

    outcome = ResponseReuseProtocol(store, eligibility_policy=policy).lookup(object())

    assert outcome == Miss()
    assert len(store.read_identities) == 1
    assert policy.evaluated_responses == []


def test_lookup_returns_unavailable_for_cache_store_failure_channel() -> None:
    """Operational read-failure values never become cache misses."""
    store = FakeStore[object](CacheStoreFailure())
    policy = RecordingEligibilityPolicy[object](ReuseAllowed())

    outcome = ResponseReuseProtocol(store, eligibility_policy=policy).lookup(object())

    assert outcome == Unavailable()
    assert len(store.read_identities) == 1
    assert policy.evaluated_responses == []


def test_lookup_rejects_none_read_channel_after_one_read() -> None:
    """None is not a valid response, miss, or failure channel."""
    store = NoneReadStore()
    policy = RecordingEligibilityPolicy[object](ReuseAllowed())

    with pytest.raises(TypeError, match="must not return None"):
        ResponseReuseProtocol[object, object](
            store,  # pyright: ignore[reportArgumentType]
            eligibility_policy=policy,
        ).lookup(object())

    assert len(store.read_identities) == 1
    assert policy.evaluated_responses == []


def test_lookup_propagates_store_exception() -> None:
    """Exceptions are transport failures, not Response Reuse value channels."""
    store = FakeStore[object](NotFound(), read_exception=ValueError("invalid adapter"))
    policy = RecordingEligibilityPolicy[object](ReuseAllowed())

    with pytest.raises(ValueError, match="invalid adapter"):
        ResponseReuseProtocol(store, eligibility_policy=policy).lookup(object())

    assert policy.evaluated_responses == []


@pytest.mark.parametrize("invalid_result", [None, True, False, object()])
def test_lookup_rejects_invalid_policy_decisions_after_one_evaluation(
    invalid_result: object,
) -> None:
    """No falsey, truthy, or foreign result can be interpreted as a decision."""
    response = object()
    store = FakeStore(read_result=response)
    policy = InvalidDecisionPolicy(invalid_result)

    with pytest.raises(TypeError):
        ResponseReuseProtocol(
            store,
            eligibility_policy=policy,  # pyright: ignore[reportArgumentType]
        ).lookup(object())

    assert store.writes == []
    assert policy.evaluated_responses == [response]


def test_lookup_propagates_policy_exception_after_one_evaluation() -> None:
    """A policy exception remains visible instead of becoming a cache outcome."""
    response = object()
    policy_error = ValueError("policy failed")
    store = FakeStore(read_result=response)
    policy = RecordingEligibilityPolicy[object](ReuseAllowed(), exception=policy_error)

    with pytest.raises(ValueError, match="policy failed") as error_info:
        ResponseReuseProtocol(store, eligibility_policy=policy).lookup(object())

    assert error_info.value is policy_error
    assert store.writes == []
    assert policy.evaluated_responses == [response]


def test_protocol_requires_a_keyword_only_eligibility_policy() -> None:
    """Construction has no default policy and accepts policy injection only by keyword."""
    parameters = tuple(signature(ResponseReuseProtocol).parameters.values())

    assert tuple(parameter.name for parameter in parameters) == ("store", "eligibility_policy")
    assert parameters[1].kind is Parameter.KEYWORD_ONLY
    assert parameters[1].default is Parameter.empty


def test_protocol_rejects_omitted_or_positional_eligibility_policy() -> None:
    """The intentional source break is enforced through Python call semantics."""
    store = FakeStore[object](NotFound())
    policy = RecordingEligibilityPolicy[object](ReuseAllowed())

    with pytest.raises(TypeError):
        ResponseReuseProtocol(store)  # pyright: ignore[reportCallIssue]
    with pytest.raises(TypeError):
        ResponseReuseProtocol(store, policy)  # pyright: ignore[reportCallIssue]


def test_record_returns_cached_and_forwards_opaque_objects_once() -> None:
    """A successful write retains the caller's exact identity and response."""
    identity = object()
    response = object()
    store = FakeStore(response)
    policy = RecordingEligibilityPolicy[object](ReuseAllowed())

    outcome = ResponseReuseProtocol(store, eligibility_policy=policy).record(identity, response)

    assert outcome == Cached(response)
    assert isinstance(outcome, Cached)
    assert outcome.response is response
    assert store.read_identities == []
    assert store.writes == [(identity, response)]
    assert policy.evaluated_responses == []


def test_record_returns_not_cached_and_preserves_response_on_write_failure() -> None:
    """An explicit retention-failure value keeps the response available."""
    identity = object()
    response = object()
    store = FakeStore(response, write_result=CacheStoreWriteFailure())
    policy = RecordingEligibilityPolicy[object](ReuseAllowed())

    outcome = ResponseReuseProtocol(store, eligibility_policy=policy).record(identity, response)

    assert outcome == NotCached(response)
    assert isinstance(outcome, NotCached)
    assert outcome.response is response
    assert store.read_identities == []
    assert store.writes == [(identity, response)]
    assert policy.evaluated_responses == []


def test_record_rejects_foreign_write_channel_after_one_write() -> None:
    """Only explicit write channels may be mapped to record outcomes."""
    identity = object()
    response = object()
    store = ForeignWriteStore()
    policy = RecordingEligibilityPolicy[object](ReuseAllowed())

    with pytest.raises(TypeError, match="must return a write channel value"):
        ResponseReuseProtocol[object, object](
            store,  # pyright: ignore[reportArgumentType]
            eligibility_policy=policy,
        ).record(
            identity,
            response,
        )

    assert store.writes == [(identity, response)]
    assert policy.evaluated_responses == []


def test_record_propagates_store_exception() -> None:
    """Exceptions remain visible rather than becoming record outcomes."""
    response = object()
    store = FakeStore(response, write_exception=ValueError("invalid adapter"))
    policy = RecordingEligibilityPolicy[object](ReuseAllowed())

    with pytest.raises(ValueError, match="invalid adapter"):
        ResponseReuseProtocol(store, eligibility_policy=policy).record(object(), response)

    assert store.read_identities == []
    assert policy.evaluated_responses == []
