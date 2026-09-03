# Plan Reviewer Reference

Use this file to keep repo-visible topic-plan review aligned with the repository workflow.

## Review basis

Review topic plans against the shared contract sources together:

1. `plan/agent-handoff-workflow.md`
2. `plan/topic-plan-contract.md`
3. this skill's local `reference.md`, `checklist.md`, and `examples.md`

Do not treat any one source as sufficient by itself. The workflow defines the canonical execution contract, `plan/topic-plan-contract.md` defines the canonical topic-plan section and fallback contract, and this skill's local materials define review heuristics and common failure signals.

When a topic uses correction / delta artifacts, also verify that the plan keeps the workflow body slim, lists exact parent/correction paths, makes parent-sync closure explicit, keeps review-log usage conditional on routing-controlling feedback, and leaves the minimum correction artifact contract in reference / examples instead of the workflow body.

## Correction-review input allowlist

For a declared correction route, review only the exact repo-visible inputs named by that route:
the target plan, its required step tracker, its declared parent/correction artifacts, the shared
workflow and topic-plan contracts, and recorded Copilot feedback explicitly attached to those
artifacts. The Plan-Reviewer may write only the declared correction-plan verdict. Chat, branch,
summary, `GOAL.md`, legacy `.github/agents/**`, and superseded normal/recovery evidence are never
review inputs or routing authority.

The correction-artifact extension is conditional, not a universal plan requirement. When a route
declares it, the complete set is: correction plan, correction step, correction-plan review log,
Tester evidence, and implementation-review log. Their exact paths, write owners, ordering, and
schema authority must be declared. The correction-plan review log is the pre-implementation gate;
Tester evidence attests the immutable subject before independent implementation review.

If the topic is a correction-lifecycle contract refresh, verify that it refreshes existing workflow / plan surfaces now and does not create a standalone correction skill unless a separate topic explicitly justifies extraction because repeated instability or cross-workflow reuse has been demonstrated.

## What counts as blocking

Treat these as blocking issues:

- missing required sections
- invalid or non-canonical transitions
- skipping the independent Tester phase or allowing `publish-in-progress` -> `merged`
- vague or drifting `Artifact Paths`
- undeclared or mixed stable-library intent
- non-JSON reviewer handoff
- wrong post-merge or release timing
- mixed role ownership
- placeholders where the workflow needs an explicit contract
- vague correction evidence paths such as `merged implementation`
- missing parent-sync closure logic when correction artifacts are used
- reviewer-owned logging or verdict work inside creator `Implementation Steps`
- workflow-body bloat that turns the plan into a field-by-field correction schema
- unconditional review-log requirements when routing control or multi-round rework is absent
- turning a sample round cap into a repository-wide invariant
- a correction-lifecycle refresh topic that quietly broadens into standalone-skill creation without separate justification
- correction review that accepts an undeclared input or treats chat, branch, summary, `GOAL.md`,
  `.github/agents/**`, or superseded evidence as authority

Do not raise blocking issues for tone, phrasing, or layout preferences that do not change contract meaning.

## Workflow position

`plan-reviewer` runs after a repo-visible topic plan exists and before later execution begins under `plan/agent-handoff-workflow.md`.

Typical operating sequence:

1. `plan-creator` authors `plan/<topic>/<topic>.plan.md`
2. Main Agent routes the plan to an independent reviewer through a separate
   reviewer path
3. required fixes are applied
4. only then does branch preparation or later execution continue

This skill is a planning-contract gate. It does not replace the existing implementation-review step in Phase 4, and it does not create a new numbered phase by itself.

## Output rule

Return exactly one JSON object with:

- `verdict`
- `blocking_issues`
- `copilot_feedback_triage`
  - `ADDRESS`
  - `DISCUSS`
  - `SKIP`

Keep all reasoning inside structured fields. Do not append prose before or after the JSON object.

## Committed candidate and correction-record rule

A correction route may use an extended correction-review JSON record instead of the normal generic
plan-review verdict. Its route declaration is the schema authority. The record retains verdict,
blockers, and Copilot triage, and records only post-commit candidate identity: candidate id,
committed revision/tree, every declared planning path/blob, first-parent/non-merge admission, and
review basis.

`approved` may name exactly one active candidate and a next phase, but takes routing effect only
after the unchanged record itself is committed. `needs-rework` is a blocker: it must name no active
candidate, next phase, implementation subject, close authorization, or self-closing transition.
Planner may select only a committed explicit approved candidate record; it must not infer from an
author worktree or direct Plan-Creator to refine, select, or close a candidate.

An actual-Q gate may write a separately declared evidence-only active-candidate close record only
after it verifies committed T/V evidence blobs semantically refer to the same immutable subject,
Tester says that subject passed, and Reviewer says that subject is approved. The record authorizes
only post-Q thread classification; it never authorizes Human PR approval, merge, release, or
post-merge work. `Reviewer` here is the independent implementation verifier, not a Human reviewer.

## B6R10 deterministic evidence invariants

B6R10 remains a single current route with B6R9/Q15 frozen. Review its R20 baseline without
precommitting B6R10/R20 commit, tree, blob, or outcome facts. The route must declare these exact,
fail-closed later evidence objects (and no alternative Markdown/front-matter representation):

- T16 top-level keys are exactly `schema_version`, `correction_id`, `phase`, `subject`, `test_run`,
  and `timestamp`. `subject` has exactly `phase`, `commit_sha`, `test_path`, where phase is `S16`
  and SHA is 40 lowercase hexadecimal characters. `test_run` has exactly `command`, `status`,
  `exit_code`, with `passing` and `0` required.
- V16 top-level keys are exactly `schema_version`, `correction_id`, `phase`, `subject`,
  `tester_evidence`, `verdict`, `blocking_issues`, and `timestamp`. It must bind the same S16
  subject and committed T16 commit/path/blob/subject/status; all commit/blob values are 40 lowercase
  hexadecimal characters, verdict is `APPROVED`, and blockers is `[]`.
- Q16 top-level keys are exactly `schema_version`, `correction_id`, `phase`, `artifacts`,
  `parsed_claims`, `actual_git`, `close_authorization`, and `timestamp`. Its artifacts bind each
  committed S16/T16/V16 commit/parent/path/blob; claims bind the same S16 and T16 `passing`/V16
  `APPROVED`; actual Git binds the explicit triple, linear result, `S16..V16` range and name-status.
  `close_authorization` is exactly classification-only `ACTIVE_CANDIDATE_CLOSED`; it forbids thread
  resolution, Human review, merge, release, and post-merge. Q16 contains no self commit/tree/blob.

Any missing, extra, malformed, abbreviated, non-hex, or semantically inconsistent field is a
blocking fail-closed result. Reviewer may write Q16 only after V16 is committed; its record becomes
active only when an independent Implementer commits it unchanged as the sole evidence-only path.
