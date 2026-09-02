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

## Frozen B5 provenance

All B4R7/S6/T6/missing-V6 content above, B5/R8 and all older epochs are frozen provenance; none is current,
pending, candidate or gate.

## B5R Current Acceptance Criteria

B5R is the sole current, non-subject, non-merge seven-planning-path baseline; its pre-commit artifacts embed
no B5R SHA/blob SHA/`HEAD`/review outcome. R9 independently reviews every committed B5R blob and is separately
committed unchanged. Only approved R9 permits test-only non-merge S7. Direct imports remain mandatory and
`step-creator` remains deferred.

The S7 actual Git graph assertion reads only all three explicit `ODG_S7_SHA`, `ODG_T7_SHA`, `ODG_V7_SHA` values
through subprocess real `git rev-parse`, `git rev-list`, `git diff --name-status`. It is explicitly
skip/unverified only when all three are absent. Partial/invalid/`HEAD`/nonexistent/merge/wrong-parent-or-graph/
multi-path values fail closed. T7 executes it using a complete real triple and records a non-skipped passing
result. T7/V7 are the only linear non-merge descendants and named `S7..V7` lists exactly their B5R evidence
paths; Q7 remains full-V7-SHA read-only, no-artifact, without lifecycle or thread authority.
