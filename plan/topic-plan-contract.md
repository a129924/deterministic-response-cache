# Topic Plan Contract

## Purpose

Define the shared repo-level contract for topic-plan authority in this
repository.

This file is the shared repo-local authority for topic-plan structure,
review basis, fallback behavior, and contract-level blocking semantics.

This document governs topic-plan contract semantics. It does not replace:

- `AGENTS.md` as the governance canonical source
- `plan/agent-handoff-workflow.md` as the repo-level workflow-phase contract
- `plan/<topic>/<topic>.plan.md` as the topic-specific execution contract

## Scope

- This document defines the repo-level authority ordering for topic-plan
  contract semantics.
- This document defines the required section contract for
  `plan/<topic>/<topic>.plan.md`.
- This document defines repo-level reviewer handoff expectations and fallback
  review basis for topic plans.
- This document does not define workflow phases, stop points, release routing,
  or PR-loop behavior.
- This document does not authorize convergence, projection, runtime
  adaptation, or skill-surface migration work.

## Contract Version

- `contract_version`: `1.0`
- Versioning is human-facing and repo-local.
- Future strict verification may add `contract_hash`, but `contract_version`
  remains the primary contract-language field for this repository topic-plan
  surface.

## Authority Ordering

When topic-plan authority questions arise, use this order:

1. `AGENTS.md`
2. `plan/agent-handoff-workflow.md`
3. `plan/topic-plan-contract.md`
4. `plan/<topic>/<topic>.plan.md`
5. `skills/plan-creator/**` and `skills/plan-reviewer/**`

Interpretation rules:

- `AGENTS.md` governs repo-level governance and source-of-truth boundaries.
- `plan/agent-handoff-workflow.md` governs repo-level workflow phases, stop
  points, roles, and status transitions.
- This document governs repo-level topic-plan contract semantics.
- Each topic plan governs one topic's bounded execution contract inside the
  repo-level governance and workflow constraints above.
- `skills/plan-creator/**` and `skills/plan-reviewer/**` are consumer guidance
  and evidence surfaces only; they do not own repo-level contract authority.

## Required Topic-Plan Sections

Every repo-visible topic plan must include these sections:

1. `Goal / Outcome`
2. `Scope`
3. `Locked Decisions`
4. `Boundaries / Exclusions`
5. `Status / Allowed Transitions`
6. `Artifact Paths`
7. `Implementation Steps`
8. `Validation / Acceptance Checks`
9. `Reviewer Handoff`
10. `Post-merge / release actions`
11. `Open Questions / Unresolved Items`

Section rules:

- Section names must stay canonical.
- A topic plan may add bounded topic-specific sections only when they do not
  contradict the required section set above.
- Topics that affect stable-library surfaces must add `Stable library metadata`
  and define timing explicitly.
- Topics that do not affect stable-library surfaces must state that intent
  explicitly instead of leaving it implicit.

## Shared Review Basis

Both planning skills must evaluate topic plans against this shared basis:

1. `plan/agent-handoff-workflow.md`
2. `plan/topic-plan-contract.md`
3. the local skill's own examples, checklist, template, and references

Local skill files may add implementation guidance or review heuristics, but
they must not redefine required sections, role ownership, fallback authority,
or blocking semantics away from this file.

## Execution-Start Input Model

For topic execution:

- `plan/<topic>/<topic>.plan.md` is the unconditional execution-start
  contract.
- `plan/<topic>/<topic>.step.md`,
  `plan/<topic>/<topic>.review-log.md`, and
  `plan/<topic>/<topic>.summary.md` are topic-local truth artifacts, not
  unconditional startup prerequisites.
- When present, they must be read according to their role semantics.
- When absent, execution may still begin unless the topic plan or repo-level
  workflow contract makes them conditionally required for the current stage.

## Artifact Path Rules

`Artifact Paths` is an executable contract and must use exact repo-visible
paths with owner and role.

Each listed artifact must include:

- exact repo-visible path
- owner
- role

Do not use vague labels such as `docs`, `skill folder`, `maybe version files`,
or other non-executable path descriptions.

If execution needs files outside the listed paths, repair the topic plan before
continuing.

If a topic uses correction artifacts, each parent artifact, correction
artifact, and any routing-controlling `review-log` or equivalent handoff path
must be listed explicitly.

## Topic-Plan Contract Rules

- `Implementation Steps` stay creator-owned; reviewer verdict logging,
  reviewer acceptance work, and Main Agent routing work do not belong there.
- `Reviewer Handoff` must be one machine-consumable JSON object.
- `Post-merge / release actions` must match the topic's actual stable-library
  and release timing.
- If a topic declares analysis artifacts as frozen prerequisites, execution may
  read and validate them only. Execution must not silently reopen or
  regenerate them without a separately approved scope change.
- Unsafe placeholders such as `TBD`, `later`, or `follow normal process` are
  contract failures when explicit workflow decisions are required.

## Reviewer Handoff Contract

The repo-level reviewer handoff contract for topic-plan review is:

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

Rules:

- The delivered reviewer handoff must be exactly one JSON object.
- `blocking_issues` is reserved for true contract-breaking problems.
- `copilot_feedback_triage` may be empty, but its three arrays must still be
  present.
- No prose may wrap or trail the final JSON reviewer verdict.

## Stable-Library Contract

If the topic affects stable-library surfaces, the plan must state:

- whether `README.md` changes
- whether `VERSION` changes
- when those changes occur
- whether post-merge release or tagging work exists

Do not defer these decisions with placeholders such as `TBD`, `later`, or
`follow normal process`.

## Fallback Rules

If the local topic-plan template is absent:

- `plan-creator` must fall back to the required section list in this file
- `plan-reviewer` must review against the required section list in this file

Neither skill may invent a new topic-plan shape when the template is absent.

## Blocking Semantics

Treat these as contract-breaking issues:

- missing required sections
- non-canonical or invalid status transitions
- vague or drifting `Artifact Paths`
- undeclared or mixed stable-library intent
- non-JSON reviewer handoff
- wrong post-merge or release timing
- mixed role ownership
- missing, contradictory, or insufficient frozen analysis prerequisites when a
  topic declares them as required execution inputs
- execution-meaning conflicts among `plan.md`, `step.md`, `review-log.md`, and
  `summary.md`
- conflicts between a required repo-level contract file and a topic-local truth
  artifact
- simulated role separation where one actor claims planner, reviewer,
  implementer, and final-gate completion without real separation
- placeholders where explicit contract is required

`plan-creator` must stop and ask when required planning inputs are missing or
would require guessing.

`plan-reviewer` must return `needs-rework` when any contract-breaking issue is
found in an otherwise reviewable plan.

If the plan file or required shared contract sources cannot be read, stop and
record that the review could not proceed on valid contract grounds.

Execution must stop and surface the issue when a contract-breaking conflict or
fake-separation condition is encountered. The executor must not silently choose
the more convenient artifact or role interpretation.

## Boundaries

- This document does not rewrite `skills/plan-creator/**` or
  `skills/plan-reviewer/**`.
- This document does not authorize edits under `skills/**`,
  `.github/skills/**`, `.codex/skills/**`, `.github/agents/**`, or
  `.codex/agents/**`.
- This document does not treat accepted Phase 1 planning inputs as approved
  implementation spec.
- Convergence, projection, runtime adaptation, `python-blueprint-review`
  absorption, and generic `copilot-instructions-init` convergence remain
  deferred to later bounded topics.

## Authority Boundaries

- Keep this contract repo-local.
- Do not externalize it to `~/.` or cross-repo shared storage in this topic.
- Do not let compatibility surfaces redefine this contract.
- Do not infer authority from `.github/skills/` or `.codex/skills/` presence.
