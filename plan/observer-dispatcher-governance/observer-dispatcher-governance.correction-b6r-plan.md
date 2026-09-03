# Observer / Dispatcher Governance — B6R Correction Plan

## Retention and baseline

B6/R10 and all earlier records are immutable frozen provenance. B6R is the sole current non-subject,
non-merge seven-path planning baseline; `step-creator` remains deferred.

The B6R admission's first-parent named diff contains exactly these paths once: shared workflow, shared
contract, parent plan/spec/step, and this B6R plan/step. Before admission, B6R planning artifacts contain no
B6R SHA, blob SHA, `HEAD`, or review outcome. Commit-time truth is the exact seven-path non-merge admission;
B6R never establishes `implementation_subject_sha`.

## Route and gates

Independent Plan-Reviewer clean-checkout-reviews B6R fields, all seven artifact revisions, and actual
first-parent exact-seven admission, then writes only R11 at
`plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r-review-log.md`.
Independent Implementer separately commits unchanged approved R11. Only then may non-merge S9 modify only
`tests/test_observer_dispatcher_governance_contract.py`.

S9 retains direct imports and rejects `importlib`, `__import__`, and `sys.modules`. Its actual graph test uses
only complete explicit `ODG_S9_SHA`/`ODG_T9_SHA`/`ODG_V9_SHA` and real subprocess `git rev-parse`,
`git rev-list`, and `git diff --name-status`; all absent is explicit skip/unverified and partial/invalid/
`HEAD`/merge/wrong-graph/multi-path input fails closed.

T9 and V9 are the only non-merge `S9 -> T9 -> V9` descendants. Their exact evidence paths are respectively
`observer-dispatcher-governance.correction-b6r-tester-evidence.md` and
`observer-dispatcher-governance.correction-b6r-implementation-review-log.md`; named `S9..V9` contains only
those paths. Q9 is committed-V9-SHA-only, read-only, artifact-free, and has no thread authority.

## Boundaries

No historical rewrite, legacy recovery, `step-creator` activation, new implementation path, PR thread
resolution, merge, release, or post-merge action is in scope.
