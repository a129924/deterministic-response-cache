---
topic: model-response-codecs
phase: plan-authoring
created: 2026-09-24
---

# model-response-codecs — Step Tracking

## Workflow Stages

- [X] plan-authoring
- [ ] plan-review
- [ ] tdd-test-authoring
- [ ] implementation
- [ ] implementation-review
- [ ] code-review

## Actionable Steps

- [ ] **Actor:** Implementer — **Action:** 只將五份 initial planning artifacts 作為單一 planning candidate commit，交 Independent Plan-Reviewer 審查。
- [ ] **Actor:** Independent Plan-Reviewer — **Action:** 只審 committed candidate，依 normal plan-reviewer contract 寫三鍵 JSON verdict；不得自行 commit 或 route。
- [ ] **Actor:** Implementer — **Action:** 原樣以 sole evidence-only commit 提交三鍵 Plan-Reviewer receipt，其 direct parent 必須是 exact-five planning candidate；Planner 以 Git topology 與 committed approved verdict route。
- [ ] **Actor:** Implementer — **Action:** approved planning gate 後，先更新五個 BC 架構面並唯讀確認一致性，通過後才寫 Python；最後對 declared docs/code/test/archify paths 建同一 immutable subject，交 independent Tester。
- [ ] **Actor:** Tester／Implementer — **Action:** Tester 只寫 same-subject factual evidence；Implementer 原樣 sole evidence-only commit 後才交 Independent Reviewer。
- [ ] **Actor:** Independent Reviewer／Implementer — **Action:** Reviewer 只消費 committed passing same-subject Tester evidence 並寫 review log；Implementer 原樣 sole evidence-only commit。

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

## Main Agent Actionable Steps — Fixed Tail

- [ ] Planner 依同 topic committed approved evidence 完成 Phase 4.5 alignment；既有 Human authorization 俱全後才派 Implementer bounded push 並開 draft PR，停於 Human PR review/merge boundary。

## Handoff / Gate Notes

- Source plan：`plan/model-response-codecs/model-response-codecs.plan.md`；analysis routing 為 strict mode。本 tracker 不代表 Plan-Reviewer approval。
- Topic selector：`topic=model-response-codecs; branch=topic/model-response-codecs; managed-path-intent=/Users/andrew/code/python/worktrees/model-response-codecs; primary-worktree=false`。
- 只有 `## Implementation Steps` 十個 markers 是 implementation-completion gate；第 2 項架構確認須在第 3–9 項 Python/source/test/dependency 前完成。其餘 stage/action markers 僅依真實 committed evidence 更新。
- Normal planning receipt 不含 candidate SHA；只有它的 sole commit direct parent 是 exact-five planning candidate 時，Planner 才可由 Git topology 綁定。Tester／Independent Reviewer evidence 須同 topic、同 immutable full-SHA subject；不能跨 topic 重用，也不能從 chat、branch 或本 tracker 自行推斷 approval。
- Human 獨占 PR review、merge、release、post-merge、tag 與 final summary；此 topic 不執行 release。
