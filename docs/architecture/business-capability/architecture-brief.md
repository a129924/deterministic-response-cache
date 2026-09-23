# Architecture Brief: Business Capability Baseline

## Confirmation gate

這份 brief 是互動式架構圖的設計輸入。scene 與 viewer 必須等此 brief 經人工確認後才可建立。

## Thesis

**identify → reuse → retain → execute**

以模型與完整請求身分為前提，先安全重用 response。Model Execution 已提供 provider-neutral coordination contracts；runtime retention、provider 對接與跨 BC 組裝仍屬未來整合。

## Planes

| Plane | Role | Phase |
| --- | --- | --- |
| Consumer integration | 外部 Python consumer 提交模型與請求脈絡、接收結果；不屬於 library 核心。 | External |
| Identity authority | 唯一確認模型身分與完整請求身分，並交接 opaque confirmed identity。 | Conceptual order 1 |
| Response reuse | 根據 opaque confirmed identity 決定是否安全重用，並擁有內部 CacheStore。 | Independent Protocol topic / conceptual order 2 |
| Runtime retention | 重用已初始化 runtime，並擁有獨立 Runtime Store／Runtime Registry。 | Implementation order 3 |
| Model execution | 提供同步、可注入的 runtime access／invocation coordination contracts。 | Coordination contracts implemented / integration future |
| Provider boundary | 以可替換 local／remote adapter 對接實際 provider。 | Implementation order 5 / External |

## Components

| Component | Plane | Ownership | Responsibility | Non-obvious boundary |
| --- | --- | --- | --- | --- |
| Python consumer | Consumer integration | Swappable app surface | 使用 library capability。 | 不成為核心政策 owner。 |
| Request submission | Consumer integration | Swappable app surface | 將模型與請求脈絡交給核心。 | 不判定 reuse。 |
| Result receiver | Consumer integration | Swappable app surface | 接收可重用或新產生的結果。 | 不知道 provider。 |
| Model identity | Identity authority | Owned abstraction | 確認是否為同一模型。 | 不以名稱或路徑單獨保證身分。 |
| Complete request identity | Identity authority | Owned abstraction | 確認是否為同一完整請求。 | 不由 CacheStore 推測欄位。 |
| Identity confirmation | Identity authority | Owned abstraction | 交付已確認 identity。 | 是唯一 identity authority。 |
| Response Reuse BC | Response reuse | Owned abstraction | 決定是否安全重用。 | 不執行模型。 |
| Safe reuse decision | Response reuse | Owned abstraction | 分出 Hit、Miss 與 Unavailable。 | 不建立 identity，也不將 unavailable 降級為 miss。 |
| CacheStore | Response reuse | Owned abstraction | 保存與取回 response。 | 內部元件，不是頂層 BC。 |
| Reused response return | Response reuse | Owned abstraction | 將 Hit response 交還 consumer。 | 不呼叫 runtime。 |
| Retention result | Response reuse | Owned abstraction | 將新 response 的 Cached 或 NotCached 結果交還 consumer。 | NotCached 仍保留 response。 |
| Loaded Runtime Cache | Runtime retention | Owned abstraction | 重用 initialized runtime。 | 未來能力，非 Response Reuse 一部分。 |
| Runtime Store / Registry | Runtime retention | Owned abstraction | 保存 runtime retention state。 | 與 CacheStore 分離。 |
| Runtime preparation | Runtime retention | Owned abstraction | 為 miss path 準備 runtime。 | 不保存 response。 |
| Model Execution | Model execution | Owned abstraction | 已提供 runtime access／invocation ports、outcomes 與同步 protocol orchestration。 | 不擁有 identity、reuse、runtime retention 或 provider 規則。 |
| Execution result handoff | Model execution | Owned abstraction | 未來將新結果交回 Response Reuse。 | 尚未整合，且不直接保存 response。 |
| Provider adapter boundary | Provider boundary | Swappable infra surface | 將核心連到 provider。 | 可替換，位於核心外部。 |
| Local provider adapter | Provider boundary | Swappable infra surface | 對接 local provider。 | 未來 capability。 |
| Remote provider adapter | Provider boundary | Swappable infra surface | 對接 remote provider。 | 未來 capability。 |

## Main data and control flows

1. Python consumer 將模型與請求脈絡交給 Identity authority。
2. Model identity 與 Complete request identity 匯入 Identity confirmation。
3. Identity confirmation 將已確認 identity 交給 Response Reuse BC。
4. Response Reuse BC 查詢內部 CacheStore。
5. Safe reuse decision 在 Hit 時走向 Reused response return，再回到 Result receiver；在 Unavailable 時停在 Response Reuse boundary。
6. Safe reuse decision 在 Miss 時走向未來的 Loaded Runtime Cache；此 cross-BC handoff 尚未整合。
7. Loaded Runtime Cache 使用其獨立 Runtime Store／Registry。
8. Runtime preparation 未來將可執行 runtime 交給 Model Execution；Model Execution 的 injected runtime access contract 已實作，實際 wiring 尚未整合。
9. Model Execution 的 injected invocation contract 已實作；具體 Provider adapter 與 cross-BC composition 未來才會接上可替換的 Local 或 Remote provider adapter。
10. Provider adapter 將執行結果交回 Execution result handoff。
11. Execution result handoff 未來將新結果交回 Response Reuse BC；目前尚未整合。
12. Response Reuse BC 透過 CacheStore 嘗試保存新 response，產生 Cached 或保留 response 的 NotCached 結果。
13. Response Reuse BC 將 retention result 交還 Result receiver。

## Phase split

**Conceptual 演進順序**：Identity → Response Reuse → Loaded Runtime Cache → Model Execution → Provider Adapter。每個 BC 都需要獨立 topic；Response Reuse Protocol 可獨立實作，只消費 Identity authority 交接的 opaque confirmed identity，並不等待 Identity implementation completion。

**Topology 與交付狀態**：`identity/`、`response_reuse/`、`loaded_runtime_cache/`、`model_execution/`、`provider_adapter/` 位於 `src/deterministic_response_cache/` 下。每個 `.gitkeep` 只是 topology-reservation marker。Model Execution 已有 `outcomes.py`、`ports.py`、`protocol.py` executable modules 與 defining-module direct-import contracts；不建立 child package initializer、facade 或 re-export。

**邊界維持**：Identity 是模型與完整 request identity 的唯一 authority；CacheStore 僅在 Response Reuse 內部。Model Execution 的 provider-neutral coordination contracts 已實作，但 Loaded Runtime Cache 實際 wiring／retention/backend、具體 Provider Adapter、cross-BC composition，以及 Response Reuse `Miss`／execution result handoff integration 仍屬未來。三個 BC 維持獨立，具體 provider integration 仍在核心外部且可替換；目前不宣稱端到端 pipeline 已完成。

## Diagram acceptance checks

- Response Reuse 必須標示為 independent Protocol topic，而不是由 Identity implementation completion 解鎖。
- lookup 必須清楚呈現 Hit direct return、Miss future handoff 與 Unavailable boundary stop；record 必須呈現 Cached/NotCached retention result。
- 圖面必須區分已實作的 Model Execution coordination contracts 與仍屬 future 的 runtime/provider/cross-BC integration。
- CacheStore 必須放在 Response Reuse BC 內部。
- Runtime Store／Runtime Registry 必須獨立於 CacheStore。
- Provider boundary 必須位於核心外，並呈現為可替換 surface。
- 所有 identity flow 都必須由 Identity authority 匯出，而不是由其他 component 重新建立。
