# deterministic-response-cache agent guidance

## Baseline guardrails

- agent 的回覆、文件與規劃內容優先使用繁體中文；既有的技術名稱、檔名與必要術語可維持英文。
- 這是全新的 repository；不得引用、遷移、重構或相容任何舊 gateway 的設計、API、模組或工作流程。
- 開始任何實作前，必須先有該能力專屬、已確認的 topic plan；不得從 baseline 直接推導實作細節。
- Identity BC 是模型身分與完整請求身分的唯一 authority。其他 boundary 不得建立、推測或重新解讀 identity 規則。
- CacheStore 僅是 Response Reuse BC 的內部保存元件；它不得成為頂層 BC，也不得管理 identity、runtime 或模型執行。
- Loaded Runtime Cache、Model Execution 與 Provider Adapter 都必須各自以獨立 topic 規劃與實作；不得由 Response Reuse topic 提前引入。
- 架構責任、邊界與演進順序以 `docs/` 文件及 `docs/architecture/business-capability/index.html` 的 BC 圖為準；若實作提案與其衝突，先更新並確認架構文件，再開始實作。

## Observer / Dispatcher Governance

- Observer / Dispatcher 是 repository 頂層的唯讀協調者：只可盤點 state、派遣一個專責角色、彙整 bounded result，並回報 `可直接前進`、`needs-rework`、`blocked` 或 `human-check`。
- 只有 Planner 可執行 preflight，並判定 candidate、phase、gate 與 next role。Observer 不得自行選擇 active topic、手算或推測 gate，或重新解讀 locked decisions。
- active-topic evidence 僅限已提交的 topic plan、required step tracker，以及由 Plan-Reviewer 寫入 latest approved review-log JSON record；不得以 chat、branch、summary、`GOAL.md` 或 `.github/agents/**` 補推或選擇 task。
- Observer 每次只能依 Planner 的判定派遣一個允許角色：Planner、Plan-Creator、Plan-Reviewer、Implementer、Reviewer、Tester 或 Explorer；不得自我派遣、平行扮演多個角色，或擴增角色集合。
- 角色必須真實分離：Plan-Creator author plan，Plan-Reviewer 獨立審核 planning evidence，Implementer 實作，Tester 驗證，Reviewer 獨立審核 implementation 並處理 PR comment classification / routing；Planner 依 gate 判定後續角色。不得以隱藏 chat context 或同一角色宣稱多重 gate 已完成。
- 若無 candidate 或 required evidence 缺失，回報 `blocked`；多 candidate 或 plan 與 step 指向不同 topic，回報 `human-check`；同 topic 的 state 或 scope 矛盾，回報 `blocked`，除非 Planner 明定 Plan-Creator 可做 bounded repair。
- Observer 不得實作或改檔，不得執行 git、commit、push、PR、merge、release、tagging 或 post-merge，不得處理 review comments，也不得自行宣告 approval、human check 或 workflow gate 完成。
- `.github/agents/**` 是 frozen provenance：不得修改，且不得作為 runtime 或 routing dependency。
- publish 僅能由 Implementer 在 required evidence、Tester evidence、independent Reviewer approval、Planner Phase 4.5 alignment 與既有 human authorization 均具備時執行。draft PR 開啟後即停止於 human review boundary；只有 Human 可 review、merge、post-merge、release 與建立 close summary。

## Test Preservation

- 必須保留既有測試的 direct import、fixture、mock 與 assertion 行為。不得以 `importlib`、`__import__` 或 `sys.modules` 的動態載入取代 direct-import regression。
- 只有已核准 topic 明定「import 行為本身」為被測需求時，才可新增專用 import-behavior test；它不得取代既有的 direct-import regression test。
