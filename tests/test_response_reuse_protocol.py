# Copyright (c) 2026 deterministic-response-cache contributors

"""Branch mapping tests for the synchronous Response Reuse Protocol."""

import pytest

from deterministic_response_cache.response_reuse._cache_store import (
    CacheStoreFailure,
    CacheStoreWriteFailure,
    NotFound,
    TokenWritten,
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
    """A stored response becomes Hit without inspecting its identity."""
    identity = object()
    response = object()
    store = FakeStore(read_result=response)

    outcome = ResponseReuseProtocol(store).lookup(identity)

    assert outcome == Hit(response)
    assert isinstance(outcome, Hit)
    assert outcome.response is response
    assert store.read_identities == [identity]
    assert store.writes == []


def test_lookup_returns_miss_for_not_found_channel() -> None:
    """An explicit absent-entry value channel becomes Miss."""
    store = FakeStore[object](NotFound())

    outcome = ResponseReuseProtocol(store).lookup(object())

    assert outcome == Miss()
    assert len(store.read_identities) == 1


def test_lookup_returns_unavailable_for_cache_store_failure_channel() -> None:
    """Operational read-failure values never become cache misses."""
    store = FakeStore[object](CacheStoreFailure())

    outcome = ResponseReuseProtocol(store).lookup(object())

    assert outcome == Unavailable()
    assert len(store.read_identities) == 1


def test_lookup_rejects_none_read_channel_after_one_read() -> None:
    """None is not a valid response, miss, or failure channel."""
    store = NoneReadStore()

    with pytest.raises(TypeError, match="must not return None"):
        ResponseReuseProtocol[object, object](store).lookup(object())  # pyright: ignore[reportArgumentType]

    assert len(store.read_identities) == 1


def test_lookup_propagates_store_exception() -> None:
    """Exceptions are transport failures, not Response Reuse value channels."""
    store = FakeStore[object](NotFound(), read_exception=ValueError("invalid adapter"))

    with pytest.raises(ValueError, match="invalid adapter"):
        ResponseReuseProtocol(store).lookup(object())


def test_record_returns_cached_and_forwards_opaque_objects_once() -> None:
    """A successful write retains the caller's exact identity and response."""
    identity = object()
    response = object()
    store = FakeStore(response)

    outcome = ResponseReuseProtocol(store).record(identity, response)

    assert outcome == Cached(response)
    assert isinstance(outcome, Cached)
    assert outcome.response is response
    assert store.read_identities == []
    assert store.writes == [(identity, response)]


def test_record_returns_not_cached_and_preserves_response_on_write_failure() -> None:
    """An explicit retention-failure value keeps the response available."""
    identity = object()
    response = object()
    store = FakeStore(response, write_result=CacheStoreWriteFailure())

    outcome = ResponseReuseProtocol(store).record(identity, response)

    assert outcome == NotCached(response)
    assert isinstance(outcome, NotCached)
    assert outcome.response is response
    assert store.writes == [(identity, response)]


def test_record_rejects_foreign_write_channel_after_one_write() -> None:
    """Only explicit write channels may be mapped to record outcomes."""
    identity = object()
    response = object()
    store = ForeignWriteStore()

    with pytest.raises(TypeError, match="must return a write channel value"):
        ResponseReuseProtocol[object, object](store).record(  # pyright: ignore[reportArgumentType]
            identity,
            response,
        )

    assert store.writes == [(identity, response)]


def test_record_propagates_store_exception() -> None:
    """Exceptions remain visible rather than becoming record outcomes."""
    response = object()
    store = FakeStore(response, write_exception=ValueError("invalid adapter"))

    with pytest.raises(ValueError, match="invalid adapter"):
        ResponseReuseProtocol(store).record(object(), response)
