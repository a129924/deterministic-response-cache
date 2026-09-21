---
topic: response-reuse-eligibility-policy
phase: review-evidence-capability-repair
created: 2026-09-18
---

# response-reuse-eligibility-policy — Step Tracking

## Workflow Stages

- [X] plan-authoring
- [X] plan-review
- [X] tdd-test-authoring
- [X] implementation
- [X] implementation-review
- [ ] code-review

## Actionable Steps

- [X] **Actor:** Implementer — **Action:** Committed the exact-five corrected planning candidate `43a255f03b69be94e56abcc7ca13bf684e3395f3`.
- [X] **Actor:** Independent Plan-Reviewer / Implementer — **Action:** Independently approved candidate `43a255f03b69be94e56abcc7ca13bf684e3395f3`; Implementer committed the unchanged approved receipt as sole evidence commit `8b6658014674ab3a304115e130e58d295d804c7d`.
- [X] **Actor:** Tester / Implementer — **Action:** Tested immutable exact-five implementation subject `695888bb72927b301f4f98e38d3587824803f263`; Implementer committed the passing Tester evidence as sole evidence commit `e531a84a6fc48187af3137ada0634e876afc5365`.
- [X] **Actor:** Implementer — **Action:** Marked the six `## Implementation Steps` markers complete in the sole step-progress commit `e3009d719caba782901e58ff422ab2b3869be665`.
- [X] **Actor:** Independent Reviewer / Implementer — **Action:** Consumed the committed passing same-subject Tester evidence, recorded an approved review, and committed that unchanged review evidence as sole evidence commit `01f80439bd9c57739e588521081406cb343645f8`.
- [X] **Actor:** Implementer — **Action:** Created the bounded code implementation subject `e6cb65d450e37e052c26e58b6001cd842d859c42` for the two shared code `needs-fix` threads.
- [X] **Actor:** Tester / Implementer — **Action:** Tested that subject and committed the passing Tester evidence as sole evidence commit `6e79af1f079c0e7031b0e5acd40c6155cefc0ad2`.
- [ ] **Actor:** Plan-Creator / Implementer / Independent Plan-Reviewer — **Action:** Commit this two-file `review-evidence-capability-repair` planning candidate, then write and sole-commit the new `plan-review-receipt.fix-1.json` under the existing receipt schema; do not modify prior evidence files.
- [ ] **Actor:** Independent Reviewer / Implementer — **Action:** Only after the committed approved fix-1 Plan-Reviewer receipt, write and sole-commit `implementation-review-log.fix-1.json` using the existing review schema and the fixed subject/Tester evidence bindings.

## Implementation Steps

- [X] 1. Create `src/deterministic_response_cache/response_reuse/eligibility/policy.py` as the sole stdlib-only eligibility leaf; add frozen/slotted field-less `ReuseAllowed` and `ReuseDenied`, their explicit union, and generic `ReuseEligibilityPolicy.evaluate(response, /)` without importing protocol, outcomes, CacheStore, Identity, or another BC.
- [X] 2. Modify `src/deterministic_response_cache/response_reuse/protocol.py` to import the policy contracts one way, require keyword-only `eligibility_policy`, perform the exact successful-read allow/deny/invalid-decision mapping once, and preserve every non-response lookup channel plus all record behavior.
- [X] 3. Create `tests/test_response_reuse_eligibility.py` with defining-module direct imports that verify decision frozen/slotted/distinct value semantics, union and structural Protocol typing, and the leaf module boundary without dynamic imports.
- [X] 4. Modify `tests/test_response_reuse_protocol.py` so every constructor injects a typed fake policy while preserving its direct imports, fixtures, mocks, and assertions; add allow, deny, invalid result, policy exception, short-circuit, source-break, response identity, and record zero-call coverage.
- [X] 5. Modify `tests/response_reuse/test_in_memory_store.py` only to inject a deterministic allow policy at `ResponseReuseProtocol` construction, retaining every existing store behavior, fixture, direct import, and assertion.
- [X] 6. Run the declared lint, strict type, targeted, full-suite, exact-subject, package-layout, direct-import, and diff-whitespace validations; Tester later records actual commands and exit codes only after the immutable implementation subject exists.

## Main Agent Actionable Steps — Fixed Tail

- [ ] Complete only source-authorised lifecycle actions.

## Handoff / Gate Notes

- Current phase is `review-evidence-capability-repair / plan-review-pending`: bounded code implementation subject
  `e6cb65d450e37e052c26e58b6001cd842d859c42` has passing Tester evidence committed at
  `6e79af1f079c0e7031b0e5acd40c6155cefc0ad2`. Independent Reviewer substantive review is complete, but the
  original immutable implementation-review-log path has no lawful place to record this fix-cycle assessment; that
  uncommitted assessment is not routing authority and is not approved evidence.
- The six `## Implementation Steps` markers are already `[X]`; their marker-only step-progress commit remains
  `e3009d719caba782901e58ff422ab2b3869be665`. Independent Reviewer evidence committed at
  `01f80439bd9c57739e588521081406cb343645f8` applies only to the original immutable subject and cannot be
  overwritten or reused for this fix cycle.
- This repair adds only the dedicated `plan-review-receipt.fix-1.json` and
  `implementation-review-log.fix-1.json` evidence capabilities. The former must bind the committed
  workflow-correction planning candidate under the existing receipt schema. The latter must bind
  `e6cb65d450e37e052c26e58b6001cd842d859c42` and
  `6e79af1f079c0e7031b0e5acd40c6155cefc0ad2` under the existing review schema. Existing evidence paths and
  contents remain immutable.
- Until the new review evidence is legally written and committed with an `approved` verdict, Planner must not enter
  Phase 4.5, and no actor may push, reply to, or resolve any PR thread. Only a later independent exact
  `addressed-and-resolvable` classification may route an Implementer to leave a bounded reply and resolve that thread.
- The initial five paths are the sole initial planning candidate subject. A plan-review receipt, Tester evidence,
  and implementation-review log are evidence-only paths and must never share a commit with planning or
  implementation subject paths. Human alone reviews and merges the PR.
