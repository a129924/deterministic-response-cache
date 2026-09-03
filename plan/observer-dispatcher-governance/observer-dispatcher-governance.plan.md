# Observer / Dispatcher Governance

## Goal / Outcome

以 B6R10 correction baseline 收斂 governance conformance route，建立可獨立驗證的
B6R10 -> R20 -> S16 -> T16 -> V16 -> Q16 -> thread-classification/human-check。本 topic 是 non-stable、
review-ready-only work；停在 Human boundary。

## Scope

- **In Scope:** B6R10 exact-eleven planning baseline、R20 extended plan review、S16 single test-path correction、T16/V16
  evidence、Q16 evidence-only actual Git close record，以及 passed Q16 後的 independent per-thread classification。
- **Out Of Scope:** B6R9/Q15 與所有其他 frozen provenance、legacy migration、step-creator activation、產品/
  architecture work、unlisted paths、thread resolve、merge、release、post-merge。

## B6R10 Current Contract

Only an unchanged, separately committed R20 record with `verdict: approved`, one explicit active candidate, and
`next_phase: S16` routes work. `needs-rework` is a blocker only. Planner selects that committed evidence and does not
direct Plan-Creator to refine/select/self-close. S16 preserves direct imports and only changes
`tests/test_observer_dispatcher_governance_contract.py` to validate committed T16/V16 blob semantics: correct topology
and paths, same full S16 SHA, T16 `passing`, V16 `APPROVED`. Q16 writes only the declared B6R10 actual-gate evidence
close record after actual full-triple validation; it authorizes thread classification, not merge. Reviewer is not Human.

## B6R10 Deterministic Evidence Contract

T16 is one JSON object with exactly `schema_version`, `correction_id`, `phase`, `subject`, `test_run`, `timestamp`.
`subject` is exactly `phase:S16`, a 40-character lowercase hexadecimal `commit_sha`, and the one S16 `test_path`;
`test_run` is exactly `command`, `status:passing`, `exit_code:0`. V16 is one JSON object with exactly
`schema_version`, `correction_id`, `phase`, `subject`, `tester_evidence`, `verdict`, `blocking_issues`, `timestamp`;
it binds same-S16 plus committed T16 commit/path/blob/subject/status, requires uppercase `APPROVED` and `[]` blockers.

Q16 is one JSON object with exactly `schema_version`, `correction_id`, `phase`, `artifacts`, `parsed_claims`,
`actual_git`, `close_authorization`, `timestamp`. It binds committed S16/T16/V16 commit/parent/path/blob facts,
same-S16/`passing`/`APPROVED` parsed claims, and actual full Git triple/linear/`S16..V16`/name-status. Q16 may be
written only after committed V16 and has no self commit/tree/blob; it becomes active only when an independent
Implementer commits it unchanged as the sole evidence-only path. Its authorization is
`ACTIVE_CANDIDATE_CLOSED` classification permitted only: resolve threads, Human review, merge, release, post-merge
are forbidden. All missing, extra, malformed, abbreviated, non-hex, or inconsistent values fail closed.

## Locked Decisions

- 唯一 current correction 是 `observer-dispatcher-governance/high/b6r10`；current state 是
  `R20_REVIEW_PENDING`。`B6R10 -> R20 -> S16 -> T16 -> V16 -> Q16 -> thread-classification -> human-check`
  是唯一 current route。
- B6R9/R19/S15/T15/V15/Q15 僅為 immutable frozen predecessor provenance：不得作 routing、subject、gate 或
  thread authority；舊 plan/spec/step/evidence 不得改寫、恢復或補推 current state。
- B6R10 admission 是 non-merge first-parent exact-eleven；pre-admission artifacts 不含 B6R10/R20 commit、tree、
  blob、HEAD 或 review outcome。R20 只在 committed B6R10 clean checkout 記錄該等 post-commit facts。
- 只有 unchanged、separately committed 且 `verdict: approved` 的 R20，並具有一個 explicit active candidate 和
  `next_phase: S16`，才可 route。`needs-rework` 是 blocker，沒有 active candidate、next phase、subject 或 close
  authorization。
- B6R10/R20 均是 non-subject；S16 是唯一 implementation subject，完整 diff 僅可修改
  `tests/test_observer_dispatcher_governance_contract.py`。direct imports 必須保留；禁止
  `importlib`、`__import__`、`sys.modules` substitution。
- S16 只驗證 committed T16/V16 evidence blobs 的 topology/path、同一 full S16 SHA、T16 `passing` 與 V16
  `APPROVED`。Q16 僅在 committed V16 後以 actual full triple 寫 declared evidence-only active-candidate close
  record；它只授權 classification，絕不授權 PR approval 或 merge。

## Boundaries / Exclusions

Observer 只 dispatch/aggregate。Planner 單獨決定 candidate、phase、gate 與 next role。Plan-Creator 只寫 declared
planning paths，不能 refine、select 或 self-close candidate；Plan-Reviewer 只寫 R20；Implementer 只做 approved
bounded commits；Tester/Reviewer 只寫 declared evidence。Reviewer 是 independent implementation verifier，不是
Human PR reviewer。任何 actor 不得 widen allowlist、處理或 resolve threads、merge、release 或 post-merge。

## Status / Allowed Transitions

**Current:** `R20_REVIEW_PENDING`。

唯一 transition 是 `B6R10 -> R20 -> S16 -> T16 -> V16 -> Q16 -> thread-classification -> human-check`。R20 必須
clean-checkout-review committed B6R10、eleven blobs/admission；approved R20 原樣另行提交後才可 S16，並以
`R20_COMPLETE_S16_NEXT` 作 effective committed state。S16 需要 R20 approval；T16 需要 same-S16 full-suite result；
V16 需要 passing T16；Q16 需要 committed V16。failure 回 Planner；merge/release 停在 Human boundary。

## Artifact Paths

| Artifact | Exact path | Write owner | Decision authority | Role |
| --- | --- | --- | --- | --- |
| Governance guidance | AGENTS.md | Plan-Creator | Planner | B6R10 contract |
| Reviewer skill | .agents/skills/plan-reviewer/SKILL.md | Plan-Creator | Planner | B6R10 contract |
| Reviewer checklist | .agents/skills/plan-reviewer/checklist.md | Plan-Creator | Planner | B6R10 contract |
| Reviewer reference | .agents/skills/plan-reviewer/reference.md | Plan-Creator | Planner | B6R10 contract |
| Shared workflow | plan/agent-handoff-workflow.md | Plan-Creator | Planner | B6R10 contract |
| Shared contract | plan/topic-plan-contract.md | Plan-Creator | Planner | B6R10 contract |
| Parent plan | plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md | Plan-Creator | Planner | Current truth |
| Parent spec | plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md | Plan-Creator | Planner | Acceptance |
| Parent step | plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md | Plan-Creator | Planner | Tracker |
| B6R10 plan | plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r10-plan.md | Plan-Creator | Planner | Baseline delta |
| B6R10 step | plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r10-step.md | Plan-Creator | Planner | Baseline tracker |
| R20 review | plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r10-review-log.md | Plan-Reviewer | Plan-Reviewer verdict | Pre-S16 gate |
| S16 subject | tests/test_observer_dispatcher_governance_contract.py | Implementer | Planner | Sole implementation subject |
| T16 evidence | plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r10-tester-evidence.md | Tester | Factual test result | First descendant |
| V16 evidence | plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r10-implementation-review-log.md | Reviewer | Reviewer verdict | Final descendant |
| Q16 evidence | plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r10-actual-gate-evidence.md | Reviewer | Actual-gate result | Classification gate |

README.md、VERSION、.github/copilot-instructions.md 與 .github/agents/** are ReadOnly. No path is Deleted. Only
the eleven B6R10 planning paths are Written/Modified at admission; all other paths are excluded.

## Implementation Steps

1. Plan-Creator prepares exactly the B6R10 eleven planning paths; Independent Implementer commits their exact
   non-merge first-parent admission.
2. Independent Plan-Reviewer clean-checkout-reviews committed B6R10, its tree and all eleven blobs/admission, then
   writes R20. Independent Implementer separately commits approved R20 unchanged; its effective committed state is
   `R20_COMPLETE_S16_NEXT` and next phase is S16.
3. Planner verifies R20 and dispatches S16, whose only change is the declared test-path correction while retaining
   direct imports and fail-closed actual input.
4. Tester writes T16 after the full suite. Reviewer writes V16 after passing T16 and validates exact topology/path and
   committed evidence semantics.
5. Reviewer executes Q16 only after V16 commit and writes only its declared close record; an independent Reviewer may
   then classify each thread. Stop at
   human-check.

## Validation / Acceptance Checks

- B6R10 admission is non-merge, first-parent, exact-eleven; R20 captures reviewed commit, tree, every declared blob,
  first-parent admission, Copilot triage, verdict and blockers.
- B6R10/R20 do not establish a subject; S16 is the sole test-path subject and direct imports remain direct.
- S16 requires committed T16/V16 blobs with exact topology/path, same full S16 SHA, T16 `passing`, and V16 `APPROVED`.
- Q16 uses committed full actual triple and real subprocess Git, writes only its declared evidence-only close record,
  and never authorizes resolution, PR approval, or merge; its exact JSON schema checks all committed artifacts,
  parsed claims, actual Git facts and the classification-only close authorization.

## Reviewer Handoff

~~~json
{"current_route":"B6R10->R20->S16->T16->V16->Q16","correction_id":"observer-dispatcher-governance/high/b6r10","plan_review_path":"plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r10-review-log.md","implementation_subject":"S16 only","range":"S16..V16","verdict":"approved|needs-rework"}
~~~

## Post-merge / release actions

No release action is authorized. Stop at the Human boundary.

## Open Questions / Unresolved Items

step-creator remains deferred and has no effect on this route. B6R9/Q15 and all earlier records are frozen
predecessor provenance; no old failure creates a current route or repair obligation.
