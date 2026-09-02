---
topic: observer-dispatcher-governance
correction: high-b4r7
state: B4R7_REVIEW_PENDING
---

# B4R7 Correction Steps

- [X] Define B4R7 as the sole current non-subject baseline; freeze B4R6 and older history.
- [ ] Independent Implementer: create the first non-merge B4R7 baseline commit with exactly the seven
  declared paths; report the named first-parent exact diff admission.
- [ ] Independent Plan-Reviewer: clean-checkout-review all seven actual B4R7 blobs and write only R7.
- [ ] Independent Implementer: separately commit unchanged approved R7 record.
- [ ] Planner: verify approved R7 and dispatch S6 over the unchanged 15-path allowlist.
- [ ] Tester then Reviewer: write B4R7 T6/V6 only; prove named non-merge `S6 -> T6 -> V6` and exact
  `S6..V6` evidence-only range.
- [ ] Stop at Human boundary.
