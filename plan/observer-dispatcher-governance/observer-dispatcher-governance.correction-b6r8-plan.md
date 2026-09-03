# Observer / Dispatcher Governance — B6R8 Correction Plan

`B6R8 -> R18 -> S14 -> T14 -> V14 -> Q14` is the sole current route. B6R8/R18 are non-subject; S14 alone changes
`tests/test_observer_dispatcher_governance_contract.py`, preserves direct imports, and proves temporal frozen
provenance/current-route/subject/topology semantics. B6R8 admission is a non-merge first-parent exact-seven baseline:
the five canonical planning paths plus this plan and this step. This pre-admission artifact contains no B6R8/R18
revision, tree SHA, blob SHA, `HEAD`, or review outcome.

The B6R7 baseline `03d90755b378063a312e62f9eefbe31caa081981` and R17 approved receipt
`a7770348222049f1c8bb6a0ee67e3136f2f47c3f` are frozen predecessor receipt facts only; they do not route this epoch.

## Matrix

| Phase | Path | Writer | Gate |
| --- | --- | --- | --- |
| R18 | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r8-review-log.md` | Plan-Reviewer | committed B6R8 exact-seven baseline and R17 receipt verification |
| S14 | `tests/test_observer_dispatcher_governance_contract.py` | Implementer | approved committed R18 |
| T14 | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r8-tester-evidence.md` | Tester | same-S14 full suite |
| V14 | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r8-implementation-review-log.md` | Reviewer | passing T14 |
| Q14 | no written path | Reviewer | committed V14/full explicit actual triple |

T14 records factual same-S14 full-suite result. V14 proves only structural non-merge `S14 -> T14 -> V14` and exact
`S14..V14` two-evidence range, whose only paths are the B6R8 T14/V14 paths above. Q14 is post-V14, no-artifact,
read-only actual gate using complete explicit `ODG_S14_SHA`/`ODG_T14_SHA`/`ODG_V14_SHA` and subprocess Git. All-absent
input is no-environment skip/unverified; partial/invalid/symbolic/nonexistent/merge/wrong graph/range is fail closed.
No thread action occurs before passed Q14 and independent classification.

## R18 Schema

```json
{"schema_version":"observer-dispatcher-governance.correction-b6r8-plan-review.v1","correction_id":"observer-dispatcher-governance/high/b6r8","review_kind":"correction-b6r8-plan","reviewed_commit_sha":"<full B6R8 SHA>","reviewed_tree_sha":"<full B6R8 tree SHA>","reviewed_artifacts":[{"path":"<one exact B6R8 planning path>","blob_sha":"<that path blob SHA>"}],"first_parent_admission":{"commit_sha":"<full B6R8 SHA>","parent_sha":"<full first-parent SHA>","non_merge":true,"exact_declared_paths":true,"name_status":["<one exact status-and-path entry per declared path>"]},"predecessor_receipt_verification":{"review_log_path":"plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r7-review-log.md","reviewed_commit_sha":"03d90755b378063a312e62f9eefbe31caa081981","receipt_commit_sha":"a7770348222049f1c8bb6a0ee67e3136f2f47c3f","verdict":"approved","non_merge":true,"first_parent":true},"next_phase":"S14","effective_committed_state":"R17_COMPLETE_S14_NEXT","review_basis":"independent clean-checkout tree, seven-blob, first-parent admission, and frozen predecessor receipt review","copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]},"verdict":"approved|needs-rework","blocking_issues":[],"timestamp":"<RFC 3339 timestamp>"}
```

R18 writes post-admission facts only: one reviewed commit/tree, exactly seven path/blob entries, the B6R8
first-parent admission result, and exact R17 predecessor receipt verification. B6R8/R18 never write
`implementation_subject_sha`. An approved committed R18 has effective state `R17_COMPLETE_S14_NEXT` and next phase
S14.
