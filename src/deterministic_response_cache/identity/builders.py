# Copyright (c) 2026 deterministic-response-cache contributors

"""Injected orchestration for model, feature, and complete request identities."""

from collections.abc import Mapping
from types import MappingProxyType
from typing import cast

from .contracts import (
    CompleteRequestIdentity,
    Encoder,
    Failure,
    FeatureIdentity,
    Hash,
    Hasher,
    IdentityField,
    IdentitySource,
    LeafIdentityAggregate,
    ModelIdentity,
    PureType,
    RawIdentity,
    Serializer,
    Sorter,
    Success,
    ValidatedIdentity,
    Validator,
)


class _PipelineStages:
    """The injected dependencies needed for one complete pipeline traversal."""

    def __init__(
        self,
        *,
        validator: Validator,
        sorter: Sorter,
        encoder: Encoder,
        serializer: Serializer,
        hasher: Hasher,
    ) -> None:
        """Store each dependency without assigning concrete stage behavior."""
        self.validator = validator
        self.sorter = sorter
        self.encoder = encoder
        self.serializer = serializer
        self.hasher = hasher


def _run_pipeline(identity: RawIdentity, stages: _PipelineStages) -> Success[Hash] | Failure:
    """Run the locked pipeline, stopping immediately on validation failure."""
    validation = stages.validator.validate(identity)
    if isinstance(validation, Failure):
        return validation

    validated: ValidatedIdentity = validation.value
    sorted_identity = stages.sorter.sort(validated)
    encoded_identity = stages.encoder.encode(sorted_identity)
    serialized_identity = stages.serializer.serialize(encoded_identity)
    return Success(stages.hasher.hash(serialized_identity))


class _SnapshotList(tuple[PureType, ...]):
    """Preserve a source list's type boundary in an immutable private snapshot."""

    __slots__ = ()

    _canonical_identity_list = True


def _snapshot_value(value: object, active_ids: set[int]) -> object:
    """Return an immutable valid snapshot while preserving an active cyclic leaf."""
    if isinstance(value, list):
        return _snapshot_list(cast("list[object]", value), active_ids)
    if isinstance(value, tuple):
        return _snapshot_tuple(cast("tuple[object, ...]", value), active_ids)
    if isinstance(value, Mapping):
        return _snapshot_mapping(cast("Mapping[object, object]", value), active_ids)
    return value


def _snapshot_list(value: list[object], active_ids: set[int]) -> object:
    """Snapshot a source list without erasing its list-versus-tuple boundary."""
    value_id = id(value)
    if value_id in active_ids:
        return value
    active_ids.add(value_id)
    try:
        return _SnapshotList(cast("PureType", _snapshot_value(item, active_ids)) for item in value)
    finally:
        active_ids.remove(value_id)


def _snapshot_tuple(value: tuple[object, ...], active_ids: set[int]) -> object:
    """Snapshot a source tuple while retaining its immutable tuple boundary."""
    value_id = id(value)
    if value_id in active_ids:
        return value
    active_ids.add(value_id)
    try:
        return tuple(cast("PureType", _snapshot_value(item, active_ids)) for item in value)
    finally:
        active_ids.remove(value_id)


def _snapshot_mapping(value: Mapping[object, object], active_ids: set[int]) -> object:
    """Snapshot a mapping recursively while retaining the original invalid key values."""
    value_id = id(value)
    if value_id in active_ids:
        return value
    active_ids.add(value_id)
    try:
        snapshot: dict[object, object] = {
            key: _snapshot_value(item, active_ids) for key, item in value.items()
        }
        return MappingProxyType(snapshot)
    finally:
        active_ids.remove(value_id)


def _source_snapshot(source: IdentitySource) -> RawIdentity:
    """Recursively snapshot source values before they cross the validation boundary."""
    fields = tuple(
        IdentityField(
            name,
            cast("PureType", _snapshot_value(value, set())),
        )
        for name, value in source.identity_fields().items()
    )
    return RawIdentity(fields=fields)


class ModelIdentityBuilder:
    """Build a model leaf identity using injected identity pipeline stages."""

    def __init__(
        self,
        *,
        validator: Validator,
        sorter: Sorter,
        encoder: Encoder,
        serializer: Serializer,
        hasher: Hasher,
    ) -> None:
        """Store the complete, independently injected pipeline."""
        self._validator = validator
        self._sorter = sorter
        self._encoder = encoder
        self._serializer = serializer
        self._hasher = hasher

    def build(self, source: IdentitySource) -> Success[ModelIdentity] | Failure:
        """Build a distinct model identity from one identity source snapshot."""
        outcome = _run_pipeline(
            _source_snapshot(source),
            _PipelineStages(
                validator=self._validator,
                sorter=self._sorter,
                encoder=self._encoder,
                serializer=self._serializer,
                hasher=self._hasher,
            ),
        )
        if isinstance(outcome, Failure):
            return outcome
        return Success(ModelIdentity(value=outcome.value))


class FeatureIdentityBuilder:
    """Build feature leaf identities and compose confirmed leaf identities."""

    def __init__(
        self,
        *,
        validator: Validator,
        sorter: Sorter,
        encoder: Encoder,
        serializer: Serializer,
        hasher: Hasher,
    ) -> None:
        """Store the complete, independently injected pipeline."""
        self._validator = validator
        self._sorter = sorter
        self._encoder = encoder
        self._serializer = serializer
        self._hasher = hasher

    def build(self, source: IdentitySource) -> Success[FeatureIdentity] | Failure:
        """Build a distinct feature identity from one identity source snapshot."""
        outcome = _run_pipeline(
            _source_snapshot(source),
            _PipelineStages(
                validator=self._validator,
                sorter=self._sorter,
                encoder=self._encoder,
                serializer=self._serializer,
                hasher=self._hasher,
            ),
        )
        if isinstance(outcome, Failure):
            return outcome
        return Success(FeatureIdentity(value=outcome.value))

    def combine(
        self,
        model_identity: ModelIdentity,
        feature_identity: FeatureIdentity,
    ) -> Success[CompleteRequestIdentity] | Failure:
        """Re-run the pipeline for the fixed aggregate of both leaf identities."""
        aggregate = LeafIdentityAggregate(
            model_identity=model_identity,
            feature_identity=feature_identity,
        )
        aggregate_identity = RawIdentity(
            fields=(
                IdentityField("model_identity", aggregate.model_identity.value.value),
                IdentityField("feature_identity", aggregate.feature_identity.value.value),
            ),
        )
        outcome = _run_pipeline(
            aggregate_identity,
            _PipelineStages(
                validator=self._validator,
                sorter=self._sorter,
                encoder=self._encoder,
                serializer=self._serializer,
                hasher=self._hasher,
            ),
        )
        if isinstance(outcome, Failure):
            return outcome
        return Success(CompleteRequestIdentity(value=outcome.value))
