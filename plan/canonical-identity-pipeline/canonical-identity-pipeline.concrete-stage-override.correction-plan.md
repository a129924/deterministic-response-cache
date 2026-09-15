---
topic: canonical-identity-pipeline
correction_id: canonical-identity-pipeline/concrete-stage-override
phase: correction-plan-review
created: 2026-09-15
---

# CSO1 — Concrete-stage named inheritance and `@override` correction plan

## Trigger and current truth

Human requires the delivered concrete stages to declare their existing Protocol relationship
nominally and to mark their one public Protocol implementation with Python 3.12 `@override`.
This is a narrow correction to the open `canonical-identity-pipeline` draft PR #6, not a change to
the canonical grammar, Builder orchestration, public handoffs, or identity ownership.

The parent technical specification, topic plan, topic specification, and step tracker are updated
by C0 and are CSO1 current truth. This file and its paired correction step define the narrow
subject, role sequence, and extended evidence schema. The prior original six-path subject and all
CAVO1 records are frozen provenance: they cannot be reused as a CSO1 candidate, Tester record, or
Reviewer record.

## Locked scope

- The new CSO1 immutable implementation subject changes exactly these two paths:
  1. `src/deterministic_response_cache/identity/canonical.py`
  2. `tests/test_canonical_identity_pipeline.py`
- `canonical.py` imports `override` only from Python 3.12 `typing`. It makes the five concrete
  classes directly and explicitly inherit, respectively, `Validator`, `Sorter`, `Encoder`,
  `Serializer`, and `Hasher` from the existing `contracts.py`; it does not alter that module.
- Only `PureTypeValidator.validate`, `CanonicalSorter.sort`, `CanonicalEncoder.encode`,
  `CanonicalSerializer.serialize`, and `SHA256Hasher.hash` receive `@override`. Private class
  helpers (`_validate_value`, `_validate_sequence`, `_validate_mapping`, `_sort_value`,
  `_encode_value`, `_encode_scalar`) and all module helpers/factories remain unmarked.
- The dedicated test preserves every existing direct import and pipeline regression. It adds direct
  nominal assertions for each named base (`stage.__bases__ == (expected_protocol,)`),
  `stage_method.__override__ is True` on each matching public method, and
  `getattr(private_helper, "__override__", False) is False` for every private class helper. It uses
  no `importlib`, `__import__`, or `sys.modules` substitution.
- `contracts.py`, `builders.py`, `identity/__init__.py`, every existing test other than the one
  dedicated module, both Archify artifacts, README, `pyproject.toml`, `uv.lock`, and all historic
  planning/evidence files are read-only for C3. No new API, export, dependency, diagram, version,
  publish file, or new PR is authorized.

## Acceptance delta

CSO1 passes only when all of the following are true:

1. Each concrete stage's direct named base is exactly its matching existing Protocol.
2. The five matching public stage methods, and only those methods among class helpers, expose
   `__override__ is True`.
3. The existing exact Encoder-string, Serializer-bytes, validation, deterministic, composition,
   direct-import, and Builder regression behavior continues unchanged.
4. The immutable C3 diff has exactly the two declared paths; no CAVO1 evidence or subject is
   referenced as CSO1 evidence.
5. Required tests and static checks complete with exit code 0, then CSO1 receives a fresh
   same-subject passing Tester record and independent approved Reviewer record.

## Exact correction artifacts and evidence order

| Order | Artifact | Exact path | Writer | Authority / condition |
| --- | --- | --- | --- | --- |
| C0 | Parent technical specification | `analysis/canonical-identity-pipeline/technical-spec.md` | Plan-Creator | CSO1 execution-facing contract and exact two-path subject. |
| C0 | Parent topic plan | `plan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md` | Plan-Creator | Current topic route, path contract, and Phase 4.5 condition. |
| C0 | Parent topic specification | `plan/canonical-identity-pipeline/canonical-identity-pipeline.spec.md` | Plan-Creator | Testable nominal-inheritance and marker behavior. |
| C0 | Parent step tracker | `plan/canonical-identity-pipeline/canonical-identity-pipeline.step.md` | Plan-Creator | CSO1 progression truth only. |
| C0 | Correction plan | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-plan.md` | Plan-Creator | This CSO1 trigger, scope, ordering, and extended schema authority. |
| C0 | Correction step | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-step.md` | Plan-Creator | CSO1 execution/evidence tracking. |
| C1 | Correction Plan-Reviewer log | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-plan-review-log.json` | Independent Plan-Reviewer | Written only after C0 is committed and reviewed from a clean checkout. |
| C2 | Committed C1 evidence | same C1 path | Independent Implementer | Commits unchanged approved C1 evidence as its sole evidence-only commit; only then may Planner route C3. |
| C3 | Immutable implementation subject | `src/deterministic_response_cache/identity/canonical.py`, `tests/test_canonical_identity_pipeline.py` | Implementer | Exactly the two locked paths; no evidence is in this commit. |
| C4 | Correction Tester evidence | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-tester-evidence.json` | Tester | Factual same-subject validation only; not self-committed. |
| C5 | Committed C4 evidence | same C4 path | Independent Implementer | Commits unchanged passing C4 evidence as its sole evidence-only commit. |
| C6 | Correction implementation-review log | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-implementation-review-log.json` | Independent Reviewer | Only after committed passing C4; reviews a clean committed C5 tree and the same C3 subject. |
| C7 | Committed C6 evidence | same C6 path | Independent Implementer | Commits unchanged approved C6 evidence as its sole evidence-only commit. |
| C8 | Phase 4.5 / bounded PR update | no new CSO1 artifact | Planner, then Implementer if authorized | Requires C7, parent alignment, and existing human authorization; pushes only to update draft PR #6 and never authorizes merge or a new PR. |

`needs-rework` in C1 or C6 returns to Planner. A new implementation subject starts a new C3–C7
sequence; no prior C4/C5/C6/C7 can be reused. Missing evidence is `blocked`; competing candidate,
evidence, subject, or worktree facts are `human-check`.

## Extended evidence schemas

These schemas supersede generic parent evidence shapes only for CSO1. Every object has exactly the
listed top-level keys. Commit and tree IDs are complete lowercase 40-hex SHA values. Every command
entry has exactly a non-empty string `command` and integer `exit_code`. Extra, missing, malformed,
cross-topic, cross-correction, or cross-subject fields fail closed.

### C1 correction Plan-Reviewer log

`reviewed_paths` contains exactly the six C0 paths in the table order; every entry has exactly
`path` and `blob_sha`. `approved` requires an empty `blocking_issues`; `needs-rework` requires at
least one issue.

```json
{
  "schema_version": "canonical-identity-pipeline.concrete-stage-override.correction-plan-review.v1",
  "topic": "canonical-identity-pipeline",
  "correction_id": "canonical-identity-pipeline/concrete-stage-override",
  "candidate_commit": "<40-hex C0 commit>",
  "candidate_tree": "<40-hex C0 tree>",
  "reviewed_paths": [
    {"path": "analysis/canonical-identity-pipeline/technical-spec.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.spec.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.step.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-plan.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-step.md", "blob_sha": "<40-hex>"}
  ],
  "review_basis": "clean committed C0 tree; explicit Human override; exact CSO1 two-path subject and fresh evidence route",
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "copilot_feedback_triage": {"ADDRESS": [], "DISCUSS": [], "SKIP": []},
  "recorded_by": "Independent Plan-Reviewer"
}
```

### C4 correction Tester evidence

`implementation_subject_paths` is exactly the two C3 paths in the stated order. `passing` requires
every command exit code to be 0; `failing` requires at least one non-zero exit code. Tester verifies
the C3 commit's exact two-path name-status before running the direct-import and pipeline regressions,
format/lint/type/architecture/full-test/pre-commit checks.

```json
{
  "schema_version": "canonical-identity-pipeline.concrete-stage-override.correction-tester-evidence.v1",
  "topic": "canonical-identity-pipeline",
  "correction_id": "canonical-identity-pipeline/concrete-stage-override",
  "implementation_subject_commit": "<40-hex C3 SHA>",
  "implementation_subject_paths": [
    "src/deterministic_response_cache/identity/canonical.py",
    "tests/test_canonical_identity_pipeline.py"
  ],
  "status": "passing|failing",
  "commands": [{"command": "<exact command>", "exit_code": 0}],
  "recorded_by": "Tester"
}
```

### C6 correction implementation-review log

`reviewed_paths` is exactly the two C3 paths in the stated order. `approved` requires
`clean_worktree: true`, committed same-subject C4 `status: "passing"`, an empty
`blocking_issues`, named base/marker assertions, preserved direct imports, and no scope drift.
`needs-rework` requires at least one blocking issue.

```json
{
  "schema_version": "canonical-identity-pipeline.concrete-stage-override.correction-implementation-review.v1",
  "topic": "canonical-identity-pipeline",
  "correction_id": "canonical-identity-pipeline/concrete-stage-override",
  "implementation_subject_commit": "<same 40-hex C3 SHA>",
  "tester_evidence_commit": "<40-hex C5 SHA>",
  "reviewed_tree": "<40-hex C5 tree>",
  "clean_worktree": true,
  "reviewed_paths": [
    "src/deterministic_response_cache/identity/canonical.py",
    "tests/test_canonical_identity_pipeline.py"
  ],
  "review_basis": "clean committed C5 tree; same-subject passing C4 evidence; CSO1 nominal Protocol base, public override marker, private-helper, direct-import, and scope verification",
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "copilot_feedback_triage": {"ADDRESS": [], "DISCUSS": [], "SKIP": []},
  "recorded_by": "Independent Reviewer"
}
```

## Required CSO1 validation

Tester records the actual commands and exit codes for the following checks; exact C3 scope must be
verified before their execution:

```bash
git diff-tree --no-commit-id --name-status -r <C3-full-SHA>
uv run pytest tests/test_canonical_identity_pipeline.py tests/test_model_feature_identity_contracts.py tests/test_model_feature_identity_builders.py
uv run ruff format --check .
uv run ruff check .
uv run pyright
uv run tach check
uv run pytest
uv run pre-commit run --all-files
```

No Archify command runs for CSO1. A required non-zero result is factual `failing` evidence and
returns to Planner; it is never described as success.
