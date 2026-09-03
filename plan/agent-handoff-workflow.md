# Agent handoff workflow

## Current route

唯一 current route 是 `B6R13 -> R23 -> S17 -> T17 -> V17 -> Q17 -> thread-classification -> comment-resolve -> human-check`。
current correction 是 `observer-dispatcher-governance/high/b6r13`，state 是 `R23_REVIEW_PENDING`。B6R13/R23 都是
non-subject；只有 S17 建立 implementation subject，且完整 diff 只可修改 declared exact-fourteen allowlist。
B6R12/R22/S16-Q16、B6R10/R20 及更早 records 是 frozen predecessor provenance。

## Authority and roles

Authority ordering 是 AGENTS.md、本文件、plan/topic-plan-contract.md、parent plan、parent step、current exact
review record。GOAL.md 只描述 repository mission；chat、branch、summary 與 .github/agents/** 都不是 routing
authority，後者僅為 frozen provenance。

Observer 只讀盤點、派遣 Planner-selected role 與彙整 verdict。Planner 是 route/phase/gate 唯一 authority，不寫
artifact，且只可選擇已提交、明確 approved 的 current candidate record；未提交、隱含或 `needs-rework` record
一律不能 route。Plan-Creator 只寫 declared planning artifact，不能 refine/select/self-close candidate；
Plan-Reviewer 只審 committed baseline；Implementer 只做 approved bounded work；Tester 只寫 factual evidence；
Reviewer 只做 independent implementation verification 與 passed Q gate 後的 thread classification。`Reviewer`
不是 Human PR reviewer。Human-only actions 是 PR review、merge、release、post-merge、tag 與 final summary。

## Frozen B6R10 admission and gates

B6R10 是 non-merge、first-parent 的 exact-eleven planning baseline。admission 的 named diff 必須恰好各一次包含
以下十一個 paths：

1. `AGENTS.md`
2. `.agents/skills/plan-reviewer/SKILL.md`
3. `.agents/skills/plan-reviewer/checklist.md`
4. `.agents/skills/plan-reviewer/reference.md`
5. `plan/agent-handoff-workflow.md`
6. `plan/topic-plan-contract.md`
7. `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md`
8. `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md`
9. `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md`
10. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r10-plan.md`
11. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r10-step.md`

R20 只在 committed B6R10 clean checkout 審上述十一個 blob、reviewed tree 與 first-parent admission，並只寫
`plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r10-review-log.md`。R20 的 extended
record 必須完整記錄 candidate id、commit/tree、十一個 path/blob、first-parent admission、review basis、verdict、
blockers 與 Copilot triage。`needs-rework` 沒有 active candidate、next phase、subject 或 close authorization；只有
Independent Implementer 以單獨 evidence-only commit 原樣提交的 approved R20 可建立唯一 active candidate，effective
state 為 `R20_COMPLETE_S16_NEXT`，next phase 是 S16。B6R10/R20 均不得建立 implementation subject。

S16 是唯一 non-merge subject，保留測試的 direct imports；不得以 `importlib`、`__import__` 或 `sys.modules`
substitution 取代既有測試行為。S16 驗證 committed T16/V16 blob semantics：topology/path、同一完整 S16 SHA、T16
`passing` 與 V16 `APPROVED`。T16、V16 是唯一 linear non-merge S16 descendants，且 named Git diff 的 exact
evidence paths 與 lexical tuple order 必須以 B6R10 parent contract 為準。T16 必須如實記錄同一 S16 的完整 suite
結果；V16 只有在 passing T16 後才能審核 S16 與 topology。

Q16 只能在 V16 committed 後執行，為 actual full-triple、read-only Git gate；它只接受完整 explicit
`ODG_S16_SHA`、`ODG_T16_SHA`、`ODG_V16_SHA`，並以 real subprocess `git rev-parse`、`git rev-list` 與
`git diff --name-status` 驗證。三者皆 absent 是 explicit no-environment skip/unverified；partial、symbolic/HEAD、
nonexistent、merge、wrong graph 或 widened range 一律 fail closed。Q16 只可寫 B6R10 declared actual-gate
evidence-only close record；該 record 只授權 thread classification，永不授權 PR approval 或 merge。只有通過 Q16
後，獨立 Reviewer 才可對每一 PR thread 做 addressed-and-resolvable classification；未明確標記者不得 resolve。

## Frozen B6R10 deterministic evidence schema

所有 B6R10 T16/V16/Q16 evidence 是單一 JSON object，exact keys（含 nested object keys）是 contract；缺鍵、
多鍵、非 40 位 lowercase hexadecimal SHA、錯誤 enum、錯誤 path/blob/parent 或 cross-record subject mismatch 都
fail closed。T16 的 top-level keys 僅為 `schema_version`、`correction_id`、`phase`、`subject`、`test_run`、
`timestamp`；`subject` 僅為 `phase:S16`、`commit_sha`、`test_path`，`test_run` 僅為 `command`、
`status:passing`、`exit_code:0`。

V16 的 top-level keys 僅為 `schema_version`、`correction_id`、`phase`、`subject`、`tester_evidence`、`verdict`、
`blocking_issues`、`timestamp`。它必須以 committed T16 的 `commit_sha`、`path`、`blob_sha`、S16 subject SHA 和
`status:passing` 綁定同一 S16；`verdict` 必為 uppercase `APPROVED`，`blocking_issues` 必為 `[]`。

Q16 的 top-level keys 僅為 `schema_version`、`correction_id`、`phase`、`artifacts`、`parsed_claims`、
`actual_git`、`close_authorization`、`timestamp`。`artifacts` 的 S16/T16/V16 每個 entry 都恰有 committed
`commit_sha`、`parent_sha`、`path`、`blob_sha`；`parsed_claims` 恰綁同一 S16、`passing`、`APPROVED`；`actual_git`
恰記 explicit full triple、linear、`S16..V16` range 及 name-status。`close_authorization` 只能宣告
`ACTIVE_CANDIDATE_CLOSED` 與 classification permitted，並明列 thread resolve、Human review、merge、release、
post-merge forbidden。Q16 不得記載其自身 commit/tree/blob。Reviewer 只可在 V16 committed 後寫 Q16；獨立
Implementer 原樣以 sole evidence-only commit 提交後，該 close record 才 active。

## B6R13 admission and gates

B6R13 is a non-merge, first-parent exact-eight planning baseline. The admission named diff contains exactly once:
`AGENTS.md`, `plan/agent-handoff-workflow.md`, `plan/topic-plan-contract.md`, parent plan/spec/step, and B6R13 plan/step.
Pre-admission artifacts contain no B6R13/R23 commit, tree, blob, HEAD, or outcome claim. R23 reviews only a committed
clean B6R13 checkout and writes only `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r13-review-log.md`.
It records candidate id, committed revision/tree, eight path/blob facts, first-parent admission, predecessor receipt,
review basis, Copilot triage, verdict and blockers. `needs-rework` has no active candidate, next phase, subject or close
authorization. Only an independent Implementer committing an unchanged approved R23 activates `R23_COMPLETE_S17_NEXT`
with next phase S17.

S17 exact allowlist is only these fourteen paths:

1. `.codex/agents/planner.toml`
2. `.codex/agents/implementer.toml`
3. `.codex/agents/reviewer.toml`
4. `.codex/agents/tester.toml`
5. `.agents/skills/plan-creator/SKILL.md`
6. `.agents/skills/plan-creator/checklist.md`
7. `.agents/skills/plan-creator/templates/topic-plan-template.md`
8. `.agents/skills/plan-reviewer/SKILL.md`
9. `.agents/skills/plan-reviewer/checklist.md`
10. `.agents/skills/plan-reviewer/reference.md`
11. `.agents/skills/plan-reviewer/examples.md`
12. `.agents/skills/python-implementation-workflow/SKILL.md`
13. `.agents/skills/python-plan-authoring/templates/canonical-python-topic-plan-template.md`
14. `tests/test_observer_dispatcher_governance_contract.py`

S17 must make Planner bootstrap exactly once with no later Planner next-role, Plan-Creator the sole planning writer,
Tester independent/factual with actual exit code, Reviewer dependent on same-subject passing Tester evidence, Implementer
bounded and never merge, and Explorer bounded read-only. The generic/Python templates must preserve these boundaries and
conditional release transition. Direct imports remain direct; `importlib`, `__import__`, and `sys.modules` substitution
is forbidden. T17 and V17 are new B6R13 evidence paths and sole non-merge S17 descendants. Q17 is post-V17 actual
full-SHA triple/read-only evidence, authorizes classification only, and never authorizes comment resolution, PR approval,
merge, release or post-merge. Only an independent per-thread classification may mark an exact thread
`addressed-and-resolvable`; only then may an Implementer leave the bounded reply and resolve it.

## Frozen provenance

normal/recovery records、B0–B6R9、R1–R19、S1–S15、T1–T15、V1–V15、Q1–Q15 與所有較早 correction artifacts 都是
immutable frozen nonrouting predecessor provenance；不得作 current routing、subject、gate、next-phase 或 Planner
authority。Q14 的唯一失敗是 raw `git diff --name-status` lexical ordering assertion；它不是 thread-resolution
authority。step-creator 仍 deferred。

## Human boundary

缺 required evidence 是 blocked；candidate conflict 是 human-check；contract drift 保守回 Planner。Ready for
review 不等於 merge approval。merge、release、post-merge、tag 與 final summary 一律停在 Human boundary。
