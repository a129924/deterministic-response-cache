---
topic: canonical-identity-pipeline
correction_id: canonical-identity-pipeline/pr-comment-review-and-fix-p8-p10-final-state-reconciliation
phase: correction-plan-review-pending
created: 2026-09-17
---

# PRCF1 P8–P10 final-state reconciliation correction plan

## Trigger and current truth

This Human-authorized planning-only candidate reconciles the parent and PRCF1 planning records to
the committed route facts. The recovery Plan-Reviewer receipt is
`b903cb06c2e174501228aab1325179fc1e13bc08`; Planner then completed P8 Phase 4.5; fresh P9
classification was committed unchanged as the sole P10 classification-evidence commit
`8a86e88621e00bbc10e773411cb10c6272b6fc45`. These are immutable facts.

`18d9b4751df26376c9cf47fe7968130870f07fe7` is superseded immutable nonrouting provenance. It
cannot be reused as P8, P9, P10, reply, or resolution authority. P11 is pending. This candidate
does not perform P11, classify a thread, reply, resolve, push, change a PR, approve, merge,
release, tag, or post-merge work.

## Locked scope and admission

The candidate must be a clean non-merge direct child of
`8a86e88621e00bbc10e773411cb10c6272b6fc45` and change exactly these eight paths in this order:

```text
M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md
M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.step.md
M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-plan.md
M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-step.md
M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p8-p10-route-recovery.correction-plan.md
M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p8-p10-route-recovery.correction-step.md
A\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p8-p10-final-state-reconciliation.correction-plan.md
A\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p8-p10-final-state-reconciliation.correction-step.md
```

All other paths are read-only, including code, tests, `uv.lock`, analysis/specification artifacts,
existing receipts and evidence, PR metadata, and threads. A dirty tree, a parent other than 8a86,
a merge commit, an unlisted path, changed `uv.lock`, a missing b903/P8/8a86 fact, an attempt to
reuse 18d, or any P11 action fails closed and returns to Planner.

## Evidence boundary and sole receipt

This correction creates no implementation subject, Tester evidence, implementation-review log,
classification, or reply/resolution evidence. Its sole conditional Plan-Reviewer receipt path is:

`plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p8-p10-final-state-reconciliation.correction-plan-review-log.json`

After this candidate is committed, Independent Plan-Reviewer alone may write that path. It must be
one JSON object with exactly the following top-level and nested keys; no earlier receipt or P9/P10
record may substitute for it:

```json
{
  "schema_version": "canonical-identity-pipeline.pr-comment-review-and-fix-p8-p10-final-state-reconciliation.correction-plan-review.v1",
  "topic": "canonical-identity-pipeline",
  "correction_id": "canonical-identity-pipeline/pr-comment-review-and-fix-p8-p10-final-state-reconciliation",
  "candidate_commit": "<40-hex reconciliation candidate>",
  "candidate_tree": "<40-hex reconciliation candidate tree>",
  "reviewed_paths": [
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.step.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-plan.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-step.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p8-p10-route-recovery.correction-plan.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p8-p10-route-recovery.correction-step.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p8-p10-final-state-reconciliation.correction-plan.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p8-p10-final-state-reconciliation.correction-step.md", "blob_sha": "<40-hex>"}
  ],
  "first_parent_admission": {
    "candidate_commit": "<same 40-hex candidate>",
    "candidate_tree": "<same 40-hex candidate tree>",
    "parent_commit": "8a86e88621e00bbc10e773411cb10c6272b6fc45",
    "non_merge": true,
    "first_parent": "8a86e88621e00bbc10e773411cb10c6272b6fc45",
    "exact_declared_paths": [
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.step.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-plan.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-step.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p8-p10-route-recovery.correction-plan.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p8-p10-route-recovery.correction-step.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p8-p10-final-state-reconciliation.correction-plan.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p8-p10-final-state-reconciliation.correction-step.md"
    ],
    "name_status": [
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.step.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-plan.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-step.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p8-p10-route-recovery.correction-plan.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p8-p10-route-recovery.correction-step.md",
      "A\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p8-p10-final-state-reconciliation.correction-plan.md",
      "A\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p8-p10-final-state-reconciliation.correction-step.md"
    ]
  },
  "review_basis": "clean committed eight-path final-state reconciliation tree; b903 recovery receipt; completed Planner P8; fresh P9/P10 commit 8a86; 18d superseded nonrouting provenance; P11 pending; unchanged nine-thread triage",
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "copilot_feedback_triage": {
    "ADDRESS": ["PRRC_kwDOUJTij87vvFvj", "PRRC_kwDOUJTij87vvFvo", "PRRC_kwDOUJTij87vvFvu", "PRRC_kwDOUJTij87vvF0O", "PRRC_kwDOUJTij87vvF0q", "PRRC_kwDOUJTij87vvF0_", "PRRC_kwDOUJTij87vvF1r"],
    "DISCUSS": [],
    "SKIP": ["PRRC_kwDOUJTij87vvFve", "PRRC_kwDOUJTij87vvF1V"]
  },
  "recorded_by": "Independent Plan-Reviewer"
}
```

`reviewed_paths` contains exactly the eight displayed path/blob objects in displayed order.
`exact_declared_paths` and `name_status` contain exactly the eight admission entries displayed
above in the same order; every SHA is lowercase 40-hex and each `name_status` value uses a literal
tab. `approved` requires an empty `blocking_issues` array; `needs-rework` requires at least one
non-empty blocker. The actual receipt preserves the unchanged seven ADDRESS and two `uv.lock` SKIP
node/comment pairs without classifying, replying to, or resolving them.

Only Independent Implementer may commit an unchanged approved receipt as a clean non-merge direct
child and exact one-path evidence-only commit. That possible later receipt commit only permits
Planner to route the bounded next role; it does not complete P11 or authorize any PR action.

## Stop conditions

No unlisted artifact, candidate selection, self-approval, P11 result, thread action, or Human-only
action is authorized. Missing required evidence or inconsistent state is `blocked`; candidate,
subject, worktree, or thread-identity conflict is `human-check`.
