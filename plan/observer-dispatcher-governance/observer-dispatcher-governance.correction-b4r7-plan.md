# Observer / Dispatcher Governance — B4R7 Correction Plan

## B4R7 Commit-Time Baseline

`b900366`, B0–B4R6, S1–S5, T1–T5, V1–V5, normal/recovery records, `7d23e8c`, `6ede06b`, every older
correction artifact and any uncommitted B4R6 review log are frozen nonrouting provenance. B4R7 is the
sole current non-subject baseline. Before its commit, no planning artifact embeds an expected SHA, blob
SHA, `HEAD`, or review result.

An Independent Implementer must make the first non-merge commit containing the complete exact B4R7
baseline set:

1. `plan/agent-handoff-workflow.md`
2. `plan/topic-plan-contract.md`
3. `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md`
4. `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md`
5. `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md`
6. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r7-plan.md`
7. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r7-step.md`

Commit admission is commit-time truth: verify that commit has one parent and report named
`git diff --name-status <B4R7-parent>..<B4R7-SHA>`. It must list exactly these seven paths, each once;
no test, implementation, evidence, routing, or eighth path may be present. B4R7 never establishes
`implementation_subject_sha`.

## R7, S6, and Evidence Route

Independent Plan-Reviewer reviews the actual seven committed B4R7 blobs from a clean checkout and writes
only `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r7-review-log.md`.
The record uses `observer-dispatcher-governance.correction-b4r7-plan-review.v1`, identifies
`observer-dispatcher-governance/high/b4r7`, names the committed B4R7 SHA, and lists each baseline path
once with its actual B4R7 blob SHA. Independent Implementer separately commits that unchanged approved
R7 record. Only then may S6 begin.

S6 is the sole immutable non-merge subject, using only the parent plan's existing exact 15-path allowlist.
Direct imports remain mandatory; `importlib`, `__import__`, and `sys.modules` substitutions remain
forbidden. The `step-creator` threads remain deferred. S6 test work adds only B4R7 fail-closed assertions:
frozen history cannot route; B4R7/R7 cannot become subject; admission set/schema and S6 allowlist cannot
mutate; direct imports/deferred work cannot change; and the named actual graph/range must be
`S6 -> T6 -> V6` / `S6..V6`.

Tester writes only
`plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r7-tester-evidence.md`
for factual same-S6 results. Reviewer writes only
`plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r7-implementation-review-log.md`
after passing same-S6 T6. Actual named SHA graph queries prove linear non-merge `S6 -> T6 -> V6`;
`git diff --name-status S6..V6` lists exactly those two B4R7 paths. `HEAD`, merge, third descendant, or
textual topology inference fails closed. V6 is authored before its own commit and cannot self-reference.
