---
topic: observer-dispatcher-governance
correction: high-b1
state: PLANNER_REPLAN
created: 2026-09-02
---

# Observer / Dispatcher Governance — B1 Correction Steps

## Ordered Checkpoints

- [X] 1. **Planner:** freeze B1 direction, seven planning paths, frozen B0/S1/T1/V1 provenance,
  test-only S2 subject, and T2/V2 topology.
- [X] 2. **Plan-Creator:** synchronize the seven B1 planning artifacts and create only this B1
  plan/step; do not write evidence, commit, or alter prior correction artifacts.
- [ ] 3. **Correction Plan-Reviewer:** before S2, tree/blob review exactly the seven uncommitted B1
  planning artifacts and write one schema-complete `correction-b1-review-log.md`; `needs-rework`
  returns to Planner.
- [ ] 4. **Independent Implementer:** only on approved B1 review and existing Human commit
  authorization, commit the unchanged record and exact reviewed set as non-subject `B1`.
- [ ] 5. **Independent Implementer:** only after B1, modify only
  `tests/test_observer_dispatcher_governance_contract.py` in non-merge immutable subject `S2`.
- [ ] 6. **Tester:** attest only S2 in `correction-b1-tester-evidence.md` as non-merge T2.
- [ ] 7. **Reviewer:** after same-S2 passing T2, write `correction-b1-implementation-review-log.md`
  as non-merge V2 and verify exact two-path `S2..V2` topology.
- [ ] 8. **Human boundary:** stop; no lifecycle action without new explicit direction.

## Required Evidence Schemas

- The B1 review, T2 Tester, and V2 Reviewer records must use the complete three-object schemas in
  `plan/topic-plan-contract.md#current-topic-correction-evidence-schemas`. Plan-Reviewer writes
  only its verdict; Tester writes only factual results; Reviewer writes only its verdict; Planner
  alone decides route, status, and next role.

## Invariants

- B0/S1/T1/V1 are frozen provenance, never B1 gate or subject. B1 is non-subject.
- S2 changes only the declared governance contract test. Final `S2..V2` contains exactly T2 then
  V2 evidence paths, with no merge, extra descendant, or `HEAD` range.
