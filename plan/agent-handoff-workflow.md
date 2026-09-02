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

## Frozen provenance

`b900366`、normal/recovery records、B0–B5R（含 R8/R9）、S1–S7、T1–T7、V1–V7、Q7，及所有較早
correction artifacts 均為 immutable historical provenance；僅保留追溯用途，排除於 B6 route。
`step-creator` work 維持 deferred。

## Current B6 route

`B6 -> R10 -> S8 -> T8 -> V8 -> Q8 -> comment-classification/human-check` 是唯一 current route。

B6 是 non-subject、non-merge 的七-path planning baseline。其 first-parent named diff 必須只含以下
paths，各一次：

1. `plan/agent-handoff-workflow.md`
2. `plan/topic-plan-contract.md`
3. `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md`
4. `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md`
5. `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md`
6. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6-plan.md`
7. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6-step.md`

Pre-commit B6 planning artifacts 不得嵌入 B6 SHA、blob SHA、`HEAD` 或 review outcome。Independent
Plan-Reviewer 只在 committed B6 clean checkout 審全部七 blobs，並寫唯一 R10：
`plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6-review-log.md`。
Independent Implementer 必須另以 evidence-only commit 提交 unchanged approved R10。B6/R10 都不得建立
`implementation_subject_sha`。

只有 approved R10 可以開始 one non-merge S8；S8 complete diff 只可修改
`tests/test_observer_dispatcher_governance_contract.py`。Direct imports 維持 mandatory，禁止 `importlib`、
`__import__` 與 `sys.modules` substitution。S8 的 actual Git assertion 只可使用完整 explicit
`ODG_S8_SHA`/`ODG_T8_SHA`/`ODG_V8_SHA` triple 和真實 subprocess `git rev-parse`、`git rev-list`、
`git diff --name-status`。三值全 absent 時必須明確 `skip`/`unverified`；部分值、`HEAD`、不存在 revision、
merge、wrong parent/graph 或 multi-path range 都必須 fail closed。

T8、V8 是唯一 linear、non-merge 的 S8 descendants。Tester 只寫
`plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6-tester-evidence.md`；
Reviewer 只寫
`plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6-implementation-review-log.md`。
Named `git diff --name-status S8..V8` 必須只列這兩個 paths。T8 必須用 complete real triple 執行
actual assertion 並記錄 non-skipped passing result；V8 在自身 commit 前撰寫且僅在 same-S8 passing T8 後
撰寫。

Q8 只可在 V8 commit 後，以 committed full V8 SHA 執行 read-only actual query。Q8 不得建立 artifact、
不得使用或推論 `HEAD`、不得 routing lifecycle、不得 resolve PR threads。

## Gates and human boundary

缺少 required evidence 為 `blocked`；candidate conflict 為 `human-check`；contract drift 保守回到
Planner。Ready for review 不是 merge approval。comment classification 僅能由獨立 Reviewer 在 Q8 後執行；
thread resolution 需要該 Reviewer 對每一 thread 明確標記 `addressed-and-resolvable`。merge、release、
post-merge 與 final summary 均為 Human boundary。
