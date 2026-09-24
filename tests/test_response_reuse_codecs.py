# Copyright (c) 2026 deterministic-response-cache contributors
# pyright: reportUnknownMemberType=false

"""Focused codec, selector and stored-format contract tests."""

import json
from dataclasses import FrozenInstanceError
from typing import cast

import pandas as pd  # pyright: ignore[reportMissingTypeStubs]
import pytest

from deterministic_response_cache.response_reuse.codecs.contract import (
    Decoded,
    Encoded,
    EncodeFailure,
    InvalidPayload,
    RoundTripMismatch,
    UnknownCodec,
    UnsupportedPayload,
)
from deterministic_response_cache.response_reuse.codecs.json_response import JsonResponseCodec
from deterministic_response_cache.response_reuse.codecs.pyarrow_dataframe import (
    PyArrowDataFrameCodec,
)
from deterministic_response_cache.response_reuse.codecs.selector import (
    decode_response,
    encode_response,
)
from deterministic_response_cache.response_reuse.model_response import ModelResponse
from deterministic_response_cache.response_reuse.stored_response import (
    ResponseCodecId,
    StoredResponse,
)


def test_value_objects_and_codec_ids_are_closed() -> None:
    """The store envelope is bytes and VO fields cannot be rebound."""
    response = ModelResponse({"answer": [1, True, None]})
    encoded = encode_response(response)

    assert isinstance(encoded, Encoded)
    stored = encoded.stored
    assert stored.codec_id is ResponseCodecId.JSON_V1
    assert isinstance(stored.payload, bytes)
    assert {item.value for item in ResponseCodecId} == {"json/v1", "dataframe/v1"}
    assert not hasattr(response, "__dict__")
    assert not hasattr(stored, "__dict__")
    with pytest.raises(FrozenInstanceError):
        response.value = {}  # pyright: ignore[reportAttributeAccessIssue]


@pytest.mark.parametrize(
    "value",
    [
        {"answer": [1, 2.5, False, None, "繁體中文"]},
        [1, {"nested": []}],
        {},
        [],
    ],
)
def test_json_round_trip(value: dict[str, object] | list[object]) -> None:
    """JSON preserves supported native tree values and creates a new tree."""
    response = ModelResponse(value)
    encoded = JsonResponseCodec().encode(response)
    assert isinstance(encoded, Encoded)
    decoded = JsonResponseCodec().decode(encoded.stored.payload)

    assert isinstance(decoded, Decoded)
    assert encoded.stored.codec_id is ResponseCodecId.JSON_V1
    assert decoded.response.value == value
    assert decoded.response.value is not value


@pytest.mark.parametrize(
    "value",
    [
        {1: "non-string key"},
        {"nonfinite": float("nan")},
        {"tuple": (1, 2)},
        {"object": object()},
        [float("inf")],
    ],
)
def test_json_rejects_lossy_trees(value: object) -> None:
    """Neither key coercion nor nested Python type changes are cached."""
    result = JsonResponseCodec().encode(
        ModelResponse(cast("dict[str, object] | list[object]", value)),
    )
    assert result == UnsupportedPayload()


def test_json_rejects_cyclic_tree_as_encode_failure() -> None:
    """A cycle must not escape as recursion failure or reach the Store."""
    value: list[object] = []
    value.append(value)
    assert JsonResponseCodec().encode(ModelResponse(value)) == EncodeFailure()


def test_json_codec_returns_encode_failure_for_serializer_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A supported tree reaches the serializer and reports its failure as a value."""

    def failing_dumps(*args: object, **kwargs: object) -> str:
        del args, kwargs
        raise TypeError

    monkeypatch.setattr(json, "dumps", failing_dumps)
    assert JsonResponseCodec().encode(ModelResponse({"answer": 1})) == EncodeFailure()


@pytest.mark.parametrize("payload", [b"not json", b"null", b"42", b"\xff", b'{"a":NaN}'])
def test_json_rejects_invalid_stored_bytes(payload: bytes) -> None:
    """A declared JSON id does not allow malformed or scalar payloads."""
    assert JsonResponseCodec().decode(payload) == InvalidPayload()


def test_fixed_selector_rejects_other_payloads_and_unknown_id() -> None:
    """No registry or byte sniffing can make a foreign format usable."""
    assert encode_response(ModelResponse(42)) == UnsupportedPayload()
    alien = StoredResponse(cast("ResponseCodecId", "alien/v1"), b"{}")
    assert decode_response(alien) == UnknownCodec()
    illegal = StoredResponse(cast("ResponseCodecId", "json/v1"), b"{}")
    assert decode_response(illegal) == UnknownCodec()


def test_fixed_selector_returns_tagged_success_and_invalid_bytes() -> None:
    """Selector uses the declared codec id and preserves both success wrappers."""
    encoded = encode_response(ModelResponse({"answer": [1]}))
    assert isinstance(encoded, Encoded)
    decoded = decode_response(encoded.stored)
    assert isinstance(decoded, Decoded)
    assert decoded.response.value == {"answer": [1]}
    assert decode_response(StoredResponse(ResponseCodecId.JSON_V1, b"invalid")) == InvalidPayload()
    alien = StoredResponse(cast("ResponseCodecId", "alien/v1"), cast("bytes", "invalid"))
    assert decode_response(alien) == UnknownCodec()


def test_dataframe_arrow_ipc_round_trip_keeps_metadata() -> None:
    """Arrow stream restores dtype, index, timezone and nullable data."""
    index = pd.Index(["first", "second"], name="row")
    frame = pd.DataFrame(
        {
            "count": pd.Series([1, None], index=index, dtype="Int64"),
            "when": pd.to_datetime(["2026-01-01", "2026-01-02"], utc=True),
        },
        index=index,
    )
    encoded = PyArrowDataFrameCodec().encode(ModelResponse(frame))
    assert isinstance(encoded, Encoded)
    decoded = PyArrowDataFrameCodec().decode(encoded.stored.payload)

    assert isinstance(decoded, Decoded)
    assert encoded.stored.codec_id is ResponseCodecId.DATAFRAME_V1
    selected = encode_response(ModelResponse(frame))
    assert isinstance(selected, Encoded)
    selected_decoded = decode_response(selected.stored)
    assert isinstance(selected_decoded, Decoded)
    assert frame.equals(selected_decoded.response.value)
    assert frame.equals(decoded.response.value)
    assert frame.dtypes.equals(decoded.response.value.dtypes)
    assert frame.index.equals(decoded.response.value.index)
    assert decoded.response.value is not frame


def test_empty_dataframe_arrow_ipc_round_trip() -> None:
    """An empty frame retains its nullable dtype and named index."""
    frame = pd.DataFrame(
        {"count": pd.Series([], dtype="Int64")},
        index=pd.Index([], name="row"),
    )

    encoded = PyArrowDataFrameCodec().encode(ModelResponse(frame))
    assert isinstance(encoded, Encoded)
    decoded = PyArrowDataFrameCodec().decode(encoded.stored.payload)

    assert isinstance(decoded, Decoded)
    assert encoded.stored.codec_id is ResponseCodecId.DATAFRAME_V1
    assert decoded.response.value.empty
    assert frame.equals(decoded.response.value)
    assert frame.dtypes.equals(decoded.response.value.dtypes)
    assert frame.index.equals(decoded.response.value.index)
    assert decoded.response.value is not frame


def test_dataframe_codec_rejects_round_trip_mismatch(monkeypatch: pytest.MonkeyPatch) -> None:
    """An unequal decoded frame fails before any Store write."""
    frame = pd.DataFrame({"count": [1]})

    def unequal_decode(self: PyArrowDataFrameCodec, payload: bytes) -> Decoded[pd.DataFrame]:
        del self, payload
        return Decoded(ModelResponse(pd.DataFrame({"count": [2]})))

    monkeypatch.setattr(PyArrowDataFrameCodec, "decode", unequal_decode)
    assert PyArrowDataFrameCodec().encode(ModelResponse(frame)) == RoundTripMismatch()


def test_dataframe_rejects_invalid_arrow_bytes() -> None:
    """Declared DataFrame bytes must contain an Arrow IPC stream."""
    assert PyArrowDataFrameCodec().decode(b"not arrow") == InvalidPayload()


def test_dataframe_codec_returns_encode_failure_for_unrepresentable_value() -> None:
    """An Arrow conversion error is an explicit failed encode value."""
    frame = pd.DataFrame({"value": [object()]})
    assert PyArrowDataFrameCodec().encode(ModelResponse(frame)) == EncodeFailure()
