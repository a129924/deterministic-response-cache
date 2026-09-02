---
topic: observer-dispatcher-governance
correction: high-b4r7
state: B4R7_REVIEW_PENDING
---

# B4R7 Current Steps

- [X] Freeze `b900366`, B0–B4R6, `7d23e8c`, `6ede06b`, normal/recovery evidence, and any uncommitted
  B4R6 review-log as nonrouting provenance.
- [X] Plan-Creator: synchronize exactly the seven B4R7 planning paths and create B4R7 plan/step.
- [ ] Independent Implementer: make the first B4R7 admission commit. It must be non-merge, contain the
  complete exact seven-path baseline, and pass named first-parent `git diff --name-status` admission;
  it may not embed a SHA or `HEAD` in planning artifacts.
- [ ] Independent Plan-Reviewer: review all actual committed B4R7 blobs once and write only the B4R7 R7
  review log using the locked seven-blob schema.
- [ ] Independent Implementer: separately commit unchanged approved R7 review record.
- [ ] Planner: verify R7 approval and dispatch S6 only then.
- [ ] Independent Implementer: make one non-merge S6 over the exact preserved 15-path allowlist and add
  only B4R7 declared regression assertions to the test path.
- [ ] Tester: write factual same-S6 B4R7 T6 evidence only.
- [ ] Reviewer: require same-S6 passing T6, write V6, and prove named actual-SHA `S6..V6` contains only
  B4R7 T6/V6 evidence paths.
- [ ] Stop at the Human boundary; do not resolve PR threads, merge, release or post-merge.

## Frozen History

All B0–B4R6 trackers, their pending boxes, and uncommitted B4R6 review work are frozen nonrouting
provenance. The two `step-creator` deferred steps remain deferred.
