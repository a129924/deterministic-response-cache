---
topic: workflow-concurrency-supersession
phase: planning
state: planned
---

# workflow-concurrency-supersession — Step Tracking

## Workflow Stages

- [X] human-bootstrap-authorized
- [X] plan-authoring
- [ ] independent-plan-review
- [ ] implementation
- [ ] tester
- [ ] independent-review
- [ ] planner-phase-4.5-alignment
- [ ] bounded-publish
- [ ] human-merge

## Actionable Steps

- [X] **Actor:** Plan-Creator — **Action:** Create only the five declared analysis/planning artifacts.
- [ ] **Actor:** Independent Plan-Reviewer — **Action:** Review the committed planning artifacts and return the
      required `approved|needs-rework` handoff; no contract implementation occurs before Planner re-preflight.

## Implementation Steps

- [ ] 1. Implementer updates only `AGENTS.md`, `plan/agent-handoff-workflow.md`, and
      `plan/topic-plan-contract.md` after independent approval and Planner routing.
- [ ] 2. Tester records factual validation for the same immutable implementation subject.
- [ ] 3. Independent Reviewer verifies the same subject using passing Tester evidence.
- [ ] 4. Planner performs Phase 4.5 alignment; only then may human-authorized bounded publish open a draft PR.

## Main Agent Actionable Steps — Fixed Tail

- [ ] Publish only after independent Reviewer approval, Planner Phase 4.5 alignment, and explicit human authorization.
- [ ] Human alone may merge; no release, tag, or post-merge action belongs to this topic.

## Handoff / Gate Notes

- Bootstrap exception is exhausted once these planning artifacts are committed. The next role is independent
  Plan-Reviewer, followed by Planner re-preflight; no role may infer `src-implementation` work.
- B6R13/R23 remains subject-local. Its R23 chat response is non-evidence and is neither cancelled nor backfilled here.
- Concurrent topics require isolated branch/worktree and non-conflicting declared paths/evidence/subjects; any conflict
  is `human-check`.
