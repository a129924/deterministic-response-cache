# Observer / Dispatcher Governance Specification

> **B6R4 acceptance override:** B6R–B6R3 與下列 historical acceptance text 均為 frozen nonrouting provenance。
> B6R4/R14 均不得建立 subject；only S12 可只改 governance contract test，保留 direct imports 且以 real
> subprocess Git query 驗證 complete `ODG_S12_SHA`/`ODG_T12_SHA`/`ODG_V12_SHA`。T12/V12 必為 exact
> non-merge `S12 -> T12 -> V12` evidence paths，`S12..V12` 僅含兩 evidence paths。Q12 是 sole read-only
> shared human boundary；Q8–Q10 不可替代，且 resolve 需 Q11 後逐 thread `addressed-and-resolvable`。

> **Frozen provenance:** `b900366`, normal/recovery records, B0–B6 (including R8/R9/R10), S1–S10, T1–T10,
> V1–V10, Q7–Q11 and all earlier correction artifacts are immutable historical provenance, excluded from B6R4.

## B6R4 Acceptance Criteria

1. B6R4 is the only current non-subject, non-merge baseline and its named first-parent admission diff contains
   exactly the seven declared B6R4 planning paths. Pre-commit B6R4 artifacts embed neither B6R4 SHA/blob SHA,
   `HEAD`, nor review outcome.
2. Independent R14 clean-checkout-reviews every B6R4 field/blob/tree and first-parent exact-seven admission, and is
   separately committed unchanged when approved. Neither B6R4 nor R14 creates `implementation_subject_sha`.
3. Only non-merge S12 establishes the subject and changes only
   `tests/test_observer_dispatcher_governance_contract.py`.
4. Direct imports remain mandatory. `importlib`, `__import__`, and `sys.modules` substitutions fail.
5. S12 tests read the B6R4 parent workflow/contract/plan/spec/step and B6R4 plan/step, reject frozen provenance
   as B6R4 routing material, and reject B6R4/R14 as implementation subject.
6. The actual Git assertion accepts only a complete explicit `ODG_S12_SHA`/`ODG_T12_SHA`/`ODG_V12_SHA` triple
   through real subprocess `git rev-parse`, `git rev-list`, and `git diff --name-status`. All values absent
   gives explicit skip/unverified; partial, invalid, `HEAD`, nonexistent, merge, wrong parent/graph, or
   multi-path input fails closed.
7. T12 and V12 are the only linear non-merge evidence-only descendants. A named `S12..V12` diff lists exactly
   the B6R4 Tester and Reviewer evidence paths. V12 requires same-S12 passing T12.
8. Q12 is post-V12, committed-full-V12-SHA-only, read-only, creates no artifact and has neither lifecycle nor
   thread authority.

## Failure Conditions

The contract fails closed if B6R4 admission is a merge, lacks/adds a path, is not its first complete
seven-path baseline, embeds SHA/`HEAD`, misses reviewed tree/blob or first-parent result, treats B6R4/R14 as subject, widens S12, replaces
direct imports, activates deferred work, uses a wrong T12/V12 path or S12, has failing T12, accepts partial
environment input, substitutes `HEAD`, accepts merge/third descendant, or replaces named S12/V12/range
verification with textual inference.

## Non-goals

No provenance migration, legacy-log recovery, `step-creator` work, PR thread resolution, merge, release,
post-merge action, architecture change, or unlisted implementation path belongs to B6R4.
