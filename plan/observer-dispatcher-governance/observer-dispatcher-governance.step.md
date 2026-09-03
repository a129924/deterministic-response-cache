---
topic: observer-dispatcher-governance
correction: high-b6r10
state: R20_REVIEW_PENDING
---

# Observer / Dispatcher Governance Steps

## B6R10 Current Steps

- [ ] Plan-Creator: synchronize exactly eleven B6R10 planning paths and create B6R10 plan/step.
- [ ] Independent Implementer: commit B6R10 non-merge first-parent exact-eleven admission.
- [ ] Independent Plan-Reviewer: clean-checkout-review B6R10 and write only extended R20.
- [ ] Independent Implementer: separately commit unchanged approved R20; only then Planner dispatches S16.
- [ ] Implementer: create S16 only in tests/test_observer_dispatcher_governance_contract.py.
- [ ] Tester: write exact-key same-S16 T16 JSON with a 40-character lowercase hexadecimal SHA and one passing,
      zero-exit test run.
- [ ] Reviewer: write exact-key V16 JSON after committed passing T16; bind its commit/path/blob/subject/status and
      require `APPROVED` plus empty blockers.
- [ ] Reviewer: only after committed V16, write exact-key Q16 actual-gate close record; an independent Implementer
      must commit it unchanged as sole evidence-only path before `ACTIVE_CANDIDATE_CLOSED` classification-only state.
- [ ] Independent Reviewer: classify threads only after active Q16; never resolve, Human-review, merge, release, or
      post-merge from this route.
- [ ] Stop at Human boundary; no Reviewer action is Human PR review or merge.

## Frozen Provenance

B6R9/R19/S15/T15/V15/Q15 and every earlier normal, recovery, correction, tracker and evidence row are immutable frozen
nonrouting predecessor provenance. None is an active step, candidate, subject, gate, classification authority, or
repair queue. B6R10 current steps above are the sole operational tracker. step-creator remains deferred.
