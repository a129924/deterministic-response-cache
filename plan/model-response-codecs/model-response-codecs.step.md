---
topic: model-response-codecs
phase: correction-fix-1-plan-authoring
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
- [ ] **Actor:** Implementer — **Action:** 只提交 parent plan/step 與 `fix-1` correction plan/step 的 exact-four non-merge planning candidate；不得混入 code/evidence。
- [ ] **Actor:** Independent Plan-Reviewer／Implementer — **Action:** Reviewer 審 committed exact-four candidate 寫 extended correction receipt；Implementer 原樣 sole evidence-only commit，Planner 僅可 route committed approved。`needs-rework` 停回 Planner／Plan-Creator 另宣告新路徑，不覆寫本輪 receipt。
- [ ] **Actor:** Implementer — **Action:** 只修改 `json_response.py` 與兩個 declared codec tests，建立新 exact-three immutable subject；不得覆寫舊 evidence。
- [ ] **Actor:** Tester／Implementer — **Action:** Tester 對新 subject 寫 `tester-evidence.fix-1.json` actual command/exit-code evidence；Implementer 原樣 sole evidence-only commit。
- [ ] **Actor:** Independent Reviewer／Implementer — **Action:** Reviewer 只消費同 subject committed passing `fix-1` Tester evidence，寫 `implementation-review-log.fix-1.json`；Implementer 原樣 sole evidence-only commit。Tester `failing` 或 Reviewer `needs-rework` 停回 Planner／Plan-Creator 另宣告新路徑，本輪 evidence immutable，不可進 Phase 4.5。

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
- [ ] 11. 僅在新的 committed `fix-1` planning candidate 與 Independent Plan-Reviewer approved receipt 經 Planner route 後，修改 `src/deterministic_response_cache/response_reuse/codecs/json_response.py`，將已知不支援的 JSON 樹改丟 `UnsupportedPayloadError`，保留真正 serializer failure 的 `EncodeFailureError`；不修改 selector/protocol 既有 outcome 映射。
- [ ] 12. 修改 `tests/test_response_reuse_codecs.py`、`tests/test_model_response_codecs_integration.py`，補 Reviewer 指定的五類 substantive edge/assertion，保留 direct imports、fixtures/mocks；Implementer 只以這三個 code/test paths 建新的 immutable `fix-1` subject，之後交 Tester／Independent Reviewer 重跑完整新 evidence chain。

## Main Agent Actionable Steps — Fixed Tail

- [ ] Planner 依同 topic committed approved evidence 完成 Phase 4.5 alignment；既有 Human authorization 俱全後才派 Implementer bounded push 並開 draft PR，停於 Human PR review/merge boundary。

## Handoff / Gate Notes

- Source plan：`plan/model-response-codecs/model-response-codecs.plan.md`；analysis routing 為 strict mode。本 tracker 不代表 Plan-Reviewer approval。
- Topic selector：`topic=model-response-codecs; branch=topic/model-response-codecs; managed-path-intent=/Users/andrew/code/python/worktrees/model-response-codecs; primary-worktree=false`。
- 原 `## Implementation Steps` 1–10 已對原 subject 完成，卻因 committed Reviewer `needs-rework` 不構成 topic completion；新 11–12 為 `fix-1` pending implementation gate，須在新 approved correction planning receipt 後執行。其餘 stage/action markers 僅依真實 committed evidence 更新。
- Normal planning receipt 不含 candidate SHA；只有它的 sole commit direct parent 是 exact-five planning candidate 時，Planner 才可由 Git topology 綁定。Tester／Independent Reviewer evidence 須同 topic、同 immutable full-SHA subject；不能跨 topic 重用，也不能從 chat、branch 或本 tracker 自行推斷 approval。
- Human 獨占 PR review、merge、release、post-merge、tag 與 final summary；此 topic 不執行 release。
- `fix-1` 五個 conditional artifact paths、owner、schema 與先後順序以 parent plan 與 `model-response-codecs.correction-fix-1-plan.md` 為準。舊 subject `5d8873f3088769f1bd8b6da7b42d2ec96b9254f5`、Tester commit `226b95b2a1c29c7f1103d8f4e11939c29a96f266`、Reviewer needs-rework commit `57e4940150157d3cc73799c20461000eacc6bfe2` 均 immutable nonrouting provenance；新 candidate/subject/evidence SHA 與 verdict 尚未產生。
