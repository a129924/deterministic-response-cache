# Workflow Concurrency Supersession Specification

## Acceptance Criteria

1. The approved contract makes routing topic-local: only a topic's own committed approved planning and
   phase evidence controls its candidate, phase, gate and next role.
2. A missing, stale, uncommitted or `needs-rework` B6R13/R23 record blocks B6R13 only. It cannot block an
   independent topic with complete, non-conflicting topic-local evidence.
3. Every topic requires committed plan, step, Plan-Reviewer receipt, immutable implementation subject,
   factual same-subject Tester evidence and independent same-subject Reviewer evidence. No cross-topic
   reuse or chat/branch/summary/frozen-provenance substitution is allowed.
4. Parallel active topics use isolated branch/worktree. Any declared path, candidate, evidence or subject
   conflict returns `human-check` without a writer dispatch.
5. Publish still requires same-subject passing Tester evidence, independent Reviewer approval, Planner
   Phase 4.5 alignment and existing human authorization. It produces only `pr-open`; multiple draft PRs are
   allowed; only Human may merge, release, tag or perform post-merge work.
6. This topic changes neither `src-implementation` nor stable-library/release surfaces.

## Behavioral Scenarios

### Scenario 1: B6R13 stays pending while another topic is ready

- **Given** B6R13/R23 has missing or uncommitted evidence, and another topic has its own complete committed
  approved planning evidence with no conflict.
- **When** Planner preflights the latter topic.
- **Then** it routes that topic's next role; B6R13 remains blocked only for B6R13.

### Scenario 2: Parallel topics conflict

- **Given** two active topics declare overlapping write paths or inconsistent candidate/evidence/subject facts.
- **When** Planner evaluates either conflict.
- **Then** it returns `human-check` and dispatches no writer until Human resolves the overlap.

### Scenario 3: Publish remains constrained

- **Given** two independent topics have their own Tester and Reviewer evidence.
- **When** one lacks Planner Phase 4.5 alignment or human authorization.
- **Then** that topic cannot publish, while the other may open its separately authorized draft PR; neither can
  merge, release, tag or post-merge automatically.

## Error / Edge Cases

- An uncommitted Plan-Reviewer chat response is not a receipt and cannot route any topic.
- Evidence that names a different topic or immutable subject fails closed for the current topic.
- A shared worktree, non-isolated branch, or undeclared path is a conflict requiring `human-check`.
- `src-implementation` has no implied tree, naming, API or implementation decision from this governance topic.
