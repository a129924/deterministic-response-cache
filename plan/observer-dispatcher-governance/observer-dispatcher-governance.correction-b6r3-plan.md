# Observer / Dispatcher Governance — B6R3 Correction Plan

## Canonical route

`B6R3 -> R13 -> S11 -> T11 -> V11 -> Q11` is the sole current route. B6R, B6R2, and all older records are immutable frozen nonrouting provenance. B6R3 is a non-subject, non-merge first-parent planning baseline; R13 independently reviews it, and neither creates `implementation_subject_sha`.

The B6R3 admission changes exactly once each:

1. `plan/agent-handoff-workflow.md`
2. `plan/topic-plan-contract.md`
3. `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md`
4. `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md`
5. `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md`
6. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r3-plan.md`
7. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r3-step.md`

Before admission those files contain no B6R3 SHA/blob SHA/`HEAD`/review outcome. R13 is written only after a clean-checkout review of the committed B6R3 tree, its seven named blobs, and its exact first-parent diff, then separately committed unchanged by an independent Implementer.

S11 is one non-merge subject modifying only `tests/test_observer_dispatcher_governance_contract.py`. It retains direct imports, rejects `importlib`, `__import__`, and `sys.modules` substitutions, and verifies exact provenance/subject/topology semantics through real subprocess Git queries using only complete explicit S11/T11/V11 environment SHAs. T11 then V11 are the sole exact evidence-only descendants; Q11 is committed-full-V11-SHA-only, read-only, and artifact-free.

## Full artifact matrix

| Phase | Exact path(s) | Writer | Authority | Required gate |
| --- | --- | --- | --- | --- |
| B6R3 | seven paths enumerated above | Plan-Creator, then Implementer | Planner | non-merge first-parent exact-seven |
| R13 | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r3-review-log.md` | Plan-Reviewer | independent review verdict | all B6R3 blobs/tree reviewed |
| S11 | `tests/test_observer_dispatcher_governance_contract.py` | Implementer | Planner after approved R13 | one non-merge subject, direct imports |
| T11 | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r3-tester-evidence.md` | Tester | factual result | complete real triple passes |
| V11 | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r3-implementation-review-log.md` | Reviewer | independent review verdict | same-S11 T11 and exact range |
| Q11 | no written path | Reviewer, read-only | Planner/human boundary | committed full V11 SHA only |

## R13 schema

```json
{"schema_version":"observer-dispatcher-governance.correction-b6r3-plan-review.v1","correction_id":"observer-dispatcher-governance/high/b6r3","review_kind":"correction-b6r3-plan-review","reviewed_commit_sha":"<B6R3 SHA>","reviewed_tree_sha":"<B6R3 tree SHA>","reviewed_artifacts":[{"path":"<one exact B6R3 planning path>","blob_sha":"<B6R3 blob SHA>"}],"first_parent_admission":{"candidate_parent_sha":"<B6R3 first parent SHA>","observed_parent_sha":"<B6R3 first parent SHA>","non_merge":true,"exact_declared_paths":true,"name_status":"<exact seven name-status entries>"},"review_basis":"independent clean-checkout fields, blobs, and first-parent seven-path review","verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]},"timestamp":"<RFC 3339 timestamp>"}
```

## T11 / V11 schemas

```json
{"schema_version":"observer-dispatcher-governance.correction-b6r3-tester-evidence.v1","correction_id":"observer-dispatcher-governance/high/b6r3","actor":"Tester","implementation_subject_sha":"<S11 SHA>","subject_verification":{"expected_sha":"<S11 SHA>","observed_sha":"<S11 SHA>","command":"<exact command>","result":"passing|failing"},"actual_graph_assertion":{"environment":"complete-real-triple","result":"passing|failing","skipped":false},"commands":[{"command":"<exact command>","exit_code":0,"result":"passing|failing"}],"verdict":"passing|failing","timestamp":"<RFC 3339 timestamp>"}
```

```json
{"schema_version":"observer-dispatcher-governance.correction-b6r3-implementation-review.v1","correction_id":"observer-dispatcher-governance/high/b6r3","review_kind":"correction-b6r3-implementation","implementation_subject_sha":"<S11 SHA>","review_target_commit_sha":"<pre-existing T11 SHA>","tester_evidence":{"path":"plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r3-tester-evidence.md","revision":"<T11 SHA>","implementation_subject_sha":"<S11 SHA>","verdict":"passing"},"reviewed_artifacts":[{"path":"tests/test_observer_dispatcher_governance_contract.py","revision":"<S11 SHA>"}],"topology":{"s11_sha":"<S11 SHA>","t11_sha":"<T11 SHA>","v11_sha":"<pre-commit V11 SHA>","non_merge":true,"exact_range":"S11..V11","exact_evidence_paths":true},"review_basis":"independent implementation review with named actual-SHA graph queries","verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]},"timestamp":"<RFC 3339 timestamp>"}
```

## Boundaries

No history rewrite, legacy recovery, `step-creator` activation, non-test implementation, PR resolution before Q11 classification, merge, release, or post-merge action is in scope.
