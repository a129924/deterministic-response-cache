---
topic: observer-dispatcher-governance
correction: high
state: PLANNER_REPLAN
created: 2026-09-01
---

# Observer / Dispatcher Governance — High Correction Steps

## Ordered Checkpoints

- [X] 1. **Planner:** freeze correction direction, exact paths, provenance treatment and new
  subject rules.
- [X] 2. **Plan-Creator:** synced parent plan/spec/step and created correction plan/step only.
- [ ] 3. **Correction Plan-Reviewer:** under the narrow `B0` exception, before any declared
  implementation path changes, tree/blob review exactly seven uncommitted planning artifacts and
  write one schema-complete `correction-review-log.md`; `needs-rework` returns to checkpoint 1.
- [ ] 4. **Independent Implementer:** only on `approved` and existing Human commit authorization,
  commit the unchanged correction review record together with those seven reviewed artifacts as
  `B0`; `B0` is a baseline and not a subject; do not implement yet.
- [ ] 5. **Independent Implementer:** only after `B0`, complete and commit declared expanded
  implementation as non-merge `S1`, the replacement immutable subject.
- [ ] 6. **Tester:** attest `S1` in `correction-tester-evidence.md` as linear evidence-only `T1`.
- [ ] 7. **Reviewer:** after same-`S1` passing `T1` evidence, write final correction implementation
  review as `V1` and verify the non-merge exact two-path range `S1..V1`, never a `HEAD` range.
- [ ] 8. **Human boundary:** stop; no lifecycle action without new explicit direction.

## Required Evidence Schemas

- `correction-review-log.md` contains exactly one object with `review_kind: correction-plan` and
  all seven paths listed in the shared contract exactly once:

```json
{
  "schema_version": "observer-dispatcher-governance.correction-plan-review.v1",
  "correction_id": "observer-dispatcher-governance/high",
  "review_kind": "correction-plan",
  "severity": "high",
  "routing_state": "PLANNER_REPLAN",
  "reviewed_tree_sha": "<exact tree SHA for the seven uncommitted planning artifacts>",
  "reviewed_artifacts": [{"path": "<exact planning path>", "blob_sha": "<exact reviewed blob SHA>"}],
  "review_basis": "<independent correction-plan review basis>",
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "copilot_feedback_triage": {"ADDRESS": [], "DISCUSS": [], "SKIP": []},
  "timestamp": "<RFC 3339 timestamp>"
}
```

- `correction-tester-evidence.md` contains exactly one object:

```json
{
  "schema_version": "observer-dispatcher-governance.correction-tester-evidence.v1",
  "correction_id": "observer-dispatcher-governance/high",
  "actor": "Tester",
  "implementation_subject_sha": "<full immutable implementation commit SHA>",
  "subject_verification": {"expected_sha": "<same SHA>", "observed_sha": "<same SHA>", "command": "<exact command>", "result": "passing|failing"},
  "commands": [{"command": "<exact command>", "exit_code": 0, "result": "passing|failing"}],
  "correction_test_result": "passing|failing",
  "repository_validation_result": "passing|failing",
  "verdict": "passing|failing",
  "timestamp": "<RFC 3339 timestamp>"
}
```

- `correction-implementation-review-log.md` contains exactly one object:

```json
{
  "schema_version": "observer-dispatcher-governance.correction-implementation-review.v1",
  "correction_id": "observer-dispatcher-governance/high",
  "review_kind": "correction-implementation",
  "severity": "high",
  "implementation_subject_sha": "<full immutable implementation commit SHA>",
  "reviewed_commit_sha": "<V1 containing only two allowed descendants from S1>",
  "tester_evidence": {"path": "plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-tester-evidence.md", "revision": "<Tester evidence commit SHA>", "implementation_subject_sha": "<same SHA>", "verdict": "passing"},
  "reviewed_artifacts": [{"path": "<exact declared implementation or evidence path>", "revision": "<reviewed revision>"}],
  "review_basis": "<independent implementation review basis>",
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "copilot_feedback_triage": {"ADDRESS": [], "DISCUSS": [], "SKIP": []},
  "timestamp": "<RFC 3339 timestamp>"
}
```

Plan-Reviewer writes only the correction-plan verdict; Tester writes only factual test results;
Reviewer writes only its implementation verdict. Planner alone decides status, route and next role.

## Invariants

- Old epoch is terminal at `R0=cb3f66c60e95e5580cb2b30632d0d5ed9f0d0ee9`; its only predicate is
  `ecc5b6f61bacc5493ca3a9f1012d1bfdd43a810c..cb3f66c60e95e5580cb2b30632d0d5ed9f0d0ee9`.
- All normal/recovery evidence and subjects are frozen provenance for checkpoints 3–7.
- The final range `S1..V1` is exactly additions of
  `observer-dispatcher-governance.correction-tester-evidence.md` then
  `observer-dispatcher-governance.correction-implementation-review-log.md`.
