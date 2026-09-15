---
topic: canonical-identity-pipeline
correction_id: canonical-identity-pipeline/cavo1-tracker-status-sync
kind: tracker-status-synchronization
created: 2026-09-15
---

# CAVO1 tracker-status synchronization correction plan

## Purpose

Synchronize the parent topic tracker with already committed CAVO1 facts only. This is a planning
metadata correction: it neither repairs nor reopens the canonical identity pipeline, CAVO1
diagram, test results, evidence contracts, or publish scope.

## Candidate lineage

`05f5ded7e81317c69422aaabe9d6e90a5da1fe6d` is C0, the rejected three-path predecessor. It is
frozen, non-routing provenance because its S1 review-log contract did not fully specify the
candidate-admission and feedback-triage evidence shape. No S1 review log was written for C0.

This revision is C0R: a new three-path, non-merge direct child of C0. C0R is the only candidate
that S1 may review. Its immutable commit SHA, tree SHA, and three candidate blob SHAs are
post-commit facts and must not be prefilled in this candidate; only the independent S1 review log
may record them. C0R is awaiting independent Plan-Reviewer review and has no routing, publish, or
Phase 4.5 authority.

## Locked Source Facts

The following full immutable commit identifiers are the only facts this correction may record:

| CAVO1 step | Fact | Commit |
| --- | --- | --- |
| C1/C2 | Independent Plan-Reviewer record and its evidence-only commit | `d34d6311d30b4d18ed0e9c34d226cdb1800fca2a` |
| C3 | Immutable six-path implementation subject | `602d5f06540c243b591145d9c1ecaf9de840a913` |
| C4/C5 | Passing Tester evidence and its evidence-only commit | `b2a132ef1637ffbdb494c125bf91926fc2e9eb1e` |
| C6/C7 | Approved independent Reviewer evidence and its evidence-only commit | `d7f8a5ee18106fc2fa0b2b0dbfd088468ad6ee6c` |

C1–C7 are complete. C8 remains solely a pending Planner Phase 4.5 alignment. Human PR review is
pending. No publish commit, push, draft PR, merge, release, tag, post-merge, or final summary is
asserted by this correction.

## Exact Candidate Scope and admission

The Plan-Creator candidate commit contains exactly these three paths:

1. `plan/canonical-identity-pipeline/canonical-identity-pipeline.step.md`
2. `plan/canonical-identity-pipeline/canonical-identity-pipeline.cavo1-tracker-status-sync.correction-plan.md`
3. `plan/canonical-identity-pipeline/canonical-identity-pipeline.cavo1-tracker-status-sync.correction-step.md`

The candidate must preserve, without staging or editing, the existing `README.md` and
`pyproject.toml` publish diff. `uv.lock` must remain without a diff. All pipeline implementation,
tests, diagram artifacts, existing evidence, history, parent plan/specification/technical
specification, and the parent publish scope are read-only.

C0R must be a non-merge direct child whose sole first parent is C0
`05f5ded7e81317c69422aaabe9d6e90a5da1fe6d`. Its first-parent name-status diff must contain
exactly, once and in this lexical order, the following three entries:

```text
M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.cavo1-tracker-status-sync.correction-plan.md
M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.cavo1-tracker-status-sync.correction-step.md
M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.step.md
```

## Evidence Route

| Order | Artifact / action | Exact path | Sole writer or actor | Condition |
| --- | --- | --- | --- | --- |
| C0R | Revised tracker-status candidate | the three paths above | Plan-Creator | Commit only the exact three paths as the non-merge direct child of C0; do not self-close the candidate. |
| S1 | Correction Plan-Reviewer log | `plan/canonical-identity-pipeline/canonical-identity-pipeline.cavo1-tracker-status-sync.correction-plan-review-log.json` | Independent Plan-Reviewer | Review C0R from a clean committed checkout; write no other path. |
| S2 | Committed S1 evidence | same S1 path | Independent Implementer | Commit unchanged approved S1 evidence as the sole evidence-only commit. |
| S3 | C8 re-evaluation | no new correction artifact | Planner | Re-evaluate only C8 using C1–C7, S2, parent alignment, and existing Human authorization. |

`needs-rework` at S1 returns to Planner. The S1 log is not prewritten and no other role may write
it. This correction creates no Implementer source work, Tester evidence, independent implementation
review, publish authority, push authority, or PR authority.

## S1 Review-log Contract

The independent Plan-Reviewer is the unique writer of one JSON object with exactly these twelve
top-level keys and no others: `schema_version`, `topic`, `correction_id`, `candidate_commit`,
`candidate_tree`, `reviewed_paths`, `first_parent_admission`, `review_basis`, `verdict`,
`blocking_issues`, `copilot_feedback_triage`, and `recorded_by`. `<...>` values are filled only
after C0R is committed. This v2 schema supersedes the rejected C0 v1 schema; no v1-shaped record
can approve C0R.

```json
{
  "schema_version": "canonical-identity-pipeline.cavo1-tracker-status-sync.correction-plan-review.v2",
  "topic": "canonical-identity-pipeline",
  "correction_id": "canonical-identity-pipeline/cavo1-tracker-status-sync",
  "candidate_commit": "<40-hex C0R commit>",
  "candidate_tree": "<40-hex C0R tree>",
  "reviewed_paths": [
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.cavo1-tracker-status-sync.correction-plan.md", "blob_sha": "<40-hex C0R blob>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.cavo1-tracker-status-sync.correction-step.md", "blob_sha": "<40-hex C0R blob>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.step.md", "blob_sha": "<40-hex C0R blob>"}
  ],
  "first_parent_admission": {
    "candidate_commit": "<same 40-hex C0R commit>",
    "candidate_tree": "<same 40-hex C0R tree>",
    "parent_commit": "05f5ded7e81317c69422aaabe9d6e90a5da1fe6d",
    "non_merge": true,
    "first_parent": true,
    "exact_declared_paths": true,
    "name_status": [
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.cavo1-tracker-status-sync.correction-plan.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.cavo1-tracker-status-sync.correction-step.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.step.md"
    ]
  },
  "review_basis": "clean committed C0R candidate checkout; direct non-merge first-parent admission from rejected C0 05f5ded7e81317c69422aaabe9d6e90a5da1fe6d; locked C1-C7 facts retained; C8 remains Planner Phase 4.5 pending; Human PR review, merge, release, tag, post-merge, and final summary remain pending",
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "copilot_feedback_triage": {"ADDRESS": [], "DISCUSS": [], "SKIP": []},
  "recorded_by": "Independent Plan-Reviewer"
}
```

`candidate_commit`, `candidate_tree`, and every `blob_sha` must each be a lowercase 40-hex Git
object identifier. `reviewed_paths` must have exactly the three ordered entries shown above, and
every entry has exactly `path` and `blob_sha`. `first_parent_admission` has exactly
`candidate_commit`, `candidate_tree`, `parent_commit`, `non_merge`, `first_parent`,
`exact_declared_paths`, and `name_status`; its candidate values equal the top-level candidate
values, its parent is the exact C0 SHA above, both boolean admission flags are `true`, and its
`name_status` is the exact three-entry array shown above. The reviewer verifies these facts from a
clean committed C0R checkout, never from the working tree.

`review_basis` must equal the displayed literal and thereby bind the clean committed candidate,
C0's rejection, retained C1-C7 facts, C8's pending Planner-only status, and the still-pending
Human boundary. `copilot_feedback_triage` has exactly `ADDRESS`, `DISCUSS`, and `SKIP`, each an
array. `approved` requires an empty `blocking_issues`; `needs-rework` requires at least one
non-empty issue. Any extra/missing key, malformed identifier, changed nested shape, altered source
fact, unlisted candidate path, failed first-parent admission, or claim that C8/publish/push/PR/
Human review completed fails closed.

## Acceptance / Stop Conditions

- The tracker marks C1–C7 complete using the four exact full commit identifiers above.
- The tracker leaves C8 as Planner Phase 4.5 pending and Human PR review pending.
- C0R changes exactly the declared three planning paths as C0's direct non-merge child; the
  pre-existing publish diff is preserved and `uv.lock` has no diff.
- The correction stops after C0R pending independent Plan-Reviewer evidence. It does not select a
  publish route or change the parent topic's implementation/publish contract.
