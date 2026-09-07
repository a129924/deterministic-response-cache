# Workflow Concurrency Supersession Specification

## Acceptance Criteria

1. The approved contract makes routing topic-local: only a topic's own committed approved planning and
   phase evidence controls its candidate, phase, gate and next role.
2. A missing, stale, uncommitted or `needs-rework` B6R13/R23 record blocks B6R13 only. It cannot block an
   independent topic with complete, non-conflicting topic-local evidence.
3. Every topic requires committed plan, step, exact Plan-Reviewer receipt, immutable implementation subject,
   factual same-subject Tester evidence and independent same-subject Reviewer evidence. For this topic, the
   receipt path is `plan/workflow-concurrency-supersession/workflow-concurrency-supersession.plan-review-log.md`;
   Independent Plan-Reviewer is its only writer and records a machine-consumable `approved|needs-rework`
   verdict for the committed planning candidate, but never commits it. An independent Implementer is the sole
   commit owner: it commits the original Plan-Creator planning candidate, then commits an unchanged `approved`
   receipt evidence-only before Planner re-preflight routes bounded contract implementation. No cross-topic reuse
   or chat/branch/summary/frozen-provenance substitution is allowed.
4. Parallel active topics use isolated branch/worktree. Any declared path, candidate, evidence or subject
   conflict returns `human-check` without a writer dispatch.
5. Publish still requires same-subject passing Tester evidence, independent Reviewer approval, Planner
   Phase 4.5 alignment and existing human authorization. It produces only `pr-open`; multiple draft PRs are
   allowed; only Human may merge, release, tag or perform post-merge work.
6. This topic changes neither `src-implementation` nor stable-library/release surfaces. Its only product-adjacent
   change is the Human-authorized, one-time repair of
   `tests/test_observer_dispatcher_governance_contract.py`; B6R13/S17 has no future write authority for that path
   without a new human-check resolution.
7. The four-file immutable implementation subject contains `AGENTS.md`, `plan/agent-handoff-workflow.md`,
   `plan/topic-plan-contract.md`, and `tests/test_observer_dispatcher_governance_contract.py`. The first three
   accept this topic's executable evidence contract; the test changes only the two B6R12/R22 global-route assertions
   in `assert_s16_route_is_fail_closed`, making them verify B6R13/R23 as an
   `observer-dispatcher-governance` subject-local frozen-provenance obligation rather than another topic's global
   prerequisite. Tester is the sole writer of
   `plan/workflow-concurrency-supersession/workflow-concurrency-supersession.tester-evidence.json`; Independent
   Reviewer is the sole writer of
   `plan/workflow-concurrency-supersession/workflow-concurrency-supersession.implementation-review-log.json`.
   Both are machine-consumable JSON records bound to the same full 40-hex immutable four-file implementation-subject
   SHA. Direct imports, fixtures, mocks, and every other test assertion remain unchanged.
8. Tester evidence has only `schema_version` (integer `1`), `topic`, `implementation_subject_commit`, `status`,
   `commands`, and `recorded_by`; every command records a non-empty `command` and integer `exit_code`, `passing`
   requires all exit codes to be `0`, and `failing` requires at least one non-zero exit code. Reviewer evidence has
   only `schema_version` (integer `1`), `topic`, `implementation_subject_commit`, `tester_evidence_commit`,
   `verdict`, `blocking_issues`, and `recorded_by`; `blocking_issues` is a string array that is empty only for
   `approved` and non-empty for `needs-rework`. It may exist only after the committed same-subject passing Tester
   evidence it names. Tester and Reviewer never commit their own evidence.
9. The fixed order is four-file implementation-subject commit, Tester full `uv run pytest` plus evidence write,
   independent-Implementer sole Tester-evidence-only commit, Independent-Reviewer write, then independent-Implementer
   sole Reviewer-evidence-only commit. Reviewer
   only consumes the committed same-topic, same-full-SHA passing Tester evidence; `approved` alone advances to
   Planner Phase 4.5, while `needs-rework` returns to Implementer with a new subject and a new full sequence.

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

### Scenario 4: Only two global-route assertions change

- **Given** the Human-authorized one-time ownership resolution for
  `tests/test_observer_dispatcher_governance_contract.py`.
- **When** Implementer prepares the four-file subject.
- **Then** it replaces only the two B6R12/R22 global-route assertions in
  `assert_s16_route_is_fail_closed`: one verifies the B6R13/R23 route and one verifies that this obligation is
  subject-local and not another topic's global prerequisite. Direct imports, fixtures, mocks, and every other
  assertion are unchanged.

### Scenario 5: Tester evidence precedes implementation review

- **Given** the four declared implementation files have been committed as one immutable implementation subject with
  full SHA `S`.
- **When** Tester runs full `uv run pytest`, writes the required JSON evidence for `S` including that actual command
  and its zero exit code, and an independent Implementer commits that file unchanged by itself.
- **Then** Independent Reviewer may consume only that committed passing evidence, write its JSON verdict for `S`,
  and an independent Implementer commits that review file unchanged by itself; neither evidence shares a commit
  with implementation or another evidence artifact.

### Scenario 6: Contract validation is incomplete

- **Given** any one of the three governance contract texts omits either exact evidence path, the unique writer,
  required JSON fields, full-SHA binding, or Tester-before-Reviewer commit order.
- **When** this topic's implementation is validated.
- **Then** validation fails and the topic cannot proceed to Tester or publish.

## Error / Edge Cases

- An uncommitted Plan-Reviewer chat response is not a receipt and cannot route any topic.
- The only route from committed planning candidate to contract implementation is: Plan-Creator authoring or
  repair, independent Implementer planning-candidate commit, independent Plan-Reviewer receipt write only,
  independent Implementer standalone evidence-only commit of an unchanged `approved` receipt, then Planner
  re-preflight. Plan-Reviewer never commits. A `needs-rework` receipt is never committed and creates no
  candidate, route or authorization; Plan-Creator must repair only declared planning artifacts, an independent
  Implementer must commit the repaired candidate, and a new independent review is required. A receipt for a
  different commit, or a receipt written by another role, fails closed.
- This current bounded planning repair changes only this topic's plan, specification and step tracker; it does
  not amend analysis artifacts, the existing Plan-Reviewer receipt, the existing failing Tester evidence, any
  contract text, or the governance regression test.
- The prior approved Plan-Reviewer receipt and failing Tester evidence bind prior candidates/subjects. They are not
  routing authority for the repaired candidate and must remain untouched; the repaired candidate requires a new
  independent Plan-Reviewer `approved` receipt, a new four-file subject, and new Tester/Reviewer evidence.
- Evidence that names a different topic or immutable subject fails closed for the current topic.
- A missing command, non-integer exit code, non-zero command exit code paired with `passing`, missing required JSON
  key, extra top-level key, abbreviated SHA, uncommitted Tester evidence, or a Reviewer record that names a different
  subject fails closed.
- Reviewer cannot write review evidence from a failing Tester record or from a Tester record not committed as its own
  sole evidence-only commit. A Reviewer `needs-rework` record is committed only as its own evidence-only commit and
  returns the topic to Implementer; it cannot authorize Phase 4.5 or publish.
- A shared worktree, non-isolated branch, or undeclared path is a conflict requiring `human-check`.
- `src-implementation` has no implied tree, naming, API or implementation decision from this governance topic.
