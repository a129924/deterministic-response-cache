---
topic: canonical-identity-pipeline
correction_id: canonical-identity-pipeline/pr-comment-review-and-fix-p5-status-sync
phase: correction-plan-review-pending
created: 2026-09-16
---

# PRCF1 P5 status-sync correction plan

## Trigger and current truth

P3 is the immutable exact two-path implementation subject
`b8c7cc6050b3c5a44333a1fde9d3ee07145966f5`. The rejected P3 status-alignment candidate
`d430493b068608171043a7794d86c549bfc8b6fc` and its absent receipt are immutable nonrouting
provenance. The follow-up phase-repair candidate
`90fc41117b6ff9969c2ea9161d0952b2814b597d` and its committed unchanged approved receipt
`c1751ac832c6b08f2173e1d51627f70cad0e0ca3` are complete frozen facts.

Tester then wrote factual passing P4 evidence for that same P3 subject, and Independent
Implementer committed it unchanged as sole one-path P5 evidence-only commit
`dff14f3fdc0a06bf907ea82074e02862a05a36d1`. This Human-authorized status-sync candidate records
those committed facts only. P6 is pending and may consume only P5 evidence committed at
`dff14f3fdc0a06bf907ea82074e02862a05a36d1`; P7–P11 are not started. It creates no P6 review
log, classification, reply, resolution, push, PR, approval, merge, release, tag, or post-merge
outcome.

## Locked scope and admission

The candidate must be a clean non-merge direct child of
`dff14f3fdc0a06bf907ea82074e02862a05a36d1` and change exactly these eight planning paths:

```text
M	plan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md
M	plan/canonical-identity-pipeline/canonical-identity-pipeline.step.md
M	plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-plan.md
M	plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-step.md
M	plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-alignment-phase-repair.correction-plan.md
M	plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-alignment-phase-repair.correction-step.md
A	plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p5-status-sync.correction-plan.md
A	plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p5-status-sync.correction-step.md
```

Every other tracked path is read-only, including analysis/specification artifacts, code, tests,
existing evidence, diagrams, `README.md`, `pyproject.toml`, `uv.lock`, PR metadata, and threads.
This candidate creates no receipt. A dirty tree, merge or non-direct parent, unlisted path,
altered `uv.lock`, missing P3/phase-repair/P4/P5 fact, or P6 completion claim fails closed.

## P5 status-sync receipt contract

After this candidate is committed, Independent Plan-Reviewer may write only:

`plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p5-status-sync.correction-plan-review-log.json`

The sole receipt is one JSON object with exactly these top-level keys:

```json
{
  "schema_version": "canonical-identity-pipeline.pr-comment-review-and-fix-p5-status-sync.correction-plan-review.v1",
  "topic": "canonical-identity-pipeline",
  "correction_id": "canonical-identity-pipeline/pr-comment-review-and-fix-p5-status-sync",
  "candidate_commit": "<40-hex P5 status-sync candidate>",
  "candidate_tree": "<40-hex P5 status-sync candidate tree>",
  "reviewed_paths": [
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.step.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-plan.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-step.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-alignment-phase-repair.correction-plan.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-alignment-phase-repair.correction-step.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p5-status-sync.correction-plan.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p5-status-sync.correction-step.md", "blob_sha": "<40-hex>"}
  ],
  "first_parent_admission": {
    "candidate_commit": "<same 40-hex candidate>",
    "candidate_tree": "<same 40-hex candidate tree>",
    "parent_commit": "dff14f3fdc0a06bf907ea82074e02862a05a36d1",
    "non_merge": true,
    "first_parent": "dff14f3fdc0a06bf907ea82074e02862a05a36d1",
    "exact_declared_paths": [
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.step.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-plan.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-step.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-alignment-phase-repair.correction-plan.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-alignment-phase-repair.correction-step.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p5-status-sync.correction-plan.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p5-status-sync.correction-step.md"
    ],
    "name_status": [
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.step.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-plan.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-step.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-alignment-phase-repair.correction-plan.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-alignment-phase-repair.correction-step.md",
      "A\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p5-status-sync.correction-plan.md",
      "A\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p5-status-sync.correction-step.md"
    ]
  },
  "review_basis": "clean committed eight-path P5 status-sync tree; committed P3, phase-repair, P4 and P5 facts; P6 pending on dff14f3fdc0a06bf907ea82074e02862a05a36d1; unchanged PRCF1 scope and nine-thread triage",
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

`reviewed_paths`, `exact_declared_paths`, and `name_status` each contain exactly the eight
displayed paths in the displayed order; `name_status` uses literal `M<TAB>path` or `A<TAB>path`
entries. Every SHA is lowercase 40-hex. `approved` requires empty `blocking_issues`;
`needs-rework` requires at least one non-empty blocker. The receipt preserves the seven ADDRESS
and two SKIP identifiers without classifying, replying to, or resolving a thread.

Only Independent Implementer may commit an unchanged approved receipt as a clean non-merge direct
child and exact one-path evidence-only commit. That commit restores Planner routing to P6 only; it
does not authorize P6 itself, implementation review, classification, replies, resolution, PR
approval, merge, release, tag, or post-merge work.

## Stop conditions

Missing committed P3, phase-repair, P4, or P5 facts; a reused or pre-created receipt; a
non-approved or separately uncommitted P5 status-sync receipt; candidate/evidence/subject conflict;
or an attempt to expand the eight paths is `blocked` and returns to Planner. Worktree or candidate
identity conflict is `human-check`. Human alone owns PR review, merge, release, tag, post-merge,
and final summary.
