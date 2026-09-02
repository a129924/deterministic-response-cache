# Observer / Dispatcher Governance Specification

## Acceptance Criteria

1. Declared governance, custom-agent, workflow-skill and test surfaces use one
   model: Planner alone resolves candidate, phase, gate, severity, correction
   route and next role; Observer is readonly and dispatches one Planner-selected role.
2. All declared surfaces classify the issue as `high` / `PLANNER_REPLAN`, keep
   parent plan/spec/step current after backfill, retain correction plan/step as historical
   correction delta, and recognize `correction-review-log.md` as the sole current
   pre-implementation correction gate until that gate is completed.
3. The five exact correction artifacts are conditionally required: correction
   plan, correction step, correction review log, correction Tester evidence and
   correction implementation-review log; their owners, order and schemas are explicit.
4. All existing normal and `recovery-*` evidence is frozen, superseded provenance:
   no current routing / Tester / Reviewer meaning, migration, reader, compatibility or rewrite.
5. Old epoch is terminal at `R0=cb3f66c60e95e5580cb2b30632d0d5ed9f0d0ee9` and is identified only by
   `ecc5b6f61bacc5493ca3a9f1012d1bfdd43a810c..cb3f66c60e95e5580cb2b30632d0d5ed9f0d0ee9`.
   Under the narrow `B0` exception, Plan-Reviewer tree/blob reviews seven uncommitted planning
   artifacts, writes the correction review log, and Independent Implementer commits that reviewed
   set plus unchanged log as non-subject `B0`.
6. Only after approved `B0`, the declared implementation's completed non-merge `S1` commit becomes
   the replacement immutable subject; exactly `T1` Tester then `V1` Reviewer evidence-only commits
   may follow. Verification is `S1..V1`, never a `HEAD` range.
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

- **Given**: Correction Reviewer has tree/blob reviewed the seven uncommitted planning artifacts,
  written the approved schema-complete correction-plan review record, and an Independent Implementer
  has committed that record plus reviewed set as `B0`.
- **When**: Implementer completes and commits only the declared expanded implementation paths.
- **Then**: that `S1` commit alone is the replacement immutable subject; `B0` is never a subject.

### Scenario 3: Two ordered descendants

- **Given**: the replacement subject has no descendant.
- **When**: Tester records evidence and Reviewer independently records a verdict against
  the same subject.
- **Then**: each becomes its own named non-merge evidence-only descendant `T1` then `V1`;
  name-status from `S1..V1` contains exactly the two new correction evidence paths and then stops.

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
