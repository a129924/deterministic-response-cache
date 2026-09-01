# Observer / Dispatcher Governance Specification

## Acceptance Criteria

1. `GOAL.md` 只陳述 provider-agnostic Python response-reuse library 的長期
   mission 與成功方向，且不含 active topic、current phase、workflow status、
   dispatcher routing 或 release state。
2. `AGENTS.md` 將 Observer / Dispatcher 限為唯讀盤點、單一專責派遣、結果彙整與
   triage，並禁止它實作、改檔、git publish、PR / release、gate 推測、review-comment
   handling 及 locked-decision reinterpretation。
3. workflow 與 shared topic-plan contract 將 Planner 設為 candidate、phase、gate
   和 next-role 判定 authority；對 future / new review logs，active routing 僅接受
   planning artifact commit 後的 plan、required step tracker，以及 Plan-Reviewer 寫入
   review log 最後一筆 `"verdict": "approved"` NDJSON JSON record，且 plan 無
   self-authored approval marker。此 NDJSON 規則只 prospective 適用：existing legacy
   review logs 維持 frozen provenance，不遷移、不改寫、不重讀或因格式而失效；其 policy
   明確 defer 至另一個 future topic，本 topic 不建立該 topic 或修改其他 topic。
4. `.github/agents/**` 維持 frozen provenance，沒有 diff，且不被視為 runtime 或
   routing dependency。
5. 既有測試保留 direct import、fixture、mock 和 assertion 行為；本 topic 不修改
   `tests/**`，也不以 `importlib`、`__import__` 或 `sys.modules` 取代 direct import。
6. 本次 Human-authorized `needs-rework` 的 Plan-Creator diff 僅能位於 current topic
   plan、spec、step，以及 `plan/agent-handoff-workflow.md`（Human-only / 不可委派
   boundary wording）與 `plan/topic-plan-contract.md`（future / new review-log
   prospective-only wording及此 replan 的 special evidence topology）；前二者的 shared-contract alignment 與後三者的
   current-topic execution contract 均由 Plan-Creator 負責。不得建立 planning-review
   evidence、修改 legacy evidence logs、其他 topic 或 frozen provenance。replan 後只可由
   獨立 Plan-Reviewer 新建
   `plan/observer-dispatcher-governance/observer-dispatcher-governance.planning-review-evidence.md`，
   寫入一個完整 `Reviewer Handoff` machine-JSON record，並審核上述五個 latest replan
   artifacts 的 revisions / head。此 topic 不影響
   stable-library surfaces、README、VERSION 或 release。commit / push /
   draft PR 僅由 Implementer 在 required evidence 與既有 Human authorization 下執行；
   Reviewer 處理 PR comment routing；merge、post-merge、release、tagging 與 final
   summary 是不可委派的 Human-only action，重新授權不得移轉它們。
7. topic execution state 為 `needs-rework`，PR #1 仍是 Ready 的外部 `pr-open` state；
   Ready 只表示可供 Human review，絕不等同 independent implementation approval、merge
   approval 或已 merge。最新 replan 必須先由 independent Plan-Reviewer 在
   `plan/observer-dispatcher-governance/observer-dispatcher-governance.planning-review-evidence.md`
   唯一寫入 evidence，涵蓋 plan、spec、step、`plan/agent-handoff-workflow.md` 與
   `plan/topic-plan-contract.md` 的 latest revisions / head，並記錄 review basis、
   `verdict: approved|needs-rework`、`blocking_issues`、完整
   `copilot_feedback_triage`（`ADDRESS`、`DISCUSS`、`SKIP` arrays）與 timestamp。只有
   `approved` 才可在既有 Human authorization 下 commit replan 或繼續 same-head Tester /
   implementation-review gates；`needs-rework` 維持此 status，且任何後續 prospective
   replan 都必須由 Human 明示授權。frozen legacy `review-log.md` 不得作為本 current
   replan 的 routing authority。完成 approved replan 後的 PR 新 head 使舊 head evidence
   不再符合 same-head gate。Tester 必須先在
   `plan/observer-dispatcher-governance/observer-dispatcher-governance.tester-evidence.md`
   對新的同一 PR head 寫入含 `pr_number`、`head_sha`、每項 check result 與
   `verdict: passing` 的 evidence。其後 Reviewer 才能在
   `plan/observer-dispatcher-governance/observer-dispatcher-governance.implementation-review-log.md`
   reference 此 evidence，並獨立寫入 `approved|needs-rework` verdict；只有這個 verdict
   存在後才可處理已 addressed threads。新 head 的兩份 evidence 在本 replan 時均為
   pending，不得宣稱新的 Tester 或 Reviewer completion。

## Behavioral Scenarios

### Scenario 1: 唯一有效 candidate 可派遣

- **Given**: 獨立 Implementer 已建立 planning artifact commit；Planner 找到唯一
  future / new candidate，其 plan、required step tracker 與 review log 都可讀，且 review
  log 最後一筆 NDJSON record 是 Plan-Reviewer 寫入的 `"verdict": "approved"`。
- **When**: Observer 取得 Planner 的 phase / gate / next-role 判定。
- **Then**: Observer 只派遣該單一角色，彙整 bounded result，並依結果回報可前進、
  `needs-rework`、`blocked` 或 `human-check`。

### Scenario 2: candidate 不足或衝突

- **Given**: 沒有 candidate、存在多個 candidate、plan 與 step 指向不同 topic，或同
  topic 的 state / scope 相互矛盾。
- **When**: Planner 判定 routing readiness。
- **Then**: 無 candidate 為 `blocked`；多 candidate 或 topic 不一致為 `human-check`；
  state / scope 矛盾為 `blocked`，除非 Planner 明定 Plan-Creator 可進行 bounded repair。

### Scenario 3: import preservation

- **Given**: `tests/test_package_import.py` 已以直接 import 驗證 package import。
- **When**: Implementer 完成本 topic bounded change。
- **Then**: 測試檔零 diff，且沒有 `importlib`、`__import__` 或 `sys.modules` 被用來
  取代該 direct-import regression 行為。

### Scenario 4: draft PR 後停止

- **Given**: independent review 與 Planner contract alignment 均通過，且使用者已
  明示授權 commit、push 和開啟 draft PR。
- **When**: draft PR 已建立。
- **Then**: topic 停在 human review boundary；沒有 actor 自行 merge、release、
  post-merge sync 或宣告 human check 完成。

### Scenario 5: 未提交 baseline 不可開始

- **Given**: Plan-Creator 已寫入 plan、spec、step 或 shared planning contract，但
  尚未由獨立 Implementer 建立 planning artifact commit。
- **When**: Planner 準備進行 execution preflight。
- **Then**: topic 尚未為 `planned` repo-visible contract；不得進入 implementation。
  planning artifact commit 不表示 implementation approval；仍須 Plan-Reviewer
  之後寫入 latest `approved` review-log record。

### Scenario 6: Ready PR 的 rework-first evidence routing

- **Given**: PR #1 已開啟且為 Ready，且 blocking finding 已將 topic execution state
  route 至 `needs-rework`；舊 head 的 Tester / Reviewer artifacts 都是 frozen provenance。
- **When**: latest replan 等待 commit，或 Reviewer 準備處理已 addressed threads。
- **Then**: PR 仍維持 `pr-open` / Ready，但 independent Plan-Reviewer 先唯一寫入涵蓋
  latest plan、spec、step、`plan/agent-handoff-workflow.md` 與
  `plan/topic-plan-contract.md` revisions / head 的 planning-review evidence，並給出
  `approved|needs-rework`、review basis、blocking issues、完整
  `copilot_feedback_triage` 與 timestamp。只有 `approved`
  才可由 Implementer 在既有 Human authorization 下 commit / push replan 新 head；若為
  `needs-rework`，topic 保持 `needs-rework`，僅可由 Human 再授權 prospective bounded
  replan。新 head 後，Tester 對新 head 寫入 `verdict: passing` evidence，Reviewer 再獨立寫入
  reference 該 evidence 的 `approved|needs-rework` verdict。前述 gate 未滿足時不得處理
  threads，也不得把 Ready 當成 merge approval。

## Error / Edge Cases

- 缺少涵蓋 latest replan（plan、spec、step、`plan/agent-handoff-workflow.md` 與
  `plan/topic-plan-contract.md`）revision 的 independent approved planning-review evidence 時，
  不得 commit replan 或繼續 same-head Tester / implementation-review gate；不得由 branch、
  chat、summary、`GOAL.md` 或 frozen legacy review-log 補推；維持 `needs-rework`。
- 若新增的測試需求本身是 import 行為，只有 approved topic 明定時才可新增專用測試；
  原有 regression test 仍必須保持 direct import。
- 如果 implementation 需要 `Written` / `Modify` 以外檔案，先停止，由 Planner 決定
  是否需 bounded plan repair；不得自行擴張。
- existing legacy review log 不得因 future / new NDJSON requirement 而遷移、改寫、
  讀取、關閉或判為無效；policy、migration、reader 與 compatibility 只能由 separate
  future topic 定義，本 topic 不得修改其他 topic。
- `step-creator` 的角色模型衝突一律 defer 至新 topic
  `step-creator-role-model-alignment`；不可用本 topic 的 evidence repair 重新開啟。
