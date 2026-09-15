---
topic: canonical-identity-pipeline
correction_id: canonical-identity-pipeline/archify-visual-overflow
phase: correction-plan-review
created: 2026-09-15
---

# CAVO1 — Archify visual-overflow correction tracking

## Retention and current truth

This file retains the CAVO1 historical sequence. The parent technical specification, plan,
specification, and step tracker are the current topic truth after C0; this file does not replace
them. It authorizes no path other than the two Archify paths named by the parent artifacts.

## Correction workflow

- [X] C0 — Plan-Creator committed the exact six-path correction planning candidate.
- [ ] C1 — Independent Plan-Reviewer reviews C0 from a clean committed checkout and writes only
  `canonical-identity-pipeline.archify-visual-overflow.correction-plan-review-log.json`.
- [ ] C2 — Independent Implementer commits unchanged approved C1 evidence as the sole
  evidence-only commit; Planner then decides whether C3 may start.
- [ ] C3 — Implementer performs at most two focused Archify geometry/content rounds. It changes
  only `docs/architecture/canonical-identity-pipeline.dataflow.json`, re-delivers only
  `docs/architecture/canonical-identity-pipeline.html`, and preserves pipeline semantics, nodes,
  handoffs, and `Failure` boundary. It removes all visual-check sidecars before committing the
  original six-path immutable implementation subject.
- [ ] C4 — Tester writes only factual same-subject results to
  `canonical-identity-pipeline.archify-visual-overflow.correction-tester-evidence.json`; it does
  not commit the evidence.
- [ ] C5 — Independent Implementer commits unchanged passing C4 evidence as the sole
  evidence-only commit.
- [ ] C6 — Independent Reviewer uses the clean committed C5 tree and same-subject passing C4
  evidence to write only
  `canonical-identity-pipeline.archify-visual-overflow.correction-implementation-review-log.json`.
- [ ] C7 — Independent Implementer commits unchanged approved C6 evidence as the sole
  evidence-only commit.
- [ ] C8 — Planner performs Phase 4.5 alignment. Only existing Human authorization may then route
  bounded publish/push/draft-PR work; merge remains Human-only.

## Round gate

Each round must run showcase `validate`, `deliver`, and desktop `visual-check`. Passing requires
9/9 showcase checks, zero errors/warnings, delivery exit 0, visual-check exit 0, and containment
at 1440×900, 1600×1000, 1920×1080, and 2048×1320. Round 2 is the sole possible retry. If it does
not leave zero failing viewports, if either required command remains non-zero, or if two rounds do
not strictly reduce the failing viewport count, stop as `human-check`; do not create a third round.

## Evidence authority

The exact C1, C4, and C6 paths, owners, order, and extended JSON schemas are authoritative in
`canonical-identity-pipeline.archify-visual-overflow.correction-plan.md`. Generic parent
Tester/Reviewer evidence paths are not written for CAVO1. A `needs-rework` verdict returns to
Planner; no reviewer can approve a PR, merge, release, tag, or post-merge action.
