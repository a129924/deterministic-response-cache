---
topic: canonical-identity-pipeline
correction_id: canonical-identity-pipeline/pr-comment-review-and-fix-p7-status-alignment-phase-repair
phase: correction-plan-review-pending
created: 2026-09-16
---

# PRCF1 P7 status-alignment phase-repair correction plan

## Trigger and current truth

P3 is the immutable exact two-path implementation subject
`b8c7cc6050b3c5a44333a1fde9d3ee07145966f5`. P4 passing factual evidence and its sole one-path
P5 evidence commit are both `dff14f3fdc0a06bf907ea82074e02862a05a36d1`. The P5 status-sync
candidate `7a604e27d5fc00089b9c00ebeec3a142bb5ea861` and its unchanged approved sole receipt
commit `ff19d0aeda3305e6bc743930827408122d18a55a` are complete frozen facts. P6's approved
implementation-review log is committed unchanged by P7 at
`24ef18b835b7646e05bf0fc3f5828349eea52b1d`.

P7 status-sync candidate `850c1e66f2d2dc339620ca86e03660f1faef9331` is rejected immutable
nonrouting provenance. Its uncommitted Plan-Reviewer outcome is not a receipt and is neither
committed, consumed, nor reusable. This Human-authorized phase-repair candidate corrects only the
active state and declares a new independent receipt route. P8 Phase 4.5 remains pending and
Planner-only; P9–P11 have not started. It creates no alignment result, classification, reply,
resolution, push, PR, approval, merge, release, tag, or post-merge outcome.

## Locked scope and admission

The candidate must be a clean non-merge direct child of
`850c1e66f2d2dc339620ca86e03660f1faef9331` and change exactly these eight planning paths:

```text
M	plan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md
M	plan/canonical-identity-pipeline/canonical-identity-pipeline.step.md
M	plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-plan.md
M	plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-step.md
M	plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-sync.correction-plan.md
M	plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-sync.correction-step.md
A	plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-alignment-phase-repair.correction-plan.md
A	plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-alignment-phase-repair.correction-step.md
```

Every other tracked path is read-only, including analysis/specification artifacts, code, tests,
existing evidence, diagrams, `README.md`, `pyproject.toml`, `uv.lock`, PR metadata, and threads.
This candidate creates no receipt. A dirty tree, merge or non-direct parent, unlisted path,
altered `uv.lock`, missing P5S/P6/P7 fact, reused P7 status-sync outcome, or P8 completion claim
fails closed.

## P7 status-alignment phase-repair receipt contract

After this candidate is committed, Independent Plan-Reviewer may write only:

`plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-alignment-phase-repair.correction-plan-review-log.json`

The sole receipt is one JSON object with exactly these top-level keys and no others:

```json
{
  "schema_version": "canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-alignment-phase-repair.correction-plan-review.v1",
  "topic": "canonical-identity-pipeline",
  "correction_id": "canonical-identity-pipeline/pr-comment-review-and-fix-p7-status-alignment-phase-repair",
  "candidate_commit": "<40-hex phase-repair candidate>",
  "candidate_tree": "<40-hex phase-repair candidate tree>",
  "reviewed_paths": [
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.step.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-plan.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-step.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-sync.correction-plan.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-sync.correction-step.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-alignment-phase-repair.correction-plan.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-alignment-phase-repair.correction-step.md", "blob_sha": "<40-hex>"}
  ],
  "first_parent_admission": {
    "candidate_commit": "<same 40-hex candidate>",
    "candidate_tree": "<same 40-hex candidate tree>",
    "parent_commit": "850c1e66f2d2dc339620ca86e03660f1faef9331",
    "non_merge": true,
    "first_parent": "850c1e66f2d2dc339620ca86e03660f1faef9331",
    "exact_declared_paths": [
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.step.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-plan.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-step.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-sync.correction-plan.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-sync.correction-step.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-alignment-phase-repair.correction-plan.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-alignment-phase-repair.correction-step.md"
    ],
    "name_status": [
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.step.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-plan.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-step.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-sync.correction-plan.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-sync.correction-step.md",
      "A\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-alignment-phase-repair.correction-plan.md",
      "A\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-alignment-phase-repair.correction-step.md"
    ]
  },
  "review_basis": "clean committed eight-path P7 status-alignment phase-repair tree; committed P5S/P6/P7 facts; rejected 850 P7 status-sync provenance and no receipt reuse; P8 pending and Planner-only; unchanged PRCF1 scope and nine-thread triage",
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "copilot_feedback_triage": {
    "ADDRESS": [
      "PRRC_kwDOUJTij87vvFvj",
      "PRRC_kwDOUJTij87vvFvo",
      "PRRC_kwDOUJTij87vvFvu",
      "PRRC_kwDOUJTij87vvF0O",
      "PRRC_kwDOUJTij87vvF0q",
      "PRRC_kwDOUJTij87vvF0_",
      "PRRC_kwDOUJTij87vvF1r"
    ],
    "DISCUSS": [],
    "SKIP": ["PRRC_kwDOUJTij87vvFve", "PRRC_kwDOUJTij87vvF1V"]
  },
  "recorded_by": "Independent Plan-Reviewer"
}
```

`reviewed_paths`, `exact_declared_paths`, and `name_status` each contain exactly the displayed
eight paths in the displayed order; reviewed-path pairs contain only `path` and `blob_sha`; and
`name_status` uses literal `M<TAB>path` or `A<TAB>path`. Every SHA is lowercase 40-hex.
`approved` requires empty `blocking_issues`; `needs-rework` requires at least one non-empty
blocker. The receipt preserves the seven ADDRESS and two SKIP identifiers without classifying,
replying to, or resolving a thread.

Only Independent Implementer may commit an unchanged approved receipt as a clean non-merge direct
child and exact one-path evidence-only commit. That commit restores Planner routing to P8 only; it
does not authorize P8 itself, classification, replies, resolution, PR approval, merge, release,
tag, or post-merge work.

## Stop conditions

Missing committed P5S/P6/P7 facts; a reused or pre-created receipt; a non-approved or separately
uncommitted repair receipt; candidate/evidence/subject conflict; or an attempt to expand the eight
paths is `blocked` and returns to Planner. Worktree or candidate identity conflict is
`human-check`. Human alone owns PR review, merge, release, tag, post-merge, and final summary.
