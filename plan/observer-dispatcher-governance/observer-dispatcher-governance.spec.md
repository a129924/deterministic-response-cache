# Observer / Dispatcher Governance Specification

## B6R9 Acceptance Criteria

1. B6R9 -> R19 -> S15 -> T15 -> V15 -> Q15 is the sole current route; B6R8/Q14 and all earlier routes are frozen
   nonrouting provenance.
2. B6R9 is a non-subject, non-merge first-parent exact-seven planning baseline. R19 independently records committed
   revision, reviewed tree, seven declared path/blob pairs, first-parent admission, Copilot triage, verdict and
   blockers. B6R9/R19 never establish implementation_subject_sha; approved committed R19 carries
   R19_COMPLETE_S15_NEXT and next phase S15.
3. Only non-merge S15 establishes the subject and changes only tests/test_observer_dispatcher_governance_contract.py.
4. Existing direct imports remain mandatory; importlib, __import__, and sys.modules substitutions fail.
5. S15 makes only the Q14 raw name-status ordering repair: assert structured status/path tuples in lexical path
   order, with B6R9 implementation-review-log before B6R9 tester-evidence. Existing actual-Git and full-input
   fail-closed semantics remain unchanged.
6. Named S15..V15 contains only B6R9 implementation-review-log then tester-evidence paths. V15 requires passing
   same-S15 T15 and a non-merge graph.
7. Actual Git assertions use only a complete explicit ODG_S15_SHA/ODG_T15_SHA/ODG_V15_SHA triple and real subprocess
   git rev-parse, git rev-list, and git diff --name-status. All absent yields explicit no-environment skip/unverified;
   partial, symbolic/HEAD, nonexistent, merge, wrong graph, or widened range fails closed.
8. Q15 runs only after V15 is committed; it is read-only, writes no artifact, and has no lifecycle or thread
   authority. Only passed Q15 permits independent per-thread classification; only explicit addressed-and-resolvable
   permits resolve.

## Failure Conditions

The contract fails closed if a prior route is current, B6R9 admission is merge/not-exact-seven, R19 lacks required
tree/blob/admission/triage field, B6R9/R19 is treated as subject, S15 widens paths or replaces direct imports, expected
raw tuple order is not review-log before tester-evidence, T15/V15 uses another path/subject, topology differs from
S15 -> T15 -> V15, actual input is invalid, or Q15 creates artifact/lifecycle/thread authority.

## Non-goals

No provenance migration, legacy-log recovery, step-creator work, thread resolution, merge, release, post-merge action,
architecture work, or unlisted implementation path belongs to B6R9.
