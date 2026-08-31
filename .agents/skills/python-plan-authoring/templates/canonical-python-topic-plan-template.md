# <topic>

## Goal / Outcome

- State one observable Python-library outcome.

## Scope

- **In scope**:
- **Out of scope**:

## Locked Decisions

- Record decisions that downstream roles must not rediscover.

## Boundaries / Exclusions

- State BC and adjacent-topic boundaries.

## Status / Allowed Transitions

- **Current**: `planned`
- **Allowed transitions**: use only `plan/agent-handoff-workflow.md` values.

## Artifact Paths

| Artifact | Path | Owner | Role |
| --- | --- | --- | --- |
| Topic plan | `plan/<topic>/<topic>.plan.md` | Planning actor | Execution contract |
| Topic spec | `plan/<topic>/<topic>.spec.md` | Planning actor | Behavior contract |
| Step tracker | `plan/<topic>/<topic>.step.md` | Creator | Progression truth |

## Python implementation metadata

### Non-goals

- Will not:
- Will not:
- Will not:

### Current Context

### Requirements

### Decisions

- Async-planning status: exempt|triggered — cite exemption|trigger evidence:
- Module/package placement:
- New public API:
- Interface changes:
- Breaking changes allowed:
- New dependencies:
- Error-handling strategy:
- Typing strategy:

### Public Contract / API Changes

### Affected Files / Modules

### Test Plan

- Happy path:
- Invalid input:
- Edge case:
- Regression:
- Backward compatibility:

### Risks

### Rollback Plan

## Implementation Steps

1. Name a concrete file and action.

## Validation / Acceptance Checks

- Name runnable validation commands or the project config that supplies them.

## Reviewer Handoff

```json
{
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "copilot_feedback_triage": {"ADDRESS": [], "DISCUSS": [], "SKIP": []}
}
```

## Post-merge / release actions

State the explicit no-release or release action.

## Open Questions / Unresolved Items

None.
