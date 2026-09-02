# Observer / Dispatcher Governance Specification

> **B2 correction override:** B0/S1/T1/V1、B1 及其 invalid review record are frozen provenance.
> Before implementation, only the seven B2 planning artifacts receive a temporary-index verified
> Git tree/blob review and non-subject B2 baseline commit with post-commit validation. The sole
> subsequent subject is test-only S3; its only allowed non-merge descendants are T3 then V3,
> verified as `S3..V3`, never `HEAD`.

## Acceptance Criteria

1. Declared governance, custom-agent, workflow-skill and test surfaces use one
   model: Planner alone resolves candidate, phase, gate, severity, correction
   route and next role; Observer is readonly and dispatches one Planner-selected role.
2. All declared surfaces classify the issue as `high` / `PLANNER_REPLAN`, keep parent plan/spec/step
   current after backfill, retain `correction-b2-plan.md` / `correction-b2-step.md` as bounded
   B2 correction delta, and recognize `correction-b2-review-log.md` as the sole current B2
   pre-subject gate until that gate is completed.
3. The five exact B2 correction artifacts are conditionally required: correction-b2 plan,
   correction-b2 step, correction-b2 review log, correction-b2 Tester evidence, and correction-b2
   implementation-review log; their owners, order, and schemas are explicit.
4. B0/S1/T1/V1, all existing normal evidence, and all `recovery-*` evidence are frozen provenance:
   no current routing / subject / Tester / Reviewer meaning, migration, reader, compatibility, or rewrite.
5. Before any S3 change, under the one-time B2 exception, Plan-Reviewer uses a temporary index
   seeded from `HEAD` to build and verify a Git tree over exactly seven uncommitted B2 planning
   artifacts—two shared contracts, parent plan/spec/step, and B2 correction plan/step—then
   Independent Implementer commits that unchanged approved record and exact reviewed set as
   non-subject B2 and verifies the record/tree/blob relationship post-commit.
6. Only after approved, post-commit-validated non-subject `B2`, test-only non-merge `S3` becomes
   the replacement immutable subject; exactly `T3` Tester then `V3` Reviewer evidence-only commits
   may follow. Verification is `S3..V3`, never a `HEAD` range.
7. Tester starts `pending`, tests only the replacement subject and records exact
   commands/results and `passing|failing`; Reviewer proceeds only from the same
   subject and a passing new Tester record.
8. `tests/test_observer_dispatcher_governance_contract.py` detects expanded-schema
   drift without replacing direct-import regressions or adding dynamic imports.

## Behavioral Scenarios

### Scenario 1: High correction begins

- **Given**: parent artifacts are synchronized and old normal/recovery evidence is frozen.
- **When**: Planner routes the correction.
- **Then**: topic remains `needs-rework` / `PLANNER_REPLAN`; Plan-Creator creates only
  parent/correction planning artifacts and makes none of the old evidence current.

### Scenario 2: Replacement immutable subject

- **Given**: Correction Plan-Reviewer has temporary-index tree/blob reviewed exactly the seven
  uncommitted B2 planning artifacts, written the approved schema-complete correction-b2 review
  record, and an Independent Implementer has committed that unchanged record plus exact reviewed
  set as B2 and validated the retained tree/blob relation.
- **When**: Implementer commits only `tests/test_observer_dispatcher_governance_contract.py`.
- **Then**: that non-merge `S3` commit alone is the replacement immutable subject; B2 is never a subject.

### Scenario 3: Two ordered descendants

- **Given**: the replacement subject has no descendant.
- **When**: Tester records evidence and Reviewer independently records a verdict against
  the same subject.
- **Then**: each becomes its own named non-merge evidence-only descendant `T3` then `V3`;
  name-status from `S3..V3` contains exactly the two named correction-b2 evidence paths and then stops.

### Scenario 4: Drift fails closed

- **Given**: any surface omits a path, gives Observer Planner authority, makes legacy
  evidence current, permits an extra descendant, or attests a descendant as subject.
- **When**: the new contract test or independent review runs.
- **Then**: correction remains `needs-rework`; no lifecycle action is inferred.

## Error / Edge Cases

- Missing/non-approved correction review, or correction review evidence written after any
  implementation change, blocks implementation and subject creation.
- Missing/failing Tester evidence, mismatched SHA, merge, extra path or third descendant
  invalidates the chain and cannot be repaired by reusing legacy/recovery evidence.
- An undeclared path, provenance migration, standalone correction skill or lifecycle action
  is returned to Planner/Human, not silently added to this topic.
