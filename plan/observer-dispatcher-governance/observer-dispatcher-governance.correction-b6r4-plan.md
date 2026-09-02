# Observer / Dispatcher Governance — B6R4 Correction Plan

## Canonical route

`B6R4 -> R14 -> S12 -> T12 -> V12 -> Q12` is the sole current route. B6R3/R13 and all older records are immutable frozen nonrouting provenance. B6R4 is a non-subject, non-merge first-parent planning baseline; its exact-seven admission is already committed. R14 independently reviews that committed baseline, and neither B6R4 nor R14 creates `implementation_subject_sha`.

The B6R4 admission changed exactly once each:

1. `plan/agent-handoff-workflow.md`
2. `plan/topic-plan-contract.md`
3. `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md`
4. `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md`
5. `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md`
6. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r4-plan.md`
7. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r4-step.md`

Before admission those files contain no actual B6R4 identity, blob identity, `HEAD`, or review outcome. R14 is written only after a clean-checkout review of the committed B6R4 tree, its seven named blobs, and its exact first-parent diff, then separately committed unchanged by an independent Implementer.

S12 is one non-merge subject modifying only `tests/test_observer_dispatcher_governance_contract.py`. It retains direct imports, rejects `importlib`, `__import__`, and `sys.modules` substitutions, and verifies exact provenance/subject/topology semantics through real subprocess Git queries using only complete explicit S12/T12/V12 environment SHAs. T12 then V12 are the sole exact evidence-only descendants; Q12 is committed-full-V12-SHA-only, read-only, and artifact-free.

## Full artifact matrix

| Phase | Exact path(s) | Writer | Authority | Required gate |
| --- | --- | --- | --- | --- |
| B6R4 | seven paths enumerated above | Plan-Creator, then Implementer | Planner | committed non-merge first-parent exact-seven |
| R14 | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r4-review-log.md` | Plan-Reviewer | independent review verdict | all B6R4 blobs/tree reviewed |
| S12 | `tests/test_observer_dispatcher_governance_contract.py` | Implementer | Planner after approved R14 | one non-merge subject, direct imports |
| T12 | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r4-tester-evidence.md` | Tester | factual result | complete real triple passes |
| V12 | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r4-implementation-review-log.md` | Reviewer | independent review verdict | same-S12 T12 and exact range |
| Q12 | no written path | Reviewer, read-only | Planner/human boundary | committed full V12 SHA only |

## R14 schema

```json
{"schema_version":"observer-dispatcher-governance.correction-b6r4-plan-review.v1","correction_id":"observer-dispatcher-governance/high/b6r4","review_kind":"correction-b6r4-plan-review","reviewed_commit_sha":"<B6R4 SHA>","reviewed_tree_sha":"<B6R4 tree SHA>","reviewed_artifacts":[{"path":"<one exact B6R4 planning path>","blob_sha":"<B6R4 blob SHA>"}],"first_parent_admission":{"candidate_parent_sha":"<B6R4 first parent SHA>","observed_parent_sha":"<B6R4 first parent SHA>","non_merge":true,"exact_declared_paths":true,"name_status":"<exact seven name-status entries>"},"review_basis":"independent clean-checkout fields, blobs, and first-parent seven-path review","verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]},"timestamp":"<RFC 3339 timestamp>"}
```

## T12 / V12 schemas

```json
{"schema_version":"observer-dispatcher-governance.correction-b6r4-tester-evidence.v1","correction_id":"observer-dispatcher-governance/high/b6r4","actor":"Tester","implementation_subject_sha":"<S12 SHA>","subject_verification":{"expected_sha":"<S12 SHA>","observed_sha":"<S12 SHA>","command":"<exact command>","result":"passing|failing"},"actual_graph_assertion":{"environment":"complete-real-triple","result":"passing|failing","skipped":false},"commands":[{"command":"<exact command>","exit_code":0,"result":"passing|failing"}],"verdict":"passing|failing","timestamp":"<RFC 3339 timestamp>"}
```

```json
{"schema_version":"observer-dispatcher-governance.correction-b6r4-implementation-review.v1","correction_id":"observer-dispatcher-governance/high/b6r4","review_kind":"correction-b6r4-implementation","implementation_subject_sha":"<S12 SHA>","review_target_commit_sha":"<pre-existing T12 SHA>","tester_evidence":{"path":"plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r4-tester-evidence.md","revision":"<T12 SHA>","implementation_subject_sha":"<S12 SHA>","verdict":"passing"},"reviewed_artifacts":[{"path":"tests/test_observer_dispatcher_governance_contract.py","revision":"<S12 SHA>"}],"topology":{"s12_sha":"<S12 SHA>","t12_sha":"<T12 SHA>","v12_sha":"<pre-commit V12 SHA>","non_merge":true,"exact_range":"S12..V12","exact_evidence_paths":true},"review_basis":"independent implementation review with named actual-SHA graph queries","verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]},"timestamp":"<RFC 3339 timestamp>"}
```

## Boundaries

No history rewrite, legacy recovery, `step-creator` activation, non-test implementation, PR resolution before Q12 classification, merge, release, or post-merge action is in scope.
