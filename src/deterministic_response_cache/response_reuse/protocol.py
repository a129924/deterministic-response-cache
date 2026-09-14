# Copyright (c) 2026 deterministic-response-cache contributors
# ruff: noqa: INP001

"""Synchronous orchestration at the Response Reuse boundary."""

from deterministic_response_cache.response_reuse._cache_store import (
    CacheStore,
    CacheStoreFailure,
    CacheStoreWriteFailure,
    NotFound,
    TokenWritten,
)
from deterministic_response_cache.response_reuse.outcomes import (
    Cached,
    Hit,
    LookupOutcome,
    Miss,
    NotCached,
    RecordOutcome,
    Unavailable,
)


class ResponseReuseProtocol[IdentityT, ResponseT]:
    """Map internal CacheStore operations to deterministic reuse outcomes."""

    def __init__(self, store: CacheStore[IdentityT, ResponseT]) -> None:
        """Create the protocol with its internal CacheStore dependency."""
        self._store = store

    def lookup(self, confirmed_identity: IdentityT) -> LookupOutcome[ResponseT]:
        """Find a reusable response without interpreting the identity."""
        match self._store.read(confirmed_identity):
            case NotFound():
                return Miss()
            case CacheStoreFailure():
                return Unavailable()
            case None:
                msg = "CacheStore.read must not return None"
                raise TypeError(msg)
            case response:
                return Hit(response)

    def record(
        self,
        confirmed_identity: IdentityT,
        response: ResponseT,
    ) -> RecordOutcome[ResponseT]:
        """Attempt to retain a response while preserving it on write failure."""
        match self._store.write(confirmed_identity, response):
            case TokenWritten():
                return Cached(response)
            case CacheStoreWriteFailure():
                return NotCached(response)
            case _:
                msg = "CacheStore.write must return a write channel value"
                raise TypeError(msg)
