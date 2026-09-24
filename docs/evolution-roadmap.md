# Evolution Roadmap

## Pipeline

模型／請求身分確認

→ Response Reuse Protocol lookup：Hit / Miss / Unavailable

→ Hit 時依保存的 codec id 解碼後回傳原生 `ModelResponse`；Unavailable 停在 Response Reuse boundary

→ Miss 時，未來由 Loaded Runtime Cache 取得或準備 runtime

→ Model Execution 已有同步、可注入的 coordination contracts；未來由 cross-BC composition 接上 runtime 與 provider 後執行模型

→ 未來新 response 以相同 confirmed identity 交回 Response Reuse record，編成 bytes envelope 後得到 Cached / NotCached

→ 回傳結果

## 演進順序

1. **Identity foundation**：固定模型與完整請求身分的唯一 authority。
2. **Response Reuse**：以已確認 identity 決定 response 是否可安全重用。
3. **Loaded Runtime Cache**：以獨立的 Runtime Store／Runtime Registry 重用 initialized runtime。
4. **Model Execution**：已交付 provider-neutral runtime access／invocation ports、outcomes 與同步 protocol orchestration。
5. **Provider Adapter**：在可替換邊界對接具體 local／remote provider。

每個階段都需要獨立 topic plan。這是 conceptual sequence，不是 Response Reuse Protocol 等待 Identity implementation completion 的 gate：Response Reuse 只消費 Identity authority 已確認的 opaque identity。前一階段不得偷帶下一階段的責任。

## Package topology and delivery status

下列 directory topology 隔離各 BC；每個 `.gitkeep` 只是純文字 topology-reservation marker。directory 可由 Python 解析為 implicit namespace subpackage，但 marker 本身不提供 executable module、public symbol 或 re-export。Model Execution 已在預留目錄內交付 executable modules，並維持 defining-module direct imports；不建立 child package initializer、facade、re-export 或 `cache_store/` 頂層目錄。

| Implementation order | BC | Reserved directory |
| --- | --- | --- |
| 1 | Identity | `src/deterministic_response_cache/identity/` |
| 2 | Response Reuse | `src/deterministic_response_cache/response_reuse/` |
| 3 | Loaded Runtime Cache | `src/deterministic_response_cache/loaded_runtime_cache/` |
| 4 | Model Execution | `src/deterministic_response_cache/model_execution/`（coordination contracts 已實作；runtime/provider/cross-BC wiring 仍屬未來） |
| 5 | Provider Adapter | `src/deterministic_response_cache/provider_adapter/`（僅預留 BC topology；具體 provider integration 維持核心外部且可替換） |

Identity 是第一個 conceptual implementation topic，也是模型與完整 request identity 的唯一 authority。Response Reuse Protocol 可獨立規劃與實作，但只消費由 Identity authority 交接的 opaque confirmed identity；它不實作或重解 identity。Model Execution 的 provider-neutral、同步、可注入 coordination contracts 已交付。Loaded Runtime Cache 的實際 wiring／retention/backend、具體 Provider Adapter、cross-BC composition，以及 Response Reuse `Miss`／execution result handoff integration 仍是後續獨立工作；目前不宣稱端到端 pipeline 已完成。
