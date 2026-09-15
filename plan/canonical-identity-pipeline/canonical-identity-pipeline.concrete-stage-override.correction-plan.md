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

The parent technical specification, topic plan, topic specification, and step tracker were updated
by C0. C0 is the immutable six-path candidate
`82bb4413f0f53e912b4cf30abb65b5a13c84a93a`; its approved C1 log binds tree
`e2e4c638b74205b7cb158e1c8f92e592970a03bb`. C2 is the immutable sole-evidence commit
`15c23d67856b627fa8f736eb66694cccc9e5ec89`, a non-merge direct child of C0 whose exact one-path
diff adds the unchanged approved C1 log. These facts, the log, and its recorded reviewed blobs are
frozen; no later role may rewrite, re-review, or use them as C3 Tester or Reviewer evidence.

The rejected status-only route is C0S `46b707c209839f64935beb08e4db8a1b565c8114`: its C1S JSON
schema used double-escaped tab text, preventing parsed `name_status` values from matching Git.
No C1S log was written. The currently active route is C0S-R1, its Human-authorized status-only
non-merge direct child. It repairs that contract while synchronizing frozen C0/C1/C2 facts across
the four CSO1 planning state surfaces before C3 begins. This file, its paired correction step, the
parent plan, and the parent step tracker are C0S-R1's only mutable state surfaces. The prior
original six-path subject and all CAVO1 records remain frozen provenance: they cannot be reused as
a CSO1 candidate, Tester record, or Reviewer record.

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

## C0S-R1 status-synchronization boundary

- C0S is rejected frozen provenance. C0S-R1 changes exactly six existing planning paths: the parent
  plan, parent step tracker, this CSO1 correction plan, this CSO1 correction step, and the paired
  status-sync correction plan/step. It records only frozen-complete C0/C1/C2, rejected C0S,
  C0S-R1 review pending, C3 pending, and C4–C8 not started. It creates no implementation subject
  or execution evidence.
- C0S-R1 must be a non-merge direct child whose sole first parent is rejected C0S
  `46b707c209839f64935beb08e4db8a1b565c8114`. Its first-parent name-status diff must contain
  exactly once, in lexical path order, the following entries:

  ```text
  M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-status-sync.correction-plan.md
  M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-status-sync.correction-step.md
  M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-plan.md
  M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-step.md
  M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md
  M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.step.md
  ```

- No C0S-R1 commit SHA, tree SHA, candidate blob SHA, review outcome, or C1S evidence may be filled
  in before C0S-R1 is committed. `README.md`, `pyproject.toml`, and `uv.lock` remain unstaged and
  unchanged. C0S-R1 never modifies analysis, the parent specification, code, tests, diagrams,
  existing evidence, the draft PR, or the published stable-library surface.
- The independent C1S reviewer must fail closed unless all four state surfaces agree on the same
  frozen C0/C1/C2 facts, rejected C0S, C0S-R1 review-pending status, C3 as the only pending CSO1
  execution step, and C4–C8 as not started; it must also parse every `name_status` string as one
  `M`, one actual tab, and its exact path. An approved C1S log is separately committed unchanged
  by an Independent Implementer as C2S; only then may Planner route the existing C3 subject.

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
| C0 | Parent technical specification | `analysis/canonical-identity-pipeline/technical-spec.md` | Plan-Creator | Completed immutable six-path CSO1 candidate surface. |
| C0 | Parent topic plan | `plan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md` | Plan-Creator | Completed candidate's current route and path contract. |
| C0 | Parent topic specification | `plan/canonical-identity-pipeline/canonical-identity-pipeline.spec.md` | Plan-Creator | Completed testable nominal-inheritance and marker contract. |
| C0 | Parent step tracker | `plan/canonical-identity-pipeline/canonical-identity-pipeline.step.md` | Plan-Creator | CSO1 progression truth, synchronized by C0S-R1 only. |
| C0 | Correction plan | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-plan.md` | Plan-Creator | This CSO1 trigger, scope, ordering, and schema authority; synchronized by C0S-R1 only. |
| C0 | Correction step | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-step.md` | Plan-Creator | CSO1 execution/evidence tracking; synchronized by C0S-R1 only. |
| C1 | Correction Plan-Reviewer log | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-plan-review-log.json` | Independent Plan-Reviewer | Completed approved record, committed unchanged by C2; frozen provenance for all later steps. |
| C2 | Committed C1 evidence | same C1 path | Independent Implementer | Completed sole-evidence commit `15c23d67856b627fa8f736eb66694cccc9e5ec89`; C3 is not routable until C2S. |
| C0S-R1 | Revised status-sync candidate | parent plan, parent step, this CSO1 plan/step, and paired status-sync plan/step | Plan-Creator | Exact six-path non-merge direct child of rejected C0S; records state only and awaits C1S. |
| C1S | Status-sync Plan-Reviewer log | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-status-sync.correction-plan-review-log.json` | Independent Plan-Reviewer | Sole C0S-R1 review artifact, written only from a clean committed C0S-R1 checkout under the v2 schema below. |
| C2S | Committed C1S evidence | same C1S path | Independent Implementer | Commits unchanged approved C1S evidence as its sole evidence-only commit; only then may Planner route C3. |
| C3 | Immutable implementation subject | `src/deterministic_response_cache/identity/canonical.py`, `tests/test_canonical_identity_pipeline.py` | Implementer | Exactly the two locked paths; no evidence is in this commit. |
| C4 | Correction Tester evidence | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-tester-evidence.json` | Tester | Factual same-subject validation only; not self-committed. |
| C5 | Committed C4 evidence | same C4 path | Independent Implementer | Commits unchanged passing C4 evidence as its sole evidence-only commit. |
| C6 | Correction implementation-review log | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-implementation-review-log.json` | Independent Reviewer | Only after committed passing C4; reviews a clean committed C5 tree and the same C3 subject. |
| C7 | Committed C6 evidence | same C6 path | Independent Implementer | Commits unchanged approved C6 evidence as its sole evidence-only commit. |
| C8 | Phase 4.5 / bounded PR update | no new CSO1 artifact | Planner, then Implementer if authorized | Requires C7, parent alignment, and existing human authorization; pushes only to update draft PR #6 and never authorizes merge or a new PR. |

`needs-rework` in C1S or C6 returns to Planner. An approved C1S does not implement or approve C3;
it only restores Planner routing authority for that still-pending subject. A new implementation
subject starts a new C3–C7 sequence; no prior C4/C5/C6/C7 can be reused. Missing evidence is
`blocked`; competing candidate, evidence, subject, or worktree facts are `human-check`.

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

### C1S status-sync correction Plan-Reviewer log

Only the independent C1S Plan-Reviewer may create this file, only after the C0S-R1 candidate is
committed and from a clean checkout of that commit. It is a single JSON object with exactly the
twelve top-level keys below. `reviewed_paths` has exactly the six entries in the stated order and
each entry has exactly `path` and `blob_sha`. `first_parent_admission` has exactly the seven keys
shown. All Git identifiers are lowercase 40-hex values. `approved` requires empty
`blocking_issues`; `needs-rework` requires at least one non-empty issue. Extra/missing keys,
altered nested shape, mismatched rejected-C0S parent, merge topology, unlisted path, a
`name_status` value that does not parse to `M<TAB>path`, non-clean review, inconsistent
four-surface facts, a C3 completion claim, or a publish/PR/Human-review claim fails closed.

```json
{
  "schema_version": "canonical-identity-pipeline.concrete-stage-override-status-sync.correction-plan-review.v2",
  "topic": "canonical-identity-pipeline",
  "correction_id": "canonical-identity-pipeline/concrete-stage-override-status-sync",
  "candidate_commit": "<40-hex C0S-R1 commit>",
  "candidate_tree": "<40-hex C0S-R1 tree>",
  "reviewed_paths": [
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-status-sync.correction-plan.md", "blob_sha": "<40-hex C0S-R1 blob>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-status-sync.correction-step.md", "blob_sha": "<40-hex C0S-R1 blob>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-plan.md", "blob_sha": "<40-hex C0S-R1 blob>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-step.md", "blob_sha": "<40-hex C0S-R1 blob>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md", "blob_sha": "<40-hex C0S-R1 blob>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.step.md", "blob_sha": "<40-hex C0S-R1 blob>"}
  ],
  "first_parent_admission": {
    "candidate_commit": "<same 40-hex C0S-R1 commit>",
    "candidate_tree": "<same 40-hex C0S-R1 tree>",
    "parent_commit": "46b707c209839f64935beb08e4db8a1b565c8114",
    "non_merge": true,
    "first_parent": true,
    "exact_declared_paths": true,
    "name_status": [
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-status-sync.correction-plan.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-status-sync.correction-step.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-plan.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-step.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.step.md"
    ]
  },
  "review_basis": "clean committed C0S-R1 candidate checkout; direct non-merge first-parent admission from rejected C0S 46b707c209839f64935beb08e4db8a1b565c8114; C0S-R1 name_status parses to six actual M-tab-path entries; four state surfaces agree on frozen C0/C1/C2 facts, rejected C0S, C0S-R1 review pending, C3 pending, and C4-C8 not started; no implementation, Tester, Reviewer, publish, push, PR, or Human review claim",
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "copilot_feedback_triage": {"ADDRESS": [], "DISCUSS": [], "SKIP": []},
  "recorded_by": "Independent Plan-Reviewer"
}
```

The reviewer's C1S file is not prewritten, is not part of C0S-R1, and cannot be combined with any
other path. Only an Independent Implementer may commit an unchanged approved C1S file as C2S.
After C2S, Planner must independently perform the route decision; C0S-R1 never itself selects C3.

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
