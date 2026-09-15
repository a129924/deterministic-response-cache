---
topic: canonical-identity-pipeline
correction_id: canonical-identity-pipeline/concrete-stage-override-c7-status-sync
phase: correction-plan-review
created: 2026-09-15
---

# C7S — CSO1 committed-C7 status synchronization correction plan

## Trigger and current truth

This Human-authorized, status-only correction aligns the CSO1 planning surfaces after C5S, C6, and
C7 completed. It does not change the C3 implementation subject, its passing Tester evidence, its
approved implementation review, the public API, tests, diagram, publish files, lockfile, or draft
PR #6.

C5S candidate `2d042543d60a40519e174326462a6739f9b19f6c` and its committed approved receipt
`92f7db262bec8d774f1c6f8b1b2b16aaa82b624e` are complete frozen status facts. Independent
Reviewer wrote approved C6 evidence for immutable C3 subject
`cbee5f23310b973d9e52e4e1c662ca1d9f9169d8`; Independent Implementer committed that unchanged
evidence as sole C7 evidence-only commit `e4a2e67f29a4562f6244c5031498426b610d0a91`.

C7S is the sole active candidate. It records only C5S/C6/C7 completion, declares its future
Plan-Reviewer receipt, and leaves C8 Phase 4.5 pending and Planner-only. It creates no receipt,
Tester evidence, Reviewer evidence, C8 outcome, push, PR, Human-review, merge, release, tag,
post-merge, or final-summary claim.

## Locked scope and admission

- C7S changes exactly these eight planning paths:
  1. `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c5-status-sync.correction-plan.md`
  2. `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c5-status-sync.correction-step.md`
  3. `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c7-status-sync.correction-plan.md`
  4. `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c7-status-sync.correction-step.md`
  5. `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-plan.md`
  6. `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-step.md`
  7. `plan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md`
  8. `plan/canonical-identity-pipeline/canonical-identity-pipeline.step.md`
- Its commit must be a non-merge direct child of C7
  `e4a2e67f29a4562f6244c5031498426b610d0a91`. Its first-parent name-status is exactly two
  `A<TAB>path` entries (the paired C7S plan/step) and six `M<TAB>path` entries (completed C5S
  plan/step, CSO1 plan/step, and parent plan/step), in the lexical order above.
- No C7S candidate commit SHA, tree SHA, blob SHA, review outcome, or receipt is prefilled. The
  declared C7S review-log path is not created by this candidate.
- All code, tests, analysis, evidence, diagrams, README, `pyproject.toml`, `uv.lock`, publish, PR,
  and historic paths are read-only.

## Future receipt schema and route

1. Plan-Creator commits this clean eight-path C7S candidate.
2. Independent Plan-Reviewer, from the candidate's clean committed checkout, may write only
   `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c7-status-sync.correction-plan-review-log.json`.
3. The future receipt is one JSON object with
   `schema_version: "canonical-identity-pipeline.concrete-stage-override-c7-status-sync.correction-plan-review.v1"`
   and exactly these top-level keys:
   `schema_version`, `topic`, `correction_id`, `candidate_commit`, `candidate_tree`,
   `reviewed_paths`, `first_parent_admission`, `review_basis`, `verdict`, `blocking_issues`,
   `copilot_feedback_triage`, and `recorded_by`. `reviewed_paths` contains only ordered `path` and
   `blob_sha` entries for the eight paths above. `first_parent_admission` contains only
   `candidate_commit`, `candidate_tree`, `parent_commit`, `non_merge`, `first_parent`,
   `exact_declared_paths`, and `name_status`. All Git identifiers are lowercase 40-hex SHA values;
   `approved` requires `blocking_issues: []`, while `needs-rework` requires at least one non-empty
   blocker. `first_parent_admission.name_status` is exactly the following lexical 2A/6M list:

   ```text
   M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c5-status-sync.correction-plan.md
   M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c5-status-sync.correction-step.md
   A\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c7-status-sync.correction-plan.md
   A\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c7-status-sync.correction-step.md
   M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-plan.md
   M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-step.md
   M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md
   M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.step.md
   ```
4. Only an Independent Implementer may commit an unchanged approved C7S receipt as the sole
   evidence-only commit. Only then may Planner select C8 Phase 4.5; C8 has no outcome declared by
   C7S.

## Stop conditions

Fail closed and return to Planner for a dirty or uncommitted candidate, parent other than C7, a
merge, any path beyond the declared eight, a name-status other than the exact 2A/6M admission,
inconsistent C5S/C6/C7/C8 facts, a prefilled C7S receipt/outcome, or any C8/publish/PR/Human-review
claim. Candidate, evidence, subject, or worktree conflict is `human-check`.
