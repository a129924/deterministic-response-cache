{
  "schema_version": "observer-dispatcher-governance.correction-b2-tester-evidence.v1",
  "correction_id": "observer-dispatcher-governance/high/b2",
  "actor": "Tester",
  "implementation_subject_sha": "b83b8e731e07a0dc6c7c219e5713fdc3ca92e6d9",
  "subject_verification": {
    "expected_sha": "b83b8e731e07a0dc6c7c219e5713fdc3ca92e6d9",
    "observed_sha": "b83b8e731e07a0dc6c7c219e5713fdc3ca92e6d9",
    "command": "git show -s --format='S3=%H%nparents=%P%nsubject=%s' b83b8e731e07a0dc6c7c219e5713fdc3ca92e6d9 && git show --format= --name-status b83b8e731e07a0dc6c7c219e5713fdc3ca92e6d9",
    "result": "passing"
  },
  "commands": [
    {
      "command": "git show -s --format='S3=%H%nparents=%P%nsubject=%s' b83b8e731e07a0dc6c7c219e5713fdc3ca92e6d9 && git show --format= --name-status b83b8e731e07a0dc6c7c219e5713fdc3ca92e6d9",
      "exit_code": 0,
      "result": "passing"
    },
    {
      "command": "git diff --name-status b10406604c05a28b50757ef51e56741725ccb13e 2075fc91253da1d43eb77dee3b84f4ab63557e65^{tree} && git cat-file -e b10406604c05a28b50757ef51e56741725ccb13e^{tree}",
      "exit_code": 0,
      "result": "passing"
    },
    {
      "command": "uv run pytest tests/test_observer_dispatcher_governance_contract.py",
      "exit_code": 0,
      "result": "passing (20 passed)"
    },
    {
      "command": "uv run pytest",
      "exit_code": 0,
      "result": "passing (42 passed)"
    },
    {
      "command": "uv run pyright",
      "exit_code": 0,
      "result": "passing (0 errors, 0 warnings, 0 informations)"
    },
    {
      "command": "uv run tach check",
      "exit_code": 0,
      "result": "passing (no validation failures; reported no first-party imports warning)"
    },
    {
      "command": "uv run pre-commit run --all-files",
      "exit_code": 0,
      "result": "passing (ruff format, ruff check, pyright, tach check)"
    },
    {
      "command": "rg -n \"^(import deterministic_response_cache)$|importlib|__import__|sys\\.modules\" tests",
      "exit_code": 0,
      "result": "passing (tests/test_package_import.py retains direct import; no dynamic-import matches)"
    },
    {
      "command": "git diff --check 2075fc91253da1d43eb77dee3b84f4ab63557e65 b83b8e731e07a0dc6c7c219e5713fdc3ca92e6d9",
      "exit_code": 0,
      "result": "passing"
    }
  ],
  "correction_test_result": "passing",
  "repository_validation_result": "passing",
  "verdict": "passing",
  "next_gate": "Only independent Reviewer V3 may follow this T3 evidence, must attest the same S3 SHA, and must verify named S3..V3 contains exactly the T3 and V3 evidence paths.",
  "timestamp": "2026-09-02T06:11:20Z"
}
