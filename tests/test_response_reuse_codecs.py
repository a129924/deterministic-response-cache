# Copyright (c) 2026 deterministic-response-cache contributors
# pyright: reportUnknownMemberType=false

"""Focused codec, selector and stored-format contract tests."""

from dataclasses import FrozenInstanceError
from typing import cast

import pandas as pd  # pyright: ignore[reportMissingTypeStubs]
import pytest

from deterministic_response_cache.response_reuse.codecs.contract import (
    EncodeFailureError,
    InvalidPayloadError,
    RoundTripMismatchError,
    UnknownCodecError,
    UnsupportedPayloadError,
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
    stored = encode_response(response)

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
    stored = JsonResponseCodec().encode(response)
    decoded = JsonResponseCodec().decode(stored.payload)

    assert stored.codec_id is ResponseCodecId.JSON_V1
    assert decoded.value == value
    assert decoded.value is not value


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
    with pytest.raises(EncodeFailureError):
        JsonResponseCodec().encode(ModelResponse(cast("dict[str, object] | list[object]", value)))


def test_json_rejects_cyclic_tree_as_encode_failure() -> None:
    """A cycle must not escape as recursion failure or reach the Store."""
    value: list[object] = []
    value.append(value)
    with pytest.raises(EncodeFailureError):
        JsonResponseCodec().encode(ModelResponse(value))


@pytest.mark.parametrize("payload", [b"not json", b"null", b"42", b"\xff", b'{"a":NaN}'])
def test_json_rejects_invalid_stored_bytes(payload: bytes) -> None:
    """A declared JSON id does not allow malformed or scalar payloads."""
    with pytest.raises(InvalidPayloadError):
        JsonResponseCodec().decode(payload)


def test_fixed_selector_rejects_other_payloads_and_unknown_id() -> None:
    """No registry or byte sniffing can make a foreign format usable."""
    with pytest.raises(UnsupportedPayloadError):
        encode_response(ModelResponse(42))
    alien = StoredResponse(cast("ResponseCodecId", "alien/v1"), b"{}")
    with pytest.raises(UnknownCodecError):
        decode_response(alien)


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
    stored = PyArrowDataFrameCodec().encode(ModelResponse(frame))
    decoded = PyArrowDataFrameCodec().decode(stored.payload)

    assert stored.codec_id is ResponseCodecId.DATAFRAME_V1
    assert frame.equals(decoded.value)
    assert frame.dtypes.equals(decoded.value.dtypes)
    assert frame.index.equals(decoded.value.index)
    assert decoded.value is not frame


def test_dataframe_codec_rejects_round_trip_mismatch(monkeypatch: pytest.MonkeyPatch) -> None:
    """An unequal decoded frame fails before any Store write."""
    frame = pd.DataFrame({"count": [1]})

    def unequal_decode(self: PyArrowDataFrameCodec, payload: bytes) -> ModelResponse[pd.DataFrame]:
        del self, payload
        return ModelResponse(pd.DataFrame({"count": [2]}))

    monkeypatch.setattr(PyArrowDataFrameCodec, "decode", unequal_decode)
    with pytest.raises(RoundTripMismatchError):
        PyArrowDataFrameCodec().encode(ModelResponse(frame))


def test_dataframe_rejects_invalid_arrow_bytes() -> None:
    """Declared DataFrame bytes must contain an Arrow IPC stream."""
    with pytest.raises(InvalidPayloadError):
        PyArrowDataFrameCodec().decode(b"not arrow")
