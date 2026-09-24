# Copyright (c) 2026 deterministic-response-cache contributors
# ruff: noqa: INP001

"""Synchronous orchestration at the Response Reuse boundary."""

from typing import assert_never, cast

from deterministic_response_cache.response_reuse._cache_store import (
    CacheStore,
    CacheStoreFailure,
    CacheStoreWriteFailure,
    NotFound,
    TokenWritten,
)
from deterministic_response_cache.response_reuse.codecs.contract import (
    CodecUnavailable,
    Decoded,
    Encoded,
    EncodeFailure,
    InvalidPayload,
    RoundTripMismatch,
    UnknownCodec,
    UnsupportedPayload,
)
from deterministic_response_cache.response_reuse.codecs.selector import (
    decode_response,
    encode_response,
)
from deterministic_response_cache.response_reuse.eligibility.policy import (
    ReuseAllowed,
    ReuseDenied,
    ReuseEligibilityPolicy,
)
from deterministic_response_cache.response_reuse.model_response import ModelResponse
from deterministic_response_cache.response_reuse.outcomes import (
    Cached,
    Hit,
    LookupOutcome,
    Miss,
    NotCached,
    NotCachedReason,
    RecordOutcome,
    Unavailable,
    UnavailableReason,
)
from deterministic_response_cache.response_reuse.stored_response import StoredResponse


class ResponseReuseProtocol[IdentityT, PayloadT]:
    """Map internal CacheStore operations to deterministic reuse outcomes."""

    def __init__(
        self,
        store: CacheStore[IdentityT, StoredResponse],
        *,
        eligibility_policy: ReuseEligibilityPolicy[ModelResponse[PayloadT]],
    ) -> None:
        """Create the protocol with its store and reuse eligibility policy."""
        self._store = store
        self._eligibility_policy = eligibility_policy

    def lookup(self, confirmed_identity: IdentityT) -> LookupOutcome[PayloadT]:  # noqa: C901, PLR0911
        """Find a reusable response without interpreting the identity."""
        read_result: object = self._store.read(confirmed_identity)
        match read_result:
            case NotFound():
                return Miss()
            case CacheStoreFailure():
                return Unavailable(UnavailableReason.STORE_FAILURE)
            case None:  # pyright: ignore[reportUnnecessaryComparison]
                msg = "CacheStore.read must not return None"
                raise TypeError(msg)
            case StoredResponse() as stored:
                decoded = decode_response(stored)
                match decoded:
                    case UnknownCodec():
                        return Unavailable(UnavailableReason.UNKNOWN_CODEC)
                    case CodecUnavailable():
                        return Unavailable(UnavailableReason.CODEC_UNAVAILABLE)
                    case InvalidPayload():
                        return Unavailable(UnavailableReason.INVALID_PAYLOAD)
                    case Decoded(response=decoded_response):
                        response = cast("ModelResponse[PayloadT]", decoded_response)
                    case _ as unreachable:
                        assert_never(unreachable)
                decision = self._eligibility_policy.evaluate(response)
                if type(decision) is ReuseAllowed:
                    return Hit(response)
                if type(decision) is ReuseDenied:
                    return Miss()
                msg = "ReuseEligibilityPolicy.evaluate must return a decision value"
                raise TypeError(msg)
            case _:
                return Unavailable(UnavailableReason.INVALID_PAYLOAD)

    def record(
        self,
        confirmed_identity: IdentityT,
        response: ModelResponse[PayloadT],
    ) -> RecordOutcome[PayloadT]:
        """Attempt to retain a response while preserving it on write failure."""
        encoded = encode_response(cast("ModelResponse[object]", response))
        match encoded:
            case UnsupportedPayload():
                return NotCached(response, NotCachedReason.UNSUPPORTED_PAYLOAD)
            case CodecUnavailable():
                return NotCached(response, NotCachedReason.CODEC_UNAVAILABLE)
            case RoundTripMismatch():
                return NotCached(response, NotCachedReason.ROUND_TRIP_MISMATCH)
            case EncodeFailure():
                return NotCached(response, NotCachedReason.ENCODE_FAILURE)
            case Encoded(stored=stored):
                pass
            case _ as unreachable:
                assert_never(unreachable)
        match self._store.write(confirmed_identity, stored):
            case TokenWritten():
                return Cached(response)
            case CacheStoreWriteFailure():
                return NotCached(response, NotCachedReason.STORE_WRITE_FAILURE)
            case _:
                msg = "CacheStore.write must return a write channel value"
                raise TypeError(msg)
