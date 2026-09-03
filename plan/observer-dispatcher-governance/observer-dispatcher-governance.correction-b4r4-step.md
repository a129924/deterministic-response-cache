---
topic: observer-dispatcher-governance
correction: high-b4r4
state: PLANNER_REPLAN
---

# B4R4 Correction Steps

- [X] Freeze `8b87aab` B4R3 and its failed clean review as nonrouting provenance.
- [X] Create only the seven B4R4 planning-path delta.
- [ ] Independent Implementer: change only declared test to fixed B4R4 acceptance assertions and
  commit exactly eight B4R4 baseline paths; report named `8b87aab..<B4R4-SHA>` diff.
- [ ] Independent Plan-Reviewer: from clean B4R4 checkout, review eight committed blobs and write
  only B4R4 review evidence.
- [ ] Independent Implementer: separately commit unchanged approved B4R4 review record.
- [ ] Planner: verify B4R4 record and dispatch S5 only then.
- [ ] Independent Implementer: create sole non-merge S5 over exact preserved 15-path allowlist.
- [ ] Tester: create factual same-S5 B4R4 T5 evidence only, without routing/lifecycle/status/
  `next_gate` fields.
- [ ] Reviewer: require same-S5 passing T5, create V5, and prove actual named non-merge
  `S5 -> T5 -> V5` with `git diff --name-status S5..V5` listing only B4R4 T5/V5 paths.
- [ ] Stop at Human boundary; do not act on PR threads, merge, release or post-merge.
