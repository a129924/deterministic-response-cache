# Observer / Dispatcher Governance

> **Frozen provenance:** `b900366`, B0–B4R6, S1–S5, T1–T5, V1–V5, normal/recovery records,
> `7d23e8c`, `6ede06b`, every older correction artifact, and any uncommitted B4R6 review-log are
> historical nonrouting provenance. They create no current candidate, status, gate, subject, schema,
> checklist, or pending work.

## Goal / Outcome

完成 B4R7 correction baseline：以一次 commit-time exact-seven-path admission、獨立 R7 review，
再以已鎖定的 S6 15-path subject 和 T6/V6 evidence 收斂至 Human boundary。

## Scope

- **In scope:** B4R7 seven planning paths、R7 review record、既有 S6 exact 15-path allowlist，
  以及 B4R7 專屬 T6/V6 evidence paths。
- **Out of scope:** B4R6 或更早 epoch、legacy migration、`step-creator` threads、未列 path、
  產品/architecture work、PR thread action、merge、release、post-merge。

## Locked Decisions

- B4R7 是唯一 current non-subject baseline。它在 commit 前不嵌入 SHA、`HEAD`、預測 blob 或
  review outcome；commit admission 以其 first-parent non-merge commit 的 named exact diff 作 truth。
- R7 只在 committed B4R7 seven-blob baseline 上作獨立 review。只有 separately committed approved
  R7 record 才能啟動 S6；B4R7 與 R7 都不能建立 `implementation_subject_sha`。
- S6 是唯一 implementation subject，且只能修改下列既有 15-path allowlist；direct imports 保持
  mandatory，禁止 `importlib`、`__import__`、`sys.modules` substitution。
- 實際 named SHA graph 必須證明非 merge 的 `S6 -> T6 -> V6`；`git diff --name-status S6..V6`
  只可含 B4R7 的兩個 evidence paths，絕不使用 `HEAD` 或文字推論。
- 兩個 `step-creator` threads 持續 deferred；本 topic 為 non-stable、review-ready-only work。

## Boundaries / Exclusions

Observer bootstrap-dispatches Planner only; Planner is the sole routing authority. Plan-Creator writes
only B4R7's seven planning artifacts; Plan-Reviewer writes only R7; Independent Implementer commits
approved artifacts or S6; Tester and Reviewer independently write only their declared evidence. No actor
may resolve PR threads, merge, release, or widen the allowlist.

## Status / Allowed Transitions

`B4R7_REVIEW_PENDING` means only this: an Independent Implementer must first create one non-merge
baseline commit whose named first-parent admission diff contains the complete exact B4R7 seven-path set.
The planning text contains no commit SHA or `HEAD` placeholder. After that admission succeeds, R7 reviews
the committed seven blobs, then the route is `B4R7 -> R7 -> S6 -> T6 -> V6 -> human-check`.
Any failure returns to Planner; frozen history is never a fallback.

## Artifact Paths

| Artifact | Exact path | Write owner | Decision authority | Role |
| --- | --- | --- | --- | --- |
| Shared workflow | `plan/agent-handoff-workflow.md` | Plan-Creator | Planner | B4R7 contract |
| Shared contract | `plan/topic-plan-contract.md` | Plan-Creator | Planner | B4R7 contract |
| Parent plan | `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md` | Plan-Creator | Planner | Current execution truth |
| Parent spec | `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md` | Plan-Creator | Planner | Acceptance contract |
| Parent step | `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md` | Plan-Creator | Planner | Current tracker |
| B4R7 plan | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r7-plan.md` | Plan-Creator | Planner | B4R7 delta |
| B4R7 step | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r7-step.md` | Plan-Creator | Planner | B4R7 tracker |
| R7 review | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r7-review-log.md` | Plan-Reviewer | Plan-Reviewer verdict | Pre-S6 gate |
| T6 evidence | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r7-tester-evidence.md` | Tester | Factual test result | First descendant |
| V6 evidence | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r7-implementation-review-log.md` | Reviewer | Reviewer verdict; Planner route | Final descendant |

After separately committed approved R7 review, S6 may modify exactly:

1. `AGENTS.md`
2. `.codex/agents/planner.toml`
3. `.codex/agents/implementer.toml`
4. `.codex/agents/reviewer.toml`
5. `.agents/skills/plan-creator/SKILL.md`
6. `.agents/skills/plan-creator/checklist.md`
7. `.agents/skills/plan-creator/templates/topic-plan-template.md`
8. `.agents/skills/plan-reviewer/SKILL.md`
9. `.agents/skills/plan-reviewer/checklist.md`
10. `.agents/skills/plan-reviewer/reference.md`
11. `.agents/skills/plan-reviewer/examples.md`
12. `.agents/skills/python-implementation-workflow/SKILL.md`
13. `.agents/skills/python-implementation-workflow/reference.md`
14. `.agents/skills/python-plan-authoring/templates/canonical-python-topic-plan-template.md`
15. `tests/test_observer_dispatcher_governance_contract.py`

## Implementation Steps

1. Independent Implementer performs B4R7 commit admission: one non-merge commit, first containing
   exactly the complete seven declared baseline paths, and reports the named exact diff against its
   immediate first parent.
2. Independent Plan-Reviewer writes R7 after reviewing every committed B4R7 blob once; Independent
   Implementer separately commits the unchanged approved R7 record.
3. Planner verifies R7 then dispatches one non-merge S6 over the exact 15-path allowlist. Tester writes
   T6 and Reviewer writes V6 as its two evidence-only descendants.

## Validation / Acceptance Checks

- B4R7 admission commit is non-merge and its named first-parent diff is exactly the seven declared B4R7
  paths, each present; no SHA/`HEAD` was embedded in the pre-commit planning artifacts.
- R7 records the B4R7 committed SHA and each of those seven actual blobs exactly once; its approved record
  is separately committed unchanged before S6.
- S6 is the unique subject and has no path outside the preserved 15-path allowlist.
- T6 and V6 attest the same S6; V6 requires passing T6; each uses its exact B4R7 evidence path.
- Actual named Git commands prove non-merge `S6 -> T6 -> V6` and named `git diff --name-status S6..V6`
  lists exactly the two B4R7 T6/V6 evidence paths.
- Tests fail closed for frozen provenance as route/subject, B4R7/R7 as subject, admission/path mutation,
  direct-import substitution, deferred-work activation, merge/third descendant, or wrong named range.

## Reviewer Handoff

```json
{"current_route":"B4R7-admission->R7->S6->T6->V6","b4r7_review_path":"plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r7-review-log.md","implementation_subject":"S6 only","range":"S6..V6","verdict":"approved|needs-rework"}
```

The B4R7 R7/T6/V6 schemas are defined by
`plan/topic-plan-contract.md#b4r7-correction-evidence-schemas`.

## Post-merge / release actions

Stop at the Human boundary; none are authorized.

## Open Questions / Unresolved Items

The sole pending action is B4R7 commit admission. B4R7's commit SHA is intentionally unknown until that
admission completes; all B4R6 and earlier evidence remains frozen.

## B5 Current-Route Supersession

All B4R7 content above is frozen nonrouting provenance. B5 is the only current route:
`B5 -> R8 -> S7 -> T7 -> V7 -> Q7 -> comment-classification/human-check`. B5 is a non-subject exact
seven-planning-path baseline; R8 is a separate clean-checkout review. B4R7/S6/T6 and missing V6 cannot
route current work.

S7 is the sole non-merge subject and changes only
`tests/test_observer_dispatcher_governance_contract.py`. Its actual graph/range test relies only on complete
explicit `ODG_S7_SHA`, `ODG_T7_SHA`, `ODG_V7_SHA` input and real subprocess `git rev-parse`, `git rev-list`,
and `git diff --name-status`; no variables explicitly skip, partial/invalid/`HEAD`/merge/wrong-parent/
multi-path input fails closed. Direct imports and deferred `step-creator` remain locked.

T7/V7 are evidence-only descendants. Q7 is post-V7 read-only actual query using full V7 SHA, with no artifact,
no `HEAD`, no lifecycle decision, and no PR-thread resolution authority.
