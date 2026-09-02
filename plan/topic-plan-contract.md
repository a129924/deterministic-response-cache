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
6. `plan/<topic>/<topic>.review-log.md`，或在本文件明定的 current-topic correction
   route 中，該 route 的 exact correction-review evidence path
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

### Human-authorized current-topic correction route

本 shared contract 不建立 generic legacy-log migration 或第二種一般 planning-review
evidence。Human 對 current topic `observer-dispatcher-governance` 的唯一 scope expansion
authorization 是：`2. 授權擴張 current topic。` 依此授權，唯一 current correction route
是 parent plan / spec / step 與 correction plan / step 在兩份 shared contracts 下的
bounded combination；parent artifacts 保持 current execution truth，correction artifacts
只保留 correction delta，不能升格為 parent。

此 route 的 exact pre-implementation evidence path 是：

`plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-review-log.md`

舊 epoch 的 terminal 是 `R0=cb3f66c60e95e5580cb2b30632d0d5ed9f0d0ee9`；其唯一識別 predicate
是 `ecc5b6f61bacc5493ca3a9f1012d1bfdd43a810c..cb3f66c60e95e5580cb2b30632d0d5ed9f0d0ee9`。
它與所有 normal / `recovery-*` evidence 均為 frozen provenance，不能作為 current gate。

這是只適用 current topic 的狹義一次性 `B0` exception。normal planning-artifact-commit
prerequisite 在此例外中暫停：independent Plan-Reviewer 可在任何 declared implementation
path 被寫入前，審閱同一 working tree 的 tree SHA 與下列七個**未提交** planning artifact 的
exact path/blob revision：

- `plan/agent-handoff-workflow.md`
- `plan/topic-plan-contract.md`
- `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md`
- `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md`
- `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md`
- `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-plan.md`
- `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-step.md`

Plan-Reviewer only owns its independent verdict, not topic routing. After that reviewer writes the
single schema-complete correction record, an Independent Implementer under existing Human commit
authorization commits exactly that record plus those seven reviewed planning artifacts as `B0`.
`B0` is not an `implementation_subject_sha`. An `approved` `B0` permits declared implementation;
`needs-rework` keeps the topic in `needs-rework` and Planner decides bounded repair.

The subsequent non-merge commit completing declared implementation is `S1`, the replacement
immutable `implementation_subject_sha`. Only `T1` (Tester writes
`observer-dispatcher-governance.correction-tester-evidence.md`) then `V1` (Reviewer writes
`observer-dispatcher-governance.correction-implementation-review-log.md`) may descend from `S1`.
Both attest `S1`, the second references passing `T1`, and verification is exactly
`git diff --name-status S1..V1`; it must list only those two paths and never substitute `HEAD`.
This current-topic exception grants no push, PR-thread action, merge, post-merge, release, tagging
or summary action, and cannot be generalized to another topic.

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
path、**write owner**、**decision authority** 與 role；不得用 `docs`、`tests` 或 `skill
folder` 等 catch-all 描述。write owner 不會因寫入 artifact 取得 route、status、gate 或
lifecycle authority。

每個 topic 至少明確列出：

- `plan/<topic>/<topic>.plan.md`（Plan-Creator）
- `plan/<topic>/<topic>.spec.md`（Plan-Creator）
- `plan/<topic>/<topic>.step.md`（Plan-Creator）
- `plan/<topic>/<topic>.review-log.md`（Plan-Reviewer）

若 topic 需要 correction artifacts 或 human summary，也必須在 artifact table 中列出
exact path、write owner、decision authority、role。若 work 需要未列 path，停止並交 Planner；
不得自行擴張。

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

### Current-topic correction evidence schemas

下列三個 JSON object 只適用
`observer-dispatcher-governance` 的 current correction route；每個 exact evidence path 只可
含一個 object，不得附加 Markdown 或 prose。它們不改寫 generic future / new review-log
schema，也不追溯適用 frozen legacy / recovery evidence。

先於 implementation 的 correction-plan review record 必須符合：

```json
{
  "schema_version": "observer-dispatcher-governance.correction-plan-review.v1",
  "correction_id": "observer-dispatcher-governance/high",
  "review_kind": "correction-plan",
  "severity": "high",
  "routing_state": "PLANNER_REPLAN",
  "reviewed_tree_sha": "<exact tree SHA containing the seven uncommitted reviewed planning artifacts>",
  "reviewed_artifacts": [
    {
      "path": "<one of the seven exact current correction planning paths>",
      "blob_sha": "<exact reviewed working-tree blob SHA>"
    }
  ],
  "review_basis": "<independent correction-plan review basis>",
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

`reviewed_artifacts` must contain each of the seven paths enumerated in the current-topic route
exactly once. `reviewed_tree_sha` and every path/blob revision identify the exact uncommitted
correction state reviewed before `B0`. Only Plan-Reviewer writes this record; its `approved`
verdict is a precondition for the `B0` commit and then implementation. Planner still owns route
and status decisions.

Tester evidence after the immutable implementation subject must conform to:

```json
{
  "schema_version": "observer-dispatcher-governance.correction-tester-evidence.v1",
  "correction_id": "observer-dispatcher-governance/high",
  "actor": "Tester",
  "implementation_subject_sha": "<full immutable implementation commit SHA>",
  "subject_verification": {
    "expected_sha": "<same full SHA>",
    "observed_sha": "<same full SHA>",
    "command": "<exact verification command>",
    "result": "passing|failing"
  },
  "commands": [
    {
      "command": "<exact command>",
      "exit_code": 0,
      "result": "passing|failing"
    }
  ],
  "correction_test_result": "passing|failing",
  "repository_validation_result": "passing|failing",
  "verdict": "passing|failing",
  "timestamp": "<RFC 3339 timestamp>"
}
```

Implementation-review evidence after a passing Tester record must conform to:

```json
{
  "schema_version": "observer-dispatcher-governance.correction-implementation-review.v1",
  "correction_id": "observer-dispatcher-governance/high",
  "review_kind": "correction-implementation",
  "severity": "high",
  "implementation_subject_sha": "<full immutable implementation commit SHA>",
  "reviewed_commit_sha": "<V1 commit SHA containing only the two allowed evidence descendants from S1>",
  "tester_evidence": {
    "path": "plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-tester-evidence.md",
    "revision": "<Tester evidence commit SHA>",
    "implementation_subject_sha": "<same full immutable SHA>",
    "verdict": "passing"
  },
  "reviewed_artifacts": [
    {
      "path": "<exact declared implementation or evidence path>",
      "revision": "<reviewed revision>"
    }
  ],
  "review_basis": "<independent implementation review basis>",
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

Tester writes only factual test evidence. Reviewer writes only its independent verdict. Neither
write owner may change the subject, route, status or next role; those remain Planner decisions.

## Blocking Semantics

下列情況是 contract-breaking：

- required section、required step tracker、exact artifact path 或 required planning
  evidence 缺失；
- status transition 無效；
- artifact path scope drift、undeclared stable-library intent 或錯誤 release timing；
- future / new review log 或已明定 special replan evidence 的 latest record 非有效 JSON、
  shape 不符、reviewed revision 未覆蓋 required latest artifact，或 verdict 非 `approved`；
- current correction review evidence is absent, not schema-complete, lacks `reviewed_tree_sha` or
  one exact path/blob revision for each of the seven declared uncommitted planning artifacts, is
  not committed with exactly that reviewed set as `B0`, or is written after declared implementation begins;
- correction Tester / Reviewer record 的 `implementation_subject_sha` 不存在、不相同、不是
  `S1` completed implementation commit，或 correction descendant 不是 `S1 -> T1 -> V1` linear /
  evidence-only chain，或 `git diff --name-status S1..V1` 不是恰好兩個 declared implementation
  evidence paths，或以 `HEAD` 取代具名 `V1`；
- self-authored approval marker、混合 role ownership 或 simulated separation；
- plan、step、review-log、已明定 special replan evidence 或 required repo contract 的
  execution meaning 衝突；
- 以 chat、branch、summary、`GOAL.md` 或 frozen provenance 取代 required evidence。

Plan-Creator 遇到缺失 planning input 必須停止；Plan-Reviewer 對 contract-breaking
issue 必須回傳 `needs-rework`；Planner 對 unresolved conflict 必須 route `blocked` 或
`human-check`，不可自行選擇方便的 interpretation。

## Boundaries

- 本文件不授權修改 `skills/**`、`.github/skills/**`、`.codex/skills/**`、
  `.github/agents/**` 或 `.codex/agents/**`；本 correction 的唯一狹義 `.codex` exception 是
  `.codex/agents/planner.toml` 與 `.codex/agents/implementer.toml`，不得擴及其他 `.codex/**` path。
- 本文件不把 planning baseline 或 planning-review approval 轉換成 implementation
  approval。
- 本文件不授權 product、BC、runtime、identity、provider 或 release work。
- 本文件不授權對 frozen legacy review logs 的 migration、reader、compatibility layer 或
  其他 topic 修改；這些只可由獨立 future policy topic 規劃。
