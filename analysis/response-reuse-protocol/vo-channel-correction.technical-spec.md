# VO channel correction — Technical Specification

## Contract

`src/deterministic_response_cache/response_reuse/_cache_store.py` 定義內部 generic synchronous `CacheStore`
`Protocol` 及四個 frozen、slotted dataclass value object：`NotFound`、`CacheStoreFailure`、`TokenWritten`、
`CacheStoreWriteFailure`。它們不繼承 `Exception`，且不可用 `None` 代替。

```python
read(confirmed_identity: IdentityT) -> ResponseT | NotFound | CacheStoreFailure
write(confirmed_identity: IdentityT, response: ResponseT) -> TokenWritten | CacheStoreWriteFailure
```

`ResponseReuseProtocol` 使用 `match`／`case`，且只以 exact channel members 決定結果：

| Port result | Protocol result |
| --- | --- |
| `ResponseT` from `read` | `Hit(response)` |
| `NotFound` | `Miss()` |
| `CacheStoreFailure` | `Unavailable()` |
| `TokenWritten` | `Cached(original_response)` |
| `CacheStoreWriteFailure` | `NotCached(original_response)` |

`ResponseT` 在型別層指定且 opaque，不新增 runtime response validator。因此 read 的任何 non-`None`、非 channel value
都必須視為合法 `ResponseT`，並原樣回傳 `Hit`；`None` 是可偵測的 contract violation，必須 raise `TypeError`。write
只允許兩個可辨識 VO channels，任何其他 write value 均是可偵測的 contract violation，必須 raise `TypeError`。
Protocol 不得用 `try`／`except` 將任何 exception 或 value 轉成既有 outcome；store method 所拋出的 exception 必須
propagate。

## Implementation and test constraints

- 僅使用下列四個 implementation paths：
  - `src/deterministic_response_cache/response_reuse/_cache_store.py`
  - `src/deterministic_response_cache/response_reuse/protocol.py`
  - `tests/test_response_reuse_protocol.py`
  - `docs/business-capability-architecture.md`
- 測試保留 direct imports，並驗證每一 valid channel、read 的 `None` violation、write 的 foreign-value violation、
  read 的 opaque non-`None` response passthrough，以及 port method 所拋出的 exception 均不會被隱性分類。
  `read`／`write` 各僅呼叫一次，opaque identity 與 original response identity 必須保留。
- documentation 只更新 value-object channels 與 mapping；仍宣告 CacheStore 是 Response Reuse 的內部元件，且不新增
  未來 BC implementation。
