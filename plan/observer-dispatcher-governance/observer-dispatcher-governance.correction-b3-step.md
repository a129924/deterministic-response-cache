---
topic: observer-dispatcher-governance
correction: high-b3
state: PLANNER_REPLAN
created: 2026-09-02
---

# Observer / Dispatcher Governance — B3 Correction Steps

## Ordered Checkpoints

- [X] 1. **Planner:** freeze B3 route, historical provenance, S4-only subject, and T4/V4 schema.
- [X] 2. **Plan-Creator:** synchronize seven B3 planning paths and create only this plan/step.
- [ ] 3. **Plan-Reviewer:** temporary-index tree/blob review exactly seven uncommitted B3 planning
  paths and write one schema-complete `correction-b3-review-log.md`.
- [ ] 4. **Independent Implementer:** commit unchanged approved record plus exact reviewed set as
  non-subject B3, then validate retained tree/blob values and one-path tree-to-B3 diff.
- [ ] 5. **Independent Implementer:** create non-merge S4 changing only
  `tests/test_observer_dispatcher_governance_contract.py`.
- [ ] 6. **Tester:** attest only S4 in B3 Tester evidence as non-merge T4.
- [ ] 7. **Reviewer:** after passing same-S4 T4, write pre-commit V4 record targeting T4 through
  `review_target_commit_sha`, then independently validate post-commit V4 and exact `S4..V4`.
- [ ] 8. **Human boundary:** stop; no lifecycle action without explicit direction.

## Invariants

- B0/B1/B2/S1/S3/T1/T3/V1/V3 plus normal/recovery artifacts are frozen nonrouting provenance;
  V3 has no review-log artifact and cannot be fabricated.
- B3 is non-subject. S4 is the only current subject. T4 and V4 are its only two linear non-merge,
  evidence-only descendants, and their named range contains only their two new B3 evidence paths.
- V4's review record must target pre-existing T4 and may not contain, require, or infer V4's own SHA.
