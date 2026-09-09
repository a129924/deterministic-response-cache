---
topic: package-topology-skeleton-replay
phase: plan-authoring
created: 2026-09-09
---

# package-topology-skeleton-replay — Step Tracking

## Workflow Stages

- [X] plan-authoring
- [ ] plan-review
- [ ] tdd-test-authoring
- [ ] implementation
- [ ] implementation-review
- [ ] code-review

## Actionable Steps

- [ ] **Actor:** Implementer — **Action:** After a committed approved candidate receipt, complete only the six source implementation steps in order.

## Implementation Steps

- [ ] 1. Update `docs/business-capability-architecture.md` with the fixed mapping and topology-only boundary.
- [ ] 2. Update `docs/evolution-roadmap.md` with the fixed Identity-first five-BC evolution sequence.
- [ ] 3. Update `docs/architecture/business-capability/architecture-brief.md` to synchronize topology and BC boundaries.
- [ ] 4. Update `docs/architecture/business-capability/scene.js` to synchronize the visual implementation-order labels.
- [ ] 5. Update `docs/architecture/business-capability/index.html` to mirror the synchronized visual labels.
- [ ] 6. Create the five declared BC `.gitkeep` files under `src/deterministic_response_cache/` and no other package paths.

## Main Agent Actionable Steps — Fixed Tail

- [ ] Complete only source-authorised lifecycle actions.

## Handoff / Gate Notes

- Only the six pending entries in `## Implementation Steps` are the implementation-completion gate.
- An independent Plan-Reviewer must write one receipt with exactly `schema_version`, `candidate_commit`, `verdict`, `blocking_issues`, and `copilot_feedback_triage`; `schema_version` is `1`, `candidate_commit` is the committed candidate's full SHA, and the receipt must then be committed unchanged as the sole receipt path with that candidate as its direct parent before Planner selects an Implementer.
- Tester evidence must attest the same immutable implementation subject and be committed unchanged as its sole evidence path before Independent Reviewer work.
- Independent Reviewer evidence must bind that committed passing Tester evidence and be committed unchanged as its sole evidence path before Planner Phase 4.5 alignment.
