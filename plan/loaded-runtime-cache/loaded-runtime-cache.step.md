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

- [X] **Actor:** Implementer — **Action:** Commit C5 as exactly the five planning artifacts, then carry it to a clean
  `origin/dev` base with no Loaded Runtime Cache artifacts. C5 must not carry old source, tests, architecture, evidence
  or receipts. The candidate SHA remains absent from planning text and is routed only by Planner from committed evidence.
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
- [ ] 4. **RED-test-only subject:** Only after Step 3 passes, add exactly the two declared tests and commit that
  immutable subject with no production-source module or RED evidence. The two tests must fail on all five C5
  regressions: opaque unhashable/custom-equality token identity-only semantics; direct `importlib.import_module`;
  direct `__import__`; `importlib`／`builtins.__import__` alias/module-alias; and cross-BC duplicate semantic types.
  Only after the commit exists, run the locked expected-nonzero command and write the factual JSON at the versioned
  path bound to that subject's full SHA.
- [ ] 5. **RED evidence-only commit:** Commit the unchanged RED JSON as a sole evidence-only commit containing neither
  tests nor production source. Green work is forbidden until this separate evidence commit exists.
- [ ] 6. **Immutable green subject:** Only after the RED evidence-only commit, add `RuntimeReuseKey`, Registry／Retention
  Protocols and lookup／retention outcomes in locked taxonomy. Correct all five C5 RED regressions only here: use
  identity-only key semantics without token equality/hash, and reject direct／alias cross-BC import and duplicate-type
  declarations. Preserve `.gitkeep`, opaque non-exposing key behavior, no mapper, no concrete class; Registry owns
  `RuntimeRegistryLookupUnavailable`, lookup outcome owns `Unavailable()`.
- [ ] 7. **Green verification and T3／V3:** Run formatting, strict Pyright, targeted/full pytest and direct-import
  regression. The alias-aware BC-independence test covers direct import, direct `importlib.import_module`, direct
  `__import__`, `importlib`／`builtins.__import__` alias/module-alias, duplicate semantic types, and `sys.modules`
  bypass. Tester then writes T3 and Reviewer writes V3 only at new SHA-bound, non-overwritable paths for the green
  subject.

## Main Agent Actionable Steps — Fixed Tail

- [ ] **Actor:** Implementer — **Action:** Complete only source-authorized lifecycle actions after committed
  Plan-Reviewer approval, same-subject passing Tester evidence, independent Reviewer approval, Planner Phase 4.5
  alignment and existing Human authorization.

## Handoff / Gate Notes

- This tracker and plan name one `loaded-runtime-cache` topic. The feature branch is lineage only, not routing
  authority.
- C5 planning candidate action is complete. Its SHA and receipt are intentionally not repeated or prefilled in planning
  artifacts; Independent Plan-Reviewer is the pending next actor and may review only that committed candidate. C5 has
  only the five planning artifacts and must be replayed onto a clean `origin/dev` base containing no Loaded Runtime
  Cache artifacts; old source, tests, architecture, evidence and receipts cannot enter C5.
- The fixed-name legacy plan-review receipt is historical frozen provenance only; it cannot be overwritten, consumed
  or used to route C5 or any successor. A `needs-rework` receipt creates no implementation subject.
- T3／V3 must be new SHA-bound, versioned receipt paths. They cannot overwrite, reuse, or infer from the legacy
  `6110cb…` Tester／`44e477…` Reviewer evidence. Tester writes factual evidence only for the new immutable green
  subject and does not commit it; Independent Reviewer consumes only committed passing same-subject T3 evidence.
- Architecture authority／dataflow completion precedes RED-test-only work. The RED subject precedes its factual
  expected-nonzero run, the resulting SHA-bound RED JSON is committed separately as sole evidence, and only that
  evidence-only commit precedes the green subject. Human alone reviews and merges a draft PR.
- Architecture-path overlap is Human review／merge coordination only; it never relaxes declared paths or evidence
  gates.
