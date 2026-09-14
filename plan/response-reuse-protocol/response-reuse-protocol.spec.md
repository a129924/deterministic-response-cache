# response-reuse-protocol Specification

## Acceptance Criteria

1. `ResponseReuseProtocol.lookup` 接受 generic opaque `confirmed_identity`，只將同一 object 交給
   CacheStore `read`，且不 import 或解讀 Identity implementation。
2. `read` 回傳 response 時，`lookup` 回傳 `Hit(response)`；`read` 回傳 `None` 時，回傳 `Miss()`。
3. `read` 拋出 `CacheStoreFailure` 時，`lookup` 回傳 `Unavailable()`，不得回傳 `Miss()`。
4. `ResponseReuseProtocol.record` 將原 identity 與 response 交給 CacheStore `write`；成功回傳
   `Cached(response)`，`CacheStoreFailure` 回傳 `NotCached(response)`，兩者皆保留同一 response object。
5. 五個 architecture surfaces 同步呈現獨立可交付的 Response Reuse Protocol、Identity authority、
   CacheStore internal-only boundary、future BC separation，以及 Hit/Miss/Unavailable/Cached/NotCached flow。
6. implementation subject 只改變 declared ten implementation paths；`.gitkeep`、root exports、README、
   version、configuration 與現有 direct-import regression 均維持不變。

## Behavioral Scenarios

### Scenario 1: reusable response hit

- **Given**: CacheStore 對同一 `confirmed_identity` 的 `read` 回傳 stored response。
- **When**: consumer 呼叫 `ResponseReuseProtocol.lookup`。
- **Then**: 結果是含相同 response object 的 `Hit`，且不涉及任何 runtime、execution 或 provider call。

### Scenario 2: miss handoff boundary

- **Given**: CacheStore 對 absent、invalid 或 expired entry 回傳 `None`。
- **When**: consumer 呼叫 `lookup`。
- **Then**: 結果是 `Miss()`；Protocol 不執行 downstream work，文件只把後續 path 標為 future handoff。

### Scenario 3: store unavailable

- **Given**: CacheStore `read` 拋出 `CacheStoreFailure`。
- **When**: consumer 呼叫 `lookup`。
- **Then**: 結果是 `Unavailable()`，不把 operational failure 隱藏為 cache miss。

### Scenario 4: response retention attempt

- **Given**: future boundary 已提供同一 confirmed identity 與新 response。
- **When**: consumer 呼叫 `record`。
- **Then**: `write` 成功得到 `Cached(response)`；若 `write` 拋出 `CacheStoreFailure`，得到
  `NotCached(response)`，原 response 仍可交付。

## Error / Edge Cases

- CacheStore 自行處理 entry validity、expiry 與 removal policy；它以 `None` 表達無可用 entry，Protocol
  不新增 TTL 或 eviction policy。
- `CacheStoreFailure` 以外的 exception 是 contract/programming failure，必須 propagate，不能被分類為
  `Miss`、`Unavailable` 或 `NotCached`。
- `None` 不可作為可 cache response value，因為 port 將它保留為 no-usable-entry sentinel。
- 不允許新增 `response_reuse/__init__.py` 或 root-package re-export；唯一支援的 imports 是直接 module path。
