# deterministic-response-cache

`deterministic-response-cache` 是一個全新的、provider-agnostic、可嵌入的 Python library baseline。

目前不提供可執行 library、cache backend、model runtime 或 provider adapter。這個 repository 的第一個 topic
只固定專案方向、Business Capability（BC）責任、演進流程與互動式架構文件。

## 兩條不可違反的原則

1. 只有模型與完整輸入都沒有改變時，response 才可以安全重用。
2. 模型一旦改變，即使名稱、路徑或其他描述看起來相同，也絕不能重用舊 response。

## 目前階段

一致性承諾僅限於同一個 cache instance 的生命週期。跨重啟持久化、跨程序一致性與模型本身的 deterministic 推論都不屬於目前 baseline。

下一步是先確認 `docs/architecture/business-capability/architecture-brief.md`，之後才會建立互動式 BC 架構圖。
