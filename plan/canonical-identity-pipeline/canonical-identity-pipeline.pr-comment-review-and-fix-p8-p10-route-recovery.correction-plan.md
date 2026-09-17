---
topic: canonical-identity-pipeline
correction_id: canonical-identity-pipeline/pr-comment-review-and-fix-p8-p10-route-recovery
phase: correction-plan-review-pending
created: 2026-09-17
---

# PRCF1 P8–P10 route-recovery correction plan

## Trigger and current truth

PRCF1 P3 is the immutable two-path subject
`b8c7cc6050b3c5a44333a1fde9d3ee07145966f5`; its factual passing P4 evidence and sole P5
evidence-only commit are both `dff14f3fdc0a06bf907ea82074e02862a05a36d1`. Independent Reviewer's
approved P6 evidence was committed unchanged as sole P7 evidence at
`24ef18b835b7646e05bf0fc3f5828349eea52b1`. This P3 → P5 → P7 full-SHA chain is immutable and
must be preserved exactly; no CAVO1, CSO1, rejected P7 status-sync, or other topic evidence may
substitute for it.

P7 status-sync candidate `850c1e66f2d2dc339620ca86e03660f1faef9331` remains rejected immutable
nonrouting provenance. P7 status-alignment phase-repair candidate
`87eb3de65d6b5a4efaef745d23e5d6cc34c70c59` and its approved sole receipt commit
`40824056def6c9d3402e95039af6a931b67ee547` are complete frozen facts. The later clean
eight-path P7 receipt-status-sync candidate `8ac6bd76ff85d04c16407518105dc023180871ef` and its
approved sole receipt commit `49c0bcd197c6b9ac4fb1baba115c903060ff52cf` are complete frozen
facts. `49c` records the completed P7 receipt; it made Planner P8 the next action but did not
perform P8.

The direct child `18d9b4751df26376c9cf47fe7968130870f07fe7` has a structurally correct one-path
thread-classification payload, but it was committed before Planner performed P8. It is therefore
immutable nonrouting provenance. It establishes neither P8 nor P10, cannot be used to reply to or
resolve a thread, and is **not yet superseded**. It becomes superseded only after the fresh P9
classification below is committed as the fresh sole P10 evidence commit.

This Human-authorized recovery candidate repairs routing only. It creates no receipt, P8 outcome,
thread classification, P10 commit, reply, resolution, code/test change, `uv.lock` change, push,
PR action, approval, merge, release, tag, or post-merge outcome.

## Locked scope and admission

The candidate must be a clean, non-merge direct child of
`18d9b4751df26376c9cf47fe7968130870f07fe7` and change exactly these ten paths in this order:

```text
M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md
M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.step.md
M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-plan.md
M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-step.md
M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-alignment-phase-repair.correction-plan.md
M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-alignment-phase-repair.correction-step.md
M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-alignment-receipt-status-sync.correction-plan.md
M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-alignment-receipt-status-sync.correction-step.md
A\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p8-p10-route-recovery.correction-plan.md
A\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p8-p10-route-recovery.correction-step.md
```

All other tracked paths are read-only, including the historical 18d classification JSON, all
existing receipts/evidence, analysis/specification files, code, tests, diagrams, `README.md`,
`pyproject.toml`, `uv.lock`, PR metadata, and threads. A dirty tree, wrong or merge parent,
unlisted path, altered `uv.lock`, missing P3/P5/P7 chain, missing 49c receipt fact, receipt created
in this candidate, or P8/P9/P10 completion claim fails closed.

## Evidence boundary

This recovery declares no new implementation subject, Tester evidence, or implementation-review
log. Its only new correction lifecycle artifacts are this correction plan, this correction step,
and the sole route-recovery Plan-Reviewer receipt. The existing exact evidence paths remain
read-only completed facts: Tester owns
`plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-tester-evidence.json`
for P4/P5, while Independent Reviewer owns
`plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-implementation-review-log.json`
for P6/P7. Their schemas and the P3/P5/P7 binding are authoritative in the parent PRCF1
correction plan; neither may be regenerated or rewritten by this route. The recovery receipt is
reviewer-controlled routing evidence, and fresh P9/P10 is a later classification-only sequence.

## Sole route-recovery Plan-Reviewer receipt

After this candidate is committed, Independent Plan-Reviewer may write only:

`plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p8-p10-route-recovery.correction-plan-review-log.json`

This is the sole receipt for this recovery route. It is one JSON object with exactly these
top-level and nested keys; no earlier P7 receipt or 18d record may be reused as this receipt:

```json
{
  "schema_version": "canonical-identity-pipeline.pr-comment-review-and-fix-p8-p10-route-recovery.correction-plan-review.v1",
  "topic": "canonical-identity-pipeline",
  "correction_id": "canonical-identity-pipeline/pr-comment-review-and-fix-p8-p10-route-recovery",
  "candidate_commit": "<40-hex recovery candidate>",
  "candidate_tree": "<40-hex recovery candidate tree>",
  "reviewed_paths": [
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.step.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-plan.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-step.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-alignment-phase-repair.correction-plan.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-alignment-phase-repair.correction-step.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-alignment-receipt-status-sync.correction-plan.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-alignment-receipt-status-sync.correction-step.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p8-p10-route-recovery.correction-plan.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p8-p10-route-recovery.correction-step.md", "blob_sha": "<40-hex>"}
  ],
  "first_parent_admission": {
    "candidate_commit": "<same 40-hex candidate>",
    "candidate_tree": "<same 40-hex candidate tree>",
    "parent_commit": "18d9b4751df26376c9cf47fe7968130870f07fe7",
    "non_merge": true,
    "first_parent": "18d9b4751df26376c9cf47fe7968130870f07fe7",
    "exact_declared_paths": [
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.step.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-plan.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-step.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-alignment-phase-repair.correction-plan.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-alignment-phase-repair.correction-step.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-alignment-receipt-status-sync.correction-plan.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-alignment-receipt-status-sync.correction-step.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p8-p10-route-recovery.correction-plan.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p8-p10-route-recovery.correction-step.md"
    ],
    "name_status": [
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.step.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-plan.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-step.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-alignment-phase-repair.correction-plan.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-alignment-phase-repair.correction-step.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-alignment-receipt-status-sync.correction-plan.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-alignment-receipt-status-sync.correction-step.md",
      "A\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p8-p10-route-recovery.correction-plan.md",
      "A\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p8-p10-route-recovery.correction-step.md"
    ]
  },
  "review_basis": "clean committed ten-path P8-P10 route-recovery tree; committed 49c P7 receipt; immutable same-subject P3/P5/P7 chain; 18d structural pre-P8 nonrouting provenance; fresh P8 then P9/P10 required; unchanged nine-thread triage",
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

`reviewed_paths`, `exact_declared_paths`, and `name_status` must contain exactly the displayed ten
entries in displayed order. Each reviewed-path object contains only `path` and `blob_sha`; each SHA
is lowercase 40-hex; `name_status` uses a literal tab. `approved` requires an empty
`blocking_issues` array, while `needs-rework` requires at least one non-empty blocker. The receipt
preserves the seven ADDRESS and two SKIP identifiers without classifying, replying to, or resolving
a thread.

Only Independent Implementer may commit the unchanged approved receipt as a clean non-merge direct
child and exact one-path evidence-only commit. That receipt commit does not perform P8 or create a
classification result; it permits Planner, and only Planner, to redo P8.

## P8, fresh P9, and fresh P10 route

After the recovery receipt is committed, Planner redoes P8 Phase 4.5 using the existing Human
authorization and the unchanged P3/P5/P7 full-SHA chain. P8 authorizes fresh classification only;
it never authorizes PR approval, merge, release, tag, post-merge, reply, or resolution.

Only after that redone P8 may Independent Reviewer write the fresh P9 record:

`plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p8-p10-route-recovery.thread-classification.json`

It is a single JSON object with exactly `schema_version`, `topic`, `correction_id`,
`pull_request`, `implementation_subject_commit`, `tester_evidence_commit`,
`implementation_review_commit`, `threads`, and `recorded_by`. It binds PR #6, P3, P5, P7, and all
nine existing node/comment pairs; `schema_version` is
`canonical-identity-pipeline.pr-comment-review-and-fix-p8-p10-route-recovery.thread-classification.v1`,
its `correction_id` is
`canonical-identity-pipeline/pr-comment-review-and-fix-p8-p10-route-recovery`, and its
`recorded_by` is `Independent Reviewer`. Each thread has exactly `node_id`, `comment_id`,
`classification`, and `reason`; classification is exactly `addressed-and-resolvable` or
`skip-not-resolvable`, and `reason` is non-empty factual text. The seven ADDRESS and two SKIP
identifiers remain unchanged and in their declared order.

Only Independent Implementer may commit that unchanged fresh P9 JSON as the sole one-path P10
classification-evidence commit. Only after that fresh P10 commit is present does
`18d9b4751df26376c9cf47fe7968130870f07fe7` become superseded immutable nonrouting provenance.
Until then, its status remains pre-P8 immutable nonrouting provenance, not superseded. A fresh P10
commit still grants no PR approval, merge, release, tag, post-merge, reply, or resolution action.

## Stop conditions

Missing or mismatched P3/P5/P7 evidence, missing 49c receipt fact, a reused receipt, a
pre-created receipt or classification, a non-approved or separately uncommitted receipt, wrong
parent, merge commit, unlisted path, `uv.lock` change, consumed 18d classification, or P8/P9/P10
completion claim in this candidate is `blocked` and returns to Planner. Candidate, evidence,
subject, worktree, or thread-identity conflict is `human-check`. Human alone owns PR review,
merge, release, tag, post-merge, and final summary.
