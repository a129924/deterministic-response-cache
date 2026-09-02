# Observer / Dispatcher Governance — B3 Correction Plan

## Trigger / Frozen Provenance

- V3 has a frozen `needs-rework` outcome but no repo-visible V3 review record. It cannot be amended,
  inferred, or reused. B0/B1/B2/S1/S3/T1/T3/V1/V3 plus normal/recovery artifacts are frozen,
  nonrouting historical provenance.

## Scope / Direction

- B3 changes only seven planning paths before review: the two shared contracts, parent plan/spec/step,
  and this B3 plan/step. It creates no evidence and no commit.
- Independent Plan-Reviewer uses a temporary index seeded from HEAD, stages only those paths, runs
  `git write-tree`, verifies it with `git rev-parse <tree>^{tree}` and `git cat-file -e <tree>^{tree}`,
  and records one tree-derived blob revision per path in `correction-b3-review-log.md`.
- Independent Implementer commits the unchanged approved record plus exact reviewed set as non-subject
  B3, then proves every recorded blob matches both the reviewed tree and B3 and the only tree diff
  path is the B3 review log.
- Only approved/validated B3 permits non-merge S4, which changes only
  `tests/test_observer_dispatcher_governance_contract.py`. S4 is the sole current subject.

## T4 / V4 Evidence Contract

- T4 writes only `correction-b3-tester-evidence.md` for S4.
- V4 writes only `correction-b3-implementation-review-log.md` after T4. Its pre-commit record uses
  `review_target_commit_sha` equal to the already-existing T4 SHA. No V4 SHA field, requirement, or
  self-reference is permitted; post-commit validation independently identifies V4.
- The only valid descendant topology is non-merge `S4 -> T4 -> V4`. Named
  `git diff --name-status S4..V4` contains exactly the two B3 evidence paths, never HEAD.

## Acceptance Delta

- S4 direct, non-dynamic-import tests must fail closed if any B0/B1/B2/S1/S3/T1/T3/V1/V3 frozen
  provenance becomes routing evidence; B3 or any prior commit becomes a subject; S4 is not the only
  subject; topology is not non-merge S4 -> T4 -> V4; the named S4..V4 range, exact two B3 evidence
  paths, or no-HEAD rule changes; or mutation negatives remove any of these markers.
- Direct imports remain the existing test behavior; `importlib`, `__import__`, and `sys.modules`
  substitutions are forbidden.
- All prior artifacts remain byte-for-byte unchanged; no thread, publish, release, or lifecycle work
  is authorized by this plan.
