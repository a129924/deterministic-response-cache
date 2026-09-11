# model-feature-identity Specification

## Acceptance Criteria

1. `IdentitySource` exposes only the abstract `identity_fields() -> Mapping[str, PureType]` source
   contract required for Model and Feature identity input.
2. The public identity package provides fully typed immutable VO, `Success`/`Failure`,
   `ValidationIssue`, and injectable Validator, Sorter, Encoder, Serializer, and Hasher Protocols.
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
  Hasher again, and returns CompleteRequestIdentity.

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
- A proposed concrete hash format, direct hash-string concatenation, runtime/cache behavior, root
  re-export, or change to `identity/.gitkeep` is scope drift and must return to Planner.
