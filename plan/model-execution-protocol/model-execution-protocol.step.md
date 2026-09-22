---
topic: model-execution-protocol
phase: planning-amendment-in-progress
created: 2026-09-22
---

# model-execution-protocol — Step Tracking

> **Executor**: 只有 action owner 可在精確 evidence 成立後將對應 step 標為 `[X]`。
> `## Implementation Steps` 全部完成，才可提交 independent implementation review。

## Workflow Stages

- [X] plan-authoring
- [X] plan-review
- [ ] planning-amendment-review
- [ ] tdd-test-authoring
- [ ] implementation
- [ ] implementation-review
- [ ] code-review

## Actionable Steps

- [X] **Actor:** Implementer — **Action:** 將五份 initial planning artifacts 以唯一 planning-candidate commit 提交；不得混入 code 或 evidence。
- [X] **Actor:** Independent Plan-Reviewer — **Action:** 審查 committed five-path candidate，寫入 full-SHA-bound `plan/model-execution-protocol/model-execution-protocol.plan-review-receipt.json`。
- [X] **Actor:** Implementer — **Action:** 原樣以 sole evidence-only commit 提交 Plan-Reviewer receipt，等待 Planner 依 verdict route。
- [X] **Actor:** Plan-Creator — **Action:** 只在本 topic planning paths 起草 Human 指示的 `protocol.py` 結構 amendment 與對應 transition；舊 approved candidate/receipt 保持 immutable provenance。
- [ ] **Actor:** Implementer — **Action:** 只提交本次修訂的 planning artifacts，建立新的 immutable planning candidate；不得混入 code、receipt 或其他 evidence。
- [ ] **Actor:** Independent Plan-Reviewer — **Action:** 只審新 committed candidate，寫入三欄 `plan/model-execution-protocol/model-execution-protocol.amendment-plan-review-receipt.json`；不覆寫舊 receipt。
- [ ] **Actor:** Implementer — **Action:** 原樣以 sole evidence-only commit 提交 amendment receipt，第一 parent 必須是新 candidate commit；交 Planner 依 Git binding 與 verdict re-route。`needs-rework` 返回 Plan-Creator，只有新 `approved` 可進 implementation。
- [ ] **Actor:** Implementer — **Action:** 在 approved planning receipt 與 Planner route 後，只以四份 declared implementation paths 建 immutable subject。
- [ ] **Actor:** Tester — **Action:** 對 immutable subject 執行驗證，寫入 actual command/exit-code evidence；Implementer 原樣單獨提交。
- [ ] **Actor:** Independent Reviewer — **Action:** 只消費 committed passing same-subject Tester evidence，寫入 review evidence；Implementer 原樣單獨提交。

## Implementation Steps

- [ ] 1. 新增 `src/deterministic_response_cache/model_execution/outcomes.py`，定義 technical spec 所列 frozen/slotted port 與 execution outcomes、三種 failure reasons，以及精確 union aliases。
- [ ] 2. 新增 `src/deterministic_response_cache/model_execution/ports.py`，定義同步 generic `RuntimeAccess` 與 `ModelInvoker` Protocol，僅 import 本 BC outcomes，不 import Identity、Response Reuse、Loaded Runtime Cache 或 Provider Adapter。
- [ ] 3. 新增 `src/deterministic_response_cache/model_execution/protocol.py`，依 technical spec 以 `execute`、`_prepare_and_invoke`、`_invoke` 各自單層 `match/case` 實作 resolve → conditional prepare → invoke mapping，保留 opaque object identity、限制呼叫次數並拒絕 foreign/`None` results。
- [ ] 4. 新增 `tests/test_model_execution_protocol.py`，以 direct imports 與 typed fakes 驗證 ready、missing、unavailable、preparation failure、invocation failure、invalid port results、exception propagation 與不觸碰其他 BC 的界線。

## Main Agent Actionable Steps — Fixed Tail

- [ ] 只在 required evidence、Planner Phase 4.5 alignment 與既有 Human authorization 均具備時，派 Implementer 對 declared scope 進行 bounded commit、push 與 draft PR；`pr-open` 後交還 Human review/merge。

## Handoff / Gate Notes

- Source plan：`plan/model-execution-protocol/model-execution-protocol.plan.md`；本 tracker 不代表 Plan-Reviewer approval。
- Topic selector：`topic=model-execution-protocol; branch=topic/model-execution-protocol; managed-path-intent=<repo-parent>/worktrees/model-execution-protocol; primary-worktree=false`。
- Planning receipt、Tester evidence、independent Reviewer evidence 只消費同 topic、同 candidate/subject 的 actual committed evidence，不能跨 topic 重用，也不能由 chat 或 branch 狀態補推。
- 第一個 five-path candidate `5f08dbc610a25fc4ae39eaaac20282f9a94e907d` 與 `needs-rework` receipt commit `64ab26c09831b47599543ce74c61733e052bcd44` 已提交；修訂 candidate `07c0a62bdfb640cc02b7370d1af616c970629084` 的 `approved` Plan-Reviewer receipt 已由 sole evidence-only commit `aa41081300cbf2191b5d5b51c64cc67ebfb5cf1b` 提交。前三個 `[X]` 是過往 planning actions，不是本次 amendment approval。Human 已指示以本次 `protocol.py` 結構 amendment 取代舊 approved candidate；舊 candidate/receipt 是 immutable provenance，不得審查或核准新修訂。新 candidate SHA 和 verdict 尚未產生；新三欄 receipt 只能由 Independent Plan-Reviewer 對 committed candidate 寫入，Implementer 原樣 sole evidence-only commit 且其第一 parent 為新 candidate commit 後，Planner 以 Git candidate commit/tree、五份 planning artifact blobs 與 receipt commit 核對 binding 並 re-route；在此之前沒有可供實作的 active candidate，任一時點不得有兩個 active candidates。
- PR #7 實際 runtime contract 未鎖定；本 topic 以本地 injected port/test doubles 驗證，未來接線另行規劃。
- 只有 `## Implementation Steps` 是 implementation-completion gate；Human 獨占 PR review、merge、release、post-merge、tag 與 final summary。
