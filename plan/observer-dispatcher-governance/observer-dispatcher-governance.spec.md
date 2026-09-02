# Observer / Dispatcher Governance Specification

> **B6R3 acceptance override:** B6R/B6R2 與下列 B6R acceptance text 均為 frozen nonrouting provenance。
> B6R3/R13 均不得建立 subject；only S11 可只改 governance contract test，保留 direct imports 且以 real
> subprocess Git query 驗證 complete `ODG_S11_SHA`/`ODG_T11_SHA`/`ODG_V11_SHA`。T11/V11 必為 exact
> non-merge `S11 -> T11 -> V11` evidence paths，`S11..V11` 僅含兩 evidence paths。Q11 是 sole read-only
> shared human boundary；Q8–Q10 不可替代，且 resolve 需 Q11 後逐 thread `addressed-and-resolvable`。

> **Frozen provenance:** `b900366`, normal/recovery records, B0–B6 (including R8/R9/R10), S1–S10, T1–T10,
> V1–V10, Q7–Q10 and all earlier correction artifacts are immutable historical provenance, excluded from B6R3.

## B6R3 Acceptance Criteria

1. B6R3 is the only current non-subject, non-merge baseline and its named first-parent admission diff contains
   exactly the seven declared B6R3 planning paths. Pre-commit B6R3 artifacts embed neither B6R3 SHA/blob SHA,
   `HEAD`, nor review outcome.
2. Independent R13 clean-checkout-reviews every B6R3 field/blob/tree and first-parent exact-seven admission, and is
   separately committed unchanged when approved. Neither B6R3 nor R13 creates `implementation_subject_sha`.
3. Only non-merge S11 establishes the subject and changes only
   `tests/test_observer_dispatcher_governance_contract.py`.
4. Direct imports remain mandatory. `importlib`, `__import__`, and `sys.modules` substitutions fail.
5. S11 tests read the B6R3 parent workflow/contract/plan/spec/step and B6R3 plan/step, reject frozen provenance
   as B6R3 routing material, and reject B6R3/R13 as implementation subject.
6. The actual Git assertion accepts only a complete explicit `ODG_S11_SHA`/`ODG_T11_SHA`/`ODG_V11_SHA` triple
   through real subprocess `git rev-parse`, `git rev-list`, and `git diff --name-status`. All values absent
   gives explicit skip/unverified; partial, invalid, `HEAD`, nonexistent, merge, wrong parent/graph, or
   multi-path input fails closed.
7. T11 and V11 are the only linear non-merge evidence-only descendants. A named `S11..V11` diff lists exactly
   the B6R3 Tester and Reviewer evidence paths. V11 requires same-S11 passing T11.
8. Q11 is post-V11, committed-full-V11-SHA-only, read-only, creates no artifact and has neither lifecycle nor
   thread authority.

## Failure Conditions

The contract fails closed if B6R3 admission is a merge, lacks/adds a path, is not its first complete
seven-path baseline, embeds SHA/`HEAD`, misses reviewed tree/blob or first-parent result, treats B6R3/R13 as subject, widens S11, replaces
direct imports, activates deferred work, uses a wrong T11/V11 path or S11, has failing T11, accepts partial
environment input, substitutes `HEAD`, accepts merge/third descendant, or replaces named S11/V11/range
verification with textual inference.

## Non-goals

No provenance migration, legacy-log recovery, `step-creator` work, PR thread resolution, merge, release,
post-merge action, architecture change, or unlisted implementation path belongs to B6R3.
