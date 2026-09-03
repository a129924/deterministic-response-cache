---
topic: observer-dispatcher-governance
correction: high-b4r6
state: B4R6_REVIEW_PENDING
---

# B4R6 Correction Steps

- [X] Freeze `b900366` and all B0–B4R5 routing semantics as nonrouting provenance.
- [X] Create only the seven B4R6 planning-path delta.
- [X] `7d23e8c595af0a00ae1d122749614b39bf400506` is the immutable completed B4R6 non-subject
  baseline; its named `b900366..7d23e8c595af0a00ae1d122749614b39bf400506` diff is frozen.
- [ ] Independent Plan-Reviewer: from a clean checkout of
  `7d23e8c595af0a00ae1d122749614b39bf400506`, review seven committed blobs and write only B4R6
  review evidence using the locked seven-blob schema.
- [ ] Independent Implementer: separately commit unchanged approved B4R6 review record.
- [ ] Planner: verify B4R6 record and dispatch S6 only then.
- [ ] Independent Implementer: create sole non-merge S6 over exact preserved 15-path allowlist and
  add only B4R6 declared regression assertions to the test path.
- [ ] Tester: create factual same-S6 B4R6 T6 evidence only.
- [ ] Reviewer: require same-S6 passing T6, create V6, and prove actual named non-merge
  `S6 -> T6 -> V6` with `git diff --name-status S6..V6` listing only B4R6 T6/V6 paths.
- [ ] Stop at Human boundary; do not act on PR threads, merge, release, or post-merge.
