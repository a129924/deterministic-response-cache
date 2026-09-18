---
topic: loaded-runtime-cache
phase: independent-plan-review
created: 2026-09-17
---

# loaded-runtime-cache — Step Tracking

## Workflow Stages

- [X] plan-authoring
- [X] planning-candidate-commit
- [ ] plan-review
- [ ] tdd-test-authoring
- [ ] implementation
- [ ] implementation-review
- [ ] code-review

## Actionable Steps

- [X] **Actor:** Implementer — **Action:** Commit exactly the five planning artifacts as a non-merge planning
  candidate. The candidate SHA remains absent from planning text and is routed only by Planner from committed evidence.
- [ ] **Actor:** Independent Plan-Reviewer — **Action:** Review only the committed candidate and, only after it
  exists, write `plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<planning-candidate-40-hex-sha>.json`
  using the locked normal-plan receipt schema. Each candidate gets one immutable non-overwritable SHA-bound receipt.
- [ ] **Actor:** Implementer — **Action:** Commit unchanged Plan-Reviewer receipt as a sole evidence-only commit.
  Only its committed `approved` verdict can be routed by Planner for implementation.

## Implementation Steps

- [ ] 1. **Architecture-contract-only:** Synchronize only the five declared architecture authority files to describe
  protocol-only capability, external unimplemented ACL mapping, and future lifecycle／execution／provider work. Commit
  this before any new test or production-source path; F ownership remains Human-only.
- [ ] 2. **Dataflow authoring:** Author `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.json`
  with contract-only `backend` mapping. Show `RuntimeReuseKey` as retain input; dashed relationships are explicit async
  only and never represent synchronous retain failure.
- [ ] 3. **Architecture visual gate:** After every JSON revision run showcase validate; only final 9/9, zero-error,
  zero-warning output may be delivered and visual-checked at all four declared desktop viewports. A nonzero or skipped
  result blocks RED and source work.
- [ ] 4. **RED-test-only:** Only after Step 3 passes, add and execute the two declared tests with expected failures;
  this subject has no production-source module. Record actual nonzero command facts in the versioned RED evidence path.
- [ ] 5. **Immutable green subject:** Only after committed RED evidence, add `RuntimeReuseKey`, Registry／Retention
  Protocols and lookup／retention outcomes in locked taxonomy. Preserve `.gitkeep`, opaque non-exposing key behavior,
  no mapper, no concrete class; Registry owns `RuntimeRegistryLookupUnavailable`, lookup outcome owns `Unavailable()`.
- [ ] 6. **Green verification and T2／V2:** Run formatting, strict Pyright, targeted/full pytest and direct-import
  regression. The BC-independence test covers direct import, `importlib`, `__import__`, and `sys.modules` bypass.
  Tester then writes T2 and Reviewer writes V2 only at new SHA-bound, non-overwritable paths for the green subject.

## Main Agent Actionable Steps — Fixed Tail

- [ ] **Actor:** Implementer — **Action:** Complete only source-authorized lifecycle actions after committed
  Plan-Reviewer approval, same-subject passing Tester evidence, independent Reviewer approval, Planner Phase 4.5
  alignment and existing Human authorization.

## Handoff / Gate Notes

- This tracker and plan name one `loaded-runtime-cache` topic. The feature branch is lineage only, not routing
  authority.
- A committed planning candidate exists. Its SHA is intentionally not repeated or prefilled in planning artifacts;
  Independent Plan-Reviewer is the pending next actor and may review only that committed candidate.
- The fixed-name legacy plan-review receipt is historical frozen provenance only; it cannot be overwritten, consumed
  or used to route candidate C or any successor. A `needs-rework` receipt creates no implementation subject.
- T2／V2 must be new SHA-bound, versioned receipt paths. They cannot overwrite, reuse, or infer from the legacy
  `6110cb…` Tester／`44e477…` Reviewer evidence. Tester writes factual evidence only for the new immutable green
  subject and does not commit it; Independent Reviewer consumes only committed passing same-subject T2 evidence.
- Architecture authority／dataflow completion precedes RED-test-only work; RED evidence precedes the green subject.
  Human alone reviews and merges a draft PR.
- Architecture-path overlap is Human review／merge coordination only; it never relaxes declared paths or evidence
  gates.
