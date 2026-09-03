---
topic: observer-dispatcher-governance
correction: high-b2
state: PLANNER_REPLAN
created: 2026-09-02
---

# Observer / Dispatcher Governance — B2 Correction Steps

## Ordered Checkpoints

- [X] 1. **Planner:** freeze B2 direction, verified-tree baseline, frozen B0/S1/T1/V1/B1 provenance,
  test-only S3 subject, and T3/V3 topology.
- [X] 2. **Plan-Creator:** synchronize the seven B2 planning artifacts and create only this B2
  plan/step; do not write evidence, commit, or alter prior correction artifacts.
- [ ] 3. **Correction Plan-Reviewer:** before S3, use temporary index plus `git write-tree`,
  `git rev-parse`, and `git cat-file` to independently tree/blob review exactly the seven
  uncommitted B2 planning artifacts and write one schema-complete `correction-b2-review-log.md`;
  `needs-rework` returns to Planner.
- [ ] 4. **Independent Implementer:** only on approved B2 review and existing Human commit
  authorization, commit unchanged record plus exact reviewed set as non-subject B2, then validate
  retained tree/blob values and the one-path reviewed-tree-to-B2 diff.
- [ ] 5. **Independent Implementer:** only after validated B2, modify only
  `tests/test_observer_dispatcher_governance_contract.py` in non-merge immutable subject S3.
- [ ] 6. **Tester:** attest only S3 in `correction-b2-tester-evidence.md` as non-merge T3.
- [ ] 7. **Reviewer:** after same-S3 passing T3, write `correction-b2-implementation-review-log.md`
  as non-merge V3 and verify exact two-path `S3..V3` topology.
- [ ] 8. **Human boundary:** stop; no lifecycle action without new explicit direction.

## Required Evidence Schemas

- The B2 review, T3 Tester, and V3 Reviewer records must use the complete three-object schemas in
  `plan/topic-plan-contract.md#current-topic-correction-evidence-schemas`. Plan-Reviewer writes only
  its verdict; Tester writes only factual results; Reviewer writes only its verdict; Planner alone
  decides route, status, and next role.

## Invariants

- B0/S1/T1/V1, B1, and B1 invalid review record are frozen provenance, never B2 gate or subject.
  B2 is non-subject and reviewed tree is a verified Git tree object.
- S3 changes only the declared governance contract test. Final `S3..V3` contains exactly T3 then V3
  evidence paths, with no merge, extra descendant, or `HEAD` range.
