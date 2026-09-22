---
topic: loaded-runtime-cache
phase: plan-review-pending
created: 2026-09-17
---

# loaded-runtime-cache — Step Tracking

## Workflow Stages

- [x] plan-authoring
- [ ] planning-candidate-commit
- [ ] plan-review
- [ ] tdd-test-authoring
- [ ] implementation
- [ ] implementation-review
- [ ] code-review

## Actionable Steps

- [ ] **Actor:** Implementer — **Action:** Commit C10 as exactly the five planning artifacts on the existing Loaded
  Runtime Cache source ancestor. It carries no source, tests, architecture, evidence or receipts. The candidate SHA
  remains absent from planning text and is routed only by Planner from committed evidence.
- [ ] **Actor:** Independent Plan-Reviewer — **Action:** Review only the committed C10 candidate and, only after it
  exists, write `plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<planning-candidate-40-hex-sha>.json`
  using the locked normal-plan receipt schema. Each candidate gets one immutable non-overwritable SHA-bound receipt.
- [ ] **Actor:** Implementer — **Action:** Commit unchanged C10 Plan-Reviewer receipt as a sole evidence-only commit.
  Only its committed `approved` verdict can be routed by Planner for implementation.

## Implementation Steps

- [ ] 1. **Reuse frozen provenance:** Treat C5→V3 architecture/dataflow/source artifacts and C8/C9 unapproved planning
  predecessors as ReadOnly. Do not modify, regenerate or reclassify them as C10 implementation evidence; F ownership
  remains Human-only.
- [ ] 2. **C10 isolated assertion subject:** After the C10 approved receipt is committed, modify exactly
  `tests/test_loaded_runtime_cache_contracts.py` and `tests/test_loaded_runtime_cache_bc_independence.py`, adding one
  isolated executable RED assertion to each. The subject contains no production source, architecture, Archify artifact
  or evidence; assertions cover opaque identity and all specified dynamic-import/duplicate-type regressions.
- [ ] 3. **Executable validation:** Run the locked Ruff, strict Pyright, targeted/full pytest and package-import
  regression commands against the C10 subject. Assertions execute against the existing source ancestor; their actual
  result is not an expected-nonzero historical RED record.
- [ ] 4. **T10:** Tester writes only fresh SHA-bound T10 factual evidence for the C10 assertion subject; an Implementer
  commits it unchanged in a sole evidence-only commit. Failing T10 returns to Implementer.
- [ ] 5. **V10:** Independent Reviewer consumes only committed passing T10 for the same C10 subject, writes V10, and an
  Implementer commits it unchanged in a sole evidence-only commit. C5/T3/V3, C8/C9 and legacy evidence cannot be reused.

## Main Agent Actionable Steps — Fixed Tail

- [ ] **Actor:** Planner — **Action:** 對已提交的 C10→T10→V10 evidence chain 執行 Phase 4.5 alignment。只有通過後，才可
  派遣獨立 Reviewer 分類 current PR threads；本項不代表 PR classification、thread reply／resolution、F ownership
  human-check、publish 或 Human action 已完成。

## Handoff / Gate Notes

- This tracker and plan name one `loaded-runtime-cache` topic. The feature branch is lineage only, not routing
  authority.
- C5 `505c30609f5d65030a2eda740d8135b768cc06ca` and its successor evidence are frozen nonrouting provenance for C10.
  C8/C9 are frozen, unapproved predecessor planning candidates with no routing authority. C10 starts on the existing
  source ancestor; it does not replay a clean base or recreate historical source-absent gates.
- The fixed-name legacy plan-review receipt is historical frozen provenance only; it cannot be overwritten, consumed
  or used to route C5 or any successor. A `needs-rework` receipt creates no implementation subject.
- Architecture-only `442cc94`, historical RED/green subjects, T3 and V3 are frozen provenance only. C10 reuses the
  already implemented source and architecture evidence but must create fresh T10/V10 paths for its own assertion subject.
- C10 has no expected-nonzero RED JSON. Its two test assertions execute against existing source; Human alone reviews
  and merges a draft PR.
- Architecture-path overlap is Human review／merge coordination only; it never relaxes declared paths or evidence
  gates.
- C10 is the sole active planning candidate and awaits its candidate-only commit. After that commit, the next routing
  action is independent Plan-Reviewer review pending. Only after C10 T10/V10 and
  Planner Phase 4.5 alignment may an independent Reviewer classify current PR threads; this tracker does not mark code
  review, publish, comments, F ownership, or Human actions complete.
