# Observer / Dispatcher Governance Specification

## B6R8 Acceptance Criteria

1. `B6R8 -> R18 -> S14 -> T14 -> V14 -> Q14` is the sole current route; all earlier routes are frozen
   nonrouting provenance.
2. B6R8 is a non-subject, non-merge first-parent exact-seven planning baseline. R18 independently records the
   committed revision, reviewed tree, all seven declared path/blob pairs, first-parent admission result, Copilot
   feedback triage, verdict and blockers, and verifies the frozen R17 receipt path, reviewed commit
   `03d90755b378063a312e62f9eefbe31caa081981`, approved receipt commit
   `a7770348222049f1c8bb6a0ee67e3136f2f47c3f`, approved verdict, non-merge and first-parent. B6R8/R18 never establish
   `implementation_subject_sha`; an approved committed R18 carries effective state `R17_COMPLETE_S14_NEXT` and next phase S14.
3. Only non-merge S14 establishes the subject and changes only
   `tests/test_observer_dispatcher_governance_contract.py`.
4. Existing test direct imports remain mandatory; `importlib`, `__import__`, and `sys.modules` substitutions fail.
5. S14 tests read the five canonical planning docs plus B6R8 plan/step, enforce temporal frozen provenance, reject
   B6R8/R18/B6R7/R17/S1–S13 as a current subject, and require only `S14 -> T14 -> V14`.
6. The exact named `S14..V14` range contains only the B6R8 T14/V14 evidence paths. V14 requires passing same-S14
   T14 and a non-merge graph.
7. Actual Git assertions use only a complete explicit `ODG_S14_SHA`/`ODG_T14_SHA`/`ODG_V14_SHA` triple and real
   subprocess `git rev-parse`, `git rev-list`, and `git diff --name-status`. All absent yields explicit
   no-environment skip/unverified; partial, symbolic/`HEAD`, nonexistent, merge, wrong graph, or widened range
   fails closed.
8. Q14 runs only after V14 is committed; it is read-only, writes no artifact, and has no lifecycle or thread
   authority. Only a passed Q14 permits independent per-thread classification; only explicit
   `addressed-and-resolvable` permits resolve.

## Failure Conditions

The contract fails closed if a prior route is current, B6R8 admission is merge/not-exact-seven, R18 lacks any
required tree/blob/admission/predecessor-receipt/triage field, B6R8/R18 is treated as subject, S14 widens paths or replaces direct imports,
T14/V14 uses another path/subject, a topology differs from `S14 -> T14 -> V14`, actual input is invalid, or Q14
creates artifact/lifecycle/thread authority.

## Non-goals

No provenance migration, legacy-log recovery, `step-creator` work, thread resolution, merge, release, post-merge
action, architecture work, or unlisted implementation path belongs to B6R8.
