# Workflow plan-contract alignment

## Goal / Outcome

- Align the repo-local Python planning workflow to one canonical topic-plan
  contract and add a runnable conformance fixture.

## Scope

- **In scope**: the analysis artifacts for this topic; Python workflow skills,
  templates, and references under `.agents/skills/`; a conformance fixture and
  pytest test under `tests/`.
- **Out of scope**: product library code, Business Capability implementation,
  package public APIs, dependencies, README/VERSION changes, releases, and
  unrelated `pyproject.toml` changes.

## Locked Decisions

- `plan/topic-plan-contract.md` remains the governing topic-plan authority.
- A Python topic uses one canonical plan, not a second 13-section plan.
- Python-specific information lives in `Python implementation metadata`.
- This topic is review-ready-only and does not affect stable-library surfaces.
- The fixture is a workflow conformance artifact, not an Identity topic.

## Boundaries / Exclusions

- Do not change Identity, Response Reuse, CacheStore, runtime, execution, or
  provider responsibilities.
- Do not make the wrapper workflow an autonomous orchestrator or simulate an
  independent approval.
- Do not modify files outside the declared paths; surface later drift for a
  new topic plan.

## Status / Allowed Transitions

- **Current**: `approved`
- **Execution model**: creator work is followed by independent reviewer JSON
  handoff; this topic stops before publish and release.
- **Allowed transitions**: `creator-in-progress` -> `review-ready` ->
  `reviewer-in-progress` -> `approved|needs-rework`; `needs-rework` ->
  `creator-in-progress`; `approved` -> `publish-in-progress` only after a
  separate human instruction.

## Artifact Paths

| Artifact | Path | Owner | Role |
| --- | --- | --- | --- |
| Requirements | `analysis/workflow-plan-contract-alignment/requirements.md` | Planning actor | Business and scope guardrail |
| Technical specification | `analysis/workflow-plan-contract-alignment/technical-spec.md` | Planning actor | Execution-facing schema mapping |
| Topic plan | `plan/workflow-plan-contract-alignment/workflow-plan-contract-alignment.plan.md` | Planning actor | Execution contract |
| Topic spec | `plan/workflow-plan-contract-alignment/workflow-plan-contract-alignment.spec.md` | Planning actor | Acceptance scenarios |
| Step tracker | `plan/workflow-plan-contract-alignment/workflow-plan-contract-alignment.step.md` | Creator | Progression truth |
| Review log | `plan/workflow-plan-contract-alignment/workflow-plan-contract-alignment.review-log.md` | Reviewer | Routing truth for reviewer-driven rework |
| Topic summary | `plan/workflow-plan-contract-alignment/workflow-plan-contract-alignment.summary.md` | Main Agent | Required close and next-handoff truth |
| Python plan authoring skill | `.agents/skills/python-plan-authoring/` | Creator | Canonical plan and step templates |
| Python plan review skill | `.agents/skills/python-plan-review/` | Creator | Python metadata review contract |
| Python TDD skill | `.agents/skills/python-tdd-test-authoring/` | Creator | RED-test authoring contract |
| Python implementation review skill | `.agents/skills/python-implementation-review/` | Creator | Plan-to-implementation traceability contract |
| Python workflow wrapper | `.agents/skills/python-implementation-workflow/` | Creator | Parent workflow sequencing contract |
| Step creation skill | `.agents/skills/step-creator/` | Creator | Canonical Python step rendering |
| Step tracker skill | `.agents/skills/plan-step-tracker/` | Creator | Read-only progression and gate query |
| Fixture tests | `tests/fixtures/python-topic-plan-contract/`, `tests/test_python_topic_plan_contract.py` | Creator | Executable conformance evidence |

README.md, VERSION, and `.github/copilot-instructions.md` are not modified.

## Python implementation metadata

### Non-goals

- Will not add a product-library module or public import.
- Will not introduce async runtime behaviour or dependencies.
- Will not publish, tag, or promise stable-library compatibility.

### Current Context

The repository has a canonical topic-plan contract and independent plan
reviewer, but Python-specific skills still require an incompatible 13-section
top-level plan. The existing package remains an empty tooling baseline.

### Requirements

- Every Python workflow gate accepts the canonical plan plus metadata profile.
- Python step templates meet the repo's required step headings.
- A fixture test detects future divergence without production code.

### Decisions

- Async-planning status: exempt — cite exemption evidence: this topic changes
  documentation, templates, and synchronous test fixtures only; it introduces
  no async boundary, lifecycle, concurrency, timeout, or cancellation policy.
- Module/package placement: `.agents/skills/` workflow instructions and
  `tests/` conformance files.
- New public API: no.
- Interface changes: workflow artifact schema only.
- Breaking changes allowed: yes, for untracked internal workflow guidance that
  currently cannot satisfy repository authority.
- New dependencies: no.
- Error-handling strategy: skills return BLOCKED or needs-rework when required
  canonical fields are absent; fixture tests fail on schema drift.
- Typing strategy: fixture test is fully typed Python with no `Any`.

### Public Contract / API Changes

The public contract is the repo-local plan/step artifact format. No Python
package API changes.

### Affected Files / Modules

- `.agents/skills/python-plan-authoring/`, `python-plan-review/`,
  `python-tdd-test-authoring/`, and `python-implementation-review/`
- `.agents/skills/step-creator/`, `plan-step-tracker/`, and
  `python-implementation-workflow/`
- `tests/fixtures/python-topic-plan-contract/` and
  `tests/test_python_topic_plan_contract.py`

### Test Plan

- Happy path: a complete canonical Python fixture is accepted.
- Invalid input: missing required metadata heading is rejected.
- Edge case: lowercase `[x]` remains pending for the implementation gate.
- Regression: fixed lifecycle steps do not block the implementation-only gate.
- Backward compatibility: standard canonical topic-plan headings remain
  present and in order.

### Risks

Overly broad wording could make the new profile harder to follow than the old
schema. References and templates must use identical names.

### Rollback Plan

Revert the declared `.agents/skills/`, `tests/`, `analysis/`, and `plan/`
paths as one topic change.

## Implementation Steps

1. Update the Python authoring and review skills/templates to require the
   canonical plan plus `Python implementation metadata` profile.
2. Update TDD, implementation review, step creation, tracker references, and
   wrapper workflow to consume the same plan and step profile.
3. Add a complete fixture plan/spec/step and pytest conformance test.
4. Run fixture, tracker, and repository validation commands; record any
   independent-review work as pending rather than self-approving.

## Validation / Acceptance Checks

- No Python workflow skill retains a 13-top-level-section prerequisite.
- The templates and fixture carry the exact metadata and step headings.
- The fixture test verifies the behaviour described in its Test Plan.
- `uv run pytest tests/test_python_topic_plan_contract.py` and the tracker
  tests pass, alongside the repository validation suite.
- A later independent reviewer returns the required JSON handoff object.

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

When a reviewer finding controls rework or another review round, the Reviewer
records its verdict and the required repair in the declared review log. The log
is routing history only; this plan remains the current execution contract.

## Post-merge / release actions

No repository release action is required. A human must explicitly authorise
any later commit, push, pull request, or follow-up product topic. Before the
topic is closed or handed to that actor, Main Agent creates the declared summary
artifact with `current state`, `completed`, `not completed`, `required
follow-up`, and `next handoff` fields; `next handoff` names the next actor and
next step.

## Open Questions / Unresolved Items

None. Independent plan review remains pending by workflow design.
