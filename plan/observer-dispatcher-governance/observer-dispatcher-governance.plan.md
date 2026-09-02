# Observer / Dispatcher Governance

> **B6R3 current-route override:** 其餘 normal/recovery、B0–B6、B6R/B6R2 route 文字均為 frozen
> nonrouting provenance。唯一 current route 是
> `B6R3 -> R13 -> S11 -> T11 -> V11 -> Q11 -> comment-classification/human-check`。B6R3/R13 non-subject；
> S11 是唯一 subject 且只可改 `tests/test_observer_dispatcher_governance_contract.py`。T11/V11 是 exact
> evidence-only descendants，Q11 為唯一 shared human boundary；Q8–Q10 無 current authority。comment
> resolution 僅限 Q11 後由獨立 Reviewer 對逐 thread 明示 `addressed-and-resolvable` 者。

> **Frozen provenance:** `b900366`, normal/recovery records, B0–B6 (including R8/R9/R10), S1–S10, T1–T10,
> V1–V10, Q7–Q10, and all earlier correction artifacts are immutable historical provenance. They are excluded
> from the B6R3 route. `step-creator` work remains deferred.

## Goal / Outcome

完成 B6R3 correction baseline，建立可獨立驗證的 `B6R3 -> R13 -> S11 -> T11 -> V11 -> Q11` route：只補強
governance contract test 的 route/provenance/topology assertions，並停在 Human boundary。

## Scope

- **In scope:** B6R3 seven planning paths、R13 review record、S11 single test path、T11/V11 evidence paths，及
  Q11 read-only actual query。
- **Out of scope:** frozen provenance、legacy migration、`step-creator` activation、產品或 architecture
  work、未列 paths、PR thread resolution、merge、release、post-merge。

## Locked Decisions

- B6R3 是唯一 current non-subject route；R13 是 B6R3 的 exact independent review record；S11 是唯一
  implementation subject。
- B6R3 admission 是 non-merge、first-parent exact seven-path baseline；B6R3 planning artifacts 不得包含
  B6R3 SHA/blob SHA/`HEAD`/review outcome。
- S11 complete diff 僅能修改 `tests/test_observer_dispatcher_governance_contract.py`。原有 direct imports
  必須保留；禁止用 `importlib`、`__import__` 或 `sys.modules` 取代測試行為。
- S11 actual graph assertion 只接受 complete explicit `ODG_S11_SHA`/`ODG_T11_SHA`/`ODG_V11_SHA`，並透過
  real subprocess `git rev-parse`、`git rev-list`、`git diff --name-status` 驗證。三值全 absent 為
  explicit skip/unverified；partial/invalid/`HEAD`/nonexistent/merge/wrong parent-or-graph/multi-path
  全部 fail closed。
- T11/V11 是唯一 linear non-merge S11 descendants；Q11 只讀、無 artifact、無 lifecycle 或 thread authority。
- 本 topic 為 non-stable、review-ready-only work；`step-creator` 維持 deferred。

## Boundaries / Exclusions

Observer 只 bootstrap-dispatch Planner；Planner 是唯一 routing authority。Plan-Creator 僅寫 B6R3
planning artifacts；Plan-Reviewer 僅寫 R13；Independent Implementer 只提交 approved artifacts 或
S11；Tester 和 Reviewer 僅寫已宣告 evidence。任何 actor 均不得 resolve PR threads、merge、release 或
widen allowlist。

## Status / Allowed Transitions

**Current:** `B6R3_REVIEW_PENDING`。

唯一 allowed route 是 `B6R3 -> R13 -> S11 -> T11 -> V11 -> Q11 -> comment-classification/human-check`。
B6R3 admission 尚待 exact seven-path non-merge commit-time truth；接著必須由獨立 R13 review。
approved R13 才可 dispatch S11；T11/V11 需同一 S11 的 passing evidence。
任何 failure 回到 Planner；Human boundary 前不會有 merge/release action。

## Artifact Paths

| Artifact | Exact path | Write owner | Decision authority | Role |
| --- | --- | --- | --- | --- |
| Shared workflow | `plan/agent-handoff-workflow.md` | Plan-Creator | Planner | B6R3 contract |
| Shared contract | `plan/topic-plan-contract.md` | Plan-Creator | Planner | B6R3 contract |
| Parent plan | `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md` | Plan-Creator | Planner | Current execution truth |
| Parent spec | `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md` | Plan-Creator | Planner | Acceptance contract |
| Parent step | `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md` | Plan-Creator | Planner | Current tracker |
| B6R3 plan | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r3-plan.md` | Plan-Creator | Planner | B6R3 delta |
| B6R3 step | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r3-step.md` | Plan-Creator | Planner | B6R3 tracker |
| R13 review | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r3-review-log.md` | Plan-Reviewer | Plan-Reviewer verdict | Pre-S11 gate |
| S11 implementation | `tests/test_observer_dispatcher_governance_contract.py` | Implementer | Planner | Sole test-only subject |
| T11 evidence | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r3-tester-evidence.md` | Tester | Factual test result | First descendant |
| V11 evidence | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r3-implementation-review-log.md` | Reviewer | Reviewer verdict; Planner route | Final descendant |

`README.md`、`VERSION`、`.github/copilot-instructions.md` 不修改。列外 path 必須停止並交 Planner。

## Implementation Steps

1. B6R3 non-merge admission 待完成，named first-parent diff 恰好為七個
   declared planning paths。
2. Independent Plan-Reviewer 在 committed B6R3 clean checkout 審 R13 fields 與 first-parent exact-seven
   admission，寫 R13；Independent Implementer 另行提交 unchanged approved R13。
3. Planner 驗證 R13 後，dispatch one non-merge S11，僅補強 test 中 B6R3 frozen provenance、B6R3/R13
   non-subject、S11 subject、T11/V11 topology/exact range、all-absent skip 和 partial/invalid fail-closed
   assertions。
4. Tester 寫 T11，Reviewer 寫 V11；二者均以 exact declared evidence paths 為限。

## Validation / Acceptance Checks

- B6R3 admission 為 non-merge，named first-parent diff 恰好七 paths，各一次；pre-commit artifacts
  不含 B6R3 SHA/blob SHA/`HEAD`/review outcome。
- R13 審每個 B6R3 field/blob/tree 與 first-parent result，approved record 另行 unchanged commit；B6R3/R13 不建立 subject。
- S11 是唯一 subject 且僅改 test path；direct imports 保持，dynamic import substitution 失敗。
- Test 讀取 parent workflow/contract/plan/spec/step 與 B6R3 plan/step，驗證 historical provenance 不可
  作 B6R3 route，並用 actual Git subprocess 驗證 complete S11/T11/V11 triple。
- T11/V11 是唯一 non-merge `S11 -> T11 -> V11`；named `S11..V11` 僅含其兩 paths；Q11 只讀且無 artifact/thread
  authority。

## Reviewer Handoff

```json
{"current_route":"B6R3->R13->S11->T11->V11->Q11","b6r3_review_path":"plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r3-review-log.md","implementation_subject":"S11 only","range":"S11..V11","verdict":"approved|needs-rework"}
```

## Post-merge / release actions

Stop at the Human boundary; no release action is authorized.

## Open Questions / Unresolved Items

The next action is B6R3 admission then independent R13 review; no identity is embedded before review.
