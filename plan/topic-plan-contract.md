# Topic Plan Contract

## Current correction contract

`B6R13 -> R23 -> S17 -> T17 -> V17 -> Q17 -> thread-classification -> comment-resolve -> human-check` 是唯一 current
contract；current state 是 `R23_REVIEW_PENDING`。B6R13/R23 are non-subject；S17 alone modifies the declared
exact-fourteen runtime/template/test allowlist and retains direct imports。T17/V17 是唯一 S17 evidence descendants；Q17
是 committed V17 後的 evidence-only actual full-triple gate。B6R12/R22/S16-Q16、B6R10/R20 and earlier are frozen
predecessor provenance.

## Authority and required plan structure

Authority ordering 是 AGENTS.md、plan/agent-handoff-workflow.md、本文件、parent plan、parent step、current exact
review record、local planning skill。GOAL.md 是 project mission，不是 topic/phase authority；chat、branch、summary
與 .github/agents/** 不可補推 planning evidence，後者只作 frozen provenance。

每個 topic plan 必須依 canonical order 包含 Goal / Outcome、Scope、Locked Decisions、Boundaries / Exclusions、
Status / Allowed Transitions、Artifact Paths、Implementation Steps、Validation / Acceptance Checks、Reviewer Handoff、
Post-merge / release actions、Open Questions / Unresolved Items。Artifact Paths 是 executable contract：每個 path
都要有 exact path、write owner、decision authority 與 role；unlisted path 必須停止並返回 Planner。

## Planner preflight and boundaries

Planner bootstraps once, then reads only parent plan, parent step and committed approved R23. It selects candidate, phase,
gate and one non-Planner next role; missing evidence is blocked, candidate conflict is human-check, and only Planner routes
bounded rework. Planning approval never establishes execution approval. This contract grants no direct thread resolution,
merge, release, post-merge, tag or summary.

## Frozen B6R10 current-candidate contract

B6R10 admission is a non-merge, first-parent exact-eleven baseline: `AGENTS.md`, the three declared plan-reviewer
skill files, shared workflow/contract, parent plan/spec/step, and B6R10 plan/step. Pre-admission artifacts contain no
B6R10/R20 SHA, tree, blob, HEAD, or review outcome. R20 is the declared extended JSON correction record, not the
generic three-field verdict. It records candidate id, committed revision/tree, all eleven path/blob entries,
first-parent admission, review basis, verdict, blockers and Copilot triage. `needs-rework` has no active candidate,
next phase, subject or close authorization. Only a separately committed approved R20 has exactly one active candidate,
`R20_COMPLETE_S16_NEXT`, and next phase S16. Planner selects only that record and never asks Plan-Creator to refine,
select, or self-close.

Frozen B6R10 S16 was the sole non-merge test subject and preserved direct imports; `importlib`, `__import__`, and `sys.modules`
substitution is forbidden. It verifies committed T16/V16 blob semantics: topology/path, one identical full S16 SHA,
T16 `passing`, and V16 `APPROVED`. Q16 is a post-V16, actual full-triple, read-only Git gate which may write only
`plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r10-actual-gate-evidence.md` as an
evidence-only active-candidate close record. That record authorizes classification only, never PR approval or merge.
Reviewer is an implementation verifier; Human alone performs PR review and merge.

## Frozen B6R10 deterministic evidence contract

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

## B6R13 current-candidate contract

B6R13 admission is non-merge, first-parent, exact-eight: `AGENTS.md`, shared workflow/contract, parent plan/spec/step,
and B6R13 plan/step. Pre-admission B6R13/R23 commit, tree, blob, HEAD and outcome facts are prohibited. R23 is the
declared extended correction receipt, recording one candidate's committed revision/tree, all eight path/blob facts,
first-parent admission, predecessor receipt, review basis, Copilot triage, verdict and blockers. `needs-rework` has no
active candidate, next phase, subject or close authorization. Only separately committed unchanged approved R23 establishes
the one active candidate, `R23_COMPLETE_S17_NEXT`, and next phase S17.

S17 is the sole non-merge subject and only changes its exact fourteen allowlisted wrapper, skill/template and governance
test paths named in the shared workflow. It retains direct imports and forbids `importlib`, `__import__`, and `sys.modules`
substitution. Planner bootstraps once and cannot select Planner as a later next role; Plan-Creator is the only planning
writer; Tester factual evidence includes actual exit code; Reviewer consumes same-subject passing Tester evidence;
Explorer is read-only. Implementer is bounded and may never merge. T17/V17/Q17 use only new B6R13 evidence paths; Q17
actual full triple permits classification only. A later independent classification, not Q17, may permit an Implementer
to respond to and resolve one explicit addressed-and-resolvable thread.

## B6R13 deterministic evidence contract

T17/V17/Q17 are single JSON objects whose exact key sets, nested key sets, paths, 40-character lowercase SHA values,
enums, parents and same-subject references fail closed. T17 records S17, actual command, actual exit code and factual
result. V17 binds committed T17 path/blob and S17, with `APPROVED` and empty blockers. Q17 binds committed S17/T17/V17
commit/parent/path/blob facts and actual explicit full triple/linear/range/name-status, has no Q17 self commit/tree/blob,
and after an unchanged independent Implementer evidence-only commit authorizes only `ACTIVE_CANDIDATE_CLOSED` with
classification permitted. It never directly authorizes comment resolution, Human review, merge, release or post-merge.

## Frozen provenance

normal/recovery records and all B0–B6R9 / R1–R19 / S1–S15 / T1–T15 / V1–V15 / Q1–Q15 artifacts are frozen
nonrouting predecessor provenance. They have no current routing, gate, next-phase, subject, candidate-selection or
Planner authority. Q14's sole failure is raw `git diff --name-status` lexical ordering; it is frozen provenance, not
an instruction for S16. step-creator remains deferred.
