# model-execution-protocol Specification

## Acceptance Criteria

1. 呼叫端注入同步 `RuntimeAccess` 與 `ModelInvoker` 後，可在未接入真實 runtime 或 provider 下呼叫 `ModelExecutionProtocol.execute(runtime_request, invocation)`。
2. resolve 回傳 `RuntimeReady(runtime)` 時，prepare 呼叫零次、invoke 呼叫一次，並回傳保留同一 response object 的 `Executed(response)`。
3. resolve 回傳 `RuntimeMissing()` 時，prepare 呼叫一次；其 `RuntimeReady(runtime)` 使 invoke 呼叫一次並回傳 `Executed(response)`。
4. resolve 回傳 `RuntimeUnavailable()` 時，回傳 `ExecutionFailed(RUNTIME_UNAVAILABLE)`，且 prepare/invoke 均未呼叫。
5. prepare 回傳 `RuntimePreparationFailed()` 時，回傳 `ExecutionFailed(RUNTIME_PREPARATION_FAILED)`，且 invoke 未呼叫。
6. invoke 回傳 `InvocationFailed()` 時，回傳 `ExecutionFailed(INVOCATION_FAILED)`；所有 failure 均無 response 欄位，也不呼叫 Response Reuse `record`。
7. 每次 execute 最多呼叫 resolve、prepare、invoke 各一次；`runtime_request`、`invocation` 與 ready `runtime` 皆原 object 傳遞，不建立或解讀 identity。
8. 每個 port 回傳 `None` 或宣告 union 外的值均 raise `TypeError`；port 自行拋出的 exception 原樣傳播，不能被轉成任一業務 failure。
9. 新 module 可以 direct import，既有 Identity、Response Reuse 與 package import regressions 均維持通過。

## Behavioral Scenarios

### Scenario 1: 既有 runtime

- **Given:** 外部已判定 Response Reuse `Miss()`；runtime access 的 resolve 回傳 `RuntimeReady(runtime)`。
- **When:** 外部以 opaque runtime request 與 invocation request 呼叫 execute。
- **Then:** invoker 使用同一 runtime 執行一次，交回 `Executed(response)`；沒有 prepare 或自行 record。

### Scenario 2: runtime 缺失後準備成功

- **Given:** resolve 回傳 `RuntimeMissing()`，prepare 回傳 `RuntimeReady(runtime)`。
- **When:** 呼叫 execute。
- **Then:** 依 resolve → prepare → invoke 順序各呼叫一次，交回 `Executed(response)`。

### Scenario 3: runtime 不可用

- **Given:** resolve 回傳 `RuntimeUnavailable()`。
- **When:** 呼叫 execute。
- **Then:** 交回 `ExecutionFailed(RUNTIME_UNAVAILABLE)`，不呼叫 prepare/invoke，且無 response。

### Scenario 4: 準備失敗

- **Given:** resolve 回傳 `RuntimeMissing()`，prepare 回傳 `RuntimePreparationFailed()`。
- **When:** 呼叫 execute。
- **Then:** 交回 `ExecutionFailed(RUNTIME_PREPARATION_FAILED)`，不呼叫 invoke，且無 response。

### Scenario 5: invocation 失敗

- **Given:** runtime 已 ready，invoker 回傳 `InvocationFailed()`。
- **When:** 呼叫 execute。
- **Then:** 交回 `ExecutionFailed(INVOCATION_FAILED)`，且無 response。

## Error / Edge Cases

- resolve、prepare 或 invoke 的 foreign/`None` result 各自構成 port contract violation；`TypeError` 後不得繼續至下一步。
- 任一 port 拋出 exception 時原樣傳播，不製造成功 response、不進行 retry。
- 本契約不定義 `ModelIdentity`→runtime key 映射、PR #7 實際 API 或 provider adapter；需要接線時由後續 topic 規劃。
