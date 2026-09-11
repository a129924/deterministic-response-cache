---
topic: response-reuse-protocol
correction: vo-channel-correction
phase: plan-authoring
created: 2026-09-12
---

# response-reuse-protocol — VO Channel Correction Step Tracking

## Workflow Stages

- [X] plan-authoring
- [ ] plan-review
- [ ] tdd-test-authoring
- [ ] implementation
- [ ] implementation-review
- [ ] code-review

## Actionable Steps

- [ ] **Actor:** Implementer — **Action:** Commit exactly the five correction planning artifacts declared in the
  correction plan as one non-merge planning candidate; do not include receipt, evidence, implementation, or original
  provenance paths.
- [ ] **Actor:** Independent Plan-Reviewer — **Action:** Review only that committed correction candidate and write
  `plan/response-reuse-protocol/response-reuse-protocol.vo-channel-correction.plan-review-receipt.json`, binding
  `planning_candidate_commit` to its final full 40-hex SHA only after review.
- [ ] **Actor:** Implementer — **Action:** Commit that unchanged correction plan-review receipt as the sole path in
  one evidence-only commit. Do not combine it with a planning repair, implementation, or other evidence.

## Implementation Steps

- [ ] 1. Modify only `_cache_store.py` to define the four immutable slotted non-Exception value-object channels and
  exact non-`None` read/write unions.
- [ ] 2. Modify only `protocol.py` to map exact read/write channel values via `match`／`case`, preserving opaque
  objects, treating each non-`None` nonchannel read value as `ResponseT`, and raising `TypeError` only for detectable
  channel-contract violations.
- [ ] 3. Modify only `tests/test_response_reuse_protocol.py` with direct-import proof of valid mappings, read `None`
  and foreign-write `TypeError`, opaque non-`None` read passthrough, propagated exceptions, and one-call/
  payload-preservation behavior.
- [ ] 4. Modify only `docs/business-capability-architecture.md` to describe the value-object port channels without
  changing existing BC boundaries.
- [ ] 5. Tester runs the correction validation commands against the immutable four-path subject and writes factual
  `response-reuse-protocol.vo-channel-correction.tester-evidence.json` without committing it.
- [ ] 6. Independent Implementer commits the unchanged correction Tester evidence as the sole path in one
  evidence-only commit.
- [ ] 7. Independent Reviewer consumes only that committed same-subject passing evidence, writes
  `response-reuse-protocol.vo-channel-correction.implementation-review-log.json` without committing it, and an
  Independent Implementer commits it unchanged as the sole path in one evidence-only commit.

## Main Agent Actionable Steps — Fixed Tail

- [ ] Complete only source-authorised lifecycle actions.

## Handoff / Gate Notes

- The original Response Reuse planning, implementation, Tester/Reviewer evidence, pushed branch, and draft PR are
  immutable provenance. They do not satisfy this correction's candidate or subject gates and must never be modified.
- Only committed same-SHA-bound `approved` correction Plan-Reviewer receipt authorizes the correction implementation
  route. A `needs-rework` receipt returns only to Implementer for a new correction planning candidate.
- Only passing correction Tester evidence committed as its own sole evidence-only commit may be consumed by
  Independent Reviewer. Only committed same-subject `approved` correction Reviewer evidence may enter Planner
  Phase 4.5.
- Only the seven `## Implementation Steps` entries are the correction implementation-completion gate. Planner
  alignment plus existing Human authorization is required before any push or draft PR. Human alone reviews and merges.
