# package-topology-skeleton-replay — Requirements

## Goal

在全新 repository 的 `src/deterministic_response_cache/` 下，預先保留五個 Business Capability (BC) 的空目錄拓撲，並使 architecture documentation 對該拓撲、邊界與演進順序有一致且明確的敘述。

## Required outcomes

1. 僅建立下列目錄中的 `.gitkeep`：`identity`、`response_reuse`、`loaded_runtime_cache`、`model_execution`、`provider_adapter`。
2. 每個目錄只代表預先保留的 topology；不代表該 BC 已實作或可使用，且不新增 executable Python module、public symbol 或 re-export。
3. `Identity` 是模型身分與完整 request identity 的唯一 authority。
4. `CacheStore` 是 `Response Reuse` 的內部元件，不是頂層 BC，且不得建立 `cache_store/`。
5. `Loaded Runtime Cache`、`Model Execution` 與 `Provider Adapter` 保持各自獨立的未來 BC；本 topic 不實作它們。
6. 演進順序固定為 Identity → Response Reuse → Loaded Runtime Cache → Model Execution → Provider Adapter。
7. 既有 root package `__init__.py` 和 direct-import 行為不變。

## Constraints

- 不新增 child `__init__.py`、Python module、public API、動態 import、測試替身、dependency 或舊 gateway 相容層。
- 本 topic 只可修改十個 implementation paths；其他 tracked path 一律不在 scope。
- 本 topic 不建立 release，也不宣告 stable-library surface。
