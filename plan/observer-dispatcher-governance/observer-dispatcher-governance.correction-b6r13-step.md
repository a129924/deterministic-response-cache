---
topic: observer-dispatcher-governance
correction: high-b6r13
state: R23_REVIEW_PENDING
---

# B6R13 Correction Steps

- [x] Planner defines B6R13 runtime/wrapper alignment and freezes B6R12/R22/S16-Q16, B6R10/R20 and earlier provenance.
- [x] Plan-Creator writes exactly eight B6R13 planning paths.
- [ ] Independent Implementer commits B6R13 as a non-merge first-parent exact-eight admission.
- [ ] Independent Plan-Reviewer reviews the committed B6R13 clean checkout and writes only R23, validating eight
      path/blob records, first-parent exact-eight admission, frozen predecessor receipts, Copilot triage and conditional
      approval semantics.
- [ ] Independent Implementer commits unchanged approved R23; only then Planner selects `R23_COMPLETE_S17_NEXT` and S17.
- [ ] Implementer changes only S17 exact fourteen allowlisted paths; direct imports remain direct.
- [ ] Tester writes factual actual-exit-code T17 after same-S17 execution.
- [ ] Reviewer writes V17 only after committed same-S17 passing T17, then Q17 only after committed V17.
- [ ] Independent Reviewer classifies threads after active passed Q17. Only named addressed-and-resolvable threads may be
      replied to/resolved by bounded Implementer action.
- [ ] Stop at Human boundary; do not merge, release or post-merge.
