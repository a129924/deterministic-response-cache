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
      `plan/topic-plan-contract.md` after independent approval and Planner routing, and commits those three files
      together as the one immutable implementation subject. Record its full 40-hex SHA as `S`.
- [ ] 2. Tester, as sole writer, writes
      `plan/workflow-concurrency-supersession/workflow-concurrency-supersession.tester-evidence.json` for `S`.
      The single JSON object has only `schema_version`, `topic`, `implementation_subject_commit`, `status`,
      `commands`, and `recorded_by`; `schema_version` is integer `1`, `topic` is
      `workflow-concurrency-supersession`, `recorded_by` is `Tester`, `implementation_subject_commit` is `S`,
      `status` is `passing|failing`, and every `commands` entry has only a non-empty `command` and integer
      `exit_code`. `passing` requires every exit code to be `0`; `failing` requires at least one non-zero exit code.
      Tester does not commit.
- [ ] 3. Independent Implementer commits the unchanged passing Tester evidence as its own sole evidence-only
      commit. No planning, implementation, or other evidence path may share that commit.
- [ ] 4. Independent Reviewer, as sole writer, consumes only that committed same-topic, same-`S`, passing Tester
      evidence and writes
      `plan/workflow-concurrency-supersession/workflow-concurrency-supersession.implementation-review-log.json`.
      The single JSON object has only `schema_version`, `topic`, `implementation_subject_commit`,
      `tester_evidence_commit`, `verdict`, `blocking_issues`, and `recorded_by`; `tester_evidence_commit` is the
      full SHA of step 3's sole evidence-only commit, `schema_version` is integer `1`, `verdict` is
      `approved|needs-rework`, `blocking_issues` is a string array (empty only for `approved`, non-empty for
      `needs-rework`), and `recorded_by` is `Independent Reviewer`. Reviewer does not commit.
- [ ] 5. Independent Implementer commits the unchanged Reviewer evidence as its own sole evidence-only commit.
      `approved` permits Planner Phase 4.5 alignment; `needs-rework` returns to Implementer and requires a new
      subject `S` plus steps 2–5 again.
- [ ] 6. Validate that all three governance contract texts contain and accept the exact two evidence paths, unique
      writers, required schemas, same full-SHA binding, Tester-before-Reviewer ordering, actual command/exit-code
      rule, and evidence-only commits; otherwise stop as `needs-rework`.
- [ ] 7. Planner performs Phase 4.5 alignment; only then may human-authorized bounded publish open a draft PR.

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
- The exact Tester and Independent Reviewer evidence paths, schemas, full-SHA binding, and evidence-only commit
  order are fixed in steps 2–5. The three contract texts are an acceptance target of step 6; these planning artifacts
  do not themselves validate or create either evidence file.
