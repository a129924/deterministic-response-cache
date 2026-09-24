# Copyright (c) 2026 deterministic-response-cache contributors
# ruff: noqa: INP001

"""Common native-response codec contract and expected codec failures."""

from typing import Protocol

from deterministic_response_cache.response_reuse.model_response import ModelResponse
from deterministic_response_cache.response_reuse.stored_response import (
    ResponseCodecId,
    StoredResponse,
)


class ResponseCodec[PayloadT](Protocol):
    """Encode a native response and decode only its matching payload bytes."""

    @property
    def codec_id(self) -> ResponseCodecId:
        """Identify the stored format."""
        ...

    def encode(self, response: ModelResponse[PayloadT]) -> StoredResponse:
        """Encode a complete model response."""
        ...

    def decode(self, payload: bytes) -> ModelResponse[PayloadT]:
        """Decode bytes into a new response."""
        ...


class UnsupportedPayloadError(ValueError):
    """The value is outside the supported response payload types."""


class CodecUnavailableError(RuntimeError):
    """A selected optional codec cannot be used in this installation."""


class EncodeFailureError(ValueError):
    """A supported payload could not be encoded without loss."""


class RoundTripMismatchError(EncodeFailureError):
    """DataFrame encoding changed the response's observable data."""


class UnknownCodecError(ValueError):
    """The stored codec id does not identify a supported decoder."""


class InvalidPayloadError(ValueError):
    """Stored bytes cannot be decoded by their declared codec."""
