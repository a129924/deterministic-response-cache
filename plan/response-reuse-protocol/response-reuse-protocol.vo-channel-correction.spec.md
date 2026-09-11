# Response Reuse VO Channel Correction Specification

## Acceptance Criteria

1. `_cache_store.py` declares `NotFound`、`CacheStoreFailure`、`TokenWritten`、`CacheStoreWriteFailure` as frozen,
   slotted VO types; none is an `Exception`, and none accepts or represents `None`.
2. `CacheStore.read` declares `ResponseT | NotFound | CacheStoreFailure`; `CacheStore.write` declares
   `TokenWritten | CacheStoreWriteFailure`. No port signature uses `None` as a channel.
3. `ResponseReuseProtocol.lookup` uses `match`／`case` to map response to `Hit`, `NotFound` to `Miss`, and
   `CacheStoreFailure` to `Unavailable`; `record` maps `TokenWritten` to `Cached(original_response)` and
   `CacheStoreWriteFailure` to `NotCached(original_response)`.
4. `ResponseT` is type-layer opaque: every non-`None` nonchannel read value is a legal response and becomes `Hit`.
   Read `None` and every foreign write return object cause `TypeError`; exceptions raised by a store method propagate
   unchanged. No runtime response validator is added.
5. The four permitted implementation paths are the entire correction implementation subject; direct-import test
   behavior and all unlisted repository paths remain unchanged.

## Behavioral Scenarios

### Read channel mapping

- Given a store returns the exact response object, `lookup` returns `Hit` retaining that object.
- Given a store returns `NotFound`, `lookup` returns `Miss()`.
- Given a store returns `CacheStoreFailure`, `lookup` returns `Unavailable()`.
- Given a store returns `None`, `lookup` raises `TypeError` after one read call.
- Given a store returns any opaque non-`None` nonchannel object, `lookup` treats it as legal `ResponseT` and returns
  `Hit` retaining that object.

### Write channel mapping

- Given a store returns `TokenWritten`, `record` returns `Cached` retaining the caller's original response object.
- Given a store returns `CacheStoreWriteFailure`, `record` returns `NotCached` retaining that same response object.
- Given a store returns `None` or an unrelated object, `record` raises `TypeError` after one write call.

### Boundary behavior

- Given a store method raises any exception, Protocol propagates it; it does not convert exception transport into a
  value channel or an outcome.
- Given opaque identity and response objects, Protocol forwards them unchanged and does not inspect identity or
  invoke runtime, execution, or provider behavior.

## Documentation Criterion

`docs/business-capability-architecture.md` replaces only the old `None`/exception cache-port explanation with the
locked value-object channel explanation. It continues to state that Identity is the sole authority and CacheStore is
internal to Response Reuse.
