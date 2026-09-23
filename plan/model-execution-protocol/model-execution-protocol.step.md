---
topic: model-execution-protocol
phase: phase-4.5-alignment-pending
created: 2026-09-22
---

# model-execution-protocol — Step Tracking

> **Executor**: 只有 action owner 可在精確 evidence 成立後將對應 step 標為 `[X]`。
> `## Implementation Steps` 全部完成，才可提交 independent implementation review。

## Workflow Stages

- [X] plan-authoring
- [X] plan-review
- [X] planning-amendment-review
- [X] tdd-test-authoring
- [X] implementation
- [X] implementation-review
- [ ] code-review

## Actionable Steps

- [X] **Actor:** Implementer — **Action:** 將五份 initial planning artifacts 以唯一 planning-candidate commit 提交；不得混入 code 或 evidence。
- [X] **Actor:** Independent Plan-Reviewer — **Action:** 審查 committed five-path candidate，寫入 full-SHA-bound `plan/model-execution-protocol/model-execution-protocol.plan-review-receipt.json`。
- [X] **Actor:** Implementer — **Action:** 原樣以 sole evidence-only commit 提交 Plan-Reviewer receipt，等待 Planner 依 verdict route。
- [X] **Actor:** Plan-Creator — **Action:** 只在本 topic planning paths 起草 Human 指示的 `protocol.py` 結構 amendment 與對應 transition；舊 approved candidate/receipt 保持 immutable provenance。
- [X] **Actor:** Implementer — **Action:** 只提交本次修訂的 planning artifacts，建立新的 immutable planning candidate；不得混入 code、receipt 或其他 evidence。
- [X] **Actor:** Independent Plan-Reviewer — **Action:** 只審新 committed candidate，寫入三欄 `plan/model-execution-protocol/model-execution-protocol.amendment-plan-review-receipt.json`；不覆寫舊 receipt。
- [X] **Actor:** Implementer — **Action:** 原樣以 sole evidence-only commit 提交 amendment receipt，第一 parent 必須是新 candidate commit；交 Planner 依 Git binding 與 verdict re-route。`needs-rework` 返回 Plan-Creator，只有新 `approved` 可進 implementation。
- [X] **Actor:** Implementer — **Action:** 在 approved planning receipt 與 Planner route 後，只以四份 declared implementation paths 建 immutable subject `868df3b338e022371a55a2125b270a52ba1c6874`。
- [X] **Actor:** Tester — **Action:** 對 immutable subject 執行驗證，寫入 actual command/exit-code evidence；Implementer 已原樣以 passing evidence sole commit `12bdfb1b5350ee71e3af70df38a462ce9286fba5` 提交。
- [X] **Actor:** Independent Reviewer — **Action:** 已只消費 immutable subject `868df3b338e022371a55a2125b270a52ba1c6874` 的 committed passing Tester evidence sole commit `12bdfb1b5350ee71e3af70df38a462ce9286fba5`，並由 Implementer 原樣以 approved review evidence sole commit `dee1740b73d0274445d0c3967272d0475d82e779` 提交。

## Implementation Steps

- [X] 1. 新增 `src/deterministic_response_cache/model_execution/outcomes.py`，定義 technical spec 所列 frozen/slotted port 與 execution outcomes、三種 failure reasons，以及精確 union aliases。
- [X] 2. 新增 `src/deterministic_response_cache/model_execution/ports.py`，定義同步 generic `RuntimeAccess` 與 `ModelInvoker` Protocol，僅 import 本 BC outcomes，不 import Identity、Response Reuse、Loaded Runtime Cache 或 Provider Adapter。
- [X] 3. 新增 `src/deterministic_response_cache/model_execution/protocol.py`，依 technical spec 以 `execute`、`_prepare_and_invoke`、`_invoke` 各自單層 `match/case` 實作 resolve → conditional prepare → invoke mapping，保留 opaque object identity、限制呼叫次數並拒絕 foreign/`None` results。
- [X] 4. 新增 `tests/test_model_execution_protocol.py`，以 direct imports 與 typed fakes 驗證 ready、missing、unavailable、preparation failure、invocation failure、invalid port results、exception propagation 與不觸碰其他 BC 的界線。

## Main Agent Actionable Steps — Fixed Tail

- [ ] 只在 required evidence、Planner Phase 4.5 alignment 與既有 Human authorization 均具備時，派 Implementer 對 declared scope 進行 bounded commit、push 與 draft PR；`pr-open` 後交還 Human review/merge。

## Handoff / Gate Notes

- Source plan：`plan/model-execution-protocol/model-execution-protocol.plan.md`；本 tracker 不代表 Plan-Reviewer approval。
- Topic selector：`topic=model-execution-protocol; branch=topic/model-execution-protocol; managed-path-intent=<repo-parent>/worktrees/model-execution-protocol; primary-worktree=false`。
- Planning receipt、Tester evidence、independent Reviewer evidence 只消費同 topic、同 candidate/subject 的 actual committed evidence，不能跨 topic 重用，也不能由 chat 或 branch 狀態補推。
- 第一個 five-path candidate `5f08dbc610a25fc4ae39eaaac20282f9a94e907d` 與 `needs-rework` receipt commit `64ab26c09831b47599543ce74c61733e052bcd44` 已提交。舊修訂 candidate `07c0a62bdfb640cc02b7370d1af616c970629084` 與其 `approved` receipt sole commit `aa41081300cbf2191b5d5b51c64cc67ebfb5cf1b` 僅保留為 immutable provenance，不再作 active routing authority。本次 amendment active candidate 是 `b2847eb2e7ac0ed65a5bef8c33d13cb3248aee99`；Independent Plan-Reviewer 的 `approved` amendment receipt 已由 sole evidence-only commit `5145a59be17a3845da074d88e8530b59bfb45e57` 提交，Planner 已以 Git candidate commit/tree、五份 planning artifact blobs 與 receipt commit 核對 binding 成立。後續 implementation route 仍須由 Planner 判定，不由本 tracker 自行宣告。
- Phase 4.5 alignment binding：active planning candidate `b2847eb2e7ac0ed65a5bef8c33d13cb3248aee99`、approved amendment Plan-Reviewer receipt sole commit `5145a59be17a3845da074d88e8530b59bfb45e57`、immutable implementation subject `868df3b338e022371a55a2125b270a52ba1c6874`、passing Tester evidence sole commit `12bdfb1b5350ee71e3af70df38a462ce9286fba5` 與 approved Independent Reviewer evidence sole commit `dee1740b73d0274445d0c3967272d0475d82e779` 已綁定；Planner Phase 4.5 alignment 尚待判定，本 tracker 不自行宣告 publish 完成、PR review 或 merge，亦未記錄 remote 或 PR。
- PR #7 實際 runtime contract 未鎖定；本 topic 以本地 injected port/test doubles 驗證，未來接線另行規劃。
- 只有 `## Implementation Steps` 是 implementation-completion gate；Human 獨占 PR review、merge、release、post-merge、tag 與 final summary。
