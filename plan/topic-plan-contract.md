# Topic Plan Contract

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

`b900366`、normal/recovery records、B0–B5R（含 R8/R9）、S1–S7、T1–T7、V1–V7、Q7，及所有較早
correction artifacts 是 immutable historical provenance；只作追溯，排除於 B6 route。`step-creator`
work 維持 deferred。

## B6 correction contract

B6 是唯一 non-subject、non-merge seven-path planning baseline。其 named first-parent diff 必須恰好含：

1. `plan/agent-handoff-workflow.md`
2. `plan/topic-plan-contract.md`
3. `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md`
4. `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md`
5. `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md`
6. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6-plan.md`
7. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6-step.md`

Before admission, B6 planning artifacts contain no B6 SHA/blob SHA/`HEAD`/review outcome. Independent
Plan-Reviewer clean-checkout-reviews every B6 blob and writes only R10 at
`plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6-review-log.md`.
Independent Implementer separately commits unchanged approved R10. B6/R10 never create
`implementation_subject_sha`.

```json
{"schema_version":"observer-dispatcher-governance.correction-b6-plan-review.v1","correction_id":"observer-dispatcher-governance/high/b6","reviewed_commit_sha":"<B6 SHA>","reviewed_artifacts":[{"path":"<one exact B6 planning path>","blob_sha":"<B6 blob SHA>"}],"review_basis":"independent clean-checkout seven-blob review after exact first-parent admission","verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]},"timestamp":"<RFC 3339 timestamp>"}
```

Only approved R10 permits S8, the only non-merge implementation subject. S8 changes only
`tests/test_observer_dispatcher_governance_contract.py`, retains direct imports, and rejects `importlib`,
`__import__`, and `sys.modules` substitution. Its actual graph assertion uses only complete explicit
`ODG_S8_SHA`/`ODG_T8_SHA`/`ODG_V8_SHA` plus real subprocess `git rev-parse`, `git rev-list`, and
`git diff --name-status`. All absent values are an explicit `skip`/`unverified`; partial/invalid/`HEAD`/
nonexistent/merge/wrong-parent-or-graph/multi-path input fails closed.

T8 then V8 are S8's only linear non-merge evidence-only descendants. Named `git diff --name-status S8..V8`
contains exactly:

1. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6-tester-evidence.md`
2. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6-implementation-review-log.md`

```json
{"schema_version":"observer-dispatcher-governance.correction-b6-tester-evidence.v1","correction_id":"observer-dispatcher-governance/high/b6","actor":"Tester","implementation_subject_sha":"<S8 SHA>","subject_verification":{"expected_sha":"<S8 SHA>","observed_sha":"<S8 SHA>","command":"<exact command>","result":"passing|failing"},"actual_graph_assertion":{"environment":"complete-real-triple","result":"passing|failing","skipped":false},"commands":[{"command":"<exact command>","exit_code":0,"result":"passing|failing"}],"verdict":"passing|failing","timestamp":"<RFC 3339 timestamp>"}
```

```json
{"schema_version":"observer-dispatcher-governance.correction-b6-implementation-review.v1","correction_id":"observer-dispatcher-governance/high/b6","review_kind":"correction-b6-implementation","implementation_subject_sha":"<S8 SHA>","review_target_commit_sha":"<pre-existing T8 SHA>","tester_evidence":{"path":"plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6-tester-evidence.md","revision":"<T8 SHA>","implementation_subject_sha":"<S8 SHA>","verdict":"passing"},"reviewed_artifacts":[{"path":"tests/test_observer_dispatcher_governance_contract.py","revision":"<S8 SHA>"}],"review_basis":"independent implementation review with named actual-SHA graph queries","verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]},"timestamp":"<RFC 3339 timestamp>"}
```

V8 is authored before its own commit; post-commit validation independently identifies V8 and verifies named
actual-SHA non-merge `S8 -> T8 -> V8` with the exact range. Q8 uses committed full V8 SHA only; it is
read-only, writes no artifact and has no lifecycle or thread authority.

## Planner preflight

Planner reads only current parent plan, parent step and exact current approved review record. It selects
candidate, phase, gate and next role. Missing evidence is `blocked`; multiple candidates or conflict is
`human-check`; only Planner routes bounded rework. Planning approval never sets execution status to `approved`.

## Artifact path rules and boundaries

`Artifact Paths` are executable contracts: every artifact has exact repo-visible path, write owner, decision
authority and role. Unlisted paths stop and return to Planner. This document grants no PR thread action,
merge, post-merge, release, tag or summary.
