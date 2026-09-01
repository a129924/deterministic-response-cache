# Recovery Tester Evidence — Observer / Dispatcher Governance

- `implementation_subject_sha`: `ecc5b6f61bacc5493ca3a9f1012d1bfdd43a810c`
- `actor`: `Tester`
- `timestamp`: `2026-09-01T09:08:33Z`

## Subject Verification

| command / check | result |
| --- | --- |
| `git rev-parse HEAD` | PASS — exactly `ecc5b6f61bacc5493ca3a9f1012d1bfdd43a810c`; checks were run against the immutable implementation subject, not a descendant. |
| `git status --short` before this record | PASS — no output. |
| `git diff-tree --no-commit-id --name-status -r ecc5b6f61bacc5493ca3a9f1012d1bfdd43a810c` | PASS — the planning-evidence subject contains only the five declared replan artifacts and `observer-dispatcher-governance.recovery-planning-review-evidence.md`. |
| `git log --merges --format=%H ecc5b6f61bacc5493ca3a9f1012d1bfdd43a810c^..ecc5b6f61bacc5493ca3a9f1012d1bfdd43a810c` | PASS — no output; the subject commit is not a merge. |
| `git diff --check ecc5b6f61bacc5493ca3a9f1012d1bfdd43a810c^..ecc5b6f61bacc5493ca3a9f1012d1bfdd43a810c` | PASS — no whitespace errors. |

## Declared Checks and Direct-Import Preservation

| command / check | result |
| --- | --- |
| `git diff --quiet ecc5b6f61bacc5493ca3a9f1012d1bfdd43a810c^..ecc5b6f61bacc5493ca3a9f1012d1bfdd43a810c -- tests/` | PASS — the immutable subject has no `tests/**` diff. |
| `git diff --quiet ecc5b6f61bacc5493ca3a9f1012d1bfdd43a810c^..ecc5b6f61bacc5493ca3a9f1012d1bfdd43a810c -- .github/agents/` | PASS — frozen provenance has no diff. |
| Direct-import inspection: `rg -n "^(import deterministic_response_cache)$|importlib|__import__|sys\\.modules" tests` | PASS — `tests/test_package_import.py` retains `import deterministic_response_cache`; no dynamic-import replacement was found under `tests/`. |
| `uv run pytest` | PASS — `22 passed`, including `tests/test_package_import.py::test_package_imports`. |
| `uv run pyright` | PASS — `0 errors, 0 warnings, 0 informations`. |
| `uv run tach check` | PASS — all modules validated; it emitted only its non-failing no-first-party-imports configuration warning. |
| `uv run pre-commit run --all-files` | PASS — `ruff format`, `ruff check`, `pyright`, and `tach check` passed. |

## Evidence Conclusion

- `verdict`: `passing`
- The declared repository checks and direct-import preservation pass for immutable subject `ecc5b6f61bacc5493ca3a9f1012d1bfdd43a810c`.
