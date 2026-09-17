# Copyright (c) 2026 deterministic-response-cache contributors
# ruff: noqa: INP001, S101

"""Contract tests for the process-local InMemoryCacheStore."""

import pytest

from deterministic_response_cache.response_reuse._cache_store import NotFound, TokenWritten
from deterministic_response_cache.response_reuse.outcomes import Cached, Hit, Miss
from deterministic_response_cache.response_reuse.protocol import ResponseReuseProtocol
from deterministic_response_cache.response_reuse.stores.in_memory import InMemoryCacheStore


class KeyWithFailingHash:
    """A hashable-shaped opaque key whose hash operation fails."""

    def __hash__(self) -> int:
        """Expose a key-operation error that must not become a cache miss."""
        msg = "key hash failed"
        raise KeyError(msg)


def test_read_returns_not_found_for_an_unknown_opaque_hashable_key() -> None:
    """An unrecorded key produces the existing explicit miss channel."""
    store = InMemoryCacheStore[object, object]()

    result = store.read(object())

    assert result == NotFound()


def test_write_then_read_preserves_the_caller_owned_response_reference() -> None:
    """The store retains and returns the exact supplied response object."""
    store = InMemoryCacheStore[object, dict[str, str]]()
    identity = object()
    response = {"answer": "first"}

    result = store.write(identity, response)
    response["answer"] = "updated"
    retained = store.read(identity)

    assert result == TokenWritten()
    assert retained is response
    assert retained == {"answer": "updated"}


def test_write_overwrites_the_response_for_the_same_opaque_key() -> None:
    """A later write for one key replaces its earlier response."""
    store = InMemoryCacheStore[object, str]()
    identity = object()

    store.write(identity, "first")
    result = store.write(identity, "second")

    assert result == TokenWritten()
    assert store.read(identity) == "second"


def test_different_opaque_keys_are_isolated() -> None:
    """Responses can only be read back with their exact hashable key."""
    store = InMemoryCacheStore[object, str]()
    first_identity = object()
    second_identity = object()

    store.write(first_identity, "first")
    store.write(second_identity, "second")

    assert store.read(first_identity) == "first"
    assert store.read(second_identity) == "second"


def test_each_store_instance_has_an_independent_process_local_mapping() -> None:
    """Responses do not leak from one store instance into another."""
    identity = object()
    first_store = InMemoryCacheStore[object, str]()
    second_store = InMemoryCacheStore[object, str]()

    first_store.write(identity, "retained")

    assert second_store.read(identity) == NotFound()


def test_read_with_an_unhashable_key_follows_mapping_type_error_semantics() -> None:
    """The generic store neither validates nor reinterprets opaque read keys."""
    store = InMemoryCacheStore[object, object]()
    unhashable_key: list[str] = []

    with pytest.raises(TypeError, match="unhashable type"):
        store.read(unhashable_key)  # pyright: ignore[reportArgumentType]

    assert store.read("other-key") == NotFound()


def test_write_with_an_unhashable_key_follows_mapping_type_error_semantics() -> None:
    """The generic store neither validates nor reinterprets opaque write keys."""
    store = InMemoryCacheStore[object, object]()
    unhashable_key: list[str] = []

    with pytest.raises(TypeError, match="unhashable type"):
        store.write(unhashable_key, object())  # pyright: ignore[reportArgumentType]

    assert store.read("other-key") == NotFound()


def test_key_operation_errors_propagate_instead_of_becoming_misses() -> None:
    """A valid key's internal failure remains visible to the caller."""
    store = InMemoryCacheStore[KeyWithFailingHash, object]()

    with pytest.raises(KeyError, match="key hash failed"):
        store.read(KeyWithFailingHash())


def test_store_is_injectable_into_the_response_reuse_protocol() -> None:
    """The concrete store satisfies the existing generic internal port."""
    protocol = ResponseReuseProtocol(InMemoryCacheStore[str, str]())

    miss = protocol.lookup("opaque-key")
    cached = protocol.record("opaque-key", "response")
    hit = protocol.lookup("opaque-key")

    assert miss == Miss()
    assert cached == Cached("response")
    assert hit == Hit("response")
