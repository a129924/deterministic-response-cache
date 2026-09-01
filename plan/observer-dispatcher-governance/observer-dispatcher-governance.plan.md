# Observer / Dispatcher Governance

## Goal / Outcome

- 建立 repository mission 型 `GOAL.md`，並將 `AGENTS.md`、repo workflow
  與 shared topic-plan contract 對齊為可審計的 Observer / Dispatcher
  governance。
- 完成後，Observer 只讀取狀態、依已核准 topic plan 與 step tracker
  派遣單一專責角色、彙整結果並於 human boundary 停止；它不取得任何
  實作、git publish、PR、release 或自我核准權限。

> **Analysis-layer warning:** `analysis/observer-dispatcher-governance/requirements.md`
> 與 `analysis/observer-dispatcher-governance/technical-spec.md` 均不存在。
> 本 plan 僅以已確認的 human topic specification、`AGENTS.md` 與 `docs/`
> 架構輸入 author；不得將此 warning 當作重新開啟 architecture、path 或
> contract decision 的授權。

## Scope

- **In scope**:
  - `GOAL.md` 的 repository 長期 mission 與非-routing authority boundary。
  - `AGENTS.md` 的 Observer / Dispatcher governance、角色分離、human
    boundary 與既有測試 direct-import preservation rule。
  - `plan/agent-handoff-workflow.md` 與 `plan/topic-plan-contract.md` 的
    ownership、candidate resolution 與 approved-evidence 對齊。
  - 本 topic 的 plan、spec、step、frozen planning review-log、此次 replan 的 exact
    planning-review evidence、tester-evidence、implementation-review-log 與 human-close
    summary handoff artifacts。
  - 本次 Human-authorized `needs-rework` bounded replan 的精確 Plan-Creator 路徑集：
    `plan/agent-handoff-workflow.md`（將 merge、post-merge、release、tagging 與 final
    summary 鎖為不可委派的 Human-only action）、
    `plan/topic-plan-contract.md`（將 future / new review-log NDJSON 規則鎖為
    prospective-only，並保留 legacy logs 為 frozen provenance），以及本 topic 的
    `.plan.md`、`.spec.md`、`.step.md`。這五個路徑同屬已存在 diff 的 bounded repair；
    前二者由 Plan-Creator 依 shared-contract alignment 負責，後三者由 Plan-Creator
    依 current-topic execution contract 負責。

- **Out of scope**:
  - `src/**`、`tests/**`、public API、Business Capability、Identity、Response
    Reuse、CacheStore、runtime、model execution、provider adapter 與 architecture
    docs。
  - `.github/agents/**`、README、VERSION、CI、依賴、release metadata，及任何
    未在本 plan `Artifact Paths` 列出的檔案。

## Locked Decisions

- `GOAL.md` 只描述 repository 的最終 mission 與成功方向；它不是 workflow、
  active topic、current phase、task routing 或 release state 的 authority。
- active-topic routing 的唯一可接受輸入為 Planner 判定的 candidate，其中必須有
  planning artifact commit、required step tracker 與 Plan-Reviewer 寫入的 latest
  approved review-log JSON record；chat、branch、summary、`GOAL.md` 與
  `.github/agents/**` 均不得用於推測或選擇 task。
- Observer 是 repo 頂層 readonly dispatcher：只盤點、單一派遣、彙整與 triage
  （`可直接前進`、`needs-rework`、`blocked`、`human-check`）；不得實作、改檔、
  git/PR/release、手算 gate、處理 review comments 或重新解讀 locked decisions。
- Planner 是唯一可判定 candidate、phase、gate 與 next role 的角色；若無
  candidate 則 `blocked`，多 candidate 或 plan/step 指向不同 topic 則
  `human-check`，同 topic 狀態或 scope 矛盾則 `blocked`，除非 Planner 指定
  Plan-Creator 可做 bounded repair。
- planning approval evidence 不得由 topic plan 自我宣稱。對本 shared contract 生效後
  新建的 future review log，最後一筆完整 reviewer-handoff NDJSON JSON record 的
  `"verdict": "approved"` 才是 planning evidence；它由 Plan-Reviewer 寫入，並由
  獨立 Implementer 在 Planner preflight 前以 review-log-only evidence commit 固化。
  此規則只 prospective 適用於 future / new logs；既有 review logs 是 frozen
  provenance，不能被遷移、改寫、重讀或僅因格式被判定失效。其分類、reader 與長期
  policy 明確 defer 至另一個 future policy topic，不在本 topic 建立、命名或執行。
  frozen `.github/agents/**` 亦僅為 provenance，不可修改，也不可作 runtime / routing
  dependency。
- 此次 Human-authorized `needs-rework` replan 是不遷移 legacy log 的狹義例外：唯一
  routing evidence 為 exact path
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.planning-review-evidence.md`。
  它只由 independent Plan-Reviewer 在 latest replan 後寫入一個完整 shared
  `Reviewer Handoff` JSON object，並覆蓋五個 declared replan artifacts 的 latest
  revisions / head；它不改變 generic future NDJSON rule，也不給其他 topic 建立第二種
  evidence 的先例。
- 保留所有既有測試的 direct import、fixture、mock 與 assertion 行為；不得以
  `importlib`、`__import__` 或 `sys.modules` 動態載入取代。只有 approved topic
  明定 import 行為本身為被測需求時，才可新增專用測試，且不得取代 regression test。
- 本 topic 為 review-ready-only、無 stable-library surface；不修改 README 或
  VERSION，且不執行 release 或 tagging。

## Boundaries / Exclusions

- Identity BC 仍是模型身分與完整請求身分唯一 authority；本 governance topic
  不得創建、推測或重解其規則。
- CacheStore 仍只是 Response Reuse BC 內部保存元件；不得將它升為頂層 BC 或使其
  管理 identity、runtime 或執行。
- Loaded Runtime Cache、Model Execution 與 Provider Adapter 維持各自獨立的未來
  topic；不得由本 topic 提前引入。
- 計畫 author、實作、獨立 review 及 human git boundary 必須真實分離；不可藉由
  hidden chat context 或同一角色宣稱多重 gate 已完成。
- 若執行需要未列 path、改變 locked contract 或觸及 frozen provenance，必須停止並
  回交 Planner / human，而不是擴張 scope。
- `step-creator` 的角色模型衝突不屬本 topic 的 governance implementation 或本次
  evidence repair 範圍；明確 defer 至新 topic
  `step-creator-role-model-alignment`，不得藉此重開既有 topic。
- legacy review-log NDJSON finding 只是一項 prospective-policy defer：不得在本 topic
  遷移 legacy logs、建立 reader / compatibility layer、改動其他 topic 或以此重開既有
  evidence。完整 policy 僅能由另一個 future topic 決定。

## Status / Allowed Transitions

- **Current**: `needs-rework`。PR #1 仍是外部可見的 **Ready** `pr-open`，但 topic
  execution state 已因 blocking review finding 回到 `needs-rework`。Ready 只表示 PR
  可供 Human review，絕不等同 independent implementation approval、merge approval 或
  已 merge。
- **Bounded historical recovery**: preflight 曾在 implementation 前完成，但 step
  tracker 漏記該事實。Planner-authorized backfill 以 commit
  `490066f6753271181d289abdd593f119bd9ef48c`
  (`docs(governance): confirm observer plan preflight`) 為 evidence，將 parent plan /
  step 同步至 `creator-in-progress`。這只是 progression truth correction：不重跑或要求
  重跑 planning review、review-log evidence 或 preflight，不重開任何 locked decision，
  亦不宣稱 implementation 或 testing 已完成。
- **Current corrective gate**: 在任何人 commit 最新 replan 前，獨立 Plan-Reviewer
  必須先寫入 exact
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.planning-review-evidence.md`
  的 single machine-JSON record，且其 verdict 為 `approved`。
  evidence 必須涵蓋最新 replan 的 plan、spec、step、
  `plan/agent-handoff-workflow.md` 與 `plan/topic-plan-contract.md` revisions / head；
  frozen legacy `review-log.md` 不具此 current-replan routing authority。若 verdict 為
  `needs-rework`，topic 保持 `needs-rework`，且後續 prospective bounded replan 只能在
  Human 明示授權下由 Plan-Creator 修訂；不得 commit、push 或開始 Tester / Reviewer 的
  same-head gate。只有此 evidence 通過後，Implementer 才可在既有 Human authorization
  下 commit / push replan，令 PR #1 產生新的 head。既有 tester-evidence 與
  implementation-review-log 都是舊 head 的 frozen provenance，不能滿足新 head 的
  same-head gate。新 head 上，Tester 必須先寫入 passing evidence；其後 Reviewer 必須
  reference 該 evidence，並獨立寫入 `approved` 或 `needs-rework` verdict。這些 future
  actions 均為 pending；不得把舊 evidence、口頭說法、step 或 PR Ready state 當成完成。
- **Thread gate**: 只有上述新 head 的 Tester passing evidence 與 Reviewer independent
  verdict 都存在且對同一 PR head 時，Reviewer 才可處理 PR #1 的已 addressed threads；
  在此之前 reviewer-comments replan 維持 pending。此 gate 不授權任何 actor merge、
  resolve human approval 或把 Ready 重解為 approval。
- **Recorded nonconformance**: PR #1 已存在的 Ready state 是 current external fact，
  不補正為不存在，也不治癒 rework requirement。舊 head evidence 僅保留為 frozen
  provenance；本 bounded replan 不修改它們，並要求 rework 後以新 same-head evidence
  重新進 gate。
- **Execution model**: topic 在 planning review、review-log evidence commit 與
  Planner preflight 期間維持 `planned`。preflight 證實 required evidence 已
  approved 後進入 `creator-in-progress`，由 Implementer 完成 bounded change，並交由
  Tester 驗證；implementation 與 testing 都必須有真實完成證據後，才可進入
  `review-ready`、獨立 Reviewer review 與 Planner Phase 4.5 判定。使用者已明示 git
  publish 授權時，Implementer 才可 commit、push 並開 draft PR；之後停止於 human review
  boundary。本 topic 不進入 release。
- **Allowed transitions**:
  - `planned` -> `creator-in-progress`
  - `creator-in-progress` -> `review-ready`
  - `review-ready` -> `reviewer-in-progress`
  - `reviewer-in-progress` -> `approved`
  - `reviewer-in-progress` -> `needs-rework`
  - `needs-rework` -> `creator-in-progress`
  - `approved` -> `creator-in-progress`
  - `approved` -> `publish-in-progress`
  - `publish-in-progress` -> `pr-open`
  - `pr-open` -> `needs-rework`
  - `pr-open` -> `merged`
  - `merged` -> terminal

Routing notes:

- planning evidence 的 `approved` 不改變 topic execution status；`approved` status
  只屬 independent implementation Reviewer verdict。
- Phase 4.5 Planner contract alignment is required after each independent
  implementation `approved` verdict; it may return the topic to
  `creator-in-progress` on contract drift, otherwise it permits
  `publish-in-progress`.
- `pr-open` means draft PR 已開啟且等待 human review；Reviewer 處理 comments 的
  classification / routing；Observer 與 Implementer 不得自行處理 comments、merge 或
  post-merge work。
- PR #1 的 Ready state 保持不變；本 replan 只補足 evidence / review routing，並不
  回填、模擬或重新宣告先前 testing、review 或 Phase 4.5 已完成。

## Artifact Paths

| Artifact | Path | Owner | Role |
| --- | --- | --- | --- |
| Repository mission | `GOAL.md` | Implementer | Project long-term mission only; never active-task or phase authority |
| Governance | `AGENTS.md` | Implementer | Repo-level Observer / Dispatcher and test-preservation rules |
| Repo workflow | `plan/agent-handoff-workflow.md` | Plan-Creator | Phase, ownership, stop-point and routing alignment |
| Shared topic-plan contract | `plan/topic-plan-contract.md` | Plan-Creator | Candidate and reviewer-evidence contract alignment |
| Topic plan | `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md` | Plan-Creator | Current execution contract |
| Topic specification | `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md` | Plan-Creator | Acceptance scenarios and scope guardrail |
| Step tracker | `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md` | Plan-Creator | Progression truth and gate state |
| Frozen legacy review log | `plan/observer-dispatcher-governance/observer-dispatcher-governance.review-log.md` | Plan-Reviewer | Frozen provenance only; never current-replan routing authority |
| Planning-review evidence | `plan/observer-dispatcher-governance/observer-dispatcher-governance.planning-review-evidence.md` | Plan-Reviewer | 此次 Human-authorized latest replan 唯一的 single machine-JSON routing evidence；不是 generic migration，且 required before replan commit or same-head continuation |
| Tester evidence | `plan/observer-dispatcher-governance/observer-dispatcher-governance.tester-evidence.md` | Tester | PR #1 current-head 的 declared checks、結果與 passing verdict；必須先於 implementation review log |
| Implementation review log | `plan/observer-dispatcher-governance/observer-dispatcher-governance.implementation-review-log.md` | Reviewer | Reference tester evidence 的獨立 implementation verdict；是 addressed-thread handling 的前置 gate |
| Topic summary | `plan/observer-dispatcher-governance/observer-dispatcher-governance.summary.md` | Human operator | Required close / next-handoff truth at human boundary |

- `README.md`, `VERSION`, `.github/copilot-instructions.md`, `src/**`, `tests/**`,
  `docs/**`，以及 `.github/agents/**` 不可修改；其中 `.github/agents/**` 為 frozen
  provenance 且不可用於 routing。
- 若後續工作需要 artifact table 之外的檔案，先由 Planner 修復 topic plan，再開始
  該工作；不得 broad-stage 或隱性納入。
- 本次 Human-authorized `needs-rework` 的 Plan-Creator repair 精確修改本 plan、`.spec.md`、
  `.step.md`、`plan/agent-handoff-workflow.md` 與 `plan/topic-plan-contract.md`：兩個
  shared-contract 文件分別限於 Human-only / 不可委派 boundary、future / new review-log 的
  prospective-only wording，以及此次 special evidence topology 的對齊；不得建立
  planning-review evidence。其後
  只有獨立 Plan-Reviewer 可寫入 declared planning-review evidence。既有 review-log、
  tester-evidence、implementation-review-log 皆為唯讀 frozen provenance；不得修改。

## Implementation Steps

### Implementation Dispatch Manifest

#### Goal

- 建立 project-mission 型 `GOAL.md`，並完成 Observer / Dispatcher governance
  與既有 workflow / topic-plan contract 的 bounded 對齊。

#### Non-Goal

- 不變更產品程式碼、public API、BC、Identity、Response Reuse、CacheStore、runtime、
  model execution、provider adapter 或 architecture decisions。
- 不修改 tests，不以動態 import 取代原有測試行為，且不執行 release、tagging、merge
  或 post-merge 動作。

#### In-Scope

- `GOAL.md`、`AGENTS.md`、`plan/agent-handoff-workflow.md`、
  `plan/topic-plan-contract.md` 與本 topic artifact table 所列檔案。

#### Out-Of-Scope

- 本 manifest 的 `ReadOnly`、`Deleted` 所列路徑，以及任何未在 `Written` 或
  `Modify` 所列的檔案。

#### ReadOnly

- `docs/project-direction.md` — 架構與 project mission 參考。
- `docs/business-capability-architecture.md` — BC boundary 參考。
- `docs/architecture/business-capability/architecture-brief.md` — BC architecture
  brief 參考。
- `docs/architecture/business-capability/index.html` — BC diagram 參考。
- `tests/test_package_import.py` — direct-import regression 行為參考。
- `pyproject.toml` — repository validation configuration 參考。
- `.github/agents/**` — frozen provenance；不可修改且不可作 runtime / routing
  dependency。

#### Written

| Path | Owner | Role |
| --- | --- | --- |
| `GOAL.md` | Implementer | Repository 長期 mission；非 task / phase authority |
| `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md` | Plan-Creator | Topic execution contract |
| `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md` | Plan-Creator | Acceptance scenarios |
| `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md` | Plan-Creator | Progression truth |

#### Modify

| Path | Owner | Role |
| --- | --- | --- |
| `AGENTS.md` | Implementer | Observer / Dispatcher governance and import-preservation policy |
| `plan/agent-handoff-workflow.md` | Plan-Creator | Workflow roles, stop points and phase routing alignment |
| `plan/topic-plan-contract.md` | Plan-Creator | Topic-plan authority and approved-evidence alignment |

本 manifest 僅列出 Plan-Creator 與 Implementer 的 bounded implementation work；Tester、
Reviewer、Plan-Reviewer 與 Human operator 的 evidence、verdict、routing 或 close
artifact 不在此 manifest 內，仍依既有 `Status / Allowed Transitions`、`Reviewer Handoff`
與 step tracker contract 管理。

#### Deleted

- None.

#### TestCase

- `tests/test_package_import.py::test_package_imports` 繼續以
  `import deterministic_response_cache` 直接匯入並通過既有 pytest check。
- 本 topic diff 不得修改既有 tests，亦不得新增 `importlib`、`__import__` 或
  `sys.modules` 作為 direct import 的替代。
- `GOAL.md` 僅包含 project mission / success direction；不得包含 active topic、
  current phase、workflow status、dispatcher routing 或 release state。
- 本 manifest 所涵蓋的 Plan-Creator／Implementer diff，除 `ReadOnly` 與
  `.github/agents/**` 必須為零 diff 外，僅能落在 `Written` 或 `Modify` 中列出的
  exact paths。

1. Implementer 在 `AGENTS.md` 寫入 repo 頂層 Observer / Dispatcher 規則：只讀
   state、委派單一角色、彙整 triage，並明確禁止實作、git / PR / release、gate
   推測及 review-comment handling。
2. Implementer 建立 `GOAL.md`，以 `docs/project-direction.md` 的
   provider-agnostic response-reuse mission 為方向，並明示它不具 task / phase
   authority。
3. Implementer 的 implementation diff 僅可包含 `AGENTS.md` 與 `GOAL.md`，並須
   保留既有 tests 的 direct-import 行為及 manifest 的所有 locked scope。
4. 本次 Human-authorized bounded replan 僅由 Plan-Creator 修正本 plan、`.spec.md`、
   `.step.md`、`plan/agent-handoff-workflow.md` 與 `plan/topic-plan-contract.md`；後兩個
   shared-contract 路徑只對齊 Human-only / 不可委派 boundary、future / new review-log 的
   prospective-only wording與已授權 special evidence topology。不得遷移或修改任何 legacy
   log、建立 reader / compatibility layer、觸及其他 topic，或由 Plan-Creator 建立 evidence；
   evidence gate 與後續 routing 只在 `Reviewer Handoff` 與 step tracker 定義。

## Validation / Acceptance Checks

- `GOAL.md` 符合 project mission boundary，且不含 active-work authority。
- `AGENTS.md` 的 Observer / Dispatcher 規則符合 locked decisions，且角色只使用
  已允許的 Planner、Plan-Creator、Plan-Reviewer、Reviewer、Tester、Implementer、
  Explorer。
- workflow 與 shared contract 的 active routing、planning evidence、conflict triage、
  human boundary 彼此一致：Planner 執行 preflight / Phase 4.5、Reviewer 處理 comments、
  Implementer 僅在 required evidence 與既有 human authorization 下 publish；沒有
  legacy publisher authority。
- 僅比較 manifest 所涵蓋的 Plan-Creator／Implementer paths：artifact table 與
  dispatch manifest 的 path、owner、role 必須一致，且該兩個角色的 diff 不得落在
  `Written` / `Modify` 外。此比較明確排除 `Reviewer Handoff`、step-owned special
  planning evidence 與 Reviewer-owned implementation-review evidence；它們不屬
  manifest，並持續依既有 `Reviewer Handoff`、status 與 step routing gates 驗證。
- existing test direct import 未被替換；相關 repository checks 在後續 Tester
  階段執行：`uv run pytest`、`uv run pyright`、`uv run tach check`、
  `uv run pre-commit run --all-files`。尚未有 declared tester-evidence artifact 前，
  不得聲稱這些 checks 已通過。
- latest replan 必須先由獨立 Plan-Reviewer 審核，並由其唯一寫入 declared
  planning-review evidence。single JSON record 必須完整符合 `Reviewer Handoff` schema，
  包含五個 declared replan artifacts 的 reviewed revisions / head、review basis、
  `verdict: approved|needs-rework`、`blocking_issues`、完整 `copilot_feedback_triage` 與
  timestamp，且必須涵蓋 latest replan revision。只有 `approved` record 可在既有 Human authorization
  下 commit replan，並讓後續 Tester / implementation-review same-head gates 繼續；frozen
  legacy review-log 不能取代此 gate。
- PR #1 的 current head 必須先有 Tester 的 passing evidence，再由 Reviewer 寫入
  reference 該 evidence 的 independent implementation verdict；只有 `approved` 或
  `needs-rework` 的有效 verdict 存在後，Reviewer 才可處理已 addressed threads。
- legacy review-log NDJSON finding 已明確 defer 為 prospective-only future policy；本
  topic 不進行 migration、reader、compatibility 或其他 topic 變更。既有 evidence logs
  維持 frozen provenance。
- 本 rework 產生新 PR #1 head 後，任何舊 head 的 Tester / Reviewer evidence 均不再
  滿足 same-head gate；必須重新執行，且本 plan 不宣稱新的 Tester 或 Reviewer completion。

## Reviewer Handoff

```json
{
  "reviewed_artifacts": [
    {
      "path": "<exact repo-visible path>",
      "revision": "<latest reviewed revision or head>"
    }
  ],
  "review_basis": "<independent review basis>",
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "copilot_feedback_triage": {
    "ADDRESS": [],
    "DISCUSS": [],
    "SKIP": []
  },
  "timestamp": "<RFC 3339 timestamp>"
}
```

`plan/observer-dispatcher-governance/observer-dispatcher-governance.planning-review-evidence.md`
是 current replan 唯一的 planning-review routing evidence。它只可由獨立
Plan-Reviewer 在審核 latest replan 後寫入；Plan-Creator、Implementer、Tester、Reviewer
或 Planner 不得代寫。它必須只含一個完整 JSON object，不可附帶 Markdown 或 prose；
`reviewed_artifacts` 必須恰好記錄 plan、spec、step、`plan/agent-handoff-workflow.md` 與
`plan/topic-plan-contract.md` 的 latest revisions / head，並完整包含 schema 的
`review_basis`、`verdict`、`blocking_issues`、`copilot_feedback_triage` 與 `timestamp`。

此 artifact 必須先覆蓋 latest replan revision，並具有 `approved` verdict，才可 commit
replan 或繼續 same-head Tester / implementation-review gates。`needs-rework` verdict 不可
自行恢復：topic 維持 `needs-rework`，僅可由 Human 再授權 prospective bounded replan。
existing `review-log.md` 是 frozen legacy provenance；不遷移、改寫、重讀，也不是 current
replan routing authority。這不是 topic plan 的 self-authored approval marker。

### Implementation Evidence and Review Gate

- `observer-dispatcher-governance.tester-evidence.md` 的最小 schema 為一個可讀的
  Markdown record，明列 `pr_number`、`head_sha`、`actor: Tester`、每項
  `command` 與 `result`，以及最終 `verdict: passing|failing`。只有同一 PR #1 head 的
  `verdict: passing` 可進入下一 gate；此 artifact 尚未建立時一律為 pending。
- `observer-dispatcher-governance.implementation-review-log.md` 的最小 schema 為一筆
  JSON object，除 `pr_number`、`head_sha`、`tester_evidence_path` 與
  `tester_evidence_verdict` 外，必須完整符合 shared `Reviewer Handoff`：
  `reviewed_artifacts`（current PR head 的 exact paths / revisions）、`review_basis`、
  `verdict: approved|needs-rework`、`blocking_issues`、完整
  `copilot_feedback_triage`（`ADDRESS`、`DISCUSS`、`SKIP` arrays）與 RFC 3339
  `timestamp`。Reviewer 必須獨立產生此 verdict；它不可由 Tester 或 Implementer 代寫。
- Reviewer 僅可在 implementation-review-log reference 到同一 head 的
  `verdict: passing` tester evidence 後，處理 PR #1 的已 addressed threads。此限制不
  改變 PR #1 的 Ready state，亦不授權 merge 或人類 approval。

## Post-merge / release actions

- 本 topic 無 repository release、VERSION bump 或 tagging action。
- draft PR 開啟後進入 human review boundary；Observer、Planner、Implementer 與
  Reviewer 均不得自行 merge、post-merge sync、release、tagging 或更新 final summary；
  這些 Human-only action 不可經由重新授權委派。
- human 於適當的 close / handoff 時建立 declared summary，至少包含 `current state`、
  `completed`、`not completed`、`required follow-up` 與 `next handoff`（含 next
  actor 與 next step）。

## Open Questions / Unresolved Items

- topic execution state 是 `needs-rework`；latest replan（本 plan、spec、step、
  `plan/agent-handoff-workflow.md` 與 `plan/topic-plan-contract.md`）的 independent
  planning-review evidence、approved replan commit、rework 後新 head 的 Tester evidence、
  Reviewer verdict 與 reviewer-comments routing 均為 pending。前一項 planning-review
  evidence 未有 `approved` 前，不可 commit replan 或繼續 same-head gates。舊 head 的
  same-head evidence 已失效於新 gate，不得宣稱新的 Tester 或 Reviewer completion。
- legacy review-log NDJSON finding 已 defer 至未建立的 future policy topic；本 topic
  只採 prospective interpretation，不遷移 logs、不建立 reader / compatibility layer，
  也不修改其他 topic。
- `step-creator` role-model conflict 已 out-of-scope defer 至
  `step-creator-role-model-alignment`；本 topic 不重新開啟它。
- optional analysis-layer artifacts 缺失已在 Goal / Outcome 警告中記錄；本 topic 不
  重新開啟已鎖定的 architecture、path 或 contract decisions。
