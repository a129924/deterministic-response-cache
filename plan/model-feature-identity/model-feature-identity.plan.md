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
- All R1–R5, S1/S2, T1/S2 Tester, V1/S2 Reviewer; PRC1 candidate
  `ccc5a8cba8259d990d7c929a534de1f927bbcbfa` with receipt `3cabeb5`; PRCR1 candidate
  `b55af90425e60a8bf358bfc6c15eae3f3e4834fd` with receipt
  `c10cd66420f0955deffc6690063a21615a32d6b6`; PRCR1C1 candidate
  `654bc0d4a342db44b2cd3bf98dcae423160b297e` with receipt
  `5688fd31e82e8f71f287f80785487ed66b85f50a` are immutable historical nonrouting provenance. Their
  paths and blobs remain unchanged; none is PRF1P1 or PRF2P1 routing authority. The committed S2 Reviewer
  evidence is the prior publish gate only and does not authorize comment fixing or thread resolution.
- The complete failed PRF1 chain—PRF1P1 candidate `eda6934d90b88c965dfc8d3776a5169d7a6a67fc`, approved
  prerequisite receipt `2eb875c017838c4c8852f12b1d0a5755215ba86f`, subject
  `32100576337b2b71dcf21fdd076f5f6aebf7d5f9`, Tester evidence
  `1b135c977e511b38e681d96cd541590984140851`, and Reviewer `needs-rework` receipt
  `08f5ec591204442c00a7a0246b92f2072f286c7c`—is immutable historical nonrouting provenance. It is
  neither amended nor retried and cannot authorize repair, publication, classification, reply, or resolution.
- This one-time, Human-authorized PRF2P1 prerequisite correction lifts only the recorded PRF1 terminal
  boundary and resumes the existing four-thread route with a replacement, two-file PRF2 repair. It may not
  alter `.gitkeep`, public package topology, any other test, architecture file, prior evidence, or
  response-related path. No unlisted PR thread, review comment, source path, or evidence path is in
  scope.
- Plan-Creator writes only this plan and this step tracker for PRF2P1. Plan-Reviewer, Tester,
  Independent Reviewer, and Implementer may each write only their own declared subsequent artifact;
  Implementer alone performs the bounded source/test repair and commits. After approved PRF2
  Tester/Reviewer evidence and Planner Phase 4.5 alignment, Implementer first pushes the existing
  PR #5 lineage through the committed PRF2 Reviewer-evidence revision. Only after PR #5 actually
  equals that revision may Independent Reviewer classify the four threads. Implementer then commits
  and pushes the classification record before posting each record's exact reply body and resolving
  its matching thread. No role may merge or approve on behalf of Human.

## Status / Allowed Transitions

- **Historical immutable state**: all R1–R5/S1/S2/T1/V1 evidence records and the original PR #5
  publish lineage are committed provenance only.
- **Current after this candidate is committed**: `PRF2P1_PLAN_REVIEW_PENDING`. Planner derives the
  current state from the committed PRF2P1 candidate, its receipt, same-subject repair evidence, and the
  PR rather than any static R5 state claim.
- **Execution model**: committed PRF2P1 planning candidate → independent Plan-Reviewer prerequisite
  receipt → one replacement PRF2 source/test repair subject → independent Tester evidence → independent Reviewer
  evidence → Planner Phase 4.5 alignment → Implementer push of the existing PR #5 through the
  Reviewer-evidence revision → independent four-thread classification record → Implementer commits
  and pushes that record → either terminal `human-check` or bounded Implementer reply/resolve → Human
  review. This topic stops before release.
- **Allowed transitions**:
  - `PRF2P1_CANDIDATE_COMMITTED` → `PRF2P1_PLAN_REVIEW_PENDING` →
    `PRF2P1_APPROVED_RECEIPT_COMMITTED` | `PRF2P1_NEEDS_REWORK_RECEIPT_COMMITTED`.
  - Only a committed `approved` PRF2P1 prerequisite receipt resumes the one replacement PRF2 subject.
    PRF2 changes exactly `src/deterministic_response_cache/identity/builders.py` and
    `tests/test_model_feature_identity_builders.py`.
  - `PRF2_SUBJECT_COMMITTED` → `PRF2_TESTER_IN_PROGRESS` →
    `PRF2_TESTER_EVIDENCE_COMMITTED` → `PRF2_REVIEWER_IN_PROGRESS` →
    `PRF2_REVIEW_EVIDENCE_COMMITTED` | `PRF2_NEEDS_REWORK_COMMITTED`.
  - Only committed passing same-PRF2 Tester evidence and committed `approved` Reviewer evidence permit
    Planner Phase 4.5 alignment. That alignment permits Implementer to push the existing PR #5 lineage
    through the committed PRF2 Reviewer-evidence revision, and no classification may begin until the
    actual PR #5 head equals that exact revision. Only then may the independent four-thread resolution
    record be written. The record may contain both permitted per-thread classifications.
  - If any record entry is `not-addressable`, the route is terminal `human-check`; no GitHub action is
    authorized. Only a committed record whose four entries are all `addressed-and-resolvable`, after
    Implementer has pushed its sole record-evidence commit to the existing PR #5, permits Implementer
    to post each entry's exact `reply_body` to its matching thread and then resolve that same thread.
    `pr-open` remains under Human review; only Human may merge.
  - The failed PRF1 subject/Test/Reviewer lineage ending at `08f5ec591204442c00a7a0246b92f2072f286c7c`
    is frozen nonrouting provenance. Its terminal boundary is lifted exactly once for this PRF2P1 candidate;
    no other PRF1 retry or route is authorized. Any PRF2P1 plan-review failure, Tester failure, Reviewer
    `needs-rework`, non-addressable or changed
    thread, additional unresolved thread, PR/head mismatch, dirty worktree, GitHub failure, or unlisted
    path is terminal `human-check`. PRC2, PRCR2, R6, retries, workflow rewrites, and scope expansion are forbidden.

## Artifact Paths

| Artifact | Path | Write owner | Decision authority / role |
| --- | --- | --- | --- |
| Requirements | `analysis/model-feature-identity/requirements.md` | Plan-Creator | Business-intent guardrail |
| Technical specification | `analysis/model-feature-identity/technical-spec.md` | Plan-Creator | Execution-facing planning source |
| Topic plan | `plan/model-feature-identity/model-feature-identity.plan.md` | Plan-Creator | Repo-visible execution contract |
| Topic specification | `plan/model-feature-identity/model-feature-identity.spec.md` | Plan-Creator | Behavioral contract |
| Step tracker | `plan/model-feature-identity/model-feature-identity.step.md` | Plan-Creator | Progression truth |
| PRC1 plan-review receipt | `plan/model-feature-identity/model-feature-identity.pr-comment-plan-review-receipt.json` | Independent Plan-Reviewer | Immutable committed PRC1 `needs-rework` provenance; nonrouting, path/blob unchanged |
| PRCR1 recovery plan-review receipt | `plan/model-feature-identity/model-feature-identity.pr-comment-recovery-plan-review-receipt.json` | Independent Plan-Reviewer | Immutable committed PRCR1 `needs-rework` provenance; nonrouting, path/blob unchanged |
| PRCR1C1 correction plan-review receipt | `plan/model-feature-identity/model-feature-identity.pr-comment-recovery-reference-plan-review-receipt.json` | Independent Plan-Reviewer | Immutable committed PRCR1C1 `needs-rework` provenance; nonrouting, path/blob unchanged |
| PRF1P1 prerequisite plan-review receipt | `plan/model-feature-identity/model-feature-identity.pr-comment-prf1-prerequisite-plan-review-receipt.json` | Independent Plan-Reviewer | Immutable committed PRF1P1 approval provenance; nonrouting after the failed PRF1 subject/test/review route |
| PRF2P1 prerequisite plan-review receipt | `plan/model-feature-identity/model-feature-identity.pr-comment-prf2-prerequisite-plan-review-receipt.json` | Independent Plan-Reviewer | Sole PRF2P1 planning approval; binds the full committed PRF2P1 candidate SHA and, only when approved, permits the one replacement PRF2 route |
| Plan-review receipt R1 | `plan/model-feature-identity/model-feature-identity.plan-review-receipt.json` | Independent Plan-Reviewer | Immutable committed `needs-rework` provenance; nonrouting, path/blob unchanged |
| Plan-review receipt R2 | `plan/model-feature-identity/model-feature-identity.plan-review-receipt-r2.json` | Independent Plan-Reviewer | Immutable committed `needs-rework` provenance; nonrouting, path/blob unchanged |
| Plan-review receipt R3 | `plan/model-feature-identity/model-feature-identity.plan-review-receipt-r3.json` | Independent Plan-Reviewer | Immutable committed `approved` provenance; nonrouting for PRCR1 |
| Plan-review receipt R4 | `plan/model-feature-identity/model-feature-identity.plan-review-receipt-r4.json` | Independent Plan-Reviewer | Immutable committed `needs-rework` provenance; nonrouting, path/blob unchanged |
| Plan-review receipt R5 | `plan/model-feature-identity/model-feature-identity.plan-review-receipt-r5.json` | Independent Plan-Reviewer | Immutable committed `approved` provenance; nonrouting for PRCR1 |
| Contracts module | `src/deterministic_response_cache/identity/contracts.py` | Implementer | Identity types, ABC, Outcome, and stage Protocol contracts |
| Builders module | `src/deterministic_response_cache/identity/builders.py` | Implementer | Bounded pipeline orchestration |
| Identity package exports | `src/deterministic_response_cache/identity/__init__.py` | Implementer | Explicit identity public surface only |
| Contract tests | `tests/test_model_feature_identity_contracts.py` | Implementer | ABC, VO, Outcome, and Protocol contract verification |
| Builder tests | `tests/test_model_feature_identity_builders.py` | Implementer | Pipeline order, failure, and composition verification |
| Tester evidence T1 | `plan/model-feature-identity/model-feature-identity.tester-evidence.json` | Tester | Immutable committed passing S1 provenance; path/blob unchanged and not S2 evidence |
| Implementation review log V1 | `plan/model-feature-identity/model-feature-identity.implementation-review-log.json` | Independent Reviewer | Immutable committed S1 `needs-rework` provenance; path/blob unchanged and not S2 evidence |
| Tester evidence S2 | `plan/model-feature-identity/model-feature-identity.tester-evidence-s2.json` | Tester | Factual same-S2-subject validation; an independent Implementer commits it unchanged as the sole S2 Tester-evidence commit |
| Implementation review log S2 | `plan/model-feature-identity/model-feature-identity.implementation-review-log-s2.json` | Independent Reviewer | Same-S2-subject review after committed passing S2 Tester evidence; an independent Implementer commits it unchanged as the sole S2 Reviewer-evidence commit |
| PRF1 Tester evidence | `plan/model-feature-identity/model-feature-identity.pr-comment-tester-evidence.json` | Tester | Immutable committed failed-PRF1 provenance; nonrouting and path/blob unchanged |
| PRF1 implementation review log | `plan/model-feature-identity/model-feature-identity.pr-comment-implementation-review-log.json` | Independent Reviewer | Immutable committed failed-PRF1 provenance; nonrouting and path/blob unchanged |
| PRF2 Tester evidence | `plan/model-feature-identity/model-feature-identity.pr-comment-prf2-tester-evidence.json` | Tester | Factual same-PRF2 validation; Implementer commits unchanged as sole evidence-only commit |
| PRF2 implementation review log | `plan/model-feature-identity/model-feature-identity.pr-comment-prf2-implementation-review-log.json` | Independent Reviewer | Same-PRF2 independent review after committed passing Tester evidence; Implementer commits unchanged as sole evidence-only commit |
| PR #5 thread-resolution record | `plan/model-feature-identity/model-feature-identity.pr-comment-thread-resolution.json` | Independent Reviewer | Four-thread per-entry classification only after Phase 4.5 has pushed PR #5 to the approved PRF2 Reviewer-evidence revision; Implementer commits and pushes it unchanged as sole evidence-only commit before the all-addressed bounded reply/resolve action |

`README.md`, project version metadata, `pyproject.toml`, root
`src/deterministic_response_cache/__init__.py`, existing tests, and
`src/deterministic_response_cache/identity/.gitkeep` are explicitly read-only. No artifact is
deleted. Any path outside this table is a plan-alignment stop and must return to Planner.

### Evidence schemas

- Every R1–R5/S1/S2/T1/V1 record, PRC1 candidate `ccc5a8cba8259d990d7c929a534de1f927bbcbfa` with
  receipt `3cabeb5`, PRCR1 candidate `b55af90425e60a8bf358bfc6c15eae3f3e4834fd` with receipt
  `c10cd66420f0955deffc6690063a21615a32d6b6`, and PRCR1C1 candidate
  `654bc0d4a342db44b2cd3bf98dcae423160b297e` with receipt
  `5688fd31e82e8f71f287f80785487ed66b85f50a`, and the complete failed PRF1 chain—PRF1P1 candidate
  `eda6934d90b88c965dfc8d3776a5169d7a6a67fc`, approved prerequisite receipt
  `2eb875c017838c4c8852f12b1d0a5755215ba86f`, subject `32100576337b2b71dcf21fdd076f5f6aebf7d5f9`,
  Tester evidence `1b135c977e511b38e681d96cd541590984140851`, and Reviewer `needs-rework` receipt
  `08f5ec591204442c00a7a0246b92f2072f286c7c` are immutable historical provenance only. They cannot
  be changed, replaced, retried, or used as PRF2P1 routing authority.
- PRF2P1 prerequisite receipt is written only at
  `plan/model-feature-identity/model-feature-identity.pr-comment-prf2-prerequisite-plan-review-receipt.json`
  and has exactly `schema_version`, `topic`, `planning_candidate_commit`, `verdict`, `blocking_issues`,
  and `recorded_by`. It binds the full 40-hex PRF2P1 planning candidate SHA, uses
  `approved|needs-rework`, has empty blockers only for `approved`, and is written by
  `Independent Plan-Reviewer`. No other PRF2P1 receipt path is authorized.
- PRF2 Tester evidence has exactly `schema_version`, `topic`, `implementation_subject_commit`,
  `status`, `commands`, and `recorded_by`; it binds the full PRF2 SHA, records actual commands and
  integer exit codes, uses `passing|failing`, and is written by `Tester`.
- PRF2 Reviewer evidence has exactly `schema_version`, `topic`, `implementation_subject_commit`,
  `tester_evidence_commit`, `verdict`, `blocking_issues`, and `recorded_by`; both full SHAs bind the
  same PRF2 lineage, `approved` requires empty blockers, and `recorded_by` is `Independent Reviewer`.
- The thread-resolution record has exactly `schema_version`, `topic`, `pull_request_number`,
  `reviewed_pull_request_head_commit`, `implementation_review_log_commit`, `threads`, and
  `recorded_by`. It binds PR `5`, the exact committed PRF2 Reviewer-evidence commit that is the
  actual current PR #5 head at classification, and exactly four entries. The top-level record permits
  both per-thread classifications. Each entry must use exactly one of these shapes:
  - `addressed-and-resolvable`: exactly `id`, `url`, `classification`, `reply_body`, and
    `verification_basis`; both added fields are non-empty strings and `blocking_issue` is absent.
  - `not-addressable`: exactly `id`, `url`, `classification`, and `blocking_issue`; `blocking_issue`
    is a non-empty string and `reply_body` and `verification_basis` are absent.
  The entries must be the four IDs and URLs listed in `PR #5 comment-fix route`, and `recorded_by` is
  `Independent Reviewer`.

### PR #5 comment-fix route

The route has exactly these threads and no inferred equivalent:

| Thread ID | URL | Required verification responsibility |
| --- | --- | --- |
| `PRRT_kwDOUJTij86hljUO` | `https://github.com/a129924/deterministic-response-cache/pull/5#discussion_r3992115152` | Verify separated evidence ancestry. |
| `PRRT_kwDOUJTij86hlk-Z` | `https://github.com/a129924/deterministic-response-cache/pull/5#discussion_r3992125326` | Verify recursive source snapshot canonical immutability through the declared PRF2 builder test. |
| `PRRT_kwDOUJTij86hlk--` | `https://github.com/a129924/deterministic-response-cache/pull/5#discussion_r3992125394` | Verify stale static state is replaced by this Planner-derived PRCR1 recovery route. |
| `PRRT_kwDOUJTij86hlk_c` | `https://github.com/a129924/deterministic-response-cache/pull/5#discussion_r3992125442` | Verify Failure tuple and element validation through the declared contract test. |

The classification record is written only after Planner Phase 4.5 verifies the committed PRF2 subject,
its passing Tester evidence, its approved Reviewer evidence, a clean worktree, and that Implementer
has pushed the existing PR #5 so its actual head equals the committed Reviewer-evidence revision. At
classification time both `reviewed_pull_request_head_commit` and
`implementation_review_log_commit` must name that committed Reviewer-evidence revision. Its subsequent
sole evidence-only commit must contain no source/test change and Implementer must push it to PR #5
before any reply or resolution. Any `not-addressable` entry is terminal `human-check` and authorizes
no GitHub action. Before the all-addressed reply/resolve action, Implementer verifies that the PR head
is that resolution-record commit and that its source tree remains the reviewed repair tree; Implementer
posts each entry's exact `reply_body` to its matching ID and then resolves that same ID.

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
  `Failure(issues: tuple[ValidationIssue, ...])`. `Failure.issues` is a non-empty tuple containing
  only `ValidationIssue` values.
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
  Failure`. Each recursively snapshots nested `PureType` values before invoking Validator: scalar
  values are retained, list/tuple values become recursively snapshotted tuples, and mappings become
  recursively snapshotted `MappingProxyType` values wrapping fresh dictionaries. No nested mutable
  source container may be shared with the resulting `RawIdentity`.
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

## PRF2P1 comment-fix repair correction

- **Frozen failed provenance:** PRC1 candidate `ccc5a8cba8259d990d7c929a534de1f927bbcbfa` with receipt
  `3cabeb5`, PRCR1 candidate `b55af90425e60a8bf358bfc6c15eae3f3e4834fd` with receipt
  `c10cd66420f0955deffc6690063a21615a32d6b6`, PRCR1C1 candidate
  `654bc0d4a342db44b2cd3bf98dcae423160b297e` with receipt
  `5688fd31e82e8f71f287f80785487ed66b85f50a`, and the complete failed PRF1 chain—PRF1P1 candidate
  `eda6934d90b88c965dfc8d3776a5169d7a6a67fc`, approved prerequisite receipt
  `2eb875c017838c4c8852f12b1d0a5755215ba86f`, subject `32100576337b2b71dcf21fdd076f5f6aebf7d5f9`,
  Tester evidence `1b135c977e511b38e681d96cd541590984140851`, and Reviewer `needs-rework` receipt
  `08f5ec591204442c00a7a0246b92f2072f286c7c` remain immutable and nonrouting. They are not amended,
  replaced, retried, or consumed as approval.
- **PRF2P1 planning candidate allowlist:** only this plan and this step tracker. It lifts only the
  recorded PRF1 terminal boundary, declares one replacement PRF2 repair, and writes no receipt, Tester,
  Reviewer, resolution, source, or test artifact.
- **PRF2P1 approval:** Independent Plan-Reviewer writes only
  `model-feature-identity.pr-comment-prf2-prerequisite-plan-review-receipt.json`; an independent
  Implementer commits an unchanged `approved` receipt as a sole evidence-only commit. Only that approval
  permits PRF2. A `needs-rework` verdict is terminal `human-check`.
- **PRF2 repair-subject allowlist:** only
  `src/deterministic_response_cache/identity/builders.py` and
  `tests/test_model_feature_identity_builders.py`. It only replaces the nested snapshot handoff with a
  canonical immutable representation: recursively snapshot lists and tuples as tuples, mappings as fresh
  dictionaries wrapped by `MappingProxyType`, and add a direct `RawIdentity` handoff immutability test.
  It preserves public contracts, `contracts.py`, exports, `.gitkeep`, all other tests, planning, and
  evidence.
- **PRF2 evidence and publish order:** Independent Plan-Reviewer first writes the PRF2P1 prerequisite
  receipt; an independent Implementer commits it unchanged as a sole evidence-only commit. After that
  approval, Implementer creates the one PRF2 subject. Tester writes only
  `pr-comment-prf2-tester-evidence.json`; a distinct Implementer commits it unchanged as sole evidence.
  Independent Reviewer then writes only `pr-comment-prf2-implementation-review-log.json`; a distinct
  Implementer commits it unchanged as sole evidence. After Planner Phase 4.5 alignment, Implementer
  pushes the existing PR #5 lineage through that committed PRF2 Reviewer-evidence revision. Only once
  the actual PR #5 head equals that revision may Independent Reviewer write the existing
  `pr-comment-thread-resolution.json`; a distinct Implementer commits and pushes it unchanged as sole
  evidence. No evidence file may share a commit with a subject, planning artifact, or another evidence
  file.
- **Bounded PR action:** only after the resolution-record commit is pushed to PR #5 may Implementer
  reply with the record's exact `reply_body` and resolve its exact four thread IDs, and only when all
  four record entries are `addressed-and-resolvable`. Any `not-addressable` entry is terminal
  `human-check` and authorizes no GitHub action. This does not authorize a new PR, merge, release,
  tag, or post-merge work.

## Validation / Acceptance Checks

- For S1 provenance, verify the implementation diff contains only the five `Written` source/test
  paths; it must not modify or delete `identity/.gitkeep` or any ReadOnly path.
- For PRF2P1, verify the candidate diff contains only this plan and this tracker; for PRF2, verify the
  subject diff contains only `builders.py` and `test_model_feature_identity_builders.py`; for every evidence-only commit, verify the
  diff contains exactly its declared evidence path.
- Confirm each Builder's successful path uses Validator → Sorter → Encoder → Serializer → Hasher;
  each Validator Failure returns all recorded issues and has no downstream calls.
- Confirm the replacement snapshot recursively represents lists and tuples as tuples and mappings as
  `MappingProxyType`, and that a nested source mutation after `build()` cannot alter the Validator-recorded
  `RawIdentity` handoff.
- Confirm `combine()` accepts one ModelIdentity and one FeatureIdentity, executes a fresh full pipeline,
  and yields only CompleteRequestIdentity.
- Run `uv lock --check`, `uv run ruff format --check .`, `uv run ruff check .`, `uv run pyright`,
  `uv run tach check`, `uv run pytest`, and `uv run pre-commit run --all-files`.
- Tester records every executed command and actual exit code in the declared PRF2 evidence. Independent
  Reviewer verifies the same immutable subject, committed passing Tester evidence, exact scope,
  contract conformance, preserved direct imports, PR #5 ancestry, and all four exact thread IDs/URLs
  before producing its implementation-review evidence. Planner then confirms Phase 4.5 before the
  Implementer push that makes PR #5 equal the Reviewer-evidence revision. Only afterwards may the
  Independent Reviewer produce the resolution record. Verify every resolution entry has exactly its
  permitted shape and only perform bounded GitHub actions when all four entries are addressed and the
  resolution record has been committed and pushed.

## Reviewer Handoff

The following is the PRF2P1 prerequisite plan-review fixed-schema template, not a receipt. Independent
Plan-Reviewer writes it only at the declared PRF2P1 prerequisite receipt path. Only an independently
produced and committed `approved` receipt that binds the actual full PRF2P1 candidate SHA permits PRF2; this plan
does not select, declare, or deny a candidate.

```json
{
  "schema_version": 1,
  "topic": "model-feature-identity",
  "planning_candidate_commit": "<full-40-hex-PRF2P1-SHA>",
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "recorded_by": "Independent Plan-Reviewer"
}
```

## Post-merge / release actions

No release, tag, version bump, README update, post-merge action, or final summary is authorized by
this topic. After its draft PR opens, Human performs review and may merge; Human owns every subsequent
action.

## Open Questions / Unresolved Items

None. R1–R5/S1/S2/T1/V1 plus PRC1 candidate `ccc5a8cba8259d990d7c929a534de1f927bbcbfa` with receipt
`3cabeb5`, PRCR1 candidate `b55af90425e60a8bf358bfc6c15eae3f3e4834fd` with receipt
`c10cd66420f0955deffc6690063a21615a32d6b6`, and PRCR1C1 candidate
`654bc0d4a342db44b2cd3bf98dcae423160b297e` with receipt
`5688fd31e82e8f71f287f80785487ed66b85f50a`, and the complete failed PRF1 chain—PRF1P1 candidate
`eda6934d90b88c965dfc8d3776a5169d7a6a67fc`, approved prerequisite receipt
`2eb875c017838c4c8852f12b1d0a5755215ba86f`, subject `32100576337b2b71dcf21fdd076f5f6aebf7d5f9`,
Tester evidence `1b135c977e511b38e681d96cd541590984140851`, and Reviewer `needs-rework` receipt
`08f5ec591204442c00a7a0246b92f2072f286c7c`, remain immutable nonrouting provenance. PRF2P1 has
exactly one SHA-bound prerequisite receipt path, one two-file replacement repair subject, two new
implementation-evidence paths, and the existing four-thread resolution path bound only to approved PRF2
Reviewer evidence; no PRF2P2, PRF3, retry, extra thread, or expanded repair is authorized.
