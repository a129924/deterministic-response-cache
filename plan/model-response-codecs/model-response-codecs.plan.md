# model-response-codecs

## Goal / Outcome

- **Analysis-layer routing:** strict mode；`analysis/model-response-codecs/technical-spec.md` 是 execution-facing source of truth，`analysis/model-response-codecs/requirements.md` 是 business-intent guardrail。本 plan 將兩者映射為單一 Response Reuse BC Mission。
- 嵌入式應用以 opaque confirmed identity 保存 dict、list 或 `pandas.DataFrame` 模型回應為帶 codec id 的 bytes，lookup 後得到原生型別的 `ModelResponse`；DataFrame hit 相互隔離，寫入必須通過 `DataFrame.equals` 往返門檻。

## Scope

- **In-Scope:** `ModelResponse.value`、封閉 codec id 與 bytes envelope、共同 codec Protocol、兩個明確繼承且使用 `@override` 的具體 codec、固定 selector、record/lookup outcomes、可選 pandas/pyarrow extra、受 source break 影響的測試、五個 BC 架構面與 archify dataflow 交付；精確寫入面見 `Artifact Paths`。
- **Out-Of-Scope:** Identity 建立／比對／規則、Loaded Runtime Cache、Model Execution、Provider Adapter、跨 BC orchestration、Store backend／TTL／持久化／遷移、其他 payload、動態 registry、跨版本或跨程序相容、release。
- **ReadOnly:** `AGENTS.md`、`plan/topic-plan-contract.md`、`plan/agent-handoff-workflow.md`、`README.md`、`src/deterministic_response_cache/__init__.py`、`src/deterministic_response_cache/response_reuse/_cache_store.py`、`src/deterministic_response_cache/response_reuse/stores/in_memory.py`、`src/deterministic_response_cache/response_reuse/eligibility/policy.py`、`tests/test_response_reuse_eligibility.py`、`tests/test_package_import.py`、其他 BC 與所有未列寫入路徑。
- **Written:** 原 subject 已新增 VO、codec、test、archify paths；`fix-1` planning artifacts 與 `needs-rework` receipt 已提交，均為 frozen history。本輪 Plan-Creator 只新增 `fix-2` correction plan/step；新 `fix-2` receipt/Tester/Reviewer evidence 依表列角色順序寫入。
- **Modify:** 原 subject 已修改 protocol/outcomes、依賴檔、既有測試與架構面；本輪 planning 只修改 parent plan/step，後續 repair subject 只修改三個標為 `fix-2` **Modify** 的 code/test paths。
- **Deleted:** 無。原對話舊提案的單一 `src/deterministic_response_cache/response_reuse/codecs.py` 從計畫移除，原本不存在且本 topic 不建立或刪除它。
- **Current correction `fix-2`:** 原 implementation Reviewer 判 `needs-rework` 後，`fix-1` committed planning candidate `b51e557c535510c7660a4c17229ed1f0c008c4cf` 又獲 committed Plan-Reviewer `needs-rework` receipt `4d1a730783d5904f36f5a0a0a43cc69c578a9538`；沒有 active approved correction candidate 或新 code subject。本輪只維持 `json_response.py` 與兩個 codec tests 的原 exact-three repair；原 analysis/spec、其餘 source、依賴、架構圖及 archify 交付均 read-only。

## Locked Decisions

- `ModelResponse[PayloadT]` 為 frozen、slotted VO，欄位僅 `value`，直接保有 dict/list/DataFrame；`StoredResponse` 為 frozen、slotted 未解碼 bytes envelope，欄位 `codec_id: ResponseCodecId`、`payload: bytes`；`ResponseCodecId(StrEnum)` 僅 `JSON_V1="json/v1"`、`DATAFRAME_V1="dataframe/v1"`。
- `ResponseCodec[PayloadT](Protocol)` 只宣告 `codec_id` property、`encode(response: ModelResponse[PayloadT]) -> StoredResponse` 與 `decode(payload: bytes) -> ModelResponse[PayloadT]`。`JsonResponseCodec(ResponseCodec[JsonPayload])` 與 `PyArrowDataFrameCodec(ResponseCodec[pandas.DataFrame])` 明確繼承；每個實作的 property 與兩個方法都用 `typing.override`，property decorator 依序是 `@property`、`@override`。
- JSON 寫入僅接收 dict/list 與可無損往返的 JSON 樹；DataFrame 是唯一 Arrow IPC payload codec，不另設 PyArrow payload codec。DataFrame encode 使用記憶體內 Arrow IPC stream，將完整 `ModelResponse` 傳入，寫入前 decode 並檢查 `original.equals(decoded)`；每次 hit 重新 decode。
- selector 無動態 registry。寫入依 `response.value` 固定分流，讀取只依保存的 codec id 以 `match/case` 分流；未知／不合法 id fail closed，絕不嗅探 bytes。純 JSON direct import 與操作不急切載入 pandas/pyarrow；沒有 `codecs.py`、`codecs/__init__.py`、任何套件層 re-export、`importlib`、`__import__` 或 `sys.modules` 替換。
- 既有 generic response 直存 API 改為 `ModelResponse`／`StoredResponse` 是已授權 source break；只調整因此失效的既有行為斷言，保留 direct imports 及可沿用 fixture/mock。Store generic port/backend 的實作不變，eligibility policy 在 decode 後評估 `ModelResponse`。
- `NotCached` 的封閉 reason 為 `UNSUPPORTED_PAYLOAD`、`CODEC_UNAVAILABLE`、`ENCODE_FAILURE`、`ROUND_TRIP_MISMATCH`、`STORE_WRITE_FAILURE`；`Unavailable` 的封閉 reason 為 `STORE_FAILURE`、`UNKNOWN_CODEC`、`CODEC_UNAVAILABLE`、`INVALID_PAYLOAD`。`Cached`、`NotCached` 均保留原 `ModelResponse`。只有 entry 缺失或 eligibility 拒絕產生 `Miss`。
- 本 topic 不修改 README row、VERSION、release notes 或 release timing；沒有 repository release action。bytes 只承諾同一 cache instance 內使用，不承諾跨重啟、跨程序、跨版本讀取。
- 若 proposal 與既有 BC 圖文衝突，同一 implementation 工作中必須先更新五個既有 BC 架構面並完成唯讀一致性確認，才改 Python/source/test/dependency。此停點只確認本 topic 的架構責任符合已核准 plan 及 `docs/`／BC 圖，不建立另一個 approval gate、commit 或 evidence path；確認失敗停回 Planner。最後 docs、Python、archify 一次性建立同一 immutable implementation subject，接單一 Tester／Independent Reviewer sequence。
- **Correction `fix-2` 繼承原兩個 blocker，scope 不擴。** 原 subject `5d8873f3088769f1bd8b6da7b42d2ec96b9254f5`、Tester commit `226b95b2a1c29c7f1103d8f4e11939c29a96f266`、implementation Reviewer `needs-rework` commit `57e4940150157d3cc73799c20461000eacc6bfe2`，以及 `fix-1` planning candidate／Plan-Reviewer `needs-rework` receipt 均為 immutable nonrouting provenance。已知不支援 JSON 樹固定產生 `UNSUPPORTED_PAYLOAD`，真正 serializer failure 才是 `ENCODE_FAILURE`；補齊原五類 edge assertions。Goal、BC、Arrow IPC、equals、optional extra、direct imports、archify 不變。

## Boundaries / Exclusions

- Identity BC 是模型及完整請求 identity 的唯一 authority；Response Reuse 原樣轉交 opaque `confirmed_identity`，不建立、推測或重新解讀 identity。
- CacheStore 是 Response Reuse 內部保存元件，只保存 envelope，不能選 codec、執行模型或管理 runtime。Loaded Runtime Cache、Model Execution、Provider Adapter 分別保留獨立 topic。
- 架構文字、BC 圖與 archify 圖只呈現本 Mission 的 Response Reuse codec 流程；不宣稱跨 BC 整合已完成。Implementer 先更新既有 BC 文件並唯讀確認與 docs/ BC authority、scene mirror 和本 plan 一致，才開始 Python；若無法消除衝突，停回 Planner，不由 Implementer 重開 locked decisions。
- 未列路徑、擴充 public re-export、改動既有 direct-import 行為或超出 source break 授權的測試修改，一律停止並回 Planner。Plan-Creator 不是 Plan-Reviewer；Tester、Independent Reviewer、Human 各自保有獨立 gate。

## Status / Allowed Transitions

- **Current:** `needs-rework`；`fix-2` correction plan authoring 進行中。原 implementation subject 的 passing Tester／needs-rework Reviewer evidence、`fix-1` candidate 與其 committed `needs-rework` Plan-Reviewer receipt 都是 history；沒有 active approved correction candidate、`fix-2` receipt 或新 implementation subject。
- **Initial execution model（historical through needs-rework）:** Plan-Creator author → Implementer 提交 exactly five planning artifacts → Independent Plan-Reviewer 審 committed candidate → Implementer 以 sole receipt commit 作 direct child 綁定 candidate → Planner route → Implementer 先更新／確認 BC docs、再寫 Python 並建立原 immutable subject → independent Tester evidence → Independent Reviewer `needs-rework` evidence。此歷史不授權 Phase 4.5 或 publish；當前 route 僅以下述 `fix-2` 為準，本 topic 仍停在 release 前。
- **Initial historical transitions:** `planned` → `planning-candidate-committed` → `plan-review-in-progress` → `plan-review-receipt-committed`，再經原 implementation／Tester／Reviewer 到 `needs-rework`；normal 三鍵 receipt 僅綁 initial candidate，不能供 `fix-2` route。
- **Implementation route:** `creator-in-progress` → `tester-in-progress` → `review-ready` → `reviewer-in-progress` → `approved|needs-rework`；本 topic 的再次 `needs-rework` 須先回 Planner／Plan-Creator 另宣告 bounded correction route 與新 evidence paths，不能直接覆寫既有 Add evidence 再做新 subject。只有同 subject committed passing Tester evidence 可進 Reviewer。
- **Publish route:** `approved` → `publish-in-progress` 僅在 Planner Phase 4.5 alignment 與既有 Human authorization 俱全時成立；`publish-in-progress` → `pr-open`；`pr-open` → `needs-rework|merged`，其中 PR review/merge 唯 Human；`merged` terminal。沒有 `publish-in-progress` → `merged`，Reviewer approval 不等於 Human PR approval。
- **`fix-1` frozen route:** exact-four planning candidate `b51e557c535510c7660a4c17229ed1f0c008c4cf` 的 extended receipt 由 sole commit `4d1a730783d5904f36f5a0a0a43cc69c578a9538` 記 `needs-rework`、`candidate.active=false`、`route_authorization=null`；沒有新 implementation subject、Tester/Reviewer `fix-1` evidence 或 publish authority。`fix-1` planning artifacts/receipt 不覆寫；保留未寫的 `fix-1` evidence paths 為 frozen reserved history。
- **Active `fix-2` route:** Plan-Creator 只修 parent plan/step、新增 `fix-2` correction plan/step；Implementer 建 exact-four non-merge planning candidate。Independent Plan-Reviewer 只審 committed candidate 並寫 `fix-2` extended JSON；Implementer 原樣 sole evidence-only commit，Planner 僅從其 committed `approved` 與 actual binding route exact-three code/test subject。其後 Tester 寫新 `fix-2` factual evidence、Implementer sole commit；Independent Reviewer 只消費 committed passing 同 subject evidence，寫新 `fix-2` review evidence、Implementer sole commit；只有新 committed `approved` 可進 Planner Phase 4.5。此輪任何 `needs-rework`／`failing` 停回 Planner／Plan-Creator 宣告下一輪新 paths，不覆寫 `fix-2` evidence，不 publish。

## Artifact Paths

下表每列的 **Authority / role** 指定該 path 的決策權；未列 path 不得寫。所有路徑相對此 topic worktree 根目錄。Initial 與 `fix-1` 路徑保留歷史；本輪 Plan-Creator 只修改 parent plan/step 並新增 `fix-2` correction plan/step。

| Artifact | Exact path / action | Write owner | Authority / role |
| --- | --- | --- | --- |
| Requirements | `analysis/model-response-codecs/requirements.md` **Add** | Plan-Creator | Human intent 的 business guardrail；planning candidate |
| Technical spec | `analysis/model-response-codecs/technical-spec.md` **Add** | Plan-Creator | Execution-facing contract；planning candidate |
| Topic plan | `plan/model-response-codecs/model-response-codecs.plan.md` **Add** | Plan-Creator | 本 topic 的 canonical path/scope authority；planning candidate |
| Topic spec | `plan/model-response-codecs/model-response-codecs.spec.md` **Add** | Plan-Creator | Acceptance / scenario authority；planning candidate |
| Step tracker | `plan/model-response-codecs/model-response-codecs.step.md` **Add** | Plan-Creator；後續 Implementer 僅可依 gate 更新 implementation markers | Topic progression truth；planning candidate |
| Plan review receipt | `plan/model-response-codecs/model-response-codecs.plan-review-receipt.json` 原 **Add** | Independent Plan-Reviewer | Initial normal 三鍵 approved receipt；已提交 frozen history，不能作 `fix-2` handoff |
| Model response VO | `src/deterministic_response_cache/response_reuse/model_response.py` **Add** | Implementer | 本 plan/spec；immutable subject |
| Stored response VO | `src/deterministic_response_cache/response_reuse/stored_response.py` **Add** | Implementer | 本 plan/spec；immutable subject |
| Codec Protocol | `src/deterministic_response_cache/response_reuse/codecs/contract.py` **Add** | Implementer | 本 plan/spec；immutable subject |
| JSON codec | `src/deterministic_response_cache/response_reuse/codecs/json_response.py` 原 **Add**；`fix-2` **Modify** | Implementer | `fix-1` 未進 implementation；active correction 只修 unsupported-tree failure classification |
| DataFrame codec | `src/deterministic_response_cache/response_reuse/codecs/pyarrow_dataframe.py` **Add** | Implementer | 本 plan/spec；immutable subject |
| Fixed selector | `src/deterministic_response_cache/response_reuse/codecs/selector.py` **Add** | Implementer | 本 plan/spec；immutable subject |
| Response Reuse protocol | `src/deterministic_response_cache/response_reuse/protocol.py` **Modify** | Implementer | 本 plan/spec；immutable subject |
| Response Reuse outcomes | `src/deterministic_response_cache/response_reuse/outcomes.py` **Modify** | Implementer | 本 plan/spec；immutable subject |
| Optional dependencies | `pyproject.toml` **Modify** | Implementer | 本 plan/spec；pandas/pyarrow extra only；immutable subject |
| Locked dependencies | `uv.lock` **Modify** | Implementer | 同步 `pyproject.toml`；immutable subject |
| Codec unit tests | `tests/test_response_reuse_codecs.py` 原 **Add**；`fix-2` **Modify** | Implementer | active correction 補 unsupported-tree 與 empty DataFrame 等邊界 assertion |
| Codec integration tests | `tests/test_model_response_codecs_integration.py` 原 **Add**；`fix-2` **Modify** | Implementer | active correction 補 outcome/Store 與 foreign envelope cases |
| Existing protocol tests | `tests/test_response_reuse_protocol.py` **Modify** | Implementer | 只更新 source break 受影響斷言；immutable subject |
| Existing outcome tests | `tests/test_response_reuse_outcomes.py` **Modify** | Implementer | 只更新 source break 受影響斷言；immutable subject |
| Existing in-memory store tests | `tests/response_reuse/test_in_memory_store.py` **Modify** | Implementer | envelope integration 斷言，保留 generic store regression；immutable subject |
| BC architecture | `docs/business-capability-architecture.md` **Modify** | Implementer | BC 文本 authority；immutable subject |
| Evolution roadmap | `docs/evolution-roadmap.md` **Modify** | Implementer | BC 演進文本；immutable subject |
| Architecture brief | `docs/architecture/business-capability/architecture-brief.md` **Modify** | Implementer | BC 圖文契約；immutable subject |
| Scene source | `docs/architecture/business-capability/scene.js` **Modify** | Implementer | BC 互動圖 source；immutable subject |
| Scene mirror | `docs/architecture/business-capability/index.html` **Modify** | Implementer | `scene.js` generated block 的精確 mirror；immutable subject |
| Archify specification | `docs/architecture/model-response-codecs.dataflow.json` **Add** | Implementer | 本 plan/spec 與 archify dataflow schema；immutable subject |
| Archify HTML | `docs/architecture/model-response-codecs.html` **Add** | Implementer | showcase deliver 的自包含圖；immutable subject |
| Visual-check receipt | `docs/architecture/model-response-codecs.visual-check.json` **Add** | Implementer | archify visual-check factual receipt；immutable subject |
| Visual-check contact sheet | `docs/architecture/model-response-codecs.visual-check.html` **Add** | Implementer | 截圖檢視證據；immutable subject |
| Visual light small | `docs/architecture/model-response-codecs.visual-check.1440x900.light.png` **Add** | Implementer | visual-check screenshot；immutable subject |
| Visual dark small | `docs/architecture/model-response-codecs.visual-check.1440x900.dark.png` **Add** | Implementer | visual-check screenshot；immutable subject |
| Visual light large | `docs/architecture/model-response-codecs.visual-check.2048x1320.light.png` **Add** | Implementer | visual-check screenshot；immutable subject |
| Visual dark large | `docs/architecture/model-response-codecs.visual-check.2048x1320.dark.png` **Add** | Implementer | visual-check screenshot；immutable subject |
| Tester evidence | `plan/model-response-codecs/model-response-codecs.tester-evidence.json` 原 **Add** | Tester | 原 subject passing evidence；已提交 frozen history，不能作 `fix-2` evidence |
| Implementation review | `plan/model-response-codecs/model-response-codecs.implementation-review-log.json` 原 **Add** | Independent Reviewer | 原 subject needs-rework evidence；已提交 frozen history，不能作 `fix-2` approval |
| Correction plan `fix-1` | `plan/model-response-codecs/model-response-codecs.correction-fix-1-plan.md` 原 **Add** | Plan-Creator | Frozen needs-rework planning provenance；read-only |
| Correction step `fix-1` | `plan/model-response-codecs/model-response-codecs.correction-fix-1-step.md` 原 **Add** | Plan-Creator | Frozen needs-rework planning provenance；read-only |
| Correction Plan-Reviewer receipt `fix-1` | `plan/model-response-codecs/model-response-codecs.correction-fix-1-plan-review-log.json` 原 **Add** | Independent Plan-Reviewer | Committed needs-rework sole evidence `4d1a730783d5904f36f5a0a0a43cc69c578a9538`；frozen read-only |
| Correction Tester evidence `fix-1` | `plan/model-response-codecs/model-response-codecs.tester-evidence.fix-1.json` reserved, **not written** | Tester | `fix-1` never entered implementation；不得建立或作 routing evidence |
| Correction implementation review `fix-1` | `plan/model-response-codecs/model-response-codecs.implementation-review-log.fix-1.json` reserved, **not written** | Independent Reviewer | `fix-1` never entered implementation；不得建立或作 routing evidence |
| Correction plan `fix-2` | `plan/model-response-codecs/model-response-codecs.correction-fix-2-plan.md` **Add** | Plan-Creator | Active correction trigger、exact-three scope、schemas、parent sync；exact-four planning candidate |
| Correction step `fix-2` | `plan/model-response-codecs/model-response-codecs.correction-fix-2-step.md` **Add** | Plan-Creator | Active ordered repair、review、evidence、closure checkpoints；exact-four planning candidate |
| Correction Plan-Reviewer receipt `fix-2` | `plan/model-response-codecs/model-response-codecs.correction-fix-2-plan-review-log.json` **Add** | Independent Plan-Reviewer | 只審 committed exact-four candidate，依 `fix-2` extended schema 寫入；Implementer 原樣 sole evidence-only commit，Planner 只 route committed approved |
| Correction Tester evidence `fix-2` | `plan/model-response-codecs/model-response-codecs.tester-evidence.fix-2.json` **Add** | Tester | 對新 exact-three immutable subject 記 actual commands/exit codes；Implementer 原樣 sole evidence-only commit |
| Correction implementation review `fix-2` | `plan/model-response-codecs/model-response-codecs.implementation-review-log.fix-2.json` **Add** | Independent Reviewer | 只消費同 subject committed passing `fix-2` Tester evidence；Implementer 原樣 sole evidence-only commit |

本 `fix-2` planning candidate 僅修改 parent plan/step 並新增兩份 `fix-2` correction planning 檔；新 implementation subject 僅修改上述三個 `fix-2` code/test paths。`analysis/model-response-codecs/{requirements,technical-spec}.md`、原 `*.spec.md`、initial/fix-1 artifacts 與 receipt/evidence、`README.md`、VERSION（若存在）、`.github/copilot-instructions.md`（若存在）、package `__init__.py`、Store implementation、原 docs/archify 交付、其他 topic 與其他未列路徑均 read-only；沒有 deletion。未寫的 `fix-1` Tester/Reviewer paths 保持不存在。若 visual-check 因工具不可用未生成四圖與 contact sheet，Implementer 記錄 skipped receipt 並回 Planner 做 path/gate alignment，不以缺件冒稱交付完成。

### Evidence shape and order

- 原 initial planning candidate 的 Normal Plan-Reviewer receipt 是 `.agents/skills/plan-reviewer/SKILL.md` §Process 7 的單一三鍵 JSON object，top-level **恰為** `verdict: approved|needs-rework`、`blocking_issues: [{issue, file, fix}, ...]`、`copilot_feedback_triage: {ADDRESS: [{comment, location, why}, ...], DISCUSS: [{comment, optional, why}, ...], SKIP: [{comment, why}, ...]}`；無 candidate SHA、topic、schema version、recorded_by 等 extended 欄位。此三鍵格式只屬原 initial route；`fix-1` 的 extended correction receipt 亦已提交 `needs-rework`，兩者都不是當前 handoff。原 receipt 曾由 Independent Plan-Reviewer 寫、Implementer 原樣 sole evidence commit；Planner 以 Git direct-parent／exact-five diff 綁定原 candidate。當前唯一 Plan-Reviewer handoff 是下方 `fix-2` extended JSON path/schema，不能由 initial/fix-1 歷史 receipt route。
- 原 Tester evidence 為單一 JSON object：`schema_version: 1`、`topic`、`implementation_subject_commit: <full 40-hex>`、`status: passing|failing`、`commands: [{command: <non-empty string>, exit_code: <integer>}, ...]`、`recorded_by: "Tester"`；已提交 passing，僅作原 subject history。
- 原 Independent Reviewer evidence 為單一 JSON object：`schema_version: 1`、`topic`、`implementation_subject_commit: <same full 40-hex>`、`tester_evidence_commit: <passing evidence sole commit full 40-hex>`、`verdict: approved|needs-rework`、`blocking_issues: []|[string]`、`recorded_by: "Independent Reviewer"`；已提交 needs-rework，不能進 Phase 4.5 或授權 `fix-2`。
- 上述 normal receipt 與原 Tester/Reviewer evidence、`fix-1` planning artifacts 及 committed `needs-rework` receipt 均為 immutable predecessor truth；`fix-1` 未建立 subject 或新 Tester/Reviewer evidence。當前唯一 handoff 與 route 是 `fix-2`：exact-four planning candidate → Independent Plan-Reviewer 依 `model-response-codecs.correction-fix-2-plan.md` 的 extended schema 寫 `fix-2` receipt → Implementer sole evidence commit → Planner 驗 committed approved → exact-three subject → Tester `fix-2` evidence → Implementer sole evidence commit → Independent Reviewer `fix-2` evidence → Implementer sole evidence commit → Planner Phase 4.5。新 SHA、verdict、outcome 均只能 post-commit 記錄。

## Python implementation metadata

### Non-goals

- 不改 Identity BC 身分規則或建立跨 BC handoff。
- 不實作 runtime retention、model execution、provider adapter 或其他 response 類型。
- 不做持久化、migration、跨版本 bytes 相容、動態 codec registry 或 Store backend 變更。
- 不做 README/VERSION/release、root/package re-export 或 `codecs/__init__.py`。

### Current Context

初始 planning 時 `response_reuse/protocol.py` 將 generic `ResponseT` 直存；現已依本 topic 建 `ModelResponse`／`StoredResponse`、JSON/DataFrame codecs、optional extra 與圖面。原 implementation subject `5d8873f3088769f1bd8b6da7b42d2ec96b9254f5` 經 passing Tester 後被 Independent Reviewer 判 `needs-rework`；`fix-1` planning candidate 又因 parent Reviewer Handoff 指向舊 normal 三鍵 JSON 而獲 committed Plan-Reviewer `needs-rework`，並未實作。`json_response.py` 仍把已知不支援 JSON 樹丟為 `EncodeFailureError`，protocol 因而映射 `ENCODE_FAILURE`；兩個 codec tests 仍缺原 Reviewer 指定邊界案例。其餘原 subject 是 frozen predecessor，不在本 correction 改動面。

### Requirements

- 只存有 `ResponseCodecId` 與 bytes 的 `StoredResponse`；讀取只依 id decode，不嗅探 bytes。
- JSON dict/list round trip 無損；DataFrame 以 Arrow IPC 保存 pandas metadata，寫入以 equals gate，hit 獨立。
- optional pandas/pyarrow 不污染 JSON-only import；所有 expected failure 可由 outcome reason 區分，identity 原樣傳給 Store。
- direct-import 回歸、pyright strict、ruff、pytest 與 archify showcase/desktop visual gate 均有實際證據。

### Decisions

- **Async-planning status:** exempt — 現有 Response Reuse Protocol 與新 codecs 都是純同步、process-local bytes 編解碼；本 topic 不加入 async boundary、pooled resource、背景任務、timeout 或 cancellation。
- **Module/package placement:** VO 在 `response_reuse/` defining modules；codec 共同契約與兩個實作、selector 在 `response_reuse/codecs/` 的四個 defining modules，沒有 package initializer。
- **New public API:** `ModelResponse`、`StoredResponse`、`ResponseCodecId`、`ResponseCodec`、`JsonResponseCodec`、`PyArrowDataFrameCodec` 透過各自 defining module direct import。
- **Interface changes:** `ResponseReuseProtocol` 收 `CacheStore[IdentityT, StoredResponse]`，record/lookup 的 response 改為 `ModelResponse`；`Hit`、`Cached`、`NotCached` 包含此 VO，失敗 outcome 增加封閉 reason。
- **Breaking changes allowed:** yes，Human 已接受 generic `ResponseT` 直存 API source break；不另設 compatibility layer。
- **New dependencies:** yes，只在 `pyproject.toml` 可選 `dataframe` extra 宣告 `pandas>=2.2`、`pyarrow>=20`，並同步 `uv.lock`；基礎安裝為零 runtime dependencies。
- **Error-handling strategy:** JSON/DataFrame 預期 codec 失敗映射到明確 `NotCached`/`Unavailable` reason；不合法/未知 id fail closed；Store value channel 維持原映射；未預期 Store/policy exception 依既有邊界傳播。
- **Typing strategy:** Python 3.12 generics/StrEnum/Protocol、`typing.override`、pyright strict；具體 codec 明確繼承且簽名符合 contract，無 `Any` 或動態載入替代 direct imports。

### Public Contract / API Changes

- `ModelResponse[PayloadT](value: PayloadT)`：frozen/slotted。`ResponseCodecId(StrEnum)` 僅 `json/v1`、`dataframe/v1`。`StoredResponse(codec_id: ResponseCodecId, payload: bytes)`：frozen/slotted。
- `ResponseCodec[PayloadT]`：唯讀 `codec_id`、`encode(ModelResponse[PayloadT]) -> StoredResponse`、`decode(bytes) -> ModelResponse[PayloadT]`。`JsonResponseCodec` 明確繼承 `ResponseCodec[JsonPayload]`；`PyArrowDataFrameCodec` 明確繼承 `ResponseCodec[pandas.DataFrame]`，並用 `@override` 實作全部三個 member。
- `ResponseReuseProtocol[IdentityT, PayloadT]`：`record(confirmed_identity, response: ModelResponse[PayloadT]) -> RecordOutcome[PayloadT]`、`lookup(confirmed_identity) -> LookupOutcome[PayloadT]`；其 Store 為 `CacheStore[IdentityT, StoredResponse]`，eligibility policy 對 `ModelResponse[PayloadT]` 評估。outcome 封裝新 response VO；`NotCached`、`Unavailable` 另帶上述 reason。原泛型 response 直存呼叫端須改用 VO。
- 具體 codec 的預期 encode/decode failure 使用其本地 typed failure，再由 protocol 翻譯為 outcome；不把壞 bytes／未知 id 當 miss，也不引入新的 Store exception contract。

### Affected Files / Modules

**Likely affected files:** `Artifact Paths` 中全部 **Add** VO/codec/test/archify paths、全部 **Modify** source/test/dependency/BC paths。**Candidate files to inspect, read-only:** `response_reuse/_cache_store.py`、`response_reuse/stores/in_memory.py`、`response_reuse/eligibility/policy.py`、`tests/test_response_reuse_eligibility.py`、`tests/test_package_import.py`、`docs/architecture/canonical-identity-pipeline.dataflow.json`（僅作圖形範例，不作本 topic 事實來源）。

### Test Plan

- **Happy path:** `tests/test_response_reuse_codecs.py` 與 `tests/test_model_response_codecs_integration.py` 驗證 JSON dict/list、DataFrame dtype/index/timezone/NA Arrow IPC round trip、獨立 hit 與 opaque identity passthrough。
- **Invalid input:** 測 non-string key、nonfinite number、tuple/custom/nested loss、scalar、未知/不合法 id、壞 bytes、invalid envelope，確認不寫入或 `Unavailable` 而非 `Miss`。
- **Edge case:** DataFrame equals False、encode exception、缺 optional deps、Store read/write failure、eligibility denial、empty JSON containers 與 empty DataFrame。
- **Regression:** 保留 existing direct imports、fixture/mock 與未受 source break 影響的 Store/policy assertions；pyright strict 驗證具體 codec 明確繼承及 override 簽名；無只檢查 decorator 存在的測試。
- **Backward compatibility:** 明確驗證 source break；舊 generic response 直存用法不再屬可支援 API，其他 BC、Store generic port/backend 及 eligibility policy 本體保持原行為。
- **Architecture precedence:** 在 implementation 工作中先完成五個既有 BC 架構面的更新，唯讀對照 docs/ BC authority、BC 圖責任與 scene mirror，確認後才開始 Python；若不通過則停止，不建立 implementation subject。最終 Tester/Reviewer 檢查同一 subject 的全部 docs/code/test/archify 變更。
- **Correction `fix-2`:** `tests/test_response_reuse_codecs.py` 與 `tests/test_model_response_codecs_integration.py` 對已知 unsupported JSON tree、empty DataFrame、DataFrame optional codec unavailable record、真正 encoder failure、foreign malformed envelope 補有意義的 assertion；由 `src/deterministic_response_cache/response_reuse/codecs/json_response.py` 區分 unsupported value 與 serializer failure。舊測試的 defining-module direct imports、fixtures/mocks 與原有 assertions 保留。除此三檔無新的 Python/API、依賴、docs 或 archify 修改。

### Risks

- Arrow IPC/pandas metadata 可能無法對每種 DataFrame 無損往返；equals gate 必須在 Store write 前阻止失真。
- Python import graph 可能讓 JSON-only 使用者被迫安裝 pandas/pyarrow；用 direct-import 隔離與缺依賴環境驗證。
- source break 可能影響既有 caller 和 direct-import regression；只依本 scope 更新測試，不動其他 BC。
- archify visual-check 依賴本機瀏覽器；receipt skipped 不能冒稱視覺通過。

### Rollback Plan

若本 topic 尚未 merge，任何 rollback/superseding subject 均須先返回 Planner 建立獨立 bounded route；本 `fix-2` 只可修改 exact-three repair paths，不能回復 generic API 或改寫其他 topic/初始/fix-1 committed provenance。Implementer 不得自行 merge、release 或刪除 evidence。

## Implementation Steps

1. 在 `docs/business-capability-architecture.md`、`docs/evolution-roadmap.md`、`docs/architecture/business-capability/architecture-brief.md`、`docs/architecture/business-capability/scene.js`、`docs/architecture/business-capability/index.html` 先更新 Response Reuse bytes 保存/解碼及 outcomes，維持 Identity/Store/其他 BC 責任與 scene mirror；此時不編輯 Python/source/test/dependency。
2. 唯讀核對前述五個 BC 文件與 `AGENTS.md`、本 plan/spec 的責任／演進順序及 `scene.js`／`index.html` generated block mirror；一致性未確認即停回 Planner，不開始 Python，也不建立 subject commit。此為同一 implementation 工作內的架構確認停點，不取代後續 Tester/Reviewer。
3. 在 `src/deterministic_response_cache/response_reuse/model_response.py`、`stored_response.py` 建立 frozen/slotted VO 與封閉 `ResponseCodecId`；在 `codecs/contract.py` 定義三 member 的 generic `ResponseCodec` Protocol。
4. 在 `src/deterministic_response_cache/response_reuse/codecs/json_response.py` 建立 `JsonPayload` 與明確繼承 `ResponseCodec[JsonPayload]` 的 JSON codec，使用正確 `@property`/`@override` 順序、無損驗證及 UTF-8 bytes。
5. 在 `src/deterministic_response_cache/response_reuse/codecs/pyarrow_dataframe.py` 建立明確繼承 `ResponseCodec[pandas.DataFrame]` 的 Arrow IPC codec，使用三個 `@override`，接收完整 `ModelResponse` 並在 encode 內以 `equals` 驗證往返。
6. 在 `src/deterministic_response_cache/response_reuse/codecs/selector.py` 建立固定 value/id 分流及分支內 direct imports，讓純 JSON 路徑不載入 pandas/pyarrow；未知 id fail closed，不建立 `codecs.py` 或 `codecs/__init__.py`。
7. 在 `src/deterministic_response_cache/response_reuse/outcomes.py`、`protocol.py` 將 public response/Store contract 改為 `ModelResponse`/`StoredResponse`，完整 VO 傳 encoder，加入封閉 failure reasons，保留 Store/policy exception 邊界。
8. 在 `pyproject.toml` 新增 pandas/pyarrow 的 `dataframe` optional extra 並更新 `uv.lock`；基礎 JSON 安裝維持無 runtime deps。
9. 在 `tests/test_response_reuse_codecs.py`、`tests/test_model_response_codecs_integration.py` 建立 codec、selector、JSON-only import、outcome 與 DataFrame isolation 測試；在 `tests/test_response_reuse_protocol.py`、`tests/test_response_reuse_outcomes.py`、`tests/response_reuse/test_in_memory_store.py` 僅調整本次 source break 影響的斷言。
10. 在 `docs/architecture/model-response-codecs.dataflow.json` 依 archify dataflow schema 產生繁體中文圖規格，通過 showcase validation，交付 `docs/architecture/model-response-codecs.html`，再以 `visual-check --repo-root` 產生 `Artifact Paths` 所列六個 sidecars，檢查四種 desktop containment 及實際圖面；最後對 docs/code/test/archify 建同一 immutable implementation subject。
11. 僅在新的 committed `fix-2` planning candidate 與 Independent Plan-Reviewer approved extended receipt 經 Planner route 後，修改 `src/deterministic_response_cache/response_reuse/codecs/json_response.py`，將已知不支援的 JSON 樹改丟 `UnsupportedPayloadError`，保留真正 serializer failure 的 `EncodeFailureError`；不修改 selector/protocol 既有 outcome 映射。
12. 修改 `tests/test_response_reuse_codecs.py`、`tests/test_model_response_codecs_integration.py`，補 Reviewer 指定的五類 substantive edge/assertion，保留 direct imports、fixtures/mocks；Implementer 只以這三個 code/test paths 建新的 immutable `fix-2` subject，之後交 Tester／Independent Reviewer 重跑完整新 evidence chain。

## Validation / Acceptance Checks

- `uv run --extra dataframe pytest`、`uv run --extra dataframe pyright`（strict 由 `pyproject.toml` 配置）、`uv run --extra dataframe ruff check .` 全部完成且 Tester 記錄實際 exit code；保留 direct-import regression，不新增 decorator-presence-only 測試。
- 實作前的架構確認需核對五個 BC 面仍顯示 Identity 唯一 authority、CacheStore 內部保存、其他 BC 未被提前實作、`scene.js` 與 `index.html` generated block 一致；未通過即停止。此確認發生在任何 Python/source/test/dependency 編輯前，最終由 Tester/Reviewer 對同一 committed subject 再驗證。
- 原 initial normal Plan-Reviewer receipt 僅三鍵、已 frozen；`fix-1` extended receipt 為 committed `needs-rework`。當前 `fix-2` 必須依其獨立 extended schema、exact-four candidate/tree/blob/first-parent facts 與 sole receipt commit 判定，不接受舊 receipt、chat 或 branch 作 routing authority。
- 核對 immutable implementation subject 只觸碰表中 **Add/Modify** implementation paths；`codecs.py`、`codecs/__init__.py` 及 package re-export 均不存在，無 `importlib`、`__import__`、`sys.modules` 替換。
- 在不安裝 pandas/pyarrow 的基礎環境驗證 `json_response.py`、selector 與 protocol 的 defining-module direct imports 和 JSON record/lookup；DataFrame path 回明確 unavailable/not-cached reason。
- archify：`node /Users/andrew/.codex/skills/archify/bin/archify.mjs validate dataflow docs/architecture/model-response-codecs.dataflow.json --quality showcase --json`，需 9/9、0 composition errors、0 warnings；`deliver` 後執行 `visual-check docs/architecture/model-response-codecs.html --repo-root . --json`，檢查 1440×900、1600×1000、1920×1080、2048×1320 containment、兩種主題截圖並實際目視。未可目視時如實標 skipped。
- Independent Reviewer 核對同 topic full-SHA subject、committed passing Tester evidence、public/source-break contract、架構邊界、path exactness 和圖面 receipt；Planner Phase 4.5 只在同 subject approved review evidence 提交後 align。
- `fix-2` 只接受 exact-four planning candidate、committed approved extended Plan-Reviewer receipt、exact-three new implementation subject、同 subject 新 committed passing Tester evidence 與新 approved Independent Reviewer evidence。測試須證明已知 unsupported JSON tree 回 `UNSUPPORTED_PAYLOAD` 且 Store 未寫入，真正 encode failure 仍是 `ENCODE_FAILURE`；empty DataFrame、可選 codec 不可用時的 DataFrame record、foreign malformed envelope 都有明確 outcome/assertion。Initial/fix-1 needs-rework evidence 不得改寫或用作新 subject gate。

## Reviewer Handoff

```json
{
  "active_correction_id": "fix-2",
  "handoff_kind": "extended-correction-json",
  "sole_active_plan_review_path": "plan/model-response-codecs/model-response-codecs.correction-fix-2-plan-review-log.json",
  "schema_authority": "plan/model-response-codecs/model-response-codecs.correction-fix-2-plan.md#active-extended-plan-reviewer-receipt-schema",
  "required_receipt_keys": [
    "schema_version", "topic", "correction_id", "candidate", "reviewed_artifacts",
    "first_parent_admission", "review_basis", "verdict", "blocking_issues",
    "copilot_feedback_triage", "route_authorization", "recorded_by"
  ],
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "copilot_feedback_triage": {"ADDRESS": [], "DISCUSS": [], "SKIP": []}
}
```

## Post-merge / release actions

本 topic 不執行 repository release、tag 或 version bump。Draft PR 後的 review、merge、post-merge 與 final summary 均是 Human boundary；`merged` 對本 topic terminal。

## Open Questions / Unresolved Items

None；Human 已決定 DataFrame Arrow IPC、`equals` 門檻、optional extra、source break、codec 分層與圖面交付。任何實作新問題先回 Planner，不自行擴張 scope。
