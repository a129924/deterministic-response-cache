# canonical-identity-pipeline Specification

## Acceptance Criteria

1. The public Identity package exports the five declared concrete stages and two default-builder
   factories without changing an existing Protocol, value object, Builder, or existing export.
2. Valid `PureType` data is validated, sorted, encoded as a type-tagged compact ASCII JSON-like
   `EncodedIdentity.value: str`, serialized as identical ASCII bytes, and hashed as a
   64-character lowercase SHA-256 hex string.
3. `1`, `True`, and `[1, "x"]` use exact recursive grammar strings `["int","1"]`,
   `["bool",true]`, and `["list",[["int","1"],["str","x"]]]`; the Encoder public return is
   `EncodedIdentity`, never a list/dictionary.
4. Mapping insertion order does not affect a valid identity; list/tuple, scalar type, meaningful
   value, and non-zero float representation distinctions do affect it; `-0.0` and `0.0` are equal.
5. Every safely discoverable invalid input finding is returned as `Failure`, including unsupported
   type, non-string field/mapping key, non-finite float, and cycle; no downstream stage runs.
6. Default factories produce existing Model/Feature Builders and retain complete-request composition
   through `combine()`.
7. An Archify showcase dataflow diagram accurately depicts source snapshot, five stages, string/bytes
   boundaries, leaf identities, `combine()`, complete identity, and Validator short-circuit without
   depicting another BC. CAVO1 may change only its two diagram artifacts to repair desktop overflow;
   it preserves those semantics, nodes/order, and `Failure` boundary.

## Behavioral Scenarios

### Scenario 1: create equal leaf identities from equivalent mappings

- **Given** two `IdentitySource` values with the same nested model/feature content but different
  mapping insertion orders.
- **When** a consumer uses a default builder from the public Identity package.
- **Then** validation succeeds, canonical stages produce equal leaf hashes, and the same input run in
  a fresh Python process produces the same hash.

### Scenario 2: preserve type-tagged Encoder string handoff

- **Given** a sorted identity containing scalar and sequence values.
- **When** `CanonicalEncoder.encode()` runs.
- **Then** it returns `EncodedIdentity(value=<compact canonical JSON-like str>)`, including the
  required `int`, `bool`, and list value grammar; `CanonicalSerializer.serialize()` returns the
  exact ASCII bytes for that string.

### Scenario 3: reject invalid input before canonicalization

- **Given** an identity with a `set`, non-string mapping key, non-finite float, and cyclic
  container in independently reachable fields.
- **When** a default Model or Feature Builder runs.
- **Then** one `Failure` contains all four issue kinds and no Sorter, Encoder, Serializer, or
  Hasher call occurs.

### Scenario 4: create a complete request identity

- **Given** confirmed model and feature identities from official canonical builders.
- **When** `FeatureIdentityBuilder.combine()` runs.
- **Then** it keeps the existing fixed aggregate and full pipeline traversal and produces a stable
  `CompleteRequestIdentity` without hash-string concatenation.

### Scenario 5: repair and deliver the bounded pipeline visualization

- **Given** Python stages and direct tests are ready.
- **When** the CAVO1 Plan-Reviewer gate is committed and the Implementer uses Archify for one or,
  only when diagnostics require it, two focused geometry/content rounds.
- **Then** each round validates at showcase 9/9 with zero errors/warnings, delivers successfully,
  and visual-checks all four desktop viewports without overflow; delivered HTML is backed by a
  frozen showcase-passing JSON source, and its only failure route leaves Validator before Sorter.
- **And** if the second round remains non-contained, a required command is non-zero, or two rounds
  do not reduce the failing viewport count, the route stops as `human-check` without a third round.

## Error / Edge Cases

- `NaN`, `Infinity`, `-Infinity`, `set`, unsupported custom objects, non-string field names,
  non-string mapping keys, and active-reference cycles fail through `Failure`; no public exception
  or partial pipeline work is introduced.
- Empty strings, empty mappings, empty lists, empty tuples, nested combinations, escaped Unicode,
  very large integers, and finite float values are valid and retain fixed grammar.
- A cyclic invalid value must not raise `RecursionError` during Builder snapshotting. It must reach
  Validator and return a `cyclic-reference` issue while valid snapshots remain immutable.
- An externally constructed non-ASCII `EncodedIdentity.value` is outside canonical Encoder output;
  `CanonicalSerializer` uses strict ASCII and may raise `UnicodeEncodeError` rather than changing
  the existing Protocol to add a failure outcome.
- A proposed path outside Artifact Paths, dynamic import, or change to `contracts.py`/existing
  direct-import tests is plan drift and returns to Planner. Within CAVO1 only, failed visual
  containment is handled by its declared maximum two-round route; it becomes `human-check` after
  the second failure or two non-improving rounds.
