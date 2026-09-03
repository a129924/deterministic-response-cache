---
topic: observer-dispatcher-governance
correction: high-b4r5
state: PLANNER_REPLAN
---

# B4R5 Correction Steps

- [X] Freeze `8190dbb` B4R4 and its bootstrap-test route as nonrouting provenance.
- [X] Create only the seven B4R5 planning-path delta.
- [ ] Independent Implementer: commit exactly seven B4R5 baseline paths as non-subject; report named
  `8190dbb..<B4R5-SHA>` diff.
- [ ] Independent Plan-Reviewer: from clean B4R5 checkout, review seven committed blobs and write
  only B4R5 review evidence using locked schema.
- [ ] Independent Implementer: separately commit unchanged approved B4R5 review record.
- [ ] Planner: verify B4R5 record and dispatch S5 only then.
- [ ] Independent Implementer: create sole non-merge S5 over exact preserved 15-path allowlist and
  add only its three declared regression assertion groups to the test path.
- [ ] Tester: create factual same-S5 B4R5 T5 evidence only.
- [ ] Reviewer: require same-S5 passing T5, create V5, and prove actual named non-merge
  `S5 -> T5 -> V5` with `git diff --name-status S5..V5` listing only B4R5 T5/V5 paths.
- [ ] Stop at Human boundary; do not act on PR threads, merge, release or post-merge.
