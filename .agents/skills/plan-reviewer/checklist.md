# Plan Reviewer Checklist

Use this checklist when reviewing a repo-visible topic plan before later execution begins.

- [ ] The plan path is `plan/<topic>/<topic>.plan.md`.
- [ ] The review uses the shared contract sources:
  - [ ] `plan/agent-handoff-workflow.md`
  - [ ] `plan/topic-plan-contract.md`
  - [ ] local `reference.md`
  - [ ] local `checklist.md`
- [ ] All workflow-required plan sections are present, using the canonical section list from `plan/topic-plan-contract.md`:
  - [ ] `Goal / Outcome`
  - [ ] `Scope`
  - [ ] `Locked Decisions`
  - [ ] `Boundaries / Exclusions`
  - [ ] `Status / Allowed Transitions`
  - [ ] `Artifact Paths`
  - [ ] `Implementation Steps`
  - [ ] `Validation / Acceptance Checks`
  - [ ] `Reviewer Handoff`
  - [ ] `Post-merge / release actions`
  - [ ] `Open Questions / Unresolved Items`
- [ ] `Status / Allowed Transitions` uses canonical workflow transitions only: independent Tester
  precedes reviewer work, `publish-in-progress` only reaches `pr-open`, and Human alone may merge
  from `pr-open`.
- [ ] The current status matches the actual topic state.
- [ ] `Artifact Paths` are exact, bounded, repo-visible, and role-labeled.
- [ ] If correction artifacts are used, each parent artifact, correction artifact, and any routing-controlling review-log / equivalent handoff artifact is listed explicitly.
- [ ] If correction artifacts are used, review inputs are limited to that route's declared
  allowlist; chat, branch, summary, `GOAL.md`, and `.github/agents/**` are excluded.
- [ ] The conditional correction extension lists correction plan, correction step,
  correction-plan review log, Tester evidence, and implementation-review log with exact
  path/owner/order/schema authority.
- [ ] Correction topics keep parent artifacts as current truth after backfill and correction artifacts as historical truth.
- [ ] When correction artifacts are used, the minimum correction artifact contract lives in reference / examples, not as a workflow-body schema dump.
- [ ] `Implementation Steps` remain creator-owned; reviewer verdict logging, reviewer acceptance tasks, and main-agent routing work are not mixed into them.
- [ ] Correction guidance in the workflow body stays slim; detailed correction artifact schema or long samples are not embedded as workflow-body bloat.
- [ ] Parent-sync closure requirements are explicit when correction artifacts are used.
- [ ] `review-log` requirements are conditional and not universalized.
- [ ] Any round cap is clearly topic-specific policy, not a repository-wide invariant.
- [ ] Correction-lifecycle refresh topics do not broaden into a standalone correction skill unless a separately scoped topic explicitly justifies extraction via repeated instability or cross-workflow reuse.
- [ ] Stable-library intent is explicit:
  - [ ] clearly absent for non-stable topics, or
  - [ ] declared with `Stable library metadata` when stable surfaces are involved.
- [ ] `Reviewer Handoff` is one machine-consumable JSON object.
- [ ] A declared correction route names one extended correction-review JSON schema; the reviewer does not reduce it to the normal generic three-field verdict.
- [ ] The correction record contains only post-commit candidate facts (commit, tree, declared blobs and first-parent admission).
- [ ] `needs-rework` names no active candidate, next phase, implementation subject, close record, or self-closing action.
- [ ] Only a separately committed approved correction record can establish the one active candidate and its next phase.
- [ ] Planner routing selects only that committed explicit candidate evidence and never directs Plan-Creator to refine, select, or close a candidate.
- [ ] For B6R10, T16's declared JSON object has exactly `schema_version`, `correction_id`, `phase`,
  `subject`, `test_run`, and `timestamp`; its S16 SHA is exactly 40 lowercase hexadecimal characters and
  its test run is `passing` with exit code `0`.
- [ ] For B6R10, V16's declared JSON object has exactly `schema_version`, `correction_id`, `phase`,
  `subject`, `tester_evidence`, `verdict`, `blocking_issues`, and `timestamp`; it binds S16 and committed
  T16 commit/path/blob/subject/status, has verdict `APPROVED`, and has `blocking_issues: []`.
- [ ] For B6R10, Q16 is declared only after committed V16. Its exact schema binds committed S16/T16/V16
  commit/parent/path/blob facts, parsed same-S16/passing/APPROVED claims, actual Git triple/linear/range/name-status,
  and only `ACTIVE_CANDIDATE_CLOSED` classification permission. It has no Q16 self commit/tree/blob field.
- [ ] For B6R10, missing, extra, malformed, abbreviated, non-hex, or inconsistent schema data fails closed;
  an independent Implementer commits the Reviewer-authored Q16 record unchanged before it becomes active.
- [ ] `Reviewer` is checked as independent implementation verification, not as a Human PR reviewer; Human-only PR review and merge authority remain distinct.
- [ ] `Post-merge / release actions` match the actual scope and timing.
- [ ] Planning actor, creator, reviewer, and Main Agent responsibilities are not mixed.
- [ ] No unsafe placeholders such as `TBD`, `later`, or `follow normal process` remain where the workflow needs an explicit contract.
- [ ] The final output is exactly one JSON verdict object with no trailing prose.
