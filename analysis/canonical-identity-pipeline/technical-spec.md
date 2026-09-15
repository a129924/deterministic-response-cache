# canonical-identity-pipeline — Technical Specification

## Execution-facing scope

This is an Identity BC-only, non-async Python capability. It implements the five existing stage
Protocols without changing their signatures, handoff value objects, or either existing Builder's
keyword-only injection contract. No other BC may derive or reinterpret identity.

### Current correction authority

`canonical-identity-pipeline/archify-visual-overflow` (CAVO1) 已完成，並保留為不可重用的
historical evidence；它不再是 active route，也不授權重新修改 Archify artifacts。

Human 的 explicit correction 要求目前只啟用
`canonical-identity-pipeline/concrete-stage-override` (CSO1)。本 technical specification、
parent plan/specification/step tracker 與 paired CSO1 correction plan/step 是 CSO1 的 current
truth；CSO1 只能修改 `canonical.py` 與 dedicated test，不能改變 pipeline 語意、公開 API
shape、Builder injection、diagram、README、version 或 BC scope。

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

- Valid leaves are exactly `None`, `bool`, `int`, finite `float`, and `str`; valid containers are
  recursive `list`, `tuple`, and `Mapping` with only `str` keys.
- `bool` is distinct from `int`; `NaN`, positive/negative infinity, `set`, an unsupported runtime
  value, a non-string field or mapping key, and an object-reference cycle are invalid.
- `PureTypeValidator` traverses every reachable child it can safely inspect, collects all
  discoverable `ValidationIssue` values, and returns one `Failure` when any issue exists. Its
  issue codes are `non-string-field-name`, `non-string-mapping-key`, `non-finite-float`,
  `cyclic-reference`, and `unsupported-type`.
- Validation paths use a root `$`, JSON-quoted field/key segments (for example `$["model"]`),
  and zero-based list/tuple indexes. Issue order follows deterministic pre-order traversal; valid
  string mapping keys use Unicode code-point order, while invalid mapping keys retain input order
  because they cannot participate in canonical sorting.
- The private snapshot traversal in `builders.py` remains recursive and immutable for valid values.
  For an active object-reference cycle only, it preserves the original repeated reference at that
  leaf so `PureTypeValidator` reports `cyclic-reference` rather than raising recursion before
  Validator. Since validation fails, no mutable invalid leaf reaches a later stage. No public Builder
  behavior or signature changes.
- `CanonicalSorter` sorts top-level `IdentityField` values by `name` and every valid mapping by
  Unicode code-point `str` key. It retains list/tuple order and their distinction.

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
