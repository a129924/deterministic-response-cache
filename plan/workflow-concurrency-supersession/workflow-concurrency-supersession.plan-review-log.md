{
  "schema_version": "1.0",
  "topic": "workflow-concurrency-supersession",
  "candidate_commit": "4de24817bc197f04f067c5721311e369da1dc9c8",
  "candidate_tree": "fac42c2c1c88a2773c6722d185c7daa26e1aaaaa",
  "candidate_parent": "928d76ee4e4ee7386289cabf03bc0fe8e6618b4a",
  "candidate_admission": {
    "is_merge_commit": false,
    "first_parent": "928d76ee4e4ee7386289cabf03bc0fe8e6618b4a",
    "candidate_diff_paths": [
      "plan/workflow-concurrency-supersession/workflow-concurrency-supersession.plan.md",
      "plan/workflow-concurrency-supersession/workflow-concurrency-supersession.spec.md",
      "plan/workflow-concurrency-supersession/workflow-concurrency-supersession.step.md"
    ]
  },
  "reviewed_planning_artifacts": [
    {
      "path": "analysis/workflow-concurrency-supersession/requirements.md",
      "blob_sha": "5b8b63451c03ced89db6864def64d7669aa85825"
    },
    {
      "path": "analysis/workflow-concurrency-supersession/technical-spec.md",
      "blob_sha": "cf5b54532a64d56f9f2f5a5ad0f5251e34acb92f"
    },
    {
      "path": "plan/workflow-concurrency-supersession/workflow-concurrency-supersession.plan.md",
      "blob_sha": "efeeab34e3a4aa4d28dcb5b40be4e51d6775a492"
    },
    {
      "path": "plan/workflow-concurrency-supersession/workflow-concurrency-supersession.spec.md",
      "blob_sha": "f68367eaab06cb7f17a8efda8926ee2afaec2040"
    },
    {
      "path": "plan/workflow-concurrency-supersession/workflow-concurrency-supersession.step.md",
      "blob_sha": "ab55da6d3fb25e862016c2e6bc8900477da471f3"
    }
  ],
  "review_basis": {
    "workflow_contracts": [
      {
        "path": "AGENTS.md",
        "blob_sha": "e8cbd313e03623bd8d26ef7a7ec95a27c4dc8c8c"
      },
      {
        "path": "plan/agent-handoff-workflow.md",
        "blob_sha": "f7e25531f7798f7007d4b8ebacb50fc9687b3322"
      },
      {
        "path": "plan/topic-plan-contract.md",
        "blob_sha": "26e16b5291b176455e213c8a9335560e0e00d352"
      }
    ],
    "excluded_inputs": [
      "chat",
      "branch",
      "summary",
      "GOAL.md",
      ".github/agents/**",
      "legacy receipt candidate content"
    ]
  },
  "verdict": "approved",
  "blocking_issues": [],
  "copilot_feedback_triage": {
    "ADDRESS": [],
    "DISCUSS": [],
    "SKIP": []
  },
  "next_gate": {
    "required_phase": "approved-receipt-commit-pending",
    "required_actor": "Independent Implementer",
    "required_action": "Commit this unchanged approved receipt as the sole standalone evidence-only path, then return the topic to Planner re-preflight.",
    "eligible_following_gate": "bounded-contract-implementation only after Planner re-preflight",
    "does_not_authorize": [
      "publish",
      "pull-request approval",
      "merge",
      "release",
      "tag",
      "post-merge"
    ]
  }
}
