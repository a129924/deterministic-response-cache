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
- **Execution model**: creator -> independent Tester -> reviewer -> bounded publish -> draft PR ->
  Human merge.
- **Allowed transitions**:
  - `planned` -> `creator-in-progress`
  - `creator-in-progress` -> `tester-in-progress`
  - `tester-in-progress` -> `review-ready`
  - `review-ready` -> `reviewer-in-progress`
  - `reviewer-in-progress` -> `approved|needs-rework`
  - `needs-rework` -> `creator-in-progress`
  - `approved` -> `creator-in-progress|publish-in-progress`
  - `publish-in-progress` -> `pr-open`
  - `pr-open` -> `needs-rework`
  - `pr-open` -> `merged`
  - `merged` -> terminal

Do not add a direct `publish-in-progress` -> `merged` transition. Tester evidence must attest the
same immutable implementation subject later reviewed by Reviewer; only Human may merge from
`pr-open`.

## Artifact Paths

| Artifact | Path | Owner | Role |
| --- | --- | --- | --- |
| Topic plan | `plan/<topic>/<topic>.plan.md` | Planning actor | Execution contract |
| Topic spec | `plan/<topic>/<topic>.spec.md` | Planning actor | Behavior contract |
| Step tracker | `plan/<topic>/<topic>.step.md` | Creator | Progression truth |

If this topic declares a correction route, conditionally add exact rows for correction plan,
correction step, correction-plan review log, Tester evidence, and implementation-review log.
Each row must state its write owner, ordering, and schema authority;
do not add this extension to topics without a declared correction route.

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
