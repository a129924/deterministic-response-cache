# package-topology-skeleton-replay

## Goal / Outcome

Create a topology-only Business Capability skeleton under `src/deterministic_response_cache/` and align all declared architecture documentation to its fixed BC names, boundaries, and Identity-first evolution order. The result contains no executable BC implementation or new public import surface.

## Scope

- **In scope**:
  - The ten implementation paths listed in `Artifact Paths`: five architecture surfaces and five `.gitkeep` reservations.
  - Architecture alignment that explicitly states the directories are pre-created topology, not implemented or usable capabilities.
  - The fixed mapping: Identity → `identity`, Response Reuse → `response_reuse`, Loaded Runtime Cache → `loaded_runtime_cache`, Model Execution → `model_execution`, Provider Adapter → `provider_adapter`.

- **Out of scope**:
  - Any Python behavior, domain rule, runtime, provider, cache behavior, public API, dependency, or compatibility layer.
  - Child `__init__.py`, Python source, dynamic import (`importlib`, `__import__`, or `sys.modules` substitution), testing double, or `cache_store/` directory.
  - Changes to the root package, existing tests, configuration, README, release, tag, merge, or post-merge work.

## Locked Decisions

- This is a non-stable, topology-only topic. It does not affect a stable-library surface; `README.md` and version metadata remain unchanged, and there is no release action.
- The source-of-truth text mapping is `docs/business-capability-architecture.md`. `docs/evolution-roadmap.md` owns the ordered implementation sequence. The architecture brief and interactive scene are synchronized presentations, not alternate authority.
- The order is immutable for this topic: Identity → Response Reuse → Loaded Runtime Cache → Model Execution → Provider Adapter. Existing Response-Reuse-first wording is corrected.
- Identity alone owns model identity and complete request identity. Response Reuse only consumes confirmed identity. CacheStore stays an internal Response Reuse concept and does not receive a top-level directory.
- Loaded Runtime Cache, Model Execution, and Provider Adapter remain separate future BCs; a reserved folder does not authorize their implementation.
- Every reserved directory contains only `.gitkeep`; none contains `__init__.py` or Python code. Existing `src/deterministic_response_cache/__init__.py` remains the sole package initializer and direct-import behavior is preserved.
- The topic is not a correction route and declares no correction artifacts. Earlier topic artifacts and evidence are frozen nonrouting provenance and are not review inputs or routing authority.

## Boundaries / Exclusions

- Plan-Creator writes only the five initial planning artifacts. Implementer may write only the ten implementation paths after Planner selects a committed approved candidate receipt. Tester and Independent Reviewer write only their declared evidence paths. An unlisted path is a plan-alignment stop and returns to Planner.
- This topic may not change `AGENTS.md`, workflow contracts, project configuration, root package initializer, test sources, README, or any old gateway design/API/workflow.
- No role may treat the pre-created folders as importable child packages, infer identity outside Identity, make CacheStore a BC, or combine the three future BCs.

## Status / Allowed Transitions

- **Current**: `planned`.
- **Execution model**: committed planning candidate → independent Plan-Reviewer receipt → immutable implementation subject → independent Tester evidence → independent implementation review evidence → Planner Phase 4.5 alignment → bounded publish → draft PR → Human review and merge. This topic stops before release.
- **Allowed transitions**:
  - `planned` -> `planning-candidate-committed`
  - `planning-candidate-committed` -> `plan-review-in-progress`
  - `plan-review-in-progress` -> `plan-review-receipt-committed`
  - `plan-review-receipt-committed` -> `creator-in-progress`
  - `creator-in-progress` -> `tester-in-progress`
  - `tester-in-progress` -> `tester-evidence-committed`
  - `tester-evidence-committed` -> `reviewer-in-progress`
  - `reviewer-in-progress` -> `reviewer-evidence-committed`
  - `reviewer-evidence-committed` -> `approved`
  - `creator-in-progress` -> `needs-rework`
  - `reviewer-in-progress` -> `needs-rework`
  - `needs-rework` -> `creator-in-progress` only with a new immutable implementation subject and a complete new Tester/Reviewer evidence chain
  - `approved` -> `publish-in-progress`
  - `publish-in-progress` -> `pr-open`
  - `pr-open` -> `needs-rework`
  - `pr-open` -> `merged` by Human only
  - `merged` -> terminal

- **Candidate and evidence chain**:
  1. An Implementer commits the five initial planning artifacts as the non-merge candidate commit.
  2. An independent Plan-Reviewer writes the declared receipt against that exact full candidate SHA; an independent Implementer commits that unchanged receipt as the sole changed path, with the candidate as its direct parent.
  3. Only a committed receipt with `verdict: "approved"` permits Planner to select the candidate and dispatch an Implementer. A `needs-rework` receipt establishes no implementation subject or next role.
  4. The Implementer creates a non-merge immutable implementation subject commit that changes exactly the ten implementation paths. The six `## Implementation Steps` entries remain the sole declared completion gate; this replay candidate leaves all six initially pending and does not add the step tracker to the subject diff.
  5. An independent Tester writes factual evidence for that exact full subject SHA without committing it. An independent Implementer commits it unchanged as a sole evidence-only commit whose direct parent is the subject.
  6. An Independent Reviewer consumes only the committed passing Tester evidence for that same subject, writes the review log without committing it, and an independent Implementer commits it unchanged as a sole evidence-only commit whose direct parent is the Tester-evidence commit.
  7. Planner Phase 4.5 may align only the committed approved review log with the same subject. Existing Human authorization is required before bounded push and the topic's draft PR. Human alone reviews and merges the PR.

## Artifact Paths

| Artifact | Path | Write owner | Decision authority and role |
| --- | --- | --- | --- |
| Requirements analysis | `analysis/package-topology-skeleton-replay/requirements.md` | Plan-Creator | Business-intent guardrail; planning candidate only. |
| Technical specification | `analysis/package-topology-skeleton-replay/technical-spec.md` | Plan-Creator | Execution-facing topology contract; planning candidate only. |
| Topic plan | `plan/package-topology-skeleton-replay/package-topology-skeleton-replay.plan.md` | Plan-Creator | Canonical executable topic contract; planning candidate only. |
| Topic specification | `plan/package-topology-skeleton-replay/package-topology-skeleton-replay.spec.md` | Plan-Creator | Acceptance and edge-case contract; planning candidate only. |
| Step tracker | `plan/package-topology-skeleton-replay/package-topology-skeleton-replay.step.md` | Plan-Creator; later Implementer only for its six implementation-step markers | Progression truth; only `## Implementation Steps` is the implementation-completion gate. |
| Plan-review receipt | `plan/package-topology-skeleton-replay/package-topology-skeleton-replay.plan-review-receipt.json` | Independent Plan-Reviewer | Candidate-bound plan approval; must be committed unchanged by an independent Implementer as a receipt-only commit. |
| Architecture source of truth | `docs/business-capability-architecture.md` | Implementer | Defines fixed BC-to-directory mapping and topology-only semantics. |
| Evolution roadmap | `docs/evolution-roadmap.md` | Implementer | Defines fixed Identity-first implementation order. |
| Architecture brief | `docs/architecture/business-capability/architecture-brief.md` | Implementer | Synchronizes BC boundaries, mapping, and phase/order. |
| Interactive scene source | `docs/architecture/business-capability/scene.js` | Implementer | Synchronizes visual labels with the fixed order. |
| Interactive scene mirror | `docs/architecture/business-capability/index.html` | Implementer | Mirrors the same scene labels and order. |
| Identity reservation | `src/deterministic_response_cache/identity/.gitkeep` | Implementer | Topology-only marker for Identity. |
| Response Reuse reservation | `src/deterministic_response_cache/response_reuse/.gitkeep` | Implementer | Topology-only marker for Response Reuse. |
| Loaded Runtime Cache reservation | `src/deterministic_response_cache/loaded_runtime_cache/.gitkeep` | Implementer | Topology-only marker for Loaded Runtime Cache. |
| Model Execution reservation | `src/deterministic_response_cache/model_execution/.gitkeep` | Implementer | Topology-only marker for Model Execution. |
| Provider Adapter reservation | `src/deterministic_response_cache/provider_adapter/.gitkeep` | Implementer | Topology-only marker for Provider Adapter. |
| Tester evidence | `plan/package-topology-skeleton-replay/package-topology-skeleton-replay.tester-evidence.json` | Tester | Factual same-subject validation; an independent Implementer commits the unchanged file as the sole evidence-only commit. |
| Independent implementation review log | `plan/package-topology-skeleton-replay/package-topology-skeleton-replay.implementation-review-log.json` | Independent Reviewer | Same-subject review result; an independent Implementer commits the unchanged file as the sole evidence-only commit. |

`README.md`, project version metadata, `.github/copilot-instructions.md`, root `src/deterministic_response_cache/__init__.py`, `tests/test_package_import.py`, `pyproject.toml`, and `.gitignore` are explicitly read-only. No artifact is deleted. Any path not listed in this table is out of contract and must return to Planner before modification.

### Candidate-bound evidence schemas

All SHA values below are lowercase 40-character hexadecimal Git commit IDs. Any missing, extra, malformed, or cross-topic/cross-subject value fails closed.

- Plan-review receipt is one JSON object with exactly `schema_version`, `candidate_commit`, `verdict`, `blocking_issues`, and `copilot_feedback_triage`. `schema_version` is integer `1`; `candidate_commit` is the full candidate SHA; `verdict` is `approved|needs-rework`; `blocking_issues` is a string array and must be empty for `approved`; `copilot_feedback_triage` is an object with exactly `ADDRESS`, `DISCUSS`, and `SKIP` string arrays. Receipt review inputs are only the five committed candidate artifacts, this topic's declared contract sources, and this topic's recorded feedback. The receipt-only commit changes only this path and has the candidate commit as direct parent.
- Tester evidence is one JSON object with exactly `schema_version`, `topic`, `implementation_subject_commit`, `status`, `commands`, and `recorded_by`. `schema_version` is integer `1`; `topic` is `package-topology-skeleton-replay`; `implementation_subject_commit` is the full immutable subject SHA; `status` is `passing|failing`; `commands` is a non-empty array whose entries have exactly non-empty string `command` and integer `exit_code`; `recorded_by` is `Tester`. `passing` requires every exit code to be `0`; `failing` requires at least one non-zero exit code.
- Independent implementation review log is one JSON object with exactly `schema_version`, `topic`, `implementation_subject_commit`, `tester_evidence_commit`, `verdict`, `blocking_issues`, and `recorded_by`. `schema_version` is integer `1`; `topic` is `package-topology-skeleton-replay`; both commit fields are full SHA values and bind the same subject; `tester_evidence_commit` names the sole committed passing Tester-evidence commit; `verdict` is `approved|needs-rework`; `blocking_issues` is a string array, empty only for `approved`; `recorded_by` is `Independent Reviewer`.

## Python implementation metadata

### Non-goals

- Will not implement any Identity, Response Reuse, runtime, execution, provider, or CacheStore behavior.
- Will not add a public API, child package initializer, Python module, dynamic import, or compatibility facade.
- Will not change root-package direct imports, tests, project configuration, dependencies, README, version, release, tag, merge, or post-merge state.

### Current Context

`src/deterministic_response_cache/__init__.py` is the existing empty public package surface and `tests/test_package_import.py` is its direct-import smoke test. Architecture documents already define the five BC concepts and boundaries, but `docs/evolution-roadmap.md`, `scene.js`, and `index.html` still describe Response Reuse as the first implementation topic. The package has no BC child folders.

### Requirements

1. Create exactly five specified `.gitkeep` files and no `cache_store/`, child `__init__.py`, or Python source below those directories.
2. Align all five architecture surfaces to the fixed mapping, topology-only semantics, boundaries, and Identity-first order.
3. Preserve root package source and direct import behavior unchanged.
4. Keep the implementation subject diff to exactly the ten declared implementation paths.

### Decisions

- Async-planning status: exempt — cited exemption evidence: this topic creates static documentation and empty directory markers only; it introduces no async boundary, lifecycle, concurrency, timeout, cancellation, or I/O behavior.
- Module/package placement: no Python module is added; the five fixed directories are topology-only reservations beneath `src/deterministic_response_cache/`.
- New public API: no.
- Interface changes: no; `src/deterministic_response_cache/__init__.py` and its direct-import behavior remain unchanged.
- Breaking changes allowed: no; no executable package interface changes.
- New dependencies: no.
- Error-handling strategy: no runtime behavior is introduced; invalid extra paths or scope expansion fail plan alignment and return to Planner.
- Typing strategy: no Python code or type surface is introduced.

### Public Contract / API Changes

None. The reserved child directories are not packages and create no public import surface.

### Affected Files / Modules

**Written implementation paths:**

- `docs/business-capability-architecture.md`
- `docs/evolution-roadmap.md`
- `docs/architecture/business-capability/architecture-brief.md`
- `docs/architecture/business-capability/scene.js`
- `docs/architecture/business-capability/index.html`
- `src/deterministic_response_cache/identity/.gitkeep`
- `src/deterministic_response_cache/response_reuse/.gitkeep`
- `src/deterministic_response_cache/loaded_runtime_cache/.gitkeep`
- `src/deterministic_response_cache/model_execution/.gitkeep`
- `src/deterministic_response_cache/provider_adapter/.gitkeep`

**Read-only verification paths:**

- `src/deterministic_response_cache/__init__.py`
- `tests/test_package_import.py`
- `pyproject.toml`
- `.gitignore`
- `README.md`

### Test Plan

- **TestCase 1 — topology happy path:** inspect the package tree; each fixed directory has `.gitkeep`.
- **TestCase 2 — invalid topology:** assert no `cache_store/`, child `__init__.py`, or `.py` file exists in the five reserved directories.
- **TestCase 3 — architecture edge case:** inspect all five architecture surfaces; none calls Response Reuse the first implementation topic, and all state topology-only status without claiming BC availability.
- **TestCase 4 — regression:** run `uv run pytest tests/test_package_import.py`; the unchanged direct root import succeeds.
- **TestCase 5 — backward compatibility:** compare the immutable subject against its parent; `src/deterministic_response_cache/__init__.py` and `tests/test_package_import.py` are absent from the diff and no public import surface is added.

### Risks

- `scene.js` and `index.html` duplicate scene data; updating only one creates visual/documentation drift.
- Empty reserved directories can be mistaken for implemented child packages unless every architecture surface explicitly preserves topology-only semantics.

### Rollback Plan

Revert the immutable implementation subject commit, which removes the five `.gitkeep` files and restores the five named architecture paths. No root package, test, configuration, or release artifact requires rollback.

## Implementation Steps

1. Update `docs/business-capability-architecture.md` to add the fixed five-BC-to-directory mapping, state that each reservation is topology only and non-importable, retain Identity as sole authority, retain CacheStore as Response Reuse internal-only, and retain the future BC separations.
2. Update `docs/evolution-roadmap.md` to make Identity → Response Reuse → Loaded Runtime Cache → Model Execution → Provider Adapter the only stated implementation sequence; replace the conflicting Response-Reuse-first future-topic statement and declare that this topic only reserves folders.
3. Update `docs/architecture/business-capability/architecture-brief.md` to synchronize the fixed mapping, topology-only meaning, Identity-first phase sequence, CacheStore boundary, and separation of the three future BCs.
4. Update `docs/architecture/business-capability/scene.js` so the visible labels mark Identity as the first implementation topic, Response Reuse as second, and describe the folder reservations as non-implemented topology without altering runtime behavior.
5. Update `docs/architecture/business-capability/index.html` with the matching scene-data label changes from `scene.js`, preserving visual parity between the two sources.
6. Create only `identity/.gitkeep`, `response_reuse/.gitkeep`, `loaded_runtime_cache/.gitkeep`, `model_execution/.gitkeep`, and `provider_adapter/.gitkeep` under `src/deterministic_response_cache/`; do not create any child `__init__.py`, Python source, or `cache_store/` path.

## Validation / Acceptance Checks

- Confirm the implementation-subject diff names exactly the ten implementation paths in `Artifact Paths`; no path is deleted.
- Confirm `find src/deterministic_response_cache -mindepth 1 -maxdepth 2 -type f | sort` shows the existing root `__init__.py` and only the five new `.gitkeep` files below the reserved BC folders.
- Confirm `find src/deterministic_response_cache -type f \( -name '__init__.py' -o -name '*.py' \) | sort` lists only the unchanged root `__init__.py`.
- Confirm no `src/deterministic_response_cache/cache_store` directory exists.
- Confirm the five architecture paths contain the same mapping, topology-only wording, Identity-first order, and CacheStore/internal plus future-BC boundaries.
- Run the project validation commands: `uv lock --check`; `uv run ruff format --check .`; `uv run ruff check .`; `uv run pyright`; `uv run tach check`; `uv run pytest`; and `uv run pre-commit run --all-files`.
- Tester records each command and its actual exit code in the declared Tester evidence. Independent Reviewer verifies the same immutable subject, passing evidence, exact ten-path diff, preserved direct import, and no forbidden source/package path.

## Reviewer Handoff

The following is a shape-only template, not a receipt: the Plan-Reviewer replaces the candidate placeholder with the exact committed candidate SHA before writing the receipt.

```json
{
  "schema_version": 1,
  "candidate_commit": "<full-40-hex-candidate-sha>",
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

No release, tag, version bump, README update, post-merge action, or final summary is authorized by this topic. After the draft PR opens, Human performs review and may merge; Human owns every subsequent action.

## Open Questions / Unresolved Items

None. The Human-approved replay route and the fixed topology, boundaries, implementation order, read-only paths, evidence sequence, and validation commands resolve the planning decisions for this topic.
