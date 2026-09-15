---
topic: canonical-identity-pipeline
phase: concrete-stage-override-correction-plan-review-pending
created: 2026-09-14
updated: 2026-09-15
---

# canonical-identity-pipeline — Step Tracking

## Current state

The original six-path pipeline subject, completed CAVO1 sequence, and existing draft PR #6 are
committed historical facts. They remain reviewable provenance but cannot be reused as routing,
Tester, or Reviewer evidence for `canonical-identity-pipeline/concrete-stage-override` (CSO1).
CSO1 is the sole active correction route and exists only to add named Protocol inheritance and
public-method `@override` declarations without altering runtime pipeline behavior.

| Step | Status | Committed fact |
| --- | --- | --- |
| C0 | complete | Plan-Creator authored this exact six-path CSO1 planning candidate. Its commit/tree/blob facts may be recorded only by C1. |
| C1 | pending | Independent Plan-Reviewer, from a clean committed C0 checkout, writes only `canonical-identity-pipeline.concrete-stage-override.correction-plan-review-log.json`. |
| C2 | pending | Independent Implementer commits unchanged approved C1 evidence as its sole evidence-only commit; only then may Planner route C3. |
| C3 | pending | Implementer creates one new immutable subject that changes exactly `src/deterministic_response_cache/identity/canonical.py` and `tests/test_canonical_identity_pipeline.py`. |
| C4 | pending | Tester writes only factual same-subject results to `canonical-identity-pipeline.concrete-stage-override.correction-tester-evidence.json`; it does not commit the evidence. |
| C5 | pending | Independent Implementer commits unchanged passing C4 evidence as its sole evidence-only commit. |
| C6 | pending | Independent Reviewer consumes committed passing C4 evidence from a clean C5 tree and writes only `canonical-identity-pipeline.concrete-stage-override.correction-implementation-review-log.json`. |
| C7 | pending | Independent Implementer commits unchanged approved C6 evidence as its sole evidence-only commit. |
| C8 | pending | Planner performs Phase 4.5 alignment; only then may a bounded Implementer push the correction commits to update existing draft PR #6. |

## CSO1 actionable steps

- [X] **C0:** Plan-Creator wrote the two active correction artifacts and synchronized the parent
  technical specification, plan, specification, and tracker as one six-path candidate commit.
- [ ] **C1/C2:** Independent Plan-Reviewer writes, then an independent Implementer commits, the
  approved CSO1 correction-plan review log under its exact schema.
- [ ] **C3:** Implementer changes only `canonical.py` and the dedicated direct-import regression
  module. Each concrete stage has exactly its matching named Protocol base; only `validate`,
  `sort`, `encode`, `serialize`, or `hash` is marked `@override`; private helpers remain unmarked.
- [ ] **C4/C5:** Tester writes, then an independent Implementer commits, factual passing CSO1
  Tester evidence that binds C3's full SHA and exact two-path diff.
- [ ] **C6/C7:** Independent Reviewer consumes committed same-subject passing C4 evidence, writes
  an approved CSO1 review log, then an independent Implementer commits it unchanged.
- [ ] **C8:** Planner verifies all CSO1 evidence and existing human authorization before routing a
  bounded update to draft PR #6. This does not authorize a new PR, PR approval, merge, release,
  tag, post-merge, or final summary.

## Historical provenance and stop conditions

- CAVO1's committed Plan-Reviewer, Tester, and Reviewer evidence remains frozen provenance only;
  it cannot satisfy C1, C4, or C6. CSO1 must complete a fresh same-subject sequence.
- `contracts.py`, builders, public exports, both Archify artifacts, README, `pyproject.toml`,
  `uv.lock`, existing regression modules, and all historic evidence are read-only for C3.
- A missing, mismatched, cross-subject, non-passing, or uncommitted C1/C4/C6 record; an unlisted
  path; a dirty evidence commit; or a request to change public contract behavior is `blocked` and
  returns to Planner. Candidate/evidence/subject conflict is `human-check`.
- Human alone owns PR review, merge, release, tag, post-merge, and final summary. CSO1 success can
  update existing draft PR #6 only after Planner Phase 4.5; it never creates or merges a PR.
