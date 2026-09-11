# Evolution Roadmap

## Pipeline

模型／請求身分確認

→ Response 是否可安全重用？

→ 可重用時直接回傳 response

→ 不可重用時，未來由 Loaded Runtime Cache 取得或準備 runtime

→ 未來由 Model Execution 執行模型

→ Response Reuse 保存新 response

→ 回傳結果

## 演進順序

1. **Identity foundation**：固定模型與完整請求身分的唯一 authority。
2. **Response Reuse**：以已確認 identity 決定 response 是否可安全重用。
3. **Loaded Runtime Cache**：以獨立的 Runtime Store／Runtime Registry 重用 initialized runtime。
4. **Model Execution**：協調 runtime 與模型執行。
5. **Provider Adapter**：在可替換邊界對接具體 local／remote provider。

每個階段都需要獨立 topic plan。前一階段不得偷帶下一階段的責任。

## Package topology reservation

本 topic 只預先建立下列 directory topology；每個 `.gitkeep` 是純文字 topology-reservation marker。directory 可被 Python 解析為 implicit namespace subpackage，但 marker 不提供 executable module、public symbol 或 re-export，也不代表 BC 已實作或可使用；不建立 `cache_store/` 頂層目錄。

| Implementation order | BC | Reserved directory |
| --- | --- | --- |
| 1 | Identity | `src/deterministic_response_cache/identity/` |
| 2 | Response Reuse | `src/deterministic_response_cache/response_reuse/` |
| 3 | Loaded Runtime Cache | `src/deterministic_response_cache/loaded_runtime_cache/` |
| 4 | Model Execution | `src/deterministic_response_cache/model_execution/` |
| 5 | Provider Adapter | `src/deterministic_response_cache/provider_adapter/`（僅預留 BC topology；具體 provider integration 維持核心外部且可替換） |

Identity 是第一個後續 implementation topic；Response Reuse 只能在 Identity 已獨立規劃與實作後進行。Loaded Runtime Cache、Model Execution 與 Provider Adapter 各自保留為後續獨立 BC。本 baseline 只定義方向、責任與 topology，不是任何 BC 的實作承諾。
