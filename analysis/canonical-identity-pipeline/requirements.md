# canonical-identity-pipeline — Requirements

## Mission

Identity BC needs a first-party canonical v1 pipeline so that a Python consumer can turn a
model or feature `IdentitySource` into a repeatable `ModelIdentity`, `FeatureIdentity`, and
`CompleteRequestIdentity` without supplying test-only stage doubles. Identity remains the only
authority for these identities.

## User-visible outcome

- Consumer code can use the exported concrete stages with the existing dependency-injected
  builders, or obtain the existing builders from the two exported default-builder factories.
- Equal valid inputs produce equal SHA-256 lowercase-hex hashes across independent processes;
  mapping insertion order cannot change the result.
- A validation failure contains every discoverable issue and stops before Sorter, Encoder,
  Serializer, or Hasher.
- The public Encoder handoff remains `EncodedIdentity(value: str)`; no public stage returns a
  list, dictionary, or another intermediate Python grammar object.

## Scope classification

| Field | Requirement |
| --- | --- |
| Goal | Add the official v1 canonical identity pipeline inside Identity BC. |
| In-Scope | Five concrete stages, two default-builder factories, the private snapshot adjustment needed to present cyclic invalid input to validation, public exports, dedicated tests, a later dataflow diagram, and publish-time README/version promotion. |
| Out-Of-Scope | Provider extraction, Response Reuse, CacheStore, loaded runtime cache, model execution, provider adapters, persistence, telemetry, configurable profiles, profile migration, and cache-key policy. |
| ReadOnly | Existing Protocol signatures, value-object fields, builder injection signatures, direct-import tests, root package surface, architecture BC ownership documents, and `identity/.gitkeep`. |
| Written | `identity/canonical.py`, `tests/test_canonical_identity_pipeline.py`, the two Archify diagram artifacts, and this topic's five planning artifacts/evidence files at their declared owner phases. |
| Modify | `identity/builders.py` only for private cycle-safe source snapshot traversal; `identity/__init__.py` only for exports; `README.md` and `pyproject.toml` only during `publish-in-progress`. |
| Deleted | No tracked file. Archify visual-check sidecars are untracked verification output and must be removed before the immutable implementation-subject commit. |
| TestCase | Canonical happy paths, invalid-input aggregation, downstream short-circuit, ordering/type boundaries, exact Encoder strings and Serializer bytes, cross-process hashes, builder composition, export compatibility, and diagram delivery evidence. |

## Locked human decisions

- v1 is a public type-tagged canonical JSON-like grammar and compatibility boundary.
- `EncodedIdentity.value` is a canonical JSON-like `str`; `Serializer` converts that string to
  `SerializedIdentity.value: bytes` with a fixed ASCII encoding rule.
- SHA-256 produces a 64-character lowercase hexadecimal `Hash`.
- `-0.0` and `0.0` have the same identity.
- Existing Protocols, value objects, and builder injection signatures do not change.
- Concrete stages and default builder factories are official public Identity BC API.
- At `publish-in-progress`, add the README API row and bump the repository's version source in
  `pyproject.toml` from `0.0.0` to `0.1.0`. There is no repository `VERSION` file.
- After the Python implementation is ready, use Archify to deliver the declared static dataflow
  diagram with showcase validation and a truthful desktop visual-check receipt.

## Completion signals

1. The concrete stages obey the fixed grammar and existing handoff types.
2. All valid canonical inputs are deterministic and preserve required distinctions.
3. All supported invalid inputs fail before downstream work.
4. `combine()` continues to compose only confirmed model and feature identities through the
   existing full pipeline traversal.
5. The diagram describes only Identity BC and does not introduce an adjacent BC responsibility.

## Analysis-layer status

The analysis layer was absent when the draft was discussed. This committed `requirements.md` and
its companion `technical-spec.md` complete that layer for this candidate: requirements remain the
business-intent guardrail, while the technical specification is the execution-facing source of
truth. No chat-time instruction supersedes either artifact.
