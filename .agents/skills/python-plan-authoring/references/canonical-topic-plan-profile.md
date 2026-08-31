# Canonical Python Topic-Plan Profile

Python implementation work uses the single execution-facing artifact at
`plan/<topic>/<topic>.plan.md`. It must retain the eleven canonical topic-plan
sections from `plan/topic-plan-contract.md` in their canonical order.

Python topics add one bounded top-level section immediately after `## Artifact
Paths`:

```markdown
## Python implementation metadata
### Non-goals
### Current Context
### Requirements
### Decisions
### Public Contract / API Changes
### Affected Files / Modules
### Test Plan
### Risks
### Rollback Plan
```

The canonical sections provide the remaining shared information:

| Python planning information | Canonical location |
| --- | --- |
| Goal | `## Goal / Outcome` |
| Implementation Steps | `## Implementation Steps` |
| Validation Commands | `## Validation / Acceptance Checks` |
| Open Questions | `## Open Questions / Unresolved Items` |

`### Decisions` must start with `Async-planning status: triggered|exempt — cite
...`, answer module placement, public API, interface changes, breaking changes,
dependencies, error handling, and typing, and add the established async
subsections when triggered.

Python `.step.md` files contain `Workflow Stages`, `Actionable Steps`,
`Implementation Steps`, `Main Agent Actionable Steps — Fixed Tail`, and
`Handoff / Gate Notes`. Only `Implementation Steps` is the
implementation-completion gate.

The general `plan-reviewer` remains the official topic-plan approval gate and
returns its required JSON handoff. `python-plan-review` is the specialised
Python-profile check; it does not replace that gate.
