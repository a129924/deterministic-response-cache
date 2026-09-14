# Copyright (c) 2026 deterministic-response-cache contributors

"""Contract tests for the public model and feature identity types."""

from dataclasses import FrozenInstanceError, fields
from inspect import Parameter, signature
from typing import cast

import pytest

from deterministic_response_cache.identity import (
    CompleteRequestIdentity,
    EncodedIdentity,
    Encoder,
    Failure,
    FeatureIdentity,
    FeatureIdentityBuilder,
    Hash,
    Hasher,
    IdentityField,
    IdentitySource,
    LeafIdentityAggregate,
    ModelIdentity,
    ModelIdentityBuilder,
    PureType,
    RawIdentity,
    SerializedIdentity,
    Serializer,
    SortedIdentity,
    Sorter,
    Success,
    ValidatedIdentity,
    ValidationIssue,
    Validator,
)


def test_identity_source_has_only_the_required_abstract_method() -> None:
    """Require every source to provide identity fields and nothing else abstract."""
    assert IdentitySource.__abstractmethods__ == frozenset({"identity_fields"})
    source_type = cast("type[object]", IdentitySource)
    with pytest.raises(TypeError):
        source_type()


def test_public_value_objects_are_frozen_and_have_exact_fields() -> None:
    """Preserve the named immutable handoffs and distinct identity value types."""
    issue = ValidationIssue(path="model", code="invalid", message="not valid")
    identity_field = IdentityField(name="model", value="gpt")
    model_identity = ModelIdentity(value=Hash(value="model-hash"))
    feature_identity = FeatureIdentity(value=Hash(value="feature-hash"))

    expected_fields = {
        IdentityField: ("name", "value"),
        RawIdentity: ("fields",),
        ValidatedIdentity: ("fields",),
        SortedIdentity: ("fields",),
        EncodedIdentity: ("value",),
        SerializedIdentity: ("value",),
        Hash: ("value",),
        ModelIdentity: ("value",),
        FeatureIdentity: ("value",),
        LeafIdentityAggregate: ("model_identity", "feature_identity"),
        CompleteRequestIdentity: ("value",),
        ValidationIssue: ("path", "code", "message"),
        Success: ("value",),
        Failure: ("issues",),
    }

    for value_type, expected in expected_fields.items():
        assert tuple(field.name for field in fields(value_type)) == expected

    with pytest.raises(FrozenInstanceError):
        model_identity.__setattr__("value", Hash(value="other"))

    assert model_identity != feature_identity
    assert LeafIdentityAggregate(model_identity, feature_identity).model_identity is model_identity
    assert CompleteRequestIdentity(value=Hash(value="complete-hash")).value.value == "complete-hash"
    assert Success(value=issue).value is issue
    assert identity_field.value == "gpt"


def test_failure_requires_an_immutable_non_empty_issue_tuple() -> None:
    """Reject construction without diagnostics while preserving every supplied issue."""
    issue = ValidationIssue(path="features[0]", code="unsupported", message="set is invalid")
    failure = Failure(issues=(issue,))

    assert failure.issues == (issue,)
    with pytest.raises(ValueError, match="at least one ValidationIssue"):
        Failure(issues=())
    with pytest.raises(FrozenInstanceError):
        failure.__setattr__("issues", ())


def test_failure_rejects_non_exact_tuple_and_non_issue_members() -> None:
    """Require the runtime diagnostics container and every member to match the contract."""
    issue = ValidationIssue(path="features[0]", code="unsupported", message="set is invalid")

    class IssueTuple(tuple[ValidationIssue, ...]):
        """A tuple subclass that must not satisfy Failure's exact tuple contract."""

        __slots__ = ()

    with pytest.raises(TypeError, match="exact tuple"):
        Failure(issues=cast("tuple[ValidationIssue, ...]", [issue]))
    with pytest.raises(TypeError, match="exact tuple"):
        Failure(issues=cast("tuple[ValidationIssue, ...]", IssueTuple((issue,))))
    with pytest.raises(TypeError, match="only ValidationIssue"):
        Failure(issues=cast("tuple[ValidationIssue, ...]", (issue, "not-an-issue")))


def test_pure_type_allows_the_declared_recursive_input_shape() -> None:
    """Make the accepted recursive value contract explicit to type checkers and readers."""
    pure_value: PureType = {
        "model": "gpt",
        "options": [True, None, {"temperature": 0.25}],
        "ordered": (1, "second"),
    }
    identity_fields: dict[str, PureType] = {"request": pure_value}

    assert identity_fields["request"] is pure_value


def test_stage_protocols_and_builder_constructors_have_locked_signatures() -> None:
    """Keep injection points and all Builder dependencies explicit and keyword-only."""
    stage_signatures = {
        Validator: ("self", "identity"),
        Sorter: ("self", "identity"),
        Encoder: ("self", "identity"),
        Serializer: ("self", "identity"),
        Hasher: ("self", "identity"),
    }
    for protocol, expected in stage_signatures.items():
        method_name = next(
            name
            for name in dir(protocol)
            if name in {"validate", "sort", "encode", "serialize", "hash"}
        )
        assert tuple(signature(getattr(protocol, method_name)).parameters) == expected

    for builder in (ModelIdentityBuilder, FeatureIdentityBuilder):
        parameters = tuple(signature(builder).parameters.values())
        assert tuple(parameter.name for parameter in parameters) == (
            "validator",
            "sorter",
            "encoder",
            "serializer",
            "hasher",
        )
        assert all(parameter.kind is Parameter.KEYWORD_ONLY for parameter in parameters)
