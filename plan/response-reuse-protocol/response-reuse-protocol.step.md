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

- [ ] **Actor:** Implementer — **Action:** Commit exactly the five initial planning artifacts as the planning candidate; do not add implementation or evidence paths to that commit.
- [ ] **Actor:** Independent Plan-Reviewer — **Action:** Review only the committed planning candidate and write the declared plan-review receipt.

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

## Handoff / Gate Notes

- An independent Plan-Reviewer must approve the committed planning candidate before implementation.
- Only the seven `## Implementation Steps` entries are the implementation-completion gate.
- Tester evidence must bind the exact immutable implementation subject. Independent Reviewer may consume only committed passing same-subject Tester evidence. Human alone reviews and merges a draft PR.
