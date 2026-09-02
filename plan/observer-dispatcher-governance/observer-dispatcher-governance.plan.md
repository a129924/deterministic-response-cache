# Observer / Dispatcher Governance

> **Frozen provenance:** `b900366`, normal/recovery records, B0–B5R (including R8/R9), S1–S7, T1–T7,
> V1–V7, Q7, and all earlier correction artifacts are immutable historical provenance. They are excluded
> from the B6 route. `step-creator` work remains deferred.

## Goal / Outcome

完成 B6 correction baseline，建立可獨立驗證的 `B6 -> R10 -> S8 -> T8 -> V8 -> Q8` route：只補強
governance contract test 的 route/provenance/topology assertions，並停在 Human boundary。

## Scope

- **In scope:** B6 seven planning paths、R10 review record、S8 single test path、T8/V8 evidence paths，及
  Q8 read-only actual query。
- **Out of scope:** frozen provenance、legacy migration、`step-creator` activation、產品或 architecture
  work、未列 paths、PR thread resolution、merge、release、post-merge。

## Locked Decisions

- B6 是唯一 current non-subject route；R10 是 B6 的 exact independent review record；S8 是唯一
  implementation subject。
- B6 admission 是 non-merge、first-parent exact seven-path baseline；B6 planning artifacts 不得包含
  B6 SHA/blob SHA/`HEAD`/review outcome。
- S8 complete diff 僅能修改 `tests/test_observer_dispatcher_governance_contract.py`。原有 direct imports
  必須保留；禁止用 `importlib`、`__import__` 或 `sys.modules` 取代測試行為。
- S8 actual graph assertion 只接受 complete explicit `ODG_S8_SHA`/`ODG_T8_SHA`/`ODG_V8_SHA`，並透過
  real subprocess `git rev-parse`、`git rev-list`、`git diff --name-status` 驗證。三值全 absent 為
  explicit skip/unverified；partial/invalid/`HEAD`/nonexistent/merge/wrong parent-or-graph/multi-path
  全部 fail closed。
- T8/V8 是唯一 linear non-merge S8 descendants；Q8 只讀、無 artifact、無 lifecycle 或 thread authority。
- 本 topic 為 non-stable、review-ready-only work；`step-creator` 維持 deferred。

## Boundaries / Exclusions

Observer 只 bootstrap-dispatch Planner；Planner 是唯一 routing authority。Plan-Creator 僅寫 B6
planning artifacts；Plan-Reviewer 僅寫 R10；Independent Implementer 只提交 approved artifacts 或
S8；Tester 和 Reviewer 僅寫已宣告 evidence。任何 actor 均不得 resolve PR threads、merge、release 或
widen allowlist。

## Status / Allowed Transitions

**Current:** `B6_ADMISSION_PENDING`。

唯一 allowed route 是 `B6 -> R10 -> S8 -> T8 -> V8 -> Q8 -> comment-classification/human-check`。
B6 admission 後 R10 才可 review；approved R10 才可 dispatch S8；T8/V8 需同一 S8 的 passing evidence。
任何 failure 回到 Planner；Human boundary 前不會有 merge/release action。

## Artifact Paths

| Artifact | Exact path | Write owner | Decision authority | Role |
| --- | --- | --- | --- | --- |
| Shared workflow | `plan/agent-handoff-workflow.md` | Plan-Creator | Planner | B6 contract |
| Shared contract | `plan/topic-plan-contract.md` | Plan-Creator | Planner | B6 contract |
| Parent plan | `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md` | Plan-Creator | Planner | Current execution truth |
| Parent spec | `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md` | Plan-Creator | Planner | Acceptance contract |
| Parent step | `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md` | Plan-Creator | Planner | Current tracker |
| B6 plan | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6-plan.md` | Plan-Creator | Planner | B6 delta |
| B6 step | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6-step.md` | Plan-Creator | Planner | B6 tracker |
| R10 review | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6-review-log.md` | Plan-Reviewer | Plan-Reviewer verdict | Pre-S8 gate |
| S8 implementation | `tests/test_observer_dispatcher_governance_contract.py` | Implementer | Planner | Sole test-only subject |
| T8 evidence | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6-tester-evidence.md` | Tester | Factual test result | First descendant |
| V8 evidence | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6-implementation-review-log.md` | Reviewer | Reviewer verdict; Planner route | Final descendant |

`README.md`、`VERSION`、`.github/copilot-instructions.md` 不修改。列外 path 必須停止並交 Planner。

## Implementation Steps

1. Independent Implementer 作一次 B6 non-merge admission commit，named first-parent diff 恰好為七個
   declared planning paths。
2. Independent Plan-Reviewer 在 committed B6 clean checkout 審七 blobs，寫 R10；Independent
   Implementer 另行提交 unchanged approved R10。
3. Planner 驗證 R10 後，dispatch one non-merge S8，僅補強 test 中 B6 frozen provenance、B6/R10
   non-subject、S8 subject、T8/V8 topology/exact range、all-absent skip 和 partial/invalid fail-closed
   assertions。
4. Tester 寫 T8，Reviewer 寫 V8；二者均以 exact declared evidence paths 為限。

## Validation / Acceptance Checks

- B6 admission 為 non-merge，named first-parent diff 恰好七 paths，各一次；pre-commit artifacts
  不含 B6 SHA/blob SHA/`HEAD`/review outcome。
- R10 審每個 B6 blob 一次，approved record 另行 unchanged commit；B6/R10 不建立 subject。
- S8 是唯一 subject 且僅改 test path；direct imports 保持，dynamic import substitution 失敗。
- Test 讀取 parent workflow/contract/plan/spec/step 與 B6 plan/step，驗證 historical provenance 不可
  作 B6 route，並用 actual Git subprocess 驗證 complete S8/T8/V8 triple。
- T8/V8 是唯一 non-merge `S8 -> T8 -> V8`；named `S8..V8` 僅含其兩 paths；Q8 只讀且無 artifact/thread
  authority。

## Reviewer Handoff

```json
{"current_route":"B6->R10->S8->T8->V8->Q8","b6_review_path":"plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6-review-log.md","implementation_subject":"S8 only","range":"S8..V8","verdict":"approved|needs-rework"}
```

## Post-merge / release actions

Stop at the Human boundary; no release action is authorized.

## Open Questions / Unresolved Items

The next action is B6 admission commit; its SHA is intentionally unknown until that commit exists.
