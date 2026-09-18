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

- [X] **Actor:** Implementer — **Action:** Committed the initial exact-five planning candidate `cdf4c66ac8534a340118dca50b5e103f22335a25`; it contains only the five initial planning artifacts and no implementation or evidence path.
- [X] **Actor:** Independent Plan-Reviewer / Implementer — **Action:** The first independent review recorded `needs-rework` and Implementer committed the unchanged receipt as sole evidence commit `42d99f1d4413c95d8e362ff1a10d340f20c44a33`.
- [X] **Actor:** Plan-Creator / Implementer — **Action:** The scoped plan correction was committed as re-review candidate `63d9683f94e42bc8b6cf252adde15a014b06911e`.
- [X] **Actor:** Independent Plan-Reviewer / Implementer — **Action:** The re-review again recorded `needs-rework` and Implementer committed the unchanged receipt as sole evidence commit `5a5d7c727caaddfd354eb09569c1c34baf14d8bd`.
- [ ] **Actor:** Implementer — **Action:** Commit this corrected step tracker as the new non-merge planning candidate; do not share its commit with implementation or evidence paths.
- [ ] **Actor:** Independent Plan-Reviewer — **Action:** Review only that newly committed planning candidate and write `plan/response-reuse-eligibility-policy/response-reuse-eligibility-policy.plan-review-receipt.json` after review; do not prefill its candidate SHA from planning artifacts.
- [ ] **Actor:** Implementer — **Action:** Commit the unchanged new plan-review receipt as its own sole evidence-only commit; no other path may share that commit.
- [ ] **Actor:** Planner — **Action:** Route only a committed same-candidate fresh `approved` receipt to bounded implementation; route `needs-rework` conservatively to Plan-Creator.

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

- Current state is `needs-rework`: the initial candidate `cdf4c66ac8534a340118dca50b5e103f22335a25` and the
  re-review candidate `63d9683f94e42bc8b6cf252adde15a014b06911e` each received a committed `needs-rework` receipt.
  Plan review remains pending until a newly committed corrected planning candidate receives a fresh committed,
  same-candidate `approved` receipt; no implementation is authorized before then.
- The initial five paths are the sole initial planning candidate subject. A plan-review receipt, Tester evidence,
  and implementation-review log are evidence-only paths and must never share a commit with planning or
  implementation subject paths.
- Tester evidence must bind the exact immutable five-path implementation subject. Independent Reviewer may consume
  only committed same-topic/same-subject `passing` Tester evidence. Planner Phase 4.5 is required before any
  Human-authorized publish. Human alone reviews and merges a draft PR.
