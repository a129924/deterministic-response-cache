# Observer / Dispatcher Governance — B5 Correction Plan

## B5 Commit-Time Baseline

B4R7/S6/T6, missing V6, and every prior epoch are frozen nonrouting provenance. B5 is the sole current
non-subject baseline. Before commit no B5 planning artifact embeds B5 SHA, blob SHA, `HEAD`, or review result.

The first non-merge B5 admission commit contains exactly:

1. `plan/agent-handoff-workflow.md`
2. `plan/topic-plan-contract.md`
3. `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md`
4. `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md`
5. `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md`
6. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b5-plan.md`
7. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b5-step.md`

Named first-parent `git diff --name-status <B5-parent>..<B5-SHA>` must list exactly those seven paths once.
B5 never establishes `implementation_subject_sha`.

## R8, S7, Evidence, and Q7 Route

Independent Plan-Reviewer clean-checkout-reviews every actual B5 blob and writes only B5 R8. Independent
Implementer separately commits unchanged approved R8. Only then may non-merge S7 begin, changing only
`tests/test_observer_dispatcher_governance_contract.py`.

S7 uses only complete explicit `ODG_S7_SHA`, `ODG_T7_SHA`, `ODG_V7_SHA` input and subprocess real
`git rev-parse`, `git rev-list`, `git diff --name-status`. No input explicitly skips rather than passes.
Missing/partial/`HEAD`/nonexistent/merge/wrong-parent/multi-path input fails closed. Direct imports remain
mandatory; `step-creator` stays deferred.

T7 and V7 are the sole non-merge `S7 -> T7 -> V7` descendants. Named `S7..V7` changes only B5 T7/V7 evidence
paths. V7 is authored before its own commit. Q7 then reads actual full V7 SHA, creates no artifact, uses no
`HEAD`, and cannot route lifecycle or resolve threads.
