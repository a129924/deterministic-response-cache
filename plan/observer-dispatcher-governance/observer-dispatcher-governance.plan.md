# Observer / Dispatcher Governance

> **B6R6 current-plan override:** only `B6R6 -> R16 -> S14 -> T14 -> V14 -> Q14 -> comment-classification/human-check`
> is current. B6R6/R16 are non-subject; S14 only changes the governance contract test with direct imports. T14/V14 are
> the only linear non-merge descendants and Q14 is the post-V14 actual full-triple read-only gate. B6R5 and every older
> normal/recovery/correction route is frozen nonrouting provenance; `step-creator` remains deferred.

> **B6R6 status:** `B6R6_REVIEW_PENDING`. Creator/admission are complete; R16, S14, T14, V14, Q14 and independent
> classification are pending. Exact B6R6 admission paths are shared workflow/contract, parent plan/spec/step and B6R6
> plan/step; no unlisted path is allowed.

> **B6R5 current-route override:** 其餘 normal/recovery、B0–B6、B6R–B6R4、R14、S12 與所有較早 route
> 文字均為 frozen nonrouting provenance。唯一 current route 是
> `B6R5 -> R15 -> S13 -> T13 -> V13 -> Q13 -> comment-classification/human-check`。B6R5/R15 non-subject；
> S13 是唯一 subject 且只可改 `tests/test_observer_dispatcher_governance_contract.py`，保留 direct imports。
> T13 是 truthful passing full-suite evidence，one no-environment actual graph 為 `skip`/`unverified`，不得宣稱
> complete triple。V13 只審 structural `S13 -> T13 -> V13` 與 `S13..T13`。Q13 在 committed V13 後以 complete
> explicit full SHA triple 執行唯一 non-skipped actual Git gate；失敗閉鎖，才可進獨立 comment classification。

> **Frozen provenance:** `b900366`, normal/recovery records, B0–B6 (including R8/R9/R10), S1–S10, T1–T10,
> V1–V10, Q7–Q11, and all earlier correction artifacts are immutable historical provenance. They are excluded
> from the B6R5 route. `step-creator` work remains deferred. B6R4/R14/S12 為 failed frozen nonrouting provenance。

## Goal / Outcome

完成 B6R4 correction baseline，建立可獨立驗證的 `B6R4 -> R14 -> S12 -> T12 -> V12 -> Q12` route：只補強
governance contract test 的 route/provenance/topology assertions，並停在 Human boundary。

## Scope

- **In scope:** B6R4 seven planning paths、R14 review record、S12 single test path、T12/V12 evidence paths，及
  Q12 read-only actual query。
- **Out of scope:** frozen provenance、legacy migration、`step-creator` activation、產品或 architecture
  work、未列 paths、PR thread resolution、merge、release、post-merge。

## Locked Decisions

- B6R4 是唯一 current non-subject route；R14 是 B6R4 的 exact independent review record；S12 是唯一
  implementation subject。
- B6R4 admission 是 non-merge、first-parent exact seven-path baseline；B6R4 planning artifacts 不得包含
  B6R4 SHA/blob SHA/`HEAD`/review outcome。
- S12 complete diff 僅能修改 `tests/test_observer_dispatcher_governance_contract.py`。原有 direct imports
  必須保留；禁止用 `importlib`、`__import__` 或 `sys.modules` 取代測試行為。
- S12 actual graph assertion 只接受 complete explicit `ODG_S12_SHA`/`ODG_T12_SHA`/`ODG_V12_SHA`，並透過
  real subprocess `git rev-parse`、`git rev-list`、`git diff --name-status` 驗證。三值全 absent 為
  explicit skip/unverified；partial/invalid/`HEAD`/nonexistent/merge/wrong parent-or-graph/multi-path
  全部 fail closed。
- T12/V12 是唯一 linear non-merge S12 descendants；Q12 只讀、無 artifact、無 lifecycle 或 thread authority。
- 本 topic 為 non-stable、review-ready-only work；`step-creator` 維持 deferred。

## Boundaries / Exclusions

Observer 只 bootstrap-dispatch Planner；Planner 是唯一 routing authority。Plan-Creator 僅寫 B6R4
planning artifacts；Plan-Reviewer 僅寫 R14；Independent Implementer 只提交 approved artifacts 或
S12；Tester 和 Reviewer 僅寫已宣告 evidence。任何 actor 均不得 resolve PR threads、merge、release 或
widen allowlist。

## Status / Allowed Transitions

**Current:** `B6R4_REVIEW_PENDING`。

唯一 allowed route 是 `B6R4 -> R14 -> S12 -> T12 -> V12 -> Q12 -> comment-classification/human-check`。
B6R4 admission 已 committed；下一步必須由獨立 R14 clean-checkout review。
approved R14 才可 dispatch S12；T12/V12 需同一 S12 的 passing evidence。
任何 failure 回到 Planner；Human boundary 前不會有 merge/release action。

## Artifact Paths

| Artifact | Exact path | Write owner | Decision authority | Role |
| --- | --- | --- | --- | --- |
| Shared workflow | `plan/agent-handoff-workflow.md` | Plan-Creator | Planner | B6R4 contract |
| Shared contract | `plan/topic-plan-contract.md` | Plan-Creator | Planner | B6R4 contract |
| Parent plan | `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md` | Plan-Creator | Planner | Current execution truth |
| Parent spec | `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md` | Plan-Creator | Planner | Acceptance contract |
| Parent step | `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md` | Plan-Creator | Planner | Current tracker |
| B6R4 plan | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r4-plan.md` | Plan-Creator | Planner | B6R4 delta |
| B6R4 step | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r4-step.md` | Plan-Creator | Planner | B6R4 tracker |
| R14 review | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r4-review-log.md` | Plan-Reviewer | Plan-Reviewer verdict | Pre-S12 gate |
| S12 implementation | `tests/test_observer_dispatcher_governance_contract.py` | Implementer | Planner | Sole test-only subject |
| T12 evidence | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r4-tester-evidence.md` | Tester | Factual test result | First descendant |
| V12 evidence | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r4-implementation-review-log.md` | Reviewer | Reviewer verdict; Planner route | Final descendant |

`README.md`、`VERSION`、`.github/copilot-instructions.md` 不修改。列外 path 必須停止並交 Planner。

## Implementation Steps

1. B6R4 non-merge admission 已完成，named first-parent diff 恰好為七個 declared planning paths。
2. Independent Plan-Reviewer 在 committed B6R4 clean checkout 審 R14 fields 與 first-parent exact-seven
   admission，寫 R14；Independent Implementer 另行提交 unchanged approved R14。
3. Planner 驗證 R14 後，dispatch one non-merge S12，僅補強 test 中 B6R4 frozen provenance、B6R4/R14
   non-subject、S12 subject、T12/V12 topology/exact range、all-absent skip 和 partial/invalid fail-closed
   assertions。
4. Tester 寫 T12，Reviewer 寫 V12；二者均以 exact declared evidence paths 為限。

## Validation / Acceptance Checks

- B6R4 admission 為 non-merge，named first-parent diff 恰好七 paths，各一次；pre-commit artifacts
  不含 B6R4 SHA/blob SHA/`HEAD`/review outcome。
- R14 審每個 B6R4 field/blob/tree 與 first-parent result，approved record 另行 unchanged commit；B6R4/R14 不建立 subject。
- S12 是唯一 subject 且僅改 test path；direct imports 保持，dynamic import substitution 失敗。
- Test 讀取 parent workflow/contract/plan/spec/step 與 B6R4 plan/step，驗證 historical provenance 不可
  作 B6R4 route，並用 actual Git subprocess 驗證 complete S12/T12/V12 triple。
- T12/V12 是唯一 non-merge `S12 -> T12 -> V12`；named `S12..V12` 僅含其兩 paths；Q12 只讀且無 artifact/thread
  authority。

## Reviewer Handoff

```json
{"current_route":"B6R4->R14->S12->T12->V12->Q12","b6r4_review_path":"plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r4-review-log.md","implementation_subject":"S12 only","range":"S12..V12","verdict":"approved|needs-rework"}
```

## Post-merge / release actions

Stop at the Human boundary; no release action is authorized.

## Open Questions / Unresolved Items

The B6R4 admission is already committed; the next action is independent R14 review. No B6R4 SHA/blob/`HEAD`/review outcome is embedded in pre-admission planning artifacts.
