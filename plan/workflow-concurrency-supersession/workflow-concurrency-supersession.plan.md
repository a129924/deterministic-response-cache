# Workflow Concurrency Supersession

## Goal / Outcome

以 topic-local committed evidence 取代 B6R13/R23 的全域 routing lock。完成後，互不衝突的
topics 可在隔離 branch/worktree 內並行完成各自 planning、implementation、Tester 與 independent
Reviewer phases；publish 與 Human boundary 維持 subject-local gates。

## Scope

- **In scope**：建立本 topic analysis/plan/spec/step artifacts；在 independent Plan-Reviewer
  approval、Planner re-preflight 與後續 topic-local gates 後，僅更新 `AGENTS.md`、
  `plan/agent-handoff-workflow.md`、`plan/topic-plan-contract.md` 以記載 supersession contract。
- **Out of scope**：`src-implementation` folders 或任何產品設計；R23/S17 或 B6R13 的執行、
  repair、取消或補建；frozen provenance；README/VERSION；release、tag、merge、post-merge。

## Locked Decisions

- Human 的明確 override 僅授權此唯一 bootstrap exception；聊天方向不是 Git evidence，且不能
  追認或取代未提交 R23。
- B6R13/R23 保留其 subject-local obligations。其 pending、missing、needs-rework 或同-topic
  divergence 只影響 B6R13，不能阻擋無衝突新 topic。
- 每個 topic 必須以自身 committed plan、step、Plan-Reviewer receipt、immutable subject、Tester
  evidence 與 independent Reviewer evidence route；任何 evidence 不得跨 topic 使用。
- 平行只允許隔離 branch/worktree。declared write path、candidate、evidence 或 subject 的衝突
  一律 `human-check`；不自動 rebase、合併、選擇 candidate 或擴大 allowlist。
- publish 仍要求同-subject passing Tester evidence、independent Reviewer approval、Planner Phase
  4.5 alignment 及既有 human authorization；允許多個 draft PR。只有 Human 可 merge、release、
  tag 與 post-merge。
- 本 topic 是 non-stable、無 README/VERSION change、無 release；不建立任何 stable-library API。

## Boundaries / Exclusions

Observer 維持唯讀 dispatch/aggregate；Planner 維持 candidate/phase/gate/one-next-role authority。Plan-Creator
只寫 declared planning artifacts，Plan-Reviewer 獨立審 planning evidence，Implementer 只執行 approved
bounded contract update，Tester 只寫 factual evidence，Reviewer 只獨立驗證同-subject Tester evidence。
Reviewer 不是 Human PR reviewer。未列於 Artifact Paths 的檔案、任何 folder tree、產品程式或既有
governance-topic evidence 都必須停止並返回 Planner。

## Status / Allowed Transitions

**Current**：`planned`。

**Bootstrap transition**：Human 明確授權本 topic 在 B6R13/R23 未完成時建立 planning evidence，但不合併
角色。Plan-Creator 只 author 或 bounded repair 五份 declared analysis/planning artifacts；本次 `needs-rework`
repair 僅可變更本 plan、spec 與 step 三檔，無需變更 analysis artifacts。獨立
Implementer 是唯一 commit owner，必須先以 planning-candidate-only commit 提交 Plan-Creator 原樣產物，才產生
可審核的 committed planning candidate。其唯一 next role 是 independent Plan-Reviewer。

**Planning-review transition**：Independent Plan-Reviewer 只可寫入
`plan/workflow-concurrency-supersession/workflow-concurrency-supersession.plan-review-log.md`，並以既定
machine-consumable `approved|needs-rework` schema 對該 committed candidate 作出 verdict；Plan-Reviewer 不得
commit。若 verdict 是 `approved`，獨立 Implementer 必須先原樣以 standalone evidence-only commit 提交該
receipt，Planner 才可 re-preflight 並 route 至 bounded contract Implementer。若 verdict 是 `needs-rework`，
receipt 不得提交，且不產生 candidate、route 或 authorization；只可回到 Plan-Creator bounded repair，接著由
獨立 Implementer 提交新的 planning repair candidate，並重新接受獨立 Plan-Reviewer review。此 exception
不啟動 `src-implementation`。

**Execution model**：`planned` -> `plan-creator-authoring-or-repair` ->
`planning-candidate-commit-pending` -> `planning-review-pending` ->
`plan-review-receipt-pending` -> `approved-receipt-commit-pending` -> `planner-repreflight-pending` ->
`implementer-in-progress` -> `tester-in-progress` -> `review-ready` -> `reviewer-in-progress` -> `approved` ->
`publish-in-progress` -> `pr-open` -> Human `merged` -> terminal。Plan-Creator 不實作 contract；bounded contract
Implementer 必須先經 independent Tester。Tester passing evidence 與 independent Reviewer approval 必須綁定同一
immutable subject。標準 Phase 4.5 Planner alignment 適用於 publish。

**Allowed transitions**：`planned` -> `plan-creator-authoring-or-repair`; `plan-creator-authoring-or-repair` ->
`planning-candidate-commit-pending`; `planning-candidate-commit-pending` -> `planning-review-pending`（僅於獨立
Implementer 已提交原樣 planning candidate 後）；`planning-review-pending` -> `plan-review-receipt-pending`;
`plan-review-receipt-pending` -> `approved-receipt-commit-pending|plan-creator-authoring-or-repair`；只有
`approved-receipt-commit-pending` 在獨立 Implementer 已提交原樣 `approved` receipt 後可轉為
`planner-repreflight-pending`；Planner 重新 preflight 後才可轉為 `implementer-in-progress`。`needs-rework`
receipt 不得 commit，且只允許回到 bounded planning repair。其後為 `implementer-in-progress` ->
`tester-in-progress` -> `review-ready` -> `reviewer-in-progress` -> `approved|needs-rework`; implementation
`needs-rework` -> `implementer-in-progress`; `approved` -> `publish-in-progress`; `publish-in-progress` ->
`pr-open`; `pr-open` -> `needs-rework|merged`; `merged` -> terminal。Only Human may move `pr-open` to `merged`;
no release transition exists.

## Artifact Paths

| Artifact | Exact path | Write owner | Decision authority / role |
| --- | --- | --- | --- |
| Requirements | `analysis/workflow-concurrency-supersession/requirements.md` | Plan-Creator | Human override scope guardrail |
| Technical specification | `analysis/workflow-concurrency-supersession/technical-spec.md` | Plan-Creator | execution-facing planning source |
| Topic plan | `plan/workflow-concurrency-supersession/workflow-concurrency-supersession.plan.md` | Plan-Creator | topic execution contract |
| Topic specification | `plan/workflow-concurrency-supersession/workflow-concurrency-supersession.spec.md` | Plan-Creator | acceptance contract |
| Step tracker | `plan/workflow-concurrency-supersession/workflow-concurrency-supersession.step.md` | Plan-Creator | committed topic progression evidence |
| Plan-Reviewer receipt | `plan/workflow-concurrency-supersession/workflow-concurrency-supersession.plan-review-log.md` | Independent Plan-Reviewer | only writer; machine-consumable verdict for the committed planning candidate; never commits it |
| Governance guardrails | `AGENTS.md` | Implementer | approved topic-local routing contract |
| Workflow handoff contract | `plan/agent-handoff-workflow.md` | Implementer | approved lifecycle/routing contract |
| Topic-plan contract | `plan/topic-plan-contract.md` | Implementer | approved candidate/evidence conflict contract |

`README.md`、`VERSION` 與 `.github/copilot-instructions.md` 不得修改。Artifact Paths 是 executable
allowlist；Plan-Creator 僅可寫入前五份 analysis/planning artifacts，Plan-Reviewer 僅可寫入上述 exact
receipt path 且絕不可 commit，獨立 Implementer 是唯一 commit owner：先提交原樣 planning candidate、再在
approved verdict 後提交原樣 receipt evidence-only，並只在 Planner re-preflight routing 後寫入三份 governance
contract。任何新增 receipt/evidence location、產品 path 或其他文件都必須停止並由 Planner 重新路由。

## Implementation Steps

1. 以本 technical specification 的五項 contract model 更新三個 declared governance contract files：
   以 topic-local evidence routing 取代全域唯一 current route，並保留 B6R13/R23 為 subject-local
   frozen/current obligation。
2. 在三份 contract 中明定每個 topic 的 committed evidence isolation、隔離 branch/worktree、衝突的
   `human-check` behavior，以及不得用 chat、branch、summary 或 frozen provenance 作 routing evidence。
3. 在三份 contract 中保留 Tester -> independent Reviewer -> Planner Phase 4.5 -> human-authorized
   bounded publish -> `pr-open` -> Human-only merge/release/tag/post-merge sequence，並允許多個 draft PR。
4. 驗證完整 diff 只包含本 Artifact Paths；不建立 `src-implementation` folder tree，亦不變更
   B6R13/R23 artifacts。

## Validation / Acceptance Checks

- planning artifacts 與 implementation diff 均只使用列出的 exact paths；current status 是 `planned`。
- B6R13/R23 未提交聊天結果明確為 non-evidence，且 B6R13 僅 subject-local blocked，不可封鎖無衝突 topic。
- 契約要求每一 topic 的 plan、step、Plan-Reviewer receipt、subject、Tester 與 Reviewer evidence 同 topic
  且 committed；cross-topic reuse、path/candidate/evidence/subject conflict 導向 `human-check`。
- 任何 topic 未具 same-subject passing Tester、independent Reviewer、Planner Phase 4.5 或 human authorization
  時不可 publish；多 draft PR 可同時存在，Human-only merge/release/tag/post-merge 不變。
- Independent Plan-Reviewer 僅能在 exact receipt path 以 machine-consumable record 寫入本 committed
  candidate 的 `approved` 或 `needs-rework` verdict；record 必須包含 `topic`、`candidate_commit`（完整 SHA）、
  `verdict` 與 `blocking_issues`，且 Plan-Reviewer 不得 commit。只有獨立 Implementer 原樣提交的 `approved`
  receipt standalone evidence-only commit 允許 Planner re-preflight；`needs-rework` receipt 不得提交、不產生
  candidate、route 或 authorization，必須由 Plan-Creator bounded repair、獨立 Implementer 提交新 candidate 後
  重新獨立 review。Plan-Creator 或 Observer 均不可自行前進。

## Reviewer Handoff

The exact Plan-Reviewer receipt path is
`plan/workflow-concurrency-supersession/workflow-concurrency-supersession.plan-review-log.md`. Its only
writer is Independent Plan-Reviewer. The file contains one machine-consumable JSON object for the committed
planning candidate; its required fields are `topic`, `candidate_commit` (full SHA), `verdict`
(`approved|needs-rework`) and `blocking_issues`. The receipt is not created or prefilled by Plan-Creator.
Plan-Reviewer never commits. Only an independent Implementer may commit an `approved` receipt unchanged as a
standalone evidence-only commit, which may authorize Planner re-preflight; a `needs-rework` receipt is never
committed and returns this topic to bounded planning repair. The repaired planning artifacts must be committed
as a new candidate by an independent Implementer and independently reviewed again.

## Post-merge / release actions

No repository release action is authorized. `README.md` and `VERSION` remain unchanged. Only Human may
merge; no release, tag or post-merge work belongs to this topic.

## Open Questions / Unresolved Items

None. `src-implementation` remains a later, separate topic whose folders and implementation requirements are
intentionally undecided.
