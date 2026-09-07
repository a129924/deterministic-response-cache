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
- [ ] **Actor:** Independent Implementer — **Action:** Commit the Plan-Creator's unchanged planning candidate
      as the sole planning-candidate commit; Planner then routes independent Plan-Reviewer. Plan-Creator does not
      commit.
- [ ] **Actor:** Independent Plan-Reviewer — **Action:** Review that committed planning candidate and, as the
      only writer, write the required machine-consumable `approved|needs-rework` receipt at
      `plan/workflow-concurrency-supersession/workflow-concurrency-supersession.plan-review-log.md`; never
      commit the receipt.
- [ ] **Actor:** Independent Implementer — **Action:** If and only if the receipt is `approved`, commit it
      unchanged as a standalone evidence-only commit; Planner must then re-preflight before bounded contract
      implementation. A `needs-rework` receipt is not committed and creates no candidate, route or authorization;
      Plan-Creator repairs only declared planning artifacts (for this repair: plan, spec and step only), Independent
      Implementer commits the new candidate, and Independent Plan-Reviewer reviews that new candidate again.

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

- Bootstrap exception is exhausted once an Independent Implementer has committed the five Plan-Creator
  analysis/planning artifacts unchanged as the planning candidate. The next role is independent Plan-Reviewer,
  whose sole receipt path is `plan/workflow-concurrency-supersession/workflow-concurrency-supersession.plan-review-log.md`;
  Plan-Reviewer writes but never commits its machine-consumable receipt. Only an `approved` receipt for that
  committed candidate, committed unchanged by an Independent Implementer as standalone evidence-only evidence,
  permits Planner re-preflight. A `needs-rework` receipt is never committed or routing authority; its repair
  needs a newly committed candidate and a new independent review. No role may infer `src-implementation` work.
- B6R13/R23 remains subject-local. Its R23 chat response is non-evidence and is neither cancelled nor backfilled here.
- Concurrent topics require isolated branch/worktree and non-conflicting declared paths/evidence/subjects; any conflict
  is `human-check`.
