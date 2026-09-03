---
topic: observer-dispatcher-governance
correction: high-b6r12
state: R22_REVIEW_PENDING
---

# B6R12 Correction Steps

- [x] Planner defines the B6R12 conditional routing-receipt correction; B6R11/R21 and B6R10/R20 remain frozen.
- [x] Plan-Creator writes exactly the five B6R12 planning paths.
- [ ] Independent Implementer admits B6R12 as a non-merge first-parent exact-five commit in declared lexical order.
- [ ] Independent Plan-Reviewer writes only R22 from committed B6R12; it validates the executable full Draft 2020-12
      schema against actual five-record `reviewed_artifacts` and identical `first_parent_admission.name_status`
      `prefixItems`/`items:false`, all 40-hex candidate/tree/parent/blob fields and the lexical name-status diff.
- [ ] Independent Implementer commits unchanged approved R22; only then Planner selects `R22_COMPLETE_S16_NEXT` and dispatches S16.
- [ ] Implementer changes only `tests/test_observer_dispatcher_governance_contract.py`; direct imports remain direct.
- [ ] Tester writes retained B6R10-path T16 only after same-S16 full-suite passing.
- [ ] Reviewer writes retained B6R10-path V16 only after committed passing T16, then Q16 after committed V16.
- [ ] Independent Reviewer classifies threads only after active passed Q16; never resolves, Human-reviews, merges, releases or post-merges from this route.
- [ ] Stop at Human boundary.

## Frozen provenance

B6R11 `995c5a8`, absent R21, R20 `FROZEN_INVALID_NOT_ROUTING`, B6R10, B6R9/Q15 and every earlier normal, recovery, correction, tracker and evidence row are immutable nonrouting provenance. step-creator remains deferred.
