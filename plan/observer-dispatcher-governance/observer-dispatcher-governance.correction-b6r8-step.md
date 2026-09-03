---
topic: observer-dispatcher-governance
correction: high-b6r8
state: R18_REVIEW_PENDING
---

# B6R8 Correction Steps

- [ ] Plan-Creator: synchronize exactly seven B6R8 planning paths and create B6R8 plan/step.
- [ ] Independent Implementer: commit B6R8 non-merge first-parent exact-seven admission.
- [ ] Independent Plan-Reviewer: clean-checkout-review B6R8 tree, seven blobs/admission and frozen R17 receipt; write only R18.
- [ ] Independent Implementer: separately commit unchanged approved R18 with effective state `R17_COMPLETE_S14_NEXT`.
- [ ] Planner: verify R18 then dispatch test-only S14.
- [ ] Implementer: create S14 with temporal frozen-provenance/current-route assertions, direct imports and fail-closed actual input.
- [ ] Tester: write truthful same-S14 T14 at the B6R8 evidence path after the full suite.
- [ ] Reviewer: write B6R8-path V14 after passing T14 and prove non-merge `S14 -> T14 -> V14` and exact `S14..V14`.
- [ ] Reviewer: after committed V14 execute read-only actual full-triple Q14.
- [ ] Independent Reviewer: after passed Q14 classify threads; only explicit `addressed-and-resolvable` permits resolve.
- [ ] Stop at Human boundary.

## Frozen Provenance

All normal/recovery and B0–B6R7 tracker rows are frozen nonrouting provenance. B6R7 baseline
`03d90755b378063a312e62f9eefbe31caa081981` and R17 receipt `a7770348222049f1c8bb6a0ee67e3136f2f47c3f` are frozen
receipt facts, not route state.
