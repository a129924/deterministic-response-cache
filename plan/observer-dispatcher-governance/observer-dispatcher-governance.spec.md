# Observer / Dispatcher Governance Specification

> **Frozen provenance:** `b900366` and B0–B4R5, S1–S5, T1–T5, V1–V5, normal/recovery records and
> every older correction artifact are nonrouting history. They have no current schema, blocker,
> checklist, pending work, subject, evidence, or route semantics.

## B4R6 Acceptance Criteria

1. B4R6 consists exactly of seven planning paths; no bootstrap test exception exists and the committed
   blobs remain non-subject.
2. An Independent Plan-Reviewer reviews each actual committed B4R6 blob once from a clean checkout,
   writes only its B4R6 review record, and an Independent Implementer separately commits it unchanged.
3. Neither B4R6 commit may establish `implementation_subject_sha`; only later non-merge S6 can.
4. S6 changes exactly the preserved 15-path allowlist and rejects `importlib`, `__import__`, `sys.modules`.
5. S6 tests fail closed if frozen provenance routes, B4R6/prior subjects become subject, path sets or
   B4R6 review schema mutate, direct imports change, or deferred `step-creator` work becomes in scope.
6. Fresh B4R6 T6 then V6 are the only evidence-only non-merge descendants; V6 requires same-S6 passing T6.
7. Actual named SHA queries prove `S6 -> T6 -> V6`; named `git diff --name-status S6..V6` lists
   exactly B4R6 Tester and Reviewer evidence paths, never `HEAD` or inferred topology.

## Failure Conditions

The contract fails closed if a frozen epoch becomes current, B4R6 becomes subject, the baseline lacks
or adds a path, review misses a blob, S6 widens the allowlist, evidence has a wrong path/S6, T6 is
failing, V6 is self-referential, graph has a merge or third descendant, or named S6/V6/range check is
replaced by `HEAD`.

## Non-goals

No legacy evidence migration, PR thread resolution, merge, release, post-merge action, architecture
change or unlisted implementation path is part of B4R6.
