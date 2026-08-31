# Architecture Brief: Business Capability Baseline

## Confirmation gate

這份 brief 是互動式架構圖的設計輸入。scene 與 viewer 必須等此 brief 經人工確認後才可建立。

## Thesis

**identify → reuse → retain → execute**

以模型與完整請求身分為前提，先安全重用 response；未來才重用已載入 runtime 並協調模型執行。

## Planes

| Plane | Role | Phase |
| --- | --- | --- |
| Consumer integration | 外部 Python consumer 提交模型與請求脈絡、接收結果；不屬於 library 核心。 | External |
| Identity authority | 唯一確認模型身分與完整請求身分。 | Foundation |
| Response reuse | 根據已確認 identity 決定是否安全重用，並擁有內部 CacheStore。 | Now |
| Runtime retention | 重用已初始化 runtime，並擁有獨立 Runtime Store／Runtime Registry。 | Future |
| Model execution | 在 reuse miss 後協調 runtime 與模型執行。 | Future |
| Provider boundary | 以可替換 local／remote adapter 對接實際 provider。 | Future / External |

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
| Safe reuse decision | Response reuse | Owned abstraction | 分出 hit 與 miss。 | 不建立 identity。 |
| CacheStore | Response reuse | Owned abstraction | 保存與取回 response。 | 內部元件，不是頂層 BC。 |
| Reused response return | Response reuse | Owned abstraction | 將可安全重用 response 交還 consumer。 | 不呼叫 runtime。 |
| Loaded Runtime Cache | Runtime retention | Owned abstraction | 重用 initialized runtime。 | 未來能力，非 Response Reuse 一部分。 |
| Runtime Store / Registry | Runtime retention | Owned abstraction | 保存 runtime retention state。 | 與 CacheStore 分離。 |
| Runtime preparation | Runtime retention | Owned abstraction | 為 miss path 準備 runtime。 | 不保存 response。 |
| Model Execution | Model execution | Owned abstraction | 協調模型執行。 | 不擁有 identity 或 reuse 規則。 |
| Execution result handoff | Model execution | Owned abstraction | 將新結果交回 Response Reuse。 | 不直接保存 response。 |
| Provider adapter boundary | Provider boundary | Swappable infra surface | 將核心連到 provider。 | 可替換，位於核心外部。 |
| Local provider adapter | Provider boundary | Swappable infra surface | 對接 local provider。 | 未來 capability。 |
| Remote provider adapter | Provider boundary | Swappable infra surface | 對接 remote provider。 | 未來 capability。 |

## Main data and control flows

1. Python consumer 將模型與請求脈絡交給 Identity authority。
2. Model identity 與 Complete request identity 匯入 Identity confirmation。
3. Identity confirmation 將已確認 identity 交給 Response Reuse BC。
4. Response Reuse BC 查詢內部 CacheStore。
5. Safe reuse decision 在 hit 時走向 Reused response return，再回到 Result receiver。
6. Safe reuse decision 在 miss 時走向未來的 Loaded Runtime Cache。
7. Loaded Runtime Cache 使用其獨立 Runtime Store／Registry。
8. Runtime preparation 將可執行 runtime 交給未來的 Model Execution。
9. Model Execution 透過 Provider adapter boundary 呼叫可替換的 Local 或 Remote provider adapter。
10. Provider adapter 將執行結果交回 Execution result handoff。
11. Execution result handoff 將新結果交回 Response Reuse BC。
12. Response Reuse BC 透過 CacheStore 保存新 response。
13. Response Reuse BC 將新結果交還 Result receiver。

## Phase split

**現在承諾**：Identity authority 與 Response Reuse 的方向和責任邊界；本 repository 尚未實作它們。

**未來演進**：Loaded Runtime Cache、Runtime Store／Runtime Registry、Model Execution、Provider adapter boundary，以及任何 local／remote adapter。

## Diagram acceptance checks

- Current planes 必須和 future planes 使用明顯不同的視覺層級。
- CacheStore 必須放在 Response Reuse BC 內部。
- Runtime Store／Runtime Registry 必須獨立於 CacheStore。
- Provider boundary 必須位於核心外，並呈現為可替換 surface。
- 所有 identity flow 都必須由 Identity authority 匯出，而不是由其他 component 重新建立。
