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

- [X] **Actor:** Implementer — **Action:** Commit exactly the five correction planning artifacts declared in the
  correction plan as one non-merge planning candidate; do not include receipt, evidence, implementation, or original
  provenance paths. The immutable candidate is `48bf0eb2e1b0be7d2088acaae6f5b59df27fed7f`.
- [X] **Actor:** Independent Plan-Reviewer — **Action:** Review only that committed correction candidate and write
  `plan/response-reuse-protocol/response-reuse-protocol.vo-channel-correction.plan-review-receipt.json`, binding
  `planning_candidate_commit` to its final full 40-hex SHA only after review; its committed verdict is
  `needs-rework` because its schema lacked sufficient immutable candidate/admission provenance.
- [X] **Actor:** Implementer — **Action:** Commit that unchanged correction plan-review receipt as the sole path in
  one evidence-only commit. Do not combine it with a planning repair, implementation, or other evidence.
- [X] **Actor:** Independent Implementer — **Action:** Create this repair planning candidate by modifying only
  `response-reuse-protocol.vo-channel-correction.plan.md` and
  `response-reuse-protocol.vo-channel-correction.step.md`; its first-parent `--name-status` diff is exactly these two
  `M` paths. Do not modify the three remaining correction planning artifacts, the immutable receipt, evidence, or
  implementation paths.
- [ ] **Actor:** Independent Plan-Reviewer — **Action:** Review only this committed repair candidate and write
  `plan/response-reuse-protocol/response-reuse-protocol.vo-channel-correction.repair-plan-review-receipt.json` using
  the correction plan's exact extended schema: repair candidate commit/tree, five ordered candidate-tree
  `{path,blob_sha}` facts, and immutable original-admission commit/tree/parent/non-merge/exact-path/name-status facts.
- [ ] **Actor:** Implementer — **Action:** Commit that unchanged replacement receipt as the sole path in one
  evidence-only commit. Only its same-SHA-bound `approved` verdict may route to correction implementation.

## Implementation Steps

- [X] 1. Modify only `_cache_store.py` to define the four immutable slotted non-Exception value-object channels and
  exact non-`None` read/write unions.
- [X] 2. Modify only `protocol.py` to map exact read/write channel values via `match`／`case`, preserving opaque
  objects, treating each non-`None` nonchannel read value as `ResponseT`, and raising `TypeError` only for detectable
  channel-contract violations.
- [X] 3. Modify only `tests/test_response_reuse_protocol.py` with direct-import proof of valid mappings, read `None`
  and foreign-write `TypeError`, opaque non-`None` read passthrough, propagated exceptions, and one-call/
  payload-preservation behavior.
- [X] 4. Modify only `docs/business-capability-architecture.md` to describe the value-object port channels without
  changing existing BC boundaries.
- [X] 5. Tester runs the correction validation commands against the immutable four-path subject and writes factual
  `response-reuse-protocol.vo-channel-correction.tester-evidence.json` without committing it.
- [X] 6. Independent Implementer commits the unchanged correction Tester evidence as the sole path in one
  evidence-only commit.
- [X] 7. Independent Reviewer consumes only that committed same-subject passing evidence, writes
  `response-reuse-protocol.vo-channel-correction.implementation-review-log.json` without committing it, and an
  Independent Implementer commits it unchanged as the sole path in one evidence-only commit.

## Main Agent Actionable Steps — Fixed Tail

- [ ] Complete only source-authorised lifecycle actions.

## Handoff / Gate Notes

- The original Response Reuse planning, implementation, Tester/Reviewer evidence, pushed branch, and draft PR are
  immutable provenance. They do not satisfy this correction's candidate or subject gates and must never be modified.
- The original correction receipt is immutable `needs-rework` provenance. The replacement receipt path is
  `response-reuse-protocol.vo-channel-correction.repair-plan-review-receipt.json`; only its committed same-SHA-bound
  `approved` verdict, with the exact candidate/tree/blob/admission provenance schema, authorizes correction
  implementation. A replacement `needs-rework` returns only to Implementer for a new correction planning candidate.
- The repair candidate first-parent diff is exactly two `M` paths: the correction plan and correction step tracker.
  The independent Plan-Reviewer must verify the original five-artifact admission facts and the repair candidate's
  five candidate-tree blob facts before writing the replacement receipt.
- Only passing correction Tester evidence committed as its own sole evidence-only commit may be consumed by
  Independent Reviewer. Only committed same-subject `approved` correction Reviewer evidence may enter Planner
  Phase 4.5.
- Only the seven `## Implementation Steps` entries are the correction implementation-completion gate. Planner
  alignment plus existing Human authorization is required before any push or draft PR. Human alone reviews and merges.
