# Agent handoff workflow

## Current route

唯一 current route 是 `B6R8 -> R18 -> S14 -> T14 -> V14 -> Q14 -> comment-classification/human-check`。
current correction 是 `observer-dispatcher-governance/high/b6r8`，state 是
`R18_REVIEW_PENDING`。B6R8 與 R18 都是 non-subject；只有 S14 建立 implementation subject，且完整
diff 只可修改 `tests/test_observer_dispatcher_governance_contract.py`。

## Authority and roles

Authority ordering 是 `AGENTS.md`、本文件、`plan/topic-plan-contract.md`、parent plan、parent step、current
exact review record。 `GOAL.md` 只描述 repository mission；chat、branch、summary 與 `.github/agents/**` 都不是
routing authority，後者僅為 frozen provenance。

Observer 只讀盤點、派遣 Planner-selected role 與彙整 verdict。Planner 是 route/phase/gate 唯一 authority，
不寫 artifact。Plan-Creator 只寫 declared planning artifact；Plan-Reviewer 只審 committed baseline；
Implementer 只做 approved bounded work；Tester 只寫 factual evidence；Reviewer 只做 independent
implementation review 與 thread classification。Human-only actions 是 review、merge、release、post-merge、tag
與 final summary。

## B6R8 admission and gates

B6R8 是 non-merge、first-parent 的 exact-seven planning baseline。admission 的 named diff 必須恰好各一次
包含以下七個 paths：

1. `plan/agent-handoff-workflow.md`
2. `plan/topic-plan-contract.md`
3. `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md`
4. `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md`
5. `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md`
6. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r8-plan.md`
7. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r8-step.md`

R18 只在 committed B6R8 clean checkout 審上述七個 blob、reviewed tree 與 first-parent admission，並只寫
`plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r8-review-log.md`。R18 也必須驗證
frozen R17 receipt：review log path 是
`plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r7-review-log.md`、reviewed baseline
commit 是 `03d90755b378063a312e62f9eefbe31caa081981`、approved receipt commit 是
`a7770348222049f1c8bb6a0ee67e3136f2f47c3f`，且 receipt 為 non-merge first-parent。approved R18 必須由
Independent Implementer 以單獨 evidence-only commit 原樣提交；B6R8/R18 均不得建立
`implementation_subject_sha`。effective committed R18 approved state 是 `R17_COMPLETE_S14_NEXT`，next phase 是 `S14`。

S14 是唯一 non-merge subject，保留測試的 direct imports；不得以 `importlib`、`__import__` 或 `sys.modules`
substitution 取代既有測試行為。T14、V14 是唯一 linear non-merge S14 descendants，且 named
`git diff --name-status S14..V14` 只能列：

1. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r8-tester-evidence.md`
2. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r8-implementation-review-log.md`

T14 必須如實記錄同一 S14 的完整 suite 結果。V14 只有在 passing T14 後才能審核 S14 與 topology。
Q14 只能在 V14 committed 後執行，為 read-only、no-artifact、no-lifecycle/no-thread-authority 的 actual
Git gate：只接受完整 explicit `ODG_S14_SHA`、`ODG_T14_SHA`、`ODG_V14_SHA`，並以 real subprocess
`git rev-parse`、`git rev-list` 與 `git diff --name-status` 驗證。三者皆 absent 是 explicit
no-environment `skip`/`unverified`；partial、symbolic/`HEAD`、nonexistent、merge、wrong graph 或 widened range
一律 fail closed。通過 Q14 後，才可由獨立 Reviewer 對每一 PR thread 做
`addressed-and-resolvable` classification；未明確標記者不得 resolve。

## Frozen provenance

normal/recovery records、B0–B6、B6R–B6R7、R1–R17、S1–S13、T1–T13、V1–V13、Q1–Q13 與所有較早 correction
artifacts 都是 immutable frozen nonrouting provenance；不得作 B6R8 routing、subject 或 gate authority。B6R7
baseline `03d90755b378063a312e62f9eefbe31caa081981` 與 R17 approved receipt
`a7770348222049f1c8bb6a0ee67e3136f2f47c3f` 只作 frozen receipt facts，不是 current route。
`step-creator` 仍 deferred。

## Human boundary

缺 required evidence 是 `blocked`；candidate conflict 是 `human-check`；contract drift 保守回 Planner。
Ready for review 不等於 merge approval。merge、release、post-merge、tag 與 final summary 一律停在 Human
boundary。
