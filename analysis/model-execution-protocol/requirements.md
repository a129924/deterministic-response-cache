# model-execution-protocol — Requirements

## Mission

當外部協調者已從 Response Reuse 取得 `Miss()`，Model Execution 接收一次執行需求，透過可替換的 runtime 與 invocation 能力產生新 response，或回傳可辨識且不含 response 的失敗結果。本 topic 交付可執行的同步協調能力，不接入真實模型或 provider。

## Actor 與結果

- Actor 是處理 `Miss()` 後續流程的外部協調者；它負責先完成 Identity 與 Response Reuse 決策，並在成功後決定是否呼叫 Response Reuse `record`。
- 成功時交回一個新 response；失敗時能辨別 runtime 不可用、準備失敗或 invocation 失敗，且不宣稱有新 response。
- 透過 test doubles 可展示 runtime 已有、缺失後準備、不可用、準備失敗與 invocation 失敗。

## 業務規則

1. 已有可用 runtime 時，僅以該 runtime 執行一次 invocation。
2. 確認 runtime 缺失時，要求外部 runtime 能力準備，再執行一次 invocation。
3. runtime 不可用不等於缺失，不得觸發準備或 invocation。
4. 準備失敗不得觸發 invocation；invocation 失敗不得產生可供 `record` 的 response。
5. Model Execution 只傳遞呼叫端提供的 opaque runtime 需求與 invocation 需求，不建立或解讀 identity、runtime 保存政策與 provider 政策。

## 邊界與相依

- Identity BC 是模型及完整請求 identity 的唯一 authority；本 topic 不定義 `ModelIdentity` 到 runtime reuse key 的對應。
- Response Reuse 擁有 lookup、eligibility、record 與 CacheStore；本 topic 不呼叫它們，也不保存 response。
- Loaded Runtime Cache 擁有 runtime reuse、準備與 Runtime Store／Registry；本 topic 只透過注入的 port 請求這些能力。
- Provider Adapter 的具體 local／remote integration 是後續獨立 topic；本 topic 只透過注入的 invocation port 呼叫。
- PR #7 的 Loaded Runtime Cache 契約仍未在此 repo baseline 鎖定。本 topic 的測試不以其未確認型別、名稱或 module 為前提；實際接線待其契約穩定後另行規劃。

## 不納入

- 跨 BC 組裝、Response Reuse `Miss()` 以外的分支、真實 runtime/provider、retry、timeout、cancellation、async、並行、持久化、跨程序保證。
- identity 規則、runtime key 映射、runtime lifecycle、response reuse 或記錄政策。

## 驗收

- 上述五種結果均能以直接 import 與 test doubles 驗證，不需模型、網路或 provider。
- 每次執行至多 resolve 一次、prepare 一次、invoke 一次；準備僅發生在明確缺失時。
- 成功與失敗使用不同結果型別；失敗結果不攜帶 response。
- Python production 變更僅位於 Model Execution BC；既有 BC 與 direct-import regression 維持原樣。

## PR comment architecture status amendment

- Human 已要求處理 PR thread `PRRT_kwDOUJTij86lAh0Z`。該 thread 指出架構文件仍把 Model Execution 全部標成 future，與已交付的 provider-neutral、同步、可注入 coordination contracts 不一致。
- 本 amendment 只把下列五份架構來源同步為目前狀態：`docs/business-capability-architecture.md`、`docs/evolution-roadmap.md`、`docs/architecture/business-capability/architecture-brief.md`、`docs/architecture/business-capability/scene.js`、`docs/architecture/business-capability/index.html`。
- 五份來源必須一致表達：`ports.py`、`outcomes.py`、`protocol.py` 的 coordination contracts 已實作；Loaded Runtime Cache 的實際 wiring、retention/backend、具體 Provider Adapter、cross-BC composition，以及 Response Reuse `Miss`／execution result handoff integration 仍是 future work。
- 本 amendment 不改 Python 行為、public contract 或測試。相對 immutable predecessor PR HEAD `9a3460b6e4412384ed7e3426ebc32820a46818e6`，`src/` 與 `tests/` 的 blobs 必須不變。
- `docs/architecture/business-capability/scene.js` 是 `index.html` 中 `SCENE START (generated)` 與 `SCENE END` markers 間的 scene source；correction subject 必須維持該區段與 `scene.js` byte-for-byte 相同。
