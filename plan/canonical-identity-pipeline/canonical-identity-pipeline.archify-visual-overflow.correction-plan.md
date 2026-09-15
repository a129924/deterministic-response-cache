# CAVO1 — Archify visual-overflow correction plan

## Trigger and retained history

`canonical-identity-pipeline/archify-visual-overflow` (CAVO1) is a narrow correction route
triggered because the delivered Archify dataflow viewer passed showcase validation but
`visual-check` reported desktop vertical overflow. The parent technical specification, topic plan,
topic specification, and step tracker are updated by this candidate and become the current
execution truth. This correction plan and its paired correction step retain the historical reason,
round evidence contract, and correction-specific lifecycle; they do not replace the parent
artifacts as the topic's current truth.

## Locked scope

- The only paths a later correction Implementer may *modify* are
  `docs/architecture/canonical-identity-pipeline.dataflow.json` and
  `docs/architecture/canonical-identity-pipeline.html`.
- Geometry and concise authored-content changes are allowed only to eliminate desktop overflow.
  The Identity pipeline semantics, main-rail nodes and order, string/bytes handoffs, leaf and
  `combine()` behavior, `Failure` boundary, BC ownership, public Python API, Python code, and
  tests are unchanged. No new node, relationship, adjacent BC, or failure route is permitted.
- The pre-existing uncommitted Python implementation paths remain byte-identical through CAVO1;
  they are neither staged nor committed by this correction-planning candidate. The final immutable
  implementation subject still has the original six non-publish paths, but CAVO1 permits changing
  only its two Archify entries after its review gate.
- Each focused round changes the Archify source as needed, re-delivers the HTML from that source,
  then runs showcase validation, delivery, and desktop visual-check. Generated contact sheets,
  screenshots, and JSON sidecars are temporary untracked evidence and must be removed before the
  immutable implementation-subject commit.

## Acceptance delta and bounded rounds

At most two focused geometry/content rounds are permitted. In every round all of the following are
required: showcase validation reports 9/9 checks with zero errors and warnings; `deliver` exits 0;
and `visual-check` exits 0 for 1440×900, 1600×1000, 1920×1080, and 2048×1320, with no horizontal
or vertical document overflow. A failing viewport count is the number of these four viewports that
fails containment. Round 2 is allowed only as a focused response to Round 1 diagnostics. If two
rounds do not strictly reduce that count, or if Round 2 still has any overflow or any required
command is non-zero, the outcome is `human-check`; no third round, alternate renderer change, or
scope expansion is authorized.

## Exact correction artifacts and evidence order

| Order | Artifact | Exact path | Writer | Authority / condition |
| --- | --- | --- | --- | --- |
| C0 | Correction plan | `plan/canonical-identity-pipeline/canonical-identity-pipeline.archify-visual-overflow.correction-plan.md` | Plan-Creator | Historical CAVO1 trigger, scope, acceptance delta, and extended schema authority. |
| C0 | Correction step | `plan/canonical-identity-pipeline/canonical-identity-pipeline.archify-visual-overflow.correction-step.md` | Plan-Creator | Historical CAVO1 execution/evidence sequence. |
| C1 | Correction Plan-Reviewer log | `plan/canonical-identity-pipeline/canonical-identity-pipeline.archify-visual-overflow.correction-plan-review-log.json` | Independent Plan-Reviewer | Written only after this six-path planning candidate is committed and reviewed from a clean checkout. |
| C2 | Committed C1 evidence | same C1 path | Independent Implementer | Commits the unchanged approved C1 log as its sole evidence-only commit; only then may Planner route the CAVO1 Implementer. |
| C3 | Immutable implementation subject | the original six non-publish implementation paths | Implementer | May alter only the two declared Archify paths during CAVO1; the four pre-existing Python paths remain byte-identical. |
| C4 | Correction Tester evidence | `plan/canonical-identity-pipeline/canonical-identity-pipeline.archify-visual-overflow.correction-tester-evidence.json` | Tester | Factual C3 validation only; binds the same full implementation-subject SHA and is not self-committed. |
| C5 | Committed C4 evidence | same C4 path | Independent Implementer | Commits unchanged passing C4 evidence as its sole evidence-only commit. |
| C6 | Correction Reviewer log | `plan/canonical-identity-pipeline/canonical-identity-pipeline.archify-visual-overflow.correction-implementation-review-log.json` | Independent Reviewer | Only after committed passing C4; reviews a clean committed tree and the same C3 subject. |
| C7 | Committed C6 evidence | same C6 path | Independent Implementer | Commits unchanged approved C6 evidence as its sole evidence-only commit. |
| C8 | Phase 4.5 / publish decision | no new CAVO1 artifact | Planner, then Implementer if authorized | Requires C7, parent-plan alignment, and existing Human authorization; it never authorizes merge. |

`needs-rework` in C1 or C6 stops the CAVO1 route and returns to Planner; no evidence path is
written for a rejected predecessor. A successful CAVO1 route does not supersede Human review,
merge, release, tag, or post-merge authority.

## Extended evidence schemas

These schemas are the CAVO1 authority and supersede the parent plan's generic Tester/Reviewer
schemas only for this correction route. Every object uses exactly the listed top-level keys; SHA
values are complete lowercase 40-hex commits unless a field explicitly names a SHA-256 artifact
digest. Extra, missing, cross-topic, cross-subject, or malformed fields fail closed.
Each C1 `reviewed_paths` entry has exactly `path` and `blob_sha`. Each C4 round has exactly
`round`, `showcase`, `delivery`, and `visual_check`; those nested objects have exactly the keys
shown below. Each C6 `reviewed_paths` entry is one of the two exact strings shown below.

### C1 correction Plan-Reviewer log

```json
{
  "schema_version": "canonical-identity-pipeline.archify-visual-overflow.correction-plan-review.v1",
  "topic": "canonical-identity-pipeline",
  "correction_id": "canonical-identity-pipeline/archify-visual-overflow",
  "candidate_commit": "<40-hex C0 commit>",
  "candidate_tree": "<40-hex C0 tree>",
  "reviewed_paths": [
    {"path": "analysis/canonical-identity-pipeline/technical-spec.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.spec.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.step.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.archify-visual-overflow.correction-plan.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.archify-visual-overflow.correction-step.md", "blob_sha": "<40-hex>"}
  ],
  "review_basis": "clean committed C0 tree; parent current-truth sync; exact CAVO1 scope and evidence route",
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "copilot_feedback_triage": {"ADDRESS": [], "DISCUSS": [], "SKIP": []},
  "recorded_by": "Independent Plan-Reviewer"
}
```

### C4 correction Tester evidence

```json
{
  "schema_version": "canonical-identity-pipeline.archify-visual-overflow.correction-tester-evidence.v1",
  "topic": "canonical-identity-pipeline",
  "correction_id": "canonical-identity-pipeline/archify-visual-overflow",
  "implementation_subject_commit": "<40-hex C3 SHA>",
  "rounds": [
    {
      "round": 1,
      "showcase": {"command": "<validate command>", "exit_code": 0, "checks": 9, "errors": 0, "warnings": 0},
      "delivery": {"command": "<deliver command>", "exit_code": 0, "source_sha256": "<64-hex>", "artifact_sha256": "<64-hex>"},
      "visual_check": {"command": "<visual-check command>", "exit_code": 0, "failing_viewports": 0}
    }
  ],
  "status": "passing|failing",
  "commands": [{"command": "<exact command>", "exit_code": 0}],
  "recorded_by": "Tester"
}
```

`rounds` contains one or two sequential entries only. A `passing` record has one successful round
with `failing_viewports: 0`; a `failing` record documents the actual non-zero command or remaining
overflow. The `commands` array is non-empty and every entry has exactly a non-empty `command` and
integer `exit_code`.

### C6 correction implementation-review log

```json
{
  "schema_version": "canonical-identity-pipeline.archify-visual-overflow.correction-implementation-review.v1",
  "topic": "canonical-identity-pipeline",
  "correction_id": "canonical-identity-pipeline/archify-visual-overflow",
  "implementation_subject_commit": "<same 40-hex C3 SHA>",
  "tester_evidence_commit": "<40-hex C5 SHA>",
  "reviewed_tree": "<40-hex C5 tree>",
  "clean_worktree": true,
  "reviewed_paths": [
    "docs/architecture/canonical-identity-pipeline.dataflow.json",
    "docs/architecture/canonical-identity-pipeline.html"
  ],
  "review_basis": "clean committed C5 tree; same-subject passing C4 evidence; CAVO1 scope, delivery, and visual containment verification",
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "copilot_feedback_triage": {"ADDRESS": [], "DISCUSS": [], "SKIP": []},
  "recorded_by": "Independent Reviewer"
}
```

An `approved` C6 record requires `clean_worktree: true`, exactly the two reviewed Archify paths,
committed same-subject C4 `status: "passing"`, zero remaining overflow, and no sidecars in the C3
diff. `approved` requires an empty `blocking_issues` array; `needs-rework` requires a non-empty
array.

## Parent synchronization and stopping rule

The parent technical specification, plan, specification, and step tracker name CAVO1 as the
current correction route and reference this file for detail. They must be kept in sync by this C0
commit; later CAVO1 changes do not edit those parent artifacts. Any need to change another path,
pipeline meaning, node/edge content, or round policy returns to Planner. A non-zero result, failed
containment after the second focused round, or two rounds without a strict viewport-count reduction
is `human-check` rather than an implicit retry.
