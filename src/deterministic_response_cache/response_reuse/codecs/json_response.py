# Copyright (c) 2026 deterministic-response-cache contributors
# ruff: noqa: INP001

"""Lossless JSON response codec for dict and list roots."""

import json
import math
from typing import cast, override

from deterministic_response_cache.response_reuse.codecs.contract import (
    Decoded,
    DecodeResult,
    Encoded,
    EncodeFailure,
    EncodeResult,
    InvalidPayload,
    ResponseCodec,
    UnsupportedPayload,
)
from deterministic_response_cache.response_reuse.model_response import ModelResponse
from deterministic_response_cache.response_reuse.stored_response import (
    ResponseCodecId,
    StoredResponse,
)

type JsonPayload = dict[str, object] | list[object]


def _valid_json_tree(value: object) -> bool:
    """Reject Python values that JSON would coerce or silently change."""
    if value is None or type(value) in (str, bool, int):
        return True
    if type(value) is float:
        return math.isfinite(value)
    if type(value) is list:
        return all(_valid_json_tree(item) for item in cast("list[object]", value))
    if type(value) is dict:
        return all(
            type(key) is str and _valid_json_tree(item)
            for key, item in cast("dict[object, object]", value).items()
        )
    return False


class JsonResponseCodec(ResponseCodec[JsonPayload]):
    """UTF-8 JSON codec with explicit root and round-trip checks."""

    @property
    @override
    def codec_id(self) -> ResponseCodecId:
        """Return the closed JSON format id."""
        return ResponseCodecId.JSON_V1

    @override
    def encode(self, response: ModelResponse[JsonPayload]) -> EncodeResult:
        """Encode only a lossless dict or list response."""
        try:
            valid = _valid_json_tree(response.value)
        except RecursionError:
            return EncodeFailure()
        if type(response.value) not in (dict, list) or not valid:
            return UnsupportedPayload()
        try:
            payload = json.dumps(
                response.value,
                ensure_ascii=False,
                allow_nan=False,
            ).encode("utf-8")
        except (TypeError, ValueError, UnicodeError, RecursionError):
            return EncodeFailure()
        decoded = self.decode(payload)
        if not isinstance(decoded, Decoded) or decoded.response.value != response.value:
            return EncodeFailure()
        return Encoded(StoredResponse(self.codec_id, payload))

    @override
    def decode(self, payload: bytes) -> DecodeResult[JsonPayload]:
        """Decode a stored JSON dict or list without guessing its format."""
        try:
            value: object = json.loads(payload.decode("utf-8"))
        except (UnicodeError, ValueError, TypeError, RecursionError):
            return InvalidPayload()
        if type(value) not in (dict, list):
            return InvalidPayload()
        try:
            valid = _valid_json_tree(value)
        except RecursionError:
            return InvalidPayload()
        if not valid:
            return InvalidPayload()
        return Decoded(ModelResponse(cast("JsonPayload", value)))
