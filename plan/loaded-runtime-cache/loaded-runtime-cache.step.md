---
topic: loaded-runtime-cache
phase: independent-plan-review
created: 2026-09-17
---

# loaded-runtime-cache — Step Tracking

## Workflow Stages

- [X] plan-authoring
- [X] planning-candidate-commit
- [X] plan-review
- [X] tdd-test-authoring
- [X] implementation
- [X] implementation-review
- [ ] code-review

## Actionable Steps

- [X] **Actor:** Implementer — **Action:** Commit C5 as exactly the five planning artifacts, then carry it to a clean
  `origin/dev` base with no Loaded Runtime Cache artifacts. C5 must not carry old source, tests, architecture, evidence
  or receipts. The candidate SHA remains absent from planning text and is routed only by Planner from committed evidence.
- [X] **Actor:** Independent Plan-Reviewer — **Action:** Review only the committed candidate and, only after it
  exists, write `plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<planning-candidate-40-hex-sha>.json`
  using the locked normal-plan receipt schema. Each candidate gets one immutable non-overwritable SHA-bound receipt.
- [X] **Actor:** Implementer — **Action:** Commit unchanged Plan-Reviewer receipt as a sole evidence-only commit.
  Only its committed `approved` verdict can be routed by Planner for implementation.

## Implementation Steps

- [X] 1. **Architecture-contract-only:** Synchronize only the five declared architecture authority files to describe
  protocol-only capability, external unimplemented ACL mapping, and future lifecycle／execution／provider work. Commit
  this before any new test or production-source path; F ownership remains Human-only.
- [X] 2. **Dataflow authoring:** Author `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.json`
  with contract-only `backend` mapping. Show `RuntimeReuseKey` as retain input; dashed relationships are explicit async
  only and never represent synchronous retain failure.
- [X] 3. **Architecture visual gate:** After every JSON revision run showcase validate; only final 9/9, zero-error,
  zero-warning output may be delivered and visual-checked at all four declared desktop viewports. A nonzero or skipped
  result blocks RED and source work.
- [X] 4. **RED-test-only subject:** Only after Step 3 passes, add exactly the two declared tests and commit that
  immutable subject with no production-source module or RED evidence. The two tests must fail on all five C5
  regressions: opaque unhashable/custom-equality token identity-only semantics; direct `importlib.import_module`;
  direct `__import__`; `importlib`／`builtins.__import__` alias/module-alias; and cross-BC duplicate semantic types.
  Only after the commit exists, run the locked expected-nonzero command and write the factual JSON at the versioned
  path bound to that subject's full SHA.
- [X] 5. **RED evidence-only commit:** Commit the unchanged RED JSON as a sole evidence-only commit containing neither
  tests nor production source. Green work is forbidden until this separate evidence commit exists.
- [X] 6. **Immutable green subject:** Only after the RED evidence-only commit, add `RuntimeReuseKey`, Registry／Retention
  Protocols and lookup／retention outcomes in locked taxonomy. Correct all five C5 RED regressions only here: use
  identity-only key semantics without token equality/hash, and reject direct／alias cross-BC import and duplicate-type
  declarations. Preserve `.gitkeep`, opaque non-exposing key behavior, no mapper, no concrete class; Registry owns
  `RuntimeRegistryLookupUnavailable`, lookup outcome owns `Unavailable()`.
- [X] 7. **Green verification and T3／V3:** Run formatting, strict Pyright, targeted/full pytest and direct-import
  regression. The alias-aware BC-independence test covers direct import, direct `importlib.import_module`, direct
  `__import__`, `importlib`／`builtins.__import__` alias/module-alias, duplicate semantic types, and `sys.modules`
  bypass. Tester then writes T3 and Reviewer writes V3 only at new SHA-bound, non-overwritable paths for the green
  subject.

## Main Agent Actionable Steps — Fixed Tail

- [X] **Actor:** Implementer — **Action:** Complete only source-authorized lifecycle actions after committed
  Plan-Reviewer approval, same-subject passing Tester evidence, independent Reviewer approval, Planner Phase 4.5
  alignment and existing Human authorization.

## Handoff / Gate Notes

- This tracker and plan name one `loaded-runtime-cache` topic. The feature branch is lineage only, not routing
  authority.
- C5 `505c30609f5d65030a2eda740d8135b768cc06ca` is committed as exactly the five planning artifacts. Its independently
  approved R5 receipt is committed in the sole evidence-only commit `c870dd06ae47c2a8d3832604f349126f026ee1e6`.
  C5 was replayed onto clean `origin/dev` lineage without prior Loaded Runtime Cache artifacts.
- The fixed-name legacy plan-review receipt is historical frozen provenance only; it cannot be overwritten, consumed
  or used to route C5 or any successor. A `needs-rework` receipt creates no implementation subject.
- Architecture-only `442cc94`, RED subject `e2e125d`, its separate evidence-only commit `0b86022`, immutable green
  subject `1b5e4cf`, T3 `06da9dc`, and V3 `1c2330c` are all completed in order. T3／V3 use new SHA-bound, versioned
  receipt paths and do not reuse the legacy `6110cb…` Tester／`44e477…` evidence. T3 records passing factual validation
  for green subject `1b5e4cfbd740c1e7fa10eef43221d7198f530547`; V3 independently approves that same subject.
- Architecture authority／dataflow completion precedes RED-test-only work. The RED subject precedes its factual
  expected-nonzero run, the resulting SHA-bound RED JSON is committed separately as sole evidence, and only that
  evidence-only commit precedes the green subject. Human alone reviews and merges a draft PR.
- Architecture-path overlap is Human review／merge coordination only; it never relaxes declared paths or evidence
  gates.
- Next routing action is Planner Phase 4.5 alignment. Only after it passes may an independent Reviewer classify current
  PR threads; this tracker does not mark code review, publish, comments, F ownership, or Human actions complete.
