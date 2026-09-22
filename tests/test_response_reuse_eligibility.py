# Copyright (c) 2026 deterministic-response-cache contributors

"""Public contract tests for Response Reuse eligibility decisions."""

from dataclasses import FrozenInstanceError, fields
from inspect import Parameter, signature

import pytest

from deterministic_response_cache.response_reuse.eligibility.policy import (
    ReuseAllowed,
    ReuseDenied,
    ReuseEligibilityDecision,
    ReuseEligibilityPolicy,
)


class StructuralAllowPolicy:
    """Supply an allow decision without inheriting the policy Protocol."""

    def __init__(self) -> None:
        """Record each opaque response supplied through the structural contract."""
        self.evaluated_responses: list[object] = []

    def evaluate(self, response: object, /) -> ReuseEligibilityDecision:
        """Approve the supplied response through the required positional API."""
        self.evaluated_responses.append(response)
        return ReuseAllowed()


def _evaluate_through_policy_contract(
    policy: ReuseEligibilityPolicy[object],
    response: object,
) -> ReuseEligibilityDecision:
    """Make generic structural Protocol compatibility a static type contract."""
    return policy.evaluate(response)


@pytest.mark.parametrize("decision_type", [ReuseAllowed, ReuseDenied])
def test_reuse_decisions_are_fieldless_frozen_slotted_value_objects(
    decision_type: type[ReuseAllowed] | type[ReuseDenied],
) -> None:
    """Both legal decisions are immutable, compact, and equal by their value type."""
    decision = decision_type()

    assert tuple(field.name for field in fields(decision)) == ()
    assert not hasattr(decision, "__dict__")
    assert decision == decision_type()
    with pytest.raises((FrozenInstanceError, TypeError)):
        decision.__setattr__("forbidden", object())


def test_reuse_decisions_are_distinct_direct_module_contracts() -> None:
    """Allow and deny stay distinguishable on their sole supported import surface."""
    allowed = ReuseAllowed()
    denied = ReuseDenied()
    expected_module = "deterministic_response_cache.response_reuse.eligibility.policy"

    assert allowed != denied
    assert type(allowed) is not type(denied)
    assert ReuseAllowed.__module__ == expected_module
    assert ReuseDenied.__module__ == expected_module
    assert ReuseEligibilityPolicy.__module__ == expected_module


def test_reuse_eligibility_policy_has_a_structural_positional_only_evaluate_contract() -> None:
    """A policy remains generic, structural, and limited to response evaluation."""
    policy = StructuralAllowPolicy()
    response = object()
    method_parameters = tuple(
        signature(ReuseEligibilityPolicy[object].evaluate).parameters.values(),
    )

    decision: ReuseEligibilityDecision = _evaluate_through_policy_contract(policy, response)

    assert tuple(parameter.name for parameter in method_parameters) == ("self", "response")
    assert method_parameters[1].kind is Parameter.POSITIONAL_ONLY
    assert decision == ReuseAllowed()
    assert policy.evaluated_responses == [response]
