# Topic Plan Contract

## Current correction contract

B6R10 -> R20 -> S16 -> T16 -> V16 -> Q16 是唯一 current contract；current state 是 R20_REVIEW_PENDING。
B6R10/R20 are non-subject；S16 alone modifies tests/test_observer_dispatcher_governance_contract.py and retains
direct imports。T16/V16 是唯一 S16..V16 evidence descendants；Q16 是 committed V16 後的 evidence-only actual
full-triple gate。B6R9/Q15 是 frozen predecessor provenance。

## Authority and required plan structure

Authority ordering 是 AGENTS.md、plan/agent-handoff-workflow.md、本文件、parent plan、parent step、current exact
review record、local planning skill。GOAL.md 是 project mission，不是 topic/phase authority；chat、branch、summary
與 .github/agents/** 不可補推 planning evidence，後者只作 frozen provenance。

每個 topic plan 必須依 canonical order 包含 Goal / Outcome、Scope、Locked Decisions、Boundaries / Exclusions、
Status / Allowed Transitions、Artifact Paths、Implementation Steps、Validation / Acceptance Checks、Reviewer Handoff、
Post-merge / release actions、Open Questions / Unresolved Items。Artifact Paths 是 executable contract：每個 path
都要有 exact path、write owner、decision authority 與 role；unlisted path 必須停止並返回 Planner。

## Planner preflight and boundaries

Planner reads only parent plan, parent step and committed approved R20. It selects candidate, phase, gate and next role;
missing evidence is blocked, candidate conflict is human-check, and only Planner routes bounded rework. Planning approval
never establishes execution approval. This contract grants no thread resolution, merge, release, post-merge, tag or summary.

## B6R10 current-candidate contract

B6R10 admission is a non-merge, first-parent exact-eleven baseline: `AGENTS.md`, the three declared plan-reviewer
skill files, shared workflow/contract, parent plan/spec/step, and B6R10 plan/step. Pre-admission artifacts contain no
B6R10/R20 SHA, tree, blob, HEAD, or review outcome. R20 is the declared extended JSON correction record, not the
generic three-field verdict. It records candidate id, committed revision/tree, all eleven path/blob entries,
first-parent admission, review basis, verdict, blockers and Copilot triage. `needs-rework` has no active candidate,
next phase, subject or close authorization. Only a separately committed approved R20 has exactly one active candidate,
`R20_COMPLETE_S16_NEXT`, and next phase S16. Planner selects only that record and never asks Plan-Creator to refine,
select, or self-close.

S16 is the sole non-merge test subject and preserves direct imports; `importlib`, `__import__`, and `sys.modules`
substitution is forbidden. It verifies committed T16/V16 blob semantics: topology/path, one identical full S16 SHA,
T16 `passing`, and V16 `APPROVED`. Q16 is a post-V16, actual full-triple, read-only Git gate which may write only
`plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r10-actual-gate-evidence.md` as an
evidence-only active-candidate close record. That record authorizes classification only, never PR approval or merge.
Reviewer is an implementation verifier; Human alone performs PR review and merge.

## B6R10 deterministic evidence contract

T16/V16/Q16 must each be a single JSON object. Exact key sets, nested key sets, exact paths, 40-character lowercase
hexadecimal SHA values, enum case, parent relationships, and cross-evidence subject identity are mandatory; an omitted,
extra, malformed, abbreviated, non-hex, or inconsistent value fails closed. T16 has exactly
`schema_version`, `correction_id`, `phase`, `subject`, `test_run`, `timestamp`; subject has exactly
`phase:S16`, `commit_sha`, `test_path`, while test_run has exactly `command`, `status:passing`, `exit_code:0`.

V16 has exactly `schema_version`, `correction_id`, `phase`, `subject`, `tester_evidence`, `verdict`,
`blocking_issues`, `timestamp`. It binds S16 plus committed T16 `commit_sha`, `path`, `blob_sha`, subject and
`status:passing`; it requires `verdict:APPROVED` and `blocking_issues:[]`. Q16 has exactly `schema_version`,
`correction_id`, `phase`, `artifacts`, `parsed_claims`, `actual_git`, `close_authorization`, `timestamp`. Its S16/T16/V16
artifact entries bind committed commit/parent/path/blob facts; its parsed claims bind the same S16, `passing`, and
`APPROVED`; its actual Git record binds the full explicit triple, linear status, `S16..V16`, and name-status. Q16 has
no self commit/tree/blob field, may be written only after V16 is committed, and becomes active only after an independent
Implementer commits the unchanged record as the sole evidence-only path. Its authorization is only
`ACTIVE_CANDIDATE_CLOSED` with classification permitted; thread resolve, Human review, merge, release, and post-merge
are forbidden.

## Frozen provenance

normal/recovery records and all B0–B6R9 / R1–R19 / S1–S15 / T1–T15 / V1–V15 / Q1–Q15 artifacts are frozen
nonrouting predecessor provenance. They have no current routing, gate, next-phase, subject, candidate-selection or
Planner authority. Q14's sole failure is raw `git diff --name-status` lexical ordering; it is frozen provenance, not
an instruction for S16. step-creator remains deferred.
