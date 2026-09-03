# Observer / Dispatcher Governance — B4R5 Correction Plan

## B4R5 Baseline

`8190dbb` B4R4 and its bootstrap-test route are frozen nonrouting provenance. B0–B4R4, S1–S4,
T1–T4, V1–V4, normal/recovery records and all prior correction artifacts cannot route, satisfy a
gate, establish a subject or supply current evidence. B4R5 is the sole current pre-subject baseline
and contains exactly these seven planning paths:

1. `plan/agent-handoff-workflow.md`
2. `plan/topic-plan-contract.md`
3. `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md`
4. `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md`
5. `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md`
6. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r5-plan.md`
7. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r5-step.md`

Independent Implementer commits exactly these seven paths as non-subject B4R5. It may not alter the
conformance test, implementation, evidence or an eighth path. Named report
`git diff --name-status 8190dbb..<B4R5-SHA>` must list only these seven paths.

Independent Plan-Reviewer reviews all seven actual B4R5 blobs from a clean checkout and writes only
`plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r5-review-log.md`.
The record uses `observer-dispatcher-governance.correction-b4r5-plan-review.v1`, identifies
`observer-dispatcher-governance/high/b4r5`, the committed B4R5 SHA, and each seven paths once with
its B4R5 blob SHA. Independent Implementer separately commits the unchanged approved record. Neither
B4R5 commit establishes `implementation_subject_sha`.

## S5 Exact Allowlist and Future Test Regressions

Only separately committed approved B4R5 review evidence permits one immutable non-merge S5 over the
parent plan's unchanged exact 15-path allowlist. Direct imports remain mandatory; `importlib`,
`__import__`, and `sys.modules` substitutions are forbidden. The two `step-creator` threads remain
deferred.

S5's declared test path adds only these three future fail-closed regression groups:

1. actual named SHA graph/range verification of non-merge `S5 -> T5 -> V5` and `S5..V5`, never
   `HEAD` or textual topology;
2. exact seven-path B4R5 baseline, exact 15-path S5 allowlist, and exact two-path B4R5 evidence set;
3. mutation of the locked B4R5 plan-review schema (identity, review kind, seven reviewed blobs or
   clean-checkout basis) is rejected.

## Evidence and Actual-Graph Requirements

Tester writes only
`plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r5-tester-evidence.md`
for same-S5 factual `passing|failing` results, with no routing, lifecycle, status or `next_gate` field.
Reviewer writes only
`plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r5-implementation-review-log.md`
after same-S5 passing T5. Actual named SHA graph queries must prove linear non-merge `S5 -> T5 -> V5`.
Named `git diff --name-status S5..V5` must list exactly those two B4R5 evidence paths. `HEAD`, a merge,
third descendant, or textual topology inference fails closed. V5 is authored before its commit and
cannot self-reference or infer V5 SHA.
