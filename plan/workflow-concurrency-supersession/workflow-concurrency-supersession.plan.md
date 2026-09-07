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

**Bootstrap transition**：Human 明確授權本 topic 在 B6R13/R23 未完成時建立並提交本五份 planning
artifacts。其提交後，唯一 next role 是 independent Plan-Reviewer；approved receipt 必須 committed，
Planner 才可 re-preflight 並決定後續 role。此 exception 不啟動 `src-implementation`。

**Execution model**：`planned` -> `creator-in-progress` -> `tester-in-progress` -> `review-ready` ->
`reviewer-in-progress` -> `approved` -> `publish-in-progress` -> `pr-open` -> Human `merged` -> terminal。
Creator implementation 必須先經 independent Tester；Tester passing evidence 與 independent Reviewer approval
必須綁定同一 immutable subject。標準 Phase 4.5 Planner alignment 適用於 publish。

**Allowed transitions**：`planned` -> `creator-in-progress`; `creator-in-progress` ->
`tester-in-progress`; `tester-in-progress` -> `review-ready`; `review-ready` ->
`reviewer-in-progress`; `reviewer-in-progress` -> `approved|needs-rework`; `needs-rework` ->
`creator-in-progress`; `approved` -> `creator-in-progress|publish-in-progress`;
`publish-in-progress` -> `pr-open`; `pr-open` -> `needs-rework|merged`; `merged` -> terminal。
Only Human may move `pr-open` to `merged`; no release transition exists.

## Artifact Paths

| Artifact | Exact path | Write owner | Decision authority / role |
| --- | --- | --- | --- |
| Requirements | `analysis/workflow-concurrency-supersession/requirements.md` | Plan-Creator | Human override scope guardrail |
| Technical specification | `analysis/workflow-concurrency-supersession/technical-spec.md` | Plan-Creator | execution-facing planning source |
| Topic plan | `plan/workflow-concurrency-supersession/workflow-concurrency-supersession.plan.md` | Plan-Creator | topic execution contract |
| Topic specification | `plan/workflow-concurrency-supersession/workflow-concurrency-supersession.spec.md` | Plan-Creator | acceptance contract |
| Step tracker | `plan/workflow-concurrency-supersession/workflow-concurrency-supersession.step.md` | Plan-Creator | committed topic progression evidence |
| Governance guardrails | `AGENTS.md` | Implementer | approved topic-local routing contract |
| Workflow handoff contract | `plan/agent-handoff-workflow.md` | Implementer | approved lifecycle/routing contract |
| Topic-plan contract | `plan/topic-plan-contract.md` | Implementer | approved candidate/evidence conflict contract |

`README.md`、`VERSION` 與 `.github/copilot-instructions.md` 不得修改。Artifact Paths 是 executable
allowlist；任何新增 receipt/evidence location、產品 path 或其他文件都必須停止並由 Planner 重新路由。

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
- independent Plan-Reviewer 能以 reviewer handoff JSON 給出本 plan 的 `approved` 或 `needs-rework` verdict；
  approved 後由 Planner re-preflight，而非由 Plan-Creator 或 Observer 自行前進。

## Reviewer Handoff

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

## Post-merge / release actions

No repository release action is authorized. `README.md` and `VERSION` remain unchanged. Only Human may
merge; no release, tag or post-merge work belongs to this topic.

## Open Questions / Unresolved Items

None. `src-implementation` remains a later, separate topic whose folders and implementation requirements are
intentionally undecided.
