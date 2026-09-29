# Copyright (c) 2026 deterministic-response-cache contributors
# ruff: noqa: INP001

"""Deterministic outcomes produced at the Response Reuse boundary."""

from dataclasses import dataclass
from enum import StrEnum

from deterministic_response_cache.response_reuse.model_response import ModelResponse


class NotCachedReason(StrEnum):
    """Closed reasons why a response was not retained."""

    UNSUPPORTED_PAYLOAD = "unsupported_payload"
    CODEC_UNAVAILABLE = "codec_unavailable"
    ENCODE_FAILURE = "encode_failure"
    ROUND_TRIP_MISMATCH = "round_trip_mismatch"
    STORE_WRITE_FAILURE = "store_write_failure"


class UnavailableReason(StrEnum):
    """Closed reasons why lookup could not provide a response."""

    STORE_FAILURE = "store_failure"
    UNKNOWN_CODEC = "unknown_codec"
    CODEC_UNAVAILABLE = "codec_unavailable"
    INVALID_PAYLOAD = "invalid_payload"


@dataclass(frozen=True, slots=True)
class Hit[PayloadT]:
    """A reusable response was found."""

    response: ModelResponse[PayloadT]


@dataclass(frozen=True, slots=True)
class Miss:
    """No usable response is available for the confirmed identity."""


@dataclass(frozen=True, slots=True)
class Unavailable:
    """A stored response could not become a reusable native response."""

    reason: UnavailableReason


@dataclass(frozen=True, slots=True)
class Cached[PayloadT]:
    """A response was retained by the CacheStore."""

    response: ModelResponse[PayloadT]


@dataclass(frozen=True, slots=True)
class NotCached[PayloadT]:
    """A response remains available even though retention failed."""

    response: ModelResponse[PayloadT]
    reason: NotCachedReason


type LookupOutcome[PayloadT] = Hit[PayloadT] | Miss | Unavailable
type RecordOutcome[PayloadT] = Cached[PayloadT] | NotCached[PayloadT]
