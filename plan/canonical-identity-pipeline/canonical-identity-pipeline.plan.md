# canonical-identity-pipeline

## Goal / Outcome

Deliver the Identity BC's official v1 concrete canonical pipeline. A Python consumer can use
exported stages or a default existing Builder to turn valid model/feature sources into stable
`ModelIdentity`, `FeatureIdentity`, and `CompleteRequestIdentity` hashes without changing the
current injected-Builder contract.

## Scope

| Field | Contract |
| --- | --- |
| In-Scope | Five concrete stages, two default-builder factories, the cycle-safe private snapshot adjustment, exports, dedicated tests, a delivered Archify dataflow diagram, and publish-time README/version promotion. |
| Out-Of-Scope | Provider extraction, Response Reuse, CacheStore, runtime retention, model execution, provider adapters, persistence, telemetry, configurable/profile-versioned formats, migration, and cache-key policy. |
| ReadOnly | Existing Protocol signatures, value-object fields, keyword-only Builder injection signatures, existing direct-import tests, root package surface, `identity/.gitkeep`, and BC ownership/source-of-truth architecture files. |
| Written | `identity/canonical.py`, dedicated pipeline tests, Archify source/HTML, planning artifacts, and later role-owned evidence files. |
| Modify | `identity/builders.py` private snapshot traversal only; `identity/__init__.py` exports only; `README.md` and `pyproject.toml` only at `publish-in-progress`. |
| Deleted | No tracked file. Untracked Archify visual-check sidecars are removed before the subject commit. |
| TestCase | Valid/invalid PureType; issue aggregation; short-circuit; mapping order; type/list-tuple distinction; exact Encoder strings; Serializer bytes; `-0.0`; independent processes; factories; composition; direct imports; diagram receipts. |

The analysis layer is complete: `analysis/canonical-identity-pipeline/requirements.md` is the
business-intent guardrail and `analysis/canonical-identity-pipeline/technical-spec.md` is the
execution-facing authority. This plan maps to that technical specification without adding
alternative work.

## Locked Decisions

- This is an Identity BC-only, stable-library-affecting topic. Identity remains the unique authority
  for model and complete-request identity; no adjacent BC may reimplement the rules.
- v1 is a public type-tagged canonical JSON-like grammar. It accepts only `None`, `bool`, `int`,
  finite `float`, `str`, recursive list/tuple, and string-keyed mappings; `-0.0` normalizes to
  `0.0`; mapping/field ordering is Unicode code-point order; Unicode text is not normalized.
- Existing `Validator`, `Sorter`, `Encoder`, `Serializer`, `Hasher`, value objects, and the
  two Builder injection signatures remain unchanged. On `Failure`, later stages do not run.
- `CanonicalEncoder.encode(SortedIdentity) -> EncodedIdentity` always hands off a canonical
  JSON-like `str` in `EncodedIdentity.value`, never a Python list/dictionary/intermediate object.
  `CanonicalSerializer` alone converts that string to ASCII `bytes`.
- Required value-grammar examples are exactly `1 → '["int","1"]'`,
  `True → '["bool",true]'`, and
  `[1, "x"] → '["list",[["int","1"],["str","x"]]]'`.
- SHA-256 produces the 64-character lowercase hexadecimal `Hash`.
- Public additions are `PureTypeValidator`, `CanonicalSorter`, `CanonicalEncoder`,
  `CanonicalSerializer`, `SHA256Hasher`, `default_model_identity_builder()`, and
  `default_feature_identity_builder()`.
- The concrete profile is v1 only: no negotiation, configurable policy, migration, or silent future
  change is authorized.
- The implementation includes a static Archify dataflow diagram after Python code/test work; it
  explains only this Identity pipeline and its `Failure` short-circuit.

## Boundaries / Exclusions

- `builders.py` may change only its private snapshot traversal, solely to ensure a cyclic invalid
  runtime input reaches Validator as `Failure`; its public methods, valid-data snapshots, aggregate
  composition, and injection behavior remain unchanged.
- `contracts.py` is read-only; new classes structurally satisfy its existing Protocols rather than
  changing those Protocols or their value objects.
- Existing direct imports, fixtures, mocks, and assertions remain direct and unchanged. No
  `importlib`, `__import__`, or `sys.modules` substitution is permitted.
- Diagram files are a topic-local flow visualization, not a revision to the repository's BC
  architecture authority. CacheStore, response reuse, runtime, execution, and provider paths are
  excluded from both code and diagram.
- A path not listed below is a plan-alignment stop and returns to Planner. No correction route is
  declared for this topic.

## Status / Allowed Transitions

- **Current**: `planned`; this immutable planning candidate awaits an independent Plan-Reviewer
  receipt.
- **Execution model**: Plan-Creator candidate → independent Plan-Reviewer receipt → Implementer
  immutable subject → independent Tester evidence → evidence-only Tester commit → independent
  Reviewer evidence → evidence-only Reviewer commit → Planner Phase 4.5 alignment → existing Human
  authorization → Implementer bounded publish/push/draft PR → Human review and merge.
- **Allowed transitions**:
  - `planned` → `creator-in-progress`
  - `creator-in-progress` → `tester-in-progress`
  - `tester-in-progress` → `review-ready`
  - `review-ready` → `reviewer-in-progress`
  - `reviewer-in-progress` → `approved`
  - `reviewer-in-progress` → `needs-rework`
  - `needs-rework` → `creator-in-progress`
  - `approved` → `creator-in-progress`
  - `approved` → `publish-in-progress`
  - `publish-in-progress` → `pr-open`
  - `pr-open` → `needs-rework`
  - `pr-open` → `merged`
  - `merged` → terminal
- Tester evidence must bind the same full immutable implementation subject consumed by Reviewer.
  `publish-in-progress` can only become `pr-open`; only Human can merge from `pr-open`. Human
  also exclusively owns release, tag, post-merge, and final summary.

## Artifact Paths

| Artifact | Path | Write owner | Decision authority and role |
| --- | --- | --- | --- |
| Requirements analysis | `analysis/canonical-identity-pipeline/requirements.md` | Plan-Creator | Business-intent guardrail for this planning candidate. |
| Technical specification | `analysis/canonical-identity-pipeline/technical-spec.md` | Plan-Creator | Execution-facing source of truth for this candidate. |
| Topic plan | `plan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md` | Plan-Creator | Canonical execution contract. |
| Topic specification | `plan/canonical-identity-pipeline/canonical-identity-pipeline.spec.md` | Plan-Creator | Testable behavior and edge-case contract. |
| Step tracker | `plan/canonical-identity-pipeline/canonical-identity-pipeline.step.md` | Plan-Creator; later Implementer only for implementation markers | Progression truth; only its implementation section is the completion gate. |
| Plan-review receipt | `plan/canonical-identity-pipeline/canonical-identity-pipeline.plan-review-receipt.json` | Independent Plan-Reviewer | Committed approved candidate evidence before Planner may route implementation. |
| Concrete stages/factories | `src/deterministic_response_cache/identity/canonical.py` | Implementer | Public first-party v1 stage implementations and default existing-Builder factories. |
| Snapshot adapter | `src/deterministic_response_cache/identity/builders.py` | Implementer | Private cycle-safe invalid-input handoff; no public API/orchestration change. |
| Identity exports | `src/deterministic_response_cache/identity/__init__.py` | Implementer | Bounded re-export of the seven declared public additions. |
| Pipeline tests | `tests/test_canonical_identity_pipeline.py` | Implementer | Dedicated direct-import behavior, determinism, invalid-input, and composition coverage. |
| Archify dataflow source | `docs/architecture/canonical-identity-pipeline.dataflow.json` | Implementer | Showcase-quality Identity pipeline diagram specification. |
| Delivered dataflow viewer | `docs/architecture/canonical-identity-pipeline.html` | Implementer | Delivered static interactive diagram. |
| README API promotion | `README.md` | Implementer, only at `publish-in-progress` | Public API table row and current-stage wording after all prerequisite gates. |
| Version promotion | `pyproject.toml` | Implementer, only at `publish-in-progress` | `[project].version` minor bump from `0.0.0` to `0.1.0`. |
| Tester evidence | `plan/canonical-identity-pipeline/canonical-identity-pipeline.tester-evidence.json` | Tester | Factual same-subject validation; an independent Implementer commits it unchanged as the sole evidence-only commit. |
| Implementation review log | `plan/canonical-identity-pipeline/canonical-identity-pipeline.implementation-review-log.json` | Independent Reviewer | Same-subject review after committed passing Tester evidence; an independent Implementer commits it unchanged as the sole evidence-only commit. |

`README.md` and `pyproject.toml` are not part of the immutable implementation subject; they are
the stable-library promotion after Phase 4.5 and Human authorization. Archify visual-check contact
sheets and JSON sidecars are temporary untracked verification artifacts, not commit paths. Any
unlisted path, including a repository `VERSION` file that does not exist, requires Planner
alignment before modification.

## Stable library metadata

- **README row**: at `publish-in-progress`, add an Identity API table row identifying
  `deterministic_response_cache.identity`, its v1 concrete stages, and two default builder
  factories; revise the no-implementation baseline wording only enough to stay truthful.
- **VERSION bump**: minor, `0.0.0` → `0.1.0` in `[project].version` of `pyproject.toml`; this is
  the repository's version source because no `VERSION` file exists.
- **Timing**: `publish-in-progress`, only after same-subject passing Tester evidence, independent
  Reviewer approval, Planner Phase 4.5 alignment, and existing Human authorization.
- **Rationale**: the topic adds a new stable public identity API and canonical-format compatibility
  boundary.
- **Release notes**: no release-note file is created. Human decides any release publication, tag,
  and release notes after merge.

## Python implementation metadata

### Non-goals

- Do not modify existing Protocols, value-object fields, Builder signatures, or the root package API.
- Do not build provider-specific `IdentitySource` extraction, response reuse, CacheStore, runtime,
  model execution, provider integration, persistence, telemetry, or cache-key policy.
- Do not add dependencies, configurable/negotiated canonical profiles, profile migrations, or a
  separate versioned profile API.
- Do not alter existing direct-import tests or use dynamic import techniques.

### Current Context

`identity/contracts.py` defines all handoff values and five Protocols; `identity/builders.py`
provides injected model/feature orchestration and recursive valid-input snapshots;
`identity/__init__.py` exports the current public Identity API. Existing contract and Builder tests
directly import those symbols and must remain unchanged. `pyproject.toml` is the version source and
currently declares `0.0.0`.

### Requirements

1. Supply the seven declared public additions while structurally satisfying all existing Protocols.
2. Validate every discoverable invalid input and short-circuit all downstream stages on `Failure`.
3. Canonically sort fields/mappings, preserve scalar/container type distinctions and sequence order,
   normalize signed zero, encode ASCII canonical strings, and hash exact ASCII bytes with SHA-256.
4. Preserve existing Builder semantics while enabling cyclic invalid inputs to reach validation.
5. Prove deterministic outputs across fresh Python processes and complete-request composition.
6. Deliver and visually check the bounded dataflow diagram without changing architecture ownership.

### Decisions

- Async-planning status: exempt — cited exemption evidence: the declared paths implement synchronous
  in-memory traversal, encoding, hashing, static documentation, and a static diagram; no async
  boundary, resource lifecycle, concurrency, timeout, cancellation, or external I/O policy exists.
- Module/package placement: `src/deterministic_response_cache/identity/canonical.py` contains all
  concrete stages and default existing-Builder factories; the only existing source edit is the
  private snapshot helper in `identity/builders.py`.
- New public API: yes — five concrete stage classes plus
  `default_model_identity_builder() -> ModelIdentityBuilder` and
  `default_feature_identity_builder() -> FeatureIdentityBuilder`, re-exported by Identity.
- Interface changes: no — existing Protocol/value-object signatures and existing Builder
  constructors/methods remain byte-for-byte compatible in public shape.
- Breaking changes allowed: no — new API is additive; explicit injection continues to work.
- New dependencies: no — use only standard-library `hashlib`, `json`, `math`, and existing tools.
- Error-handling strategy: validator returns existing `Failure` with all discoverable
  `ValidationIssue` values; only invalid raw input yields `Failure`; no stage raises a new public
  domain exception.
- Typing strategy: Python 3.12 strict types using existing `PureType`, handoff values, and
  structural Protocol conformance; no `Any`, runtime type mutation, or public generic.

### Public Contract / API Changes

The seven public additions and exact signatures are in the technical specification. `Encoder` keeps
`encode(self, identity: SortedIdentity) -> EncodedIdentity`; `EncodedIdentity.value` remains
`str`; no list/dict handoff API is added. All existing public symbols and Builder signatures remain
compatible.

### Affected Files / Modules

**Written implementation paths:**

- `src/deterministic_response_cache/identity/canonical.py`
- `tests/test_canonical_identity_pipeline.py`
- `docs/architecture/canonical-identity-pipeline.dataflow.json`
- `docs/architecture/canonical-identity-pipeline.html`

**Modified implementation paths:**

- `src/deterministic_response_cache/identity/builders.py`
- `src/deterministic_response_cache/identity/__init__.py`

**Publish-only modified paths:**

- `README.md`
- `pyproject.toml`

**Read-only verification paths:**

- `src/deterministic_response_cache/identity/contracts.py`
- `tests/test_model_feature_identity_contracts.py`
- `tests/test_model_feature_identity_builders.py`
- `src/deterministic_response_cache/__init__.py`
- `src/deterministic_response_cache/identity/.gitkeep`
- `docs/business-capability-architecture.md`
- `docs/evolution-roadmap.md`
- `docs/architecture/business-capability/architecture-brief.md`
- `docs/architecture/business-capability/index.html`

### Test Plan

- **Happy path:** assert each stage and both default factories yield the documented model, feature,
  and complete identities from valid nested input.
- **Invalid input:** assert all discoverable unsupported values, non-string keys/field names,
  non-finite floats, and cycles produce every corresponding `ValidationIssue` and no downstream
  calls.
- **Edge case:** assert mapping order is irrelevant; list/tuple and scalar types are distinct; nested
  structures preserve order; `-0.0 == 0.0`; non-ASCII strings become deterministic ASCII escapes;
  `EncodedIdentity.value` and `SerializedIdentity.value` match v1 grammar exactly.
- **Regression:** run both existing direct-import test modules unchanged; assert factories retain
  existing Builders' pipeline/aggregate behavior and cyclic invalid input no longer recurses before
  Validator.
- **Backward compatibility:** assert existing Protocol/VO/Builder signatures and every old export
  remain unchanged, while seven additions are direct imports; subprocess Python invocations prove
  the same hash in independent processes.
- **Diagram TestCase:** require Archify source to describe every stage handoff and only the permitted
  failure branch, a showcase `validate`/successful `deliver`/visual-check receipt, and truthful
  manual contact-sheet review before cleanup.

### Risks

- Canonical bytes are public compatibility data; a grammar or float-format mistake would make later
  cache-key interoperability unsafe.
- A private snapshot-cycle change could regress existing immutable snapshots if valid containers leak.
- The viewer has a generated source JSON; post-delivery edits or committed visual-check sidecars would
  violate Archify handoff rules.

### Rollback Plan

Before merge, revert the immutable subject containing `canonical.py`, `builders.py`,
`__init__.py`, its dedicated test, and the two diagram artifacts together; delete only untracked
visual-check sidecars. If promotion is committed but not merged, separately revert `README.md` and
`pyproject.toml` to restore the former public description and `0.0.0`.

## Implementation Steps

1. Modify `src/deterministic_response_cache/identity/builders.py` only in the private recursive
   source-snapshot helper so valid data remains immutable and a repeated active container reference
   reaches Validator as invalid input; preserve every public Builder method and stage order.
2. Create `src/deterministic_response_cache/identity/canonical.py` with `PureTypeValidator`,
   `CanonicalSorter`, `CanonicalEncoder`, `CanonicalSerializer`, `SHA256Hasher`, and the two
   default existing-Builder factories, using the exact v1 grammar and validation behavior from the
   technical specification.
3. Modify `src/deterministic_response_cache/identity/__init__.py` to re-export only the seven
   declared public additions while retaining every existing export.
4. Create `tests/test_canonical_identity_pipeline.py` using direct imports to test exact stage
   handoffs, valid/invalid behavior, short-circuit, ordering/type boundaries, signed zero,
   subprocess determinism, default factories, composition, and existing API compatibility.
5. Use the Archify skill to create `docs/architecture/canonical-identity-pipeline.dataflow.json`,
   validate it at showcase quality, deliver
   `docs/architecture/canonical-identity-pipeline.html`, run desktop visual check, inspect its
   contact sheet, and remove untracked sidecars before the immutable subject commit.

## Validation / Acceptance Checks

- `uv run pytest tests/test_canonical_identity_pipeline.py tests/test_model_feature_identity_contracts.py tests/test_model_feature_identity_builders.py`
  passes without modifying the two existing test files.
- `uv run ruff format --check .`, `uv run ruff check .`, `uv run pyright`, `uv run tach check`,
  `uv run pytest`, and `uv run pre-commit run --all-files` pass.
- The concrete test proves exact JSON strings `["int","1"]`, `["bool",true]`, and
  `["list",[["int","1"],["str","x"]]]`, plus exact `EncodedIdentity.value` /
  `SerializedIdentity.value` handoffs. It never asserts or implies list/dict Encoder output.
- A clean-process subprocess test proves a fixed valid source produces the same lowercase
  64-character SHA-256 hex output in at least two independent Python processes.
- The implementation-subject diff is exactly the six non-publish paths: `canonical.py`,
  `builders.py`, `__init__.py`, dedicated test, Archify JSON, and Archify HTML.
- Archify validation reports all 9 showcase checks with zero errors/warnings; delivery succeeds;
  visual-check reports containment success or truthful `skipped` only if Chrome/Chromium is
  unavailable. No sidecar remains before commit.
- Tester records actual commands and integer exit codes in declared JSON evidence. Reviewer consumes
  only committed same-subject passing evidence and verifies the exact diff, direct imports,
  canonical boundaries, and diagram scope.
- At `publish-in-progress` only, verify the README API row and `pyproject.toml` `0.1.0` change;
  bounded push/draft PR still require existing Human authorization. No auto-merge/release/tag.

## Reviewer Handoff

The independent Plan-Reviewer produces exactly this JSON object (no Markdown prose) at the declared
plan-review receipt path. Only a committed `approved` verdict permits Planner routing; this
candidate itself neither selects nor closes an active candidate.

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

Tester evidence is exactly one JSON object with `schema_version`, `topic`,
`implementation_subject_commit`, `status`, `commands`, and `recorded_by`; Reviewer evidence
is exactly one JSON object with `schema_version`, `topic`, `implementation_subject_commit`,
`tester_evidence_commit`, `verdict`, `blocking_issues`, and `recorded_by`. Both bind the same
topic and full immutable subject SHA; only Tester writes the former and only Independent Reviewer
writes the latter. An Implementer separately commits each unchanged evidence file as its own sole
evidence-only commit.

## Post-merge / release actions

No automatic release, tag, post-merge, or final summary action is authorized. After the draft PR
opens, Human alone performs review, merge, and any decision to publish `0.1.0` or create release
notes/tags.

## Open Questions / Unresolved Items

None. The absent repository `VERSION` file was resolved by the discovered `[project].version`
source in `pyproject.toml`; the exact minor bump and timing are locked above.
