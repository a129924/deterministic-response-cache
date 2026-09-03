---
topic: observer-dispatcher-governance
correction: high-b6r12
state: R22_REVIEW_PENDING
---

# Observer / Dispatcher Governance Steps

## B6R12 Current Steps

- [x] Planner: define B6R12 conditional routing-receipt correction and freeze B6R11/R21 and B6R10/R20 provenance.
- [x] Plan-Creator: synchronize exactly five B6R12 planning paths and create B6R12 plan/step.
- [ ] Independent Implementer: commit B6R12 non-merge first-parent exact-five admission in declared lexical order.
- [ ] Independent Plan-Reviewer: clean-checkout-review B6R12, validate the executable full Draft 2020-12 schema against
      actual exact-five `reviewed_artifacts` and `first_parent_admission.name_status` `prefixItems`/`items:false`, all
      40-hex candidate/tree/parent/blob fields and identical first-parent lexical diff, and write only R22.
- [ ] Independent Implementer: separately commit unchanged approved R22; only then Planner dispatches S16.
- [ ] Implementer: create S16 only in `tests/test_observer_dispatcher_governance_contract.py`; direct imports remain direct.
- [ ] Tester: write retained B6R10-path T16 only after same-S16 full-suite passing.
- [ ] Reviewer: write retained B6R10-path V16 only after committed passing T16, then Q16 after committed V16.
- [ ] Independent Reviewer: classify threads only after active passed Q16; never resolve, Human-review, merge, release,
      or post-merge from this route.
- [ ] Stop at Human boundary.

## Frozen Provenance

B6R11 `995c5a8` and absent R21 are frozen predecessor receipt only; neither can authorize S16. R20 remains
`FROZEN_INVALID_NOT_ROUTING`. B6R10, B6R9/Q15 and every earlier normal, recovery, correction, tracker and evidence
row are immutable nonrouting provenance. step-creator remains deferred.
