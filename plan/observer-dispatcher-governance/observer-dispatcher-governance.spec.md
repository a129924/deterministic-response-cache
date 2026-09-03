# Observer / Dispatcher Governance Specification

## B6R10 Acceptance Criteria

1. B6R10 -> R20 -> S16 -> T16 -> V16 -> Q16 is the sole current route; B6R9/Q15 and earlier evidence are frozen.
2. B6R10 is a non-subject, non-merge first-parent exact-eleven planning baseline. R20 uses the declared extended JSON
   correction-record schema with candidate commit/tree, eleven path/blob pairs, admission, verdict/blockers and triage.
3. Only committed approved R20 creates one active candidate and permits S16; `needs-rework` creates no route.
4. S16 alone changes the existing test, retains direct imports, and rejects dynamic import substitution.
5. S16 validates committed T16/V16 paths/topology and evidence blobs semantically declare one same full S16 SHA, T16
   `passing` and V16 `APPROVED`.
6. Q16 is actual full-triple, evidence-only and can create only the active-candidate close record; it never permits merge.
7. Reviewer implementation verification is separate from Human PR review and merge.
8. T16 is a single exact-key JSON object binding only S16's 40-character lowercase hexadecimal SHA and sole test path
   to one `passing` zero-exit run; missing, extra, malformed, abbreviated, non-hex, or inconsistent data fails closed.
9. V16 is a single exact-key JSON object binding same-S16 and committed T16 commit/path/blob/subject/status, with
   uppercase `APPROVED` and empty blockers; Q16 is written only after committed V16 and becomes active only when an
   independent Implementer commits it unchanged as sole evidence-only path.
10. Q16 is a single exact-key JSON object binding committed S16/T16/V16 commit/parent/path/blob facts, same-S16
    parsed claims, `passing`/`APPROVED`, actual Git full triple/linear/`S16..V16`/name-status, and only
    `ACTIVE_CANDIDATE_CLOSED` classification permission. It contains no Q16 self commit/tree/blob and forbids thread
    resolve, Human review, merge, release, and post-merge.

## Frozen B6R9 Provenance

B6R9/R19/S15/T15/V15/Q15, their acceptance conditions, failures, non-goals and evidence are immutable predecessor
provenance. They create no current candidate, phase, subject, gate, thread authority, or implementation obligation.
They are not amended, recovered, or used to infer the B6R10 route.

## Failure Conditions

The contract fails closed if a prior route is treated as current; B6R10 admission is merge/not-exact-eleven; R20 lacks
required tree/blob/admission/triage fields; B6R10/R20 is treated as subject; S16 widens paths or replaces direct
imports; T16/V16 names another path or subject; topology differs from S16 -> T16 -> V16; evidence semantics do not
declare the same full S16 SHA with T16 `passing` and V16 `APPROVED`; actual input is invalid; or Q16 gains PR, lifecycle,
resolution, or merge authority.

## Non-goals

No B6R9 recovery or provenance migration, legacy-log recovery, step-creator work, thread resolution, merge, release,
post-merge action, architecture work, or unlisted implementation path belongs to B6R10.
