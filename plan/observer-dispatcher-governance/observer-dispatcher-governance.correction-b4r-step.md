---
topic: observer-dispatcher-governance
correction: high-b4r
state: PLANNER_REPLAN
---

# B4R Correction Steps

- [X] Freeze `B4=979798e` as failed, unapproved, non-subject provenance and retain all prior epochs as frozen nonrouting provenance.
- [X] Create the six-path B4R planning delta only.
- [ ] Independent Implementer: commit exactly the six B4R planning paths as non-subject B4R.
- [ ] Independent Plan-Reviewer: from a clean B4R checkout, review its six committed blobs and write only B4R review evidence.
- [ ] Independent Implementer: separately commit the unchanged approved B4R review record.
- [ ] Planner: verify the approved separately committed B4R record and dispatch S5 only then.
- [ ] Independent Implementer: create sole non-merge S5 over the exact 15-path allowlist, including `.codex/agents/reviewer.toml`.
- [ ] Tester: create factual same-S5 B4R T5 evidence only, with no routing, lifecycle, status, or `next_gate` fields.
- [ ] Reviewer: require same-S5 passing B4R T5, create V5, and prove exact named non-merge `S5 -> T5 -> V5` with `git diff --name-status S5..V5` listing only B4R T5/V5 paths.
- [ ] Stop at the Human boundary; do not act on PR threads, merge, release, or post-merge.
