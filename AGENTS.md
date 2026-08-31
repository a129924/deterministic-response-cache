# deterministic-response-cache agent guidance

## Baseline guardrails

- agent 的回覆、文件與規劃內容優先使用繁體中文；既有的技術名稱、檔名與必要術語可維持英文。
- 這是全新的 repository；不得引用、遷移、重構或相容任何舊 gateway 的設計、API、模組或工作流程。
- 開始任何實作前，必須先有該能力專屬、已確認的 topic plan；不得從 baseline 直接推導實作細節。
- Identity BC 是模型身分與完整請求身分的唯一 authority。其他 boundary 不得建立、推測或重新解讀 identity 規則。
- CacheStore 僅是 Response Reuse BC 的內部保存元件；它不得成為頂層 BC，也不得管理 identity、runtime 或模型執行。
- Loaded Runtime Cache、Model Execution 與 Provider Adapter 都必須各自以獨立 topic 規劃與實作；不得由 Response Reuse topic 提前引入。
- 架構責任、邊界與演進順序以 `docs/` 文件及 `docs/architecture/business-capability/index.html` 的 BC 圖為準；若實作提案與其衝突，先更新並確認架構文件，再開始實作。
