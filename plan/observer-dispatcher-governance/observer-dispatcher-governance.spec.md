# Observer / Dispatcher Governance Specification

> **Frozen provenance:** `b900366`, normal/recovery records, B0–B5R (including R8/R9), S1–S7, T1–T7,
> V1–V7, Q7 and all earlier correction artifacts are immutable historical provenance, excluded from B6.

## B6 Acceptance Criteria

1. B6 is the only current non-subject, non-merge baseline and its named first-parent admission diff contains
   exactly the seven declared B6 planning paths. Pre-commit B6 artifacts embed neither B6 SHA/blob SHA,
   `HEAD`, nor review outcome.
2. Independent R10 clean-checkout-reviews every B6 blob once and is separately committed unchanged when
   approved. Neither B6 nor R10 creates `implementation_subject_sha`.
3. Only non-merge S8 establishes the subject and changes only
   `tests/test_observer_dispatcher_governance_contract.py`.
4. Direct imports remain mandatory. `importlib`, `__import__`, and `sys.modules` substitutions fail.
5. S8 tests read the B6 parent workflow/contract/plan/spec/step and B6 plan/step, reject frozen provenance
   as B6 routing material, and reject B6/R10 as implementation subject.
6. The actual Git assertion accepts only a complete explicit `ODG_S8_SHA`/`ODG_T8_SHA`/`ODG_V8_SHA` triple
   through real subprocess `git rev-parse`, `git rev-list`, and `git diff --name-status`. All values absent
   gives explicit skip/unverified; partial, invalid, `HEAD`, nonexistent, merge, wrong parent/graph, or
   multi-path input fails closed.
7. T8 and V8 are the only linear non-merge evidence-only descendants. A named `S8..V8` diff lists exactly
   the B6 Tester and Reviewer evidence paths. V8 requires same-S8 passing T8.
8. Q8 is post-V8, committed-full-V8-SHA-only, read-only, creates no artifact and has neither lifecycle nor
   thread authority.

## Failure Conditions

The contract fails closed if B6 admission is a merge, lacks/adds a path, is not its first complete
seven-path baseline, embeds SHA/`HEAD`, misses reviewed blob, treats B6/R10 as subject, widens S8, replaces
direct imports, activates deferred work, uses a wrong T8/V8 path or S8, has failing T8, accepts partial
environment input, substitutes `HEAD`, accepts merge/third descendant, or replaces named S8/V8/range
verification with textual inference.

## Non-goals

No provenance migration, legacy-log recovery, `step-creator` work, PR thread resolution, merge, release,
post-merge action, architecture change, or unlisted implementation path belongs to B6.
