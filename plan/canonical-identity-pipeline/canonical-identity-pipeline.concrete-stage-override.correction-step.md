---
topic: canonical-identity-pipeline
correction_id: canonical-identity-pipeline/concrete-stage-override
phase: correction-plan-review
created: 2026-09-15
---

# CSO1 — Concrete-stage `@override` correction tracking

## Current correction boundary

CSO1 is a fresh, two-path correction to the existing draft PR #6. It requires named inheritance
from the existing five Protocols and `@override` only on the corresponding public stage method.
It does not alter canonical behavior, public handoff types, Builder injection, exports, documents,
version, lockfile, diagram, or CAVO1 history.

## Correction workflow

- [X] C0 — Plan-Creator committed the exact six-path CSO1 planning candidate.
- [ ] C1 — Independent Plan-Reviewer reviews C0 from a clean committed checkout and writes only
  `canonical-identity-pipeline.concrete-stage-override.correction-plan-review-log.json`.
- [ ] C2 — Independent Implementer commits unchanged approved C1 evidence as the sole
  evidence-only commit; Planner then decides whether C3 may start.
- [ ] C3 — Implementer commits one new immutable subject changing only `canonical.py` and the
  dedicated pipeline test, with exact named bases, public `@override` markers, and unchanged direct
  import/pipeline behavior.
- [ ] C4 — Tester writes only factual same-subject results to
  `canonical-identity-pipeline.concrete-stage-override.correction-tester-evidence.json`; it does
  not commit the evidence.
- [ ] C5 — Independent Implementer commits unchanged passing C4 evidence as the sole
  evidence-only commit.
- [ ] C6 — Independent Reviewer consumes same-subject passing committed C4 evidence from a clean
  C5 tree and writes only
  `canonical-identity-pipeline.concrete-stage-override.correction-implementation-review-log.json`.
- [ ] C7 — Independent Implementer commits unchanged approved C6 evidence as the sole
  evidence-only commit.
- [ ] C8 — Planner performs Phase 4.5 alignment. With existing human authorization, an Implementer
  may push only to update existing draft PR #6; merge remains Human-only.

## Stop conditions

- CAVO1 evidence cannot satisfy C1, C4, or C6. A rework needs a fresh C3 subject and repeats the
  complete C3–C7 sequence.
- An unlisted path, changed Protocol/value object/Builder injection, marker on any private helper,
  absent marker on a listed public method, or dynamic import is scope/contract drift and returns to
  Planner.
- The exact C1/C4/C6 paths, writers, ordering, and JSON schemas are authoritative in
  `canonical-identity-pipeline.concrete-stage-override.correction-plan.md`.
