---
topic: model-response-codecs
phase: correction-fix-4-plan-authoring
created: 2026-09-24
---

# model-response-codecs — Step Tracking

## Workflow Stages

- [X] plan-authoring
- [X] plan-review
- [ ] tdd-test-authoring
- [X] implementation
- [ ] implementation-review
- [ ] code-review

## Actionable Steps

- [X] **Actor:** Implementer — **Action:** 已只將五份 initial planning artifacts 作為單一 planning candidate commit，交 Independent Plan-Reviewer 審查。
- [X] **Actor:** Independent Plan-Reviewer — **Action:** 已審 committed candidate，依 normal plan-reviewer contract 寫三鍵 JSON verdict；未自行 commit 或 route。
- [X] **Actor:** Implementer — **Action:** 已原樣以 sole evidence-only commit 提交三鍵 approved Plan-Reviewer receipt，並經 Planner route。
- [X] **Actor:** Implementer — **Action:** 已先更新／確認五個 BC 架構面，再建原 immutable implementation subject `5d8873f3088769f1bd8b6da7b42d2ec96b9254f5`。
- [X] **Actor:** Tester／Implementer — **Action:** Tester 已對原 subject 寫 passing factual evidence，Implementer 已原樣 sole evidence-only commit `226b95b2a1c29c7f1103d8f4e11939c29a96f266`。
- [X] **Actor:** Independent Reviewer／Implementer — **Action:** Reviewer 已只消費原 subject 的 committed passing Tester evidence，寫 `needs-rework` log，Implementer 已原樣 sole evidence-only commit `57e4940150157d3cc73799c20461000eacc6bfe2`；此 verdict 阻斷 Q/publish。
- [X] **Actor:** Implementer — **Action:** 已只提交 parent plan/step 與 `fix-1` correction plan/step 的 exact-four candidate `b51e557c535510c7660a4c17229ed1f0c008c4cf`。
- [X] **Actor:** Independent Plan-Reviewer／Implementer — **Action:** Reviewer 已審 committed `fix-1` candidate 並寫 extended `needs-rework` receipt；Implementer 原樣 sole evidence-only commit `4d1a730783d5904f36f5a0a0a43cc69c578a9538`。`fix-1` 沒有實作 authority、subject 或新 Tester/Reviewer evidence。
- [X] **Actor:** Implementer — **Action:** 已只提交 parent plan/step 與 fix-2 correction plan/step 的 exact-four candidate `a45a7d3a31794b9d9ce75c2695efcdee93ebd539`。
- [X] **Actor:** Independent Plan-Reviewer／Implementer — **Action:** fix-2 approved extended receipt 已由 sole evidence-only commit `7277980b9442fc4142b6b9ba11b9e6ecc21ec6cd` 提交並經 Planner route。
- [X] **Actor:** Implementer — **Action:** 只修改 `json_response.py` 與兩個 declared codec tests，建立 exact-three fix-2 subject `3a1c19f3db126f8f87235c47aaf52a98cdcacb50`。
- [X] **Actor:** Tester／Implementer — **Action:** fix-2 passing factual evidence 已由 sole evidence-only commit `b4021849b92a8e67a9342f10504cfaef049336cc` 提交。
- [X] **Actor:** Independent Reviewer／Implementer — **Action:** fix-2 approved Independent Reviewer evidence 已由 sole evidence-only commit `7c474f2ff57c4a0af355e8953929f2d856e66424` 提交；只對該 subject 有效。
- [X] **Actor:** Planner／Implementer — **Action:** fix-2 已經既有 bounded publish gate 開 Draft PR #11 base `dev`；Human 現要求同 topic `needs-rework`，舊 approval 不授權 fix-3。
- [X] **Actor:** Implementer — **Action:** 已只提交 parent plan/step/spec、analysis technical spec 與 fix-3 correction plan/step 的 exact-six candidate `c67f5c23bc2b6f3a6cb1f6b8e883b9ee77a561d1`。
- [X] **Actor:** Independent Plan-Reviewer／Implementer — **Action:** fix-3 approved extended receipt 已由 sole evidence-only commit `4389ddc5b83c65ae4e08976c7e270c567ebdec7b` 提交並經 Planner route。
- [X] **Actor:** Implementer — **Action:** 已只修改 fix-3 exact-eight code/test paths，建立 immutable subject `b9a68575b24472a136bc7f3b826c8e7e581250b2`。
- [X] **Actor:** Tester／Implementer — **Action:** fix-3 passing factual evidence 已由 sole evidence-only commit `2ff945e236aaa76afce61dbac1df62fc860f45c7` 提交。
- [X] **Actor:** Independent Reviewer／Implementer — **Action:** fix-3 Reviewer needs-rework log 已由 sole evidence-only commit `dff896ce0548c8d9c8ae36cabbe60792c9211225` 提交，阻斷 Q/publish；其唯一 blocker 是深層 JSON decode 不回 `InvalidPayload`。
- [ ] **Actor:** Implementer — **Action:** 只提交 parent plan/step M 與 fix-4 correction plan/step A 的 exact-four non-merge planning candidate；不混入 code/evidence。
- [ ] **Actor:** Independent Plan-Reviewer／Implementer — **Action:** Reviewer 審 committed fix-4 candidate，只寫 active extended receipt `correction-fix-4-plan-review-log.json`；Implementer 原樣 sole evidence-only commit，Planner 僅 route committed approved。Needs-rework 停回 Planner／Plan-Creator 新 path。
- [ ] **Actor:** Implementer — **Action:** 只修改 fix-4 exact-four source/test paths，建立新 immutable subject；不得覆寫 initial/fix-1/fix-2/fix-3 evidence。
- [ ] **Actor:** Tester／Implementer — **Action:** Tester 對新 subject 寫 `tester-evidence.fix-4.json` actual command/exit-code evidence；Implementer 原樣 sole evidence-only commit。
- [ ] **Actor:** Independent Reviewer／Implementer — **Action:** Reviewer 只消費同 subject committed passing fix-4 Tester evidence，寫 `implementation-review-log.fix-4.json`；Implementer 原樣 sole evidence-only commit。Tester failing 或 Reviewer needs-rework 停回 Planner／Plan-Creator 宣告新 evidence paths，不可進 Phase 4.5。

## Implementation Steps

- [X] 1. 在 `docs/business-capability-architecture.md`、`docs/evolution-roadmap.md`、`docs/architecture/business-capability/architecture-brief.md`、`docs/architecture/business-capability/scene.js`、`docs/architecture/business-capability/index.html` 先更新 Response Reuse bytes 保存/解碼及 outcomes，維持 Identity/Store/其他 BC 責任與 scene mirror；此時不編輯 Python/source/test/dependency。
- [X] 2. 唯讀核對前述五個 BC 文件與 `AGENTS.md`、本 plan/spec 的責任／演進順序及 `scene.js`／`index.html` generated block mirror；一致性未確認即停回 Planner，不開始 Python，也不建立 subject commit。此為同一 implementation 工作內的架構確認停點，不取代後續 Tester/Reviewer。
- [X] 3. 在 `src/deterministic_response_cache/response_reuse/model_response.py`、`stored_response.py` 建立 frozen/slotted VO 與封閉 `ResponseCodecId`；在 `codecs/contract.py` 定義三 member 的 generic `ResponseCodec` Protocol。
- [X] 4. 在 `src/deterministic_response_cache/response_reuse/codecs/json_response.py` 建立 `JsonPayload` 與明確繼承 `ResponseCodec[JsonPayload]` 的 JSON codec，使用正確 `@property`/`@override` 順序、無損驗證及 UTF-8 bytes。
- [X] 5. 在 `src/deterministic_response_cache/response_reuse/codecs/pyarrow_dataframe.py` 建立明確繼承 `ResponseCodec[pandas.DataFrame]` 的 Arrow IPC codec，使用三個 `@override`，接收完整 `ModelResponse` 並在 encode 內以 `equals` 驗證往返。
- [X] 6. 在 `src/deterministic_response_cache/response_reuse/codecs/selector.py` 建立固定 value/id 分流及分支內 direct imports，讓純 JSON 路徑不載入 pandas/pyarrow；未知 id fail closed，不建立 `codecs.py` 或 `codecs/__init__.py`。
- [X] 7. 在 `src/deterministic_response_cache/response_reuse/outcomes.py`、`protocol.py` 將 public response/Store contract 改為 `ModelResponse`/`StoredResponse`，完整 VO 傳 encoder，加入封閉 failure reasons，保留 Store/policy exception 邊界。
- [X] 8. 在 `pyproject.toml` 新增 pandas/pyarrow 的 `dataframe` optional extra 並更新 `uv.lock`；基礎 JSON 安裝維持無 runtime deps。
- [X] 9. 在 `tests/test_response_reuse_codecs.py`、`tests/test_model_response_codecs_integration.py` 建立 codec、selector、JSON-only import、outcome 與 DataFrame isolation 測試；在 `tests/test_response_reuse_protocol.py`、`tests/test_response_reuse_outcomes.py`、`tests/response_reuse/test_in_memory_store.py` 僅調整本次 source break 影響的斷言。
- [X] 10. 在 `docs/architecture/model-response-codecs.dataflow.json` 依 archify dataflow schema 產生繁體中文圖規格，通過 showcase validation，交付 `docs/architecture/model-response-codecs.html`，再以 `visual-check --repo-root` 產生 `Artifact Paths` 所列六個 sidecars，檢查四種 desktop containment 及實際圖面；最後對 docs/code/test/archify 建同一 immutable implementation subject。
- [X] 11. 僅在新的 committed `fix-2` planning candidate 與 Independent Plan-Reviewer approved extended receipt 經 Planner route 後，修改 `src/deterministic_response_cache/response_reuse/codecs/json_response.py`，將已知不支援的 JSON 樹改丟 `UnsupportedPayloadError`，保留真正 serializer failure 的 `EncodeFailureError`；不修改 selector/protocol 既有 outcome 映射。
- [X] 12. 修改 `tests/test_response_reuse_codecs.py`、`tests/test_model_response_codecs_integration.py`，補 Reviewer 指定的五類 substantive edge/assertion，保留 direct imports、fixtures/mocks；Implementer 只以這三個 code/test paths 建新的 immutable `fix-2` subject，之後交 Tester／Independent Reviewer 重跑完整新 evidence chain。
- [X] 13. 僅在 committed exact-six fix-3 planning candidate 與 Independent Plan-Reviewer approved extended receipt 經 Planner route 後，在 `src/deterministic_response_cache/response_reuse/codecs/contract.py` 定義 frozen/slotted `Encoded`／`Decoded` 與六個失敗 variant、兩個 closed union，修改三 member `ResponseCodec` 簽名；不改 public outcome enums。
- [X] 14. 修改 `src/deterministic_response_cache/response_reuse/codecs/json_response.py`、`src/deterministic_response_cache/response_reuse/codecs/pyarrow_dataframe.py`，保留明確繼承／`@override`、JSON/Arrow 格式與 equals gate，將預期成功與已知失敗直接回 result 值；只捕捉預期編解碼例外，不 catch-all。
- [X] 15. 修改 `src/deterministic_response_cache/response_reuse/codecs/selector.py` 固定選擇並對 unsupported root、缺 optional codec、unknown id、bad bytes 回值；修改 `src/deterministic_response_cache/response_reuse/protocol.py` 以 `match/case` 將 result 映到既有 reasons，只有成功值進 Store/policy，TypeError 只保留 Store/policy contract violation。
- [X] 16. 修改 `tests/test_response_reuse_codecs.py`、`tests/test_model_response_codecs_integration.py`、`tests/test_response_reuse_protocol.py`，逐一驗證所有預期 variant、JSON/DF 成功、對外 reason、Store/policy 邊界與 JSON-only direct import；Implementer 只以上述 exact-eight code/test paths 建新 immutable fix-3 subject，接獨立 Tester／Reviewer 新 evidence chain。
- [X] 17. 僅在 committed exact-four fix-4 planning candidate 與 Independent Plan-Reviewer approved extended receipt 經 Planner route 後，修改 `src/deterministic_response_cache/response_reuse/codecs/json_response.py`，將 parseable 深層 JSON 在 `_valid_json_tree` 的預期 `RecursionError` 轉為 `InvalidPayload` 回值；不改 selector/protocol、外部 reasons 或其他成功路徑，不加 catch-all。
- [X] 18. 修改 `tests/test_response_reuse_codecs.py`、`tests/test_model_response_codecs_integration.py`、`tests/test_response_reuse_protocol.py`，補直接 codec 與 protocol lookup regression，確認 `InvalidPayload`／`Unavailable(INVALID_PAYLOAD)`、非 `Miss` 且 policy 不評估；Implementer 只以上述 exact-four source/test paths 建新 immutable fix-4 subject，接獨立 Tester／Reviewer 新 evidence chain。

## Main Agent Actionable Steps — Fixed Tail

- [ ] Planner 依 fix-4 同 topic／同 subject committed approved evidence 完成 Phase 4.5 alignment；既有 Human authorization 俱全後才派 Implementer bounded push 並更新已 open Draft PR #11，停於 Human PR review/merge boundary。

## Handoff / Gate Notes

- Source plan：`plan/model-response-codecs/model-response-codecs.plan.md`；analysis routing 為 strict mode。本 tracker 不代表 Plan-Reviewer approval。
- Topic selector：`topic=model-response-codecs; branch=topic/model-response-codecs; managed-path-intent=/Users/andrew/code/python/worktrees/model-response-codecs; primary-worktree=false`。
- 原 `## Implementation Steps` 1–10 對原 subject、11–12 對 fix-2 subject、13–16 對 fix-3 subject 均已完成；fix-1 planning receipt `needs-rework`，fix-3 implementation Reviewer `needs-rework`。Draft PR #11 仍 OPEN 且 origin 舊版；17–18 pending，只有 fix-4 committed approved extended planning receipt 經 Planner route 後可做。各 marker 僅依真實 committed evidence 更新。
- Normal planning receipt 不含 candidate SHA；只有它的 sole commit direct parent 是 exact-five planning candidate 時，Planner 才可由 Git topology 綁定。Tester／Independent Reviewer evidence 須同 topic、同 immutable full-SHA subject；不能跨 topic 重用，也不能從 chat、branch 或本 tracker 自行推斷 approval。
- Human 獨占 PR review、merge、release、post-merge、tag 與 final summary；此 topic 不執行 release。
- Active fix-4 五個 conditional artifact paths、writer、schema 與先後順序以 parent plan 與 `model-response-codecs.correction-fix-4-plan.md` 為準。原/fix-1/fix-2 的已提交 SHA/verdict 保持 immutable；fix-3 candidate `c67f5c23bc2b6f3a6cb1f6b8e883b9ee77a561d1`／approved receipt `4389ddc5b83c65ae4e08976c7e270c567ebdec7b`／subject `b9a68575b24472a136bc7f3b826c8e7e581250b2`／passing Tester `2ff945e236aaa76afce61dbac1df62fc860f45c7`／needs-rework Reviewer `dff896ce0548c8d9c8ae36cabbe60792c9211225` 均 immutable predecessor。未寫的 fix-1 Tester/Reviewer paths 保持 absent；fix-4 candidate/subject/evidence SHA 與 verdict 尚未產生。
