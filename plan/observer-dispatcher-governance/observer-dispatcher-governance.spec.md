# Observer / Dispatcher Governance Specification

> **B4R4 is sole current route.** `8b87aab` B4R3 clean-checkout review is failed frozen provenance.
> B0–B4R3, S1–S4, T1–T4, V1–V4 and normal/recovery records are not active schemas, blockers,
> checklists, pending work, subjects or evidence. `step-creator` threads remain deferred.

## B4R3 Acceptance Criteria

1. B4R4 consists exactly of the seven planning paths plus the declared test path. Independent
   Implementer may change that test before planning review only under the bootstrap exception; the
   committed eight blobs remain non-subject.
2. Bootstrap test adaptation directly reads workflow/contract, parent plan/spec/step and B4R4
   plan/step; it asserts frozen prior epochs, B4R4 non-subject, exact eight-path baseline, clean
   eight-blob review, preserved S5 allowlist, direct imports, deferred `step-creator`, and fresh B4R4
   evidence topology/range; mutation checks fail closed for each condition.
3. An Independent Plan-Reviewer reviews actual committed B4R4 eight blobs from a clean checkout,
   writes only unique B4R4 review record, and an Independent Implementer separately commits it unchanged.
4. Neither B4R4 commit may establish `implementation_subject_sha`; only later non-merge S5 can.
5. S5 changes exactly preserved 15-path allowlist and rejects `importlib`, `__import__`, `sys.modules`.
6. Fresh B4R4 T5 then V5 are only evidence-only non-merge descendants; V5 requires same-S5 passing T5.
7. Actual named SHA queries prove `S5 -> T5 -> V5`; named `git diff --name-status S5..V5` lists
   exactly B4R4 Tester and Reviewer evidence paths, never `HEAD` or inferred topology.

## Failure Conditions

The contract fails closed if a frozen epoch becomes current, B4R4 becomes subject, the baseline lacks
or adds a path, bootstrap test work exceeds fixed assertions, review misses a blob, S5 widens the
allowlist, evidence has a wrong path/S5, T5 is failing, V5 is self-referential, graph has a merge or
third descendant, or named S5/V5/range check is replaced by `HEAD`.

## Non-goals

No legacy evidence migration, PR thread resolution, merge, release, post-merge action, architecture
change or unlisted implementation path is part of B4R4.
