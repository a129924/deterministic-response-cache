# Topic Plan Contract

## Current correction contract

`B6R8 -> R18 -> S14 -> T14 -> V14 -> Q14` 是唯一 current contract；current state 是
`R18_REVIEW_PENDING`。B6R8/R18 are non-subject；S14 alone modifies
`tests/test_observer_dispatcher_governance_contract.py` and retains direct imports。T14/V14 是唯一
`S14..V14` evidence descendants；Q14 是 committed V14 後的 read-only actual full-triple gate。

## Authority and required plan structure

Authority ordering 是 `AGENTS.md`、`plan/agent-handoff-workflow.md`、本文件、parent plan、parent step、current
exact review record、local planning skill。 `GOAL.md` 是 project mission，不是 topic/phase authority；chat、branch、
summary 與 `.github/agents/**` 不可補推 planning evidence，`.github/agents/**` 只作 frozen provenance。

每個 topic plan 必須依 canonical order 包含：`Goal / Outcome`、`Scope`、`Locked Decisions`、
`Boundaries / Exclusions`、`Status / Allowed Transitions`、`Artifact Paths`、`Implementation Steps`、
`Validation / Acceptance Checks`、`Reviewer Handoff`、`Post-merge / release actions`、
`Open Questions / Unresolved Items`。Artifact Paths 是 executable contract：每個 path 都要有 exact path、write
owner、decision authority 與 role；unlisted path 必須停止並返回 Planner。

## B6R8 review record contract

B6R8 admission 是 non-merge first-parent exact-seven baseline，seven paths 是 shared workflow/shared contract、
parent plan/spec/step、B6R8 plan/step。pre-admission planning artifacts 不得嵌入 B6R8/R18 SHA、tree SHA、blob SHA、
`HEAD` 或 review outcome。Independent Plan-Reviewer 只可在 B6R8 committed clean checkout 寫 R18；R18 的 exact schema
如下，所有 seven `reviewed_artifacts` entries 必須存在且各自對應 admission blob：

```json
{"schema_version":"observer-dispatcher-governance.correction-b6r8-plan-review.v1","correction_id":"observer-dispatcher-governance/high/b6r8","review_kind":"correction-b6r8-plan","reviewed_commit_sha":"<full B6R8 SHA>","reviewed_tree_sha":"<full B6R8 tree SHA>","reviewed_artifacts":[{"path":"<one exact B6R8 planning path>","blob_sha":"<that path blob SHA>"}],"first_parent_admission":{"commit_sha":"<full B6R8 SHA>","parent_sha":"<full first-parent SHA>","non_merge":true,"exact_declared_paths":true,"name_status":["<one exact status-and-path entry per declared path>"]},"predecessor_receipt_verification":{"review_log_path":"plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r7-review-log.md","reviewed_commit_sha":"03d90755b378063a312e62f9eefbe31caa081981","receipt_commit_sha":"a7770348222049f1c8bb6a0ee67e3136f2f47c3f","verdict":"approved","non_merge":true,"first_parent":true},"next_phase":"S14","effective_committed_state":"R17_COMPLETE_S14_NEXT","review_basis":"independent clean-checkout tree, seven-blob, first-parent admission, and frozen predecessor receipt review","copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]},"verdict":"approved|needs-rework","blocking_issues":[],"timestamp":"<RFC 3339 timestamp>"}
```

The `reviewed_commit_sha`/`reviewed_tree_sha`/seven blobs/admission fields are post-admission facts only; no
pre-admission artifact may supply them. `predecessor_receipt_verification` is the frozen R17 receipt fact and must
verify the exact path, reviewed commit, approved receipt commit, verdict, non-merge and first-parent fields above.
An approved R18 is separately committed unchanged. B6R8/R18 never set `implementation_subject_sha`; an effective
committed approved R18 records `R17_COMPLETE_S14_NEXT` and permits only S14.

Only approved R18 permits S14. S14 has one allowed implementation path and must reject import substitution.
T14 and V14 have the exact B6R8 evidence paths declared by the parent plan. V14 must identify the same S14 and
passing T14, prove non-merge `S14 -> T14 -> V14`, and prove the named `S14..V14` range has exactly those two
evidence paths. Q14 uses full explicit SHA input and real subprocess Git only; no environment is skip/unverified,
but partial/invalid/symbolic/nonexistent/merge/wrong-graph/range input fails closed.

## Planner preflight and boundaries

Planner reads only parent plan, parent step and approved R18. It selects candidate, phase, gate and next role;
missing evidence is `blocked`, candidate conflict is `human-check`, and only Planner routes bounded rework. Planning
approval never establishes execution approval. This contract grants no thread resolution, merge, release,
post-merge, tag or summary action.

## Frozen provenance

normal/recovery records and all B0–B6R7 / R1–R17 / S1–S13 / T1–T13 / V1–V13 / Q1–Q13 artifacts are frozen
nonrouting provenance. B6R7 baseline `03d90755b378063a312e62f9eefbe31caa081981` and R17 approved receipt
`a7770348222049f1c8bb6a0ee67e3136f2f47c3f` are frozen receipt facts, not routing authority. `step-creator` remains deferred.
