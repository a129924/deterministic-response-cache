# Copyright (c) 2026 deterministic-response-cache contributors

"""Branch mapping tests for the synchronous Response Reuse Protocol."""

import pytest

from deterministic_response_cache.response_reuse._cache_store import CacheStoreFailure
from deterministic_response_cache.response_reuse.outcomes import (
    Cached,
    Hit,
    Miss,
    NotCached,
    Unavailable,
)
from deterministic_response_cache.response_reuse.protocol import ResponseReuseProtocol


class FakeStore:
    """A typed in-memory test double for the internal CacheStore port."""

    def __init__(
        self,
        read_result: object | None = None,
        read_failure: Exception | None = None,
        write_failure: Exception | None = None,
    ) -> None:
        """Configure the read result and optional operational failures."""
        self.read_result = read_result
        self.read_failure = read_failure
        self.write_failure = write_failure
        self.read_identities: list[object] = []
        self.writes: list[tuple[object, object]] = []

    def read(self, confirmed_identity: object) -> object | None:
        """Return the configured read result or raise its configured failure."""
        self.read_identities.append(confirmed_identity)
        if self.read_failure is not None:
            raise self.read_failure
        return self.read_result

    def write(self, confirmed_identity: object, response: object) -> None:
        """Record the write or raise its configured failure."""
        self.writes.append((confirmed_identity, response))
        if self.write_failure is not None:
            raise self.write_failure


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


@pytest.mark.parametrize("state", ["absent", "invalid", "expired"])
def test_lookup_returns_miss_for_no_usable_store_entry(state: str) -> None:
    """CacheStore owns invalidation and signals every unusable state with None."""
    del state
    store = FakeStore(read_result=None)

    outcome = ResponseReuseProtocol(store).lookup(object())

    assert outcome == Miss()
    assert len(store.read_identities) == 1


def test_lookup_returns_unavailable_for_cache_store_failure() -> None:
    """Operational read failures never become cache misses."""
    store = FakeStore(read_failure=CacheStoreFailure("read unavailable"))

    outcome = ResponseReuseProtocol(store).lookup(object())

    assert outcome == Unavailable()
    assert len(store.read_identities) == 1


def test_lookup_propagates_non_cache_store_failure() -> None:
    """Programming or contract failures are not classified at this boundary."""
    store = FakeStore(read_failure=ValueError("invalid adapter"))

    with pytest.raises(ValueError, match="invalid adapter"):
        ResponseReuseProtocol(store).lookup(object())


def test_record_returns_cached_and_forwards_opaque_objects_once() -> None:
    """A successful write retains the caller's exact identity and response."""
    identity = object()
    response = object()
    store = FakeStore()

    outcome = ResponseReuseProtocol(store).record(identity, response)

    assert outcome == Cached(response)
    assert isinstance(outcome, Cached)
    assert outcome.response is response
    assert store.read_identities == []
    assert store.writes == [(identity, response)]


def test_record_returns_not_cached_and_preserves_response_on_write_failure() -> None:
    """A retention failure keeps the response available to the caller."""
    identity = object()
    response = object()
    store = FakeStore(write_failure=CacheStoreFailure("write unavailable"))

    outcome = ResponseReuseProtocol(store).record(identity, response)

    assert outcome == NotCached(response)
    assert isinstance(outcome, NotCached)
    assert outcome.response is response
    assert store.writes == [(identity, response)]


def test_record_propagates_non_cache_store_failure() -> None:
    """Unexpected write failures remain visible to the caller."""
    store = FakeStore(write_failure=ValueError("invalid adapter"))

    with pytest.raises(ValueError, match="invalid adapter"):
        ResponseReuseProtocol(store).record(object(), object())
