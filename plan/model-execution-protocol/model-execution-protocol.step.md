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
- [X] architecture-amendment-plan-review
- [X] architecture-amendment-rereview
- [X] architecture-correction
- [X] architecture-correction-test
- [X] review-parent-workflow-amendment-review
- [X] review-parent-status-sync
- [X] architecture-correction-review
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
- [X] **Actor:** Human／Planner — **Action:** Human 指示處理 thread `PRRT_kwDOUJTij86lAh0Z`；Planner 將其分類為狹窄 architecture status transition，phase 為 `planning-amendment-pending`，next role 為 Plan-Creator。
- [X] **Actor:** Plan-Creator — **Action:** 只修改五份既有 planning artifacts，記錄 exact-five docs scope、locked status semantics、新 evidence schemas 與 correction route；不得修改 architecture docs、Python、tests 或既有 evidence。
- [X] **Actor:** Implementer — **Action:** 已將且只將五份 planning artifacts 提交為 immutable architecture-amendment candidate `d43621f2a604f206bbbd50684a3672bd84a1cfb9`；未混入 docs correction 或 evidence。
- [X] **Actor:** Independent Plan-Reviewer — **Action:** 已審查 committed candidate，僅寫 `model-execution-protocol.architecture-amendment-plan-review-receipt.json`，verdict 為 `needs-rework`；未自行 commit 或 route。
- [X] **Actor:** Implementer — **Action:** 已原樣以 sole one-path evidence-only commit `50cd69e7178597e7ffa61da02339ce45cd1a6e44` 提交 `needs-rework` receipt；Planner 已驗證 binding 並 route 回 Plan-Creator。
- [X] **Actor:** Plan-Creator — **Action:** 只修正 source plan 的 `### Rollback Plan`，將 rollback／superseding correction 限定於五個 declared architecture paths，保持 predecessor `src/`／`tests/` blobs 與 committed provenance 不變，並保留 merge 後 Human boundary；step tracker 只同步本輪事實。
- [X] **Actor:** Implementer — **Action:** 已只提交本輪 corrected `plan.md` 與 `step.md`，建立 immutable planning candidate `7d3475a9094da522d31f611a1a7fba4b5d2eaeef`；未混入 receipt、docs correction 或其他 path。
- [X] **Actor:** Independent Plan-Reviewer — **Action:** 已只審 committed corrected candidate `7d3475a9094da522d31f611a1a7fba4b5d2eaeef`，更新專用 architecture-amendment receipt並記錄 `approved`；未自行 commit 或 route。
- [X] **Actor:** Implementer — **Action:** 已原樣以 sole one-path evidence-only commit `793376603b1a67a3e1b5a186df1c5a050018fd1f` 提交 updated `approved` receipt；Planner 已驗證 corrected candidate binding。
- [X] **Actor:** Planner／Implementer — **Action:** Planner 已依 committed approved receipt route；Implementer 已只修改 exact-five architecture docs，建立 immutable docs-only subject `5f483a05e63c9dc8f3c63b04a63c8adec3ed2e28`。
- [X] **Actor:** Tester／Implementer — **Action:** Tester 已對 exact-five subject `5f483a05e63c9dc8f3c63b04a63c8adec3ed2e28` 寫 factual architecture-correction evidence；Implementer 已原樣以 passing evidence sole commit `f71de2beb9801cf01c37d02bca658ee0d8f28599` 提交。
- [X] **Actor:** Human／Planner — **Action:** Human 已選擇 review-parent workflow amendment 並保留既有 commit history；Planner route 的唯一 next role 為 Plan-Creator。subject `5f483a05e63c9dc8f3c63b04a63c8adec3ed2e28` 與 passing Tester evidence `f71de2beb9801cf01c37d02bca658ee0d8f28599` 保持完成且 immutable。
- [X] **Actor:** Plan-Creator — **Action:** 只修改 topic plan/step，鎖定新 planning receipt、status-sync first-parent ancestry、Reviewer reconfirmation 與 review-log direct-parent contract；不修改或採信現有 untracked review log。
- [X] **Actor:** Implementer — **Action:** 已只提交本輪 topic plan/step，建立 exact-two workflow-amendment planning candidate `7e9343a7e13cd47b5c0d85a18da491f813ec7de8`；未納入 untracked review log 或其他 path。
- [X] **Actor:** Independent Plan-Reviewer — **Action:** 已只審 committed exact-two candidate `7e9343a7e13cd47b5c0d85a18da491f813ec7de8`，寫 `model-execution-protocol.review-parent-amendment-plan-review-receipt.json` 並記錄 `approved`；未自行 commit 或 route。
- [X] **Actor:** Implementer — **Action:** 已原樣以 sole one-path evidence-only commit `aa816fbad9fb7ce48ba426c8aa4dd6e68d5b87ec` 提交新 `approved` receipt，direct parent 為 planning candidate `7e9343a7e13cd47b5c0d85a18da491f813ec7de8`；Planner 已驗證 binding。
- [X] **Actor:** Implementer／Planner — **Action:** Planner 已驗證 committed approved receipt；Implementer 以本次新的 sole-step status-sync commit 同步 review-ready 狀態。此 commit 是 single-parent、direct parent 為 receipt commit `aa816fbad9fb7ce48ba426c8aa4dd6e68d5b87ec`、只修改本 step，且 first-parent ancestry 包含 `f71de2beb9801cf01c37d02bca658ee0d8f28599`；本身 SHA 不預填，Planner 將於 commit 後再驗證 topology。
- [X] **Actor:** Independent Reviewer — **Action:** 已在 Planner 驗證 status-sync commit `51480a9b292b4099d14ee03ec5e62917047bb3b5` 後，fresh 重新審查 subject `5f483a05e63c9dc8f3c63b04a63c8adec3ed2e28`、Tester evidence `f71de2beb9801cf01c37d02bca658ee0d8f28599`、first-parent ancestry 與 schema，結論為 `approved` 且 blocking issues 為空。
- [X] **Actor:** Implementer — **Action:** 已將 Reviewer fresh 確認的原樣 correction review log 以 sole evidence commit `70aa86643577e5a4e6011aaec56c287c3e1205f1` 提交；direct parent 是 verified status-sync `51480a9b292b4099d14ee03ec5e62917047bb3b5`，兩者間沒有其他 commit。
- [ ] **Actor:** Planner／Implementer／Independent Reviewer — **Action:** Planner 完成 Phase 4.5 alignment 後，Implementer 才 push 到同一 PR；Reviewer 重新分類 exact thread。只有 `addressed-and-resolvable` 才由 Implementer bounded reply 並 resolve，否則 `human-check`。

## Implementation Steps

- [X] 1. 新增 `src/deterministic_response_cache/model_execution/outcomes.py`，定義 technical spec 所列 frozen/slotted port 與 execution outcomes、三種 failure reasons，以及精確 union aliases。
- [X] 2. 新增 `src/deterministic_response_cache/model_execution/ports.py`，定義同步 generic `RuntimeAccess` 與 `ModelInvoker` Protocol，僅 import 本 BC outcomes，不 import Identity、Response Reuse、Loaded Runtime Cache 或 Provider Adapter。
- [X] 3. 新增 `src/deterministic_response_cache/model_execution/protocol.py`，依 technical spec 以 `execute`、`_prepare_and_invoke`、`_invoke` 各自單層 `match/case` 實作 resolve → conditional prepare → invoke mapping，保留 opaque object identity、限制呼叫次數並拒絕 foreign/`None` results。
- [X] 4. 新增 `tests/test_model_execution_protocol.py`，以 direct imports 與 typed fakes 驗證 ready、missing、unavailable、preparation failure、invocation failure、invalid port results、exception propagation 與不觸碰其他 BC 的界線。

## Main Agent Actionable Steps — Fixed Tail

- [ ] 只在 architecture-amendment receipt、exact-five correction subject、passing Tester evidence、approved Reviewer evidence、Planner Phase 4.5 alignment 與既有 Human authorization均具備時，派 Implementer push 同一 PR；再派 Independent Reviewer 對 thread `PRRT_kwDOUJTij86lAh0Z` 做 same-thread reclassification。只有明確 `addressed-and-resolvable` 才派 Implementer 留 bounded reply 並 resolve；merge 仍屬 Human。

## Handoff / Gate Notes

- Source plan：`plan/model-execution-protocol/model-execution-protocol.plan.md`；本 tracker 不代表 Plan-Reviewer approval。
- Topic selector：`topic=model-execution-protocol; branch=topic/model-execution-protocol; managed-path-intent=<repo-parent>/worktrees/model-execution-protocol; primary-worktree=false`。
- Planning receipt、Tester evidence、independent Reviewer evidence 只消費同 topic、同 candidate/subject 的 actual committed evidence，不能跨 topic 重用，也不能由 chat 或 branch 狀態補推。
- 第一個 five-path candidate `5f08dbc610a25fc4ae39eaaac20282f9a94e907d` 與 `needs-rework` receipt commit `64ab26c09831b47599543ce74c61733e052bcd44` 已提交。舊修訂 candidate `07c0a62bdfb640cc02b7370d1af616c970629084` 與其 `approved` receipt sole commit `aa41081300cbf2191b5d5b51c64cc67ebfb5cf1b` 僅保留為 immutable provenance。predecessor implementation 使用的 planning candidate 是 `b2847eb2e7ac0ed65a5bef8c33d13cb3248aee99`；其 `approved` amendment receipt 已由 sole evidence-only commit `5145a59be17a3845da074d88e8530b59bfb45e57` 提交。兩者均不作本次 architecture correction 的 active routing authority。
- Immutable predecessor provenance：planning candidate `b2847eb2e7ac0ed65a5bef8c33d13cb3248aee99`、approved amendment receipt `5145a59be17a3845da074d88e8530b59bfb45e57`、implementation subject `868df3b338e022371a55a2125b270a52ba1c6874`、passing Tester evidence `12bdfb1b5350ee71e3af70df38a462ce9286fba5`、approved Reviewer evidence `dee1740b73d0274445d0c3967272d0475d82e779` 與 PR HEAD `9a3460b6e4412384ed7e3426ebc32820a46818e6` 均不得改寫。它們證明 predecessor delivery，但舊 Q／approval 不核准本次 architecture correction。
- Current correction id：`model-execution-protocol/pr-comment-architecture-status`；exact thread：`PRRT_kwDOUJTij86lAh0Z`。active approved planning binding 是 corrected candidate `7d3475a9094da522d31f611a1a7fba4b5d2eaeef` 與 updated `approved` receipt sole commit `793376603b1a67a3e1b5a186df1c5a050018fd1f`；active correction validation binding 是 exact-five subject `5f483a05e63c9dc8f3c63b04a63c8adec3ed2e28`、passing Tester evidence sole commit `f71de2beb9801cf01c37d02bca658ee0d8f28599`、verified status-sync `51480a9b292b4099d14ee03ec5e62917047bb3b5` 與 direct-child approved correction review evidence `70aa86643577e5a4e6011aaec56c287c3e1205f1`。Phase 4.5、push、reclassification、reply 與 resolve 尚未完成。
- Architecture-amendment rework provenance：candidate `d43621f2a604f206bbbd50684a3672bd84a1cfb9` 與其 committed `needs-rework` receipt `50cd69e7178597e7ffa61da02339ce45cd1a6e44` 已凍結，只證明前輪 review outcome，不作 active approval；active authority 僅為 corrected candidate `7d3475a9094da522d31f611a1a7fba4b5d2eaeef` 與其 committed `approved` receipt `793376603b1a67a3e1b5a186df1c5a050018fd1f`。
- Exact-five correction subject paths：`docs/business-capability-architecture.md`、`docs/evolution-roadmap.md`、`docs/architecture/business-capability/architecture-brief.md`、`docs/architecture/business-capability/scene.js`、`docs/architecture/business-capability/index.html`。只能是五個 `M` entries；不得 add/delete/rename。
- Locked semantics：同步 coordination ports/outcomes/protocol 已實作；Loaded Runtime Cache 實際 wiring／retention/backend、具體 Provider Adapter、cross-BC composition、Response Reuse `Miss`／result handoff integration 仍 future。Python/tests 相對 `9a3460b6e4412384ed7e3426ebc32820a46818e6` 不變。
- Mirror gate：`scene.js` 必須與 `index.html` 的 `SCENE START (generated)`／`SCENE END` 固定 markers 間內容 byte-for-byte 相同。
- New evidence paths and exact schemas are authoritative in the source plan: `model-execution-protocol.architecture-amendment-plan-review-receipt.json`（Independent Plan-Reviewer）、`model-execution-protocol.architecture-correction-tester-evidence.json`（Tester）、`model-execution-protocol.architecture-correction-implementation-review-log.json`（Independent Reviewer）。三者均由 Implementer 原樣以各自 sole evidence-only commit 提交，且必須綁定同 candidate/subject 的完整 SHA。
- Review-parent workflow binding：exact-two planning candidate `7e9343a7e13cd47b5c0d85a18da491f813ec7de8`、sole approved receipt commit `aa816fbad9fb7ce48ba426c8aa4dd6e68d5b87ec`、correction subject `5f483a05e63c9dc8f3c63b04a63c8adec3ed2e28`、passing Tester evidence `f71de2beb9801cf01c37d02bca658ee0d8f28599`、sole-step status-sync `51480a9b292b4099d14ee03ec5e62917047bb3b5` 與 direct-child sole approved review-log commit `70aa86643577e5a4e6011aaec56c287c3e1205f1` 已綁定。
- Review-parent workflow amendment 的專用 receipt 已由 `aa816fbad9fb7ce48ba426c8aa4dd6e68d5b87ec` 提交；`model-execution-protocol.architecture-correction-implementation-review-log.json` 已由 Independent Reviewer 在 verified status-sync 後 fresh 確認，並由 `70aa86643577e5a4e6011aaec56c287c3e1205f1` 原樣提交。
- Planner Phase 4.5 alignment、push、same-thread reclassification、reply 與 resolve 仍 pending；thread `PRRT_kwDOUJTij86lAh0Z` 保持 unresolved，push、reply 與 resolve 均 blocked。
- PR #7 實際 runtime contract 未鎖定；本 topic 以本地 injected port/test doubles 驗證，未來接線另行規劃。
- predecessor `## Implementation Steps` 的 `[X]` 只保留歷史完成狀態；本次 final PR gate 在新的 architecture correction route 完成前視為未完成。Human 獨占 PR review、merge、release、post-merge、tag 與 final summary。
