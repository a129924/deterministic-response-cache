# Copyright (c) 2026 deterministic-response-cache contributors
# ruff: noqa: INP001

"""Synchronous orchestration at the Response Reuse boundary."""

from typing import cast

from deterministic_response_cache.response_reuse._cache_store import (
    CacheStore,
    CacheStoreFailure,
    CacheStoreWriteFailure,
    NotFound,
    TokenWritten,
)
from deterministic_response_cache.response_reuse.codecs.contract import (
    CodecUnavailableError,
    EncodeFailureError,
    InvalidPayloadError,
    RoundTripMismatchError,
    UnknownCodecError,
    UnsupportedPayloadError,
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

    def lookup(self, confirmed_identity: IdentityT) -> LookupOutcome[PayloadT]:  # noqa: PLR0911
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
                try:
                    response = cast("ModelResponse[PayloadT]", decode_response(stored))
                except UnknownCodecError:
                    return Unavailable(UnavailableReason.UNKNOWN_CODEC)
                except CodecUnavailableError:
                    return Unavailable(UnavailableReason.CODEC_UNAVAILABLE)
                except InvalidPayloadError:
                    return Unavailable(UnavailableReason.INVALID_PAYLOAD)
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
        try:
            stored = encode_response(cast("ModelResponse[object]", response))
        except UnsupportedPayloadError:
            return NotCached(response, NotCachedReason.UNSUPPORTED_PAYLOAD)
        except CodecUnavailableError:
            return NotCached(response, NotCachedReason.CODEC_UNAVAILABLE)
        except RoundTripMismatchError:
            return NotCached(response, NotCachedReason.ROUND_TRIP_MISMATCH)
        except EncodeFailureError:
            return NotCached(response, NotCachedReason.ENCODE_FAILURE)
        match self._store.write(confirmed_identity, stored):
            case TokenWritten():
                return Cached(response)
            case CacheStoreWriteFailure():
                return NotCached(response, NotCachedReason.STORE_WRITE_FAILURE)
            case _:
                msg = "CacheStore.write must return a write channel value"
                raise TypeError(msg)
