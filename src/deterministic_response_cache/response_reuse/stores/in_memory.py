# Copyright (c) 2026 deterministic-response-cache contributors
# ruff: noqa: INP001

"""Process-local in-memory implementation of the internal CacheStore port."""

from collections.abc import Hashable

from deterministic_response_cache.response_reuse._cache_store import NotFound, TokenWritten


class InMemoryCacheStore[IdentityT: Hashable, ResponseT]:
    """Retain opaque-keyed responses for the lifetime of this store instance."""

    def __init__(self) -> None:
        """Create an empty process-local response mapping."""
        self._responses: dict[IdentityT, ResponseT] = {}

    def read(self, confirmed_identity: IdentityT) -> ResponseT | NotFound:
        """Return the retained response or the explicit missing-entry channel."""
        try:
            return self._responses[confirmed_identity]
        except KeyError:
            return NotFound()

    def write(self, confirmed_identity: IdentityT, response: ResponseT) -> TokenWritten:
        """Retain ``response`` under the opaque key, replacing any earlier value."""
        self._responses[confirmed_identity] = response
        return TokenWritten()
