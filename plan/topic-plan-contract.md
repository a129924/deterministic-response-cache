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

### Frozen B2 correction route

本 shared contract 不建立 generic legacy-log migration 或第二種一般 planning-review
evidence。Human 對 current topic `observer-dispatcher-governance` 的唯一 scope expansion
authorization 是：`2. 授權擴張 current topic。` 依此授權，唯一 current correction route
是 parent plan / spec / step 與 `correction-b2-plan.md` / `correction-b2-step.md` 在兩份 shared
contracts 下的 bounded combination；parent artifacts 保持 current execution truth，B2
correction artifacts 只保留 correction delta，不能升格為 parent。

`B0=8556d41282eb2388ff22e45623dd20052a2bf70f`、
`S1=f1a2ae1334b03ea0c5eea7612909ef77c089f38c`、
`T1=b96c484e78bdc1ea004c7629616f216657e64e07` 與
`V1=2b0e6fa653bb58537523ae4010945dadbab7b34e`、B1 與無效的
`correction-b1-review-log.md`，連同其 correction artifacts、old epoch
`R0=cb3f66c60e95e5580cb2b30632d0d5ed9f0d0ee9`、normal evidence 與 `recovery-*` evidence，
都是 frozen provenance；不能作為 current gate、current review、或新 `implementation_subject_sha`。

這是只適用 current topic 的狹義一次性 `B2` exception。normal planning-artifact-commit
prerequisite 在此例外中暫停：在任何 `S3` test-path 寫入前，independent Plan-Reviewer 可審閱
同一 working tree 的 verified Git tree object 與下列七個**未提交** B2 planning artifact 的 exact path/blob revision：

- `plan/agent-handoff-workflow.md`
- `plan/topic-plan-contract.md`
- `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md`
- `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md`
- `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md`
- `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b2-plan.md`
- `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b2-step.md`

Plan-Reviewer must build the reviewed tree using a temporary index seeded from `HEAD` and containing
only these seven changed paths; it must record the `git write-tree` result only after
`git rev-parse <tree>^{tree}` and `git cat-file -e <tree>^{tree}` succeed. Its path/blob revisions
must come from that tree, not a non-object working-tree identifier. Plan-Reviewer only owns its
independent verdict, not topic routing. After that reviewer writes the single schema-complete
`correction-b2-review-log.md`, an Independent Implementer under existing Human commit authorization
commits exactly that unchanged record plus those seven reviewed planning artifacts as `B2`. The
Implementer must then validate the retained record post-commit: its tree object exists; each of the
seven recorded blobs equals both `<reviewed_tree_sha>:<path>` and `<B2>:<path>`; and the exact
tree-to-`B2^{tree}` name-status diff lists only `correction-b2-review-log.md`. `B2` is not an
`implementation_subject_sha`. An `approved` `B2` permits only the declared test-path subject;
`needs-rework` keeps the topic in `needs-rework` and Planner decides bounded repair.

The subsequent non-merge `S3` must modify only
`tests/test_observer_dispatcher_governance_contract.py`; it is the replacement immutable
`implementation_subject_sha`. Only `T3` (Tester writes
`observer-dispatcher-governance.correction-b2-tester-evidence.md`) then `V3` (Reviewer writes
`observer-dispatcher-governance.correction-b2-implementation-review-log.md`) may descend from
`S3`. Both attest `S3`, the second references passing `T3`, and verification is exactly
`git diff --name-status S3..V3`; it must list only those two paths and never substitute `HEAD`.
This current-topic exception grants no current evidence write, commit, push, PR-thread action,
merge, post-merge, release, tagging or summary action, and cannot be generalized to another topic.

### Human-authorized current-topic B4 correction route

The B0–B3/S1–S4/T1–T4/V1–V4, normal/recovery and prior correction artifacts are frozen historical
provenance, never a candidate, gate, route or subject. The two `step-creator` threads are deferred.
The Human scope-expansion authorization `2. 授權擴張 current topic。` permits only B4: two shared
contracts, parent plan/spec/step, and correction-b4 plan/step.

An Independent Implementer commits exactly those seven paths as non-subject B4. From a clean
checkout at that B4 commit, an Independent Plan-Reviewer reviews the committed blobs and writes
only `correction-b4-review-log.md`; an Independent Implementer commits that unchanged review record
separately. B4 and its review-evidence commit are never subjects.

S5 is the sole immutable subject and may change only the exact 15-path allowlist in the parent plan.
T5 then V5 are the only linear non-merge evidence-only descendants. All verification uses actual
named commit SHA graph queries and exact `git diff --name-status S5..V5`; `HEAD` and textual topology
inference are invalid. Tester reports only factual `passing|failing`, without `next_gate`, routing or
lifecycle fields. Reviewer requires the same S5 SHA and passing exact T5 evidence path.

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

### Historical B2 correction evidence schemas (frozen provenance)

下列三個 JSON object 僅保留為已完成 B2 correction route 的 frozen provenance；每個
exact evidence path 只可含一個 object，不得附加 Markdown 或 prose。它們不改寫 generic future /
new review-log schema，也不追溯適用 frozen B0/S1/T1/V1、B1、legacy 或 recovery evidence。B1 的
review record 是 frozen invalid provenance，不能更新或重用。

先於 implementation 的 correction-plan review record 必須符合：

```json
{
  "schema_version": "observer-dispatcher-governance.correction-b2-plan-review.v1",
  "correction_id": "observer-dispatcher-governance/high/b2",
  "review_kind": "correction-b2-plan",
  "severity": "high",
  "routing_state": "PLANNER_REPLAN",
  "reviewed_tree_sha": "<verified Git tree object produced by temporary-index git write-tree>",
  "reviewed_artifacts": [
    {
      "path": "<one of the seven exact B2 planning paths>",
      "blob_sha": "<blob from reviewed_tree_sha for that path>"
    }
  ],
  "review_basis": "<independent correction-plan review basis and tree-object verification>",
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

`reviewed_artifacts` must contain each of the seven paths enumerated in the B2 route exactly once.
Before writing the record, Plan-Reviewer must use a temporary index seeded from `HEAD`, stage only
the seven B2 paths into that temporary index, run `git write-tree`, and verify the returned object
with both `git rev-parse <tree>^{tree}` and `git cat-file -e <tree>^{tree}`. Every recorded blob must
equal `git rev-parse <tree>:<path>`. Only Plan-Reviewer writes `correction-b2-review-log.md`; its
`approved` verdict is a precondition for the non-subject `B2` commit and then `S3`. After B2 is
committed, Independent Implementer must verify that tree still exists, every recorded blob equals
both the reviewed tree and `B2:<path>`, and the only name-status difference from reviewed tree to
`B2^{tree}` is the B2 review-log path. Planner still owns route and status decisions.

Tester evidence after the immutable implementation subject must conform to:

```json
{
  "schema_version": "observer-dispatcher-governance.correction-b2-tester-evidence.v1",
  "correction_id": "observer-dispatcher-governance/high/b2",
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
  "schema_version": "observer-dispatcher-governance.correction-b2-implementation-review.v1",
  "correction_id": "observer-dispatcher-governance/high/b2",
  "review_kind": "correction-b2-implementation",
  "severity": "high",
  "implementation_subject_sha": "<full immutable implementation commit SHA>",
  "reviewed_commit_sha": "<V3 commit SHA containing only the two allowed evidence descendants from S3>",
  "tester_evidence": {
    "path": "plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b2-tester-evidence.md",
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

### B4 correction evidence schemas

The following three single-JSON-object records are the only current correction evidence for this
topic. They are prospective B4 artifacts and do not rewrite frozen provenance.

```json
{
  "schema_version": "observer-dispatcher-governance.correction-b4-plan-review.v1",
  "correction_id": "observer-dispatcher-governance/high/b4",
  "review_kind": "correction-b4-plan",
  "severity": "high",
  "routing_state": "PLANNER_REPLAN",
  "reviewed_commit_sha": "<committed B4 SHA>",
  "reviewed_artifacts": [{"path": "<one exact B4 planning path>", "blob_sha": "<B4-commit blob SHA>"}],
  "review_basis": "<independent tree/blob review basis>",
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "copilot_feedback_triage": {"ADDRESS": [], "DISCUSS": [], "SKIP": []},
  "timestamp": "<RFC 3339 timestamp>"
}
```

`reviewed_artifacts` contains each of the seven B4 planning paths exactly once. The Plan-Reviewer
alone writes `correction-b4-review-log.md` from a clean B4 checkout; an approved record is committed
unchanged in a separate evidence-only commit.

```json
{
  "schema_version": "observer-dispatcher-governance.correction-b4-tester-evidence.v1",
  "correction_id": "observer-dispatcher-governance/high/b4",
  "actor": "Tester",
  "implementation_subject_sha": "<S5 SHA>",
  "subject_verification": {"expected_sha": "<S5 SHA>", "observed_sha": "<S5 SHA>", "command": "<exact command>", "result": "passing|failing"},
  "commands": [{"command": "<exact command>", "exit_code": 0, "result": "passing|failing"}],
  "correction_test_result": "passing|failing",
  "repository_validation_result": "passing|failing",
  "verdict": "passing|failing",
  "timestamp": "<RFC 3339 timestamp>"
}
```

```json
{
  "schema_version": "observer-dispatcher-governance.correction-b4-implementation-review.v1",
  "correction_id": "observer-dispatcher-governance/high/b4",
  "review_kind": "correction-b4-implementation",
  "severity": "high",
  "implementation_subject_sha": "<S5 SHA>",
  "review_target_commit_sha": "<pre-existing T5 SHA>",
  "tester_evidence": {"path": "plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4-tester-evidence.md", "revision": "<T5 SHA>", "implementation_subject_sha": "<S5 SHA>", "verdict": "passing"},
  "reviewed_artifacts": [{"path": "<exact declared path>", "revision": "<reviewed revision>"}],
  "review_basis": "<independent implementation review basis>",
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "copilot_feedback_triage": {"ADDRESS": [], "DISCUSS": [], "SKIP": []},
  "timestamp": "<RFC 3339 timestamp>"
}
```

The V5 record is written before the V5 commit and therefore must not contain, require, or infer a
V5 commit SHA. Post-commit validation independently identifies V5 and verifies exact non-merge
`S5 -> T5 -> V5` topology and `git diff --name-status S5..V5`. Tester evidence has no `next_gate`,
routing or lifecycle field.

## Blocking Semantics

下列情況是 contract-breaking：

- required section、required step tracker、exact artifact path 或 required planning
  evidence 缺失；
- status transition 無效；
- artifact path scope drift、undeclared stable-library intent 或錯誤 release timing；
- future / new review log 或已明定 special replan evidence 的 latest record 非有效 JSON、
  shape 不符、reviewed revision 未覆蓋 required latest artifact，或 verdict 非 `approved`；
- Historical B2 correction evidence defects remain frozen provenance and cannot become a current
  B3 gate. The current B3 correction review blocks if it is absent, not schema-complete, lacks a
  verified Git-object
  `reviewed_tree_sha` or one exact tree-derived path/blob revision for each of the seven declared
  uncommitted B3 planning artifacts, was not built from the prescribed temporary index, is not
  committed unchanged with exactly that reviewed set as non-subject `B3`, fails post-commit tree/blob
  validation, or is written after the `S4` test-path change begins;
- B3 correction Tester / Reviewer record 的 `implementation_subject_sha` 不存在、不相同、不是
  only-test-path `S4` completed implementation commit，或 correction descendant 不是
  `S4 -> T4 -> V4` linear / evidence-only chain，或 `git diff --name-status S4..V4` 不是恰好兩個
  declared B3 evidence paths，或以 `HEAD` 取代具名 `V4`，或 pre-commit V4 record 要求、包含或
  推定 V4 自身 SHA 而非 pre-existing `review_target_commit_sha = T4`；
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
