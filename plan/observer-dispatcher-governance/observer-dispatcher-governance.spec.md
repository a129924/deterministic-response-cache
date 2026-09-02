# Observer / Dispatcher Governance Specification

> **B4R correction override:** `B4=979798e` is failed, unapproved, non-subject frozen provenance.
> B0–B4/S1–S4/T1–T4/V1–V4 and normal/recovery are frozen nonrouting provenance; two
> `step-creator` PR threads remain deferred. B4R and its separately committed approved clean-review
> evidence are non-subject commits. Only then may S5 become the immutable non-merge subject over the
> exact 15-path B4R allowlist, including `.codex/agents/reviewer.toml`; direct imports remain mandatory.

## B4R Current Acceptance Criteria

1. Candidate selection reads only parent plan, parent step and approved B4R review evidence; Observer bootstrap-dispatches Planner only, then Planner may dispatch Tester/Explorer.
2. B4R is exactly the six permitted planning paths; Plan-Reviewer clean-checkout reviews actual committed B4R blobs, and its approved review record is separately committed before S5.
3. S5 is the only subject and changes only the exact 15-path B4R allowlist; B4, B4R, and every prior commit/evidence record are not subjects.
4. T5 then V5 are sole non-merge descendants; actual SHA graph checks and named exact `S5..V5` are mandatory, while `HEAD` and textual topology inference fail closed.
5. Tester uses factual `passing|failing` only, without routing, lifecycle, status, or `next_gate`; Reviewer requires the exact same S5 plus passing exact B4R T5 evidence.
6. Mutation tests fail closed for removing frozen markers, treating B4/B4R/prior work as subject, widening S5, omitting the reviewer custom-agent path, dynamic-import substitution, wrapper orchestration, T5 routing, mismatched/failing T5, merge/third descendant or range drift.

> **B3 correction override:** B0/B1/B2/S1/S3/T1/T3/V1/V3 plus normal/recovery evidence are frozen
> and nonrouting; V3 is a frozen needs-rework outcome without a repo-visible review log. B3 is a
> temporary-index verified-tree non-subject baseline over exactly seven B3 planning paths. S4 alone
> changes `tests/test_observer_dispatcher_governance_contract.py` and becomes the current subject;
> direct imports remain mandatory. Only T4 then V4 may descend. The V4 record is written before V4
> exists and names pre-existing T4 through `review_target_commit_sha`, never a V4 SHA. Post-commit
> validation identifies V4 independently and checks exact named `S4..V4` evidence-only range.

## B3 Current Acceptance Criteria

1. B0/B1/B2/S1/S3/T1/T3/V1/V3 and normal/recovery evidence are frozen nonrouting provenance;
   V3's historical needs-rework outcome has no review log.
2. B3 is verified through a temporary index over exactly seven planning paths and is non-subject.
3. S4 alone modifies the governance contract test. It retains direct imports and fail-closed mutation
   negatives for frozen markers, B3/prior subject use, alternate S4/T4/V4 topology, evidence paths,
   HEAD ranges, and dynamic-import substitution.
4. T4 then V4 are the only non-merge evidence descendants; V4 pre-commit JSON targets T4 through
   `review_target_commit_sha` and never contains/requires a V4 SHA.
5. External post-commit validation identifies V4 and verifies exact named `S4..V4` range with only
   the two B3 evidence paths.

## Historical B2 Record (frozen provenance)

> **B2 correction override:** B0/S1/T1/V1、B1 及其 invalid review record are frozen provenance.
> Before implementation, only the seven B2 planning artifacts receive a temporary-index verified
> Git tree/blob review and non-subject B2 baseline commit with post-commit validation. The sole
> subsequent subject is test-only S3; its only allowed non-merge descendants are T3 then V3,
> verified as `S3..V3`, never `HEAD`.

### Historical B2 Acceptance Criteria

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

### Historical B2 Behavioral Scenarios

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

### Historical B2 Error / Edge Cases

- Missing/non-approved correction review, or correction review evidence written after any
  implementation change, blocks implementation and subject creation.
- Missing/failing Tester evidence, mismatched SHA, merge, extra path or third descendant
  invalidates the chain and cannot be repaired by reusing legacy/recovery evidence.
- An undeclared path, provenance migration, standalone correction skill or lifecycle action
  is returned to Planner/Human, not silently added to this topic.
