---
topic: observer-dispatcher-governance
correction: high-b4r4
state: PLANNER_REPLAN
---

# B4R5 Current Steps

- [X] Freeze `8190dbb` B4R4 and its bootstrap-test route as nonrouting provenance.
- [X] Plan-Creator: synchronize exactly the seven B4R5 planning paths and create B4R5 plan/step.
- [ ] Independent Implementer: commit exactly the seven B4R5 baseline paths as non-subject; report
  named `8190dbb..<B4R5-SHA>` path diff.
- [ ] Independent Plan-Reviewer: clean-checkout review all seven committed B4R5 blobs and write only
  B4R5 review log using the locked seven-blob schema.
- [ ] Independent Implementer: separately commit unchanged approved B4R5 review record.
- [ ] Planner: verify B4R5 approval and dispatch S5 only then.
- [ ] Independent Implementer: make one non-merge S5 over the exact preserved 15-path allowlist,
  including the three future regression assertion groups in the test path only.
- [ ] Tester: write factual same-S5 B4R5 T5 evidence only.
- [ ] Reviewer: require same-S5 passing T5, write V5, and prove named actual-SHA `S5..V5` contains
  only B4R5 T5/V5 evidence paths.
- [ ] Stop at the Human boundary; do not resolve PR threads, merge, release or post-merge.

## Superseded B4R4 Tracker (Frozen)

- [X] Freeze `8b87aab` B4R3 and its failed clean review as nonrouting provenance.
- [X] Plan-Creator: synchronize exactly the seven B4R4 planning paths and create B4R4 plan/step.
- [ ] Independent Implementer: apply only B4R4 fixed test adaptation and commit exactly the eight
  B4R4 baseline paths as non-subject; report named `8b87aab..<B4R4-SHA>` path diff.
- [ ] Independent Plan-Reviewer: clean-checkout review all eight committed B4R4 blobs and write only
  B4R4 review log.
- [ ] Independent Implementer: separately commit unchanged approved B4R4 review record.
- [ ] Planner: verify B4R4 approval and dispatch S5 only then.
- [ ] Independent Implementer: make one non-merge S5 over the exact preserved 15-path allowlist.
- [ ] Tester: write factual same-S5 B4R4 T5 evidence only.
- [ ] Reviewer: require same-S5 passing T5, write V5, and prove named actual-SHA `S5..V5` contains
  only B4R4 T5/V5 evidence paths.
- [ ] Stop at the Human boundary; do not resolve PR threads, merge, release or post-merge.

## Frozen History

B0–B4R3, S1–S4, T1–T4, V1–V4, normal/recovery records and their steps/checklists are frozen
nonrouting provenance. They are not current pending boxes and may not be reopened or used to route
B4R4. The two `step-creator` deferred steps remain deferred.
