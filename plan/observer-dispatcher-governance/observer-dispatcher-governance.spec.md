# Observer / Dispatcher Governance Specification

> **Frozen provenance:** `b900366`, B0–B4R6, S1–S5, T1–T5, V1–V5, normal/recovery records,
> `7d23e8c`, `6ede06b`, all older correction artifacts, and any uncommitted B4R6 review-log are
> nonrouting history. None supplies a current candidate, gate, subject, schema, or pending work.

## B4R7 Acceptance Criteria

1. B4R7 is a non-subject, non-merge baseline whose first admission commit contains exactly the seven
   declared planning paths in its named first-parent diff. The pre-commit artifacts embed neither a SHA
   nor `HEAD`.
2. Independent R7 reviews every actual B4R7 committed blob once and its approved record is separately
   committed unchanged; neither B4R7 nor R7 creates `implementation_subject_sha`.
3. Only non-merge S6 may establish the subject and it changes exactly the preserved 15-path allowlist.
4. Direct imports remain mandatory; `importlib`, `__import__`, and `sys.modules` substitutions fail.
5. S6 tests fail closed for frozen provenance, B4R7/R7 subject misuse, altered B4R7 admission paths,
   wrong R7 schema, allowlist drift, or deferred `step-creator` work becoming in scope.
6. Fresh B4R7 T6 then V6 are the only evidence-only non-merge descendants; V6 requires same-S6 passing
   T6.
7. Actual named SHA queries prove `S6 -> T6 -> V6`; named `git diff --name-status S6..V6` lists exactly
   B4R7 Tester and Reviewer evidence paths, never `HEAD` or inferred topology.

## Failure Conditions

The contract fails closed if the B4R7 admission commit is a merge, lacks/adds a path, is not its first
complete seven-path baseline, uses embedded SHA/`HEAD`, misses a reviewed blob, treats B4R7/R7 as subject,
widens S6, substitutes imports, activates deferred work, uses a wrong T6/V6 path or S6, has a failing T6,
uses merge/third descendant, or replaces named S6/V6/range verification with `HEAD`.

## Non-goals

No legacy evidence migration, B4R6 log recovery, PR thread resolution, merge, release, post-merge action,
architecture change, or unlisted implementation path is part of B4R7.

## B5 Current Acceptance Criteria

All B4R7/S6/T6/missing-V6 content above is frozen provenance. B5 admission is exact seven planning paths,
non-merge, non-subject, and SHA/blob-SHA/`HEAD`/review-outcome free before commit; R8 independently reviews
the committed seven blobs and is separately committed unchanged. S7 is the only non-merge subject and edits
only `tests/test_observer_dispatcher_governance_contract.py`.

S7 actual checks use only all three explicit `ODG_S7_SHA`, `ODG_T7_SHA`, `ODG_V7_SHA` variables and subprocess
real `git rev-parse`, `git rev-list`, `git diff --name-status`; absent all three explicitly skips, while
missing/partial/`HEAD`/nonexistent/merge/wrong-parent/multi-path values fail closed. T7/V7 must be the sole
linear descendants. Q7 is a no-artifact post-V7 full-SHA read-only query and has no lifecycle or thread
authority.
