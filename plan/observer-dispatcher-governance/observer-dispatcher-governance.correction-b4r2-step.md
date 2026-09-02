---
topic: observer-dispatcher-governance
correction: high-b4r2
state: PLANNER_REPLAN
---

# B4R2 Correction Steps

- [X] Freeze B0–B4R and all prior normal/recovery records as nonrouting provenance.
- [X] Create only the six-path B4R2 planning delta.
- [ ] Independent Implementer: commit exactly the six B4R2 planning paths as non-subject B4R2.
- [ ] Independent Plan-Reviewer: from clean B4R2 checkout, review the six committed blobs and write
  only B4R2 review evidence.
- [ ] Independent Implementer: separately commit the unchanged approved B4R2 review record.
- [ ] Planner: verify the B4R2 record and dispatch S5 only then.
- [ ] Independent Implementer: create sole non-merge S5 over the preserved exact 15-path allowlist.
- [ ] Tester: create factual same-S5 B4R2 T5 evidence only, without routing/lifecycle/status/
  `next_gate` fields.
- [ ] Reviewer: require same-S5 passing T5, create V5, and prove actual named non-merge
  `S5 -> T5 -> V5` with `git diff --name-status S5..V5` listing only B4R2 T5/V5 paths.
- [ ] Stop at the Human boundary; do not act on PR threads, merge, release or post-merge.
