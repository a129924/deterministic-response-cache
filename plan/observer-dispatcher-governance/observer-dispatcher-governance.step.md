---
topic: observer-dispatcher-governance
correction: high-b4r6
state: PLANNER_REPLAN
---

# B4R6 Current Steps

- [X] Freeze `b900366` and B0–B4R5 as nonrouting provenance.
- [X] Plan-Creator: synchronize exactly the seven B4R6 planning paths and create B4R6 plan/step.
- [ ] Independent Implementer: commit exactly the seven B4R6 baseline paths as non-subject; report
  named `b900366..<B4R6-SHA>` path diff.
- [ ] Independent Plan-Reviewer: clean-checkout review all seven committed B4R6 blobs and write only
  B4R6 review log using the locked seven-blob schema.
- [ ] Independent Implementer: separately commit unchanged approved B4R6 review record.
- [ ] Planner: verify B4R6 approval and dispatch S6 only then.
- [ ] Independent Implementer: make one non-merge S6 over the exact preserved 15-path allowlist and
  add only B4R6 declared regression assertions to the test path.
- [ ] Tester: write factual same-S6 B4R6 T6 evidence only.
- [ ] Reviewer: require same-S6 passing T6, write V6, and prove named actual-SHA `S6..V6` contains
  only B4R6 T6/V6 evidence paths.
- [ ] Stop at the Human boundary; do not resolve PR threads, merge, release or post-merge.

## Frozen History

All B0–B4R5 trackers and their pending boxes are frozen nonrouting provenance; they may not be
reopened or used to route B4R6. The two `step-creator` deferred steps remain deferred.
