# model-response-codecs — Technical Specification

## Authority

本 spec 是同 topic plan 的 execution-facing source of truth；`requirements.md` 是 business-intent guardrail。它記錄 Human 已確認的局部增強，不引入第二 Mission。未列實作路徑或架構衝突需先回 Planner，不由 Implementer 擴張。

## 契約

- 在 `response_reuse/model_response.py` 定義 frozen、slotted `ModelResponse[PayloadT]`，唯一欄位 `value: PayloadT`；直接持有 dict、list、`pandas.DataFrame`。
- 在 `response_reuse/stored_response.py` 定義 frozen、slotted `StoredResponse(codec_id: ResponseCodecId, payload: bytes)` 及只含 `JSON_V1 = "json/v1"`、`DATAFRAME_V1 = "dataframe/v1"` 的 `ResponseCodecId(StrEnum)`。讀取時仍須 runtime fail closed 處理不合法／未知 id；不依 bytes 猜格式。
- 在 `response_reuse/codecs/contract.py` 定義 `ResponseCodec[PayloadT](Protocol)`，且共同介面恰為唯讀 `codec_id: ResponseCodecId` property、`encode(response: ModelResponse[PayloadT]) -> StoredResponse`、`decode(payload: bytes) -> ModelResponse[PayloadT]`。
- `codecs/json_response.py` 定義 `JsonPayload = dict[str, object] | list[object]` 的型別意圖，以及明確繼承 `ResponseCodec[JsonPayload]` 的 `JsonResponseCodec`。它只接受可無損 JSON 往返的 dict/list 樹；拒絕非字串 key、非有限浮點、tuple、自訂物件或巢狀型別變化。`encode` 收完整 `ModelResponse`；使用 UTF-8 JSON bytes，decode 拒絕根節點不是 dict/list 的內容。
- `codecs/pyarrow_dataframe.py` 定義明確繼承 `ResponseCodec[pandas.DataFrame]` 的 `PyArrowDataFrameCodec`。以記憶體內 Arrow IPC stream 與 pandas metadata 編／解碼；`encode` 接受完整 `ModelResponse`，編碼後立即 decode，只有 `response.value.equals(decoded.value)` 成立才回傳 `StoredResponse`。每次 decode 建新 DataFrame。pandas 與 pyarrow 僅在此具體 codec 的直接使用路徑載入。
- 兩個具體類別的 `codec_id`、`encode`、`decode` 均以 Python 3.12 `typing.override` 標示。property decorator 順序固定為 `@property`、`@override`、`def codec_id`；方法以 `@override` 緊鄰 `def`。pyright strict 驗證明確繼承及簽名，不另寫只查 decorator 存在的測試。
- `codecs/selector.py` 固定分流，無動態 registry。record 先辨識 dict/list 並呼叫 JSON codec；其他值只有在 DataFrame 可選依賴可用且 `isinstance(value, pandas.DataFrame)` 時呼叫 DataFrame codec；其餘 unsupported。lookup 只依保存的 codec id 以 exhaustive `match/case` 選 decoder。JSON-only import 與路徑不急切載入 pandas／pyarrow；DataFrame 相關 import 保留為分支內 direct import。沒有 `codecs.py`、`codecs/__init__.py`、套件層 re-export、`importlib`、`__import__` 或 `sys.modules` 替換。
- `ResponseReuseProtocol` 同步接收 `CacheStore[IdentityT, StoredResponse]` 與 `ReuseEligibilityPolicy[ModelResponse[PayloadT]]`，record 只接受 `ModelResponse[PayloadT]`，lookup 回傳 `ModelResponse` 封裝的 hit。selector/codec 的預期失敗轉為 outcome reason，CacheStore 值通道維持原映射，未預期 Store／policy exception 依現有邊界傳播。
- `NotCached` reason 的封閉集合恰為 `UNSUPPORTED_PAYLOAD`、`CODEC_UNAVAILABLE`、`ENCODE_FAILURE`、`ROUND_TRIP_MISMATCH`、`STORE_WRITE_FAILURE`；`Unavailable` reason 的封閉集合恰為 `STORE_FAILURE`、`UNKNOWN_CODEC`、`CODEC_UNAVAILABLE`、`INVALID_PAYLOAD`。以 enum 表示，原 `ModelResponse` 在 `Cached`／`NotCached` 保留。entry 缺失與 policy 拒絕才回 `Miss`。

## 依賴與相容性

- `pyproject.toml` 新增單一可選 extra，包含 pandas 與 pyarrow；`uv.lock` 同步。基礎安裝不引入兩者。Python 版本維持 3.12+。
- 此變更接受 source break，不提供 generic response 直存相容層；不更動 CacheStore port 或 in-memory backend 的 generic 保存實作。
- 無跨版本 bytes 相容與 schema migration 承諾；`DATAFRAME_V1` 在本次同 cache instance 的 pandas/pyarrow 版本範圍內以 equals 驗證可保留語意，失真時不寫入。

## 驗證與產物

- Implementer 進入 implementation 後，第一步只修改五個既有 BC 架構面，使 bytes 保存/解碼描述與已鎖定的 BC 邊界一致；在任何 Python/source/test/dependency 編輯前，以唯讀檢查核對 `docs/` 與 BC 圖的責任／演進順序、`scene.js` 與 `index.html` 的 generated block mirror，並確認沒有引入 Identity／Model Execution／Loaded Runtime Cache／Provider Adapter 的責任。此為本 subject 工作內的本地架構一致性停點，不宣稱新的 workflow approval；檢查失敗停下回 Planner。docs 與後續 Python/archify 變更最後才一次提交為同一 immutable implementation subject，接續單一 Tester／Independent Reviewer sequence。
- 新增 codec unit 與 protocol integration tests，修改既有 outcome/protocol/in-memory store tests 中受 source break 影響的斷言。JSON-only import 應以隔離環境或等價受控測試驗證無 pandas/pyarrow 時可用；保留 direct imports。
- 五個既有 BC 文件／圖面同步更新；archify `dataflow` JSON + HTML 及 `visual-check` 的一個 JSON receipt、一個 HTML contact sheet、四張 PNG 均使用 topic plan 的 exact paths。必須 showcase 9/9、0 error、0 warning，並實際檢視圖面；若瀏覽器不可用，誠實記錄 skipped，不聲稱 passed。
- 執行 `uv run --extra dataframe pytest`、`uv run --extra dataframe pyright`、`uv run --extra dataframe ruff check .` 及所需 archify 命令；另以乾淨 base-install 環境驗證 JSON-only import/操作。Tester's evidence 記實際 command/exit code；independent Reviewer 只消費同 subject 的 committed passing evidence。
