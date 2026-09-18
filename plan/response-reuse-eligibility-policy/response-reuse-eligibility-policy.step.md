---
topic: response-reuse-eligibility-policy
phase: plan-authoring
created: 2026-09-18
---

# response-reuse-eligibility-policy — Step Tracking

## Workflow Stages

- [X] plan-authoring
- [ ] plan-review
- [ ] tdd-test-authoring
- [ ] implementation
- [ ] implementation-review
- [ ] code-review

## Actionable Steps

- [ ] **Actor:** Implementer — **Action:** Commit exactly the five initial planning artifacts as the non-merge planning candidate; do not add implementation or evidence paths to that commit.
- [ ] **Actor:** Independent Plan-Reviewer — **Action:** Review only the committed planning candidate and write `plan/response-reuse-eligibility-policy/response-reuse-eligibility-policy.plan-review-receipt.json` after review; do not prefill its candidate SHA from planning artifacts.
- [ ] **Actor:** Implementer — **Action:** Commit the unchanged plan-review receipt as its own sole evidence-only commit; no other path may share that commit.
- [ ] **Actor:** Planner — **Action:** Route only a committed same-candidate `approved` receipt to bounded implementation; route `needs-rework` conservatively to Plan-Creator.

## Implementation Steps

- [ ] 1. Create `src/deterministic_response_cache/response_reuse/eligibility/policy.py` as the sole stdlib-only eligibility leaf; add frozen/slotted field-less `ReuseAllowed` and `ReuseDenied`, their explicit union, and generic `ReuseEligibilityPolicy.evaluate(response, /)` without importing protocol, outcomes, CacheStore, Identity, or another BC.
- [ ] 2. Modify `src/deterministic_response_cache/response_reuse/protocol.py` to import the policy contracts one way, require keyword-only `eligibility_policy`, perform the exact successful-read allow/deny/invalid-decision mapping once, and preserve every non-response lookup channel plus all record behavior.
- [ ] 3. Create `tests/test_response_reuse_eligibility.py` with defining-module direct imports that verify decision frozen/slotted/distinct value semantics, union and structural Protocol typing, and the leaf module boundary without dynamic imports.
- [ ] 4. Modify `tests/test_response_reuse_protocol.py` so every constructor injects a typed fake policy while preserving its direct imports, fixtures, mocks, and assertions; add allow, deny, invalid result, policy exception, short-circuit, source-break, response identity, and record zero-call coverage.
- [ ] 5. Modify `tests/response_reuse/test_in_memory_store.py` only to inject a deterministic allow policy at `ResponseReuseProtocol` construction, retaining every existing store behavior, fixture, direct import, and assertion.
- [ ] 6. Run the declared lint, strict type, targeted, full-suite, exact-subject, package-layout, direct-import, and diff-whitespace validations; Tester later records actual commands and exit codes only after the immutable implementation subject exists.

## Main Agent Actionable Steps — Fixed Tail

- [ ] Complete only source-authorised lifecycle actions.

## Handoff / Gate Notes

- Current state is `planned`; `plan-authoring` marks only the creation of these five artifacts, not their commit,
  approval or implementation authorization.
- The five initial paths are the sole planning candidate subject. The plan-review receipt, Tester evidence and
  implementation-review log are later evidence-only paths and must never share a commit with planning or
  implementation subject paths.
- Tester evidence must bind the exact immutable five-path implementation subject. Independent Reviewer may consume
  only committed same-topic/same-subject `passing` Tester evidence. Planner Phase 4.5 is required before any
  Human-authorized publish. Human alone reviews and merges a draft PR.
