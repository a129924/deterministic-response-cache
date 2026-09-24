# Copyright (c) 2026 deterministic-response-cache contributors
# ruff: noqa: INP001

"""Fixed response codec selection without an eager optional import."""

from typing import cast

from deterministic_response_cache.response_reuse.codecs.contract import (
    CodecUnavailable,
    DecodeResult,
    EncodeResult,
    InvalidPayload,
    UnknownCodec,
    UnsupportedPayload,
)
from deterministic_response_cache.response_reuse.model_response import ModelResponse
from deterministic_response_cache.response_reuse.stored_response import (
    ResponseCodecId,
    StoredResponse,
)


def encode_response(response: ModelResponse[object]) -> EncodeResult:
    """Select JSON or DataFrame from the native payload type."""
    value = response.value
    if isinstance(value, (dict, list)):
        from deterministic_response_cache.response_reuse.codecs.json_response import (  # noqa: PLC0415
            JsonPayload,
            JsonResponseCodec,
        )

        return JsonResponseCodec().encode(cast("ModelResponse[JsonPayload]", response))
    try:
        import pandas as pd  # noqa: PLC0415  # pyright: ignore[reportMissingTypeStubs]
    except ImportError:
        return UnsupportedPayload()
    if not isinstance(value, pd.DataFrame):
        return UnsupportedPayload()
    try:
        from deterministic_response_cache.response_reuse.codecs.pyarrow_dataframe import (  # noqa: PLC0415
            PyArrowDataFrameCodec,
        )
    except ImportError:
        return CodecUnavailable()
    return PyArrowDataFrameCodec().encode(cast("ModelResponse[pd.DataFrame]", response))


def decode_response(stored: StoredResponse) -> DecodeResult[object]:
    """Decode solely by the declared stored codec id."""
    codec_id: object = stored.codec_id
    if type(codec_id) is not ResponseCodecId:
        return UnknownCodec()
    payload: object = stored.payload
    if not isinstance(payload, bytes):  # pyright: ignore[reportUnnecessaryIsInstance]
        return InvalidPayload()
    match codec_id:
        case ResponseCodecId.JSON_V1:
            from deterministic_response_cache.response_reuse.codecs.json_response import (  # noqa: PLC0415
                JsonResponseCodec,
            )

            return JsonResponseCodec().decode(stored.payload)
        case ResponseCodecId.DATAFRAME_V1:
            try:
                from deterministic_response_cache.response_reuse.codecs.pyarrow_dataframe import (  # noqa: PLC0415
                    PyArrowDataFrameCodec,
                )
            except ImportError:
                return CodecUnavailable()
            return PyArrowDataFrameCodec().decode(stored.payload)
        case _:
            return UnknownCodec()
