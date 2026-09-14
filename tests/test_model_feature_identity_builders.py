# Copyright (c) 2026 deterministic-response-cache contributors

"""Behavioral tests for injected model and feature identity pipeline builders."""

from collections.abc import Mapping

from deterministic_response_cache.identity import (
    CompleteRequestIdentity,
    EncodedIdentity,
    Failure,
    FeatureIdentity,
    FeatureIdentityBuilder,
    Hash,
    IdentityField,
    IdentitySource,
    ModelIdentity,
    ModelIdentityBuilder,
    PureType,
    RawIdentity,
    SerializedIdentity,
    SortedIdentity,
    Success,
    ValidatedIdentity,
    ValidationIssue,
)


class Source(IdentitySource):
    """A test source with an intentionally mutable top-level mapping."""

    def __init__(self, source_fields: Mapping[str, PureType]) -> None:
        """Store the supplied source mapping for Builder snapshot verification."""
        self._source_fields = source_fields

    def identity_fields(self) -> Mapping[str, PureType]:
        """Return the identity fields visible to the Builder."""
        return self._source_fields


class RecordingValidator:
    """Record raw inputs and either pass fields through or return one configured failure."""

    def __init__(self, calls: list[str], failure: Failure | None = None) -> None:
        """Initialize the shared call log and optional validation result."""
        self.calls = calls
        self.failure = failure
        self.inputs: list[RawIdentity] = []

    def validate(self, identity: RawIdentity) -> Success[ValidatedIdentity] | Failure:
        """Record validation and produce its configured outcome."""
        self.calls.append("validate")
        self.inputs.append(identity)
        if self.failure is not None:
            return self.failure
        return Success(ValidatedIdentity(fields=identity.fields))


class RecordingSorter:
    """Record validated handoffs and preserve fields for the next fake stage."""

    def __init__(self, calls: list[str]) -> None:
        """Initialize the shared call log."""
        self.calls = calls
        self.inputs: list[ValidatedIdentity] = []

    def sort(self, identity: ValidatedIdentity) -> SortedIdentity:
        """Record and return a named sorted handoff."""
        self.calls.append("sort")
        self.inputs.append(identity)
        return SortedIdentity(fields=identity.fields)


class RecordingEncoder:
    """Record sorted handoffs and return an opaque encoded value."""

    def __init__(self, calls: list[str]) -> None:
        """Initialize the shared call log."""
        self.calls = calls
        self.inputs: list[SortedIdentity] = []

    def encode(self, identity: SortedIdentity) -> EncodedIdentity:
        """Record and return a named encoded handoff."""
        self.calls.append("encode")
        self.inputs.append(identity)
        return EncodedIdentity(value="encoded")


class RecordingSerializer:
    """Record encoded handoffs and return deterministic bytes."""

    def __init__(self, calls: list[str]) -> None:
        """Initialize the shared call log."""
        self.calls = calls
        self.inputs: list[EncodedIdentity] = []

    def serialize(self, identity: EncodedIdentity) -> SerializedIdentity:
        """Record and return a named serialized handoff."""
        self.calls.append("serialize")
        self.inputs.append(identity)
        return SerializedIdentity(value=b"serialized")


class RecordingHasher:
    """Record serialized handoffs and return configured opaque hashes in order."""

    def __init__(self, calls: list[str], hashes: list[Hash]) -> None:
        """Initialize the shared call log and queued digest values."""
        self.calls = calls
        self.hashes = hashes
        self.inputs: list[SerializedIdentity] = []

    def hash(self, identity: SerializedIdentity) -> Hash:
        """Record one serialized value and return the next configured hash."""
        self.calls.append("hash")
        self.inputs.append(identity)
        return self.hashes.pop(0)


def test_leaf_builders_snapshot_sources_and_run_each_stage_in_locked_order() -> None:
    """Build distinct model and feature identities through every injected stage."""
    calls: list[str] = []
    validator = RecordingValidator(calls)
    sorter = RecordingSorter(calls)
    encoder = RecordingEncoder(calls)
    serializer = RecordingSerializer(calls)
    hasher = RecordingHasher(calls, [Hash("model-hash"), Hash("feature-hash")])
    model_builder = ModelIdentityBuilder(
        validator=validator,
        sorter=sorter,
        encoder=encoder,
        serializer=serializer,
        hasher=hasher,
    )
    feature_builder = FeatureIdentityBuilder(
        validator=validator,
        sorter=sorter,
        encoder=encoder,
        serializer=serializer,
        hasher=hasher,
    )
    versions: list[PureType] = [1, 2]
    nested: dict[str, PureType] = {"versions": versions}
    model_fields: dict[str, PureType] = {"name": "model", "nested": nested}
    feature_fields: dict[str, PureType] = {"flag": True, "ordered": ("first", "second")}

    model_outcome = model_builder.build(Source(model_fields))
    feature_outcome = feature_builder.build(Source(feature_fields))
    model_fields["name"] = "changed-after-snapshot"
    versions.append(3)
    nested["changed-after-snapshot"] = True

    assert model_outcome == Success(ModelIdentity(value=Hash("model-hash")))
    assert feature_outcome == Success(FeatureIdentity(value=Hash("feature-hash")))
    assert calls == ["validate", "sort", "encode", "serialize", "hash"] * 2
    assert validator.inputs[0] == RawIdentity(
        fields=(
            IdentityField("name", "model"),
            IdentityField("nested", {"versions": [1, 2]}),
        ),
    )
    assert validator.inputs[1] == RawIdentity(
        fields=(
            IdentityField(name="flag", value=True),
            IdentityField("ordered", ("first", "second")),
        ),
    )
    assert sorter.inputs == [
        ValidatedIdentity(fields=raw_identity.fields) for raw_identity in validator.inputs
    ]
    assert encoder.inputs == [
        SortedIdentity(fields=validated.fields) for validated in sorter.inputs
    ]
    assert serializer.inputs == [EncodedIdentity(value="encoded"), EncodedIdentity(value="encoded")]
    assert hasher.inputs == [SerializedIdentity(value=b"serialized")] * 2


def test_validation_failure_is_returned_unchanged_without_downstream_stage_calls() -> None:
    """Short-circuit both leaf and aggregate pipeline invocations on validation failure."""
    calls: list[str] = []
    failure = Failure(
        issues=(
            ValidationIssue(path="model", code="invalid", message="set values are invalid"),
            ValidationIssue(path="feature", code="invalid", message="non-string key is invalid"),
        ),
    )
    validator = RecordingValidator(calls, failure=failure)
    sorter = RecordingSorter(calls)
    encoder = RecordingEncoder(calls)
    serializer = RecordingSerializer(calls)
    hasher = RecordingHasher(calls, [Hash("unused")])
    model_builder = ModelIdentityBuilder(
        validator=validator,
        sorter=sorter,
        encoder=encoder,
        serializer=serializer,
        hasher=hasher,
    )
    feature_builder = FeatureIdentityBuilder(
        validator=validator,
        sorter=sorter,
        encoder=encoder,
        serializer=serializer,
        hasher=hasher,
    )

    assert model_builder.build(Source({"invalid": "input"})) is failure
    assert (
        feature_builder.combine(ModelIdentity(Hash("model")), FeatureIdentity(Hash("feature")))
        is failure
    )
    assert calls == ["validate", "validate"]
    assert sorter.inputs == []
    assert encoder.inputs == []
    assert serializer.inputs == []
    assert hasher.inputs == []


def test_combine_runs_a_second_pipeline_for_the_fixed_leaf_aggregate() -> None:
    """Compose leaf hashes through fresh canonicalization rather than string concatenation."""
    calls: list[str] = []
    validator = RecordingValidator(calls)
    sorter = RecordingSorter(calls)
    encoder = RecordingEncoder(calls)
    serializer = RecordingSerializer(calls)
    hasher = RecordingHasher(calls, [Hash("complete-hash")])
    builder = FeatureIdentityBuilder(
        validator=validator,
        sorter=sorter,
        encoder=encoder,
        serializer=serializer,
        hasher=hasher,
    )
    model_identity = ModelIdentity(value=Hash("model-hash"))
    feature_identity = FeatureIdentity(value=Hash("feature-hash"))

    outcome = builder.combine(model_identity, feature_identity)

    expected_raw_identity = RawIdentity(
        fields=(
            IdentityField("model_identity", "model-hash"),
            IdentityField("feature_identity", "feature-hash"),
        ),
    )
    assert outcome == Success(CompleteRequestIdentity(value=Hash("complete-hash")))
    assert calls == ["validate", "sort", "encode", "serialize", "hash"]
    assert validator.inputs == [expected_raw_identity]
    assert sorter.inputs == [ValidatedIdentity(fields=expected_raw_identity.fields)]
    assert encoder.inputs == [SortedIdentity(fields=expected_raw_identity.fields)]
    assert serializer.inputs == [EncodedIdentity(value="encoded")]
    assert hasher.inputs == [SerializedIdentity(value=b"serialized")]
