# Topic Plan Contract

## Purpose

定義 repo-visible topic plan 的 authority、required structure、planning evidence 與 preflight
contract。本文件不取代 `AGENTS.md`、`plan/agent-handoff-workflow.md` 或個別 topic plan 的 locked scope。

## Authority Ordering

1. `AGENTS.md`
2. `plan/agent-handoff-workflow.md`
3. `plan/topic-plan-contract.md`
4. `plan/<topic>/<topic>.plan.md`
5. `plan/<topic>/<topic>.step.md`
6. `plan/<topic>/<topic>.review-log.md`，或 current correction route 明定的 exact review path
7. local planning skill guidance

`GOAL.md` 是 project mission，非 topic / phase authority。chat、branch、summary、
`.github/agents/**` 不可補推 planning evidence；`.github/agents/**` 僅為 frozen provenance。

## Required Topic-Plan Sections

每個 topic plan 依 canonical order 包含：`Goal / Outcome`、`Scope`、`Locked Decisions`、
`Boundaries / Exclusions`、`Status / Allowed Transitions`、`Artifact Paths`、
`Implementation Steps`、`Validation / Acceptance Checks`、`Reviewer Handoff`、
`Post-merge / release actions`、`Open Questions / Unresolved Items`。非 stable-library topic
必須明示 non-stable intent；影響 stable-library surface 必須另列 metadata/timing。

## Planning Baseline, Evidence, and Preflight

### Ordinary planning evidence

Plan-Creator 寫 planning artifacts 但不得 commit；已有 Human authorization 時，獨立
Implementer 可作 bounded planning commit，這不表示 implementation approval。future/new ordinary
`review-log.md` 是 chronological NDJSON，最後 nonblank object 必須符合 `Reviewer Handoff`
schema 且 verdict 為 `approved`。legacy logs 保持 frozen provenance，不得遷移、重讀或以格式
不符使其失效。

### Current-topic B4R3 correction route

本節僅適用 `observer-dispatcher-governance`。`0800dc11181cdbd7d93d85e0298ea78dc33d06d3` 已提交
B4R2，但其 clean-checkout planning review 為 failed；B4R2 及其 review 是 frozen nonrouting
history。B0、B1、B2、B3、B4、B4R、B4R2、S1–S4、T1–T4、V1–V4、normal/recovery records，及其
plan、step、review、schema、blocker、checklist 與 pending semantics 全部不得作為 candidate、gate、
subject、evidence source 或 current work。兩個 `step-creator` threads 維持 deferred。

`B4R3` 是唯一 current pre-subject route，且 planning baseline 僅可包含下列七個 paths：

1. `plan/agent-handoff-workflow.md`
2. `plan/topic-plan-contract.md`
3. `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md`
4. `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md`
5. `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md`
6. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r3-plan.md`
7. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r3-step.md`

An Independent Implementer commits exactly these seven paths as non-subject `B4R3`. From a clean
checkout of the committed B4R3 SHA, an Independent Plan-Reviewer reviews actual blobs and writes only
`plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r3-review-log.md`.
An Independent Implementer separately commits that unchanged approved record. Neither B4R3 commit
can establish `implementation_subject_sha`.

Only the separately committed approved B4R3 review record permits one non-merge `S5`. S5 alone
establishes `implementation_subject_sha` and may change only the exact preserved 15-path allowlist in
the parent plan. `T5` then `V5` are its sole linear, non-merge, evidence-only descendants. Actual
named SHA graph queries must prove `S5 -> T5 -> V5`; named `git diff --name-status S5..V5` must list
exactly the B4R3 T5/V5 evidence paths. `HEAD`, a merge, a third descendant, or textual topology
inference fails closed.

### Planner preflight

Planner reads only the current parent plan, parent step and exact current approved review record. It
selects candidate, phase, gate and next role. Missing evidence is `blocked`; multiple candidates or
conflict is `human-check`; only Planner routes bounded rework. Planning approval never sets the topic
execution status to `approved`.

## Artifact Path Rules

`Artifact Paths` 是 executable contract。每個 artifact 必須有 exact repo-visible path、write
owner、decision authority 與 role。write owner 不會取得 route、status、gate 或 lifecycle authority。
未列 path 停止並交 Planner；不得自行擴張。

## Topic-Plan Contract Rules

`Implementation Steps` 僅描述 locked implementation work，不得混入 verdict、routing、reviewer
acceptance 或 human-only action。`Reviewer Handoff` 必須嵌入 fixed machine JSON schema；special
correction evidence 必須明示 exact path、ownership 與 gate。merge、post-merge、release 留在 Human
boundary。

## Reviewer Handoff

ordinary future/new review record:

```json
{"reviewed_artifacts":[{"path":"<exact repo-visible path>","revision":"<revision>"}],"review_basis":"<independent review basis>","verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]},"timestamp":"<RFC 3339 timestamp>"}
```

### B4R3 correction evidence schemas

Only these B4R3 records are current correction evidence. Each exact evidence file contains one
complete JSON object and no trailing prose. Tester records factual results only; Tester/Reviewer
cannot route lifecycle or status.

```json
{"schema_version":"observer-dispatcher-governance.correction-b4r3-plan-review.v1","correction_id":"observer-dispatcher-governance/high/b4r3","review_kind":"correction-b4r3-plan","severity":"high","reviewed_commit_sha":"<committed B4R3 SHA>","reviewed_artifacts":[{"path":"<one exact B4R3 planning path>","blob_sha":"<B4R3 blob SHA>"}],"review_basis":"<independent clean-checkout tree/blob review basis>","verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]},"timestamp":"<RFC 3339 timestamp>"}
```

The B4R3 review record contains each seven B4R3 planning paths exactly once. An approved record must be
separately committed unchanged before S5; `needs-rework` returns only to Planner.

```json
{"schema_version":"observer-dispatcher-governance.correction-b4r3-tester-evidence.v1","correction_id":"observer-dispatcher-governance/high/b4r3","actor":"Tester","implementation_subject_sha":"<S5 SHA>","subject_verification":{"expected_sha":"<S5 SHA>","observed_sha":"<S5 SHA>","command":"<exact command>","result":"passing|failing"},"commands":[{"command":"<exact command>","exit_code":0,"result":"passing|failing"}],"correction_test_result":"passing|failing","repository_validation_result":"passing|failing","verdict":"passing|failing","timestamp":"<RFC 3339 timestamp>"}
```

```json
{"schema_version":"observer-dispatcher-governance.correction-b4r3-implementation-review.v1","correction_id":"observer-dispatcher-governance/high/b4r3","review_kind":"correction-b4r3-implementation","severity":"high","implementation_subject_sha":"<S5 SHA>","review_target_commit_sha":"<pre-existing T5 SHA>","tester_evidence":{"path":"plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r3-tester-evidence.md","revision":"<T5 SHA>","implementation_subject_sha":"<S5 SHA>","verdict":"passing"},"reviewed_artifacts":[{"path":"<one exact S5 allowlist path>","revision":"<S5 revision>"}],"review_basis":"<independent implementation review basis including named SHA graph queries>","verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]},"timestamp":"<RFC 3339 timestamp>"}
```

V5 is authored before its own commit and cannot contain, require or infer a V5 SHA. Post-commit
validation independently identifies V5 and proves named actual-SHA non-merge `S5 -> T5 -> V5`.
`git diff --name-status S5..V5` lists exactly:

1. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r3-tester-evidence.md`
2. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r3-implementation-review-log.md`

## Blocking Semantics

Missing B4R3 evidence, non-approved B4R3 review, any path outside the seven-path B4R3 baseline or
15-path S5 allowlist, a frozen epoch as current evidence, a subject other than S5, wrong T5/V5 path,
merge, third descendant, `HEAD` substitution, or a range other than named `S5..V5` is
contract-breaking. Plan-Reviewer returns `needs-rework`; Planner routes `blocked` or `human-check`
for unresolved conflict.

## Boundaries

本文件不授權修改未列 paths，也不授權 PR thread action、merge、post-merge、release、tag 或
summary。Observer only dispatches Planner; Planner is routing authority; Plan-Creator authors planning
artifacts; Implementer performs bounded implementation/commits; Tester and Reviewer independently
write only declared evidence.
