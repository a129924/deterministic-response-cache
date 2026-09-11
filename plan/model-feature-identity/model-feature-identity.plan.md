# model-feature-identity

## Goal / Outcome

建立 Identity BC 的 Python contract layer：Model 與 Feature source 經可注入的 canonical
pipeline 建立各自 leaf identity，並由 `FeatureIdentityBuilder.combine()` 重新 canonicalize、hash
成獨立的 `CompleteRequestIdentity`。完成後，不同 downstream BC 可只消費已確認的 identity，
而不自行建立或重解 identity 規則。

## Scope

- **In-Scope**:
  - `PureType`、`IdentitySource` ABC、immutable pipeline／identity VO、Outcome 和 validation issue
    contracts。
  - 可注入的 `Validator`、`Sorter`、`Encoder`、`Serializer`、`Hasher` Protocol。
  - `ModelIdentityBuilder`、`FeatureIdentityBuilder`、Validator failure short-circuit，以及 leaf
    aggregate 的完整第二次 pipeline traversal。
  - Identity package explicit re-exports、contract-level tests，與供 PR reviewer 閱讀的 Mermaid
    pipeline diagram。

- **Out-Of-Scope**:
  - concrete validation、sorting、encoding、serialization 或 hash algorithm，以及其 exception
    policy。
  - CacheStore、Response Reuse、Loaded Runtime Cache、Model Execution、Provider Adapter、cache
    persistence、runtime lifecycle、provider I/O、async behavior 或 legacy compatibility。
  - root package public surface、README、version、project configuration、既有 direct-import tests，
    以及由 `package-topology-skeleton-replay` 擁有的 `identity/.gitkeep`。

## Locked Decisions

- Analysis priority is strict: `analysis/model-feature-identity/technical-spec.md` is the
  execution-facing source of truth; `requirements.md` is its business-intent guardrail. This plan
  maps to both artifacts without introducing alternate work.
- `IdentitySource.identity_fields() -> Mapping[str, PureType]` is the only abstract source method;
  Model and Feature sources use the same ABC.
- Every stage handoff is a named immutable VO. The pipeline order is Validator → Sorter → Encoder →
  Serializer → Hasher → Hash. The exact VO fields, Protocol signatures, Builder injection, and
  aggregate mapping are fixed in the executable contract below; Encoder creates a type-tagged
  canonical representation and Serializer creates deterministic bytes without specifying either
  representation's concrete format.
- `PureType` supports JSON scalar, recursively string-keyed mappings, and ordered list／tuple.
  Validation rejects set, non-string mapping key, `NaN`, and `±Infinity`.
- `Hash.value` is opaque `str`; no digest algorithm, encoding, or length is promised.
- Validator returns `Success[T] | Failure`; `Failure` contains a non-empty immutable tuple of every
  `ValidationIssue(path, code, message)`. A failure stops its Builder invocation before Sorter.
- Model, Feature, and Complete Request identity are distinct immutable VOs. `combine()` uses a fixed
  named aggregate and the full pipeline, never hash-string concatenation.
- This is a non-stable-library topic: no README row, VERSION bump, release note, or release action.
  The top-level `deterministic_response_cache` public surface remains unchanged.

```mermaid
flowchart TB
  MS[Model IdentitySource] --> MB[ModelIdentityBuilder]
  FS[Feature IdentitySource] --> FB[FeatureIdentityBuilder]
  MB --> MV[Validator] -->|ok| MP[Sorter → Encoder → Serializer → Hasher]
  MV -->|Failure: short-circuit| F[Failure]
  MP --> MI[ModelIdentity]
  FB --> FV[Validator] -->|ok| FP[Sorter → Encoder → Serializer → Hasher]
  FV -->|Failure: short-circuit| F
  FP --> FI[FeatureIdentity]
  MI --> C[FeatureIdentityBuilder.combine()]
  FI --> C
  C --> CV[Validator] -->|ok| CP[Sorter → Encoder → Serializer → Hasher]
  CV -->|Failure: short-circuit| F
  CP --> CRI[CompleteRequestIdentity]
```

此圖僅輔助 PR review；本文與 `technical-spec.md` 的文字 contract 是行為 authority。

## Boundaries / Exclusions

- Identity BC is the sole authority for model and complete request identity. Response Reuse may only
  consume confirmed identities; CacheStore remains an internal component of that later BC.
- `identity/.gitkeep` is a ReadOnly topology marker owned by the active
  `package-topology-skeleton-replay` topic. This topic adds sibling modules only and neither modifies
  nor deletes that marker.
- Planning artifacts are authored only by Plan-Creator. Plan-Reviewer, Tester, and Independent
  Reviewer each produce only their own declared evidence; Implementer alone performs approved,
  bounded source work and may never merge. Any unlisted path or contract drift returns to Planner.
- No correction route is declared. Frozen governance provenance is nonrouting and cannot supply this
  topic's candidate, approval, subject, or evidence.
- The committed R1 and R2 receipts at
  `plan/model-feature-identity/model-feature-identity.plan-review-receipt.json` and
  `plan/model-feature-identity/model-feature-identity.plan-review-receipt-r2.json` are immutable
  committed `needs-rework` provenance only. Their paths and blobs must remain unchanged; neither is
  routing authority and neither can select a candidate, grant planning approval, or authorize a
  phase transition. The sole normal-plan retry receipt path is
  `plan/model-feature-identity/model-feature-identity.plan-review-receipt-r3.json`; only a future
  committed R3 receipt with `verdict: "approved"` can provide planning approval.

## Status / Allowed Transitions

- **Historical immutable state**: `R2_NEEDS_REWORK_COMMITTED`.
- **Current**: `R3_PLAN_REVIEW_PENDING`.
- **Execution model**: planning candidate commit → independent Plan-Reviewer receipt → immutable
  implementation subject → independent Tester evidence → independent Reviewer evidence → Planner
  Phase 4.5 alignment → bounded publish → draft PR → Human review and merge. This topic stops before
  release.
- **Allowed transitions**:
  - `R2_NEEDS_REWORK_COMMITTED` → `R3_PLANNING_CANDIDATE_COMMITTED` →
    `R3_PLAN_REVIEW_PENDING` → `R3_APPROVED_RECEIPT_COMMITTED` |
    `R3_NEEDS_REWORK_RECEIPT_COMMITTED`
  - `R3_APPROVED_RECEIPT_COMMITTED` → `implementation-in-progress`
  - `implementation-in-progress` → `tester-in-progress`
  - `tester-in-progress` → `tester-evidence-committed`
  - `tester-evidence-committed` → `reviewer-in-progress`
  - `reviewer-in-progress` → `reviewer-evidence-committed` or `needs-rework`
  - `reviewer-evidence-committed` → `approved`
  - `R3_NEEDS_REWORK_RECEIPT_COMMITTED` is immutable nonrouting provenance. It cannot authorize
    implementation; Planner must first declare a new receipt path before any further planning retry.
  - `needs-rework` → `implementation-in-progress` only with a new immutable subject and a complete
    new Tester/Reviewer evidence chain
  - `approved` → `publish-in-progress`
  - `publish-in-progress` → `pr-open`
  - `pr-open` → `needs-rework` or `merged` by Human only
  - `merged` → terminal

R1 and R2 are immutable committed `needs-rework` provenance and have no routing effect. Only the
future committed R3 normal-plan receipt at the declared R3 path, with `verdict: "approved"`, permits
Planner to route implementation. A committed R3 `needs-rework` receipt remains preserved and requires
Planner to declare a new receipt path before another planning retry. Tester evidence and independent
review must bind the same full implementation subject; only then may Planner Phase 4.5 align the
topic. Publish requires that alignment and existing human authorization. No transition authorizes
automatic merge, release, tag, post-merge, or final summary.

## Artifact Paths

| Artifact | Path | Write owner | Decision authority / role |
| --- | --- | --- | --- |
| Requirements | `analysis/model-feature-identity/requirements.md` | Plan-Creator | Business-intent guardrail |
| Technical specification | `analysis/model-feature-identity/technical-spec.md` | Plan-Creator | Execution-facing planning source |
| Topic plan | `plan/model-feature-identity/model-feature-identity.plan.md` | Plan-Creator | Repo-visible execution contract |
| Topic specification | `plan/model-feature-identity/model-feature-identity.spec.md` | Plan-Creator | Behavioral contract |
| Step tracker | `plan/model-feature-identity/model-feature-identity.step.md` | Plan-Creator | Progression truth |
| Plan-review receipt R1 | `plan/model-feature-identity/model-feature-identity.plan-review-receipt.json` | Independent Plan-Reviewer | Immutable committed `needs-rework` provenance; nonrouting, path/blob unchanged |
| Plan-review receipt R2 | `plan/model-feature-identity/model-feature-identity.plan-review-receipt-r2.json` | Independent Plan-Reviewer | Immutable committed `needs-rework` provenance; nonrouting, path/blob unchanged |
| Plan-review receipt R3 | `plan/model-feature-identity/model-feature-identity.plan-review-receipt-r3.json` | Independent Plan-Reviewer | Sole retry receipt; only a future committed `approved` R3 is planning approval; an Implementer commits it unchanged |
| Contracts module | `src/deterministic_response_cache/identity/contracts.py` | Implementer | Identity types, ABC, Outcome, and stage Protocol contracts |
| Builders module | `src/deterministic_response_cache/identity/builders.py` | Implementer | Bounded pipeline orchestration |
| Identity package exports | `src/deterministic_response_cache/identity/__init__.py` | Implementer | Explicit identity public surface only |
| Contract tests | `tests/test_model_feature_identity_contracts.py` | Implementer | ABC, VO, Outcome, and Protocol contract verification |
| Builder tests | `tests/test_model_feature_identity_builders.py` | Implementer | Pipeline order, failure, and composition verification |
| Tester evidence | `plan/model-feature-identity/model-feature-identity.tester-evidence.json` | Tester | Factual same-subject validation; an independent Implementer commits it unchanged as the sole evidence-only commit |
| Implementation review log | `plan/model-feature-identity/model-feature-identity.implementation-review-log.json` | Independent Reviewer | Same-subject review after committed passing Tester evidence; an independent Implementer commits it unchanged as the sole evidence-only commit |

`README.md`, project version metadata, `pyproject.toml`, root
`src/deterministic_response_cache/__init__.py`, existing tests, and
`src/deterministic_response_cache/identity/.gitkeep` are explicitly read-only. No artifact is
deleted. Any path outside this table is a plan-alignment stop and must return to Planner.

### Evidence schemas

- R1 is the already committed receipt at its declared path. It has fixed-schema `needs-rework`
  provenance only and must not be changed, replaced, or used as routing authority.
- R2 is the already committed receipt at its declared path. It has fixed-schema `needs-rework`
  provenance only and must not be changed, replaced, or used as routing authority.
- R3 is the only retry receipt and is exactly one JSON object with only `verdict`,
  `blocking_issues`, and `copilot_feedback_triage`, using the fixed reviewer-handoff schema below.
  Only its future committed `approved` verdict has planning-approval effect. A committed
  `needs-rework` R3 receipt is preserved as nonrouting provenance; Planner must declare a new receipt
  path before another planning retry.
- Tester evidence is one JSON object with exactly `schema_version`, `topic`,
  `implementation_subject_commit`, `status`, `commands`, and `recorded_by`. `schema_version` is
  integer `1`; `topic` is `model-feature-identity`; `implementation_subject_commit` is the full
  immutable subject SHA; `status` is `passing|failing`; `commands` is a non-empty array of objects
  with only non-empty string `command` and integer `exit_code`; `recorded_by` is `Tester`. Passing
  requires every exit code to be `0`; failing requires at least one non-zero exit code.
- The Independent Reviewer log is one JSON object with exactly `schema_version`, `topic`,
  `implementation_subject_commit`, `tester_evidence_commit`, `verdict`, `blocking_issues`, and
  `recorded_by`. Both commit values are full SHA values and bind the same subject; the Tester
  evidence commit is the sole committed passing-evidence commit. `verdict` is
  `approved|needs-rework`; `blocking_issues` is a string array, empty only for `approved`; and
  `recorded_by` is `Independent Reviewer`.

## Python implementation metadata

### Non-Goal

- Do not provide a default canonical serializer, concrete Validator/Sorter/Encoder/Serializer/Hasher,
  or a specific hash algorithm.
- Do not create, read, write, or decide any response/model cache or runtime state.
- Do not modify the top-level public package surface, architecture documents, README, version,
  dependencies, configuration, or existing direct-import test.
- Do not modify or delete `src/deterministic_response_cache/identity/.gitkeep`.

### Current Context

Python 3.12 strict typing, pytest, ruff, pyright, tach, and uv validation are configured in
`pyproject.toml`. The root package has an intentionally empty public surface. The Identity BC exists
only as the topology marker `identity/.gitkeep`; architecture documents reserve Identity as the first
implementation capability and its sole identity authority.

### Requirements

1. Provide fully typed, immutable contracts that make every pipeline handoff explicit.
2. Make both source builders consume only `IdentitySource.identity_fields()` and invoke their injected
   stages in the locked order.
3. Return every Validator issue in a non-empty immutable Failure, and ensure that failure prevents all
   downstream stages for that invocation.
4. Make `ModelIdentity`, `FeatureIdentity`, and `CompleteRequestIdentity` distinct value-object
   types; composition must use a fixed aggregate and a new full pipeline traversal.
5. Preserve direct imports and the topology marker; do not introduce dynamic loading with `importlib`,
   `__import__`, or `sys.modules` substitution.

### Decisions

- Async-planning status: exempt — cited exemption evidence: this topic introduces synchronous,
  in-memory value objects, Protocols, and Builder orchestration only; it introduces no async
  boundary, external I/O, resource lifecycle, concurrency, timeout, or cancellation behavior.
- Module/package placement: new sibling modules are
  `src/deterministic_response_cache/identity/contracts.py`, `builders.py`, and `__init__.py`; the
  pre-existing `identity/.gitkeep` remains untouched.
- New public API: yes — the `deterministic_response_cache.identity` package exports
  `IdentitySource`, `PureType`, immutable stage/identity VO, `Success`, `Failure`,
  `ValidationIssue`, the five stage Protocols, `ModelIdentityBuilder`, and
  `FeatureIdentityBuilder`; the root package exports nothing new.
- Interface changes: no existing interface changes; this introduces only the new identity package
  surface.
- Breaking changes allowed: no; the baseline has no existing identity API and the root package import
  surface remains intact.
- New dependencies: no; standard-library typing and ABC facilities only.
- Error-handling strategy: Validator represents invalid identity input as `Failure` containing all
  `ValidationIssue` values; Builder returns that Failure unchanged and does not call later stages.
  Concrete non-validation stage failure policy is deferred.
- Typing strategy: Python 3.12 strict typing; use `Protocol`, `TypeAlias`, generic `Success[T]`,
  explicit unions, and immutable dataclass-style VO; do not use `Any`.

### Public Contract / API Changes

- `class IdentitySource(ABC)`: `identity_fields(self) -> Mapping[str, PureType]` is its only
  abstract method.
- `JSONScalar = None | bool | int | float | str`; `PureType = JSONScalar | list[PureType] |
  tuple[PureType, ...] | Mapping[str, PureType]`.
- All of these are `@dataclass(frozen=True, slots=True)` with no additional public fields:
  `IdentityField(name: str, value: PureType)`,
  `RawIdentity(fields: tuple[IdentityField, ...])`,
  `ValidatedIdentity(fields: tuple[IdentityField, ...])`,
  `SortedIdentity(fields: tuple[IdentityField, ...])`,
  `EncodedIdentity(value: str)`, `SerializedIdentity(value: bytes)`, `Hash(value: str)`,
  `ModelIdentity(value: Hash)`, `FeatureIdentity(value: Hash)`,
  `LeafIdentityAggregate(model_identity: ModelIdentity, feature_identity: FeatureIdentity)`,
  `CompleteRequestIdentity(value: Hash)`,
  `ValidationIssue(path: str, code: str, message: str)`, `Success[T](value: T)`, and
  `Failure(issues: tuple[ValidationIssue, ...])`. `Failure.issues` is non-empty.
- `Validator.validate(self, identity: RawIdentity) -> Success[ValidatedIdentity] | Failure`;
  `Sorter.sort(self, identity: ValidatedIdentity) -> SortedIdentity`;
  `Encoder.encode(self, identity: SortedIdentity) -> EncodedIdentity`;
  `Serializer.serialize(self, identity: EncodedIdentity) -> SerializedIdentity`; and
  `Hasher.hash(self, identity: SerializedIdentity) -> Hash`. These five Protocols have no other
  public callable.
- Both Builder constructors are exactly
  `__init__(self, *, validator: Validator, sorter: Sorter, encoder: Encoder, serializer: Serializer,
  hasher: Hasher) -> None`; both receive independent injected stage instances only through those
  parameters.
- `ModelIdentityBuilder.build(self, source: IdentitySource) -> Success[ModelIdentity] | Failure`
  and `FeatureIdentityBuilder.build(self, source: IdentitySource) -> Success[FeatureIdentity] |
  Failure`. Each snapshots `source.identity_fields().items()` as
  `tuple(IdentityField(name, value) for name, value in ...)` before invoking Validator.
- `FeatureIdentityBuilder.combine(self, model_identity: ModelIdentity, feature_identity:
  FeatureIdentity) -> Success[CompleteRequestIdentity] | Failure`. It creates
  `LeafIdentityAggregate(model_identity=model_identity, feature_identity=feature_identity)`, then
  creates a new `RawIdentity` containing exactly the two fields named `model_identity` and
  `feature_identity`, whose values are the corresponding aggregate `Hash.value`; it executes the
  same full pipeline and wraps the resulting Hash only as `CompleteRequestIdentity`.
- Backward compatibility: no existing API changes; no root-package re-export.

### Affected Files / Modules

#### ReadOnly

- `pyproject.toml`
- `README.md`
- `src/deterministic_response_cache/__init__.py`
- `src/deterministic_response_cache/identity/.gitkeep`
- `tests/test_package_import.py`
- `docs/architecture/business-capability/architecture-brief.md`
- `docs/business-capability-architecture.md`

#### Written

- `src/deterministic_response_cache/identity/contracts.py`
- `src/deterministic_response_cache/identity/builders.py`
- `src/deterministic_response_cache/identity/__init__.py`
- `tests/test_model_feature_identity_contracts.py`
- `tests/test_model_feature_identity_builders.py`

#### Deleted

- None.

#### Modify

- None.

### TestCase

- **Happy path:** injected fake stages with the exact Protocol parameters record the locked order;
  source mapping is captured as the named immutable `IdentityField` tuple; leaf builds yield distinct
  ModelIdentity and FeatureIdentity values.
- **Invalid input:** a fake Validator returns multiple `ValidationIssue` values; each builder returns
  the same Failure and no downstream stage is called.
- **Edge case:** nested string-keyed mappings and ordered list／tuple travel through immutable named
  handoff VO; failure issues are non-empty and immutable.
- **Regression:** `combine()` consumes both leaf identity types, creates the fixed
  `LeafIdentityAggregate(model_identity, feature_identity)`, passes a RawIdentity whose exact field
  names are `model_identity` and `feature_identity` to a second full pipeline, and never concatenates
  hash strings; direct root import keeps passing.
- **Backward compatibility:** the root package public surface is unchanged, existing package import
  test passes, and `identity/.gitkeep` remains unchanged.

### Risks

- Defining a concrete serialized representation or digest behavior in a contract VO would prematurely
  lock a later algorithm topic.
- Collapsing leaf and complete identity types, or allowing hash-string concatenation, would weaken the
  Identity BC boundary and invite accidental cache-key ambiguity.
- Modifying the active topology marker would create a cross-topic declared-path conflict.

### Rollback Plan

Revert only `contracts.py`, `builders.py`, `identity/__init__.py`, and the two declared identity test
files from this topic's implementation subject. Leave `identity/.gitkeep`, root-package files,
architecture files, and other topic artifacts unchanged.

## Implementation Steps

1. Add `src/deterministic_response_cache/identity/contracts.py` with the exact `PureType`, frozen
   VO field table, `Success`/`Failure`/`ValidationIssue`, `IdentitySource`, and five Protocol
   signatures declared above; retain `identity/.gitkeep` unchanged.
2. Add `src/deterministic_response_cache/identity/builders.py` with injected-stage
   `ModelIdentityBuilder.build()` and `FeatureIdentityBuilder.build()` orchestration, returning
   Validator Failure unchanged and stopping before Sorter.
3. Add `FeatureIdentityBuilder.combine()` in
   `src/deterministic_response_cache/identity/builders.py`; construct the fixed named leaf aggregate,
   re-run Validator → Sorter → Encoder → Serializer → Hasher, and return
   `CompleteRequestIdentity` without hash-string concatenation.
4. Add `src/deterministic_response_cache/identity/__init__.py` with only the declared identity
   exports; do not add a root-package re-export or alter existing package files.
5. Add `tests/test_model_feature_identity_contracts.py` for the ABC requirement, public contracts,
   VO immutability, outcome issue invariants, and type-level separation of identity values.
6. Add `tests/test_model_feature_identity_builders.py` with injected fake stages for fixed call order,
   failure short-circuit, separate leaf results, and the combine second-pass aggregate/hash behavior.

## Validation / Acceptance Checks

- Verify the implementation diff contains only the five `Written` source/test paths; it must not
  modify or delete `identity/.gitkeep` or any ReadOnly path.
- Confirm each Builder's successful path uses Validator → Sorter → Encoder → Serializer → Hasher;
  each Validator Failure returns all recorded issues and has no downstream calls.
- Confirm `combine()` accepts one ModelIdentity and one FeatureIdentity, executes a fresh full pipeline,
  and yields only CompleteRequestIdentity.
- Run `uv lock --check`, `uv run ruff format --check .`, `uv run ruff check .`, `uv run pyright`,
  `uv run tach check`, `uv run pytest`, and `uv run pre-commit run --all-files`.
- Tester records every executed command and actual exit code in the declared evidence. Independent
  Reviewer verifies the same immutable subject, committed passing Tester evidence, exact scope,
  contract conformance, and preserved direct imports before producing its evidence.

## Reviewer Handoff

The following is the R3 normal-plan fixed-schema template, not a receipt. The independent
Plan-Reviewer must provide exactly this JSON shape with no trailing prose at the declared R3 path.
Only an independently produced and committed R3 `approved` verdict has planning-approval effect;
this plan does not select, declare, or deny an active candidate.

```json
{
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "copilot_feedback_triage": {
    "ADDRESS": [],
    "DISCUSS": [],
    "SKIP": []
  }
}
```

## Post-merge / release actions

No release, tag, version bump, README update, post-merge action, or final summary is authorized by
this topic. After its draft PR opens, Human performs review and may merge; Human owns every subsequent
action.

## Open Questions / Unresolved Items

None. R1 and R2 remain immutable committed `needs-rework` provenance and nonrouting. Planning
authority can arise only from the independently produced, committed approved R3 receipt; this plan
and its step tracker neither select, declare, nor close a candidate.
