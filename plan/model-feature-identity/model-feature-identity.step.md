---
topic: model-feature-identity
phase: plan-review
created: 2026-09-11
---

# model-feature-identity — Step Tracking

## Workflow Stages

- [X] plan-authoring
- [ ] plan-review
- [ ] tdd-test-authoring
- [ ] implementation
- [ ] implementation-review
- [ ] code-review

## Actionable Steps

- [ ] **Actor:** Independent Plan-Reviewer — **Action:** Review the committed PRF1P1 planning candidate
  against exactly the four PR #5 thread IDs/URLs and write only
  `model-feature-identity.pr-comment-prf1-prerequisite-plan-review-receipt.json`, binding the candidate's full SHA.
- [ ] **Actor:** Implementer — **Action:** Commit an unchanged approved PRF1P1 prerequisite receipt as a sole
  evidence-only commit; then create exactly one PRF1 repair subject limited to the four declared
  source/test paths.
- [ ] **Actor:** Tester — **Action:** Record actual PRF1 validation commands and exit codes only in
  `model-feature-identity.pr-comment-tester-evidence.json`; do not commit it.
- [ ] **Actor:** Independent Reviewer — **Action:** Consume the committed passing PRF1 Tester evidence
  and write only the PRF1 implementation-review log.
- [ ] **Actor:** Implementer — **Action:** Commit the unchanged approved PRF1 implementation-review log
  as a sole evidence-only commit; after Planner Phase 4.5 alignment, push the existing PR #5 lineage
  so its actual head equals that Reviewer-evidence commit.
- [ ] **Actor:** Independent Reviewer — **Action:** Only after PR #5 actually equals the committed PRF1
  Reviewer-evidence revision, classify the four exact threads in the declared resolution record using
  its permitted addressed or not-addressable per-entry schema.
- [ ] **Actor:** Implementer — **Action:** Commit the unchanged resolution record as a sole evidence-only
  commit and push it to PR #5. Only after that pushed record has all four entries
  `addressed-and-resolvable`, post each exact `reply_body` and resolve only its matching four threads.

## Implementation Steps

- [X] 1. Add `src/deterministic_response_cache/identity/contracts.py` with the declared contracts and
  retain `identity/.gitkeep` unchanged.
- [X] 2. Add `src/deterministic_response_cache/identity/builders.py` with both leaf Builder flows and
  Validator short-circuit.
- [X] 3. Add `FeatureIdentityBuilder.combine()` with fixed aggregate construction and its second full
  pipeline traversal.
- [X] 4. Add `src/deterministic_response_cache/identity/__init__.py` with the declared identity-only
  exports.
- [X] 5. Add `tests/test_model_feature_identity_contracts.py` for ABC, VO, Outcome, and Protocol
  contracts.
- [X] 6. Add `tests/test_model_feature_identity_builders.py` for stage order, failure, leaf identity,
  and composition behavior.

## Main Agent Actionable Steps — Fixed Tail

- [ ] Complete only source-authorised lifecycle actions after committed PRF1P1 approval, the required
  same-PRF1-subject evidence, Planner Phase 4.5 alignment, a push making PR #5 equal the committed
  Reviewer-evidence revision, and the subsequently committed-and-pushed four-thread classification.

## Handoff / Gate Notes

- R1–R5/S1/S2/T1/V1, PRC1 candidate `ccc5a8cba8259d990d7c929a534de1f927bbcbfa` with its `3cabeb5`
  receipt, PRCR1 candidate `b55af90425e60a8bf358bfc6c15eae3f3e4834fd` with its
  `c10cd66420f0955deffc6690063a21615a32d6b6` receipt, and PRCR1C1 candidate
  `654bc0d4a342db44b2cd3bf98dcae423160b297e` with its
  `5688fd31e82e8f71f287f80785487ed66b85f50a` receipt are immutable committed nonrouting provenance.
  After this PRF1P1 candidate commits, Planner-derived state is `PRF1P1_PLAN_REVIEW_PENDING`; no
  static R5, PRC1, PRCR1, or PRCR1C1 status is routing authority.
- PRF1P1 changes only this topic plan and this tracker. Its prerequisite receipt, PRF1 Tester evidence,
  PRF1 review log, and thread-resolution record use only their four declared new paths. PRF1 changes
  only `contracts.py`, `builders.py`, and their two direct-import test files.
- The PRCR1C1 terminal boundary is lifted only for this one PRF1P1 prerequisite candidate. Any PRF1P1
  Plan-Review failure is terminal `human-check`; no later retry, receipt, or route is authorized.
- The resolution record must bind PR #5, the actual PR #5 head that equals the committed PRF1
  Reviewer-evidence revision, that same implementation-review evidence commit, and all four fixed
  thread IDs/URLs. Each entry is either
  `addressed-and-resolvable` with non-empty `reply_body` and `verification_basis`, or
  `not-addressable` with a non-empty `blocking_issue` and no reply/resolve fields; the record may
  contain both. Any `not-addressable` entry is terminal `human-check` and authorizes no GitHub action.
  Only four addressed entries, after Implementer commits and pushes the resolution record, permit
  posting each exact `reply_body` and resolving its matching ID. Any changed/additional unresolved
  thread, dirty worktree, GitHub failure, evidence/head mismatch, unlisted path, or non-approved gate
  is `human-check`; PRC2, PRCR2, R6, retries, and scope expansion are forbidden.
- `identity/.gitkeep` is ReadOnly because `package-topology-skeleton-replay` owns it. Any modification,
  deletion, or unlisted path is a plan-alignment stop returning to Planner.
