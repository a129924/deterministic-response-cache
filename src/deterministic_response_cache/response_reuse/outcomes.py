# Copyright (c) 2026 deterministic-response-cache contributors
# ruff: noqa: INP001

"""Deterministic outcomes produced at the Response Reuse boundary."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Hit[ResponseT]:
    """A reusable response was found."""

    response: ResponseT


@dataclass(frozen=True, slots=True)
class Miss:
    """No usable response is available for the confirmed identity."""


@dataclass(frozen=True, slots=True)
class Unavailable:
    """The CacheStore could not complete a lookup."""


@dataclass(frozen=True, slots=True)
class Cached[ResponseT]:
    """A response was retained by the CacheStore."""

    response: ResponseT


@dataclass(frozen=True, slots=True)
class NotCached[ResponseT]:
    """A response remains available even though retention failed."""

    response: ResponseT


type LookupOutcome[ResponseT] = Hit[ResponseT] | Miss | Unavailable
type RecordOutcome[ResponseT] = Cached[ResponseT] | NotCached[ResponseT]
