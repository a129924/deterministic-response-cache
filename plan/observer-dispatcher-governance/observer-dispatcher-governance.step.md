---
topic: observer-dispatcher-governance
phase: needs-rework
created: 2026-09-01
---

# observer-dispatcher-governance — Step Tracking

> **B1 correction override:** B0/S1/T1/V1 are frozen provenance. The current route is one
> tree/blob review of seven B1 planning artifacts, non-subject B1, test-only S2, then T2 and V2;
> no evidence, commit, or thread is created in this Plan-Creator step.

## Workflow Stages

- [X] original-plan-authoring
- [X] original-planning-review
- [X] original-implementation-and-evidence
- [X] high-correction-planning
- [ ] b1-correction-review-and-baseline
- [ ] b1-test-only-implementation
- [ ] b1-tester-evidence
- [ ] b1-implementation-review
- [ ] human-boundary

## Actionable Steps

- [X] **Actor:** Plan-Creator — **Action:** synchronized the seven B1 planning artifacts only:
  `plan/agent-handoff-workflow.md`, `plan/topic-plan-contract.md`,
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md`,
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md`, this step tracker,
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b1-plan.md`, and
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b1-step.md`; do not
  alter frozen provenance, write evidence, commit, push, or act on threads.
- [ ] **Actor:** Independent Plan-Reviewer — **Action:** under the one-time `B1` exception, as sole
  writer of
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b1-review-log.md`,
  tree/blob review exactly the seven uncommitted B1 planning artifacts and write the schema-complete
  `correction-b1-plan` JSON with `reviewed_tree_sha` and one path/blob revision for each artifact.
- [ ] **Actor:** Independent Implementer — **Action:** only on that schema-complete `approved`
  verdict and existing Human commit authorization, commit the unchanged B1 review record plus the
  exact seven reviewed artifacts as non-subject `B1`; it never establishes an implementation subject.
- [ ] **Actor:** Independent Implementer — **Action:** only after committed B1, make one non-merge
  immutable `S2` subject commit that modifies only
  `tests/test_observer_dispatcher_governance_contract.py`.
- [ ] **Actor:** Tester — **Action:** only against same-S2, write
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b1-tester-evidence.md`
  as non-merge `T2`; no frozen record may satisfy this gate.
- [ ] **Actor:** Reviewer — **Action:** only with same-S2 passing T2, write
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b1-implementation-review-log.md`
  as non-merge `V2`, verify exact `S2..V2`, then stop at the Human boundary.

## Implementation Steps

- [ ] 1. Before implementation, hand the synchronized seven B1 planning artifacts to the independent
  Plan-Reviewer. Stop unless its B1 tree/blob review is `approved` and is committed unchanged with
  exactly that reviewed set as non-subject B1.
- [ ] 2. In S2 only, add direct fail-closed assertions to
  `tests/test_observer_dispatcher_governance_contract.py` for frozen B0/S1/T1/V1 provenance, S2 as
  the only replacement subject, and the exact T2-then-V2 evidence topology; preserve existing
  direct-import behavior.
- [ ] 3. Require T2 then V2 as the only evidence-only descendants. Verify the named
  `git diff --name-status S2..V2` range contains exactly their two declared evidence paths; never
  substitute `HEAD`, a merge, or an extra descendant.

## Main Agent Actionable Steps — Fixed Tail

- [ ] After final new Reviewer evidence, stop. Do not publish, push, act on PR threads,
  merge, sync, release, tag or create summary without new explicit Human direction.

## Handoff / Gate Notes

- State is `needs-rework` / `PLANNER_REPLAN`. B0/S1/T1/V1, every normal/recovery record, and all
  old correction artifacts are frozen provenance only: they are never current routing, a B1 gate,
  a subject, Tester evidence, or Reviewer evidence. B1 is a one-time tree/blob-reviewed planning
  baseline and is explicitly non-subject.
- Tester state remains pending until non-merge S2 exists. S2 alone establishes the replacement
  immutable `implementation_subject_sha`; final evidence must be linear, non-merge `S2 -> T2 -> V2`,
  contain exactly the two new B1 Tester and Reviewer paths, and be verified as named `S2..V2`, never
  `HEAD`. Any other topology, merge, extra descendant, or range returns to Planner.
