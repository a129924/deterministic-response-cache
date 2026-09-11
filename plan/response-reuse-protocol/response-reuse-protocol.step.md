---
topic: response-reuse-protocol
phase: plan-authoring
created: 2026-09-11
---

# response-reuse-protocol — Step Tracking

## Workflow Stages

- [X] plan-authoring
- [ ] plan-review
- [ ] tdd-test-authoring
- [ ] implementation
- [ ] implementation-review
- [ ] code-review

## Actionable Steps

- [X] **Actor:** Implementer — **Action:** Commit exactly the five initial planning artifacts as the original planning candidate; do not add implementation or evidence paths to that commit.
- [X] **Actor:** Independent Plan-Reviewer — **Action:** Review the original committed planning candidate and write the declared `needs-rework` receipt.
- [X] **Actor:** Implementer — **Action:** Commit the original `needs-rework` receipt unchanged as its own evidence-only provenance commit.
- [ ] **Actor:** Independent Plan-Reviewer — **Action:** Review only the committed recovery planning candidate and write `plan/response-reuse-protocol/response-reuse-protocol.recovery-plan-review-receipt.json`; its `planning_candidate_commit` must be the reviewed candidate's full 40-hex SHA and is never prefilled by planning artifacts. A `needs-rework` verdict is terminal `human-check`.
- [ ] **Actor:** Implementer — **Action:** Commit the recovery receipt unchanged as a sole, single-file evidence-only commit; no other path may share that commit.
- [ ] **Actor:** Implementer — **Action:** From the committed approved recovery receipt, create one direct-child, non-merge replacement implementation subject changing exactly the ten declared implementation paths; it must implement `NotCached(response)` and no other path may change.
- [ ] **Actor:** Tester — **Action:** Write only `plan/response-reuse-protocol/response-reuse-protocol.tester-evidence-recovery.json` with factual same-subject results. A failing result is terminal `human-check`.
- [ ] **Actor:** Independent Implementer — **Action:** Commit the passing recovery Tester evidence unchanged as a sole, single-file evidence-only commit.
- [ ] **Actor:** Independent Reviewer — **Action:** Consume only that committed passing recovery Tester evidence and write only `plan/response-reuse-protocol/response-reuse-protocol.implementation-review-log-recovery.json`. A `needs-rework` verdict is terminal `human-check`.
- [ ] **Actor:** Independent Implementer — **Action:** Commit the approved recovery review evidence unchanged as a sole, single-file evidence-only commit.

## Implementation Steps

- [ ] 1. Update the five declared architecture surfaces to remove Identity implementation completion as a Response Reuse gate while preserving Identity authority, CacheStore internal-only ownership, future BC separations, and the synchronized outcome flow.
- [ ] 2. Add `src/deterministic_response_cache/response_reuse/outcomes.py` with frozen slotted generic lookup and record outcome types plus their union aliases.
- [ ] 3. Add `src/deterministic_response_cache/response_reuse/_cache_store.py` with the generic synchronous internal `CacheStore` port and `CacheStoreFailure` operational-failure boundary.
- [ ] 4. Add `src/deterministic_response_cache/response_reuse/protocol.py` with `ResponseReuseProtocol.lookup` and `record` exactly as specified, without inspecting identity or implementing downstream execution.
- [ ] 5. Add `tests/test_response_reuse_outcomes.py` for outcome value semantics and payload preservation using direct imports.
- [ ] 6. Add `tests/test_response_reuse_protocol.py` with typed fake CacheStore tests for Hit, Miss, Unavailable, Cached, NotCached, single port calls, opaque identity handoff, and propagation of non-`CacheStoreFailure` exceptions.
- [ ] 7. Run the declared format, type-check, targeted test, full test, and topology/import regression commands; record their actual exit codes in Tester evidence after the immutable implementation subject exists.

## Main Agent Actionable Steps — Fixed Tail

- [ ] Complete only source-authorised lifecycle actions.

## One-time Reconciliation Route

The original, alternate, and recovery routes are immutable historical nonrouting provenance. The active route starts
with the exact two-file reconciliation planning candidate containing this tracker and the topic plan. Its only
Plan-Reviewer receipt is `plan/response-reuse-protocol/response-reuse-protocol.reconciliation-plan-review-receipt.json`,
which must bind that candidate's final full 40-hex SHA. After its committed `approved` receipt, the sole
reconciliation implementation subject may change only this file and exactly the seven `## Implementation Steps`
checkbox tokens from `[ ]` to `[X]`. Its only Tester and Reviewer paths are
`plan/response-reuse-protocol/response-reuse-protocol.tester-evidence-reconciliation.json` and
`plan/response-reuse-protocol/response-reuse-protocol.implementation-review-log-reconciliation.json`. Any
reconciliation Plan-Reviewer, Tester, or Independent Reviewer failure is terminal `human-check`; no retry,
replacement, or later receipt/evidence path is allowed.

## Handoff / Gate Notes

- `b6258d9247d6525ed7c2ba279dbb44ca711440d8`, `a2941d99201cf0aee95b71008c3f1d4e690a8770`,
  `9c65df1e57938aafada691932d8a815854a1db9b`, `86f84c834739e4114039a8c836d256b2216954ce`,
  `e6e6747f21fa02fe653894c6e99273f1f6f91a4a`, `4b233722d86db8d3bfdca4850d6ce41578ff4cb4`,
  `b653460b737930ff0bcfdc4c910288cdc51e1c4d`, `c6e9a13f3af4174963d2a175b40d6643ca9de5a7`,
  `0bb39160bbe2027cf9e07c5e8868c8bac8dfbf38`, `3183e94022c18c8fc62acf0943b8947057875bf8`,
  `ac2edec48f8d609923837a2dc97d3dd6d8a67916`, `fc285139eb64c4f114a9dc24de3f12232b7ae780`, and
  `6c36a79b15d6b3d10e4c3fda5d255ce2ef63255f` are immutable
  frozen nonrouting provenance, including all old receipt, Tester, Reviewer, implementation, and step-state
  artifacts. They never select a reconciliation candidate or satisfy a reconciliation gate.
- Only the seven `## Implementation Steps` entries are the implementation-completion gate.
- Reconciliation Tester evidence must bind the exact immutable one-file subject. Independent Reviewer may consume
  only committed passing same-subject reconciliation Tester evidence. Human alone reviews and merges a draft PR.
