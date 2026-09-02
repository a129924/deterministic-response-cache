# Agent handoff workflow

## Purpose

定義 repo-visible topic workflow、角色權責、status transition 與 human boundary。本文件不取代
`AGENTS.md`、`plan/topic-plan-contract.md` 或個別 topic plan。

## Authority and role separation

Authority ordering 是 `AGENTS.md`、本文件、`plan/topic-plan-contract.md`、parent plan、parent step、
current exact review record。`GOAL.md` 僅描述 repository mission；chat、branch、summary 與
`.github/agents/**` 不可作 routing authority；`.github/agents/**` 是 frozen provenance。

Observer 只讀盤點、派遣 Planner-selected role 與彙整 verdict；不得改檔、commit、push、gate 計算、
thread triage、PR 或 merge。Planner 決定 candidate/phase/gate/next role，但不寫 artifact。Plan-Creator
只依 locked direction 寫 planning artifact；Plan-Reviewer 獨立審 committed baseline；Implementer 只作
approved bounded work；Tester 只寫 factual evidence；Reviewer 獨立 review/classify comments。Human-only
actions 為 human review、merge、release、post-merge、tagging 與 final summary。

## Frozen B5 provenance

Human 已對 `observer-dispatcher-governance` 授權 current-topic scope expansion。以下 B5 route 是 frozen
historical nonrouting provenance，不可作 candidate、gate、subject、evidence 或 pending work。
`b900366`、B0–B4R7、S1–S6、T1–T6、V1–V5、缺少的 V6、normal/recovery evidence、所有舊 correction
artifacts 與其 pending/checklist/schema 是 frozen historical nonrouting provenance；它們不可選擇
candidate、提供 gate、建立 subject、提供 evidence 或 routing。`step-creator` threads 維持 deferred。

B5 曾是 non-subject baseline。first B5 admission 為 non-merge，named first-parent exact
diff 只能含下列七個 planning paths：

1. `plan/agent-handoff-workflow.md`
2. `plan/topic-plan-contract.md`
3. `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md`
4. `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md`
5. `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md`
6. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b5-plan.md`
7. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b5-step.md`

Pre-commit B5 planning artifacts 不得嵌入 B5 SHA、blob SHA、`HEAD` 或 review outcome。Independent
Plan-Reviewer 在 committed B5 clean checkout 審全部七 blobs，僅寫 B5 R8 review record；Independent
Implementer 另以 evidence-only commit 提交 unchanged approved R8。B5/R8 都不得建立
`implementation_subject_sha`。

Only approved R8 permits one non-merge S7 subject, whose complete diff may change only
`tests/test_observer_dispatcher_governance_contract.py`. S7 retains direct imports and uses only a complete
explicit `ODG_S7_SHA`/`ODG_T7_SHA`/`ODG_V7_SHA` environment triple plus real subprocess `git rev-parse`,
`git rev-list`, and `git diff --name-status` queries. No triple is an explicit pytest skip, never a synthetic
pass. Missing/partial values, `HEAD`, nonexistent revisions, merge, wrong parent, or multi-path range fail
closed.

T7 then V7 are the sole linear non-merge evidence-only S7 descendants. After V7 commit, Q7 is a read-only
actual query using V7's full SHA; it creates no artifact, cannot infer/use `HEAD`, resolve threads, or route
lifecycle.

## Human-authorized current-topic B5R correction route

`B5`、缺少的 `R8`、B4R7/S6/T6、缺少的 V6 與所有更早 epoch 都是 frozen nonrouting provenance；
它們不可作 current、pending、candidate 或 gate。B5R 是唯一 current non-subject baseline，且其 admission
commit 必須為 non-merge，named first-parent exact diff 只能含下列七個 planning paths：

1. `plan/agent-handoff-workflow.md`
2. `plan/topic-plan-contract.md`
3. `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md`
4. `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md`
5. `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md`
6. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b5r-plan.md`
7. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b5r-step.md`

Pre-commit B5R planning artifacts 不得嵌入 B5R SHA、blob SHA、`HEAD` 或 review outcome。Independent
Plan-Reviewer 只在 committed B5R clean checkout 審全數七 blobs，並寫唯一 R9：
`plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b5r-review-log.md`。
Independent Implementer 必須另以 evidence-only commit 提交 unchanged approved R9；B5R/R9 都不得建立
`implementation_subject_sha`。

Only approved R9 permits one non-merge S7 subject, whose complete diff may change only
`tests/test_observer_dispatcher_governance_contract.py`; direct imports and deferred `step-creator` remain
mandatory/locked. The actual Git graph assertion reads only the complete explicit
`ODG_S7_SHA`/`ODG_T7_SHA`/`ODG_V7_SHA` triple through real subprocess `git rev-parse`, `git rev-list`, and
`git diff --name-status`. It may explicitly report `skip`/`unverified` only when all three inputs are absent;
partial input, `HEAD`, nonexistent revisions, merge, wrong parent/graph, or multi-path range fails closed.

T7 and V7 are the sole non-merge linear S7 descendants and write only, respectively:

1. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b5r-tester-evidence.md`
2. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b5r-implementation-review-log.md`

Named `git diff --name-status S7..V7` must list exactly those paths. T7 must exercise the actual assertion
with a complete real triple and record a non-skipped passing result. V7 is authored before its own commit.
Q7 remains post-V7, read-only, full-V7-SHA only, creates no artifact, and cannot resolve threads or route
lifecycle.

## Gates and human boundary

`B5R -> R9 -> S7 -> T7 -> V7 -> Q7 -> comment-classification/human-check` is the only route. Missing evidence
is `blocked`; candidate conflict is `human-check`; contract drift returns conservatively to Planner. Ready
for review is not merge approval. Q7/comment classification never authorizes resolving a thread or merging.
