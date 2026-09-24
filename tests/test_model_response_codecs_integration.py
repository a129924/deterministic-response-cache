# Copyright (c) 2026 deterministic-response-cache contributors

"""Response Reuse end-to-end codec and Store behavior."""

import os
import subprocess
import sys
from pathlib import Path
from typing import cast

import pandas as pd  # pyright: ignore[reportMissingTypeStubs]
import pytest

from deterministic_response_cache.response_reuse._cache_store import NotFound
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

    def unequal_decode(self: PyArrowDataFrameCodec, payload: bytes) -> ModelResponse[pd.DataFrame]:
        del self, payload
        return ModelResponse(pd.DataFrame({"count": [2]}))

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


def test_invalid_envelope_and_unknown_codec_are_unavailable() -> None:
    """Lookup never treats a damaged entry as absence."""
    identity = object()
    store = InMemoryCacheStore[object, StoredResponse]()
    protocol = ResponseReuseProtocol(store, eligibility_policy=AllowPolicy())
    store.write(identity, StoredResponse(ResponseCodecId.JSON_V1, b"not json"))
    assert protocol.lookup(identity) == Unavailable(UnavailableReason.INVALID_PAYLOAD)
    store.write(identity, StoredResponse(cast("ResponseCodecId", "alien/v1"), b"{}"))
    assert protocol.lookup(identity) == Unavailable(UnavailableReason.UNKNOWN_CODEC)


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
        "assert decode_response(encode_response(value)).value == value.value;"
        "store = InMemoryCacheStore();"
        "store.write('key', StoredResponse(ResponseCodecId.DATAFRAME_V1, b'bytes'));"
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
