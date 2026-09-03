# Observer / Dispatcher Governance — B6R9 Correction Plan

B6R9 -> R19 -> S15 -> T15 -> V15 -> Q15 is the sole current route. B6R9/R19 are non-subject; S15 alone changes
tests/test_observer_dispatcher_governance_contract.py, preserves direct imports, and makes only the Q14 raw
name-status lexical-order correction. B6R9 admission is a non-merge first-parent exact-seven baseline: the five
canonical planning paths plus this plan and this step. This pre-admission artifact contains no B6R9/R19 revision,
tree SHA, blob SHA, HEAD, or review outcome.

B6R8/Q14 and every prior record are frozen nonrouting provenance. Q14's sole failure is expected raw git diff
--name-status lexical ordering; it neither authorizes thread action nor reopens prior decisions.

## Matrix

| Phase | Path | Writer | Gate |
| --- | --- | --- | --- |
| R19 | plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r9-review-log.md | Plan-Reviewer | committed B6R9 exact-seven baseline |
| S15 | tests/test_observer_dispatcher_governance_contract.py | Implementer | approved committed R19 |
| T15 | plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r9-tester-evidence.md | Tester | same-S15 full suite |
| V15 | plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r9-implementation-review-log.md | Reviewer | passing T15 |
| Q15 | no written path | Reviewer | committed V15/full explicit actual triple |

T15 records factual same-S15 full-suite result. V15 proves only structural non-merge S15 -> T15 -> V15 and exact
S15..V15 two-evidence range. Raw Git tuples must be compared in lexical path order: B6R9 review-log before B6R9
tester-evidence. Q15 is post-V15, no-artifact, read-only actual gate using complete explicit
ODG_S15_SHA/ODG_T15_SHA/ODG_V15_SHA and subprocess Git. All-absent input is no-environment skip/unverified;
partial/invalid/symbolic/nonexistent/merge/wrong graph/range is fail closed. No thread action occurs before passed
Q15 and independent classification.

## R19 Schema

~~~json
{"schema_version":"observer-dispatcher-governance.correction-b6r9-plan-review.v1","correction_id":"observer-dispatcher-governance/high/b6r9","review_kind":"correction-b6r9-plan","reviewed_commit_sha":"<full B6R9 SHA>","reviewed_tree_sha":"<full B6R9 tree SHA>","reviewed_artifacts":[{"path":"<one exact B6R9 planning path>","blob_sha":"<that path blob SHA>"}],"first_parent_admission":{"commit_sha":"<full B6R9 SHA>","parent_sha":"<full first-parent SHA>","non_merge":true,"exact_declared_paths":true,"name_status":["<one exact status-and-path entry per declared path>"]},"next_phase":"S15","effective_committed_state":"R19_COMPLETE_S15_NEXT","review_basis":"independent clean-checkout tree, seven-blob, and first-parent admission review","copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]},"verdict":"approved|needs-rework","blocking_issues":[],"timestamp":"<RFC 3339 timestamp>"}
~~~

R19 writes post-admission facts only: one reviewed commit/tree, exactly seven path/blob entries, and B6R9 first-parent
admission result. B6R9/R19 never write implementation_subject_sha. An approved committed R19 has effective state
R19_COMPLETE_S15_NEXT and next phase S15.
