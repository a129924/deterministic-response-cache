# Observer / Dispatcher Governance — B6R5 Correction Plan

## Canonical route

`B6R5 -> R15 -> S13 -> T13 -> V13 -> Q13` is the sole current route. B6R4/R14/S12 and every older route are
immutable frozen nonrouting failed provenance. B6R5/R15 are non-subject; S13 alone establishes the subject and
changes only `tests/test_observer_dispatcher_governance_contract.py`. Direct imports remain mandatory and
`importlib`, `__import__`, and `sys.modules` substitutions fail.

B6R5 is a non-merge first-parent exact-seven planning baseline. R15 is a normal independent clean-checkout review.
T13 truthfully records a passing full suite with one no-environment actual-graph `skip`/`unverified`, not a full
triple claim. V13 proves only the structural non-merge `S13 -> T13 -> V13` chain and named `S13..T13` range. After
V13 is committed, Q13 alone runs the non-skipped actual Git gate with complete explicit full
`ODG_S13_SHA`/`ODG_T13_SHA`/`ODG_V13_SHA` through subprocess `git rev-parse`, `git rev-list`, and
`git diff --name-status`. Absent/partial/invalid/`HEAD`/nonexistent/merge/wrong graph/range input fails closed.

## B6R5 admission paths

1. `plan/agent-handoff-workflow.md`
2. `plan/topic-plan-contract.md`
3. `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md`
4. `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md`
5. `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md`
6. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r5-plan.md`
7. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r5-step.md`

Pre-admission artifacts contain no B6R5 SHA/blob SHA/`HEAD`/review outcome. R15 is written only after its committed
baseline review and separately committed unchanged.

## Artifact matrix

| Phase | Path | Writer | Gate |
| --- | --- | --- | --- |
| R15 | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r5-review-log.md` | Plan-Reviewer | normal clean checkout |
| S13 | `tests/test_observer_dispatcher_governance_contract.py` | Implementer | approved R15 |
| T13 | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r5-tester-evidence.md` | Tester | passing full suite + no-env skip/unverified |
| V13 | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r5-implementation-review-log.md` | Reviewer | structural-only `S13..T13` |
| Q13 | no written path | Reviewer | committed V13 + actual full SHAs |

## Schemas

```json
{"schema_version":"observer-dispatcher-governance.correction-b6r5-plan-review.v1","correction_id":"observer-dispatcher-governance/high/b6r5","reviewed_commit_sha":"<B6R5 SHA>","reviewed_tree_sha":"<B6R5 tree SHA>","reviewed_artifacts":[{"path":"<B6R5 path>","blob_sha":"<blob SHA>"}],"first_parent_admission":{"non_merge":true,"exact_declared_paths":true,"name_status":"<seven paths>"},"verdict":"approved|needs-rework"}
```

```json
{"schema_version":"observer-dispatcher-governance.correction-b6r5-tester-evidence.v1","implementation_subject_sha":"<S13 SHA>","full_suite":{"result":"passing","exit_code":0},"actual_graph_assertion":{"environment":"no-env","result":"skip|unverified","skipped":true,"complete_triple_claimed":false},"verdict":"passing|failing"}
```

```json
{"schema_version":"observer-dispatcher-governance.correction-b6r5-implementation-review.v1","implementation_subject_sha":"<S13 SHA>","tester_evidence":{"revision":"<T13 SHA>","actual_graph_assertion":"no-env-skip-or-unverified"},"topology":{"non_merge":true,"exact_range":"S13..T13","exact_evidence_paths":true},"review_basis":"structural only; Q13 remains pending","verdict":"approved|needs-rework"}
```

## Boundaries

No legacy migration, `step-creator` activation, unlisted path, pre-Q13 thread resolution, merge, release, or
post-merge action is in scope. Q13 writes no artifact; only a subsequent independent per-thread classification can
label a thread `addressed-and-resolvable`.
