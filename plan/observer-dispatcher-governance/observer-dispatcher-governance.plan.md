# Observer / Dispatcher Governance

## Goal / Outcome

以 B6R7 correction baseline 收斂 governance conformance route，建立可獨立驗證的
`B6R7 -> R17 -> S14 -> T14 -> V14 -> Q14 -> comment-classification/human-check`。本 topic 是
non-stable、review-ready-only work；停在 Human boundary。

## Scope

- **In Scope:** B6R7 exact-seven planning baseline、R17 plan review、S14 single test-path subject、T14/V14
  evidence、Q14 read-only actual Git gate，以及 passed Q14 後的 independent per-thread classification。
- **Out Of Scope:** 所有 frozen provenance、legacy migration、`step-creator` activation、產品/architecture work、
  unlisted paths、thread resolve、merge、release、post-merge。

## Locked Decisions

- Current correction 是 `observer-dispatcher-governance/high/b6r7`；current state 是
  `B6R7_REVIEW_PENDING`；B6R7/R17 是 non-subject，S14 是唯一 subject。
- B6R7 admission 是 non-merge first-parent exact-seven；pre-admission artifacts 不含 B6R7 revision、blob、
  `HEAD` 或 review outcome。
- S14 complete diff 只改 `tests/test_observer_dispatcher_governance_contract.py`；direct imports 是 mandatory，
  禁止 `importlib`/`__import__`/`sys.modules` substitution。
- T14/V14 是唯一 linear non-merge S14 descendants；named `S14..V14` range 只含兩個 B6R7 evidence paths。Q14
  是 post-V14、read-only、no artifact/no thread authority。
- Actual input 只接受完整 explicit `ODG_S14_SHA`/`ODG_T14_SHA`/`ODG_V14_SHA` 與 real subprocess Git；
  all-absent 為 skip/unverified，partial/invalid/symbolic/nonexistent/merge/wrong graph/range 一律 fail closed。

## Boundaries / Exclusions

Observer 只 dispatch/aggregate。Planner 單獨決定 phase/gate/role。Plan-Creator 寫 declared planning paths；
Plan-Reviewer 寫 R17；Implementer 做 approved bounded commits；Tester/Reviewer 只寫 declared evidence。任何 actor
不得 widen allowlist、resolve threads、merge、release 或 post-merge。

## Status / Allowed Transitions

**Current:** `B6R7_REVIEW_PENDING`。

唯一 transition 是 `B6R7 -> R17 -> S14 -> T14 -> V14 -> Q14 -> comment-classification/human-check`。R17 必須
clean-checkout-review committed B6R7；approved R17 原樣另行提交後才可 S14。S14 需要 R17 approval；T14 需要
same-S14 full-suite result；V14 需要 passing T14；Q14 需要 committed V14。failure 回 Planner；merge/release 停在
Human boundary。

## Artifact Paths

| Artifact | Exact path | Write owner | Decision authority | Role |
| --- | --- | --- | --- | --- |
| Shared workflow | `plan/agent-handoff-workflow.md` | Plan-Creator | Planner | B6R7 contract |
| Shared contract | `plan/topic-plan-contract.md` | Plan-Creator | Planner | B6R7 contract |
| Parent plan | `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md` | Plan-Creator | Planner | Current truth |
| Parent spec | `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md` | Plan-Creator | Planner | Acceptance |
| Parent step | `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md` | Plan-Creator | Planner | Tracker |
| B6R7 plan | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r7-plan.md` | Plan-Creator | Planner | Baseline delta |
| B6R7 step | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r7-step.md` | Plan-Creator | Planner | Baseline tracker |
| R17 review | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r7-review-log.md` | Plan-Reviewer | Plan-Reviewer verdict | Pre-S14 gate |
| S14 subject | `tests/test_observer_dispatcher_governance_contract.py` | Implementer | Planner | Sole implementation subject |
| T14 evidence | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r7-tester-evidence.md` | Tester | Factual test result | First descendant |
| V14 evidence | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r7-implementation-review-log.md` | Reviewer | Reviewer verdict | Final descendant |

`README.md`、`VERSION`、`.github/copilot-instructions.md` 與 `.github/agents/**` are ReadOnly. No path is
Deleted. Only the seven B6R7 planning paths are Written/Modified at admission; all other paths are excluded.

## Implementation Steps

1. Plan-Creator prepares exactly the B6R7 seven planning paths; Independent Implementer commits their exact
   non-merge first-parent admission.
2. Independent Plan-Reviewer clean-checkout-reviews committed B6R7, its tree, all seven blobs and admission, then
   writes R17. Independent Implementer separately commits approved R17 unchanged.
3. Planner verifies R17 and dispatches S14, which adds temporal frozen-provenance/current-route/subject/topology
   assertions while retaining direct imports and fail-closed actual-input semantics.
4. Tester writes T14 after the full suite. Reviewer writes V14 after passing T14 and validates the exact range.
5. Reviewer executes Q14 only after V14 commit; an independent Reviewer may then classify each thread. Stop at
   human-check.

## Validation / Acceptance Checks

- B6R7 admission is non-merge, first-parent, exact-seven; R17 captures reviewed commit, tree, every declared blob,
  first-parent admission, Copilot triage, verdict and blockers.
- B6R7/R17 do not establish a subject; S14 is the sole test-path subject and direct imports remain direct.
- Tests reject frozen routes as current, B6R7/R17 as subjects, substitution imports, malformed actual input,
  merge/wrong graph/widened range, and every topology other than `S14 -> T14 -> V14`.
- T14/V14 are the only named range entries. Q14 uses committed full actual triple and real subprocess Git; all-absent
  remains skip/unverified and does not authorize classification or resolution.

## Reviewer Handoff

```json
{"current_route":"B6R7->R17->S14->T14->V14->Q14","correction_id":"observer-dispatcher-governance/high/b6r7","plan_review_path":"plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r7-review-log.md","implementation_subject":"S14 only","range":"S14..V14","verdict":"approved|needs-rework"}
```

## Post-merge / release actions

No release action is authorized. Stop at the Human boundary.

## Open Questions / Unresolved Items

`step-creator` remains deferred and has no effect on this route. All prior correction evidence is frozen provenance.
