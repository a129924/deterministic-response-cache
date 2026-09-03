# Agent handoff workflow

## Current route

唯一 current route 是 B6R9 -> R19 -> S15 -> T15 -> V15 -> Q15 -> thread-classification -> human-check。
current correction 是 observer-dispatcher-governance/high/b6r9，state 是 R19_REVIEW_PENDING。B6R9 與 R19 都是
non-subject；只有 S15 建立 implementation subject，且完整 diff 只可修改
tests/test_observer_dispatcher_governance_contract.py。

## Authority and roles

Authority ordering 是 AGENTS.md、本文件、plan/topic-plan-contract.md、parent plan、parent step、current exact
review record。GOAL.md 只描述 repository mission；chat、branch、summary 與 .github/agents/** 都不是 routing
authority，後者僅為 frozen provenance。

Observer 只讀盤點、派遣 Planner-selected role 與彙整 verdict。Planner 是 route/phase/gate 唯一 authority，不寫
artifact。Plan-Creator 只寫 declared planning artifact；Plan-Reviewer 只審 committed baseline；Implementer 只做
approved bounded work；Tester 只寫 factual evidence；Reviewer 只做 independent implementation review 與 thread
classification。Human-only actions 是 review、merge、release、post-merge、tag 與 final summary。

## B6R9 admission and gates

B6R9 是 non-merge、first-parent 的 exact-seven planning baseline。admission 的 named diff 必須恰好各一次包含以下
七個 paths：

1. plan/agent-handoff-workflow.md
2. plan/topic-plan-contract.md
3. plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md
4. plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md
5. plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md
6. plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r9-plan.md
7. plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r9-step.md

R19 只在 committed B6R9 clean checkout 審上述七個 blob、reviewed tree 與 first-parent admission，並只寫
plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r9-review-log.md。approved R19
必須由 Independent Implementer 以單獨 evidence-only commit 原樣提交；B6R9/R19 均不得建立
implementation_subject_sha。approved committed R19 的 effective state 是 R19_COMPLETE_S15_NEXT，next phase
是 S15。

S15 是唯一 non-merge subject，保留測試的 direct imports；不得以 importlib、__import__ 或 sys.modules
substitution 取代既有測試行為。其唯一 semantic correction 是將 raw git diff --name-status 的預期結果改為
structured tuple sequence，依 lexical path order 要求 implementation review-log 在 tester-evidence 之前；不得
改動 actual-Git、skip 或 fail-closed 語意。

T15、V15 是唯一 linear non-merge S15 descendants，且 named git diff --name-status S15..V15 只能列（依 raw
Git lexical order）：

1. plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r9-implementation-review-log.md
2. plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r9-tester-evidence.md

T15 必須如實記錄同一 S15 的完整 suite 結果。V15 只有在 passing T15 後才能審核 S15 與 topology。Q15 只能在
V15 committed 後執行，為 read-only、no-artifact、no-lifecycle/no-thread-authority 的 actual Git gate：只接受完整
explicit ODG_S15_SHA、ODG_T15_SHA、ODG_V15_SHA，並以 real subprocess git rev-parse、git rev-list 與
git diff --name-status 驗證。三者皆 absent 是 explicit no-environment skip/unverified；partial、
symbolic/HEAD、nonexistent、merge、wrong graph 或 widened range 一律 fail closed。通過 Q15 後，才可由獨立
Reviewer 對每一 PR thread 做 addressed-and-resolvable classification；未明確標記者不得 resolve。

## Frozen provenance

normal/recovery records、B0–B6R8、R1–R18、S1–S14、T1–T14、V1–V14、Q1–Q14 與所有較早 correction artifacts 都是
immutable frozen nonrouting provenance；不得作 B6R9 routing、subject 或 gate authority。Q14 的唯一失敗是 raw diff
name-status lexical ordering assertion；它不是 thread-resolution authority。step-creator 仍 deferred。

## Human boundary

缺 required evidence 是 blocked；candidate conflict 是 human-check；contract drift 保守回 Planner。Ready for
review 不等於 merge approval。merge、release、post-merge、tag 與 final summary 一律停在 Human boundary。
