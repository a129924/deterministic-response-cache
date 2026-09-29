# model-execution-protocol — Technical Specification

## 來源與交付

本 spec 將 `analysis/model-execution-protocol/requirements.md` 的業務規則落成同步、provider-neutral 的 Model Execution 契約。immutable predecessor implementation 已在 `src/deterministic_response_cache/model_execution/` 下三個新 module 與 `tests/test_model_execution_protocol.py` 交付。本次 PR-comment architecture amendment 不改該 Python/test surface，只同步五份架構來源；不修改其他 BC、package initializer、README、VERSION、設定或 dependency。

## 公開契約

- `ports.py` 定義兩個 generic `Protocol`：`RuntimeAccess[RuntimeRequestT, RuntimeT]` 的 `resolve(request)` 與 `prepare(request)`；`ModelInvoker[RuntimeT, InvocationT, ResponseT]` 的 `invoke(runtime, invocation)`。所有方法同步，資料參數保持 opaque。
- `outcomes.py` 定義 frozen、slotted value objects：`RuntimeReady(runtime)`、`RuntimeMissing()`、`RuntimeUnavailable()`、`RuntimePreparationFailed()`、`InvocationSucceeded(response)`、`InvocationFailed()`，以及對應的 port return union；Model Execution 的 public outcome 為 `Executed(response)`、`ExecutionFailed(reason)`。`ExecutionFailureReason` 是 `RUNTIME_UNAVAILABLE`、`RUNTIME_PREPARATION_FAILED`、`INVOCATION_FAILED` 三種 enum 值。失敗型別沒有 response 欄位。
- `RuntimeAccess.resolve` 僅可回傳 `RuntimeReady | RuntimeMissing | RuntimeUnavailable`；`prepare` 僅可回傳 `RuntimeReady | RuntimePreparationFailed`；`ModelInvoker.invoke` 僅可回傳 `InvocationSucceeded | InvocationFailed`。這些是本 BC 自有 port contract，不聲稱與 Loaded Runtime Cache PR #7 的型別或簽名相同。
- `protocol.py` 定義 `ModelExecutionProtocol(runtime_access, invoker)` 與 `execute(runtime_request, invocation) -> Executed[ResponseT] | ExecutionFailed`。以 generic type parameters 分別表達 runtime request、runtime、invocation、response；只支援 defining-module direct imports，不建立 re-export/facade。

## 決定性流程

1. `protocol.py` 以 `execute`、`_prepare_and_invoke`、`_invoke` 三個 method 分工；各 method 只使用一層 `match/case`，不得巢狀 `match`。
2. `execute` 只處理 `resolve`，並呼叫它恰一次：`RuntimeReady` 呼叫 `_invoke`；`RuntimeMissing` 呼叫 `_prepare_and_invoke`；`RuntimeUnavailable` 回傳 `ExecutionFailed(RUNTIME_UNAVAILABLE)`；其他結果（含 `None`）由 wildcard case raise `TypeError`。
3. `_prepare_and_invoke` 只處理 `prepare`，並呼叫它恰一次：`RuntimeReady` 呼叫 `_invoke`；`RuntimePreparationFailed` 回傳 `ExecutionFailed(RUNTIME_PREPARATION_FAILED)`；其他結果（含 `None`）由 wildcard case raise `TypeError`。
4. `_invoke` 只處理 `invoke`，並呼叫它恰一次：`InvocationSucceeded` 回傳 `Executed` 並保留同一 response object；`InvocationFailed` 回傳 `ExecutionFailed(INVOCATION_FAILED)`；其他結果（含 `None`）由 wildcard case raise `TypeError`。
5. port 自身拋出的 exception 原樣傳播，不推測為某個業務失敗，也不 retry；每次 `execute` 對各 port 最多呼叫一次。這些 exception 不產生 `Executed`。
6. `runtime_request` 與 `invocation` 原樣傳給 port；Model Execution 不 inspect、hash、compare 或轉換兩者。`RuntimeReady.runtime` 原樣交給 invoker，不管理其關閉或保存。

## 驗證與相依 gate

- `tests/test_model_execution_protocol.py` 以 direct imports、typed fakes 驗證所有 outcome mapping、呼叫順序與次數、opaque object identity、foreign/`None` return 和 exception propagation；無真實 I/O。
- 使用 repo 現有 `uv run ruff check ...`、`uv run pyright`、`uv run pytest ...` 驗證。Tester 對 immutable subject 記錄實際 command 與 exit code。
- PR #7 最終契約若要求不同的 runtime semantics 或本 topic 宣告路徑外的 adapter/組裝，先回 Planner/架構確認；不得在本 topic 直接修改 Loaded Runtime Cache 或 Provider Adapter。

## Architecture status correction

### Trigger 與語意

- Exact thread：`PRRT_kwDOUJTij86lAh0Z`。correction id 固定為 `model-execution-protocol/pr-comment-architecture-status`。
- 已實作狀態只涵蓋 provider-neutral、同步、可注入的 Model Execution coordination contracts：runtime access／invocation ports、outcomes 與 protocol orchestration。
- future 狀態固定涵蓋 Loaded Runtime Cache 實際 wiring、retention/backend、具體 Provider Adapter、cross-BC composition，以及 Response Reuse `Miss`／execution result handoff integration。五份架構來源不得把任一項寫成已整合，也不得把已交付的 coordination contracts 繼續全部標成 future。
- correction 不改 Python contract、行為或 tests；predecessor `b2847eb2e7ac0ed65a5bef8c33d13cb3248aee99`、`5145a59be17a3845da074d88e8530b59bfb45e57`、`868df3b338e022371a55a2125b270a52ba1c6874`、`12bdfb1b5350ee71e3af70df38a462ce9286fba5`、`dee1740b73d0274445d0c3967272d0475d82e779` 與 PR HEAD `9a3460b6e4412384ed7e3426ebc32820a46818e6` 都是 immutable provenance，不能充當本 correction 的 approval。

### Exact write surface

correction implementation subject 必須且只能修改：

1. `docs/business-capability-architecture.md`
2. `docs/evolution-roadmap.md`
3. `docs/architecture/business-capability/architecture-brief.md`
4. `docs/architecture/business-capability/scene.js`
5. `docs/architecture/business-capability/index.html`

不得新增、刪除或修改其他 path。`scene.js` 的完整內容必須與 `index.html` 中 start marker `  // ======================== SCENE START (generated) =========================` 和 end marker `  // ========================= SCENE END ======================================` 之間的內容 byte-for-byte 相同；這是既有 mirror 機制，不引入 generator。

### Correction validation

- 以 `git diff-tree --no-commit-id --name-status -r <subject>` 驗證 exact-five modified paths，且沒有 add/delete/rename。
- 以 `git diff --exit-code 9a3460b6e4412384ed7e3426ebc32820a46818e6 <subject> -- src tests` 驗證 Python 與 tests blobs 相對 predecessor 不變。
- 逐份檢查五個來源均同時描述已實作 coordination contracts 與仍屬 future 的四組整合責任；不得只修圖而留下文字來源互相矛盾。
- 以 `python -c 'from pathlib import Path; s=Path("docs/architecture/business-capability/scene.js").read_text(); h=Path("docs/architecture/business-capability/index.html").read_text(); a="  // ======================== SCENE START (generated) =========================\\n"; b="\\n  // ========================= SCENE END ======================================\\n"; assert h.count(a)==h.count(b)==1; assert h.split(a,1)[1].split(b,1)[0]==s'` 作 byte-for-byte mirror 比對；marker 缺失、多重或內容不等都 fail closed。
- 執行 `git diff --check <subject>^ <subject>` 與 `uv run pytest -q`；Tester 記錄實際 command 與 exit code，不預填結果。
