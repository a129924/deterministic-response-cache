# Copyright (c) 2026 deterministic-response-cache contributors

"""Public contracts for deterministic model and feature identity pipelines."""

from abc import ABC, abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Protocol

type JSONScalar = bool | int | float | str | None
type PureType = JSONScalar | list[PureType] | tuple[PureType, ...] | Mapping[str, PureType]


@dataclass(frozen=True, slots=True)
class IdentityField:
    """One named identity value supplied to the pipeline."""

    name: str
    value: PureType


@dataclass(frozen=True, slots=True)
class RawIdentity:
    """The immutable source snapshot presented to validation."""

    fields: tuple[IdentityField, ...]


@dataclass(frozen=True, slots=True)
class ValidatedIdentity:
    """An identity accepted by the injected validator."""

    fields: tuple[IdentityField, ...]


@dataclass(frozen=True, slots=True)
class SortedIdentity:
    """An identity after the injected canonical sorting stage."""

    fields: tuple[IdentityField, ...]


@dataclass(frozen=True, slots=True)
class EncodedIdentity:
    """An opaque, type-marked canonical identity representation."""

    value: str


@dataclass(frozen=True, slots=True)
class SerializedIdentity:
    """Deterministic bytes supplied to the injected hasher."""

    value: bytes


@dataclass(frozen=True, slots=True)
class Hash:
    """An opaque identity digest."""

    value: str


@dataclass(frozen=True, slots=True)
class ModelIdentity:
    """The distinct identity derived from a model source."""

    value: Hash


@dataclass(frozen=True, slots=True)
class FeatureIdentity:
    """The distinct identity derived from a feature source."""

    value: Hash


@dataclass(frozen=True, slots=True)
class LeafIdentityAggregate:
    """The fixed aggregate used to form a complete request identity."""

    model_identity: ModelIdentity
    feature_identity: FeatureIdentity


@dataclass(frozen=True, slots=True)
class CompleteRequestIdentity:
    """The identity derived by composing confirmed model and feature identities."""

    value: Hash


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    """One validation finding collected without partial success."""

    path: str
    code: str
    message: str


@dataclass(frozen=True, slots=True)
class Success[T]:
    """A successful pipeline outcome."""

    value: T


@dataclass(frozen=True, slots=True)
class Failure:
    """A validation failure containing every collected issue."""

    issues: tuple[ValidationIssue, ...]

    def __post_init__(self) -> None:
        """Reject an invalid failure value with no diagnostic information."""
        if not self.issues:
            message = "Failure.issues must contain at least one ValidationIssue."
            raise ValueError(message)


class IdentitySource(ABC):
    """Provide source fields for either model or feature identity construction."""

    @abstractmethod
    def identity_fields(self) -> Mapping[str, PureType]:
        """Return the fields that participate in this source's identity."""
        ...


class Validator(Protocol):
    """Validate a raw identity before later pipeline stages run."""

    def validate(self, identity: RawIdentity) -> Success[ValidatedIdentity] | Failure:
        """Return validated identity fields or every detected validation issue."""
        ...


class Sorter(Protocol):
    """Canonicalize the ordering of a validated identity."""

    def sort(self, identity: ValidatedIdentity) -> SortedIdentity:
        """Return the canonical sorted identity."""
        ...


class Encoder(Protocol):
    """Encode a sorted identity as an opaque canonical representation."""

    def encode(self, identity: SortedIdentity) -> EncodedIdentity:
        """Return the encoded identity."""
        ...


class Serializer(Protocol):
    """Serialize an encoded identity to deterministic bytes."""

    def serialize(self, identity: EncodedIdentity) -> SerializedIdentity:
        """Return the serialized identity."""
        ...


class Hasher(Protocol):
    """Produce an opaque digest for serialized identity bytes."""

    def hash(self, identity: SerializedIdentity) -> Hash:
        """Return the resulting identity hash."""
        ...
