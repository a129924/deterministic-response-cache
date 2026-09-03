# Observer / Dispatcher Governance — B2 Correction Plan

## Trigger / Evidence

- B1 correction review record has an invalid `reviewed_tree_sha`; it is frozen invalid provenance
  and cannot be amended, reused, or treated as a current gate.

## Scope / Direction

- This B2 route changes only seven planning artifacts before review: the two shared contracts,
  parent plan/spec/step, and this B2 plan/step. It creates no evidence and no commit.
- B0/S1/T1/V1, B1, its invalid review log, and all earlier normal/recovery evidence remain frozen.
  B2 is a one-time verified-tree baseline, never a subject.
- Plan-Reviewer must use a temporary index seeded from `HEAD`, add only the seven B2 planning paths,
  run `git write-tree`, and verify that object with `git rev-parse <tree>^{tree}` and
  `git cat-file -e <tree>^{tree}` before recording tree-derived blobs.
- Independent Implementer commits the unchanged approved record plus exactly the reviewed set as B2,
  then proves the record tree exists, its seven blobs match both reviewed tree and B2, and the
  reviewed-tree-to-B2 name-status diff only adds the B2 review log.
- After approved/validated B2, S3 may modify only
  `tests/test_observer_dispatcher_governance_contract.py`; T3 and V3 are its only permitted
  non-merge evidence-only descendants, verified as `S3..V3`, never `HEAD`.

## Acceptance Delta

- B2 review record has a reproducible Git tree object and exactly one tree-derived blob per B2 path.
- S3 detects frozen-provenance misuse, B1/B2 as subject, and every topology except T3 then V3.
- T3 and V3 attest the same S3 SHA, with V3 referencing passing T3; final range has exactly the two
  declared B2 evidence paths.

## Parent Sync / Retention / Closure

- Parent sync precedes B2 review. B2 correction plan/step remain retained correction delta; parent
  plan/spec/step remain current execution truth. No evidence, commit, thread, lifecycle action, or
  correction closure is authorized by this artifact.
