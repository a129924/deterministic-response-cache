# Python topic plan contract fixture

## Goal / Outcome

- Demonstrate a valid canonical Python topic plan without product behaviour.

## Scope

- **In scope**: fixture-only documentation.
- **Out of scope**: package code and public API changes.

## Locked Decisions

- This is a non-stable fixture and has no release action.

## Boundaries / Exclusions

- Do not use a provider, cache, runtime, or production module.

## Status / Allowed Transitions

- **Current**: `planned`
- **Allowed transitions**: `planned` -> `creator-in-progress` -> `review-ready`.

## Artifact Paths

| Artifact | Path | Owner | Role |
| --- | --- | --- | --- |
| Fixture plan | `tests/fixtures/python-topic-plan-contract/python-topic-plan-contract.plan.md` | Test owner | Profile input |

README.md and VERSION are not modified.

## Python implementation metadata

### Non-goals

- Will not add package code.
- Will not add dependencies.
- Will not make a stable API promise.

### Current Context

This fixture exercises the canonical Python plan profile.

### Requirements

- The plan has every required profile heading.

### Decisions

- Async-planning status: exempt — cite exemption evidence: documentation-only fixture with no async boundary, lifecycle, concurrency, timeout, or cancellation change.
- Module/package placement: `tests/fixtures/python-topic-plan-contract/`.
- New public API: no.
- Interface changes: no.
- Breaking changes allowed: no.
- New dependencies: no.
- Error-handling strategy: invalid fixtures fail conformance checks.
- Typing strategy: fully typed fixture validator with no `Any`.

### Public Contract / API Changes

No package API change.

### Affected Files / Modules

- `tests/fixtures/python-topic-plan-contract/`

### Test Plan

- Happy path: complete fixture is accepted.
- Invalid input: missing metadata is rejected.
- Edge case: lowercase marker is pending.
- Regression: fixed stages do not alter implementation gating.
- Backward compatibility: canonical headings remain available.

### Risks

Fixture headings could diverge from skill instructions.

### Rollback Plan

Revert fixture-only files.

## Implementation Steps

1. Read the fixture plan.

## Validation / Acceptance Checks

- Run `uv run pytest tests/test_python_topic_plan_contract.py`.

## Reviewer Handoff

```json
{
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "copilot_feedback_triage": {
    "ADDRESS": [],
    "DISCUSS": [],
    "SKIP": []
  }
}
```

## Post-merge / release actions

No release action.

## Open Questions / Unresolved Items

None.
