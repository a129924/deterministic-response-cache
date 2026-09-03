# Observer / Dispatcher Governance — B6R7 Correction Plan

`B6R7 -> R17 -> S14 -> T14 -> V14 -> Q14` is the sole current route. B6R7/R17 are non-subject; S14 alone changes
`tests/test_observer_dispatcher_governance_contract.py`, preserves direct imports, and proves temporal frozen
provenance/current-route/subject/topology semantics. B6R7 admission is a non-merge first-parent exact-seven baseline:
the five canonical planning paths plus this plan and this step. This pre-admission artifact contains no B6R7 revision,
blob SHA, `HEAD`, or review outcome.

## Matrix

| Phase | Path | Writer | Gate |
| --- | --- | --- | --- |
| R17 | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r7-review-log.md` | Plan-Reviewer | committed B6R7 exact-seven baseline |
| S14 | `tests/test_observer_dispatcher_governance_contract.py` | Implementer | approved R17 |
| T14 | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r7-tester-evidence.md` | Tester | same-S14 full suite |
| V14 | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r7-implementation-review-log.md` | Reviewer | passing T14 |
| Q14 | no written path | Reviewer | committed V14/full explicit actual triple |

T14 records factual same-S14 full-suite result. V14 proves only structural non-merge `S14 -> T14 -> V14` and exact
`S14..V14` two-evidence range. Q14 is post-V14, no-artifact, read-only actual gate using complete explicit
`ODG_S14_SHA`/`ODG_T14_SHA`/`ODG_V14_SHA` and subprocess Git. All-absent input is no-environment skip/unverified;
partial/invalid/symbolic/nonexistent/merge/wrong graph/range is fail closed. No thread action occurs before passed Q14
and independent classification.

## R17 Schema

```json
{"schema_version":"observer-dispatcher-governance.correction-b6r7-plan-review.v1","correction_id":"observer-dispatcher-governance/high/b6r7","review_kind":"correction-b6r7-plan","reviewed_commit_sha":"<full B6R7 SHA>","reviewed_tree_sha":"<full B6R7 tree SHA>","reviewed_artifacts":[{"path":"<one exact B6R7 planning path>","blob_sha":"<that path blob SHA>"}],"first_parent_admission":{"commit_sha":"<full B6R7 SHA>","parent_sha":"<full first-parent SHA>","non_merge":true,"exact_declared_paths":true,"name_status":["<one exact status-and-path entry per declared path>"]},"review_basis":"independent clean-checkout tree, seven-blob, and first-parent admission review","copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]},"verdict":"approved|needs-rework","blocking_issues":[],"timestamp":"<RFC 3339 timestamp>"}
```

R17 writes post-admission facts only: one reviewed commit/tree, exactly seven path/blob entries, and the B6R7
first-parent admission result. B6R7/R17 never write `implementation_subject_sha`.
