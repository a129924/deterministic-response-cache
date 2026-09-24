# model-response-codecs Specification

## Acceptance Criteria

1. `ModelResponse[PayloadT]` 是 frozen、slotted 且只有 `value` 欄位；`StoredResponse` 是 frozen、slotted 的 `codec_id: ResponseCodecId` 與 `payload: bytes` envelope。`ResponseCodecId(StrEnum)` 恰為 `JSON_V1="json/v1"`、`DATAFRAME_V1="dataframe/v1"`。
2. `ResponseCodec[PayloadT]` 恰定義 `codec_id` property、`encode(ModelResponse[PayloadT]) -> EncodeResult`、`decode(bytes) -> DecodeResult[PayloadT]`。`EncodeResult` 恰為 `Encoded(StoredResponse) | UnsupportedPayload | CodecUnavailable | EncodeFailure | RoundTripMismatch`；`DecodeResult[PayloadT]` 恰為 `Decoded(ModelResponse[PayloadT]) | UnknownCodec | CodecUnavailable | InvalidPayload`，各 variant 為 frozen/slotted 且可依 class 判別。`JsonResponseCodec(ResponseCodec[JsonPayload])` 與 `PyArrowDataFrameCodec(ResponseCodec[pandas.DataFrame])` 明確繼承，三個 member 以 Python 3.12 `typing.override` 實作；property decorator 順序為 `@property`、`@override`。
3. selector 在 record 時僅接受 dict/list 或 pandas DataFrame，讀取只依已保存的 codec id 選 decoder；無 registry、bytes sniffing、`codecs.py`、`codecs/__init__.py`、package re-export 或動態 import 替代。
4. JSON dict/list 以 UTF-8 JSON bytes 無損往返；非字串 key、非有限值、tuple、自訂 object、任何巢狀型別變化或 scalar root 不寫入。
5. DataFrame codec 以記憶體內 Arrow IPC stream bytes 保存 pandas metadata，encode 在 Store write 前 decode 並通過 `original.equals(decoded)`；每次 hit 建立獨立 DataFrame。未通過時 `NotCached` 保留原 `ModelResponse`。
6. pandas/pyarrow 僅在 `dataframe` optional extra；純 JSON defining-module direct import 和 JSON record/lookup 在無兩者環境可用。
7. `NotCached` reason 恰區分 `UNSUPPORTED_PAYLOAD`、`CODEC_UNAVAILABLE`、`ENCODE_FAILURE`、`ROUND_TRIP_MISMATCH`、`STORE_WRITE_FAILURE`；`Unavailable` reason 恰區分 `STORE_FAILURE`、`UNKNOWN_CODEC`、`CODEC_UNAVAILABLE`、`INVALID_PAYLOAD`。entry 不存在及 eligibility 拒絕才是 `Miss`。
8. `ResponseReuseProtocol` 將完整 `ModelResponse` 交給 encoder；Store 只讀寫 `StoredResponse` 且原樣接收 opaque confirmed identity；policy 在 decode 後評估 `ModelResponse`。既有 Store/policy 未預期 exception 邊界保留。
9. 既有 direct imports、fixture/mock 與可沿用的測試行為保留；受 source break 影響的 assertions 依新契約更新。pyright strict 驗證明確繼承與 override 簽名，沒有只查 decorator 存在的測試。
10. 五個 BC 架構面與 archify dataflow 同步本能力且不宣稱其他 BC 已整合。archify HTML 通過 showcase 9/9、0 error、0 warning，visual-check 產生宣告 sidecars 並完成 desktop containment 與實際目視；不能檢視時明記 skipped。
11. 既有五個 BC 架構面在任何 Python/source/test/dependency 編輯之前完成更新與唯讀一致性確認；檢查失敗停回 Planner。確認不取代 final immutable subject 的 Tester/Independent Reviewer gate。
12. fix-3 中兩個具體 codec 的預期成功/失敗直接回傳 result 值，固定 selector 對 root 分流、可選 codec 缺失、unknown id 與壞 bytes 直接回對應 variant；protocol 將結果翻譯為第 7 項既有對外 outcome/reason。只有 `Encoded` 寫 Store、只有 `Decoded` 交 policy。預期 codec/selector failure 不以例外或 `TypeError` 表示；明確 `TypeError` 只處理 Store/policy contract violation，不新增 catch-all。原本直接拿到 `StoredResponse`/`ModelResponse` 的 codec/selector 呼叫者須取成功 variant 欄位，這是已授權 fix-3 source break。

## Behavioral Scenarios

### Scenario 1: JSON record and lookup

- **Given:** 一個 opaque confirmed identity 與 `ModelResponse(value={"items": [1, True, None]})`。
- **When:** 呼叫 record 後再 lookup。
- **Then:** codec/selector 先回 `Encoded(StoredResponse(codec_id=JSON_V1, payload=<bytes>))`，Store 保存其中 envelope；lookup 只依 id decode，經 `Decoded` 回傳原生 dict 的 `Hit(ModelResponse(...))`，policy 評估解碼後 VO，identity 原樣傳遞。

### Scenario 2: DataFrame record and isolated hits

- **Given:** 含不同 dtype、index、timezone 與缺失值的 pandas DataFrame。
- **When:** 以完整 `ModelResponse` record，並連續 lookup 兩次且修改第一次結果。
- **Then:** encode 的 Arrow IPC round trip 通過 `equals` 後才寫 Store；兩次 hit 各有獨立 DataFrame，第二次的值不受第一次修改影響。

### Scenario 3: Lossy DataFrame

- **Given:** 某 DataFrame 的 Arrow IPC decode 無法通過 `original.equals(decoded)`。
- **When:** 呼叫 record。
- **Then:** 不呼叫 Store write，回傳 `NotCached` 的 `ROUND_TRIP_MISMATCH`，其中 response 仍是原 `ModelResponse`。

### Scenario 4: Bad stored codec

- **Given:** Store read 回來的 envelope 帶未知／不合法 codec id，或 id 合法但 bytes 損壞。
- **When:** 呼叫 lookup。
- **Then:** 不猜測格式，不交 policy，也不回 `Miss`；分別回 `Unavailable(UNKNOWN_CODEC)` 或 `Unavailable(INVALID_PAYLOAD)`。

## Error / Edge Cases

- Dict/list 根節點內出現非 JSON 原生且會改變型別的資料時，回 `NotCached(UNSUPPORTED_PAYLOAD)`；Store 未寫入。已支援的值在 serializer 執行時出錯才回 `ENCODE_FAILURE`。非 dict/list/DataFrame 根節點固定 `UNSUPPORTED_PAYLOAD`。
- pandas/pyarrow 缺少時 JSON-only 路徑仍可 import/運作；DataFrame record 回 `NotCached(CODEC_UNAVAILABLE)`，既有 `DATAFRAME_V1` entry lookup 回 `Unavailable(CODEC_UNAVAILABLE)`。
- DataFrame encode/decode 的預期資料錯誤不寫入，映射 `ENCODE_FAILURE`；壞的已存 bytes 映射 `INVALID_PAYLOAD`。
- CacheStore `NotFound` 或 eligibility `ReuseDenied` 各回 `Miss`；`CacheStoreFailure` 回 `Unavailable(STORE_FAILURE)`；`CacheStoreWriteFailure` 回 `NotCached(STORE_WRITE_FAILURE)` 且保留原回應。
- malformed envelope、未知 enum 值即使被 foreign Store/typed cast 注入，也 fail closed，不能落入 `Miss` 或 bytes sniffing。
- 同一 cache instance 範圍以外沒有 migration、版本互通或持久化保證。
- fix-3 direct codec/selector tests 須分別驗證 `Encoded`、`Decoded`、`UnsupportedPayload`、`CodecUnavailable`、`EncodeFailure`、`RoundTripMismatch`、`UnknownCodec`、`InvalidPayload`；protocol tests 須逐一驗證對外舊 reasons、record 失敗無 Store write、foreign malformed envelope、Store/policy 違約與直接 import 回歸。僅對已知 JSON/Arrow/pandas 編解碼例外與 optional `ImportError` 轉為結果值；未預期程式錯誤及 Store/policy 例外仍傳播。
