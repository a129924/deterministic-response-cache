{
  "schema_version": "observer-dispatcher-governance.correction-tester-evidence.v1",
  "correction_id": "observer-dispatcher-governance/high",
  "actor": "Tester",
  "implementation_subject_sha": "f1a2ae1334b03ea0c5eea7612909ef77c089f38c",
  "subject_verification": {
    "expected_sha": "f1a2ae1334b03ea0c5eea7612909ef77c089f38c",
    "observed_sha": "f1a2ae1334b03ea0c5eea7612909ef77c089f38c",
    "command": "git rev-list --parents -n 1 f1a2ae1334b03ea0c5eea7612909ef77c089f38c",
    "result": "passing"
  },
  "commands": [
    {
      "command": "git diff-tree --no-commit-id --name-status -r f1a2ae1334b03ea0c5eea7612909ef77c089f38c",
      "exit_code": 0,
      "result": "passing"
    },
    {
      "command": "test \"$(git diff-tree --no-commit-id --name-only -r f1a2ae1334b03ea0c5eea7612909ef77c089f38c | wc -l | tr -d ' ')\" -eq 13",
      "exit_code": 0,
      "result": "passing"
    },
    {
      "command": "git log --merges --format=%H f1a2ae1334b03ea0c5eea7612909ef77c089f38c^..f1a2ae1334b03ea0c5eea7612909ef77c089f38c",
      "exit_code": 0,
      "result": "passing"
    },
    {
      "command": "git diff --check f1a2ae1334b03ea0c5eea7612909ef77c089f38c^..f1a2ae1334b03ea0c5eea7612909ef77c089f38c",
      "exit_code": 0,
      "result": "passing"
    },
    {
      "command": "uv run pytest tests/test_observer_dispatcher_governance_contract.py",
      "exit_code": 0,
      "result": "passing"
    },
    {
      "command": "uv run pytest .agents/skills/plan-step-tracker/tests/test_step_tracker.py",
      "exit_code": 0,
      "result": "passing"
    },
    {
      "command": "uv run pytest",
      "exit_code": 0,
      "result": "passing"
    },
    {
      "command": "uv run pyright",
      "exit_code": 0,
      "result": "passing"
    },
    {
      "command": "uv run tach check",
      "exit_code": 0,
      "result": "passing"
    },
    {
      "command": "uv run pre-commit run --all-files",
      "exit_code": 0,
      "result": "passing"
    }
  ],
  "correction_test_result": "passing",
  "repository_validation_result": "passing",
  "verdict": "passing",
  "timestamp": "2026-09-02T03:31:41Z"
}
