# Copyright (c) 2026 deterministic-response-cache contributors

"""Response Reuse end-to-end codec and Store behavior."""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import cast

import pandas as pd  # pyright: ignore[reportMissingTypeStubs]
import pytest

from deterministic_response_cache.response_reuse._cache_store import NotFound
from deterministic_response_cache.response_reuse.codecs.contract import (
    CodecUnavailable,
    Decoded,
    EncodeResult,
)
from deterministic_response_cache.response_reuse.codecs.pyarrow_dataframe import (
    PyArrowDataFrameCodec,
)
from deterministic_response_cache.response_reuse.eligibility.policy import (
    ReuseAllowed,
    ReuseDenied,
    ReuseEligibilityDecision,
)
from deterministic_response_cache.response_reuse.model_response import ModelResponse
from deterministic_response_cache.response_reuse.outcomes import (
    Cached,
    Hit,
    Miss,
    NotCached,
    NotCachedReason,
    Unavailable,
    UnavailableReason,
)
from deterministic_response_cache.response_reuse.protocol import ResponseReuseProtocol
from deterministic_response_cache.response_reuse.stored_response import (
    ResponseCodecId,
    StoredResponse,
)
from deterministic_response_cache.response_reuse.stores.in_memory import InMemoryCacheStore


class AllowPolicy:
    """Allow a decoded response without inspecting its identity."""

    def evaluate(self, response: ModelResponse[object], /) -> ReuseEligibilityDecision:
        """Return the existing eligibility value channel."""
        del response
        return ReuseAllowed()


class DenyPolicy:
    """Reject a decoded response after a successful Store read."""

    def evaluate(self, response: ModelResponse[object], /) -> ReuseEligibilityDecision:
        """Return the existing denial value channel."""
        del response
        return ReuseDenied()


def test_json_record_and_lookup_use_stored_bytes_and_opaque_identity() -> None:
    """Protocol writes an envelope and returns a fresh decoded native value."""
    identity = object()
    store = InMemoryCacheStore[object, StoredResponse]()
    protocol = ResponseReuseProtocol(store, eligibility_policy=AllowPolicy())
    response = ModelResponse({"answer": [1, 2]})

    assert protocol.lookup(identity) == Miss()
    assert protocol.record(identity, response) == Cached(response)
    stored = store.read(identity)
    assert isinstance(stored, StoredResponse)
    assert stored.codec_id is ResponseCodecId.JSON_V1
    assert isinstance(stored.payload, bytes)
    hit = protocol.lookup(identity)
    assert hit == Hit(response)
    assert isinstance(hit, Hit)
    assert hit.response.value is not response.value


def test_dataframe_hits_are_independent() -> None:
    """Changing one hit does not mutate retained bytes or later hits."""
    identity = object()
    store = InMemoryCacheStore[object, StoredResponse]()
    protocol = ResponseReuseProtocol(store, eligibility_policy=AllowPolicy())
    frame = pd.DataFrame({"count": pd.Series([1, None], dtype="Int64")})
    response = ModelResponse(frame)

    assert protocol.record(identity, response) == Cached(response)
    first = protocol.lookup(identity)
    assert isinstance(first, Hit)
    assert isinstance(first.response.value, pd.DataFrame)
    first.response.value.loc[0, "count"] = 99
    second = protocol.lookup(identity)
    assert isinstance(second, Hit)
    assert frame.equals(second.response.value)
    assert first.response.value is not second.response.value


def test_dataframe_mismatch_never_reaches_store(monkeypatch: pytest.MonkeyPatch) -> None:
    """A failed equality gate retains the exact caller response."""
    store = InMemoryCacheStore[object, StoredResponse]()
    protocol = ResponseReuseProtocol(store, eligibility_policy=AllowPolicy())
    identity = object()
    response = ModelResponse(pd.DataFrame({"count": [1]}))

    def unequal_decode(self: PyArrowDataFrameCodec, payload: bytes) -> Decoded[pd.DataFrame]:
        del self, payload
        return Decoded(ModelResponse(pd.DataFrame({"count": [2]})))

    monkeypatch.setattr(PyArrowDataFrameCodec, "decode", unequal_decode)
    outcome = protocol.record(identity, response)

    assert outcome == NotCached(response, NotCachedReason.ROUND_TRIP_MISMATCH)
    assert isinstance(outcome, NotCached)
    assert outcome.response is response
    assert store.read(identity) == NotFound()


def test_unsupported_payload_retains_original_response_without_store_write() -> None:
    """An unsupported native response remains available to the caller."""
    store = InMemoryCacheStore[object, StoredResponse]()
    protocol = ResponseReuseProtocol(store, eligibility_policy=AllowPolicy())
    identity = object()
    response = ModelResponse(42)

    assert protocol.record(identity, response) == NotCached(
        response,
        NotCachedReason.UNSUPPORTED_PAYLOAD,
    )
    assert store.read(identity) == NotFound()
    assert protocol.lookup(identity) == Miss()


@pytest.mark.parametrize(
    "value",
    [
        {1: "non-string key"},
        {"nonfinite": float("nan")},
        {"tuple": (1, 2)},
        {"object": object()},
        {"nested": [{"tuple": (1, 2)}]},
        [float("inf")],
    ],
)
def test_unsupported_json_tree_has_protocol_reason_and_no_store_write(value: object) -> None:
    """Known lossy JSON trees retain the caller response as unsupported."""
    identity = object()
    store = InMemoryCacheStore[object, StoredResponse]()
    protocol = ResponseReuseProtocol(store, eligibility_policy=AllowPolicy())
    response = ModelResponse(value)

    outcome = protocol.record(identity, response)

    assert isinstance(outcome, NotCached)
    assert outcome.reason is NotCachedReason.UNSUPPORTED_PAYLOAD
    assert outcome.response is response
    assert store.read(identity) == NotFound()


def test_json_serializer_failure_has_distinct_record_reason(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A serializer error remains an encode failure without a Store write."""
    identity = object()
    store = InMemoryCacheStore[object, StoredResponse]()
    protocol = ResponseReuseProtocol(store, eligibility_policy=AllowPolicy())
    response = ModelResponse({"answer": 1})

    def failing_dumps(*args: object, **kwargs: object) -> str:
        del args, kwargs
        raise TypeError

    monkeypatch.setattr(json, "dumps", failing_dumps)
    outcome = protocol.record(identity, response)

    assert isinstance(outcome, NotCached)
    assert outcome.reason is NotCachedReason.ENCODE_FAILURE
    assert outcome.response is response
    assert store.read(identity) == NotFound()


def test_dataframe_arrow_failure_has_encode_failure_reason() -> None:
    """An Arrow conversion failure retains the frame without a Store write."""
    identity = object()
    store = InMemoryCacheStore[object, StoredResponse]()
    protocol = ResponseReuseProtocol(store, eligibility_policy=AllowPolicy())
    response = ModelResponse(pd.DataFrame({"value": [object()]}))

    outcome = protocol.record(identity, response)

    assert isinstance(outcome, NotCached)
    assert outcome.reason is NotCachedReason.ENCODE_FAILURE
    assert outcome.response is response
    assert store.read(identity) == NotFound()


def test_unexpected_serializer_error_propagates(monkeypatch: pytest.MonkeyPatch) -> None:
    """An unexpected program error is not translated into an expected result."""
    identity = object()
    store = InMemoryCacheStore[object, StoredResponse]()
    protocol = ResponseReuseProtocol(store, eligibility_policy=AllowPolicy())

    def broken_dumps(*args: object, **kwargs: object) -> str:
        del args, kwargs
        raise RuntimeError

    monkeypatch.setattr(json, "dumps", broken_dumps)
    with pytest.raises(RuntimeError):
        protocol.record(identity, ModelResponse({"answer": 1}))
    assert store.read(identity) == NotFound()


def test_dataframe_codec_unavailable_on_record(monkeypatch: pytest.MonkeyPatch) -> None:
    """A selected unavailable optional codec retains the original frame."""
    identity = object()
    store = InMemoryCacheStore[object, StoredResponse]()
    protocol = ResponseReuseProtocol(store, eligibility_policy=AllowPolicy())
    response = ModelResponse(pd.DataFrame({"count": [1]}))

    def unavailable_encode(
        self: PyArrowDataFrameCodec,
        response: ModelResponse[pd.DataFrame],
    ) -> EncodeResult:
        del self, response
        return CodecUnavailable()

    monkeypatch.setattr(PyArrowDataFrameCodec, "encode", unavailable_encode)
    outcome = protocol.record(identity, response)

    assert isinstance(outcome, NotCached)
    assert outcome.reason is NotCachedReason.CODEC_UNAVAILABLE
    assert outcome.response is response
    assert store.read(identity) == NotFound()


def test_invalid_envelope_and_unknown_codec_are_unavailable() -> None:
    """Lookup never treats a damaged entry as absence."""
    identity = object()
    store = InMemoryCacheStore[object, StoredResponse]()
    protocol = ResponseReuseProtocol(store, eligibility_policy=AllowPolicy())
    store.write(identity, StoredResponse(ResponseCodecId.JSON_V1, b"not json"))
    assert protocol.lookup(identity) == Unavailable(UnavailableReason.INVALID_PAYLOAD)
    store.write(identity, StoredResponse(cast("ResponseCodecId", "alien/v1"), b"{}"))
    assert protocol.lookup(identity) == Unavailable(UnavailableReason.UNKNOWN_CODEC)


def test_foreign_malformed_envelope_is_unavailable() -> None:
    """A foreign Store entry with invalid shape or bytes fails closed."""
    identity = object()
    store = InMemoryCacheStore[object, StoredResponse]()
    protocol = ResponseReuseProtocol(store, eligibility_policy=AllowPolicy())

    store.write(identity, StoredResponse(ResponseCodecId.JSON_V1, cast("bytes", "{}")))
    assert protocol.lookup(identity) == Unavailable(UnavailableReason.INVALID_PAYLOAD)
    store.write(identity, cast("StoredResponse", object()))
    assert protocol.lookup(identity) == Unavailable(UnavailableReason.INVALID_PAYLOAD)


def test_eligibility_denial_remains_miss() -> None:
    """A valid decoded entry may still be denied by policy."""
    identity = object()
    store = InMemoryCacheStore[object, StoredResponse]()
    allowing = ResponseReuseProtocol(store, eligibility_policy=AllowPolicy())
    denying = ResponseReuseProtocol(store, eligibility_policy=DenyPolicy())
    allowing.record(identity, ModelResponse({"answer": "yes"}))
    assert denying.lookup(identity) == Miss()


def test_json_only_direct_import_works_without_site_packages() -> None:
    """A base Python process can import and use the JSON defining modules."""
    project_root = Path(__file__).resolve().parents[1]
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(project_root / "src")
    script = (
        "from deterministic_response_cache.response_reuse.model_response import ModelResponse;"
        "from deterministic_response_cache.response_reuse.codecs.json_response "
        "import JsonResponseCodec;"
        "from deterministic_response_cache.response_reuse.codecs.contract "
        "import Encoded, Decoded, CodecUnavailable;"
        "from deterministic_response_cache.response_reuse.codecs.selector "
        "import encode_response, decode_response;"
        "from deterministic_response_cache.response_reuse.protocol "
        "import ResponseReuseProtocol;"
        "from deterministic_response_cache.response_reuse.stored_response "
        "import StoredResponse, ResponseCodecId;"
        "from deterministic_response_cache.response_reuse.stores.in_memory "
        "import InMemoryCacheStore;"
        "from deterministic_response_cache.response_reuse.outcomes "
        "import Unavailable, UnavailableReason;"
        "value = ModelResponse({'answer': [1]});"
        "encoded = encode_response(value);"
        "assert isinstance(encoded, Encoded);"
        "decoded = decode_response(encoded.stored);"
        "assert isinstance(decoded, Decoded) and decoded.response.value == value.value;"
        "store = InMemoryCacheStore();"
        "store.write('key', StoredResponse(ResponseCodecId.DATAFRAME_V1, b'bytes'));"
        "assert decode_response(StoredResponse(ResponseCodecId.DATAFRAME_V1, b'bytes')) "
        "== CodecUnavailable();"
        "protocol = ResponseReuseProtocol(store, eligibility_policy=object());"
        "assert protocol.lookup('key') == Unavailable(UnavailableReason.CODEC_UNAVAILABLE)"
    )
    result = subprocess.run(  # noqa: S603
        [sys.executable, "-S", "-c", script],
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
