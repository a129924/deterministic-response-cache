# Observer / Dispatcher Governance — B5R Correction Plan

## B5R Commit-Time Baseline

B5, missing R8, B4R7/S6/T6, missing V6, and all preceding normal, recovery, correction, tester and reviewer
records are frozen nonrouting provenance. They cannot be current, pending, candidate, gate, subject or
evidence. B5R is the sole current non-subject baseline. Before its commit, no B5R planning artifact embeds a
B5R SHA, blob SHA, `HEAD`, or review outcome.

The first non-merge B5R admission commit contains exactly:

1. `plan/agent-handoff-workflow.md`
2. `plan/topic-plan-contract.md`
3. `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md`
4. `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md`
5. `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md`
6. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b5r-plan.md`
7. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b5r-step.md`

Named first-parent `git diff --name-status <B5R-parent>..<B5R-SHA>` must list exactly those seven paths once.
B5R never establishes `implementation_subject_sha`.

## R9, S7, T7, V7 and Q7 Route

Independent Plan-Reviewer clean-checkout-reviews every B5R blob and writes only R9 at
`plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b5r-review-log.md`.
Independent Implementer separately commits unchanged approved R9. Only then may non-merge S7 begin, changing
only `tests/test_observer_dispatcher_governance_contract.py`; direct imports remain mandatory and
`step-creator` remains deferred.

S7's actual Git graph assertion accepts only the complete explicit `ODG_S7_SHA`, `ODG_T7_SHA`,
`ODG_V7_SHA` triple and executes real subprocess `git rev-parse`, `git rev-list`, and
`git diff --name-status`. It is explicitly `skip`/`unverified` only when all three values are absent. Partial,
invalid, `HEAD`, nonexistent, merge, wrong-parent/wrong-graph, or multi-path values fail closed.

T7 and V7 are the only non-merge `S7 -> T7 -> V7` descendants. Tester writes only
`plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b5r-tester-evidence.md` after
running the actual assertion with a complete real triple and obtaining a non-skipped passing result. Reviewer
writes only
`plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b5r-implementation-review-log.md`
after same-S7 passing T7. Named `git diff --name-status S7..V7` lists exactly those T7/V7 paths. V7 is authored
before its own commit. Q7 then uses committed full V7 SHA only, creates no artifact, uses no `HEAD`, and cannot
route lifecycle or resolve threads.

## Artifact Ownership and Gates

| Artifact | Write owner | Decision authority | Gate |
| --- | --- | --- | --- |
| B5R seven planning paths | Plan-Creator | Planner | B5R admission only |
| R9 review log | Plan-Reviewer | Plan-Reviewer verdict | approved R9 before S7 |
| S7 test path | Implementer | Planner | only one non-merge subject |
| T7 evidence | Tester | factual result only | full triple, passing, non-skipped before V7 |
| V7 review log | Reviewer | Reviewer verdict; Planner routes | same-S7 T7 and exact range |
| Q7 | Reviewer | none | post-V7 read-only only |

## Boundaries

No legacy migration, B5/R8 recovery, `step-creator` activation, new implementation path, PR-thread resolution,
merge, release, post-merge, or artifact creation by Q7 is in scope.
