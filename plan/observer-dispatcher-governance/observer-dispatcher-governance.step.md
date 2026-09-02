---
topic: observer-dispatcher-governance
phase: needs-rework
created: 2026-09-01
---

# observer-dispatcher-governance — Step Tracking

## Workflow Stages

- [X] original-plan-authoring
- [X] original-planning-review
- [X] original-implementation-and-evidence
- [X] high-correction-planning
- [ ] high-correction-implementation
- [ ] high-correction-review
- [ ] high-correction-tester-evidence
- [ ] high-correction-implementation-review
- [ ] human-boundary

## Actionable Steps

- [X] **Actor:** Plan-Creator — **Action:** synchronized all seven planning artifacts:
  `plan/agent-handoff-workflow.md`, `plan/topic-plan-contract.md`,
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md`,
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md`,
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md`,
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-plan.md`, and
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-step.md`; do not
  alter existing evidence, implement, commit or create correction review evidence.
- [ ] **Actor:** Independent Plan-Reviewer — **Action:** under narrow `B0` exception, as sole writer
  of `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-review-log.md`,
  tree/blob review all seven listed **uncommitted** planning artifacts and write the schema-complete
  `correction-plan` JSON with `reviewed_tree_sha` and one path/blob revision each.
- [ ] **Actor:** Independent Implementer — **Action:** only on that schema-complete `approved`
  verdict and existing Human commit authorization, commit unchanged review record plus the seven
  reviewed artifacts as `B0`; it is evidence baseline, not a subject.
- [ ] **Actor:** Independent Implementer — **Action:** after `B0`, commit only the complete declared
  implementation as non-merge `S1`, replacement immutable `implementation_subject_sha`.
- [ ] **Actor:** Tester — **Action:** only against `S1`, write correction-tester-evidence as `T1`;
  do not use prior/recovery evidence.
- [ ] **Actor:** Reviewer — **Action:** only with same-`S1` passing `T1` evidence, write correction
  implementation-review log as `V1`, verify `S1..V1`, then stop at Human boundary.

## Implementation Steps

- [ ] 1. Align exact declared governance, custom-agent, workflow-skill and Python-template
  surfaces on the expanded correction contract.
- [ ] 2. Add declared governance contract test and preserve existing direct-import behavior.
- [ ] 3. Before declared implementation begins, hand the synchronized planning artifacts to
  the independent Correction Plan-Reviewer and stop unless its review evidence is approved and
  committed unchanged.

## Main Agent Actionable Steps — Fixed Tail

- [ ] After final new Reviewer evidence, stop. Do not publish, push, act on PR threads,
  merge, sync, release, tag or create summary without new explicit Human direction.

## Handoff / Gate Notes

- State is `needs-rework` / `PLANNER_REPLAN`. Old epoch is terminal
  `R0=cb3f66c60e95e5580cb2b30632d0d5ed9f0d0ee9`, identified only by
  `ecc5b6f61bacc5493ca3a9f1012d1bfdd43a810c..cb3f66c60e95e5580cb2b30632d0d5ed9f0d0ee9`, and is
  frozen provenance. `B0` reviews/commits no subject; later `S1` resets the subject.
- Tester state is pending until `S1` exists. Final range must be linear/non-merge `S1 -> T1 -> V1`,
  contain exactly correction Tester then correction Reviewer evidence, and be verified as `S1..V1`,
  not `HEAD`; divergence returns to Planner.
