# Response Reuse Protocol — Technical Specification

## Authority and scope

本 technical spec 是 `response-reuse-protocol` 的 execution-facing source of truth；
`requirements.md` 是 business-intent guardrail。Human 已明確 override 舊 roadmap 中 Identity
implementation-completion 的前置敘述：Response Reuse Protocol 可獨立規劃與實作，只把
`confirmed_identity` 當作 opaque input；此 override 不改變 Identity 的唯一 authority。

## Python contract

| Module | Contract |
| --- | --- |
| `src/deterministic_response_cache/response_reuse/outcomes.py` | 定義 frozen、slotted、generic dataclass outcomes：`Hit[ResponseT](response)`、`Miss()`、`Unavailable()`、`Cached[ResponseT](response)`、`NotCached[ResponseT](response)`；並提供 `LookupOutcome[ResponseT] = Hit[ResponseT] | Miss | Unavailable` 與 `RecordOutcome[ResponseT] = Cached[ResponseT] | NotCached[ResponseT]` type aliases。 |
| `src/deterministic_response_cache/response_reuse/_cache_store.py` | 定義 internal-only `CacheStore[IdentityT, ResponseT]` `typing.Protocol`，其 `read(confirmed_identity: IdentityT) -> ResponseT | None` 與 `write(confirmed_identity: IdentityT, response: ResponseT) -> None` 是同步 port。`None` 只表示 store 已判定不存在或不可用的 entry。定義 `CacheStoreFailure(Exception)`；store adapter 必須把預期 operational read/write failure 轉譯成此 exception，而非讓 Response Reuse 猜測 backend exception。 |
| `src/deterministic_response_cache/response_reuse/protocol.py` | 定義 generic concrete class `ResponseReuseProtocol[IdentityT, ResponseT]`，constructor 接收 `CacheStore[IdentityT, ResponseT]`。`lookup(confirmed_identity: IdentityT) -> LookupOutcome[ResponseT]` 呼叫 `read` 一次：response 為 `None` 回傳 `Miss()`；response 存在回傳 `Hit(response)`；`CacheStoreFailure` 回傳 `Unavailable()`。`record(confirmed_identity: IdentityT, response: ResponseT) -> RecordOutcome[ResponseT]` 呼叫 `write` 一次：成功回傳 `Cached(response)`；`CacheStoreFailure` 回傳 `NotCached(response)`。 |

`ResponseReuseProtocol` 不檢查、序列化、比較、hash、轉型或 import identity；它只把同一個
`confirmed_identity` object 傳給 CacheStore。它不 catch `CacheStoreFailure` 以外的 exception，避免
programming error 被錯誤表述為 cache miss 或 cache failure。

## Documentation contract

五個 architecture surfaces 必須同步以下事實：

1. Identity → Response Reuse → Loaded Runtime Cache → Model Execution → Provider Adapter 繼續是
   conceptual evolution sequence，但 Identity implementation completion 不是 Response Reuse Protocol 的 gate。
2. Identity 是唯一 identity authority；Response Reuse 僅消費 opaque confirmed identity。
3. CacheStore 留在 Response Reuse BC 內；Loaded Runtime Cache、Model Execution 與 Provider Adapter
   留為獨立 future BC。
4. flow 顯示 lookup 的 Hit/Miss/Unavailable 與 record 的 Cached/NotCached outcomes；Miss downstream
   execution 僅為 future handoff，不宣稱本 topic 實作或呼叫它。
5. `scene.js` 是 interactive scene source；`index.html` 的 embedded scene 必須與它完全同步。

## Test contract

- `test_response_reuse_outcomes.py` 驗證五種 outcome 的 immutable value semantics 與 `response` payload
  preservation。
- `test_response_reuse_protocol.py` 以 typed fake CacheStore 驗證 Hit、Miss（包含 absent/invalid/expired
  store result）、Unavailable、Cached、NotCached、每個 port call 的一次性，以及 opaque identity object
  原樣交接。
- 所有新增 tests 使用 direct imports；不得用 `importlib`、`__import__` 或 `sys.modules` substitution。
