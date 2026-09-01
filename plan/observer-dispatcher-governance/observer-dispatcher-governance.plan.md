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
  - 本 topic 的 plan、spec、step、planning review-log、tester-evidence、
    implementation-review-log 與 human-close summary handoff artifacts。

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
- planning approval evidence 固定為
  `plan/<topic>/<topic>.review-log.md` 最後一筆完整 reviewer-handoff JSON record
  的 `"verdict": "approved"`。它由 Plan-Reviewer 在獨立 planning review 完成時
  寫入，並由獨立 Implementer 在 Planner preflight 前以 review-log-only evidence
  commit 固化；topic plan 不得含或依賴任何 self-authored approval marker。frozen
  `.github/agents/**` 僅為 provenance，不可修改，也不可作 runtime 或 routing
  dependency。
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

## Status / Allowed Transitions

- **Current**: `pr-open`。PR #1 維持 **Ready**；`pr-open` 可為 Draft 或 Ready，
  而 Ready 只表示 PR 可供 human review，絕不等同 independent implementation
  approval、human merge approval 或已 merge。
- **Bounded historical recovery**: preflight 曾在 implementation 前完成，但 step
  tracker 漏記該事實。Planner-authorized backfill 以 commit
  `490066f6753271181d289abdd593f119bd9ef48c`
  (`docs(governance): confirm observer plan preflight`) 為 evidence，將 parent plan /
  step 同步至 `creator-in-progress`。這只是 progression truth correction：不重跑或要求
  重跑 planning review、review-log evidence 或 preflight，不重開任何 locked decision，
  亦不宣稱 implementation 或 testing 已完成。
- **Current corrective gate**: Tester 必須先在 declared tester-evidence artifact 寫入
  passing evidence；其後 Reviewer 必須在 declared implementation-review-log reference
  該 evidence，並獨立寫入 `approved` 或 `needs-rework` verdict。兩份 artifact 在本次
  replan 時均為 pending；不得將既有口頭、step 或 PR state 當成已完成 evidence。
- **Thread gate**: 只有上述 Tester passing evidence 與 Reviewer independent verdict
  都存在且對同一 PR head 時，Reviewer 才可處理 PR #1 的已 addressed threads；在此之前
  reviewer-comments replan 維持 pending。此 gate 不授權任何 actor merge、resolve human
  approval 或把 Ready 重解為 approval。
- **Recorded nonconformance**: PR #1 已存在的 Ready state 是 current external fact，
  不補正為不存在，也不治癒 missing evidence；本 bounded replan 在不變更 PR state 的
  前提下補足 evidence-first comment routing。
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
| Review log | `plan/observer-dispatcher-governance/observer-dispatcher-governance.review-log.md` | Plan-Reviewer | Reviewer routing history; never replaces the plan |
| Tester evidence | `plan/observer-dispatcher-governance/observer-dispatcher-governance.tester-evidence.md` | Tester | PR #1 current-head 的 declared checks、結果與 passing verdict；必須先於 implementation review log |
| Implementation review log | `plan/observer-dispatcher-governance/observer-dispatcher-governance.implementation-review-log.md` | Reviewer | Reference tester evidence 的獨立 implementation verdict；是 addressed-thread handling 的前置 gate |
| Topic summary | `plan/observer-dispatcher-governance/observer-dispatcher-governance.summary.md` | Human operator | Required close / next-handoff truth at human boundary |

- `README.md`, `VERSION`, `.github/copilot-instructions.md`, `src/**`, `tests/**`,
  `docs/**`，以及 `.github/agents/**` 不可修改；其中 `.github/agents/**` 為 frozen
  provenance 且不可用於 routing。
- 若後續工作需要 artifact table 之外的檔案，先由 Planner 修復 topic plan，再開始
  該工作；不得 broad-stage 或隱性納入。

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
| `plan/observer-dispatcher-governance/observer-dispatcher-governance.review-log.md` | Plan-Reviewer | Reviewer verdict history |
| `plan/observer-dispatcher-governance/observer-dispatcher-governance.tester-evidence.md` | Tester | Current PR-head test evidence; created before implementation review |
| `plan/observer-dispatcher-governance/observer-dispatcher-governance.implementation-review-log.md` | Reviewer | Independent review verdict that references current passing tester evidence |
| `plan/observer-dispatcher-governance/observer-dispatcher-governance.summary.md` | Human operator | Close / next-handoff truth |

#### Modify

| Path | Owner | Role |
| --- | --- | --- |
| `AGENTS.md` | Implementer | Observer / Dispatcher governance and import-preservation policy |
| `plan/agent-handoff-workflow.md` | Plan-Creator | Workflow roles, stop points and phase routing alignment |
| `plan/topic-plan-contract.md` | Plan-Creator | Topic-plan authority and approved-evidence alignment |

#### Deleted

- None.

#### TestCase

- `tests/test_package_import.py::test_package_imports` 繼續以
  `import deterministic_response_cache` 直接匯入並通過既有 pytest check。
- 本 topic diff 不得修改既有 tests，亦不得新增 `importlib`、`__import__` 或
  `sys.modules` 作為 direct import 的替代。
- `GOAL.md` 僅包含 project mission / success direction；不得包含 active topic、
  current phase、workflow status、dispatcher routing 或 release state。
- `ReadOnly` 與 `.github/agents/**` 必須為零 diff；所有 diff 僅能落在 `Written`
  或 `Modify` 中列出的 exact paths。
- 獨立 Reviewer 驗證角色分離、manifest / artifact-path 一致性、frozen provenance
  boundary 與 import-preservation compliance。

1. Implementer 在 `AGENTS.md` 寫入 repo 頂層 Observer / Dispatcher 規則：只讀
   state、委派單一角色、彙整 triage，並明確禁止實作、git / PR / release、gate
   推測及 review-comment handling。
2. Implementer 建立 `GOAL.md`，以 `docs/project-direction.md` 的
   provider-agnostic response-reuse mission 為方向，並明示它不具 task / phase
   authority。
3. Implementer 的 implementation diff 僅可包含 `AGENTS.md` 與 `GOAL.md`，並須
   保留既有 tests 的 direct-import 行為及 manifest 的所有 locked scope。

## Validation / Acceptance Checks

- `GOAL.md` 符合 project mission boundary，且不含 active-work authority。
- `AGENTS.md` 的 Observer / Dispatcher 規則符合 locked decisions，且角色只使用
  已允許的 Planner、Plan-Creator、Plan-Reviewer、Reviewer、Tester、Implementer、
  Explorer。
- workflow 與 shared contract 的 active routing、planning evidence、conflict triage、
  human boundary 彼此一致：Planner 執行 preflight / Phase 4.5、Reviewer 處理 comments、
  Implementer 僅在 required evidence 與既有 human authorization 下 publish；沒有
  legacy publisher authority。
- artifact table 和 dispatch manifest 路徑、owner、role 完全一致；`Written` /
  `Modify` 外無 diff，`.github/agents/**` 零 diff。
- existing test direct import 未被替換；相關 repository checks 在後續 Tester
  階段執行：`uv run pytest`、`uv run pyright`、`uv run tach check`、
  `uv run pre-commit run --all-files`。尚未有 declared tester-evidence artifact 前，
  不得聲稱這些 checks 已通過。
- Plan-Reviewer 對已提交的 plan、spec、step 做獨立 review，將 latest fixed JSON
  verdict 記入 declared review log；只有最後一筆 record 為 `approved`，Planner 才可
  preflight implementation。
- PR #1 的 current head 必須先有 Tester 的 passing evidence，再由 Reviewer 寫入
  reference 該 evidence 的 independent implementation verdict；只有 `approved` 或
  `needs-rework` 的有效 verdict 存在後，Reviewer 才可處理已 addressed threads。

## Reviewer Handoff

Planning review log 使用 NDJSON；Plan-Reviewer 在完成 planning review 後，將下列
object 作為 `plan/observer-dispatcher-governance/observer-dispatcher-governance.review-log.md`
的最後 nonblank line。這不是 topic plan 的 self-authored approval marker。

```json
{
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "copilot_feedback_triage": {
    "ADDRESS": [],
    "DISCUSS": [],
    "SKIP": []
  }
}
```

### Implementation Evidence and Review Gate

- `observer-dispatcher-governance.tester-evidence.md` 的最小 schema 為一個可讀的
  Markdown record，明列 `pr_number`、`head_sha`、`actor: Tester`、每項
  `command` 與 `result`，以及最終 `verdict: passing|failing`。只有同一 PR #1 head 的
  `verdict: passing` 可進入下一 gate；此 artifact 尚未建立時一律為 pending。
- `observer-dispatcher-governance.implementation-review-log.md` 的最小 schema 為一筆
  JSON object，明列 `pr_number`、`head_sha`、`tester_evidence_path`、
  `tester_evidence_verdict`、`verdict: approved|needs-rework`、
  `blocking_issues`，以及 `copilot_feedback_triage`（`ADDRESS`、`DISCUSS`、`SKIP`
  arrays）。Reviewer 必須獨立產生此 verdict；它不可由 Tester 或 Implementer 代寫。
- Reviewer 僅可在 implementation-review-log reference 到同一 head 的
  `verdict: passing` tester evidence 後，處理 PR #1 的已 addressed threads。此限制不
  改變 PR #1 的 Ready state，亦不授權 merge 或人類 approval。

## Post-merge / release actions

- 本 topic 無 repository release、VERSION bump 或 tagging action。
- draft PR 開啟後進入 human review boundary；Observer、Planner、Implementer 與
  Reviewer 均不得自行 merge、post-merge sync 或更新 close summary。
- human 於適當的 close / handoff 時建立 declared summary，至少包含 `current state`、
  `completed`、`not completed`、`required follow-up` 與 `next handoff`（含 next
  actor 與 next step）。

## Open Questions / Unresolved Items

- PR #1 的 tester evidence、implementation-review-log 與 reviewer-comments replan
  均為 pending；在真實 evidence 寫入前不得宣稱完成。
- `step-creator` role-model conflict 已 out-of-scope defer 至
  `step-creator-role-model-alignment`；本 topic 不重新開啟它。
- optional analysis-layer artifacts 缺失已在 Goal / Outcome 警告中記錄；本 topic 不
  重新開啟已鎖定的 architecture、path 或 contract decisions。
