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

## 現在與未來

本 baseline 只定義方向與責任。第一個後續實作 topic 將聚焦 Response Reuse，並保持 provider-agnostic。Loaded Runtime Cache、Model Execution 與 Provider Adapter 都是未來能力，不是現在的實作承諾。
