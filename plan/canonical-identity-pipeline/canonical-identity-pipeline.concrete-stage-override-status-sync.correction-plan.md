---
topic: canonical-identity-pipeline
correction_id: canonical-identity-pipeline/concrete-stage-override-status-sync
kind: status-synchronization
created: 2026-09-15
---

# C0S — CSO1 committed-status synchronization correction plan

## Purpose

Human explicitly authorized this status-only correction to make the four CSO1 state surfaces agree
with already-committed facts. It records C1 and C2 as complete and leaves C3 pending. It neither
changes the canonical identity pipeline nor reopens, reinterprets, or substitutes any historical
evidence.

## Frozen source facts

| CSO1 step | Frozen fact |
| --- | --- |
| C0 | Immutable six-path candidate `82bb4413f0f53e912b4cf30abb65b5a13c84a93a`, tree `e2e4c638b74205b7cb158e1c8f92e592970a03bb`. |
| C1 | Approved independent Plan-Reviewer log at `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-plan-review-log.json`; it binds C0, the stated tree, six reviewed path/blob facts, empty blockers, and empty Copilot triage. |
| C2 | Immutable sole-evidence commit `15c23d67856b627fa8f736eb66694cccc9e5ec89`, a non-merge direct child of C0 whose exact one-path diff adds the unchanged C1 log. |
| C3 | Pending only; no C3 implementation subject, Tester evidence, Reviewer evidence, Phase 4.5 alignment, push, or PR completion exists. |

C0/C1/C2 and their underlying evidence are immutable. C0S may describe these facts but may not
modify their paths or claim a new outcome for them.

## Exact candidate scope and lineage

C0S is one non-merge direct child of C2
`15c23d67856b627fa8f736eb66694cccc9e5ec89`. Its sole first parent is C2 and its complete
first-parent name-status diff contains exactly the following six entries in lexical path order:

```text
A\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-status-sync.correction-plan.md
A\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-status-sync.correction-step.md
M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-plan.md
M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-step.md
M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md
M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.step.md
```

The six paths are the candidate's complete scope. Their only allowed change is to synchronize C0,
C1, C2, C3, and C4–C8 state wording; parent plan/step and CSO1 plan/step must all say that C1/C2
are complete, C3 is the sole pending execution step, and C4–C8 are not started. C0S must not write
its review log, alter the C1 log, or change analysis, technical spec, parent spec, code, tests,
diagrams, exports, README, `pyproject.toml`, `uv.lock`, publish state, or draft PR #6.

Before C0S is committed, no artifact may contain its commit/tree/blob SHA or a C1S verdict. C0S is
the sole candidate C1S may review. It has no Tester or independent implementation-Reviewer phase
because it creates no implementation subject.

## Evidence route

| Order | Artifact / action | Exact path | Sole writer or actor | Condition |
| --- | --- | --- | --- | --- |
| C0S | Status-sync candidate | the six paths above | Plan-Creator | Commit only the exact six paths as the non-merge direct child of C2; do not write C1S or select C3. |
| C1S | Correction Plan-Reviewer log | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-status-sync.correction-plan-review-log.json` | Independent Plan-Reviewer | From a clean committed C0S checkout, write only the exact JSON object defined below. |
| C2S | Committed C1S evidence | same C1S path | Independent Implementer | Commit unchanged approved C1S evidence as the sole evidence-only commit. |
| C3 | Existing CSO1 execution route | `src/deterministic_response_cache/identity/canonical.py`, `tests/test_canonical_identity_pipeline.py` | Planner, then Implementer if routed | Planner independently routes the still-pending C3 only after C2S; C0S gives no implementation, publish, push, or PR authority. |

`needs-rework` at C1S returns to Planner. C0S cannot self-close, cannot provide C3 Tester or
Reviewer evidence, and cannot satisfy Phase 4.5. C0S artifacts remain historical status-sync
provenance after C2S; the four parent/CSO1 state surfaces become current truth only after that
approved evidence-only commit.

## C1S review-log contract

C1S is one JSON object with exactly these twelve top-level keys and no others:
`schema_version`, `topic`, `correction_id`, `candidate_commit`, `candidate_tree`, `reviewed_paths`,
`first_parent_admission`, `review_basis`, `verdict`, `blocking_issues`,
`copilot_feedback_triage`, and `recorded_by`.

`candidate_commit`, `candidate_tree`, and every `blob_sha` are lowercase 40-hex Git object IDs.
`reviewed_paths` has exactly the following six ordered entries, each containing only `path` and
`blob_sha`. `first_parent_admission` has exactly `candidate_commit`, `candidate_tree`,
`parent_commit`, `non_merge`, `first_parent`, `exact_declared_paths`, and `name_status`; its
candidate values equal the top-level values, its parent is the exact C2 SHA, all three boolean
flags are `true`, and its `name_status` is the exact six-entry array below. `review_basis` must
equal the literal below. `copilot_feedback_triage` has exactly `ADDRESS`, `DISCUSS`, and `SKIP`,
each an array. `approved` requires `blocking_issues: []`; `needs-rework` requires at least one
non-empty issue.

```json
{
  "schema_version": "canonical-identity-pipeline.concrete-stage-override-status-sync.correction-plan-review.v1",
  "topic": "canonical-identity-pipeline",
  "correction_id": "canonical-identity-pipeline/concrete-stage-override-status-sync",
  "candidate_commit": "<40-hex C0S commit>",
  "candidate_tree": "<40-hex C0S tree>",
  "reviewed_paths": [
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-status-sync.correction-plan.md", "blob_sha": "<40-hex C0S blob>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-status-sync.correction-step.md", "blob_sha": "<40-hex C0S blob>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-plan.md", "blob_sha": "<40-hex C0S blob>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-step.md", "blob_sha": "<40-hex C0S blob>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md", "blob_sha": "<40-hex C0S blob>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.step.md", "blob_sha": "<40-hex C0S blob>"}
  ],
  "first_parent_admission": {
    "candidate_commit": "<same 40-hex C0S commit>",
    "candidate_tree": "<same 40-hex C0S tree>",
    "parent_commit": "15c23d67856b627fa8f736eb66694cccc9e5ec89",
    "non_merge": true,
    "first_parent": true,
    "exact_declared_paths": true,
    "name_status": [
      "A\\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-status-sync.correction-plan.md",
      "A\\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-status-sync.correction-step.md",
      "M\\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-plan.md",
      "M\\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-step.md",
      "M\\tplan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md",
      "M\\tplan/canonical-identity-pipeline/canonical-identity-pipeline.step.md"
    ]
  },
  "review_basis": "clean committed C0S candidate checkout; direct non-merge first-parent admission from CSO1 C2 15c23d67856b627fa8f736eb66694cccc9e5ec89; four state surfaces agree on frozen C0/C1/C2 facts, C1/C2 complete, C3 pending, and C4-C8 not started; no implementation, Tester, Reviewer, publish, push, PR, or Human review claim",
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "copilot_feedback_triage": {"ADDRESS": [], "DISCUSS": [], "SKIP": []},
  "recorded_by": "Independent Plan-Reviewer"
}
```

The reviewer must fail closed and must not produce C1S if the candidate is uncommitted or dirty,
does not have C2 as its direct non-merge first parent, has any path outside the declared six,
contains a malformed schema, disagrees about frozen C1/C2 facts or C3 pending state, preclaims a
C0S post-commit fact, or asserts implementation, Tester, Reviewer, Phase 4.5, push, PR, or Human
review completion. Only an Independent Implementer may commit an unchanged approved C1S log.

## Acceptance and closure

- C0S's exact six-path direct-child admission is independently verifiable from committed Git facts.
- All four state surfaces consistently expose the frozen C1/C2 facts, C3 pending, and C4–C8 not
  started; none claims a C3 subject or later evidence exists.
- `uv.lock` has no diff and no non-C0S path is staged or committed.
- C0S stops after committed approved C1S evidence and an independent Planner route decision. It
  never replaces CSO1's later Tester, Reviewer, Phase 4.5, push, or Human-review gates.
