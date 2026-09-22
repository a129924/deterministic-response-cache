---
topic: model-execution-protocol
phase: plan-review
created: 2026-09-22
---

# model-execution-protocol — Step Tracking

> **Executor**: 只有 action owner 可在精確 evidence 成立後將對應 step 標為 `[X]`。
> `## Implementation Steps` 全部完成，才可提交 independent implementation review。

## Workflow Stages

- [X] plan-authoring
- [X] plan-review
- [ ] tdd-test-authoring
- [ ] implementation
- [ ] implementation-review
- [ ] code-review

## Actionable Steps

- [X] **Actor:** Implementer — **Action:** 將五份 initial planning artifacts 以唯一 planning-candidate commit 提交；不得混入 code 或 evidence。
- [X] **Actor:** Independent Plan-Reviewer — **Action:** 審查 committed five-path candidate，寫入 full-SHA-bound `plan/model-execution-protocol/model-execution-protocol.plan-review-receipt.json`。
- [X] **Actor:** Implementer — **Action:** 原樣以 sole evidence-only commit 提交 Plan-Reviewer receipt，等待 Planner 依 verdict route。
- [ ] **Actor:** Implementer — **Action:** 在 approved planning receipt 與 Planner route 後，只以四份 declared implementation paths 建 immutable subject。
- [ ] **Actor:** Tester — **Action:** 對 immutable subject 執行驗證，寫入 actual command/exit-code evidence；Implementer 原樣單獨提交。
- [ ] **Actor:** Independent Reviewer — **Action:** 只消費 committed passing same-subject Tester evidence，寫入 review evidence；Implementer 原樣單獨提交。

## Implementation Steps

- [ ] 1. 新增 `src/deterministic_response_cache/model_execution/outcomes.py`，定義 technical spec 所列 frozen/slotted port 與 execution outcomes、三種 failure reasons，以及精確 union aliases。
- [ ] 2. 新增 `src/deterministic_response_cache/model_execution/ports.py`，定義同步 generic `RuntimeAccess` 與 `ModelInvoker` Protocol，僅 import 本 BC outcomes，不 import Identity、Response Reuse、Loaded Runtime Cache 或 Provider Adapter。
- [ ] 3. 新增 `src/deterministic_response_cache/model_execution/protocol.py`，依 technical spec 實作 constructor 與 `execute` 的 resolve → conditional prepare → invoke mapping，保留 opaque object identity、限制呼叫次數並拒絕 foreign/`None` results。
- [ ] 4. 新增 `tests/test_model_execution_protocol.py`，以 direct imports 與 typed fakes 驗證 ready、missing、unavailable、preparation failure、invocation failure、invalid port results、exception propagation 與不觸碰其他 BC 的界線。

## Main Agent Actionable Steps — Fixed Tail

- [ ] 只在 required evidence、Planner Phase 4.5 alignment 與既有 Human authorization 均具備時，派 Implementer 對 declared scope 進行 bounded commit、push 與 draft PR；`pr-open` 後交還 Human review/merge。

## Handoff / Gate Notes

- Source plan：`plan/model-execution-protocol/model-execution-protocol.plan.md`；本 tracker 不代表 Plan-Reviewer approval。
- Topic selector：`topic=model-execution-protocol; branch=topic/model-execution-protocol; managed-path-intent=<repo-parent>/worktrees/model-execution-protocol; primary-worktree=false`。
- Planning receipt、Tester evidence、independent Reviewer evidence 只消費同 topic、同 candidate/subject 的 actual committed evidence，不能跨 topic 重用，也不能由 chat 或 branch 狀態補推。
- 第一個 five-path candidate `5f08dbc610a25fc4ae39eaaac20282f9a94e907d` 與 `needs-rework` receipt commit `64ab26c09831b47599543ce74c61733e052bcd44` 已提交；Planner 已派 Plan-Creator 修訂。修訂 candidate `07c0a62bdfb640cc02b7370d1af616c970629084` 的 `approved` Plan-Reviewer receipt 已由 sole evidence-only commit `aa41081300cbf2191b5d5b51c64cc67ebfb5cf1b` 提交；目前等待 Planner route，後續 phase 須由 committed evidence 和 Planner 判定。首個 candidate 的提交 checkbox 已由該 action owner 核對 Git 後更新。
- PR #7 實際 runtime contract 未鎖定；本 topic 以本地 injected port/test doubles 驗證，未來接線另行規劃。
- 只有 `## Implementation Steps` 是 implementation-completion gate；Human 獨占 PR review、merge、release、post-merge、tag 與 final summary。
