# Topic Plan Contract

## Purpose

定義 repo-visible topic plan 的 authority、required structure、planning evidence 與
preflight contract。本文件不取代 `AGENTS.md` 的 governance、
`plan/agent-handoff-workflow.md` 的 workflow phase，或個別 topic plan 的 locked scope。

## Authority Ordering

topic-plan 問題的 authority 依序為：

1. `AGENTS.md`
2. `plan/agent-handoff-workflow.md`
3. `plan/topic-plan-contract.md`
4. `plan/<topic>/<topic>.plan.md`
5. `plan/<topic>/<topic>.step.md`
6. `plan/<topic>/<topic>.review-log.md`
7. local planning skill guidance

`GOAL.md` 是 project mission，非 topic / phase authority。chat、branch、summary 與
`.github/agents/**` 不可用於選擇 candidate 或補推 planning evidence；
`.github/agents/**` 僅為 frozen provenance。

## Required Topic-Plan Sections

每個 repo-visible topic plan 必須依下列 canonical order 包含：

1. `Goal / Outcome`
2. `Scope`
3. `Locked Decisions`
4. `Boundaries / Exclusions`
5. `Status / Allowed Transitions`
6. `Artifact Paths`
7. `Implementation Steps`
8. `Validation / Acceptance Checks`
9. `Reviewer Handoff`
10. `Post-merge / release actions`
11. `Open Questions / Unresolved Items`

topic 可加 bounded section，但不可改寫這些 required section、workflow ownership 或
status transitions。影響 stable-library surface 的 topic 必須另列 `Stable library metadata`
與 timing；不影響者必須明示 non-stable intent。

## Planning baseline, evidence, and preflight

### Planning artifact commit

- Plan-Creator 寫入 topic plan、spec、step 與必要 shared planning-contract 變更，但
  不得 commit。
- 已有 human topic authorization 時，獨立 Implementer 將上述 planning artifacts
  以一個 bounded planning artifact commit 提交。這個 commit 是 `planned` 的
  repo-visible contract 前提，且早於 Plan-Reviewer re-review。
- planning artifact commit 只表示 plan 已提交可被獨立 review；它不表示
  implementation approval，亦不允許開始 implementation。

### Planning review record

planning review 的唯一 approved evidence 是 exact path：

`plan/<topic>/<topic>.review-log.md`

該檔案由 Plan-Reviewer 在完成獨立 review 後寫入。它必須是 chronological NDJSON：
每一個 nonblank line 是一個完整 JSON object，且最後一個 nonblank line 是 latest
verdict。當且僅當該最後 record 符合下列 `Reviewer Handoff` schema 並具有
`"verdict": "approved"`，planning evidence 才有效。

Plan-Reviewer 不得修改被審的 plan、spec 或 step；Plan-Creator、Planner、Implementer
均不得寫入或自我宣稱此 verdict。在 Planner preflight 前，只有具既有 human topic
authorization 的獨立 Implementer 可提交 review-log-only evidence commit。

topic plan 不得有 self-authored approval marker 或任何等價 field。

### Planner preflight

Planner 只讀取 candidate 的下列三個 artifact：

- `plan/<topic>/<topic>.plan.md`
- `plan/<topic>/<topic>.step.md`（required step tracker）
- `plan/<topic>/<topic>.review-log.md`

它據此判定唯一 candidate、phase、gate 與 next role。沒有 candidate 為 `blocked`；多
candidate 或 plan / step 指向不同 topic 為 `human-check`；同一 topic 的 status / scope
矛盾為 `blocked`，除非 Planner 明確 route Plan-Creator 進行 bounded repair。缺少 step、
review log 或 latest approved record 時不得開始 implementation。

planning approval evidence 不會把 topic execution status 設為 `approved`；`approved`
只保留給 workflow 中 independent implementation Reviewer 的 verdict。

## Artifact Path Rules

`Artifact Paths` 是 executable contract。每個列出 artifact 必須有 exact repo-visible
path、owner 與 role；不得用 `docs`、`tests` 或 `skill folder` 等 catch-all 描述。

每個 topic 至少明確列出：

- `plan/<topic>/<topic>.plan.md`（Plan-Creator）
- `plan/<topic>/<topic>.spec.md`（Plan-Creator）
- `plan/<topic>/<topic>.step.md`（Plan-Creator）
- `plan/<topic>/<topic>.review-log.md`（Plan-Reviewer）

若 topic 需要 correction artifacts 或 human summary，也必須在 artifact table 中列出
exact path、owner、role。若 work 需要未列 path，停止並交 Planner；不得自行擴張。

## Topic-Plan Contract Rules

- `Implementation Steps` 僅描述 locked implementation work，不得混入
  Plan-Reviewer verdict、Planner routing、Reviewer acceptance 或 human-only action。
- `Reviewer Handoff` 是 Plan-Reviewer 與 Reviewer 都使用的 machine-consumable schema；
  topic plan 必須完整嵌入一份。
- `Post-merge / release actions` 必須符合 topic 的 stable-library / release intent，
  並將 merge、post-merge、release 留在 human boundary。
- 若 execution 需 frozen analysis artifacts，只可 read / validate；不得隱性重開或
  regenerate。
- `TBD`、`later`、`follow normal process` 等在需要明確 contract 時屬 blocking failure。

## Reviewer Handoff

每一筆 review-log record 與 topic plan 的 `Reviewer Handoff` 必須符合以下固定 JSON
object：

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

`blocking_issues` 只列 true contract-breaking issue。記錄不能有 JSON 外的 trailing
prose；最新 verdict 以 review log 最後 nonblank NDJSON line 為準。

## Blocking Semantics

下列情況是 contract-breaking：

- required section、required step tracker、exact artifact path 或 required planning
  evidence 缺失；
- status transition 無效；
- artifact path scope drift、undeclared stable-library intent 或錯誤 release timing；
- review log 最新 record 非有效 JSON、shape 不符或 verdict 非 `approved`；
- self-authored approval marker、混合 role ownership 或 simulated separation；
- plan、step、review-log 或 required repo contract 的 execution meaning 衝突；
- 以 chat、branch、summary、`GOAL.md` 或 frozen provenance 取代 required evidence。

Plan-Creator 遇到缺失 planning input 必須停止；Plan-Reviewer 對 contract-breaking
issue 必須回傳 `needs-rework`；Planner 對 unresolved conflict 必須 route `blocked` 或
`human-check`，不可自行選擇方便的 interpretation。

## Boundaries

- 本文件不授權修改 `skills/**`、`.github/skills/**`、`.codex/skills/**`、
  `.github/agents/**` 或 `.codex/agents/**`。
- 本文件不把 planning baseline 或 planning-review approval 轉換成 implementation
  approval。
- 本文件不授權 product、BC、runtime、identity、provider 或 release work。
