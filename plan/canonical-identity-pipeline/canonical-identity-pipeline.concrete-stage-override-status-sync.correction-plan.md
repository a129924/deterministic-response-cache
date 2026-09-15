---
topic: canonical-identity-pipeline
correction_id: canonical-identity-pipeline/concrete-stage-override-status-sync
kind: status-synchronization
created: 2026-09-15
---

# C0S-R1 — CSO1 committed-status synchronization review-contract repair plan

## Purpose

Human explicitly authorized this status-only revision after C0S was rejected: its C1S JSON source
encoded each `name_status` separator as `\\t`, so parsing produced a literal backslash-plus-`t`
rather than Git's actual tab separator. C0S-R1 repairs that review contract and retains the already
committed CSO1 facts. It neither changes the canonical identity pipeline nor reopens,
reinterprets, or substitutes historical evidence.

## Frozen source facts

| CSO1 step | Frozen fact |
| --- | --- |
| C0 | Immutable six-path candidate `82bb4413f0f53e912b4cf30abb65b5a13c84a93a`, tree `e2e4c638b74205b7cb158e1c8f92e592970a03bb`. |
| C1 | Approved independent Plan-Reviewer log at `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-plan-review-log.json`; it binds C0, the stated tree, six reviewed path/blob facts, empty blockers, and empty Copilot triage. |
| C2 | Immutable sole-evidence commit `15c23d67856b627fa8f736eb66694cccc9e5ec89`, a non-merge direct child of C0 whose exact one-path diff adds the unchanged C1 log. |
| C3 | Pending only; no C3 implementation subject, Tester evidence, Reviewer evidence, Phase 4.5 alignment, push, or PR completion exists. |

C0/C1/C2 and their underlying evidence are immutable. C0S is rejected frozen provenance: no C1S
log was written for it. C0S-R1 may describe these facts and the rejection cause, but may not modify
their paths or claim a new outcome for them.

## Exact candidate scope and lineage

`46b707c209839f64935beb08e4db8a1b565c8114` is C0S, the rejected six-path predecessor. Its C1S
schema used double-escaped tab text and therefore cannot be reviewed or routed. It is frozen,
non-routing provenance; no C1S log was written for it.

C0S-R1 is one non-merge direct child of C0S. Its sole first parent is
`46b707c209839f64935beb08e4db8a1b565c8114` and its complete first-parent name-status diff
contains exactly the following six entries in lexical path order:

```text
M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-status-sync.correction-plan.md
M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-status-sync.correction-step.md
M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-plan.md
M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-step.md
M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md
M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.step.md
```

The six paths are C0S-R1's complete scope. Their only allowed change is to synchronize C0/C1/C2 as
frozen complete, C0S as rejected, C0S-R1 as review pending, C3 as the sole pending execution step,
and C4–C8 as not started. C0S-R1 must not write its review log, alter the C1 log, or change
analysis, technical spec, parent spec, code, tests, diagrams, exports, README, `pyproject.toml`,
`uv.lock`, publish state, or draft PR #6.

Before C0S-R1 is committed, no artifact may contain its commit/tree/blob SHA or a C1S verdict.
C0S-R1 is the sole candidate C1S may review. It has no Tester or independent implementation-Reviewer
phase because it creates no implementation subject.

## Evidence route

| Order | Artifact / action | Exact path | Sole writer or actor | Condition |
| --- | --- | --- | --- | --- |
| C0S-R1 | Revised status-sync candidate | the six paths above | Plan-Creator | Commit only the exact six paths as the non-merge direct child of rejected C0S; do not write C1S or select C3. |
| C1S | Correction Plan-Reviewer log | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-status-sync.correction-plan-review-log.json` | Independent Plan-Reviewer | From a clean committed C0S-R1 checkout, write only the exact JSON object defined below. |
| C2S | Committed C1S evidence | same C1S path | Independent Implementer | Commit unchanged approved C1S evidence as the sole evidence-only commit. |
| C3 | Existing CSO1 execution route | `src/deterministic_response_cache/identity/canonical.py`, `tests/test_canonical_identity_pipeline.py` | Planner, then Implementer if routed | Planner independently routes the still-pending C3 only after C2S; C0S-R1 gives no implementation, publish, push, or PR authority. |

`needs-rework` at C1S returns to Planner. C0S-R1 cannot self-close, cannot provide C3 Tester or
Reviewer evidence, and cannot satisfy Phase 4.5. C0S-R1 artifacts remain historical status-sync
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

The reviewer must fail closed and must not produce C1S if the candidate is uncommitted or dirty,
does not have rejected C0S as its direct non-merge first parent, has any path outside the declared
six, does not parse every `name_status` string to one `M`, one actual tab, and its exact path,
contains a malformed schema, disagrees about frozen C1/C2 facts, C0S rejection, C0S-R1 review
pending, or C3 pending state, preclaims a C0S-R1 post-commit fact, or asserts implementation,
Tester, Reviewer, Phase 4.5, push, PR, or Human review completion. Only an Independent Implementer
may commit an unchanged approved C1S log.

## Acceptance and closure

- C0S-R1's exact six-path direct-child admission is independently verifiable from committed Git facts.
- All four state surfaces consistently expose frozen C0/C1/C2, rejected C0S, C0S-R1 review pending,
  C3 pending, and C4–C8 not started; none claims a C3 subject or later evidence exists.
- `uv.lock` has no diff and no non-C0S-R1 path is staged or committed.
- C0S-R1 stops after committed approved C1S evidence and an independent Planner route decision. It
  never replaces CSO1's later Tester, Reviewer, Phase 4.5, push, or Human-review gates.
