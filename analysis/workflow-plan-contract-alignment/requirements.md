# Workflow plan-contract alignment — Requirements

## Problem

Python workflow skills require a 13-section top-level plan, while the
repository workflow requires a different canonical topic-plan contract. A
single plan cannot satisfy both instructions faithfully, so downstream gates
can stop even after a plan has passed another gate.

## Outcome

One Python topic plan can move through authoring, specialised Python review,
repo-level review, test authoring, implementation review, and step tracking
without a second plan or inferred section mapping.

## Requirements

1. Keep the eleven canonical topic-plan sections defined by
   `plan/topic-plan-contract.md` unchanged.
2. Define one optional-but-required-for-Python `Python implementation metadata`
   section with the Python planning information formerly scattered across a
   competing top-level schema.
3. Make every Python workflow skill consume that section and the canonical
   sections rather than a 13-top-level-section prerequisite.
4. Standardise Python `.step.md` files on the repository's required workflow,
   actionable, implementation, and handoff/gate sections.
5. Provide an executable fixture test that detects schema drift without
   implementing a product capability.

## Exclusions

- No Identity, Response Reuse, CacheStore, runtime, execution, or provider
  implementation.
- No package public API or dependency change.
- No README, version, release, commit, push, or pull-request action.
