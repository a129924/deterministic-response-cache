# Topic Plan Contract

## Current correction contract

B6R9 -> R19 -> S15 -> T15 -> V15 -> Q15 是唯一 current contract；current state 是 R19_REVIEW_PENDING。
B6R9/R19 are non-subject；S15 alone modifies tests/test_observer_dispatcher_governance_contract.py and retains
direct imports。T15/V15 是唯一 S15..V15 evidence descendants；Q15 是 committed V15 後的 read-only actual
full-triple gate。

## Authority and required plan structure

Authority ordering 是 AGENTS.md、plan/agent-handoff-workflow.md、本文件、parent plan、parent step、current exact
review record、local planning skill。GOAL.md 是 project mission，不是 topic/phase authority；chat、branch、summary
與 .github/agents/** 不可補推 planning evidence，後者只作 frozen provenance。

每個 topic plan 必須依 canonical order 包含 Goal / Outcome、Scope、Locked Decisions、Boundaries / Exclusions、
Status / Allowed Transitions、Artifact Paths、Implementation Steps、Validation / Acceptance Checks、Reviewer Handoff、
Post-merge / release actions、Open Questions / Unresolved Items。Artifact Paths 是 executable contract：每個 path
都要有 exact path、write owner、decision authority 與 role；unlisted path 必須停止並返回 Planner。

## B6R9 review record contract

B6R9 admission 是 non-merge first-parent exact-seven baseline，seven paths 是 shared workflow/shared contract、
parent plan/spec/step、B6R9 plan/step。pre-admission planning artifacts 不得嵌入 B6R9/R19 SHA、tree SHA、blob SHA、
HEAD 或 review outcome。Independent Plan-Reviewer 只可在 B6R9 committed clean checkout 寫 R19；R19 的 exact
schema 如下，所有 seven reviewed_artifacts entries 必須存在且各自對應 admission blob：

~~~json
{"schema_version":"observer-dispatcher-governance.correction-b6r9-plan-review.v1","correction_id":"observer-dispatcher-governance/high/b6r9","review_kind":"correction-b6r9-plan","reviewed_commit_sha":"<full B6R9 SHA>","reviewed_tree_sha":"<full B6R9 tree SHA>","reviewed_artifacts":[{"path":"<one exact B6R9 planning path>","blob_sha":"<that path blob SHA>"}],"first_parent_admission":{"commit_sha":"<full B6R9 SHA>","parent_sha":"<full first-parent SHA>","non_merge":true,"exact_declared_paths":true,"name_status":["<one exact status-and-path entry per declared path>"]},"next_phase":"S15","effective_committed_state":"R19_COMPLETE_S15_NEXT","review_basis":"independent clean-checkout tree, seven-blob, and first-parent admission review","copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]},"verdict":"approved|needs-rework","blocking_issues":[],"timestamp":"<RFC 3339 timestamp>"}
~~~

These SHA/tree/blob/admission fields are post-admission facts only. An approved R19 is separately committed unchanged.
B6R9/R19 never set implementation_subject_sha; approved R19 records R19_COMPLETE_S15_NEXT and permits only S15.

Only approved R19 permits S15. S15 has one allowed implementation path; direct imports remain required and
importlib/__import__/sys.modules substitution is forbidden. S15 corrects only the expected structured tuples for raw
name-status lexical ordering: B6R9 implementation review-log precedes B6R9 tester-evidence. It retains actual-Git
full-triple and fail-closed requirements.

T15/V15 have the exact B6R9 evidence paths declared by the parent plan. V15 must identify the same S15 and passing
T15, prove non-merge S15 -> T15 -> V15, and prove named S15..V15 has exactly those two evidence paths in raw Git
lexical tuple order: review-log before tester-evidence. Q15 uses full explicit SHA input and real subprocess Git only;
no environment is skip/unverified, but partial/invalid/symbolic/nonexistent/merge/wrong-graph/range input fails closed.

## Planner preflight and boundaries

Planner reads only parent plan, parent step and approved R19. It selects candidate, phase, gate and next role; missing
evidence is blocked, candidate conflict is human-check, and only Planner routes bounded rework. Planning approval never
establishes execution approval. This contract grants no thread resolution, merge, release, post-merge, tag or summary.

## Frozen provenance

normal/recovery records and all B0–B6R8 / R1–R18 / S1–S14 / T1–T14 / V1–V14 / Q1–Q14 artifacts are frozen
nonrouting provenance. Q14's sole failure is raw git diff --name-status lexical ordering, to be addressed only by S15.
step-creator remains deferred.
