---
topic: canonical-identity-pipeline
correction_id: canonical-identity-pipeline/pr-comment-review-and-fix-p3-status-alignment
phase: rejected-provenance
created: 2026-09-16
---

# PRCF1 P3 status-alignment correction plan

## Trigger and current truth

P2 status-sync candidate `fbdbe901a84630089e07792f15b79fb0e67b0861` and committed approved
receipt `4a4a99165cdc37a3bae6931e0fb2249ad5f0ab3a` are complete frozen facts. P3 is the completed
exact two-path implementation subject `b8c7cc6050b3c5a44333a1fde9d3ee07145966f5`.

P3 status-sync candidate `2e8fc3230805bf6a09239f8225585cb59d1d22a3` is superseded nonrouting
provenance: its untracked receipt was discarded before review, commit, consumption, or reuse.
This candidate is rejected immutable nonrouting provenance at
`d430493b068608171043a7794d86c549bfc8b6fc`: independent Plan-Reviewer review found only that
the PRCF1 correction-plan frontmatter still declared `p2-status-sync-review-pending`. No receipt
from this rejected candidate is committed, consumed, or reusable. The separate phase-repair route
corrects that stale phase, records this rejection, and keeps P4 pending.

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

## Rejected receipt contract

The declared receipt path is historical only and has no usable committed content:

`plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-alignment.correction-plan-review-log.json`

No actor may create, commit, consume, or reuse an alignment receipt from this rejected candidate.
The following former schema is retained solely to identify the rejected route:

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

No receipt from this route can restore Planner routing to P4 or authorize testing, implementation
review, classification, replies, resolution, PR approval, merge, release, tag, or post-merge work.

## Stop conditions

This rejected record cannot be revived, corrected in place, or used to recreate its receipt.
Missing committed P2 status-sync/P3 facts, any reuse of P3 status-sync or alignment receipt,
candidate/evidence/subject conflict, or an attempt to expand the separate phase-repair route is
`blocked` and returns to Planner. Worktree or candidate identity conflict is `human-check`. Human
alone owns PR review, merge, release, tag, post-merge, and final summary.
