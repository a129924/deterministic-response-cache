# Observer / Dispatcher Governance — B6R10 Correction Plan

## Current route

B6R10 -> R20 -> S16 -> T16 -> V16 -> Q16 -> thread-classification -> human-check is the only current route.
B6R9/Q15 is frozen predecessor provenance. B6R10/R20 are non-subject; S16 is the sole implementation subject.

## Exact admission paths

1. `AGENTS.md`
2. `.agents/skills/plan-reviewer/SKILL.md`
3. `.agents/skills/plan-reviewer/checklist.md`
4. `.agents/skills/plan-reviewer/reference.md`
5. `plan/agent-handoff-workflow.md`
6. `plan/topic-plan-contract.md`
7. `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md`
8. `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md`
9. `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md`
10. this file
11. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r10-step.md`

The B6R10 admission is non-merge first-parent exact-eleven. Pre-admission planning artifacts contain no B6R10/R20
SHA, tree, blob, HEAD, or outcome.

## Evidence matrix

| Phase | Exact path | Writer | Gate |
| --- | --- | --- | --- |
| R20 | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r10-review-log.md` | Plan-Reviewer | committed B6R10 |
| S16 | `tests/test_observer_dispatcher_governance_contract.py` | Implementer | committed approved R20 |
| T16 | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r10-tester-evidence.md` | Tester | same S16 full suite passing |
| V16 | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r10-implementation-review-log.md` | Reviewer | committed passing T16 |
| Q16 | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r10-actual-gate-evidence.md` | Reviewer | committed V16 with `verdict:APPROVED`/full actual triple |

## R20 declared schema

```json
{"schema_version":"observer-dispatcher-governance.correction-b6r10-plan-review.v1","correction_id":"observer-dispatcher-governance/high/b6r10","review_kind":"correction-b6r10-plan","candidate":{"id":"observer-dispatcher-governance/high/b6r10","commit_sha":"<full SHA>","tree_sha":"<full SHA>","active":true|false},"reviewed_artifacts":[{"path":"<one of exact eleven>","blob_sha":"<SHA>"}],"first_parent_admission":{"commit_sha":"<full SHA>","parent_sha":"<full SHA>","non_merge":true,"exact_declared_paths":true,"name_status":["<eleven entries>"]},"review_basis":"independent clean checkout","copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]},"verdict":"approved|needs-rework","blocking_issues":[],"route_authorization":{"effective_committed_state":"R20_COMPLETE_S16_NEXT","next_phase":"S16","implementation_subject_sha":null,"close_authorization":null}|null,"timestamp":"<RFC 3339>"}
```

`needs-rework` requires `candidate.active:false` and `route_authorization:null`. Only a separately committed unchanged
approved R20 has `candidate.active:true`; Planner may select only that evidence. Plan-Creator cannot refine, select, or self-close it.

S16 retains direct imports and prohibits `importlib`, `__import__`, and `sys.modules`; it validates T16/V16 committed
blob semantics for topology/path, identical full S16 subject SHA, T16 `passing` and V16 `APPROVED`. Q16 is actual Git,
evidence-only, and writes the sole active-candidate close record. It authorizes classification only, not Human PR review or merge.

## T16 declared exact schema

```json
{"schema_version":"observer-dispatcher-governance.correction-b6r10-tester-evidence.v1","correction_id":"observer-dispatcher-governance/high/b6r10","phase":"T16","subject":{"phase":"S16","commit_sha":"<40 lowercase hexadecimal S16 SHA>","test_path":"tests/test_observer_dispatcher_governance_contract.py"},"test_run":{"command":"<exact full-suite command run>","status":"passing","exit_code":0},"timestamp":"<RFC 3339 timestamp>"}
```

This object has exactly the shown top-level and nested keys. `subject.commit_sha` is a 40-character lowercase
hexadecimal SHA, is S16's committed non-merge subject SHA, and `test_path` is the sole S16 path. `test_run` is the
factual run actually executed. Any missing/extra key, abbreviated/non-hex SHA, wrong phase/path, non-`passing`
status, nonzero exit code, or uncommitted/mismatched subject is fail closed.

## V16 declared exact schema

```json
{"schema_version":"observer-dispatcher-governance.correction-b6r10-implementation-review.v1","correction_id":"observer-dispatcher-governance/high/b6r10","phase":"V16","subject":{"phase":"S16","commit_sha":"<40 lowercase hexadecimal S16 SHA>","test_path":"tests/test_observer_dispatcher_governance_contract.py"},"tester_evidence":{"phase":"T16","commit_sha":"<40 lowercase hexadecimal T16 SHA>","path":"plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r10-tester-evidence.md","blob_sha":"<40 lowercase hexadecimal committed T16 blob SHA>","subject_commit_sha":"<same 40 lowercase hexadecimal S16 SHA>","status":"passing"},"verdict":"APPROVED","blocking_issues":[],"timestamp":"<RFC 3339 timestamp>"}
```

This object has exactly the shown top-level and nested keys. V16 is written only after T16 is committed and binds the
same S16 commit/path plus T16's committed commit/path/blob/subject/status. Every SHA is 40 lowercase hexadecimal
characters. `verdict` is exactly uppercase `APPROVED` and `blocking_issues` exactly `[]`; any other value, absent or
extra key, wrong parent topology, or semantic mismatch is fail closed.

## Q16 declared exact schema

```json
{"schema_version":"observer-dispatcher-governance.correction-b6r10-actual-gate.v1","correction_id":"observer-dispatcher-governance/high/b6r10","phase":"Q16","artifacts":{"S16":{"commit_sha":"<40 lowercase hexadecimal S16 SHA>","parent_sha":"<40 lowercase hexadecimal S16 parent SHA>","path":"tests/test_observer_dispatcher_governance_contract.py","blob_sha":"<40 lowercase hexadecimal S16 blob SHA>"},"T16":{"commit_sha":"<40 lowercase hexadecimal T16 SHA>","parent_sha":"<same 40 lowercase hexadecimal S16 SHA>","path":"plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r10-tester-evidence.md","blob_sha":"<40 lowercase hexadecimal T16 blob SHA>"},"V16":{"commit_sha":"<40 lowercase hexadecimal V16 SHA>","parent_sha":"<same 40 lowercase hexadecimal T16 SHA>","path":"plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r10-implementation-review-log.md","blob_sha":"<40 lowercase hexadecimal V16 blob SHA>"}},"parsed_claims":{"subject":{"phase":"S16","commit_sha":"<same 40 lowercase hexadecimal S16 SHA>","test_path":"tests/test_observer_dispatcher_governance_contract.py"},"tester_status":"passing","reviewer_verdict":"APPROVED"},"actual_git":{"triple":{"s16_sha":"<same 40 lowercase hexadecimal S16 SHA>","t16_sha":"<same 40 lowercase hexadecimal T16 SHA>","v16_sha":"<same 40 lowercase hexadecimal V16 SHA>"},"linear":true,"range":"S16..V16","name_status":["<exact actual name-status entries>"]},"close_authorization":{"status":"ACTIVE_CANDIDATE_CLOSED","thread_classification":"PERMITTED","thread_resolution":"FORBIDDEN","human_review":"FORBIDDEN","merge":"FORBIDDEN","release":"FORBIDDEN","post_merge":"FORBIDDEN"},"timestamp":"<RFC 3339 timestamp>"}
```

Q16 has exactly the shown top-level and nested keys, binds only already committed S16/T16/V16 artifacts and is written
only after V16 is committed. Reviewer writes it read-only from real subprocess Git full-triple evidence; an independent
Implementer commits it unchanged as the sole evidence-only path before the close record becomes active. Q16 must never
include its own commit/tree/blob. Missing/extra key, non-40/non-hex SHA, non-linear graph, wrong range/name-status,
inconsistent parsed claims, or any authorization broader than classification is fail closed. It cannot resolve threads,
perform Human review, merge, release, or post-merge.
