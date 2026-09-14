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

- [ ] **Actor:** Independent Plan-Reviewer — **Action:** Review the committed PRC1 planning candidate
  against exactly the four PR #5 thread IDs/URLs and write only
  `model-feature-identity.pr-comment-plan-review-receipt.json`, binding the candidate's full SHA.
- [ ] **Actor:** Implementer — **Action:** Commit an unchanged approved PRC1 receipt as a sole
  evidence-only commit; then create exactly one PRF1 repair subject limited to the four declared
  source/test paths.
- [ ] **Actor:** Tester — **Action:** Record actual PRF1 validation commands and exit codes only in
  `model-feature-identity.pr-comment-tester-evidence.json`; do not commit it.
- [ ] **Actor:** Independent Reviewer — **Action:** Consume the committed passing PRF1 Tester evidence,
  write only the PRF1 implementation-review log, and after Planner Phase 4.5 classify only the four
  exact threads in the declared resolution record using its permitted addressed or not-addressable
  per-entry schema.
- [ ] **Actor:** Implementer — **Action:** Commit each unchanged Reviewer artifact as its sole
  evidence-only commit; only after a committed record with all four entries
  `addressed-and-resolvable`, push the existing repair lineage, post each exact `reply_body`, and
  resolve only its matching four threads.

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

- [ ] Complete only source-authorised lifecycle actions after committed PRC1 approval, the required
  same-PRF1-subject evidence, Planner Phase 4.5 alignment, and committed four-thread classification.

## Handoff / Gate Notes

- R1–R5/S1/S2/T1/V1 are immutable committed nonrouting provenance. After this PRC1 candidate commits,
  Planner-derived state is `PRC1_PLAN_REVIEW_PENDING`; no static R5 status is routing authority.
- PRC1 changes only the technical spec, topic plan, topic spec, and this tracker. Its receipt, PRF1
  Tester evidence, PRF1 review log, and thread-resolution record use only their four declared new
  paths. PRF1 changes only `contracts.py`, `builders.py`, and their two direct-import test files.
- The resolution record must bind PR #5, the actual reviewed repair head, the implementation-review
  evidence commit, and all four fixed thread IDs/URLs. Each entry is either
  `addressed-and-resolvable` with non-empty `reply_body` and `verification_basis`, or
  `not-addressable` with a non-empty `blocking_issue` and no reply/resolve fields; the record may
  contain both. Any `not-addressable` entry is terminal `human-check` and authorizes no GitHub action.
  Only four addressed entries permit posting each exact `reply_body` and resolving its matching ID.
  Any changed/additional unresolved thread, dirty worktree, GitHub failure, evidence/head mismatch,
  unlisted path, or non-approved gate is `human-check`; PRC2, R6, retries, and scope expansion are
  forbidden.
- `identity/.gitkeep` is ReadOnly because `package-topology-skeleton-replay` owns it. Any modification,
  deletion, or unlisted path is a plan-alignment stop returning to Planner.
