# Business Capability Architecture

## 核心責任

### Identity BC

Identity BC 是模型身分與完整請求身分的唯一 authority。它唯一負責判定是否為同一模型與同一件請求；identity 規則不得分散在 Response Reuse、CacheStore、runtime、execution 或 provider adapter。

Identity BC 不保存 response、不執行模型，也不管理 loaded runtime。

### Response Reuse BC

Response Reuse BC 只消費 Identity BC 已確認的 identity，並決定既有 response 是否能安全重用。它不自行推導模型或請求身分，不執行模型，也不管理 loaded runtime。

### CacheStore

CacheStore 是 Response Reuse BC 的內部保存元件，而不是頂層 BC。它只保存與取回 response；不得建立 identity、判定模型版本、推測 request 欄位、執行模型或管理 runtime。baseline 不定義其實作、持久化方式或 lifecycle policy。

### Loaded Runtime Cache（未來）

Loaded Runtime Cache 重用已初始化且可執行的模型 runtime，避免重複載入。它必須使用獨立的 Runtime Store／Runtime Registry 概念，不能與 Response CacheStore 混用或共用責任。

### Model Execution（未來）

Model Execution 在 response 無法重用時，協調取得 runtime 與執行模型。它不擁有 response reuse 或 identity 規則。

### Provider Adapter（未來、可替換）

Provider Adapter 只對接具體的 local 或 remote provider，位於核心 library 外部的可替換邊界。它不擁有 identity、response reuse 或 runtime cache 政策。

## Boundary violations

下列變更一律是邊界違反，必須回到 BC 設計層重新討論：

- 在 Identity BC 以外建立或解讀模型／請求身分規則。
- 讓 Response Reuse BC、CacheStore 或 Provider Adapter 執行模型。
- 讓 CacheStore 管理 loaded runtime，或讓 Runtime Store／Registry 保存 response。
- 將 provider 特有規則提升為核心 identity 或 response reuse 政策。
