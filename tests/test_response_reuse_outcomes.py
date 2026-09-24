# Copyright (c) 2026 deterministic-response-cache contributors

"""Value semantics for Response Reuse outcomes."""

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


def test_lookup_outcomes_are_distinct_value_types() -> None:
    """Lookup markers remain distinguishable outcome values."""
    assert Miss() == Miss()
    assert Miss() != Unavailable(UnavailableReason.STORE_FAILURE)


def test_lookup_outcome_preserves_response_object() -> None:
    """Hit retains the exact response object supplied to it."""
    response = ModelResponse({"answer": "yes"})
    outcome: LookupOutcome[dict[str, str]] = Hit(response)

    assert isinstance(outcome, Hit)
    assert outcome.response is response


def test_record_outcome_preserves_response_object() -> None:
    """Both retention outcomes preserve their response payload."""
    response = ModelResponse({"answer": "yes"})
    cached: RecordOutcome[dict[str, str]] = Cached(response)
    not_cached: RecordOutcome[dict[str, str]] = NotCached(
        response,
        NotCachedReason.STORE_WRITE_FAILURE,
    )

    assert isinstance(cached, Cached)
    assert cached.response is response
    assert isinstance(not_cached, NotCached)
    assert not_cached.response is response
