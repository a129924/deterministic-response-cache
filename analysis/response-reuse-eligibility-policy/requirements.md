# Response Reuse Eligibility Policy — Requirements

## Intent

讓 Response Reuse BC 在 CacheStore 已讀得候選 response 時，依一個 provider-neutral 的 eligibility policy
判斷該 response 是否可安全重用。此 topic 只補足 lookup 的安全重用決策；不改變 Identity、保存、
retention 或下游模型執行責任。

## Business and boundary requirements

1. Identity BC 仍是模型身分與完整 request identity 的唯一 authority。Response Reuse 只接收 opaque
   `confirmed_identity`，將同一 object 交給 CacheStore；本 topic 不建立、驗證、比較、hash、序列化、
   import 或重新解讀 identity。
2. `ResponseReuseProtocol.lookup` 必須先對同一 `confirmed_identity` 呼叫一次 `CacheStore.read`。只有讀得
   response 後，才可對同一 response object 執行一次 eligibility evaluation。
3. policy 明確回傳 allow 時，lookup 回傳既有 `Hit(response)` 並保留同一 response object；policy 明確
   回傳 deny 時，lookup 回傳既有 `Miss()`，不得洩漏 response、寫入 store 或執行下游工作。
4. `NotFound()` 必須維持映射為 `Miss()`，`CacheStoreFailure()` 必須維持映射為 `Unavailable()`；這兩個
   channel、invalid `None` read 與 store exception 都不得呼叫 policy。既有 invalid `None` read 的
   `TypeError("CacheStore.read must not return None")` 合約維持不變。
5. policy 回傳 `None`、`bool` 或任何 foreign object 時必須 fail closed 為 `TypeError`，不使用
   truthiness，且不新增 exact error-message 合約。policy exception 原樣傳播，不得轉為 `Miss()` 或
   `Unavailable()`。
6. `record` 完全不呼叫 policy；既有 `Cached`／`NotCached` mapping、response identity、port-call 次數、
   invalid write channel 與 exception propagation 維持不變。
7. policy 必須 provider-neutral，且只接收 response；它不得接收 identity、store、runtime 或 provider
   context。實作只使用標準庫、保持同步、並以 direct defining-module import 提供 contracts。

## Delivery requirements

- 新增 `response_reuse/eligibility/policy.py` 作為有語意的 eligibility leaf module；同一 module 定義
  `ReuseAllowed`、`ReuseDenied`、`ReuseEligibilityDecision` 及 generic `ReuseEligibilityPolicy`。
- `ResponseReuseProtocol` constructor 必須要求 keyword-only `eligibility_policy`；不提供 positional、
  optional、default、allow-all 或 compatibility fallback。
- implementation subject 只可寫入 policy module 與 eligibility tests，並只可修改 protocol、protocol tests
  與 InMemory integration tests；不得刪除任何 path。
- 保留既有 direct imports、fixtures、mocks 與 assertions；不得以 `importlib`、`__import__` 或
  `sys.modules` substitution 取代 regression。
- 不修改 README、VERSION、package initializer、configuration、dependency、architecture authority 或任何
  future-BC path；不建立 `eligibility/__init__.py`、re-export、gateway 或 `.gitkeep`。
