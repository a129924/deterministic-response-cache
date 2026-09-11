# model-feature-identity Specification

## Executable Contract Surface

- `JSONScalar = None | bool | int | float | str`; `PureType = JSONScalar | list[PureType] |
  tuple[PureType, ...] | Mapping[str, PureType]`. `IdentitySource` has exactly one abstract method:
  `identity_fields(self) -> Mapping[str, PureType]`.
- The following are `@dataclass(frozen=True, slots=True)` value objects with only the listed fields:
  `IdentityField(name: str, value: PureType)`;
  `RawIdentity(fields: tuple[IdentityField, ...])`;
  `ValidatedIdentity(fields: tuple[IdentityField, ...])`;
  `SortedIdentity(fields: tuple[IdentityField, ...])`;
  `EncodedIdentity(value: str)`;
  `SerializedIdentity(value: bytes)`;
  `Hash(value: str)`;
  `ModelIdentity(value: Hash)`;
  `FeatureIdentity(value: Hash)`;
  `LeafIdentityAggregate(model_identity: ModelIdentity, feature_identity: FeatureIdentity)`;
  `CompleteRequestIdentity(value: Hash)`;
  `ValidationIssue(path: str, code: str, message: str)`;
  `Success[T](value: T)`; and `Failure(issues: tuple[ValidationIssue, ...])`. `Failure.issues`
  must be non-empty.
- The only public stage calls are:

  ```python
  Validator.validate(self, identity: RawIdentity) -> Success[ValidatedIdentity] | Failure
  Sorter.sort(self, identity: ValidatedIdentity) -> SortedIdentity
  Encoder.encode(self, identity: SortedIdentity) -> EncodedIdentity
  Serializer.serialize(self, identity: EncodedIdentity) -> SerializedIdentity
  Hasher.hash(self, identity: SerializedIdentity) -> Hash
  ```

- Both `ModelIdentityBuilder` and `FeatureIdentityBuilder` have exactly
  `__init__(self, *, validator: Validator, sorter: Sorter, encoder: Encoder, serializer: Serializer,
  hasher: Hasher) -> None`. Their respective build signatures are
  `build(self, source: IdentitySource) -> Success[ModelIdentity] | Failure` and
  `build(self, source: IdentitySource) -> Success[FeatureIdentity] | Failure`.
- `FeatureIdentityBuilder.combine(self, model_identity: ModelIdentity, feature_identity:
  FeatureIdentity) -> Success[CompleteRequestIdentity] | Failure` first constructs
  `LeafIdentityAggregate(model_identity=model_identity, feature_identity=feature_identity)`. Its
  second pipeline input is a new `RawIdentity` with exactly `model_identity` and `feature_identity`
  `IdentityField.name` values, carrying the corresponding aggregate `Hash.value` strings.

## Acceptance Criteria

1. `IdentitySource` exposes only the abstract `identity_fields() -> Mapping[str, PureType]` source
   contract required for Model and Feature identity input.
2. The public identity package provides the exact immutable VO, `Success`/`Failure`,
   `ValidationIssue`, and injectable Validator, Sorter, Encoder, Serializer, and Hasher Protocol
   signatures in the Executable Contract Surface.
3. Both leaf builders execute Validator → Sorter → Encoder → Serializer → Hasher on success and
   produce their distinct leaf identity VO.
4. A Validator Failure containing one or more issues is returned unchanged and prevents every
   downstream stage for that invocation.
5. `combine()` represents ModelIdentity and FeatureIdentity in a fixed aggregate, makes a fresh full
   pipeline traversal, and produces CompleteRequestIdentity without concatenating hash strings.
6. The implementation changes only the five declared source/test paths and leaves
   `src/deterministic_response_cache/identity/.gitkeep` unchanged.

## Behavioral Scenarios

### Scenario 1: build two leaf identities

- **Given** separate Model and Feature `IdentitySource` implementations and successful injected
  pipeline stages.
- **When** their matching Builders call `build()`.
- **Then** each stage is invoked in the locked order and the results are distinct ModelIdentity and
  FeatureIdentity values.

### Scenario 2: combine confirmed leaf identities

- **Given** a ModelIdentity and FeatureIdentity from successful leaf pipelines.
- **When** `FeatureIdentityBuilder.combine()` is called.
- **Then** it creates the fixed leaf aggregate, performs Validator → Sorter → Encoder → Serializer →
  Hasher again from the two exact aggregate field names, and returns CompleteRequestIdentity.

### Scenario 3: reject invalid identity input

- **Given** a Validator that detects invalid PureType input and returns a Failure containing multiple
  ValidationIssue values.
- **When** a leaf Builder or `combine()` invokes that Validator.
- **Then** the Builder returns that exact Failure and does not call Sorter, Encoder, Serializer, or
  Hasher.

## Error / Edge Cases

- set values, non-string mapping keys, `NaN`, and `±Infinity` are invalid PureType input and must be
  representable as collected ValidationIssue values rather than partial pipeline work.
- Nested mappings must retain the mapping sort responsibility in Sorter, while list／tuple order is
  retained as the input contract.
- Fake-stage tests must assert each exact Protocol input/output handoff, both keyword-only Builder
  constructors, the `IdentityField` source snapshot, and the exact aggregate field names before the
  second Validator invocation.
- A proposed concrete hash format, direct hash-string concatenation, runtime/cache behavior, root
  re-export, or change to `identity/.gitkeep` is scope drift and must return to Planner.
