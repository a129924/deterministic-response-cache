---
topic: loaded-runtime-cache
phase: planning-candidate-commit
created: 2026-09-17
---

# loaded-runtime-cache — Step Tracking

## Workflow Stages

- [X] plan-authoring
- [ ] planning-candidate-commit
- [ ] plan-review
- [ ] tdd-test-authoring
- [ ] implementation
- [ ] implementation-review
- [ ] code-review

## Actionable Steps

- [ ] **Actor:** Implementer — **Action:** Commit exactly these five planning artifacts as a non-merge planning
  candidate: `analysis/loaded-runtime-cache/requirements.md`, `analysis/loaded-runtime-cache/technical-spec.md`,
  `plan/loaded-runtime-cache/loaded-runtime-cache.plan.md`, `.spec.md`, `.step.md`. Do not add source, test,
  documentation, visualization, review, evidence or governance paths. The candidate SHA is unknown until commit and
  must not be prefilled.
- [ ] **Actor:** Independent Plan-Reviewer — **Action:** Review only the committed candidate and, only after it
  exists, write `plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<planning-candidate-40-hex-sha>.json`
  using the locked normal-plan receipt schema. Each candidate gets one immutable non-overwritable SHA-bound receipt.
- [ ] **Actor:** Implementer — **Action:** Commit unchanged Plan-Reviewer receipt as a sole evidence-only commit.
  Only its committed `approved` verdict can be routed by Planner for implementation.

## Implementation Steps

- [ ] 1. Add `RuntimeReuseKey`, Runtime Registry／Retention Protocols and lookup／retention outcome contracts only in
  the locked three-level taxonomy; preserve `.gitkeep` and avoid concrete classes. The Registry port owns and raises
  `RuntimeRegistryLookupUnavailable`; lookup outcome module owns `Unavailable()`.
- [ ] 2. Add direct-module contract tests with typed fakes for key-instance handoff, Registry value／missing channels,
  retention runtime preservation, failure distinction and BC-independence; no mapper test or internal-key assertion.
- [ ] 3. Synchronize only the five declared architecture authority files to describe a protocol-only BC, external
  unimplemented ACL mapping and future lifecycle／execution／provider work.
- [ ] 4. Author and deliver the locked Archify dataflow with contract-only `backend` visual mapping, validation and
  visual-check evidence; do not imply a mapper or runtime lifecycle implementation.
- [ ] 5. Run formatting, strict type checking, targeted／full tests, direct-import regression and Archify
  validate／deliver／visual-check; Tester records actual exit codes after immutable subject creation.

## Main Agent Actionable Steps — Fixed Tail

- [ ] Complete only source-authorized lifecycle actions after committed Plan-Reviewer approval, same-subject passing
  Tester evidence, independent Reviewer approval, Planner Phase 4.5 alignment and existing Human authorization.

## Handoff / Gate Notes

- This tracker and plan name one `loaded-runtime-cache` topic. The feature branch is lineage only, not routing
  authority.
- The fixed-name legacy plan-review receipt is historical frozen provenance only; it cannot be overwritten, consumed
  or used to route candidate C or any successor. A `needs-rework` receipt creates no implementation subject.
- Tester writes factual evidence only for immutable implementation subject and does not commit it. Independent
  Reviewer consumes only committed passing same-subject Tester evidence. Human alone reviews and merges a draft PR.
- Architecture-path overlap is Human review／merge coordination only; it never relaxes declared paths or evidence
  gates.
