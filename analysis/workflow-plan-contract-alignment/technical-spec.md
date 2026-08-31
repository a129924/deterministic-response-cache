# Workflow plan-contract alignment — Technical Specification

## Canonical Python topic-plan profile

`plan/<topic>/<topic>.plan.md` remains the only execution-facing plan. It must
keep the repository's eleven canonical top-level sections. A Python topic adds
one top-level `## Python implementation metadata` section immediately after
`## Artifact Paths`, with these subsections:

1. `Non-goals`
2. `Current Context`
3. `Requirements`
4. `Decisions`
5. `Public Contract / API Changes`
6. `Affected Files / Modules`
7. `Test Plan`
8. `Risks`
9. `Rollback Plan`

`Decisions` carries the explicit async status, the seven normal Python
decisions, and the existing conditional async subsections. The canonical
`Goal / Outcome`, `Implementation Steps`, `Validation / Acceptance Checks`,
and `Open Questions / Unresolved Items` supply the corresponding shared plan
information.

## Step profile

Python step files must contain, in order, `Workflow Stages`, `Actionable
Steps`, `Implementation Steps`, `Main Agent Actionable Steps — Fixed Tail`, and
`Handoff / Gate Notes`. Only `Implementation Steps` controls the
implementation-completion gate.

## Consumer updates

The Python authoring, specialised plan review, RED-test authoring,
implementation review, step renderer, tracker references, and wrapper workflow
must name this profile and use `.agents/skills/...` as the real local path.
The general `plan-creator` and `plan-reviewer` remain the authority for the
canonical topic-plan and final JSON review handoff.

## Fixture contract

Store one complete non-product Python-topic fixture under
`tests/fixtures/python-topic-plan-contract/`. A pytest test must validate its
canonical headings, metadata subsections, async exemption citation, spec
headings, and step layout. It must also prove that the repository's
`plan-step-tracker` recognises only pending implementation steps as the
implementation gate.
