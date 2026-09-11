---
topic: model-feature-identity
phase: plan-authoring
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

- [ ] **Actor:** Independent Plan-Reviewer — **Action:** Review the committed R4 planning-correction
  candidate and write only the declared R4 receipt. Only a committed `approved` R4 receipt permits
  the bounded S2 step-tracker reconciliation subject.
- [ ] **Actor:** Implementer — **Action:** After committed R4 approval only, create S2 with a subject
  diff limited to this tracker and limited within it to marking the six `## Implementation Steps` as
  complete; then follow the declared S2 Tester → Reviewer evidence chain.

## Implementation Steps

- [ ] 1. Add `src/deterministic_response_cache/identity/contracts.py` with the declared contracts and
  retain `identity/.gitkeep` unchanged.
- [ ] 2. Add `src/deterministic_response_cache/identity/builders.py` with both leaf Builder flows and
  Validator short-circuit.
- [ ] 3. Add `FeatureIdentityBuilder.combine()` with fixed aggregate construction and its second full
  pipeline traversal.
- [ ] 4. Add `src/deterministic_response_cache/identity/__init__.py` with the declared identity-only
  exports.
- [ ] 5. Add `tests/test_model_feature_identity_contracts.py` for ABC, VO, Outcome, and Protocol
  contracts.
- [ ] 6. Add `tests/test_model_feature_identity_builders.py` for stage order, failure, leaf identity,
  and composition behavior.

## Main Agent Actionable Steps — Fixed Tail

- [ ] Complete only source-authorised lifecycle actions after committed R4 approval, the required
  same-S2-subject evidence, and Planner alignment gates.

## Handoff / Gate Notes

- R1/R2/R3/T1/V1 are immutable committed provenance. The only current route is R4, whose independent
  Plan-Reviewer receipt must be committed with `verdict: "approved"` before S2 exists.
- S2 may change only this file and only the six unchecked entries under `## Implementation Steps` to
  `[X]`; no other tracker text, Python, tests, `.gitkeep`, planning artifact, or evidence path is
  authorized in its subject. Tester evidence and Independent Reviewer evidence must bind the same S2
  subject; then Planner Phase 4.5 decides whether bounded publish is eligible.
- R4 `needs-rework`, failing S2 Tester evidence, or S2 Reviewer `needs-rework` stops at Human. R5,
  an alternate S2 subject, and any route extension are forbidden.
- `identity/.gitkeep` is ReadOnly because `package-topology-skeleton-replay` owns it. Any modification,
  deletion, or unlisted path is a plan-alignment stop returning to Planner.
