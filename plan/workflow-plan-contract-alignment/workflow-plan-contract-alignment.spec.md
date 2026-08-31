# Workflow plan-contract alignment Specification

## Acceptance Criteria

1. A Python topic plan has all canonical topic-plan sections plus a complete
   `Python implementation metadata` section.
2. Python workflow skills no longer require a competing 13-top-level-section
   schema.
3. A Python step artifact includes the repository-required progression and
   handoff sections while keeping implementation completion scoped to
   `Implementation Steps`.
4. The fixture test detects missing profile headings and lowercase `[x]`.

## Behavioral Scenarios

### Scenario 1: Canonical Python plan passes the workflow profile

- **Given**: a topic plan with the canonical sections, complete metadata, a
  valid spec, and a step tracker.
- **When**: the conformance test and implementation-step tracker run.
- **Then**: the plan is structurally valid and only its implementation entries
  control the implementation gate.

### Scenario 2: Profile drift is detected

- **Given**: a fixture missing a required metadata subsection or containing a
  lowercase implementation marker.
- **When**: validation runs.
- **Then**: the missing subsection is rejected and the lowercase marker remains
  pending.

## Error / Edge Cases

- A Python plan that omits `Async-planning status` is needs-rework.
- A missing `Handoff / Gate Notes` section is invalid for a Python step file.
- Pending lifecycle stages outside `Implementation Steps` do not block an
  implementation-only completion query.
