# Observer / Dispatcher Governance — B4R4 Correction Plan

## B4R4 Baseline

`8b87aab` B4R3 and its failed clean-checkout review are frozen nonrouting provenance. B0–B4R3,
S1–S4, T1–T4, V1–V4, normal/recovery records and their prior schema/blocker/checklist/pending
semantics cannot route, satisfy a gate, establish a subject or supply current evidence. B4R4 is sole
current pre-subject baseline and contains exactly:

1. `plan/agent-handoff-workflow.md`
2. `plan/topic-plan-contract.md`
3. `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md`
4. `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md`
5. `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md`
6. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r4-plan.md`
7. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r4-step.md`
8. `tests/test_observer_dispatcher_governance_contract.py`

The first seven are Plan-Creator delta. The eighth is one-time bootstrap exception: before planning
review, Independent Implementer adapts only that test to fixed B4R4 assertions in parent spec and
commits all eight paths together. It may not create subject, evidence, routing, status, or another
path. Named report `git diff --name-status 8b87aab..<B4R4-SHA>` must list only these eight paths.
B4R4 is non-subject.

Independent Plan-Reviewer reviews all eight actual B4R4 blobs from clean checkout and writes only
`plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r4-review-log.md`.
Its schema identifies B4R4, committed B4R4 SHA, and every one of eight paths once with blob SHA.
Independent Implementer separately commits unchanged approved review evidence. Neither B4R4 commit
can establish `implementation_subject_sha`.

## Fixed Bootstrap Test Adaptation

The eighth-path test may delete obsolete B2/B3 current-route assertions and replace them only with
B4R4 assertions. It must directly read eight B4R4 routing surfaces and assert: all B4R3/prior epochs
are frozen; B4R4 baseline is non-subject; B4R4 has exact eight paths and clean eight-blob review; S5
alone is later subject over unchanged 15-path allowlist; direct imports remain required;
`step-creator` threads remain deferred; and only fresh B4R4 T5/V5 form named non-merge
`S5 -> T5 -> V5` with exact `S5..V5` evidence range. Mutation tests must fail closed for each
condition. It must not introduce `importlib`, `__import__`, or `sys.modules` substitution.

## S5 Exact Allowlist

S5 may begin only after separately committed approved B4R4 review evidence. S5 alone is immutable
non-merge subject and may modify exactly preserved parent-plan 15 paths. Direct imports remain
mandatory; `importlib`, `__import__`, and `sys.modules` substitutions are forbidden. The two
`step-creator` threads remain deferred.

## Evidence and Actual-Graph Requirements

Tester writes only
`plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r4-tester-evidence.md`
for same-S5 factual `passing|failing` results, with no routing, lifecycle, status or `next_gate` field.
Reviewer writes only
`plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r4-implementation-review-log.md`
after same-S5 passing T5. Actual named SHA graph queries must prove linear non-merge `S5 -> T5 -> V5`.
Named `git diff --name-status S5..V5` must list exactly two B4R4 evidence paths. `HEAD`, a merge,
third descendant, or textual topology inference fails closed. V5 is authored before its commit and
cannot self-reference or infer V5 SHA.
