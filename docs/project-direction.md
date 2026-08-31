# Project Direction

## 願景

建立一個 provider-agnostic、可嵌入的 Python library，使模型 response 的重用建立在清楚且可驗證的模型與請求身分之上。

## 成功定義

新加入者應能辨識哪些 response 可安全重用、模型改變時為何不可重用既有 response，以及每一項能力的責任邊界。專案的近期選擇必須保留未來 runtime reuse 與模型執行的演進空間，卻不提前實作它們。

## In scope

- 專案願景與成功定義。
- Business Capability 的責任與非責任。
- 現在／未來能力的切分與高階演進流程。
- 互動式 Business Capability 架構圖。

## Out of scope

- Python API、class、key、hash、資料格式或 schema。
- cache backend、持久化、TTL、eviction、concurrency、retry、timeout。
- model runtime、runtime pool、模型執行、provider adapter 或 service surface。
- 任一 local 或 remote provider 的優先選擇。
- 跨重啟、跨程序或模型推論層級的一致性保證。

## Non-goals

- 這不是任何舊 repository 的延續、重構、遷移或相容版本。
- 不沿用既有 API、模組、key、TTL、invalidation、adapter 或 workflow。
- 不以成本最低或命中率最高取代安全重用作為第一優先。
