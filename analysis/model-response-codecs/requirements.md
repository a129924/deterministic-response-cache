# model-response-codecs — Requirements

## Mission

嵌入本 library 的應用持有 Identity BC 已確認、對 Response Reuse 而言 opaque 的 identity 時，能保存並安全重用 dict、list 或 `pandas.DataFrame` 模型回應。Response Reuse 保存帶有明確 codec id 的 bytes；lookup 只依保存 id 還原原生型別。這是單一 Response Reuse BC Mission。

## 使用者可觀察結果

- JSON dict/list 與 DataFrame 可完成 record → store → lookup，取得原生型別的 `ModelResponse.value`。
- 每個 DataFrame hit 均為獨立可修改實體，前一次修改不影響下一次 hit。
- DataFrame 寫入只在 Arrow IPC round trip 滿足 `original.equals(decoded)` 時發生；未通過時原回應仍可用。
- unsupported payload、無法 encode、缺少可選依賴及 Store write failure 產生帶 reason 的 `NotCached`；未知 codec、損壞 bytes、缺少 decoder 及 Store read failure 產生帶 reason 的 `Unavailable`，皆不得誤稱為 `Miss`。
- 既有 eligibility policy 在解碼後評估 `ModelResponse`；entry 缺失或 policy 拒絕時才是 `Miss`。

## 範圍與限制

- 本次接受既有 generic `ResponseT` 直存 API 的 source break；新契約是 `ModelResponse.value`、`StoredResponse(codec_id, payload)` 與固定 JSON/DataFrame codec。
- pandas 與 pyarrow 是可選 extra；純 JSON import 與操作不要求安裝或載入兩者。
- 只承諾同一 cache instance 內的保存與還原，不承諾跨重啟、跨程序或跨版本 bytes 相容性。
- Identity BC 獨占 identity 規則；CacheStore 仍為 Response Reuse 內部元件。Loaded Runtime Cache、Model Execution、Provider Adapter、跨 BC handoff、持久化 backend、其他 payload codec 均不在此 Mission。
- 交付同步更新的 BC 文字與圖，以及以 archify 製作的繁體中文 dataflow 圖與視覺驗證證據。
- 若本提案與既有 BC 圖文衝突，須在同一 feature worktree 先更新既有五個 BC 架構面並完成唯讀一致性確認，才開始 Python 變更；最後仍以同一 immutable implementation subject 交 Tester 與 Independent Reviewer。

## 驗收

以 direct-import tests、pytest、pyright strict、ruff、archify showcase validation、visual-check 與實際檢視圖面驗證。需保留可沿用的既有 fixture、mock、direct import 與 assertion 行為；僅因本次已授權 source break 而失效的行為斷言可更新。
