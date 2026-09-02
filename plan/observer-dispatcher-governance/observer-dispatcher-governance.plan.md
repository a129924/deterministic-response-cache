# Observer / Dispatcher Governance

> **B6R2 current-route override:** 其餘 B6R route 文字均為 frozen nonrouting provenance。唯一 current
> route 是 `B6R2 -> R12 -> S10 -> T10 -> V10 -> Q10 -> comment-classification/human-check`。B6R2/R12
> non-subject；S10 是唯一 subject 且只可改
> `tests/test_observer_dispatcher_governance_contract.py`。T10/V10 是 exact evidence-only descendants，
> Q10 為唯一 shared human boundary；Q8/Q9 無 current authority。comment resolution 僅限 Q10 後由獨立
> Reviewer 對逐 thread 明示 `addressed-and-resolvable` 者。

> **Frozen provenance:** `b900366`, normal/recovery records, B0–B6 (including R8/R9/R10), S1–S8, T1–T8,
> V1–V8, Q7/Q8, and all earlier correction artifacts are immutable historical provenance. They are excluded
> from the B6R route. `step-creator` work remains deferred.

## Goal / Outcome

完成 B6R correction baseline，建立可獨立驗證的 `B6R -> R11 -> S9 -> T9 -> V9 -> Q9` route：只補強
governance contract test 的 route/provenance/topology assertions，並停在 Human boundary。

## Scope

- **In scope:** B6R seven planning paths、R11 review record、S9 single test path、T9/V9 evidence paths，及
  Q9 read-only actual query。
- **Out of scope:** frozen provenance、legacy migration、`step-creator` activation、產品或 architecture
  work、未列 paths、PR thread resolution、merge、release、post-merge。

## Locked Decisions

- B6R 是唯一 current non-subject route；R11 是 B6R 的 exact independent review record；S9 是唯一
  implementation subject。
- B6R admission 是 non-merge、first-parent exact seven-path baseline；B6R planning artifacts 不得包含
  B6R SHA/blob SHA/`HEAD`/review outcome。
- S9 complete diff 僅能修改 `tests/test_observer_dispatcher_governance_contract.py`。原有 direct imports
  必須保留；禁止用 `importlib`、`__import__` 或 `sys.modules` 取代測試行為。
- S9 actual graph assertion 只接受 complete explicit `ODG_S9_SHA`/`ODG_T9_SHA`/`ODG_V9_SHA`，並透過
  real subprocess `git rev-parse`、`git rev-list`、`git diff --name-status` 驗證。三值全 absent 為
  explicit skip/unverified；partial/invalid/`HEAD`/nonexistent/merge/wrong parent-or-graph/multi-path
  全部 fail closed。
- T9/V9 是唯一 linear non-merge S9 descendants；Q9 只讀、無 artifact、無 lifecycle 或 thread authority。
- 本 topic 為 non-stable、review-ready-only work；`step-creator` 維持 deferred。

## Boundaries / Exclusions

Observer 只 bootstrap-dispatch Planner；Planner 是唯一 routing authority。Plan-Creator 僅寫 B6R
planning artifacts；Plan-Reviewer 僅寫 R11；Independent Implementer 只提交 approved artifacts 或
S9；Tester 和 Reviewer 僅寫已宣告 evidence。任何 actor 均不得 resolve PR threads、merge、release 或
widen allowlist。

## Status / Allowed Transitions

**Current:** `B6R_REVIEW_PENDING`。

唯一 allowed route 是 `B6R -> R11 -> S9 -> T9 -> V9 -> Q9 -> comment-classification/human-check`。
B6R admission 已以 exact seven-path non-merge commit-time truth 完成；接著必須由獨立 R11 review。
approved R11 才可 dispatch S9；T9/V9 需同一 S9 的 passing evidence。
任何 failure 回到 Planner；Human boundary 前不會有 merge/release action。

## Artifact Paths

| Artifact | Exact path | Write owner | Decision authority | Role |
| --- | --- | --- | --- | --- |
| Shared workflow | `plan/agent-handoff-workflow.md` | Plan-Creator | Planner | B6R contract |
| Shared contract | `plan/topic-plan-contract.md` | Plan-Creator | Planner | B6R contract |
| Parent plan | `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md` | Plan-Creator | Planner | Current execution truth |
| Parent spec | `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md` | Plan-Creator | Planner | Acceptance contract |
| Parent step | `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md` | Plan-Creator | Planner | Current tracker |
| B6R plan | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r-plan.md` | Plan-Creator | Planner | B6R delta |
| B6R step | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r-step.md` | Plan-Creator | Planner | B6R tracker |
| R11 review | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r-review-log.md` | Plan-Reviewer | Plan-Reviewer verdict | Pre-S9 gate |
| S9 implementation | `tests/test_observer_dispatcher_governance_contract.py` | Implementer | Planner | Sole test-only subject |
| T9 evidence | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r-tester-evidence.md` | Tester | Factual test result | First descendant |
| V9 evidence | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r-implementation-review-log.md` | Reviewer | Reviewer verdict; Planner route | Final descendant |

`README.md`、`VERSION`、`.github/copilot-instructions.md` 不修改。列外 path 必須停止並交 Planner。

## Implementation Steps

1. B6R non-merge admission 已完成，named first-parent diff 恰好為七個
   declared planning paths。
2. Independent Plan-Reviewer 在 committed B6R clean checkout 審 R11 fields 與 first-parent exact-seven
   admission，寫 R11；Independent Implementer 另行提交 unchanged approved R11。
3. Planner 驗證 R11 後，dispatch one non-merge S9，僅補強 test 中 B6R frozen provenance、B6R/R11
   non-subject、S9 subject、T9/V9 topology/exact range、all-absent skip 和 partial/invalid fail-closed
   assertions。
4. Tester 寫 T9，Reviewer 寫 V9；二者均以 exact declared evidence paths 為限。

## Validation / Acceptance Checks

- B6R admission 為 non-merge，named first-parent diff 恰好七 paths，各一次；pre-commit artifacts
  不含 B6R SHA/blob SHA/`HEAD`/review outcome。
- R11 審每個 B6R field/blob 與 first-parent result，approved record 另行 unchanged commit；B6R/R11 不建立 subject。
- S9 是唯一 subject 且僅改 test path；direct imports 保持，dynamic import substitution 失敗。
- Test 讀取 parent workflow/contract/plan/spec/step 與 B6R plan/step，驗證 historical provenance 不可
  作 B6R route，並用 actual Git subprocess 驗證 complete S9/T9/V9 triple。
- T9/V9 是唯一 non-merge `S9 -> T9 -> V9`；named `S9..V9` 僅含其兩 paths；Q9 只讀且無 artifact/thread
  authority。

## Reviewer Handoff

```json
{"current_route":"B6R->R11->S9->T9->V9->Q9","b6r_review_path":"plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r-review-log.md","implementation_subject":"S9 only","range":"S9..V9","verdict":"approved|needs-rework"}
```

## Post-merge / release actions

Stop at the Human boundary; no release action is authorized.

## Open Questions / Unresolved Items

The next action is independent R11 review of committed B6R admission; no identity is embedded before review.
