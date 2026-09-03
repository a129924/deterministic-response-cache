# Observer / Dispatcher Governance — B6R6 Correction Plan

`B6R6 -> R16 -> S14 -> T14 -> V14 -> Q14` is the sole current route. B6R6/R16 are non-subject; only S14 changes
`tests/test_observer_dispatcher_governance_contract.py`, preserves direct imports, and proves frozen provenance,
sole subject and sole topology. B6R6 admission is a non-merge first-parent exact-seven baseline: shared workflow,
shared contract, parent plan/spec/step, this plan and this step. This pre-admission artifact contains no baseline
revision values or review outcome. B6R5 and older work are frozen nonrouting provenance; `step-creator` deferred.

## Matrix

| Phase | Path | Writer | Gate |
| --- | --- | --- | --- |
| R16 | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r6-review-log.md` | Plan-Reviewer | committed exact-seven baseline |
| S14 | `tests/test_observer_dispatcher_governance_contract.py` | Implementer | approved R16 |
| T14 | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r6-tester-evidence.md` | Tester | same-S14 passing suite |
| V14 | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r6-implementation-review-log.md` | Reviewer | passing T14 |
| Q14 | no written path | Reviewer | committed V14/full explicit actual triple |

T14 truthfully records full suite plus one no-environment skip/unverified; V14 proves structural exact range only.
Q14 is post-V14 read-only non-skipped actual Git gate using explicit `ODG_S14_SHA`/`ODG_T14_SHA`/`ODG_V14_SHA` through
subprocess Git. Partial/invalid/symbolic/nonexistent/merge/wrong graph/range fails closed. No thread resolution occurs
before passed Q14 and independent classification.

## Schemas

```json
{"schema_version":"observer-dispatcher-governance.correction-b6r6-plan-review.v1","correction_id":"observer-dispatcher-governance/high/b6r6","reviewed_commit":"post-admission value","reviewed_tree":"post-admission value","reviewed_artifacts":[{"path":"declared path","blob":"post-admission value"}],"first_parent_admission":{"non_merge":true,"exact_declared_paths":true},"verdict":"approved|needs-rework","blocking_issues":[],"timestamp":"RFC3339"}
```
```json
{"schema_version":"observer-dispatcher-governance.correction-b6r6-tester-evidence.v1","implementation_subject_ref":"S14","full_suite":{"result":"passing|failing"},"actual_graph_assertion":{"environment":"no-env|complete-real-triple","result":"skip|unverified|passing|failing"},"commands":[],"verdict":"passing|failing","timestamp":"RFC3339"}
```
```json
{"schema_version":"observer-dispatcher-governance.correction-b6r6-implementation-review.v1","implementation_subject_ref":"S14","tester_evidence":{"path":"T14 evidence","result":"passing"},"topology":{"non_merge":true,"exact_range":"S14..V14","exact_evidence_paths":true},"reviewed_artifacts":["tests/test_observer_dispatcher_governance_contract.py"],"verdict":"approved|needs-rework","blocking_issues":[],"timestamp":"RFC3339"}
```
