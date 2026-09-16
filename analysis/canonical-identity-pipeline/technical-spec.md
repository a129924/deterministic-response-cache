# canonical-identity-pipeline — Technical Specification

## Execution-facing scope

This is an Identity BC-only, non-async Python capability. It implements the five existing stage
Protocols without changing their signatures, handoff value objects, or either existing Builder's
keyword-only injection contract. No other BC may derive or reinterpret identity.

### Current correction authority

`canonical-identity-pipeline/archify-visual-overflow` (CAVO1) 已完成，並保留為不可重用的
historical evidence；它不再是 active route，也不授權重新修改 Archify artifacts。

CSO1 的 C7S independent Plan-Reviewer receipt 已在
`1123deae24fc37f6755e3eae810d453c40552f9d` committed；它和 C0–C7 均為 completed
historical provenance。C8 remains Planner-only Phase 4.5 alignment and does not by itself
authorize a code change, push, merge, or thread resolution.

Human 已授權 `canonical-identity-pipeline/pr-comment-review-and-fix` (PRCF1) 作為 draft PR #6
的獨立 correction route。它只處理已分類的 canonicalization 與 status-tracker comments；
immutable implementation subject 只能修改 `canonical.py` 與 dedicated test，不能改變
Protocol、handoff value object、Builder injection、exports、diagram、README、version、`uv.lock`
或 BC scope。`uv.lock` has been restored to `1123deae24fc37f6755e3eae810d453c40552f9d` and is
read-only for the entire route.

## Public concrete API

`src/deterministic_response_cache/identity/canonical.py` defines and
`src/deterministic_response_cache/identity/__init__.py` re-exports exactly these additions:

```text
class PureTypeValidator:
    def validate(self, identity: RawIdentity) -> Success[ValidatedIdentity] | Failure: ...

class CanonicalSorter:
    def sort(self, identity: ValidatedIdentity) -> SortedIdentity: ...

class CanonicalEncoder:
    def encode(self, identity: SortedIdentity) -> EncodedIdentity: ...

class CanonicalSerializer:
    def serialize(self, identity: EncodedIdentity) -> SerializedIdentity: ...

class SHA256Hasher:
    def hash(self, identity: SerializedIdentity) -> Hash: ...

def default_model_identity_builder() -> ModelIdentityBuilder: ...
def default_feature_identity_builder() -> FeatureIdentityBuilder: ...
```

CSO1 鎖定 concrete classes 的 nominal typing contract。使用 Python 3.12 的
`from typing import override`，並將每個 class 明確具名繼承其唯一對應的既有 Protocol：

```text
class PureTypeValidator(Validator):
    @override
    def validate(self, identity: RawIdentity) -> Success[ValidatedIdentity] | Failure: ...

class CanonicalSorter(Sorter):
    @override
    def sort(self, identity: ValidatedIdentity) -> SortedIdentity: ...

class CanonicalEncoder(Encoder):
    @override
    def encode(self, identity: SortedIdentity) -> EncodedIdentity: ...

class CanonicalSerializer(Serializer):
    @override
    def serialize(self, identity: EncodedIdentity) -> SerializedIdentity: ...

class SHA256Hasher(Hasher):
    @override
    def hash(self, identity: SerializedIdentity) -> Hash: ...
```

Only the five respective public Protocol methods carry `@override`. Private helpers, factory
functions, and all other callables do not carry it. This is additive nominal declaration only:
`contracts.py`, every Protocol signature, every value object, and Builder injection remain
byte-for-byte unchanged.

Each default factory creates a new existing Builder wired to one fresh instance of every concrete
stage. The factories do not add a pipeline value object, retain mutable state, or alter callers that
keep explicit injection.

## v1 validation and sorting

- Valid leaves are exactly `None`, `bool`, `int`, finite `float`, and exact built-in `str`; valid containers are
  recursive `list`, `tuple`, and `Mapping` with only `str` keys.
- `bool` is distinct from `int`; `NaN`, positive/negative infinity, `set`, an unsupported runtime
  value, a non-string field or mapping key, and an object-reference cycle are invalid.
- `PureTypeValidator` traverses every reachable child it can safely inspect, collects all
  discoverable `ValidationIssue` values, and returns one `Failure` when any issue exists. Its
  issue codes are `non-string-field-name`, `non-string-mapping-key`, `non-finite-float`,
  `cyclic-reference`, `surrogate-code-point`, and `unsupported-type`.
- Validation paths use a root `$`, JSON-quoted field/key segments (for example `$["model"]`),
  and zero-based list/tuple indexes. Issue order follows deterministic pre-order traversal; valid
  string mapping keys use Unicode code-point order, while invalid mapping keys retain input order
  because they cannot participate in canonical sorting.
- The private snapshot traversal in `builders.py` remains recursive and immutable for valid values.
  For an active object-reference cycle only, it preserves the original repeated reference at that
  leaf so `PureTypeValidator` reports `cyclic-reference` rather than raising recursion before
  Validator. Since validation fails, no mutable invalid leaf reaches a later stage. No public Builder
  behavior or signature changes.
- A top-level field name and a mapping key are canonical strings only when `type(value) is str`.
  A `str` subclass is invalid as `non-string-field-name` or `non-string-mapping-key`; it must never
  reach a user-defined comparator. This exact-type rule applies before either field or key sorting.
- Every exact built-in string in a canonical position—top-level field name, mapping key, or scalar
  string value—must contain no Unicode surrogate code point (`U+D800` through `U+DFFF`). Each
  occurrence adds `surrogate-code-point` at its deterministic canonical path, while validation
  continues to collect other safely reachable issues. Non-BMP Unicode scalar values remain valid.
- `CanonicalSorter` sorts top-level `IdentityField` values by exact built-in `str` name and every
  valid mapping by exact built-in `str` key in Unicode code-point order. It retains list/tuple order
  and their distinction.

## v1 encoding, serialization, and hashing

`CanonicalEncoder` may construct Python lists internally, but it must return only an
`EncodedIdentity` whose `value` is a compact canonical JSON-like ASCII `str`. It uses
`json.dumps(..., ensure_ascii=True, separators=(",", ":"))` for the completed grammar object; it
does not return that object itself.

The grammar is fixed as follows, where `V` is recursively encoded:

| Value | Grammar object before JSON serialization |
| --- | --- |
| `None` | `["null", null]` |
| `bool` | `["bool", true]` or `["bool", false]` |
| `int` | `["int", "<base-10 integer>"]` |
| `float` | `["float", "<float.hex()>"]` after replacing `-0.0` with `0.0` |
| `str` | `["str", "<string>"]` |
| `list` | `["list", [V, ...]]` |
| `tuple` | `["tuple", [V, ...]]` |
| mapping | `["map", [[["str", "<key>"], V], ...]]` with sorted keys |
| `SortedIdentity.fields` | `["identity", [[["str", "<field name>"], V], ...]]` with sorted field names |

The required value-grammar examples are exact and the containing public stage result is always an
`EncodedIdentity` string:

```text
1          # EncodedIdentity(value='["int","1"]') at the scalar grammar boundary
True       # EncodedIdentity(value='["bool",true]') at the scalar grammar boundary
[1, "x"]   # EncodedIdentity(value='["list",[["int","1"],["str","x"]]]') at that boundary
```

For an actual stage call, the sorted fields are wrapped by the fixed `identity` root tag. Tests
must assert both this root representation and the three exact recursive values. No documentation or
test may describe `Encoder.encode()` as returning a list, dictionary, or intermediate structure.

`CanonicalSerializer` encodes `EncodedIdentity.value` as strict ASCII bytes with no newline,
whitespace insertion, or reparsing. Each canonical Encoder output therefore has a one-to-one
`SerializedIdentity.value`. `SHA256Hasher` calculates `hashlib.sha256(bytes).hexdigest()` and
returns its lowercase 64-character result in `Hash`.

### PRCF1 canonicalization repair requirements

- The Builder's private `_SnapshotList` may be imported by `canonical.py` solely to recognize the
  immutable list snapshot. `_is_snapshot_list(value)` must use exact type identity
  (`type(value) is _SnapshotList`), not a public/name-based/truthy attribute lookup and not
  subclass acceptance. A tuple subclass that exposes `_canonical_identity_list = True` is still a
  tuple for direct-stage canonicalization and must encode with the `"tuple"` tag.
- Valid non-BMP text must pass through Encoder as ASCII JSON escape text, Serializer as exactly the
  same ASCII bytes, and SHA-256 as a literal fixed digest. For the model field
  `{"value": "\U0001f600"}`, the root `EncodedIdentity.value` is exactly
  `["identity",[[["str","value"],["str","\ud83d\ude00"]]]]`,
  `SerializedIdentity.value` is its ASCII byte sequence, and `Hash.value` is exactly
  `02c41d0e0019f532fef8e908145a6fdde13c471e23d3a64c2d70a8ef6b3372a6`.
- A Python string containing either surrogate half, including a literal paired-surrogate spelling,
  is invalid rather than an alternative valid encoding of the non-BMP scalar. This prevents the
  `ensure_ascii=True` representation from collapsing distinct Python inputs.

## Data flow and failure boundary

For `ModelIdentityBuilder.build()` and `FeatureIdentityBuilder.build()`, the unmodified public
orchestration remains:

```text
IdentitySource snapshot -> Validator -> Sorter -> Encoder(str) -> Serializer(bytes) -> SHA-256
```

`Failure` returns unchanged from Validator and prevents all four later stages. `combine()` remains
the existing `FeatureIdentityBuilder.combine()` flow: it constructs its fixed
`LeafIdentityAggregate`, presents only `model_identity` and `feature_identity` hash strings as
the second `RawIdentity`, and runs the same pipeline. It must not concatenate hash strings.

## Exact implementation paths

| Classification | Path | Intended change |
| --- | --- | --- |
| Write | `src/deterministic_response_cache/identity/canonical.py` | New concrete stages and two default-builder factories. |
| Modify | `src/deterministic_response_cache/identity/builders.py` | Private cycle-safe snapshot traversal only; public orchestration stays identical. |
| Modify | `src/deterministic_response_cache/identity/__init__.py` | Re-export only the seven declared public additions. |
| Write | `tests/test_canonical_identity_pipeline.py` | Dedicated direct-import, stage, factory, deterministic, invalid-input, and composition tests. |
| Write | `docs/architecture/canonical-identity-pipeline.dataflow.json` | Archify `dataflow` source describing only this pipeline. |
| Write | `docs/architecture/canonical-identity-pipeline.html` | Delivered static interactive Archify diagram. |
| Modify at publish only | `README.md` | Add canonical Identity API row and revise the no-implementation baseline claim. |
| Modify at publish only | `pyproject.toml` | Set `[project].version` from `0.0.0` to `0.1.0`. |

All other repository paths, including `contracts.py`, both existing test modules, the root package
initializer, `identity/.gitkeep`, and architecture source-of-truth documents, are read-only.

### CSO1 exact correction subject

The prior six-path original implementation subject and CAVO1 evidence are historical provenance;
they are not CSO1 inputs and must not be reused as CSO1 Tester or Reviewer evidence. After the
committed approved CSO1 correction Plan-Reviewer log, the new immutable CSO1 implementation subject
contains exactly these two paths:

| Classification | Path | Intended change |
| --- | --- | --- |
| Modify | `src/deterministic_response_cache/identity/canonical.py` | Import `typing.override`; make each of the five concrete stages explicitly inherit its matching Protocol; mark only its matching public stage method with `@override`. |
| Modify | `tests/test_canonical_identity_pipeline.py` | Retain all direct-import/pipeline regressions and add assertions for the named base and `__override__` marker on each public stage method, plus absence of the marker on each private helper. |

`src/deterministic_response_cache/identity/contracts.py`, `builders.py`, `identity/__init__.py`, both
Archify artifacts, `README.md`, `pyproject.toml`, `uv.lock`, all existing regression modules, and
every evidence/provenance path are read-only for the CSO1 subject. An unlisted path is plan drift
and returns to Planner.

### PRCF1 exact correction subject

After a committed approved PRCF1 Plan-Reviewer receipt, the only immutable PRCF1 implementation
subject paths are:

| Classification | Path | Intended change |
| --- | --- | --- |
| Modify | `src/deterministic_response_cache/identity/canonical.py` | Enforce exact built-in string validity, reject all surrogate code points at canonical-string positions, and use exact `_SnapshotList` type identity. |
| Modify | `tests/test_canonical_identity_pipeline.py` | Preserve direct imports and add strict-string, surrogate, non-BMP exact handoff/hash, and nonspoofable snapshot-list regressions. |

The tests must prove: a comparison-overriding `str` subclass is rejected at both top-level and
mapping-key boundaries without invoking its comparator; surrogate field/key/scalar positions yield
all deterministic `surrogate-code-point` findings and short-circuit downstream stages; a non-BMP
scalar yields the exact ASCII Encoder string, matching Serializer bytes, and the fixed hash above;
and an attribute-spoofing tuple subclass remains `tuple`. `contracts.py`, `builders.py`, exports,
all non-dedicated tests, diagram files, `README.md`, `pyproject.toml`, and `uv.lock` are read-only.

## Diagram contract

After Python code and tests exist, the Implementer uses the `archify` skill to create a static
`dataflow` diagram. Before authoring, read the skill's dataflow schema, common schema, and one
dataflow example. The JSON must use `meta.quality_profile: "showcase"`, at most 12 primary nodes,
automatic routes, Traditional Chinese authored labels, and no `meta.locale` because the viewer has
no Traditional-Chinese locale; the renderer-owned UI is therefore truthfully English.

Its main rail is `IdentitySource snapshot → Validator → Sorter → Encoder (str) → Serializer
(bytes) → SHA-256 → leaf identity → combine() → CompleteRequestIdentity`; a `Failure` side branch
leaves Validator and terminates downstream work. It must not depict CacheStore, reuse, runtime,
execution, or provider behavior.

CAVO1 historical route permitted at most two focused geometry/content rounds on only
`docs/architecture/canonical-identity-pipeline.dataflow.json` and the HTML freshly delivered from
that source. Content compaction may improve fitting but may not alter any required semantics, node,
relationship, handoff, or failure boundary. Each round must showcase-validate (9/9 checks, zero
errors/warnings), deliver (exit 0), and visual-check (exit 0) 1440×900, 1600×1000, 1920×1080, and
2048×1320 with no horizontal or vertical overflow. A second round may only respond to first-round
diagnostics. If two rounds do not strictly reduce the failing-viewport count, or the second still
overflows or has a non-zero required command, stop at `human-check`. Visual-check screenshots and
JSON sidecars are temporary untracked evidence, must be inspected truthfully, and must be removed
before committing the immutable subject. The correction plan is the authority for CAVO1 evidence
schemas and role order.

## Validation commands

```bash
uv run pytest tests/test_canonical_identity_pipeline.py tests/test_model_feature_identity_contracts.py tests/test_model_feature_identity_builders.py
uv run ruff format --check .
uv run ruff check .
uv run pyright
uv run tach check
uv run pytest
uv run pre-commit run --all-files
```

The diagram command sequence and its completed CAVO1 evidence are historical only. CSO1 runs the
Python validation commands above, including the dedicated direct-import regression suite; it neither
regenerates the diagram nor writes Archify evidence.
