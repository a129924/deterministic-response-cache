# Observer / Dispatcher Governance — B4R6 Correction Plan

## B4R6 Baseline

`b900366` and all B0–B4R5, S1–S5, T1–T5, V1–V5, normal/recovery evidence and older correction
artifacts are frozen nonrouting provenance. They cannot route, satisfy a gate, establish a subject,
or supply current evidence. B4R6 is the sole current pre-subject baseline and contains exactly:

1. `plan/agent-handoff-workflow.md`
2. `plan/topic-plan-contract.md`
3. `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md`
4. `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md`
5. `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md`
6. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r6-plan.md`
7. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r6-step.md`

Independent Implementer commits exactly these seven paths as non-subject B4R6 and reports named
`git diff --name-status b900366..<B4R6-SHA>`. No test, implementation, evidence, routing, or eighth
path is permitted.

Independent Plan-Reviewer reviews the actual seven committed B4R6 blobs from a clean checkout and
writes only `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r6-review-log.md`.
The record uses `observer-dispatcher-governance.correction-b4r6-plan-review.v1`, identifies
`observer-dispatcher-governance/high/b4r6`, the committed B4R6 SHA, and each seven paths once with its
B4R6 blob SHA. Independent Implementer separately commits the unchanged approved record. Neither B4R6
commit establishes `implementation_subject_sha`.

## S6 Exact Allowlist and Regression Contract

Only separately committed approved B4R6 review evidence permits one immutable non-merge S6 over the
parent plan's unchanged exact 15-path allowlist. Direct imports remain mandatory; `importlib`,
`__import__`, and `sys.modules` substitutions are forbidden. The two `step-creator` threads remain
deferred.

The S6 test path adds only fail-closed assertions for frozen B0–B4R5 provenance, B4R6 non-subject
seven-path baseline and locked review schema, S6-only exact 15-path allowlist, preserved direct imports
and deferred work, and actual named-SHA `S6 -> T6 -> V6` topology/range with exact two-path evidence.

## Evidence and Actual-Graph Requirements

Tester writes only
`plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r6-tester-evidence.md`
for same-S6 factual `passing|failing` results, with no routing, lifecycle, status, or `next_gate` field.
Reviewer writes only
`plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r6-implementation-review-log.md`
after same-S6 passing T6. Actual named SHA graph queries prove linear non-merge `S6 -> T6 -> V6`.
Named `git diff --name-status S6..V6` lists exactly those two B4R6 evidence paths. `HEAD`, a merge,
third descendant, or textual topology inference fails closed. V6 is authored before its commit and
cannot self-reference or infer V6 SHA.
