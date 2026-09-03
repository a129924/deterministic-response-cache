# Observer / Dispatcher Governance — B6R2 Correction Plan

## Canonical route

B6R/R11 and all earlier records are immutable frozen provenance. B6R2 is the sole current non-subject,
non-merge seven-path planning baseline; `step-creator` remains deferred.

Its first-parent named diff contains exactly once: `plan/agent-handoff-workflow.md`,
`plan/topic-plan-contract.md`, the parent plan/spec/step, and this B6R2 plan/step. Before admission, its
planning artifacts contain no B6R2 SHA, blob SHA, `HEAD`, or review outcome. B6R2 never establishes
`implementation_subject_sha`.

Independent Plan-Reviewer clean-checkout-reviews all seven B6R2 blobs and first-parent admission, then writes
only R12 at `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r2-review-log.md`.
Independent Implementer separately commits unchanged approved R12. Only then may non-merge S10 modify only
`tests/test_observer_dispatcher_governance_contract.py`.

S10 retains direct imports and rejects `importlib`, `__import__`, and `sys.modules`. Its actual graph test uses
only complete explicit `ODG_S10_SHA`/`ODG_T10_SHA`/`ODG_V10_SHA` and real subprocess `git rev-parse`,
`git rev-list`, and `git diff --name-status`; all absent is explicit skip/unverified and partial/invalid/
`HEAD`/merge/wrong-graph/multi-path input fails closed.

T10 and V10 are the only non-merge `S10 -> T10 -> V10` descendants. Their exact evidence paths are
`observer-dispatcher-governance.correction-b6r2-tester-evidence.md` and
`observer-dispatcher-governance.correction-b6r2-implementation-review-log.md`; named `S10..V10` contains only
those paths. Q10 is committed-V10-SHA-only, read-only, artifact-free, and has no thread authority. Q10 is the
sole shared human boundary; Q8/Q9 remain frozen and cannot classify or resolve threads.

## Boundaries

No historical rewrite, legacy recovery, `step-creator` activation, new implementation path, PR thread
resolution before Q10 independent classification, merge, release, or post-merge action is in scope.
