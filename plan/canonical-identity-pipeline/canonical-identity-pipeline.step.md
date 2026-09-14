---
topic: canonical-identity-pipeline
phase: plan-authoring
created: 2026-09-14
---

# canonical-identity-pipeline — Step Tracking

## Workflow Stages

- [X] plan-authoring
- [ ] plan-review
- [ ] tdd-test-authoring
- [ ] implementation
- [ ] implementation-review
- [ ] code-review

## Actionable Steps

- [ ] **Actor:** Independent Plan-Reviewer — **Action:** Review the committed planning candidate
  and write only `canonical-identity-pipeline.plan-review-receipt.json` using the declared
  machine-consumable JSON shape.
- [ ] **Actor:** Implementer — **Action:** After committed approved receipt and Planner route,
  complete every source `## Implementation Steps` item in order as one immutable implementation
  subject limited to six declared non-publish paths.
- [ ] **Actor:** Tester — **Action:** Write factual commands and exit codes only to
  `canonical-identity-pipeline.tester-evidence.json`; do not commit it.
- [ ] **Actor:** Independent Implementer — **Action:** Commit unchanged passing Tester evidence as
  the sole evidence-only commit.
- [ ] **Actor:** Independent Reviewer — **Action:** Consume only committed same-subject passing
  Tester evidence and write only `canonical-identity-pipeline.implementation-review-log.json`.
- [ ] **Actor:** Independent Implementer — **Action:** Commit unchanged approved Reviewer evidence
  as sole evidence-only commit; wait for Planner Phase 4.5 alignment and existing Human
  authorization before declared publish-time README/version work, push, and draft PR.

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
- [ ] 5. Use Archify to create and showcase-validate
  `docs/architecture/canonical-identity-pipeline.dataflow.json`, deliver
  `docs/architecture/canonical-identity-pipeline.html`, visual-check it, and remove untracked
  sidecars before immutable subject commit.

## Main Agent Actionable Steps — Fixed Tail

- [ ] Complete only source-authorized lifecycle actions after independently committed planning,
  Tester, and Reviewer evidence, Planner Phase 4.5 alignment, and existing Human authorization.

## Handoff / Gate Notes

- Plan-Creator's candidate commit contains only five initial planning artifacts. Planning approval
  does not establish implementation approval.
- The implementation subject excludes `README.md` and `pyproject.toml`; they are bounded stable
  library promotion paths only at `publish-in-progress` after all prerequisite gates.
- Missing evidence, dirty worktree, subject mismatch, non-passing Tester evidence, unlisted path,
  contract drift, or bypassing Human merge is blocked and returns to Planner or Human boundary as
  workflow requires.
