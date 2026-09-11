# VO channel correction — Requirements

## Business intent

將 Response Reuse 的 CacheStore interaction 從 exception／`None` sentinel 改為明確、可比對的 value-object
channel。Protocol 必須只消費這些 channel，並以 `match`／`case` 將其轉換為既有 Response Reuse outcomes；它仍不得
解讀 identity、執行下游 pipeline 或擴張 BC 邊界。

## Required behavior

- `CacheStore.read(confirmed_identity)` 的完整回傳聯集為
  `ResponseT | NotFound | CacheStoreFailure`：
  - `ResponseT` 對應 `Hit(response)`；
  - `NotFound` 對應 `Miss()`；
  - `CacheStoreFailure` 對應 `Unavailable()`。
- `CacheStore.write(confirmed_identity, response)` 的完整回傳聯集為
  `TokenWritten | CacheStoreWriteFailure`：
  - `TokenWritten` 對應 `Cached(response)`；
  - `CacheStoreWriteFailure` 對應 `NotCached(response)`。
- `ResponseT`、`NotFound`、`CacheStoreFailure`、`TokenWritten` 與 `CacheStoreWriteFailure` 都不可為 `None`。
  `None` 不是任一 port、success 或 failure channel。
- 四個 channel (`NotFound`、`CacheStoreFailure`、`TokenWritten`、`CacheStoreWriteFailure`) 都是 immutable、slotted
  value object，且不得繼承 `Exception`。
- `ResponseReuseProtocol` 只可用 `match`／`case` 映射上述 contract 成員。`ResponseT` 在型別層指定且保持 opaque：
  所有 non-`None`、非 channel 的 read value 都是合法 `ResponseT`，必須原樣傳遞為 `Hit`。`None` 或 CacheStore
  對明確 read/write channel contract 的可偵測違反必須 raise `TypeError`，不得被轉換為 miss、unavailable、cached 或
  not-cached；不新增 runtime response validator。

## Scope limits

- 僅修正 `_cache_store.py`、`protocol.py`、`tests/test_response_reuse_protocol.py` 與
  `docs/business-capability-architecture.md`。
- 不變更 outcome type、identity contract、cache backend、持久化／TTL／invalidation、runtime、execution、provider、
  public exports、其他 architecture surfaces 或既有 PR/evidence provenance。
