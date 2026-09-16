# Copyright (c) 2026 deterministic-response-cache contributors
# ruff: noqa: INP001

"""Internal CacheStore port for the Response Reuse bounded context."""

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class NotFound:
    """The store has no usable response for the confirmed identity."""


@dataclass(frozen=True, slots=True)
class CacheStoreFailure:
    """The store could not complete a read operation."""


@dataclass(frozen=True, slots=True)
class TokenWritten:
    """The store retained the supplied response."""


@dataclass(frozen=True, slots=True)
class CacheStoreWriteFailure:
    """The store could not complete a write operation."""


class CacheStore[IdentityT, ResponseT](Protocol):
    """Synchronously read and retain responses for opaque confirmed identities."""

    def read(self, confirmed_identity: IdentityT) -> ResponseT | NotFound | CacheStoreFailure:
        """Return a response or an explicit lookup channel value."""
        ...

    def write(
        self,
        confirmed_identity: IdentityT,
        response: ResponseT,
    ) -> TokenWritten | CacheStoreWriteFailure:
        """Retain a response and return an explicit write channel value."""
        ...
