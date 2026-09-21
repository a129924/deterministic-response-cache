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
- [X] **Actor:** Implementer — **Action:** Committed the two-file workflow-correction planning candidate `724ebf129eeb99fc06b1c1cd16b58757b1b0148e`.
- [X] **Actor:** Implementer — **Action:** Sole-committed the unchanged `needs-rework` `plan-review-receipt.fix-1.json` as `dd29fe45626d5b20ffffde8d988fe4843d0924ef`.
- [X] **Actor:** Implementer — **Action:** Committed the exact-two workflow-correction planning candidate `60836827cb9ab0d42e7217eb6b560bca99108a14`.
- [X] **Actor:** Implementer — **Action:** Sole-committed the unchanged `needs-rework` `plan-review-receipt.fix-2.json` as `d4b2b3de4e451d6561a94381d0998d97957705f9`.
- [X] **Actor:** Plan-Creator — **Action:** Corrected only the exact-two workflow artifacts for the committed fix-2 blockers; no receipt, code, test, or existing evidence artifact was written.
- [ ] **Actor:** Independent Plan-Reviewer — **Action:** After Planner routes the committed exact-two correction candidate formed by this artifact set and identified by Git, write only `plan-review-receipt.fix-3.json` under the existing receipt schema, whose authoritative full SHA is supplied by that candidate and the receipt binding rather than prefilled here.

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

- Current phase is `workflow-correction-candidate / awaiting committed-candidate review route`: this exact-two
  workflow-artifact set is the correction candidate for committed fix-2 blockers. Its authoritative full SHA is
  identified only by the Git committed candidate and the `fix-3` receipt binding; it is not prefilled here. After
  Implementer commits this set unchanged as the sole two-file candidate, the next legal gate is Planner routing that
  committed candidate to a fresh Independent Plan-Reviewer, not another Plan-Creator correction.
- The six `## Implementation Steps` markers are already `[X]`; their marker-only step-progress commit remains
  `e3009d719caba782901e58ff422ab2b3869be665`. Independent Reviewer evidence committed at
  `01f80439bd9c57739e588521081406cb343645f8` applies only to the original immutable subject and cannot be
  overwritten or reused for this fix cycle.
- The next receipt path is `plan-review-receipt.fix-3.json`; only Independent Plan-Reviewer may write it after
  Planner routes a fresh committed exact-two correction candidate, and only Implementer may sole-commit it. The
  planning artifacts must not prefill that candidate SHA: Git candidate state and the future receipt binding are the
  only authority for it.
  `implementation-review-log.fix-1.json` retains its fixed subject `e6cb65d450e37e052c26e58b6001cd842d859c42` and
  Tester evidence commit `6e79af1f079c0e7031b0e5acd40c6155cefc0ad2`; all prior evidence remains immutable.
- Until the new review evidence is legally written and committed with an `approved` verdict, Planner must not enter
  Phase 4.5, and no actor may push, reply to, or resolve any PR thread. Only a later independent exact
  `addressed-and-resolvable` classification may route an Implementer to leave a bounded reply and resolve that thread.
- The initial five paths are the sole initial planning candidate subject. A plan-review receipt, Tester evidence,
  and implementation-review log are evidence-only paths and must never share a commit with planning or
  implementation subject paths. Human alone reviews and merges the PR.
