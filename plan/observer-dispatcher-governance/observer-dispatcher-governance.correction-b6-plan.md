# Observer / Dispatcher Governance — B6 Correction Plan

## Trigger and retention

B4R7/B5/B5R/R9 and all earlier records are immutable frozen provenance. B6 replaces parent canonical
execution truth without altering those historical artifacts. `step-creator` remains deferred.

## B6 Commit-Time Baseline

B6 is the sole current non-subject baseline. Before its commit, no B6 planning artifact embeds B6 SHA,
blob SHA, `HEAD`, or review outcome. The first non-merge B6 admission commit contains exactly:

1. `plan/agent-handoff-workflow.md`
2. `plan/topic-plan-contract.md`
3. `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md`
4. `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md`
5. `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md`
6. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6-plan.md`
7. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6-step.md`

Named first-parent `git diff --name-status <B6-parent>..<B6-SHA>` lists exactly these paths once. B6 never
establishes `implementation_subject_sha`.

## R10, S8, T8, V8 and Q8 Route

Independent Plan-Reviewer clean-checkout-reviews every B6 blob and writes only R10 at
`plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6-review-log.md`.
Independent Implementer separately commits unchanged approved R10. Only then may non-merge S8 change only
`tests/test_observer_dispatcher_governance_contract.py`; direct imports remain mandatory and `step-creator`
remains deferred.

S8 actual Git graph assertion accepts only complete explicit `ODG_S8_SHA`, `ODG_T8_SHA`, `ODG_V8_SHA` and
executes real subprocess `git rev-parse`, `git rev-list`, and `git diff --name-status`. It reports explicit
`skip`/`unverified` only when all three are absent. Partial, invalid, `HEAD`, nonexistent, merge, wrong-parent/
wrong-graph, or multi-path values fail closed.

T8 and V8 are the only non-merge `S8 -> T8 -> V8` descendants. Tester writes only
`plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6-tester-evidence.md` after
the actual assertion passes with a complete real triple and no skip. Reviewer writes only
`plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6-implementation-review-log.md`
after same-S8 passing T8. Named `git diff --name-status S8..V8` lists exactly those two paths. V8 is authored
before its own commit. Q8 uses committed full V8 SHA only, writes no artifact, uses no `HEAD`, and cannot
route lifecycle or resolve threads.

## Artifact Ownership and Gates

| Artifact | Write owner | Decision authority | Gate |
| --- | --- | --- | --- |
| B6 seven planning paths | Plan-Creator | Planner | B6 admission only |
| R10 review log | Plan-Reviewer | Plan-Reviewer verdict | approved R10 before S8 |
| S8 test path | Implementer | Planner | only one non-merge subject |
| T8 evidence | Tester | factual result only | full triple, passing, non-skipped before V8 |
| V8 review log | Reviewer | Reviewer verdict; Planner routes | same-S8 T8 and exact range |
| Q8 | Reviewer | none | post-V8 read-only only |

## Boundaries

No historical-artifact rewrite, legacy recovery, `step-creator` activation, new implementation path,
PR-thread resolution, merge, release, post-merge, or artifact creation by Q8 is in scope.
