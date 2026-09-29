# Response Reuse Eligibility Policy — Technical Specification

## Authority and scope

本 technical spec 是 `response-reuse-eligibility-policy` 的 execution-facing source of truth；
`requirements.md` 是 business-intent guardrail。它完整採納已鎖定的 chat plan，且不重新開啟 module、API、
failure mapping、scope 或 path decisions。

Response Reuse 依架構負責判定既有 response 是否可安全重用；Identity BC 仍是 identity 的唯一 authority。
`confirmed_identity` 在本 BC 中保持 opaque，CacheStore 保持內部保存元件。Loaded Runtime Cache、Model
Execution 與 Provider Adapter 仍是不同 topic。

## Python contract

| Module | Contract |
| --- | --- |
| `src/deterministic_response_cache/response_reuse/eligibility/policy.py` | 僅依賴標準庫；定義 frozen、slotted、field-less 的 `ReuseAllowed` 與 `ReuseDenied` dataclass value objects、`ReuseEligibilityDecision = ReuseAllowed \| ReuseDenied`，以及 generic structural `ReuseEligibilityPolicy[ResponseT](Protocol)`。其唯一 method 為 `evaluate(self, response: ResponseT, /) -> ReuseEligibilityDecision`。此 module 不得 import protocol、outcomes、CacheStore、Identity 或其他 BC。 |
| `src/deterministic_response_cache/response_reuse/protocol.py` | 單向 import `eligibility.policy`，並把 constructor 固定為 `ResponseReuseProtocol(store: CacheStore[IdentityT, ResponseT], *, eligibility_policy: ReuseEligibilityPolicy[ResponseT])`。`eligibility_policy` 無預設值、只能 keyword 傳入，故 omission 與 positional passing 都是 Python `TypeError` source break。`lookup` 與 `record` method signatures 及 outcome unions 不變。 |

唯一支援的 eligibility contracts import 是：

```python
from deterministic_response_cache.response_reuse.eligibility.policy import (
    ReuseAllowed,
    ReuseDenied,
    ReuseEligibilityDecision,
    ReuseEligibilityPolicy,
)
```

不得新增 `response_reuse/__init__.py`、`eligibility/__init__.py`、root re-export、facade、`__all__`
gateway 或 `.gitkeep`。不使用 `Any`、cast 或 runtime identity inspection。

## Exact lookup contract

1. `lookup(confirmed_identity)` 對 `store.read(confirmed_identity)` 呼叫恰好一次，並原樣傳遞同一 identity
   object，不解讀其內容。
2. `NotFound()` 回傳 `Miss()`；policy call count 為 `0`。
3. `CacheStoreFailure()` 回傳 `Unavailable()`；policy call count 為 `0`，且不得降級為 `Miss()`。
4. `None` 是既有 invalid read channel，raise
   `TypeError("CacheStore.read must not return None")`；policy call count 為 `0`。
5. Store read exception 原樣傳播；policy call count 為 `0`。
6. 任何其他合法 response object 都以同一 object 傳給 `eligibility_policy.evaluate(response)` 恰好一次。
7. `ReuseAllowed()` 回傳 `Hit(response)`，且 `Hit.response is response`。
8. `ReuseDenied()` 回傳 `Miss()`；不得暴露 response、呼叫 `store.write` 或執行任何 downstream 行為。
9. `None`、`True`、`False` 或任何非兩個 decision value object 的 policy result 一律 raise `TypeError`；
   不建立新的 exact error-message contract，且不得使用 truthiness。
10. policy exception 原樣傳播；不得映射為 `Miss()` 或 `Unavailable()`。

## Exact record contract

`record(confirmed_identity, response)` 不讀 store、不執行 policy，並完整維持既有行為：
`TokenWritten()` 映射 `Cached(response)`；`CacheStoreWriteFailure()` 映射 `NotCached(response)`；foreign write
channel 為既有 `TypeError`；store write exception 原樣傳播；所有 outcome 保留同一 response object。

## Implementation subject and test contract

唯一 implementation subject 是以下五個 path，且無 deletion：

| Change | Exact path | Required contract |
| --- | --- | --- |
| Write | `src/deterministic_response_cache/response_reuse/eligibility/policy.py` | Eligibility decisions、union、generic policy Protocol，以及標準庫-only leaf boundary。 |
| Modify | `src/deterministic_response_cache/response_reuse/protocol.py` | Required keyword-only policy injection 與 exact lookup decision mapping；record 不變。 |
| Write | `tests/test_response_reuse_eligibility.py` | Defining-module direct imports、decision VO semantics、union/structural Protocol typing 與 module boundary proof。 |
| Modify | `tests/test_response_reuse_protocol.py` | 所有 construction 顯式注入 typed fake policy；保留 assertions，新增 allow/deny/invalid/exception/short-circuit/source-break/record zero-call proof。 |
| Modify | `tests/response_reuse/test_in_memory_store.py` | 只在 protocol construction 注入 deterministic allow policy，保留既有 store integration assertions。 |

Tests 必須覆蓋 allow、deny、invalid `None`／`bool`／foreign decision、policy exception、store
`NotFound`、`CacheStoreFailure`、invalid `None` read、store exception、constructor source break、record zero-call
matrix 與 existing InMemory integration。既有 direct imports、fixtures、mocks 與 assertions 不得被刪除、弱化或以
dynamic import 取代。
