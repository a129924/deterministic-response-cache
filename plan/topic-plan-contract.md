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

對於本條生效後**新建的 future review log**，該檔案由 Plan-Reviewer 在完成獨立
review 後寫入，並必須是 chronological NDJSON：每一個 nonblank line 是一個完整 JSON
object，且最後一個 nonblank line 是 latest verdict。當且僅當該最後 record 符合下列
`Reviewer Handoff` schema 並具有 `"verdict": "approved"`，planning evidence 才有效。

本 NDJSON 規則僅 prospective 適用於 future / new logs。此條生效前已存在的 review
logs 是 frozen provenance：本 contract 不會遷移、改寫、關閉、重讀或以格式不符使其
失效，也不會改變其所屬 topic 的既有 evidence status。legacy log 的分類、讀取與任何
長期 policy，必須由另一個 future policy topic 明確定義；不得在本 shared contract 或
無關 topic 內推導或補作。

Plan-Reviewer 不得修改被審的 plan、spec 或 step；Plan-Creator、Planner、Implementer
均不得寫入或自我宣稱此 verdict。在 Planner preflight 前，只有具既有 human topic
authorization 的獨立 Implementer 可提交 review-log-only evidence commit。

topic plan 不得有 self-authored approval marker 或任何等價 field。

### Human-authorized current-topic replan evidence topology

此 shared contract 不建立 generic legacy-log migration 或第二種一般 planning-review
evidence。僅對已由 Human 明示授權的 current-topic replan，個別 topic plan 可列出一個
exact、Plan-Reviewer-owned special evidence path，並必須同時列明它覆蓋的 latest replan
artifacts、revisions / head、gate 與 status。當前唯一適用實例是：

`plan/observer-dispatcher-governance/observer-dispatcher-governance.recovery-planning-review-evidence.md`

它只為 `observer-dispatcher-governance` 的目前 `needs-rework` bounded replan 提供 routing
evidence。independent Plan-Reviewer 在完成該 latest replan review 後，將一個完整 JSON
object 寫入此 exact path；Plan-Creator、Planner、Implementer、Tester 與 Reviewer 不得
代寫。該 object 的 `reviewed_artifacts` 必須只涵蓋本次 replan 的 plan、spec、step、
`plan/agent-handoff-workflow.md` 與 `plan/topic-plan-contract.md`，並記錄每個 artifact 的
latest revision / head。

只有這個 exact record 完整符合下列 `Reviewer Handoff` schema 且
`"verdict": "approved"`，獨立 Implementer 才可建立唯一的 planning-evidence commit。該
commit 同時固化五個已審 replan artifact 與這個 planning-review evidence，其 commit SHA
在建立後固定為 immutable `implementation_subject_sha`；此 subject 不是可由 chat、PR
Ready state、branch 名稱或 frozen evidence 推測或替換的值。`needs-rework` 維持 topic
`needs-rework`，不得自行恢復，後續 replan 必須另有 Human 明示授權。

在 `implementation_subject_sha` 之後，本 topic 僅允許兩個線性、evidence-only descendant
commits：Tester evidence commit 僅新增
`plan/observer-dispatcher-governance/observer-dispatcher-governance.recovery-tester-evidence.md`，
Reviewer evidence commit 僅新增
`plan/observer-dispatcher-governance/observer-dispatcher-governance.recovery-implementation-review-log.md`。
Tester 與 Reviewer 分別擁有 record 的內容；若需要 git commit，獨立 Implementer 只能原樣
固化該 role 已寫入的單一路徑 evidence，不能改寫 verdict、夾帶其他檔案或 push。
兩個 record 都必須明列同一個 `implementation_subject_sha`；Reviewer record 還必須 reference
passing Tester record。最後的 descendant range 必須無 merge 且
`git diff --name-status <implementation_subject_sha>..HEAD` 恰好只列出這兩個 declared
implementation evidence paths，不得有其他 path、thread、push、merge、release 或 summary
action。existing `review-log.md`、planning-review evidence、Tester evidence 與
implementation-review log 在 `df137326363cce4f68e43124156731a50cf29a03` 均為 frozen,
superseded provenance：不得遷移、改寫、重讀或作此 recovery routing authority。本 exception
不可被其他 topic、legacy log 或 future policy 推導或複製。

### Planner preflight

Planner 只讀取 candidate 的下列三個 artifact：

- `plan/<topic>/<topic>.plan.md`
- `plan/<topic>/<topic>.step.md`（required step tracker）
- `plan/<topic>/<topic>.review-log.md`

它據此判定唯一 candidate、phase、gate 與 next role。沒有 candidate 為 `blocked`；多
candidate 或 plan / step 指向不同 topic 為 `human-check`；同一 topic 的 status / scope
矛盾為 `blocked`，除非 Planner 明確 route Plan-Creator 進行 bounded repair。缺少 step、
review log 或 required approved record 時不得開始 implementation。對 legacy log，不得
只因本 prospective NDJSON 規則而推定 record 缺失或不合格；其既有 topic contract
仍是唯一可用的 evidence interpretation，直至 future policy topic 明確變更。

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
- `Reviewer Handoff` 是 Plan-Reviewer 與 Reviewer 都使用的 fixed machine-JSON schema；
  topic plan 必須完整嵌入一份。若是 human-authorized special replan evidence，必須於
  此 section 而非 `Implementation Steps` 宣告其 exact path、ownership 與 gate。
- `Post-merge / release actions` 必須符合 topic 的 stable-library / release intent，
  並將 merge、post-merge、release 留在 human boundary。
- 若 execution 需 frozen analysis artifacts，只可 read / validate；不得隱性重開或
  regenerate。
- `TBD`、`later`、`follow normal process` 等在需要明確 contract 時屬 blocking failure。

## Reviewer Handoff

future / new review-log record、human-authorized special replan evidence 與 topic plan 的
`Reviewer Handoff` 必須符合以下固定 machine JSON object：

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

`reviewed_artifacts` 的每個 item 都必須有 exact `path` 與其 `revision`；`review_basis`
必須足以辨識獨立審核依據；`timestamp` 必須是產生 verdict 的 RFC 3339 時間。`blocking_issues`
只列 true contract-breaking issue，`copilot_feedback_triage` 必須完整保有 `ADDRESS`、
`DISCUSS`、`SKIP` arrays。對 future / new logs，記錄不能有 JSON 外的 trailing prose，
最新 verdict 以 review log 最後 nonblank NDJSON line 為準；special evidence path 則必須
只含一個完整 JSON object。此段不追溯適用 frozen legacy logs。

唯一 current-topic recovery 的 Reviewer evidence record 除此 fixed schema 外，必須新增
`implementation_subject_sha`（planning-evidence commit 的完整 immutable SHA）、
`tester_evidence_path`、`tester_evidence_verdict: "passing"` 與 Tester record 的 revision。
Recovery Tester Markdown record 必須含相同的 `implementation_subject_sha`、`actor: Tester`、
每項 `command` / `result`、`verdict: passing|failing`、timestamp 及其 subject 驗證結果。
這些是 topic-specific additional fields，不改寫 generic future / new review-log schema。

## Blocking Semantics

下列情況是 contract-breaking：

- required section、required step tracker、exact artifact path 或 required planning
  evidence 缺失；
- status transition 無效；
- artifact path scope drift、undeclared stable-library intent 或錯誤 release timing；
- future / new review log 或已明定 special replan evidence 的 latest record 非有效 JSON、
  shape 不符、reviewed revision 未覆蓋 required latest artifact，或 verdict 非 `approved`；
- recovery Tester / Reviewer record 的 `implementation_subject_sha` 不存在、不相同、不是
  planning-evidence commit，或 recovery descendant 不是 linear / evidence-only，或其
  `git diff --name-status <implementation_subject_sha>..HEAD` 不是恰好兩個 declared
  implementation evidence paths；
- self-authored approval marker、混合 role ownership 或 simulated separation；
- plan、step、review-log、已明定 special replan evidence 或 required repo contract 的
  execution meaning 衝突；
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
- 本文件不授權對 frozen legacy review logs 的 migration、reader、compatibility layer 或
  其他 topic 修改；這些只可由獨立 future policy topic 規劃。
