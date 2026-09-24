# Copyright (c) 2026 deterministic-response-cache contributors
# ruff: noqa: INP001

"""Common native-response codec contract and tagged results."""

from dataclasses import dataclass
from typing import Protocol

from deterministic_response_cache.response_reuse.model_response import ModelResponse
from deterministic_response_cache.response_reuse.stored_response import (
    ResponseCodecId,
    StoredResponse,
)


@dataclass(frozen=True, slots=True)
class Encoded:
    """A response encoded as a stored envelope."""

    stored: StoredResponse


@dataclass(frozen=True, slots=True)
class Decoded[PayloadT]:
    """A stored payload restored as a native response."""

    response: ModelResponse[PayloadT]


@dataclass(frozen=True, slots=True)
class UnsupportedPayload:
    """The native value is outside supported payloads."""


@dataclass(frozen=True, slots=True)
class CodecUnavailable:
    """The selected optional codec is unavailable."""


@dataclass(frozen=True, slots=True)
class EncodeFailure:
    """A supported response could not be encoded."""


@dataclass(frozen=True, slots=True)
class RoundTripMismatch:
    """DataFrame encoding changed observable data."""


@dataclass(frozen=True, slots=True)
class UnknownCodec:
    """The stored codec id is not supported."""


@dataclass(frozen=True, slots=True)
class InvalidPayload:
    """Stored bytes are invalid for their declared codec."""


type EncodeResult = (
    Encoded | UnsupportedPayload | CodecUnavailable | EncodeFailure | RoundTripMismatch
)
type DecodeResult[PayloadT] = Decoded[PayloadT] | UnknownCodec | CodecUnavailable | InvalidPayload


class ResponseCodec[PayloadT](Protocol):
    """Encode a native response and decode only its matching payload bytes."""

    @property
    def codec_id(self) -> ResponseCodecId:
        """Identify the stored format."""
        ...

    def encode(self, response: ModelResponse[PayloadT]) -> EncodeResult:
        """Encode a complete model response."""
        ...

    def decode(self, payload: bytes) -> DecodeResult[PayloadT]:
        """Decode bytes into a new response."""
        ...
