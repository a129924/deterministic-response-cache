# Copyright (c) 2026 deterministic-response-cache contributors

"""Direct tests for the first-party v1 canonical Identity pipeline."""

import hashlib
import re
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import cast

import pytest

from deterministic_response_cache.identity import (
    CanonicalEncoder,
    CanonicalSerializer,
    CanonicalSorter,
    EncodedIdentity,
    Encoder,
    Failure,
    Hash,
    Hasher,
    IdentityField,
    IdentitySource,
    ModelIdentity,
    ModelIdentityBuilder,
    PureType,
    PureTypeValidator,
    RawIdentity,
    SerializedIdentity,
    Serializer,
    SHA256Hasher,
    SortedIdentity,
    Sorter,
    Success,
    ValidatedIdentity,
    Validator,
    default_feature_identity_builder,
    default_model_identity_builder,
)


class Source(IdentitySource):
    """Expose fixed fields through the existing IdentitySource contract."""

    def __init__(self, fields: Mapping[str, PureType]) -> None:
        """Store source fields for one canonical builder invocation."""
        self._fields = fields

    def identity_fields(self) -> Mapping[str, PureType]:
        """Return the configured source fields."""
        return self._fields


class NeverCalledSorter:
    """Fail if a validation failure incorrectly reaches sorting."""

    def sort(self, identity: ValidatedIdentity) -> SortedIdentity:
        """Reject an unexpected downstream invocation."""
        del identity
        raise AssertionError


class NeverCalledEncoder:
    """Fail if a validation failure incorrectly reaches encoding."""

    def encode(self, identity: SortedIdentity) -> EncodedIdentity:
        """Reject an unexpected downstream invocation."""
        del identity
        raise AssertionError


class NeverCalledSerializer:
    """Fail if a validation failure incorrectly reaches serialization."""

    def serialize(self, identity: EncodedIdentity) -> SerializedIdentity:
        """Reject an unexpected downstream invocation."""
        del identity
        raise AssertionError


class NeverCalledHasher:
    """Fail if a validation failure incorrectly reaches hashing."""

    def hash(self, identity: SerializedIdentity) -> Hash:
        """Reject an unexpected downstream invocation."""
        del identity
        raise AssertionError


class ComparisonOverridingStr(str):
    """Raise if validation incorrectly treats this string subclass as sortable."""

    __slots__ = ()

    comparisons = 0

    def __lt__(self, other: object) -> bool:
        """Reject a comparator invocation that canonical validation must avoid."""
        del other
        type(self).comparisons += 1
        raise AssertionError

    def __gt__(self, other: object) -> bool:
        """Reject a reflected comparator invocation that validation must avoid."""
        del other
        type(self).comparisons += 1
        raise AssertionError


class SnapshotListSpoof(tuple[PureType, ...]):
    """Mimic the obsolete list sentinel without becoming a Builder snapshot list."""

    __slots__ = ()

    _canonical_identity_list = True


class CapturingEncoder:
    """Delegate to the concrete Encoder while retaining its public handoff for assertions."""

    def __init__(self) -> None:
        """Create an empty capture slot for a single pipeline invocation."""
        self.encoded: EncodedIdentity | None = None

    def encode(self, identity: SortedIdentity) -> EncodedIdentity:
        """Record the concrete Encoder handoff from an existing Builder pipeline."""
        self.encoded = CanonicalEncoder().encode(identity)
        return self.encoded


def _successful_value(outcome: Success[ModelIdentity]) -> str:
    """Extract a model hash while documenting the expected successful outcome."""
    return outcome.value.value.value


def _model_hash(fields: Mapping[str, PureType]) -> str:
    """Build one official model identity and return its digest string."""
    outcome = default_model_identity_builder().build(Source(fields))
    assert isinstance(outcome, Success)
    return _successful_value(outcome)


def test_concrete_stages_directly_inherit_protocols_and_mark_only_public_overrides() -> None:
    """Keep nominal stage relationships and public override markers explicit."""
    assert PureTypeValidator.__bases__ == (Validator,)
    assert CanonicalSorter.__bases__ == (Sorter,)
    assert CanonicalEncoder.__bases__ == (Encoder,)
    assert CanonicalSerializer.__bases__ == (Serializer,)
    assert SHA256Hasher.__bases__ == (Hasher,)

    assert vars(PureTypeValidator)["validate"].__override__ is True
    assert vars(CanonicalSorter)["sort"].__override__ is True
    assert vars(CanonicalEncoder)["encode"].__override__ is True
    assert vars(CanonicalSerializer)["serialize"].__override__ is True
    assert vars(SHA256Hasher)["hash"].__override__ is True

    private_helpers = (
        vars(PureTypeValidator)["_validate_value"],
        vars(PureTypeValidator)["_validate_sequence"],
        vars(PureTypeValidator)["_validate_mapping"],
        vars(CanonicalSorter)["_sort_value"],
        vars(CanonicalEncoder)["_encode_value"],
        vars(CanonicalEncoder)["_encode_scalar"],
    )
    assert all("__override__" not in vars(helper) for helper in private_helpers)


def test_encoder_returns_exact_public_string_grammar_and_serializer_returns_its_bytes() -> None:
    """Keep the Encoder's public handoff a string rather than an intermediate structure."""
    sorted_identity = CanonicalSorter().sort(
        ValidatedIdentity(
            fields=(
                IdentityField(name="sequence", value=[1, "x"]),
                IdentityField(name="integer", value=1),
                IdentityField(name="boolean", value=True),
            ),
        ),
    )

    encoded = CanonicalEncoder().encode(sorted_identity)
    expected = (
        '["identity",[[["str","boolean"],["bool",true]],'
        '[["str","integer"],["int","1"]],'
        '[["str","sequence"],["list",[["int","1"],["str","x"]]]]]]'
    )

    assert type(encoded.value) is str
    assert encoded == EncodedIdentity(value=expected)
    assert '["int","1"]' in encoded.value
    assert '["bool",true]' in encoded.value
    assert '["list",[["int","1"],["str","x"]]]' in encoded.value
    serialized = CanonicalSerializer().serialize(encoded)
    assert serialized == SerializedIdentity(value=expected.encode("ascii"))
    assert SHA256Hasher().hash(serialized) == Hash(
        value=hashlib.sha256(expected.encode("ascii")).hexdigest(),
    )


def test_canonical_stages_preserve_order_and_type_boundaries() -> None:
    """Make equal mappings equal while retaining semantically distinct input shapes."""
    first = cast(
        "Mapping[str, PureType]",
        {
            "model": {"z": 2, "a": [True, None]},
            "options": ("first", "second"),
        },
    )
    reordered = cast(
        "Mapping[str, PureType]",
        {
            "options": ("first", "second"),
            "model": {"a": [True, None], "z": 2},
        },
    )

    assert _model_hash(first) == _model_hash(reordered)
    assert _model_hash({"value": 1}) != _model_hash({"value": True})
    assert _model_hash({"value": 1}) != _model_hash({"value": 1.0})
    assert _model_hash({"value": ["x", 1]}) != _model_hash({"value": ("x", 1)})
    assert _model_hash({"value": ["x", 1]}) != _model_hash({"value": [1, "x"]})
    assert _model_hash({"value": -0.0}) == _model_hash({"value": 0.0})


def test_validator_collects_all_issues_and_stops_the_pipeline_before_downstream_stages() -> None:
    """Report every safely reachable invalid value through one unchanged Failure."""
    cyclic: list[object] = []
    cyclic.append(cyclic)
    source_fields = cast(
        "Mapping[str, PureType]",
        {
            1: "invalid field name",
            "bad_key": {1: "invalid mapping key"},
            "cycle": cyclic,
            "finite": float("inf"),
            "unsupported": {"set"},
        },
    )
    builder = ModelIdentityBuilder(
        validator=PureTypeValidator(),
        sorter=NeverCalledSorter(),
        encoder=NeverCalledEncoder(),
        serializer=NeverCalledSerializer(),
        hasher=NeverCalledHasher(),
    )

    outcome = builder.build(Source(source_fields))

    assert isinstance(outcome, Failure)
    assert [issue.code for issue in outcome.issues] == [
        "non-string-mapping-key",
        "cyclic-reference",
        "non-finite-float",
        "unsupported-type",
        "non-string-field-name",
    ]
    assert [issue.path for issue in outcome.issues] == [
        '$["bad_key"][<non-string-key:0>]',
        '$["cycle"][0][0]',
        '$["finite"]',
        '$["unsupported"]',
        "$[<non-string-field:0>]",
    ]


def test_default_factories_build_leaf_and_complete_request_identities() -> None:
    """Expose fresh existing Builders while retaining the fixed aggregate composition."""
    model_builder = default_model_identity_builder()
    feature_builder = default_feature_identity_builder()
    model_outcome = model_builder.build(Source({"name": "model", "revision": 1}))
    feature_outcome = feature_builder.build(Source({"temperature": 0.25, "enabled": True}))

    assert isinstance(model_outcome, Success)
    assert isinstance(feature_outcome, Success)
    complete_outcome = feature_builder.combine(model_outcome.value, feature_outcome.value)

    assert isinstance(complete_outcome, Success)
    assert re.fullmatch(r"[0-9a-f]{64}", complete_outcome.value.value.value)
    assert complete_outcome == default_feature_identity_builder().combine(
        model_outcome.value,
        feature_outcome.value,
    )


def test_hashes_are_deterministic_in_an_independent_python_process(tmp_path: Path) -> None:
    """Require a second process to produce the same official canonical model hash."""
    fields = cast(
        "Mapping[str, PureType]",
        {"model": {"a": [True, None], "z": 2}, "name": "example"},
    )
    expected = _model_hash(fields)
    script = "\n".join(
        (
            (
                "from deterministic_response_cache.identity import IdentitySource, Success, "
                "default_model_identity_builder"
            ),
            "class Source(IdentitySource):",
            "    def identity_fields(self):",
            f"        return {fields!r}",
            "outcome = default_model_identity_builder().build(Source())",
            "assert isinstance(outcome, Success)",
            "print(outcome.value.value.value)",
        ),
    )

    completed = subprocess.run(  # noqa: S603
        [sys.executable, "-c", script],
        capture_output=True,
        check=True,
        cwd=tmp_path,
        text=True,
    )

    assert completed.stdout.strip() == expected


def test_serializer_rejects_non_ascii_values_outside_canonical_encoder_output() -> None:
    """Keep Serializer behavior strict instead of adding an unapproved failure variant."""
    with pytest.raises(UnicodeEncodeError):
        CanonicalSerializer().serialize(EncodedIdentity(value="非 ASCII"))


def test_concrete_validator_accepts_the_declared_valid_pure_type_shape() -> None:
    """Accept nested valid values before the later concrete stages canonicalize them."""
    raw = RawIdentity(
        fields=(
            IdentityField(
                "request",
                {
                    "none": None,
                    "scalar": "value",
                    "list": [1, True, 0.25],
                    "tuple": ("first", {"nested": False}),
                },
            ),
        ),
    )

    assert PureTypeValidator().validate(raw) == Success(ValidatedIdentity(fields=raw.fields))


def test_validator_rejects_str_subclasses_without_invoking_their_comparators() -> None:
    """Reject non-exact field names and mapping keys before either sorting boundary."""
    ComparisonOverridingStr.comparisons = 0
    hostile_field = ComparisonOverridingStr("hostile-field")
    hostile_key = ComparisonOverridingStr("hostile-key")
    source_fields = cast(
        "Mapping[str, PureType]",
        {
            hostile_field: "field value",
            "mapping": {hostile_key: "key value", "valid-key": "valid value"},
        },
    )
    builder = ModelIdentityBuilder(
        validator=PureTypeValidator(),
        sorter=NeverCalledSorter(),
        encoder=NeverCalledEncoder(),
        serializer=NeverCalledSerializer(),
        hasher=NeverCalledHasher(),
    )

    outcome = builder.build(Source(source_fields))

    assert isinstance(outcome, Failure)
    assert [(issue.path, issue.code) for issue in outcome.issues] == [
        ('$["mapping"][<non-string-key:0>]', "non-string-mapping-key"),
        ("$[<non-string-field:0>]", "non-string-field-name"),
    ]
    assert ComparisonOverridingStr.comparisons == 0


def test_validator_reports_surrogates_at_field_key_and_scalar_positions_before_downstream() -> None:
    """Reject every canonical string position that contains a surrogate code point."""
    source_fields = cast(
        "Mapping[str, PureType]",
        {
            "mapping": {"\udc00key": "\ud800mapping-value"},
            "scalar": "\udfffscalar-value",
            "\ud800field": "\udffffield-value",
        },
    )
    builder = ModelIdentityBuilder(
        validator=PureTypeValidator(),
        sorter=NeverCalledSorter(),
        encoder=NeverCalledEncoder(),
        serializer=NeverCalledSerializer(),
        hasher=NeverCalledHasher(),
    )

    outcome = builder.build(Source(source_fields))

    assert isinstance(outcome, Failure)
    assert [(issue.path, issue.code) for issue in outcome.issues] == [
        ('$["mapping"]["\\udc00key"]', "surrogate-code-point"),
        ('$["mapping"]["\\udc00key"]', "surrogate-code-point"),
        ('$["scalar"]', "surrogate-code-point"),
        ('$["\\ud800field"]', "surrogate-code-point"),
        ('$["\\ud800field"]', "surrogate-code-point"),
    ]


def test_non_bmp_text_has_exact_ascii_handoffs_and_fixed_default_pipeline_hash() -> None:
    """Keep a Unicode scalar distinct from invalid surrogate spellings through every handoff."""
    raw = RawIdentity(fields=(IdentityField(name="value", value="\U0001f600"),))
    validation = PureTypeValidator().validate(raw)
    assert isinstance(validation, Success)

    encoded = CanonicalEncoder().encode(CanonicalSorter().sort(validation.value))
    expected = '["identity",[[["str","value"],["str","\\ud83d\\ude00"]]]]'

    assert encoded == EncodedIdentity(value=expected)
    serialized = CanonicalSerializer().serialize(encoded)
    assert serialized == SerializedIdentity(value=expected.encode("ascii"))
    assert SHA256Hasher().hash(serialized) == Hash(
        value="02c41d0e0019f532fef8e908145a6fdde13c471e23d3a64c2d70a8ef6b3372a6",
    )
    assert (
        _model_hash({"value": "\U0001f600"})
        == "02c41d0e0019f532fef8e908145a6fdde13c471e23d3a64c2d70a8ef6b3372a6"
    )


def test_only_exact_builder_snapshot_lists_encode_as_lists() -> None:
    """Keep a tuple spoof separate while the private Builder snapshot remains a list grammar."""
    spoofed = SnapshotListSpoof((1, "x"))
    spoofed_encoded = CanonicalEncoder().encode(
        SortedIdentity(fields=(IdentityField(name="value", value=cast("PureType", spoofed)),)),
    )
    capturing_encoder = CapturingEncoder()
    builder = ModelIdentityBuilder(
        validator=PureTypeValidator(),
        sorter=CanonicalSorter(),
        encoder=capturing_encoder,
        serializer=CanonicalSerializer(),
        hasher=SHA256Hasher(),
    )

    outcome = builder.build(Source({"value": [1, "x"]}))

    assert isinstance(outcome, Success)
    assert spoofed_encoded == EncodedIdentity(
        value='["identity",[[["str","value"],["tuple",[["int","1"],["str","x"]]]]]]',
    )
    assert capturing_encoder.encoded == EncodedIdentity(
        value='["identity",[[["str","value"],["list",[["int","1"],["str","x"]]]]]]',
    )
