# Observer / Dispatcher Governance

## Goal / Outcome

以 B6R9 correction baseline 收斂 governance conformance route，建立可獨立驗證的
B6R9 -> R19 -> S15 -> T15 -> V15 -> Q15 -> thread-classification/human-check。本 topic 是 non-stable、
review-ready-only work；停在 Human boundary。

## Scope

- **In Scope:** B6R9 exact-seven planning baseline、R19 plan review、S15 single test-path correction、T15/V15
  evidence、Q15 read-only actual Git gate，以及 passed Q15 後的 independent per-thread classification。
- **Out Of Scope:** B6R8/Q14 與所有其他 frozen provenance、legacy migration、step-creator activation、產品/
  architecture work、unlisted paths、thread resolve、merge、release、post-merge。

## Locked Decisions

- Current correction 是 observer-dispatcher-governance/high/b6r9；current state 是 R19_REVIEW_PENDING；
  B6R9/R19 是 non-subject，S15 是唯一 subject。
- B6R9 admission 是 non-merge first-parent exact-seven；pre-admission artifacts 不含 B6R9/R19 revision、tree、
  blob、HEAD 或 review outcome。R19 記錄 committed B6R9 的 seven blobs/tree/admission，approved committed R19
  的 effective state 是 R19_COMPLETE_S15_NEXT。
- S15 complete diff 只改 tests/test_observer_dispatcher_governance_contract.py；direct imports 是 mandatory，
  禁止 importlib/__import__/sys.modules substitution。唯一修正是 raw name-status expected tuples 的 lexical
  path order：B6R9 implementation review-log 必須位於 tester-evidence 前。
- T15/V15 是唯一 linear non-merge S15 descendants；named S15..V15 range 只含兩個 B6R9 evidence paths，並以
  review-log、tester-evidence 的 lexical tuple 順序比較。Q15 是 post-V15、read-only、no artifact/no thread
  authority。
- Actual input 只接受完整 explicit ODG_S15_SHA/ODG_T15_SHA/ODG_V15_SHA 與 real subprocess Git；all-absent 為
  skip/unverified，partial/invalid/symbolic/nonexistent/merge/wrong graph/range 一律 fail closed。

## Boundaries / Exclusions

Observer 只 dispatch/aggregate。Planner 單獨決定 phase/gate/role。Plan-Creator 寫 declared planning paths；
Plan-Reviewer 寫 R19；Implementer 做 approved bounded commits；Tester/Reviewer 只寫 declared evidence。任何 actor
不得 widen allowlist、resolve threads、merge、release 或 post-merge。

## Status / Allowed Transitions

**Current:** R19_REVIEW_PENDING。

唯一 transition 是 B6R9 -> R19 -> S15 -> T15 -> V15 -> Q15 -> thread-classification/human-check。R19 必須
clean-checkout-review committed B6R9、seven blobs/admission；approved R19 原樣另行提交後才可 S15，並以
R19_COMPLETE_S15_NEXT 作 effective committed state。S15 需要 R19 approval；T15 需要 same-S15 full-suite result；
V15 需要 passing T15；Q15 需要 committed V15。failure 回 Planner；merge/release 停在 Human boundary。

## Artifact Paths

| Artifact | Exact path | Write owner | Decision authority | Role |
| --- | --- | --- | --- | --- |
| Shared workflow | plan/agent-handoff-workflow.md | Plan-Creator | Planner | B6R9 contract |
| Shared contract | plan/topic-plan-contract.md | Plan-Creator | Planner | B6R9 contract |
| Parent plan | plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md | Plan-Creator | Planner | Current truth |
| Parent spec | plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md | Plan-Creator | Planner | Acceptance |
| Parent step | plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md | Plan-Creator | Planner | Tracker |
| B6R9 plan | plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r9-plan.md | Plan-Creator | Planner | Baseline delta |
| B6R9 step | plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r9-step.md | Plan-Creator | Planner | Baseline tracker |
| R19 review | plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r9-review-log.md | Plan-Reviewer | Plan-Reviewer verdict | Pre-S15 gate |
| S15 subject | tests/test_observer_dispatcher_governance_contract.py | Implementer | Planner | Sole implementation subject |
| T15 evidence | plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r9-tester-evidence.md | Tester | Factual test result | First descendant |
| V15 evidence | plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r9-implementation-review-log.md | Reviewer | Reviewer verdict | Final descendant |

README.md、VERSION、.github/copilot-instructions.md 與 .github/agents/** are ReadOnly. No path is Deleted. Only
the seven B6R9 planning paths are Written/Modified at admission; all other paths are excluded.

## Implementation Steps

1. Plan-Creator prepares exactly the B6R9 seven planning paths; Independent Implementer commits their exact
   non-merge first-parent admission.
2. Independent Plan-Reviewer clean-checkout-reviews committed B6R9, its tree and all seven blobs/admission, then
   writes R19. Independent Implementer separately commits approved R19 unchanged; its effective committed state is
   R19_COMPLETE_S15_NEXT and next phase is S15.
3. Planner verifies R19 and dispatches S15, whose only change corrects expected raw name-status tuple lexical order
   to review-log before tester-evidence while retaining direct imports and fail-closed actual input.
4. Tester writes T15 after the full suite. Reviewer writes V15 after passing T15 and validates the exact range.
5. Reviewer executes Q15 only after V15 commit; an independent Reviewer may then classify each thread. Stop at
   human-check.

## Validation / Acceptance Checks

- B6R9 admission is non-merge, first-parent, exact-seven; R19 captures reviewed commit, tree, every declared blob,
  first-parent admission, Copilot triage, verdict and blockers.
- B6R9/R19 do not establish a subject; S15 is the sole test-path subject and direct imports remain direct.
- S15 accepts only structured status/path raw Git name-status tuples with review-log before tester-evidence, while
  preserving all actual input fail-closed checks.
- T15/V15 are the only named range entries. Q15 uses committed full actual triple and real subprocess Git; all-absent
  remains skip/unverified and does not authorize classification or resolution.

## Reviewer Handoff

~~~json
{"current_route":"B6R9->R19->S15->T15->V15->Q15","correction_id":"observer-dispatcher-governance/high/b6r9","plan_review_path":"plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r9-review-log.md","implementation_subject":"S15 only","range":"S15..V15","verdict":"approved|needs-rework"}
~~~

## Post-merge / release actions

No release action is authorized. Stop at the Human boundary.

## Open Questions / Unresolved Items

step-creator remains deferred and has no effect on this route. B6R8/Q14 are frozen provenance. Q14 has exactly one
known failure: raw git diff --name-status lexical ordering; S15 is its sole bounded correction.
