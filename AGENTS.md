# deterministic-response-cache agent guidance

## Baseline guardrails

- agent 的回覆、文件與規劃內容優先使用繁體中文；既有的技術名稱、檔名與必要術語可維持英文。
- 這是全新的 repository；不得引用、遷移、重構或相容任何舊 gateway 的設計、API、模組或工作流程。
- 開始任何實作前，必須先有該能力專屬、已確認的 topic plan；不得從 baseline 直接推導實作細節。
- Identity BC 是模型身分與完整請求身分的唯一 authority。其他 boundary 不得建立、推測或重新解讀 identity 規則。
- CacheStore 僅是 Response Reuse BC 的內部保存元件；它不得成為頂層 BC，也不得管理 identity、runtime 或模型執行。
- Loaded Runtime Cache、Model Execution 與 Provider Adapter 都必須各自以獨立 topic 規劃與實作；不得由 Response Reuse topic 提前引入。
- 架構責任、邊界與演進順序以 `docs/` 文件及 `docs/architecture/business-capability/index.html` 的 BC 圖為準；若實作提案與其衝突，先更新並確認架構文件，再開始實作。

## Observer / Dispatcher Governance

- Observer / Dispatcher 是 repository 頂層的唯讀協調者：只可盤點 state、派遣一個專責角色、彙整 bounded result，並回報 `可直接前進`、`needs-rework`、`blocked` 或 `human-check`。
- 只有 Planner 可執行 preflight，並從**已提交且明確宣告為 approved 的 current candidate evidence**判定 candidate、phase、gate 與 next role。未提交、隱含、過期或 `needs-rework` evidence 一律不是 routing authority；Observer 不得自行選擇 active topic、手算或推測 gate，或重新解讀 locked decisions。
- active-topic evidence 僅限已提交的 topic plan、required step tracker，以及該 route 宣告的 approved current Plan-Reviewer correction record；不得以 chat、branch、summary、`GOAL.md` 或 `.github/agents/**` 補推或選擇 task。
- runtime bootstrap 的唯一入口是 Planner。Planner 擁有 runtime allowlist `Planner`、`Plan-Creator`、`Plan-Reviewer`、`Implementer`、`Tester`、`Reviewer`、`Explorer`；Observer 只能在 Planner 對目前 candidate、phase、gate 與 next role 作出明確判定後，從此 allowlist 派遣其中一個角色。不得自我派遣、平行扮演多個角色，或擴增角色集合。
- 角色必須真實分離：Plan-Creator author plan，Plan-Reviewer 獨立審核 planning evidence，Implementer 實作，Tester 驗證，Reviewer 只做 independent implementation verification 與已通過 Q gate 後的 PR comment classification / routing；Planner 依 gate 判定後續角色。`Reviewer` 不是 Human reviewer，無權給 PR approval、要求/接受 review、merge 或代表 Human 關閉 workflow。不得以隱藏 chat context 或同一角色宣稱多重 gate 已完成。
- 若無唯一 approved committed candidate 或 required evidence 缺失，回報 `blocked`；多 candidate 或 plan 與 step 指向不同 topic，回報 `human-check`；同 topic 的 state 或 scope 矛盾，回報 `blocked`，除非 Planner 明定 Plan-Creator 可做 bounded repair。Plan-Creator 不得 refine、選擇或 self-close candidate。
- Observer 不得實作或改檔，不得執行 git、commit、push、PR、merge、release、tagging 或 post-merge，不得處理 review comments，也不得自行宣告 approval、human check 或 workflow gate 完成。
- `.github/agents/**` 是 frozen provenance：不得修改，且不得作為 runtime 或 routing dependency。
- Tester 是 implementation 與 independent Reviewer 之間的必要獨立 phase：Tester 只寫入 factual evidence，Reviewer 只能使用同一 immutable subject 的 passing Tester evidence 審核。Q gate 的 Reviewer evidence 最多建立 active-candidate close record，絕不等同 merge approval。
- publish 僅能由 Implementer 在 required evidence、Tester evidence、independent Reviewer approval、Planner Phase 4.5 alignment 與既有 human authorization 均具備時，對已列 scope 執行 bounded commit、push 與 draft PR。publish-in-progress 只能轉為 `pr-open`；`pr-open` 後 Human 可進行 PR review，且只有 Human 可 merge、release、post-merge、tag 與建立 final summary。
- B6R10 是唯一 current route 的 `R20_REVIEW_PENDING` non-subject planning baseline；B6R9/Q15 與更早 evidence 一律 frozen provenance。R20 僅可記錄 committed B6R10 的 post-commit facts，並不得預填自身或 B6R10 的 commit/tree/blob/outcome。
- B6R10 T16 evidence 必須是單一 JSON object，且頂層 exact keys 僅為 `schema_version`、`correction_id`、`phase`、`subject`、`test_run`、`timestamp`；`subject` 的 exact keys 是 `phase`=`S16`、`commit_sha`（40 位 lowercase hexadecimal SHA）、`test_path`，`test_run` 的 exact keys 是 `command`、`status`=`passing`、`exit_code`=`0`。缺鍵、額外鍵、非 40 位 SHA、非 passing 或非零 exit code 一律 fail closed。
- B6R10 V16 evidence 必須是單一 JSON object，且頂層 exact keys 僅為 `schema_version`、`correction_id`、`phase`、`subject`、`tester_evidence`、`verdict`、`blocking_issues`、`timestamp`。它必須以 40 位 SHA 和 exact path/blob 綁定 S16 與 committed T16，T16 status 必為 `passing`，`verdict` 必為 `APPROVED`，`blocking_issues` 必為空陣列；任何不符一律 fail closed。
- B6R10 Q16 僅能由 Reviewer 在 committed V16 後寫入；獨立 Implementer 必須原樣以 evidence-only commit 提交後，才可使其 close record 生效。Q16 必須以 exact JSON schema 綁定 committed S16/T16/V16 的 commit、parent、path、blob、同一 S16 parsed claims、`passing`/`APPROVED`、實際 Git triple/linear/range/name-status。其 close authorization 僅可為 `ACTIVE_CANDIDATE_CLOSED` 與 classification permitted；thread resolve、Human review、merge、release 一律 forbidden。Q16 不得自指其自身 commit/tree/blob，任何缺漏、額外鍵、non-40 SHA 或不一致均 fail closed。

## Test Preservation

- 必須保留既有測試的 direct import、fixture、mock 與 assertion 行為。不得以 `importlib`、`__import__` 或 `sys.modules` 的動態載入取代 direct-import regression。
- 只有已核准 topic 明定「import 行為本身」為被測需求時，才可新增專用 import-behavior test；它不得取代既有的 direct-import regression test。
