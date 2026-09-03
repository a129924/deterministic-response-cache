# Observer / Dispatcher Governance — High Correction Plan

## Trigger / Evidence

- Planner confirmed `high` severity: existing evidence topology and subject no longer establish
  confidence in the expanded Observer / Dispatcher contract.

## Scope / Direction

- Synchronize only parent-declared exact paths. Extend their shared schema with Planner-only
  authority, Observer readonly dispatch, separated write ownership / decision authority,
  conditional correction artifacts, frozen provenance and a replacement immutable-subject chain.
- Independent correction-plan review evidence is required and must be committed unchanged before
  any declared implementation begins. Its `approved` verdict is a precondition only; the later
  completed implementation commit, not the review-evidence commit, is the replacement subject.
- Old epoch is terminal at `R0=cb3f66c60e95e5580cb2b30632d0d5ed9f0d0ee9`; its only predicate is
  `ecc5b6f61bacc5493ca3a9f1012d1bfdd43a810c..cb3f66c60e95e5580cb2b30632d0d5ed9f0d0ee9`.
- The narrow `B0` exception permits Plan-Reviewer tree/blob review of exactly seven uncommitted
  planning artifacts, then its correction review log, then the `B0` commit containing that log and
  reviewed set. `B0` is not a subject. The only later chain is `S1` implementation subject, `T1`
  Tester evidence, then `V1` Reviewer evidence; verify `S1..V1`, never `HEAD`.
- No product/BC/identity/runtime/lifecycle work, `.github/agents/**` change, provenance
  migration, reader or compatibility layer is permitted.

## What Stays / Changes

- **Current after backfill:** parent plan/spec/step and, until consumed,
  `correction-review-log.md` as the sole pre-implementation correction gate. **Historical:**
  correction plan/step delta plus all normal/recovery evidence. **Changed:** fresh correction
  routing and a subject replacing all prior subjects only after independent correction review
  approval and subsequent implementation.

## Acceptance Delta

- Contract test detects cross-surface schema drift. New Tester begins pending and attests only
  replacement subject. Subject descendants are exactly Tester then implementation-review evidence.
  Correction review, Tester and final Reviewer records use the complete shared JSON schemas.

## Parent Sync / Retention / Closure

- Parent sync and approved correction-plan review evidence precede implementation. Correction
  remains retained historical truth; closure requires passing `T1` evidence, independent `V1`
  review, exact `S1..V1` two-path range and Human stop. Deletion is forbidden.
