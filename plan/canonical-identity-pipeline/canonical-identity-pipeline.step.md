---
topic: canonical-identity-pipeline
phase: correction-plan-review
created: 2026-09-14
---

# canonical-identity-pipeline — Step Tracking

## Workflow Stages

- [X] plan-authoring
- [X] plan-review (initial candidate)
- [X] CAVO1 correction-plan-authoring
- [ ] CAVO1 correction-plan-review
- [ ] tdd-test-authoring
- [ ] implementation
- [ ] implementation-review
- [ ] code-review

## CAVO1 Actionable Steps

- [ ] **Actor:** Independent Plan-Reviewer — **Action:** Review the committed six-path CAVO1
  correction planning candidate from a clean checkout and write only
  `canonical-identity-pipeline.archify-visual-overflow.correction-plan-review-log.json` using the
  extended correction schema.
- [ ] **Actor:** Independent Implementer — **Action:** Commit unchanged approved CAVO1
  Plan-Reviewer evidence as the sole evidence-only commit. No source path is modified in this step.
- [ ] **Actor:** Implementer — **Action:** After Planner route, run at most two focused Archify
  geometry/content rounds. Modify only the declared JSON/HTML diagram paths, preserve all pipeline
  semantics/nodes/handoffs/`Failure` boundary, and remove sidecars before committing the original
  six-path immutable implementation subject.
- [ ] **Actor:** Tester — **Action:** Write factual same-subject CAVO1 command/exit-code, delivery,
  showcase, and viewport evidence only to
  `canonical-identity-pipeline.archify-visual-overflow.correction-tester-evidence.json`; do not
  commit it.
- [ ] **Actor:** Independent Implementer — **Action:** Commit unchanged passing CAVO1 Tester
  evidence as the sole evidence-only commit.
- [ ] **Actor:** Independent Reviewer — **Action:** Consume only committed same-subject passing
  CAVO1 Tester evidence from a clean committed tree and write only
  `canonical-identity-pipeline.archify-visual-overflow.correction-implementation-review-log.json`.
- [ ] **Actor:** Independent Implementer — **Action:** Commit unchanged approved CAVO1 Reviewer
  evidence as the sole evidence-only commit; wait for Planner Phase 4.5 alignment and existing
  Human authorization before declared publish-time README/version work, push, and draft PR.

## Baseline Actionable Steps

- [ ] **Actor:** Implementer — **Action:** Preserve the original six non-publish implementation
  subject. During CAVO1, only its two Archify paths may change; the CAVO1 evidence sequence above
  replaces the inactive generic Tester/Reviewer route.

## Implementation Steps

- [ ] 1. Modify `src/deterministic_response_cache/identity/builders.py` only in private snapshot
  helper to pass active cycles to Validator while retaining immutable valid snapshots and unchanged
  public Builder behavior.
- [ ] 2. Create `src/deterministic_response_cache/identity/canonical.py` with five concrete v1
  stages and two default existing-Builder factories.
- [ ] 3. Modify `src/deterministic_response_cache/identity/__init__.py` to add only seven declared
  public exports.
- [ ] 4. Create `tests/test_canonical_identity_pipeline.py` with direct-import coverage for exact
  handoffs, determinism, invalid input, short-circuit, factories, composition, and compatibility.
- [ ] 5. CAVO1 only: after its committed Plan-Reviewer evidence and Planner route, use Archify for
  at most two focused geometry/content rounds on the JSON source and delivered HTML, run showcase
  validation/delivery/visual-check in every round, and remove untracked sidecars before immutable
  subject commit.

## Main Agent Actionable Steps — Fixed Tail

- [ ] Complete only source-authorized lifecycle actions after independently committed planning,
  Tester, and Reviewer evidence, Planner Phase 4.5 alignment, and existing Human authorization.

## Handoff / Gate Notes

- Plan-Creator's candidate commit contains only five initial planning artifacts. Planning approval
  does not establish implementation approval.
- CAVO1's committed six-path planning candidate makes the parent technical specification, plan,
  specification, and this step tracker current truth; its correction plan/step retain history.
- CAVO1 evidence schemas, exact writers, order, two-round cap, and `human-check` stop are in
  `canonical-identity-pipeline.archify-visual-overflow.correction-plan.md`. Generic parent
  Tester/Reviewer evidence paths are inactive for CAVO1.
- The implementation subject excludes `README.md` and `pyproject.toml`; they are bounded stable
  library promotion paths only at `publish-in-progress` after all prerequisite gates.
- Missing evidence, dirty worktree, subject mismatch, non-passing Tester evidence, unlisted path,
  contract drift, or bypassing Human merge is blocked and returns to Planner or Human boundary as
  workflow requires.
