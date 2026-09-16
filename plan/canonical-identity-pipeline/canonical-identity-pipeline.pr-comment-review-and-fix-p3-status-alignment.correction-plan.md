---
topic: canonical-identity-pipeline
correction_id: canonical-identity-pipeline/pr-comment-review-and-fix-p3-status-alignment
phase: correction-plan-review-pending
created: 2026-09-16
---

# PRCF1 P3 status-alignment correction plan

## Trigger and current truth

P2 status-sync candidate `fbdbe901a84630089e07792f15b79fb0e67b0861` and committed approved
receipt `4a4a99165cdc37a3bae6931e0fb2249ad5f0ab3a` are complete frozen facts. P3 is the completed
exact two-path implementation subject `b8c7cc6050b3c5a44333a1fde9d3ee07145966f5`.

P3 status-sync candidate `2e8fc3230805bf6a09239f8225585cb59d1d22a3` is superseded nonrouting
provenance: its untracked receipt was discarded before review, commit, consumption, or reuse. This
Human-authorized replacement synchronizes those facts, records the supersession, and keeps P4
pending. It creates only a fresh independent Plan-Reviewer gate; it does not write a receipt,
Tester evidence, Reviewer evidence, code, tests, `uv.lock`, PR metadata, or thread activity.

## Locked scope and admission

The candidate must be a clean non-merge direct child of
`2e8fc3230805bf6a09239f8225585cb59d1d22a3` and change exactly these eight planning paths:

```text
M	plan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md
M	plan/canonical-identity-pipeline/canonical-identity-pipeline.step.md
M	plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-plan.md
M	plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-step.md
M	plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-sync.correction-plan.md
M	plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-sync.correction-step.md
A	plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-alignment.correction-plan.md
A	plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-alignment.correction-step.md
```

Every other tracked path is read-only, including analysis/specification artifacts, code, tests,
existing evidence, diagrams, `README.md`, `pyproject.toml`, `uv.lock`, PR metadata, and threads.
No alignment candidate/tree/blob/review outcome or receipt is prefilled. An unlisted path, dirty
tree, non-direct or merge parent, altered `uv.lock`, or P4 completion claim fails closed.

## Alignment receipt contract

After this candidate is committed, Independent Plan-Reviewer may write only:

`plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-alignment.correction-plan-review-log.json`

The sole receipt is one JSON object with exactly these top-level keys:

```json
{
  "schema_version": "canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-alignment.correction-plan-review.v1",
  "topic": "canonical-identity-pipeline",
  "correction_id": "canonical-identity-pipeline/pr-comment-review-and-fix-p3-status-alignment",
  "candidate_commit": "<40-hex alignment candidate>",
  "candidate_tree": "<40-hex alignment candidate tree>",
  "reviewed_paths": [
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.step.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-plan.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-step.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-sync.correction-plan.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-sync.correction-step.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-alignment.correction-plan.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-alignment.correction-step.md", "blob_sha": "<40-hex>"}
  ],
  "first_parent_admission": {
    "candidate_commit": "<same 40-hex candidate>",
    "candidate_tree": "<same 40-hex candidate tree>",
    "parent_commit": "2e8fc3230805bf6a09239f8225585cb59d1d22a3",
    "non_merge": true,
    "first_parent": "2e8fc3230805bf6a09239f8225585cb59d1d22a3",
    "exact_declared_paths": [
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.step.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-plan.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-step.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-sync.correction-plan.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-sync.correction-step.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-alignment.correction-plan.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-alignment.correction-step.md"
    ],
    "name_status": [
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.step.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-plan.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-step.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-sync.correction-plan.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-sync.correction-step.md",
      "A\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-alignment.correction-plan.md",
      "A\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-alignment.correction-step.md"
    ]
  },
  "review_basis": "clean committed eight-path P3 status-alignment tree; committed P2 status-sync/P3 facts; superseded P3 status-sync provenance; P4 pending; unchanged PRCF1 scope and triage",
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

`reviewed_paths`, `exact_declared_paths`, and `name_status` each contain exactly the eight displayed
paths in the displayed order; `name_status` uses literal `M<TAB>path` or `A<TAB>path` entries.
Every SHA is lowercase 40-hex. `approved` requires empty `blocking_issues`; `needs-rework`
requires at least one non-empty blocker. The receipt retains the existing seven ADDRESS and two
SKIP IDs without classifying, replying to, or resolving a thread.

Only Independent Implementer may commit the unchanged approved receipt as a clean non-merge direct
child and exact one-path evidence-only commit. That commit restores Planner routing to P4 only; it
does not authorize P4 itself, testing, implementation review, classification, replies, resolution,
PR approval, merge, release, tag, or post-merge work.

## Stop conditions

Missing committed P2 status-sync/P3 facts, a recreated or reused P3 status-sync receipt, a
non-approved or separately uncommitted alignment receipt, candidate/evidence/subject conflict, or
an attempt to expand the eight paths is `blocked` and returns to Planner. Worktree or candidate
identity conflict is `human-check`. Human alone owns PR review, merge, release, tag, post-merge,
and final summary.
