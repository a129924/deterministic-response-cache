# deterministic-response-cache

`deterministic-response-cache` 是一個全新的、provider-agnostic、可嵌入的 Python library baseline。

目前只提供可安裝的空 package 與開發工具鏈；不提供 response cache、model runtime、model execution 或 provider adapter。專案的 baseline 已固定方向、Business Capability（BC）責任、演進流程與互動式架構文件。

## 兩條不可違反的原則

1. 只有模型與完整輸入都沒有改變時，response 才可以安全重用。
2. 模型一旦改變，即使名稱、路徑或其他描述看起來相同，也絕不能重用舊 response。

## 目前階段

一致性承諾僅限於同一個 cache instance 的生命週期。跨重啟持久化、跨程序一致性與模型本身的 deterministic 推論都不屬於目前 baseline。

## 開發工具

使用 `uv` 作為唯一的依賴與環境管理入口：

```bash
uv sync
uv run pre-commit install
```

完整驗證：

```bash
uv lock --check
uv run ruff format --check .
uv run ruff check .
uv run pyright
uv run tach check
uv run pytest
uv run pre-commit run --all-files
```

pytest-cov 會產生 terminal 與 XML coverage report，但目前不設定 coverage 門檻。這個 package skeleton 僅驗證 tooling，不代表任何 response-cache 實作。
