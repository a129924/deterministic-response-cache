---
topic: canonical-identity-pipeline
correction_id: canonical-identity-pipeline/pr-comment-review-and-fix-p2-status-sync
phase: correction-plan-review-pending
created: 2026-09-16
---

# PRCF1 P2 status synchronization correction plan

## Trigger and current truth

PRCF1 P0 is the clean ten-path candidate `bbf3bde597b1adbf074ef832802a6151c330752a`.
Independent Plan-Reviewer wrote the approved P1 receipt for that candidate; Independent
Implementer committed it unchanged as P2 at `618be901c8313447b88e9fec513dea6beb59e534`. P2 is a
non-merge direct child of P0 whose exact one-path diff adds only
`canonical-identity-pipeline.pr-comment-review-and-fix.correction-plan-review-log.json`.

The parent and PRCF1 trackers still describe P1/P2 as pending. This Human-authorized correction
only synchronizes those committed facts, keeps P3 pending, and creates the route for an independent
review of this six-path candidate. It does not write a P2 status-sync receipt, create an
implementation subject, change code or tests, alter `uv.lock`, touch PR #6, reply to or resolve a
thread, publish, merge, release, tag, or perform post-merge work.

## Locked scope and admission

This candidate is a clean non-merge direct child of
`618be901c8313447b88e9fec513dea6beb59e534` and changes exactly these six planning paths:

```text
M	plan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md
A	plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p2-status-sync.correction-plan.md
A	plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p2-status-sync.correction-step.md
M	plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-plan.md
M	plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-step.md
M	plan/canonical-identity-pipeline/canonical-identity-pipeline.step.md
```

P0, P1, and P2 are recorded as complete facts. P3 is pending. No P2 status-sync candidate SHA,
tree, blob, review outcome, or receipt is prefilled. Every other tracked path is read-only,
including all analysis/specification artifacts, code, tests, existing evidence, diagrams,
`README.md`, `pyproject.toml`, `uv.lock`, PR metadata, and threads. Any unlisted path, dirty tree,
non-direct or merge parent, altered `uv.lock`, prefilled receipt/outcome, or P3 claim fails closed.

## P2 status-sync receipt contract

After this candidate is committed, Independent Plan-Reviewer may write only:

`plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p2-status-sync.correction-plan-review-log.json`

The sole receipt is one JSON object with exactly these top-level keys:

```json
{
  "schema_version": "canonical-identity-pipeline.pr-comment-review-and-fix-p2-status-sync.correction-plan-review.v1",
  "topic": "canonical-identity-pipeline",
  "correction_id": "canonical-identity-pipeline/pr-comment-review-and-fix-p2-status-sync",
  "candidate_commit": "<40-hex P2-status-sync candidate>",
  "candidate_tree": "<40-hex P2-status-sync candidate tree>",
  "reviewed_paths": [
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p2-status-sync.correction-plan.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p2-status-sync.correction-step.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-plan.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-step.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.step.md", "blob_sha": "<40-hex>"}
  ],
  "first_parent_admission": {
    "candidate_commit": "<same 40-hex candidate>",
    "candidate_tree": "<same 40-hex candidate tree>",
    "parent_commit": "618be901c8313447b88e9fec513dea6beb59e534",
    "non_merge": true,
    "first_parent": "618be901c8313447b88e9fec513dea6beb59e534",
    "exact_declared_paths": [
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p2-status-sync.correction-plan.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p2-status-sync.correction-step.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-plan.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-step.md",
      "plan/canonical-identity-pipeline/canonical-identity-pipeline.step.md"
    ],
    "name_status": [
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md",
      "A\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p2-status-sync.correction-plan.md",
      "A\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p2-status-sync.correction-step.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-plan.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-step.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.step.md"
    ]
  },
  "review_basis": "clean committed six-path status-sync tree; committed P0/P1/P2 facts; P3 pending; unchanged PRCF1 scope and triage",
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

`reviewed_paths` contains exactly the six declared paths in the displayed order. Every SHA is a
lowercase 40-hex value. `approved` requires an empty `blocking_issues` array; `needs-rework`
requires at least one non-empty blocker. The triage must retain the exact seven ADDRESS and two
SKIP node IDs in the completed P1 receipt without classifying, replying to, or resolving a thread.

Only Independent Implementer may commit the unchanged approved receipt, as a clean non-merge direct
child and exact one-path evidence-only commit. That commit records the P2 status-sync review only;
it restores Planner routing to P3 but does not itself authorize P3, testing, implementation review,
classification, replies, resolution, PR approval, merge, release, tag, or post-merge work.

## Stop conditions

Missing committed P0/P1/P2 facts, a receipt that is not approved or is not separately committed,
candidate/evidence/subject conflict, or an attempt to expand the six paths is `blocked` and returns
to Planner. Worktree or candidate identity conflict is `human-check`. Human alone owns PR review,
merge, release, tag, post-merge, and final summary.
