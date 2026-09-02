---
topic: observer-dispatcher-governance
correction: high-b6
state: B6_ADMISSION_PENDING
---

# Observer / Dispatcher Governance Steps

## Frozen Provenance

- [X] Retain `b900366`, normal/recovery records, B0–B5R (including R8/R9), S1–S7, T1–T7, V1–V7, Q7 and
  all earlier correction artifacts only as immutable historical provenance; exclude them from B6.
- [X] Keep `step-creator` work deferred.

## B6 Current Steps

- [X] Plan-Creator: synchronize exactly the seven B6 planning paths and create B6 plan/step.
- [ ] Independent Implementer: commit one non-merge B6 admission with exact seven-path first-parent diff.
- [ ] Independent Plan-Reviewer: clean-checkout-review B6 and write only R10.
- [ ] Independent Implementer: separately commit unchanged approved R10 record.
- [ ] Planner: verify R10 then dispatch test-only S8.
- [ ] Tester: write factual T8 after full-triple actual Git assertion passes without skip.
- [ ] Reviewer: write V8 after passing same-S8 T8 and prove exact linear non-merge `S8 -> T8 -> V8` plus
  exact `S8..V8` evidence-only range.
- [ ] Reviewer: run post-V8 no-artifact Q8 from committed full V8 SHA and classify comments; thread action
  remains unavailable without explicit `addressed-and-resolvable` classification.
- [ ] Stop at Human boundary.
