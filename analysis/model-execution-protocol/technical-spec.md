# model-execution-protocol — Technical Specification

## 來源與交付

本 spec 將 `analysis/model-execution-protocol/requirements.md` 的業務規則落成同步、provider-neutral 的 Model Execution 契約。唯一 production 寫入面是 `src/deterministic_response_cache/model_execution/` 下三個新 module；測試寫入面是 `tests/test_model_execution_protocol.py`。不修改其他 BC、package initializer、README、VERSION、設定或 dependency。

## 公開契約

- `ports.py` 定義三個 generic `Protocol`：`RuntimeAccess[RuntimeRequestT, RuntimeT]` 的 `resolve(request)` 與 `prepare(request)`；`ModelInvoker[RuntimeT, InvocationT, ResponseT]` 的 `invoke(runtime, invocation)`。所有方法同步，資料參數保持 opaque。
- `outcomes.py` 定義 frozen、slotted value objects：`RuntimeReady(runtime)`、`RuntimeMissing()`、`RuntimeUnavailable()`、`RuntimePreparationFailed()`、`InvocationSucceeded(response)`、`InvocationFailed()`，以及對應的 port return union；Model Execution 的 public outcome 為 `Executed(response)`、`ExecutionFailed(reason)`。`ExecutionFailureReason` 是 `RUNTIME_UNAVAILABLE`、`RUNTIME_PREPARATION_FAILED`、`INVOCATION_FAILED` 三種 enum 值。失敗型別沒有 response 欄位。
- `RuntimeAccess.resolve` 僅可回傳 `RuntimeReady | RuntimeMissing | RuntimeUnavailable`；`prepare` 僅可回傳 `RuntimeReady | RuntimePreparationFailed`；`ModelInvoker.invoke` 僅可回傳 `InvocationSucceeded | InvocationFailed`。這些是本 BC 自有 port contract，不聲稱與 Loaded Runtime Cache PR #7 的型別或簽名相同。
- `protocol.py` 定義 `ModelExecutionProtocol(runtime_access, invoker)` 與 `execute(runtime_request, invocation) -> Executed[ResponseT] | ExecutionFailed`。以 generic type parameters 分別表達 runtime request、runtime、invocation、response；只支援 defining-module direct imports，不建立 re-export/facade。

## 決定性流程

1. `execute` 呼叫 `resolve` 恰一次。`RuntimeReady` 直接進入 invocation；`RuntimeMissing` 呼叫 `prepare` 恰一次；`RuntimeUnavailable` 直接回傳 `ExecutionFailed(RUNTIME_UNAVAILABLE)`。
2. `prepare` 回傳 `RuntimeReady` 後進入 invocation；`RuntimePreparationFailed` 回傳 `ExecutionFailed(RUNTIME_PREPARATION_FAILED)`。
3. `invoke` 呼叫恰一次；`InvocationSucceeded` 回傳 `Executed` 並保留同一 response object；`InvocationFailed` 回傳 `ExecutionFailed(INVOCATION_FAILED)`。
4. port 回傳 `None` 或非宣告結果是 contract violation，raise `TypeError`；port 自身拋出的 exception 原樣傳播，不推測為某個業務失敗。這些 exception 不產生 `Executed`。
5. `runtime_request` 與 `invocation` 原樣傳給 port；Model Execution 不 inspect、hash、compare 或轉換兩者。`RuntimeReady.runtime` 原樣交給 invoker，不管理其關閉或保存。

## 驗證與相依 gate

- `tests/test_model_execution_protocol.py` 以 direct imports、typed fakes 驗證所有 outcome mapping、呼叫順序與次數、opaque object identity、foreign/`None` return 和 exception propagation；無真實 I/O。
- 使用 repo 現有 `uv run ruff check ...`、`uv run pyright`、`uv run pytest ...` 驗證。Tester 對 immutable subject 記錄實際 command 與 exit code。
- PR #7 最終契約若要求不同的 runtime semantics 或本 topic 宣告路徑外的 adapter/組裝，先回 Planner/架構確認；不得在本 topic 直接修改 Loaded Runtime Cache 或 Provider Adapter。
