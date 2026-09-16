---
topic: canonical-identity-pipeline
correction_id: canonical-identity-pipeline/pr-comment-review-and-fix-p3-status-sync
phase: correction-plan-review-pending
created: 2026-09-16
---

# PRCF1 P3 status synchronization correction plan

## Trigger and current truth

PRCF1 P0 is the clean ten-path candidate `bbf3bde597b1adbf074ef832802a6151c330752a`; its approved
P1 receipt was committed unchanged by Independent Implementer as sole P2 evidence at
`618be901c8313447b88e9fec513dea6beb59e534`. The P2 status-sync candidate
`fbdbe901a84630089e07792f15b79fb0e67b0861` and its committed approved one-path receipt
`4a4a99165cdc37a3bae6931e0fb2249ad5f0ab3a` are complete frozen facts.

P3 is the clean non-merge exact two-path implementation subject
`b8c7cc6050b3c5a44333a1fde9d3ee07145966f5`, direct child of the committed P2 status-sync receipt.
It changes only `src/deterministic_response_cache/identity/canonical.py` and
`tests/test_canonical_identity_pipeline.py`. This Human-authorized correction only synchronizes
those committed P2 status-sync/P3 facts, keeps P4 pending, and creates the route for independent
review of this eight-path planning candidate. It does not write a P3 status-sync receipt, Tester
evidence, or Reviewer evidence; modify code, tests, or `uv.lock`; touch PR #6; reply to or resolve
a thread; publish, merge, release, tag, or perform post-merge work.

## Locked scope and admission

This candidate must be a clean non-merge direct child of
`b8c7cc6050b3c5a44333a1fde9d3ee07145966f5` and changes exactly these eight planning paths:

```text
M	plan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md
A	plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-sync.correction-plan.md
A	plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-sync.correction-step.md
M	plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p2-status-sync.correction-plan.md
M	plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p2-status-sync.correction-step.md
M	plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-plan.md
M	plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-step.md
M	plan/canonical-identity-pipeline/canonical-identity-pipeline.step.md
```

P2 status-sync/P3 are recorded as complete facts. P4 is pending. No P3 status-sync candidate SHA,
tree, blob, review outcome, or receipt is prefilled. Every other tracked path is read-only,
including all analysis/specification artifacts, code, tests, existing evidence, diagrams,
`README.md`, `pyproject.toml`, `uv.lock`, PR metadata, and threads. Any unlisted path, dirty tree,
non-direct or merge parent, altered `uv.lock`, prefilled receipt/outcome, or P4 claim fails closed.

## P3 status-sync receipt contract

After this candidate is committed, Independent Plan-Reviewer may write only:

`plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-sync.correction-plan-review-log.json`

The sole receipt is one JSON object with exactly these top-level keys:

```json
{
  "schema_version": "canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-sync.correction-plan-review.v1",
  "topic": "canonical-identity-pipeline",
  "correction_id": "canonical-identity-pipeline/pr-comment-review-and-fix-p3-status-sync",
  "candidate_commit": "<40-hex P3-status-sync candidate>",
  "candidate_tree": "<40-hex P3-status-sync candidate tree>",
  "reviewed_paths": [
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-sync.correction-plan.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-sync.correction-step.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p2-status-sync.correction-plan.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p2-status-sync.correction-step.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-plan.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-step.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.step.md", "blob_sha": "<40-hex>"}
  ],
  "first_parent_admission": {
    "candidate_commit": "<same 40-hex candidate>",
    "candidate_tree": "<same 40-hex candidate tree>",
    "parent_commit": "b8c7cc6050b3c5a44333a1fde9d3ee07145966f5",
    "non_merge": true,
    "first_parent": "b8c7cc6050b3c5a44333a1fde9d3ee07145966f5",
    "exact_declared_paths": [
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-sync.correction-plan.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-sync.correction-step.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p2-status-sync.correction-plan.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p2-status-sync.correction-step.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-plan.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-step.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.step.md"
    ],
    "name_status": [
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md",
      "A\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-sync.correction-plan.md",
      "A\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-sync.correction-step.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p2-status-sync.correction-plan.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p2-status-sync.correction-step.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-plan.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-step.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.step.md"
    ]
  },
  "review_basis": "clean committed eight-path status-sync tree; committed P2 status-sync/P3 facts; P4 pending; unchanged PRCF1 scope and triage",
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

`reviewed_paths` contains exactly the eight declared paths in the displayed order. Every SHA is a
lowercase 40-hex value. `approved` requires an empty `blocking_issues` array; `needs-rework`
requires at least one non-empty blocker. The triage retains the exact seven ADDRESS and two SKIP
node IDs from PRCF1 without classifying, replying to, or resolving a thread.

Only Independent Implementer may commit the unchanged approved receipt as a clean non-merge direct
child and exact one-path evidence-only commit. That commit records P3 status synchronization only;
it restores Planner routing to P4 but does not authorize P4 itself, testing, implementation review,
classification, replies, resolution, PR approval, merge, release, tag, or post-merge work.

## Stop conditions

Missing committed P2 status-sync/P3 facts, a receipt that is not approved or separately committed,
candidate/evidence/subject conflict, or an attempt to expand the eight paths is `blocked` and
returns to Planner. Worktree or candidate identity conflict is `human-check`. Human alone owns PR
review, merge, release, tag, post-merge, and final summary.
