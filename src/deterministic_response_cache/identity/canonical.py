# Copyright (c) 2026 deterministic-response-cache contributors

"""First-party v1 canonical stages for deterministic identity construction."""

import hashlib
import json
import math
from collections.abc import Mapping
from types import MappingProxyType
from typing import cast, override

from .builders import FeatureIdentityBuilder, ModelIdentityBuilder
from .contracts import (
    EncodedIdentity,
    Encoder,
    Failure,
    Hash,
    Hasher,
    IdentityField,
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


def _path_for_string(path: str, value: str) -> str:
    """Return one JSON-quoted path segment without Unicode normalization."""
    return f"{path}[{json.dumps(value, ensure_ascii=True, separators=(',', ':'))}]"


def _non_string_path(path: str, kind: str, index: int) -> str:
    """Return a deterministic path for a value without a valid string name."""
    return f"{path}[<{kind}:{index}>]"


def _is_snapshot_list(value: object) -> bool:
    """Identify the Builder's private immutable representation of a source list."""
    return isinstance(value, tuple) and bool(
        getattr(cast("object", value), "_canonical_identity_list", False),
    )


class PureTypeValidator(Validator):
    """Validate all reachable v1 identity values before canonicalization."""

    @override
    def validate(self, identity: RawIdentity) -> Success[ValidatedIdentity] | Failure:
        """Return every discoverable validation issue or the accepted identity."""
        issues: list[ValidationIssue] = []
        valid_fields: list[IdentityField] = []
        invalid_fields: list[tuple[int, IdentityField]] = []

        for index, field in enumerate(identity.fields):
            name = cast("object", field.name)
            if isinstance(name, str):
                valid_fields.append(field)
            else:
                invalid_fields.append((index, field))

        for field in sorted(valid_fields, key=lambda candidate: candidate.name):
            self._validate_value(
                field.value,
                _path_for_string("$", field.name),
                set(),
                issues,
            )

        for index, field in invalid_fields:
            path = _non_string_path("$", "non-string-field", index)
            issues.append(
                ValidationIssue(
                    path=path,
                    code="non-string-field-name",
                    message="Identity field names must be strings.",
                ),
            )
            self._validate_value(field.value, path, set(), issues)

        if issues:
            return Failure(issues=tuple(issues))
        return Success(ValidatedIdentity(fields=identity.fields))

    def _validate_value(
        self,
        value: object,
        path: str,
        active_ids: set[int],
        issues: list[ValidationIssue],
    ) -> None:
        """Traverse one value safely and append every reachable validation issue."""
        if value is None or type(value) in {bool, int, str}:
            return
        if type(value) is float:
            if not math.isfinite(value):
                issues.append(
                    ValidationIssue(
                        path=path,
                        code="non-finite-float",
                        message="Float values must be finite.",
                    ),
                )
            return
        if isinstance(value, (list, tuple)):
            self._validate_sequence(
                cast("list[object] | tuple[object, ...]", value),
                path,
                active_ids,
                issues,
            )
            return
        if isinstance(value, Mapping):
            self._validate_mapping(
                cast("Mapping[object, object]", value),
                path,
                active_ids,
                issues,
            )
            return
        issues.append(
            ValidationIssue(
                path=path,
                code="unsupported-type",
                message="Value has an unsupported type.",
            ),
        )

    def _validate_sequence(
        self,
        value: list[object] | tuple[object, ...],
        path: str,
        active_ids: set[int],
        issues: list[ValidationIssue],
    ) -> None:
        """Validate a sequence while detecting active object-reference cycles."""
        value_id = id(value)
        if value_id in active_ids:
            issues.append(
                ValidationIssue(
                    path=path,
                    code="cyclic-reference",
                    message="Container values must not contain object-reference cycles.",
                ),
            )
            return

        active_ids.add(value_id)
        try:
            for index, item in enumerate(value):
                self._validate_value(item, f"{path}[{index}]", active_ids, issues)
        finally:
            active_ids.remove(value_id)

    def _validate_mapping(
        self,
        value: Mapping[object, object],
        path: str,
        active_ids: set[int],
        issues: list[ValidationIssue],
    ) -> None:
        """Validate mapping keys and values in the declared deterministic order."""
        value_id = id(value)
        if value_id in active_ids:
            issues.append(
                ValidationIssue(
                    path=path,
                    code="cyclic-reference",
                    message="Container values must not contain object-reference cycles.",
                ),
            )
            return

        active_ids.add(value_id)
        try:
            valid_items: list[tuple[str, object]] = []
            invalid_items: list[tuple[int, object]] = []
            for index, (key, item) in enumerate(value.items()):
                if isinstance(key, str):
                    valid_items.append((key, item))
                else:
                    invalid_items.append((index, item))

            for key, item in sorted(valid_items, key=lambda candidate: candidate[0]):
                self._validate_value(item, _path_for_string(path, key), active_ids, issues)

            for index, item in invalid_items:
                item_path = _non_string_path(path, "non-string-key", index)
                issues.append(
                    ValidationIssue(
                        path=item_path,
                        code="non-string-mapping-key",
                        message="Mapping keys must be strings.",
                    ),
                )
                self._validate_value(item, item_path, active_ids, issues)
        finally:
            active_ids.remove(value_id)


class CanonicalSorter(Sorter):
    """Sort v1 identity fields and mapping keys without changing sequence order."""

    @override
    def sort(self, identity: ValidatedIdentity) -> SortedIdentity:
        """Return fields and mappings in Unicode code-point order."""
        return SortedIdentity(
            fields=tuple(
                IdentityField(field.name, self._sort_value(field.value))
                for field in sorted(identity.fields, key=lambda candidate: candidate.name)
            ),
        )

    def _sort_value(self, value: PureType) -> PureType:
        """Canonicalize nested map order while preserving the container type boundary."""
        if isinstance(value, list):
            return [self._sort_value(item) for item in value]
        if isinstance(value, tuple):
            items = tuple(self._sort_value(item) for item in value)
            if _is_snapshot_list(value):
                return type(value)(items)
            return items
        if isinstance(value, Mapping):
            return MappingProxyType({key: self._sort_value(value[key]) for key in sorted(value)})
        return value


class CanonicalEncoder(Encoder):
    """Encode sorted v1 values as a compact canonical JSON-like string."""

    @override
    def encode(self, identity: SortedIdentity) -> EncodedIdentity:
        """Return only the public ``EncodedIdentity.value: str`` handoff."""
        grammar = [
            "identity",
            [[["str", field.name], self._encode_value(field.value)] for field in identity.fields],
        ]
        return EncodedIdentity(
            value=json.dumps(
                grammar,
                ensure_ascii=True,
                separators=(",", ":"),
                allow_nan=False,
            ),
        )

    def _encode_value(self, value: PureType) -> object:
        """Build one internal grammar object before the public string handoff."""
        if value is None:
            return ["null", None]
        if _is_snapshot_list(value):
            snapshot = cast("tuple[PureType, ...]", value)
            return ["list", [self._encode_value(item) for item in snapshot]]
        if isinstance(value, list):
            return ["list", [self._encode_value(item) for item in value]]
        if isinstance(value, tuple):
            return ["tuple", [self._encode_value(item) for item in value]]
        if isinstance(value, Mapping):
            return [
                "map",
                [[["str", key], self._encode_value(item)] for key, item in value.items()],
            ]
        return self._encode_scalar(value)

    def _encode_scalar(self, value: PureType) -> object:
        """Encode one already-validated scalar value with its fixed type tag."""
        if type(value) is bool:
            return ["bool", value]
        if type(value) is int:
            return ["int", str(value)]
        if type(value) is float:
            normalized = 0.0 if value == 0.0 else value
            return ["float", normalized.hex()]
        if type(value) is str:
            return ["str", value]
        message = "CanonicalEncoder requires a valid SortedIdentity."
        raise TypeError(message)


class CanonicalSerializer(Serializer):
    """Serialize a canonical Encoder string without reparsing it."""

    @override
    def serialize(self, identity: EncodedIdentity) -> SerializedIdentity:
        """Return the exact strict-ASCII bytes of the Encoder handoff."""
        return SerializedIdentity(value=identity.value.encode("ascii", "strict"))


class SHA256Hasher(Hasher):
    """Hash serialized canonical bytes as a lowercase SHA-256 hexadecimal digest."""

    @override
    def hash(self, identity: SerializedIdentity) -> Hash:
        """Return the exact SHA-256 digest for one serialized identity."""
        return Hash(value=hashlib.sha256(identity.value).hexdigest())


def default_model_identity_builder() -> ModelIdentityBuilder:
    """Return a fresh existing Model builder wired to the official v1 stages."""
    return ModelIdentityBuilder(
        validator=PureTypeValidator(),
        sorter=CanonicalSorter(),
        encoder=CanonicalEncoder(),
        serializer=CanonicalSerializer(),
        hasher=SHA256Hasher(),
    )


def default_feature_identity_builder() -> FeatureIdentityBuilder:
    """Return a fresh existing Feature builder wired to the official v1 stages."""
    return FeatureIdentityBuilder(
        validator=PureTypeValidator(),
        sorter=CanonicalSorter(),
        encoder=CanonicalEncoder(),
        serializer=CanonicalSerializer(),
        hasher=SHA256Hasher(),
    )
