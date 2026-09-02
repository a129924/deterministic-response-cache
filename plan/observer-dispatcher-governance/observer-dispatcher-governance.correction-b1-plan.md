# Observer / Dispatcher Governance — B1 Correction Plan

## Trigger / Evidence

- Independent V1 returned `needs-rework`: the existing governance contract test does not fail closed
  for frozen B0/S1/T1/V1 provenance, the replacement subject reset, or the required evidence topology.

## Scope / Direction

- This B1 route changes only seven planning artifacts before review: the two shared contracts,
  parent plan/spec/step, and this B1 plan/step. It creates no evidence and no commit.
- B0/S1/T1/V1 and all earlier normal/recovery evidence remain frozen provenance. B1 is a one-time
  tree/blob-reviewed baseline, never a subject.
- After approved B1 is committed unchanged with exactly that reviewed set, S2 may modify only
  `tests/test_observer_dispatcher_governance_contract.py`. T2 and V2 are the only permitted
  non-merge evidence-only descendants; verification is `S2..V2`, never `HEAD`.

## Acceptance Delta

- The B1 review record has one tree SHA and exactly one path/blob entry for each B1 planning path.
- S2 detects frozen-provenance misuse, any subject other than S2, and every topology except T2 then V2.
- T2 and V2 attest the same S2 SHA, with V2 referencing passing T2; the final range has exactly the
  two declared B1 evidence paths.

## Parent Sync / Retention / Closure

- Parent sync precedes B1 review. B1 correction plan/step remain historical after backfill; parent
  plan/spec/step remain current execution truth. No evidence, commit, thread, lifecycle action, or
  correction closure is authorized by this artifact.
