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
- [X] **Actor:** Independent Implementer — **Action:** Commit only the earlier bounded planning-state repair as historical candidate `a2941d99201cf0aee95b71008c3f1d4e690a8770`; it is not replacement-route evidence.
- [X] **Actor:** Independent Implementer — **Action:** Commit exactly `response-reuse-protocol.plan.md` and `response-reuse-protocol.step.md` as this one-time repair planning candidate; retain the old receipt and prior candidate as immutable provenance and do not add implementation paths.
- [ ] **Actor:** Independent Plan-Reviewer — **Action:** Review only this committed repair planning candidate and, after review, write `plan/response-reuse-protocol/response-reuse-protocol.repair-plan-review-receipt.json`; its `planning_candidate_commit` must be the reviewed candidate's full 40-hex SHA and is never prefilled by a planning artifact.
- [ ] **Actor:** Implementer — **Action:** Commit the replacement receipt unchanged as a sole, single-file evidence-only commit; no other path may share that commit.

## Implementation Steps

- [X] 1. Update the five declared architecture surfaces to remove Identity implementation completion as a Response Reuse gate while preserving Identity authority, CacheStore internal-only ownership, future BC separations, and the synchronized outcome flow.
- [X] 2. Add `src/deterministic_response_cache/response_reuse/outcomes.py` with frozen slotted generic lookup and record outcome types plus their union aliases.
- [X] 3. Add `src/deterministic_response_cache/response_reuse/_cache_store.py` with the generic synchronous internal `CacheStore` port and `CacheStoreFailure` operational-failure boundary.
- [X] 4. Add `src/deterministic_response_cache/response_reuse/protocol.py` with `ResponseReuseProtocol.lookup` and `record` exactly as specified, without inspecting identity or implementing downstream execution.
- [X] 5. Add `tests/test_response_reuse_outcomes.py` for outcome value semantics and payload preservation using direct imports.
- [X] 6. Add `tests/test_response_reuse_protocol.py` with typed fake CacheStore tests for Hit, Miss, Unavailable, Cached, NotCached, single port calls, opaque identity handoff, and propagation of non-`CacheStoreFailure` exceptions.
- [X] 7. Run the declared format, type-check, targeted test, full test, and topology/import regression commands; record their actual exit codes in Tester evidence after the immutable implementation subject exists.

## Main Agent Actionable Steps — Fixed Tail

- [ ] Complete only source-authorised lifecycle actions.

## Handoff / Gate Notes

- The original candidate's committed `needs-rework` receipt at
  `plan/response-reuse-protocol/response-reuse-protocol.plan-review-receipt.json` and provenance commit
  `b6258d9247d6525ed7c2ba279dbb44ca711440d8` are immutable and are not routing authority. The prior state candidate
  `a2941d99201cf0aee95b71008c3f1d4e690a8770` is likewise not replacement-route evidence.
- The current repair candidate awaits an independent replacement Plan-Reviewer receipt at
  `plan/response-reuse-protocol/response-reuse-protocol.repair-plan-review-receipt.json`. That receipt must be
  written only by Independent Plan-Reviewer. Only after review does that reviewer fill its
  `planning_candidate_commit` with the reviewed candidate's full 40-hex SHA; planning artifacts do not prefill any
  candidate SHA. Implementer alone commits the unchanged receipt as a sole evidence-only commit.
- Only a committed, same-SHA-bound replacement receipt with verdict `approved` may enter implementation; a
  replacement `needs-rework` returns to Implementer for a new candidate.
- Only the seven `## Implementation Steps` entries are the implementation-completion gate.
- Tester evidence must bind the exact immutable implementation subject. Independent Reviewer may consume only committed passing same-subject Tester evidence. Human alone reviews and merges a draft PR.
