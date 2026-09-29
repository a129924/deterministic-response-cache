# Copyright (c) 2026 deterministic-response-cache contributors

"""Value semantics for Response Reuse outcomes."""

import pandas as pd  # pyright: ignore[reportMissingTypeStubs]

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


def test_model_response_keeps_json_value_equality() -> None:
    """Dict and list responses compare by their native Python values."""
    assert ModelResponse({"answer": [1]}) == ModelResponse({"answer": [1]})
    assert ModelResponse([1, {"answer": True}]) == ModelResponse([1, {"answer": True}])
    assert ModelResponse({"answer": [1]}) != ModelResponse({"answer": [2]})
    assert ModelResponse([1]) != ModelResponse([2])


def test_dataframe_response_and_public_outcomes_use_boolean_value_equality() -> None:
    """Different frame objects compare by DataFrame.equals through public wrappers."""
    frame = pd.DataFrame({"count": [1, 2]})
    equal_frame = frame.copy(deep=True)
    different_frame = pd.DataFrame({"count": [1, 3]})
    response = ModelResponse(frame)
    equal_response = ModelResponse(equal_frame)
    different_response = ModelResponse(different_frame)

    assert frame is not equal_frame
    assert (response == equal_response) is True
    assert (response == different_response) is False
    assert (response == ModelResponse({"count": [1, 2]})) is False
    assert (ModelResponse({"count": [1, 2]}) == response) is False
    assert (Hit(response) == Hit(equal_response)) is True
    assert (Hit(response) == Hit(different_response)) is False
    assert (Cached(response) == Cached(equal_response)) is True
    assert (Cached(response) == Cached(different_response)) is False
