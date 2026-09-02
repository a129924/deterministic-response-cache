# Topic Plan Contract

> **B6R3 current-contract override:** 下列 B6R/B6R2 contract 文字均屬 frozen nonrouting provenance。唯一
> current contract 是 `B6R3 -> R13 -> S11 -> T11 -> V11 -> Q11`。B6R3 admission 只含
> `plan/agent-handoff-workflow.md`、`plan/topic-plan-contract.md`、parent plan/spec/step 與 B6R3 plan/step
> 七 paths，且 pre-commit 不含 B6R3 SHA/blob SHA/`HEAD`/review outcome。R13 只寫
> `observer-dispatcher-governance.correction-b6r3-review-log.md`；B6R3/R13 都非 subject。S11 only 改 test
> path，保留 direct imports，並以 complete `ODG_S11_SHA`/`ODG_T11_SHA`/`ODG_V11_SHA` 和 real subprocess
> git queries fail-closed 驗證。T11/V11 的 exact evidence-only range 為 `S11..V11`。Q11 是唯一 shared
> human boundary；Q8–Q10 不可作 human boundary、classification 或 resolution authority。

## Purpose

定義 repo-visible topic plan 的 authority、required structure、planning evidence 與 preflight contract。

## Authority ordering

1. `AGENTS.md`
2. `plan/agent-handoff-workflow.md`
3. 本文件
4. `plan/<topic>/<topic>.plan.md`
5. `plan/<topic>/<topic>.step.md`
6. current correction route 明定的 exact review path
7. local planning skill guidance

`GOAL.md` 是 project mission，非 topic / phase authority。chat、branch、summary 與
`.github/agents/**` 不可補推 planning evidence；`.github/agents/**` 僅為 frozen provenance。

## Required topic-plan sections

每個 topic plan 依 canonical order 包含：`Goal / Outcome`、`Scope`、`Locked Decisions`、
`Boundaries / Exclusions`、`Status / Allowed Transitions`、`Artifact Paths`、
`Implementation Steps`、`Validation / Acceptance Checks`、`Reviewer Handoff`、
`Post-merge / release actions`、`Open Questions / Unresolved Items`。非 stable-library topic 必須明示
non-stable intent。

## Frozen provenance

`b900366`、normal/recovery records、B0–B6（含 R8/R9/R10）、S1–S10、T1–T10、V1–V10、Q7–Q10，及所有較早
correction artifacts 是 immutable historical provenance；只作追溯，排除於 B6R3 route。`step-creator`
work 維持 deferred。

## Frozen B6R correction contract

B6R 是唯一 non-subject、non-merge seven-path planning baseline。其 named first-parent diff 必須恰好含：

1. `plan/agent-handoff-workflow.md`
2. `plan/topic-plan-contract.md`
3. `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md`
4. `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md`
5. `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md`
6. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r-plan.md`
7. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r-step.md`

Before admission, B6R planning artifacts contain no B6R SHA/blob SHA/`HEAD`/review outcome. Independent
Plan-Reviewer clean-checkout-reviews every B6R blob and writes only R11 at
`plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r-review-log.md`.
Independent Implementer separately commits unchanged approved R11. B6R/R11 never create
`implementation_subject_sha`. R11 records each reviewed artifact/blob and actual first-parent exact-seven
admission result.

```json
{"schema_version":"observer-dispatcher-governance.correction-b6r-plan-review.v1","correction_id":"observer-dispatcher-governance/high/b6r","reviewed_commit_sha":"<B6R SHA>","reviewed_artifacts":[{"path":"<one exact B6R planning path>","blob_sha":"<B6R blob SHA>"}],"first_parent_admission":{"non_merge":true,"exact_declared_paths":true,"name_status":"<exact seven path entries>"},"review_basis":"independent clean-checkout fields and first-parent seven-blob review","verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]},"timestamp":"<RFC 3339 timestamp>"}
```

Only approved R11 permits S9, the only non-merge implementation subject. S9 changes only
`tests/test_observer_dispatcher_governance_contract.py`, retains direct imports, and rejects `importlib`,
`__import__`, and `sys.modules` substitution. Its actual graph assertion uses only complete explicit
`ODG_S9_SHA`/`ODG_T9_SHA`/`ODG_V9_SHA` plus real subprocess `git rev-parse`, `git rev-list`, and
`git diff --name-status`. All absent values are an explicit `skip`/`unverified`; partial/invalid/`HEAD`/
nonexistent/merge/wrong-parent-or-graph/multi-path input fails closed.

T9 then V9 are S9's only linear non-merge evidence-only descendants. Named `git diff --name-status S9..V9`
contains exactly:

1. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r-tester-evidence.md`
2. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r-implementation-review-log.md`

```json
{"schema_version":"observer-dispatcher-governance.correction-b6r-tester-evidence.v1","correction_id":"observer-dispatcher-governance/high/b6r","actor":"Tester","implementation_subject_sha":"<S9 SHA>","subject_verification":{"expected_sha":"<S9 SHA>","observed_sha":"<S9 SHA>","command":"<exact command>","result":"passing|failing"},"actual_graph_assertion":{"environment":"complete-real-triple","result":"passing|failing","skipped":false},"commands":[{"command":"<exact command>","exit_code":0,"result":"passing|failing"}],"verdict":"passing|failing","timestamp":"<RFC 3339 timestamp>"}
```

```json
{"schema_version":"observer-dispatcher-governance.correction-b6r-implementation-review.v1","correction_id":"observer-dispatcher-governance/high/b6r","review_kind":"correction-b6r-implementation","implementation_subject_sha":"<S9 SHA>","review_target_commit_sha":"<pre-existing T9 SHA>","tester_evidence":{"path":"plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r-tester-evidence.md","revision":"<T9 SHA>","implementation_subject_sha":"<S9 SHA>","verdict":"passing"},"reviewed_artifacts":[{"path":"tests/test_observer_dispatcher_governance_contract.py","revision":"<S9 SHA>"}],"review_basis":"independent implementation review with named actual-SHA graph queries","verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]},"timestamp":"<RFC 3339 timestamp>"}
```

V9 is authored before its own commit; post-commit validation independently identifies V9 and verifies named
actual-SHA non-merge `S9 -> T9 -> V9` with the exact range. Q9 uses committed full V9 SHA only; it is
read-only, writes no artifact and has no lifecycle or thread authority.

## Planner preflight

Planner reads only current parent plan, parent step and exact current approved review record. It selects
candidate, phase, gate and next role. Missing evidence is `blocked`; multiple candidates or conflict is
`human-check`; only Planner routes bounded rework. Planning approval never sets execution status to `approved`.

## Artifact path rules and boundaries

`Artifact Paths` are executable contracts: every artifact has exact repo-visible path, write owner, decision
authority and role. Unlisted paths stop and return to Planner. This document grants no PR thread action,
merge, post-merge, release, tag or summary.
