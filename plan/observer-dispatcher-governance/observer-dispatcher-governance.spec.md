# Observer / Dispatcher Governance Specification

> **Frozen provenance:** `b900366`, normal/recovery records, B0–B6 (including R8/R9/R10), S1–S8, T1–T8,
> V1–V8, Q7/Q8 and all earlier correction artifacts are immutable historical provenance, excluded from B6R.

## B6R Acceptance Criteria

1. B6R is the only current non-subject, non-merge baseline and its named first-parent admission diff contains
   exactly the seven declared B6R planning paths. Pre-commit B6R artifacts embed neither B6R SHA/blob SHA,
   `HEAD`, nor review outcome.
2. Independent R11 clean-checkout-reviews every B6R field/blob and first-parent exact-seven admission, and is
   separately committed unchanged when approved. Neither B6R nor R11 creates `implementation_subject_sha`.
3. Only non-merge S9 establishes the subject and changes only
   `tests/test_observer_dispatcher_governance_contract.py`.
4. Direct imports remain mandatory. `importlib`, `__import__`, and `sys.modules` substitutions fail.
5. S9 tests read the B6R parent workflow/contract/plan/spec/step and B6R plan/step, reject frozen provenance
   as B6R routing material, and reject B6R/R11 as implementation subject.
6. The actual Git assertion accepts only a complete explicit `ODG_S9_SHA`/`ODG_T9_SHA`/`ODG_V9_SHA` triple
   through real subprocess `git rev-parse`, `git rev-list`, and `git diff --name-status`. All values absent
   gives explicit skip/unverified; partial, invalid, `HEAD`, nonexistent, merge, wrong parent/graph, or
   multi-path input fails closed.
7. T9 and V9 are the only linear non-merge evidence-only descendants. A named `S9..V9` diff lists exactly
   the B6R Tester and Reviewer evidence paths. V9 requires same-S9 passing T9.
8. Q9 is post-V9, committed-full-V9-SHA-only, read-only, creates no artifact and has neither lifecycle nor
   thread authority.

## Failure Conditions

The contract fails closed if B6R admission is a merge, lacks/adds a path, is not its first complete
seven-path baseline, embeds SHA/`HEAD`, misses reviewed blob or first-parent result, treats B6R/R11 as subject, widens S9, replaces
direct imports, activates deferred work, uses a wrong T9/V9 path or S9, has failing T9, accepts partial
environment input, substitutes `HEAD`, accepts merge/third descendant, or replaces named S9/V9/range
verification with textual inference.

## Non-goals

No provenance migration, legacy-log recovery, `step-creator` work, PR thread resolution, merge, release,
post-merge action, architecture change, or unlisted implementation path belongs to B6R.
