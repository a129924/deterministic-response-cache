---
topic: observer-dispatcher-governance
correction: high-b4r3
state: PLANNER_REPLAN
---

# B4R3 Correction Steps

- [X] Freeze `0800dc11181cdbd7d93d85e0298ea78dc33d06d3` B4R2 and its failed clean review as
  nonrouting provenance.
- [X] Create only the seven-path B4R3 planning delta.
- [ ] Independent Implementer: commit exactly the seven B4R3 planning paths as non-subject B4R3.
- [ ] Independent Plan-Reviewer: from clean B4R3 checkout, review the seven committed blobs and
  write only B4R3 review evidence.
- [ ] Independent Implementer: separately commit the unchanged approved B4R3 review record.
- [ ] Planner: verify the B4R3 record and dispatch S5 only then.
- [ ] Independent Implementer: create sole non-merge S5 over the preserved exact 15-path allowlist.
- [ ] Tester: create factual same-S5 B4R3 T5 evidence only, without routing/lifecycle/status/
  `next_gate` fields.
- [ ] Reviewer: require same-S5 passing T5, create V5, and prove actual named non-merge
  `S5 -> T5 -> V5` with `git diff --name-status S5..V5` listing only B4R3 T5/V5 paths.
- [ ] Stop at the Human boundary; do not act on PR threads, merge, release or post-merge.
