# Observer / Dispatcher Governance Specification

> **B4R2 is sole current route.** B2, B3, B4 and B4R (and all earlier/later frozen records named
> by the parent plan) are concise frozen nonrouting history, not active schemas, blockers,
> checklists, pending work, subjects or evidence.

## B4R2 Acceptance Criteria

1. B4R2 consists exactly of the six planning paths declared in the parent plan and shared contract.
2. An Independent Plan-Reviewer reviews actual committed B4R2 blobs from a clean checkout, writes
   only the unique B4R2 review record, and an Independent Implementer separately commits it unchanged.
3. Neither B4R2 commit may establish `implementation_subject_sha`; only the later non-merge S5 can.
4. S5 changes exactly the preserved 15-path allowlist in the parent plan, uses direct imports, and
   rejects `importlib`, `__import__` and `sys.modules` substitution.
5. T5 then V5 are the only evidence-only non-merge descendants; V5 requires same-S5 passing T5.
6. Actual named SHA queries prove `S5 -> T5 -> V5`; named `git diff --name-status S5..V5` lists
   exactly the B4R2 Tester and Reviewer evidence paths, never `HEAD` or inferred topology.

## Failure Conditions

The contract fails closed if an old epoch becomes current, B4R2 becomes subject, S5 widens the
allowlist, evidence has a wrong path/S5, T5 is failing, V5 is self-referential, the graph has a
merge or third descendant, or a named S5/V5/range check is replaced by `HEAD`.

## Non-goals

No legacy evidence migration, PR thread resolution, merge, release, post-merge action, architecture
change or unlisted implementation path is part of B4R2.
