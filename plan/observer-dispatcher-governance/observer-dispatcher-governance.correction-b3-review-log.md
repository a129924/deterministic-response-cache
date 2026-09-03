{
  "schema_version": "observer-dispatcher-governance.correction-b3-plan-review.v1",
  "correction_id": "observer-dispatcher-governance/high/b3",
  "review_kind": "correction-b3-plan",
  "severity": "high",
  "routing_state": "PLANNER_REPLAN",
  "reviewed_tree_sha": "396e991b4e3dc14a396f01a4e0a77da800460d6f",
  "reviewed_artifacts": [
    {
      "path": "plan/agent-handoff-workflow.md",
      "blob_sha": "c479128c1ada6ded61eb55df304a3b7fd8212578"
    },
    {
      "path": "plan/topic-plan-contract.md",
      "blob_sha": "628a1998d2069a41d0f84b88afe6edb981418e06"
    },
    {
      "path": "plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md",
      "blob_sha": "18e2b706e65c0381c60cba140a83ab3678bc2689"
    },
    {
      "path": "plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md",
      "blob_sha": "0380dcae535cd2b4b4528e98614727416a169d5f"
    },
    {
      "path": "plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md",
      "blob_sha": "21304c6262d3166197656cd81405455ac45a9367"
    },
    {
      "path": "plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b3-plan.md",
      "blob_sha": "bcbdbb8b55cd1e8a8b0e129a450e0434ce79751d"
    },
    {
      "path": "plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b3-step.md",
      "blob_sha": "84135966d82b1d1918c00c3d748d3f3da8160e5e"
    }
  ],
  "review_basis": "Independent B3 correction-plan review of only the declared seven uncommitted planning paths. A temporary index was seeded from HEAD c9b7a066408588e83bc9ceb73e6830eaba08ac14, staged only those seven paths, and produced reviewed_tree_sha with git write-tree. git rev-parse <tree>^{tree} and git cat-file -e <tree>^{tree} both verified that object; every listed blob_sha was read from that verified tree. The reviewed contract makes B0/B1/B2/S1/S3/T1/T3/V1/V3 and normal/recovery artifacts frozen nonrouting provenance, leaves B3 non-subject, reserves the sole test path for S4, requires only S4 -> T4 -> V4 and named S4..V4 with exactly the two B3 evidence paths, and requires the pre-commit V4 record to target pre-existing T4 without a V4 SHA.",
  "verdict": "approved",
  "blocking_issues": [],
  "copilot_feedback_triage": {
    "ADDRESS": [],
    "DISCUSS": [],
    "SKIP": []
  },
  "timestamp": "2026-09-02T06:30:57Z"
}
