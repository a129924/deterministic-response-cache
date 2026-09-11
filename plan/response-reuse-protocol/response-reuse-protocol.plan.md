# response-reuse-protocol

## Goal / Outcome

- **Analysis-layer routing:** strict mode. `analysis/response-reuse-protocol/technical-spec.md` is the
  execution-facing source of truth; `analysis/response-reuse-protocol/requirements.md` is the business-intent
  guardrail. The Human override recorded in both analysis artifacts controls the obsolete Identity-completion
  gate wording.
- Deliver an independently usable, synchronous Response Reuse Protocol that accepts only opaque confirmed identity,
  exposes deterministic cache outcomes, and documents the corresponding BC flow without implementing downstream BCs.

## Scope

- **In scope**:
  - The ten implementation paths listed in `Artifact Paths`: three Response Reuse source modules, two unit-test
    modules, and five architecture surfaces.
  - `lookup` outcomes `Hit(response) | Miss | Unavailable`; `record` outcomes `Cached(response) | NotCached(response)`.
  - The architecture and interactive-flow update that removes Identity implementation completion as a gate while
    retaining Identity authority.

- **Out of scope**:
  - Identity construction, validation, hashing, serialization, comparison, imports, or any identity public API.
  - Cache backend/adapters, persistence, TTL, eviction, invalidation policy, locking, concurrency, retries,
    metrics, tracing, network I/O, and cross-process consistency.
  - Loaded Runtime Cache, Model Execution, Provider Adapter, or a downstream orchestration implementation.
  - README, versioning, release, root public exports, child package initializer, dependencies, configuration,
    deletion, migration, compatibility layer, merge, release, tag, post-merge, or final summary.

- **Read-only**:
  - `AGENTS.md`, `pyproject.toml`, `src/deterministic_response_cache/__init__.py`,
    `src/deterministic_response_cache/response_reuse/.gitkeep`, `tests/test_package_import.py`, `README.md`,
    `VERSION` (if present), `.github/copilot-instructions.md` (if present), and all paths outside this plan's
    Artifact Paths.
- **Written**: the three source and two test paths marked **Add** in Artifact Paths.
- **Modified**: only the five architecture surfaces marked **Modify** in Artifact Paths.
- **Deleted**: none; specifically preserve the Response Reuse `.gitkeep` marker.

## Locked Decisions

- Human explicitly overrides the old roadmap implementation-completion prerequisite: Response Reuse Protocol is an
  independent topic. Identity remains the sole authority, but its implementation completion is not this topic's gate.
- `confirmed_identity` and response are generic opaque values. The Protocol forwards identity unchanged to
  CacheStore and never derives or interprets it.
- `ResponseReuseProtocol[IdentityT, ResponseT]` is concrete and synchronous. Its direct module import is
  `deterministic_response_cache.response_reuse.protocol`; outcome types are likewise direct-module imports. No
  `response_reuse/__init__.py` or root re-export is added.
- CacheStore is an internal generic synchronous `typing.Protocol` with `read`/`write`. A `None` read means absent,
  invalid, or expired entry. `CacheStoreFailure` is the only operational backend failure translated by Response Reuse.
- `lookup` maps response to `Hit`, `None` to `Miss`, and `CacheStoreFailure` to `Unavailable`. It does not catch
  other exceptions.
- `record` maps a successful write to `Cached(response)` and `CacheStoreFailure` to `NotCached(response)`; both
  retain the original response object. It does not invoke execution or provider behavior.
- The topic is non-stable-library-affecting: README row, VERSION bump, release notes, and release timing are absent.
  `README.md` and version metadata are no-change paths.
- No correction route is declared. Planning, Tester, and independent implementation-review evidence use the normal
  topic evidence chain only.

## Boundaries / Exclusions

- Plan-Creator writes only the five initial planning artifacts. Plan-Reviewer writes only the normal plan-review
  receipt. Implementer performs only approved bounded planning-candidate, implementation-subject, and evidence-only
  commits; Tester writes factual evidence; Independent Reviewer writes implementation-review evidence.
- CacheStore must remain inside Response Reuse. It cannot become a top-level BC, own identity rules, execute models,
  or manage runtime. A miss is a boundary outcome, not authority to perform future downstream work.
- Documentation may depict future downstream handoff only as external/future behavior; it must not claim this topic
  implements Runtime Cache, Execution, or Provider Adapter.
- Any undeclared path, altered public export, new dependency, async behavior, identity interpretation, or doc/code
  contract drift stops work and returns to Planner.

## Status / Allowed Transitions

- **Current**: `planned`; the five initial planning artifacts are uncommitted and have no routing authority.
- **Execution model**: planning candidate → independent Plan-Reviewer receipt → immutable implementation subject →
  independent Tester evidence → independent Reviewer evidence → Planner Phase 4.5 alignment → bounded publish →
  draft PR → Human review and merge. This topic stops before release.
- **Allowed transitions**:
  - `planned` -> `planning-candidate-committed` by an Implementer committing exactly the five initial planning artifacts.
  - `planning-candidate-committed` -> `plan-review-in-progress`.
  - `plan-review-in-progress` -> `plan-review-receipt-committed` only after Independent Plan-Reviewer writes the receipt and an Implementer commits it unchanged as its own evidence-only commit.
  - `plan-review-receipt-committed` -> `implementation-in-progress` only when the committed receipt verdict is `approved` and Planner selects it.
  - `implementation-in-progress` -> `tester-in-progress` after one non-merge immutable subject changes exactly the ten declared implementation paths.
  - `tester-in-progress` -> `tester-evidence-committed` only after Tester writes factual same-subject evidence and an independent Implementer commits it unchanged as the sole evidence-only commit.
  - `tester-evidence-committed` -> `reviewer-in-progress` only with committed same-subject `passing` Tester evidence.
  - `reviewer-in-progress` -> `reviewer-evidence-committed` only after Independent Reviewer writes its evidence and an independent Implementer commits it unchanged as the sole evidence-only commit.
  - `reviewer-evidence-committed` -> `approved` only after Planner Phase 4.5 aligns the committed same-subject `approved` review evidence.
  - `implementation-in-progress` -> `needs-rework` or `reviewer-in-progress` -> `needs-rework`; rework requires a new immutable subject and a complete new Tester/Reviewer chain.
  - `approved` -> `publish-in-progress` only with existing Human authorization.
  - `publish-in-progress` -> `pr-open` by bounded push and draft PR; `pr-open` -> `needs-rework` or `merged` by Human only; `merged` -> terminal.

## Artifact Paths

| Artifact | Exact path | Write owner | Decision authority and role |
| --- | --- | --- | --- |
| Requirements analysis | `analysis/response-reuse-protocol/requirements.md` | Plan-Creator | Business-intent guardrail; planning candidate input only. |
| Technical specification | `analysis/response-reuse-protocol/technical-spec.md` | Plan-Creator | Execution-facing source of truth; Human override is recorded here. |
| Topic plan | `plan/response-reuse-protocol/response-reuse-protocol.plan.md` | Plan-Creator | Canonical execution contract and path allowlist. |
| Topic specification | `plan/response-reuse-protocol/response-reuse-protocol.spec.md` | Plan-Creator | Acceptance, behavioral, and edge-case contract. |
| Step tracker | `plan/response-reuse-protocol/response-reuse-protocol.step.md` | Plan-Creator; later Implementer only for `## Implementation Steps` markers | Progression truth; only seven implementation checkboxes form the completion gate. |
| Plan-review receipt | `plan/response-reuse-protocol/response-reuse-protocol.plan-review-receipt.json` | Independent Plan-Reviewer | Committed `approved` normal-plan receipt is the only planning approval Planner may route from. |
| Response Reuse outcomes | `src/deterministic_response_cache/response_reuse/outcomes.py` **Add** | Implementer | `Hit`, `Miss`, `Unavailable`, `Cached`, `NotCached`, and typed outcome unions. |
| Internal CacheStore port | `src/deterministic_response_cache/response_reuse/_cache_store.py` **Add** | Implementer | Internal `CacheStore` protocol and `CacheStoreFailure` boundary; no backend implementation. |
| Response Reuse protocol | `src/deterministic_response_cache/response_reuse/protocol.py` **Add** | Implementer | Concrete lookup/record orchestration within the locked BC boundary. |
| Outcome tests | `tests/test_response_reuse_outcomes.py` **Add** | Implementer | Direct-import unit proof for outcome value semantics. |
| Protocol tests | `tests/test_response_reuse_protocol.py` **Add** | Implementer | Direct-import unit proof for branch mapping and CacheStore interaction. |
| BC text architecture | `docs/business-capability-architecture.md` **Modify** | Implementer | Canonical BC boundaries, independent Response Reuse eligibility, and CacheStore ownership. |
| Evolution roadmap | `docs/evolution-roadmap.md` **Modify** | Implementer | Conceptual sequence; removes Identity-completion gate while retaining authority/boundaries. |
| Architecture brief | `docs/architecture/business-capability/architecture-brief.md` **Modify** | Implementer | Flow prose and diagram acceptance contract for all locked outcomes. |
| Interactive scene source | `docs/architecture/business-capability/scene.js` **Modify** | Implementer | Authoritative interactive scene labels, nodes, and flow edges. |
| Interactive scene mirror | `docs/architecture/business-capability/index.html` **Modify** | Implementer | Exact embedded mirror of `scene.js` response-reuse visual content. |
| Tester evidence | `plan/response-reuse-protocol/response-reuse-protocol.tester-evidence.json` | Tester | Same-subject factual validation; independent Implementer commits it unchanged as sole evidence-only commit. |
| Independent review evidence | `plan/response-reuse-protocol/response-reuse-protocol.implementation-review-log.json` | Independent Reviewer | Consumes only committed passing Tester evidence; independent Implementer commits it unchanged as sole evidence-only commit. |

`README.md`, version metadata, `.github/copilot-instructions.md`, `src/deterministic_response_cache/__init__.py`,
`src/deterministic_response_cache/response_reuse/.gitkeep`, `tests/test_package_import.py`, `pyproject.toml`,
and every unlisted path are read-only. No path may be deleted. Any required path outside this table returns to Planner.

### Review and evidence schemas

- Plan-review receipt is exactly one JSON object with only `verdict`, `blocking_issues`, and
  `copilot_feedback_triage`. `verdict` is `approved|needs-rework`; `blocking_issues` is an array of objects with
  exactly `issue`, `file`, and `fix`; `copilot_feedback_triage` has exactly `ADDRESS`, `DISCUSS`, and `SKIP` arrays.
  `ADDRESS` entries have `comment`, `location`, `why`; `DISCUSS` entries have `comment`, `optional`, `why`; `SKIP`
  entries have `comment`, `why`.
- Tester evidence is exactly one JSON object with `schema_version`, `topic`, `implementation_subject_commit`,
  `status`, `commands`, `recorded_by`. `schema_version` is integer `1`; `topic` is `response-reuse-protocol`;
  `implementation_subject_commit` is the full 40-hex immutable subject SHA; `status` is `passing|failing`;
  `commands` is a non-empty array of objects with exactly non-empty string `command` and integer `exit_code`;
  `recorded_by` is `Tester`. `passing` requires every exit code `0`; `failing` requires at least one non-zero code.
- Independent review evidence is exactly one JSON object with `schema_version`, `topic`,
  `implementation_subject_commit`, `tester_evidence_commit`, `verdict`, `blocking_issues`, `recorded_by`.
  Both commit fields are full 40-hex SHAs bound to the same subject; `tester_evidence_commit` names the committed,
  sole, passing Tester-evidence commit; `verdict` is `approved|needs-rework`; `blocking_issues` is a string array,
  empty only for `approved`; `recorded_by` is `Independent Reviewer`.

## Python implementation metadata

### Non-goals

- Will not create, validate, import, compare, serialize, hash, or reinterpret model/request identity.
- Will not implement a CacheStore backend, persistence policy, TTL/eviction/invalidation policy, concurrency model,
  retry, timeout, metrics, tracing, or external I/O.
- Will not implement Loaded Runtime Cache, Model Execution, Provider Adapter, or downstream orchestration.
- Will not create `response_reuse/__init__.py`, a root export, a new dependency, README/version change, or compatibility layer.

### Current Context

The root package has only `src/deterministic_response_cache/__init__.py`; the reserved
`src/deterministic_response_cache/response_reuse/` directory contains only `.gitkeep`. `tests/test_package_import.py`
is the existing direct-import smoke regression. The five documentation surfaces currently describe a conceptual
Identity-first sequence and contain wording that makes Identity implementation completion a Response Reuse gate;
the recorded Human override requires that wording to be corrected without weakening Identity authority.

### Requirements

1. Implement exactly the Python contract in `analysis/response-reuse-protocol/technical-spec.md` with strict typing
   under the existing Python 3.12 / pyright configuration.
2. Produce all five deterministic outcome types and no implicit failure-to-miss conversion.
3. Ensure `lookup` and `record` call their corresponding CacheStore method exactly once and preserve generic opaque
   input/payload objects.
4. Update all five documentation surfaces consistently; `scene.js` and embedded `index.html` scene data must agree.
5. Keep the immutable implementation subject to exactly the ten declared implementation paths and preserve all
   read-only paths.

### Decisions

- Async-planning status: exempt — cited exemption evidence: the locked Protocol and CacheStore port are synchronous;
  this topic introduces no async boundary, resource lifecycle, external I/O concurrency choice, timeout, cancellation,
  retry, or sync-to-async conversion.
- Module/package placement: `outcomes.py`, `_cache_store.py`, and `protocol.py` directly under the existing reserved
  `src/deterministic_response_cache/response_reuse/` directory.
- New public API: yes, direct module-path API only: `ResponseReuseProtocol`, the five outcomes, and their typed
  aliases are importable from their defining modules; `_cache_store.py` is an internal port, not a stable public
  interface. No child initializer or root-package re-export exists.
- Interface changes: no existing interface is modified. New `CacheStore` is an internal structural port with
  `read(identity) -> response | None` and `write(identity, response) -> None`.
- Breaking changes allowed: no; existing root package import behavior remains unchanged.
- New dependencies: no; use only Python standard-library `dataclasses` and `typing`.
- Error-handling strategy: CacheStore adapters raise `CacheStoreFailure` for expected operational backend failures;
  lookup maps it to `Unavailable`, record maps it to `NotCached(response)`, and all other exceptions propagate.
- Typing strategy: strict generic `TypeVar`-based annotations, `typing.Protocol` for internal store dependency,
  immutable slotted generic dataclasses, no `Any`, casts, or runtime identity inspection.

### Public Contract / API Changes

Direct-module imports add the following API without a package initializer or re-export:

```python
from deterministic_response_cache.response_reuse.outcomes import (
    Cached,
    Hit,
    LookupOutcome,
    Miss,
    NotCached,
    RecordOutcome,
    Unavailable,
)
from deterministic_response_cache.response_reuse.protocol import ResponseReuseProtocol
```

`ResponseReuseProtocol(store: CacheStore[IdentityT, ResponseT])` exposes
`lookup(confirmed_identity: IdentityT) -> LookupOutcome[ResponseT]` and
`record(confirmed_identity: IdentityT, response: ResponseT) -> RecordOutcome[ResponseT]`. `None` is reserved as
CacheStore's no-usable-entry sentinel, so responses must be non-`None` values. `_cache_store.py` and its
`CacheStore` / `CacheStoreFailure` names are implementation-internal dependencies: implementation and direct-import
tests may use them, but they receive no stable-library compatibility promise.

### Affected Files / Modules

**Written implementation paths:**

- `src/deterministic_response_cache/response_reuse/outcomes.py`
- `src/deterministic_response_cache/response_reuse/_cache_store.py`
- `src/deterministic_response_cache/response_reuse/protocol.py`
- `tests/test_response_reuse_outcomes.py`
- `tests/test_response_reuse_protocol.py`

**Modified implementation paths:**

- `docs/business-capability-architecture.md`
- `docs/evolution-roadmap.md`
- `docs/architecture/business-capability/architecture-brief.md`
- `docs/architecture/business-capability/scene.js`
- `docs/architecture/business-capability/index.html`

**Read-only verification paths:**

- `src/deterministic_response_cache/__init__.py`
- `src/deterministic_response_cache/response_reuse/.gitkeep`
- `tests/test_package_import.py`
- `pyproject.toml`

### Test Plan

- **Happy path:** `tests/test_response_reuse_protocol.py` proves a stored response becomes `Hit` and successful
  `write` becomes `Cached`, with original response identity preserved.
- **Invalid input:** no identity-shape validation is in scope; a fake CacheStore raising non-`CacheStoreFailure`
  verifies this contract/programming exception propagates rather than being classified.
- **Edge case:** parameterized absent, invalid, and expired fake-store states all return `None` and map to `Miss`;
  read failure maps to `Unavailable`; write failure maps to `NotCached` while preserving response.
- **Regression:** direct-import tests load the three new modules normally, and `uv run pytest tests/test_package_import.py`
  preserves existing root import behavior without dynamic-import substitution.
- **Backward compatibility:** verify the implementation subject changes exactly the ten declared paths; no root export,
  initializer, `.gitkeep` deletion, README/version/configuration change, or future-BC path is present.

### Risks

- Treating a backend read exception as `None` would silently conflate unavailable storage with cache miss.
- Adding a child initializer or root re-export would expand the stable public surface beyond the locked direct-module API.
- `scene.js` and `index.html` are mirrored scene definitions; editing only one would create a misleading flow diagram.

### Rollback Plan

Revert the immutable implementation subject to remove the three new Response Reuse source modules and two new tests,
then restore the five named architecture surfaces together. The preserved `.gitkeep`, root package, configuration,
README, version metadata, and existing import test need no rollback.

## Implementation Steps

1. Update `docs/business-capability-architecture.md`, `docs/evolution-roadmap.md`, and
   `docs/architecture/business-capability/architecture-brief.md` before Python code: retain Identity as sole
   authority and CacheStore as internal-only, but state that this opaque-input Response Reuse Protocol may proceed
   independently; document Hit/Miss/Unavailable and Cached/NotCached boundary flow without adding future BC behavior.
2. Update `docs/architecture/business-capability/scene.js` and the embedded scene in
   `docs/architecture/business-capability/index.html` identically: render confirmed identity lookup, Hit direct
   return, Miss future handoff/new-response record loop, Unavailable stop, and Cached/NotCached retention result;
   label downstream components as future and remove any Identity-completion gate claim.
3. Create `src/deterministic_response_cache/response_reuse/outcomes.py` with frozen slotted generic dataclasses
   `Hit`, `Miss`, `Unavailable`, `Cached`, `NotCached`, and the exact `LookupOutcome` / `RecordOutcome` union aliases.
4. Create `src/deterministic_response_cache/response_reuse/_cache_store.py` with generic synchronous
   `CacheStore[IdentityT, ResponseT]` read/write `typing.Protocol` and `CacheStoreFailure`; define `None` exclusively
   as no usable entry and make no backend implementation.
5. Create `src/deterministic_response_cache/response_reuse/protocol.py` with generic concrete
   `ResponseReuseProtocol`; implement the exact lookup/record mapping, only translating `CacheStoreFailure`, forwarding
   identity unchanged, preserving response payload, and never invoking downstream work.
6. Create `tests/test_response_reuse_outcomes.py` with direct imports and assertions for immutable outcome equality,
   distinct marker types, generic payload preservation, and lookup/record union member behavior.
7. Create `tests/test_response_reuse_protocol.py` with a typed fake CacheStore and direct imports; prove every
   acceptance scenario, one read/write call, opaque identity object forwarding, non-`CacheStoreFailure` propagation,
   and absence of execution/provider interaction.

## Validation / Acceptance Checks

- `uv run ruff check src/deterministic_response_cache/response_reuse tests/test_response_reuse_outcomes.py tests/test_response_reuse_protocol.py`
- `uv run pyright src/deterministic_response_cache/response_reuse tests/test_response_reuse_outcomes.py tests/test_response_reuse_protocol.py`
- `uv run pytest tests/test_response_reuse_outcomes.py tests/test_response_reuse_protocol.py -v`
- `uv run pytest tests/test_package_import.py -v`
- `uv run pytest -v`
- Verify `git diff --name-only <implementation-subject-parent> <implementation-subject>` is exactly the ten declared
  implementation paths, and verify `src/deterministic_response_cache/response_reuse/.gitkeep` remains tracked.
- Verify `scene.js` and `index.html` carry the same Response Reuse outcome labels/edges and none says Identity
  implementation completion is a gate.
- Verify imports are direct and no `importlib`, `__import__`, or `sys.modules` substitution appears in changed tests.

## Reviewer Handoff

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

No repository release action is authorized or required. After a Human merges the draft PR, Human alone owns
post-merge synchronization, release, tagging, and final summary; this topic declares no VERSION or README action.

## Open Questions / Unresolved Items

None. Cache backend selection, cache lifecycle policy, downstream execution integration, observability, and any
future public facade are explicitly deferred to separately planned topics.
