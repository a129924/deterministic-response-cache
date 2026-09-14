# Response Reuse Protocol — Requirements

## Intent

建立可獨立交付的 Response Reuse BC Protocol。它只接受 Identity BC 已確認的 opaque
`confirmed_identity`，安全重用既有 response，並保有把新 response 寫回其內部 CacheStore 的責任。

## Business and boundary requirements

1. Identity 仍是模型身分與完整 request identity 的唯一 authority；本 topic 不需等待 Identity
   implementation 完成，但不得建立、驗證、推測、hash 或重新解讀 identity。
2. Response Reuse 的 `lookup` 必須顯式區分 `Hit(response)`、`Miss` 與 `Unavailable`：
   可用 entry 是 Hit；不存在、失效或過期 entry 是 Miss；CacheStore 的 read failure 絕不可降級為 Miss。
3. Response Reuse 的 `record` 必須保留 caller 已有的 response：寫入成功回傳 cached outcome；
   寫入失敗回傳含原 response 的 not-cached outcome，且不丟棄或重算 response。
4. CacheStore 是 Response Reuse 的內部 port，不是頂層 BC，且不管理 identity、runtime 或模型執行。
5. miss 只表達「本 BC 沒有可安全重用的 response」。本 topic 不會載入 runtime、執行模型、呼叫
   provider 或自行推進 downstream pipeline。
6. 文件與 interactive BC flow 必須呈現：confirmed identity → lookup → Hit 直接回傳；Miss 交給未來
   downstream path 並在新 response 產生後回交 record；Unavailable 停在 Response Reuse boundary；
   record 的 cached/not-cached 結果均保留 response。

## Delivery requirements

- 新增 Response Reuse Protocol、outcome types、內部 CacheStore port 與 unit tests。
- 更新五個已列 architecture surfaces，移除「Identity implementation completion 是 Response Reuse gate」的
  敘述，保留 Identity authority 與其他 future BC 邊界。
- 保留 `src/deterministic_response_cache/response_reuse/.gitkeep`；不新增 child `__init__.py` 或 root export。
- 不修改 README、版本、root package initializer、project configuration 或既有 package-import regression。
