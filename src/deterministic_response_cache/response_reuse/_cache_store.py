# Copyright (c) 2026 deterministic-response-cache contributors
# ruff: noqa: INP001

"""Internal CacheStore port for the Response Reuse bounded context."""

from typing import Protocol


class CacheStoreFailure(Exception):  # noqa: N818
    """An expected operational failure raised by a CacheStore adapter."""


class CacheStore[IdentityT, ResponseT](Protocol):
    """Synchronously read and retain responses for opaque confirmed identities."""

    def read(self, confirmed_identity: IdentityT) -> ResponseT | None:
        """Return a usable response, or ``None`` when no usable entry exists."""

    def write(self, confirmed_identity: IdentityT, response: ResponseT) -> None:
        """Retain a response for a confirmed identity."""
