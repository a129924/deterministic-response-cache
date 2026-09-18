# response-reuse-eligibility-policy Specification

## Acceptance Criteria

1. `ReuseAllowed` 與 `ReuseDenied` 是 distinct、field-less、frozen、slotted value objects；
   `ReuseEligibilityDecision` 只由這兩者組成，且 `ReuseEligibilityPolicy[ResponseT]` 是只有
   `evaluate(response: ResponseT, /) -> ReuseEligibilityDecision` 的 generic structural Protocol。
2. eligibility contracts 只可從
   `deterministic_response_cache.response_reuse.eligibility.policy` direct import；該 leaf 只依賴標準庫，
   `protocol.py` 單向依賴它，且不建立 initializer、re-export、gateway 或 `.gitkeep`。
3. `ResponseReuseProtocol` 必須要求 keyword-only `eligibility_policy`；省略或 positional passing policy
   都得到 Python `TypeError`，且沒有 default／fallback policy。
4. lookup 的 successful response path 對同一 response object 恰好 call policy 一次；`ReuseAllowed()`
   回傳同一 response object 的 `Hit`，`ReuseDenied()` 回傳 `Miss()` 且不 write store、不洩漏 response、不做
   downstream work。
5. `NotFound()` 維持 `Miss()`、`CacheStoreFailure()` 維持 `Unavailable()`、invalid `None` read 維持
   `TypeError("CacheStore.read must not return None")`、store read exception 原樣傳播；上述路徑都不呼叫 policy。
6. policy 的 `None`、`bool` 或 foreign object result 一律 raise `TypeError`，不得依 truthiness mapping；
   policy exception 原樣傳播，不得改成 cache outcome。
7. `record` 不呼叫 policy，並完整保留既有 `Cached`／`NotCached`、foreign write channel、exception、
   identity/response object identity 和 InMemory integration contract。
8. immutable implementation subject 恰好為兩個 Written、三個 Modified paths；沒有 deletion、initializer、
   re-export、dynamic import、README/VERSION/configuration/dependency/architecture/future-BC path change。

## Behavioral Scenarios

### Scenario 1: policy permits a stored response

- **Given**: `store.read` 對 opaque confirmed identity 回傳 response object，且 injected policy 對同一 object
  回傳 `ReuseAllowed()`。
- **When**: consumer 呼叫 `ResponseReuseProtocol.lookup`。
- **Then**: store read 與 policy evaluation 各恰好一次，結果是 `Hit(response)`，且 outcome response 是同一
  object；不 write store 或執行 future/downstream behavior。

### Scenario 2: policy denies a stored response

- **Given**: `store.read` 回傳 response object，且 injected policy 回傳 `ReuseDenied()`。
- **When**: consumer 呼叫 `lookup`。
- **Then**: 結果是 `Miss()`；policy 只被呼叫一次，response 不會出現在 outcome，store 不被 write，且
  Response Reuse 不執行模型、runtime 或 provider work。

### Scenario 3: storage channels short-circuit before policy

- **Given**: store read 分別回傳 `NotFound()`、`CacheStoreFailure()`、invalid `None` 或拋出 exception。
- **When**: consumer 呼叫 `lookup`。
- **Then**: 結果分別為 `Miss()`、`Unavailable()`、既有 fixed-message `TypeError`、相同 exception；每一條
  path 的 policy call count 都是 `0`。

### Scenario 4: policy result is not a decision

- **Given**: store read 成功回傳 response，而 policy 回傳 `None`、`True`、`False` 或 foreign object，或
  policy 自己拋出 exception。
- **When**: consumer 呼叫 `lookup`。
- **Then**: invalid result raise `TypeError`，不得使用 truthiness；policy exception 原樣傳播，兩者都不被
  改寫為 `Miss()` 或 `Unavailable()`。

### Scenario 5: record remains retention-independent

- **Given**: any injected policy and a store that returns either existing valid write channel。
- **When**: consumer 呼叫 `record`。
- **Then**: policy call count 是 `0`，而既有 `Cached(response)`／`NotCached(response)` mapping 與 payload
  identity 不變。

## Error / Edge Cases

- policy 不能接收、解讀、儲存或推測 identity；identity 繼續以 opaque generic input 原樣流向 CacheStore。
- `bool` 即使是 Python 的 object 也不是 policy decision；任何 third decision state 或 duck-typed object 都不
  能成為 allow/deny。
- `CacheStoreFailure()` 是 explicit unavailable value channel，絕不可被 policy 或 protocol 壓縮為 `Miss()`。
- invalid `None` read 的現有 exact `TypeError` message 必須保留；policy invalid decision 不新增 exact message
  promise。
- existing tests 的 direct imports、fixtures、mocks 和 assertions 均為 preservation contract；不得以
  `importlib`、`__import__` 或 `sys.modules` substitution 取代。
- 如果 implementation 需要第六個 path、任何 deletion、new initializer/export/dependency，或與此 spec
  不一致的 policy rule，必須停止並返回 Planner。
