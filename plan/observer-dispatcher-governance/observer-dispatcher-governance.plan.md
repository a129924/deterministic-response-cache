# Observer / Dispatcher Governance

## Goal / Outcome

- 完成 high-severity correction，讓 Observer / Dispatcher governance、custom-agent
  instructions、workflow skills 與 executable contract test 共用可審計的派遣與
  evidence contract。
- topic 保持 `needs-rework`，直到新 correction chain 完整通過；old epoch terminal
  `R0=cb3f66c60e95e5580cb2b30632d0d5ed9f0d0ee9` 的唯一 predicate 是
  `ecc5b6f61bacc5493ca3a9f1012d1bfdd43a810c..cb3f66c60e95e5580cb2b30632d0d5ed9f0d0ee9`。
  narrow `B0` exception 之後，只有 `S1 -> T1 -> V1`；驗證使用 `S1..V1`，絕不以 `HEAD` 代替。

> **Analysis-layer warning:** `analysis/observer-dispatcher-governance/requirements.md`
> 與 `analysis/observer-dispatcher-governance/technical-spec.md` 不存在。本 plan 依
> Planner 已核准的 high-severity correction direction author；此 warning 不授權重新開啟
> architecture、BC、identity 或未列 path。

## Scope

- **In scope**: `AGENTS.md`、僅 `.codex/agents/planner.toml` 與
  `.codex/agents/implementer.toml`（唯一 narrow `.codex` exception）、workflow / topic-plan
  contract、Plan-Creator / Plan-Reviewer / Python workflow surfaces、Python plan
  template、governance contract test、本 topic parent plan/spec/step，以及五份
  `correction-*` artifacts。
- **Out of scope**: 產品 library、public API、BC、Identity、Response Reuse、CacheStore、
  runtime、architecture docs、README、VERSION、release、tag、push、PR / thread、merge、
  post-merge、summary、`.github/agents/**`、legacy evidence migration / reader /
  compatibility layer，以及未列於 `Artifact Paths` 的任何檔案。

## Locked Decisions

- 這是 Planner-confirmed `high` correction，routing state 為 `PLANNER_REPLAN`；現有
  implementation / evidence confidence 視為失效，直至新 correction chain 通過。
- Human 的此 scope expansion authorization 為 `2. 授權擴張 current topic。`；current
  correction route 的 authoritative source 是兩份 shared contracts、parent plan/spec/step、
  correction plan/step，及其 exact pre-implementation correction review evidence。
- Parent plan、spec 與 step 在 Plan-Creator backfill 後仍是 current execution truth；
  correction plan / step 是 retained historical correction delta，不取代 parent。
  `correction-review-log.md` 僅在其 pre-implementation gate 尚未完成時是 current routing
  evidence；completed 後仍保留為 evidence，不成為 parent execution truth。
- 下列既有 artifacts 與其任何 SHA / verdict 都是 frozen, superseded provenance，不得
  修改、遷移、重讀為 current gate 或推導新 subject：`review-log.md`、
  `planning-review-evidence.md`、`tester-evidence.md`、`implementation-review-log.md`，
  以及所有 `recovery-*` evidence files。
- Old epoch terminal 是 `R0=cb3f66c60e95e5580cb2b30632d0d5ed9f0d0ee9`，唯一 predicate 為
  `ecc5b6f61bacc5493ca3a9f1012d1bfdd43a810c..cb3f66c60e95e5580cb2b30632d0d5ed9f0d0ee9`。
  narrow `B0` exception 僅容許 Plan-Reviewer 以同一 tree/blob 審閱七個未提交 planning
  artifacts，寫入 correction review log，並由 Independent Implementer 將該 log 與七個
  reviewed artifacts 一起提交為 `B0`；`B0` 絕非 subject。
- 只有 `B0` 後的 declared implementation non-merge `S1` commit 建立 replacement immutable
  `implementation_subject_sha`。新 subject 後嚴格只允許 `T1`（Tester evidence）再 `V1`
  （Reviewer evidence）兩個 linear、non-merge、evidence-only commits。第三個 path、merge、
  lifecycle action 或以 `HEAD` 取代 `S1..V1` 驗證使 chain 無效並回交 Planner。
- 這是 non-stable、review-ready-only topic：README / VERSION 不修改，無 release / tag；
  standalone correction skill 只可在另開 topic 且 repeated instability 或
  cross-workflow reuse 已證實時再考慮。

## Boundaries / Exclusions

- Observer 只讀 state、依 Planner 決定派遣一個角色、彙整 bounded result 並回報
  `可直接前進`、`needs-rework`、`blocked` 或 `human-check`；不得實作、改檔、git、
  gate inference、comment handling 或重解 locked decisions。
- Planner 是 candidate、phase、gate、severity、correction routing 與 next role 的唯一
  authority。Plan-Creator 只 author / sync planning artifacts；Implementer 只實作及
  原樣固化已授權 evidence；Tester 與 Reviewer 必須真實獨立。
- `.github/agents/**` 僅為 frozen provenance，絕非 runtime dependency；唯一可修改的
  `.codex` paths 是 `.codex/agents/planner.toml` 與 `.codex/agents/implementer.toml`。Identity BC、
  CacheStore 與其餘 deferred BC boundaries 維持不變。任何未列 path 或 direction change
  都停止並回交 Planner，chat、branch、PR Ready、summary 或舊 evidence 不得補推 gate。

## Status / Allowed Transitions

- **Current**: `needs-rework`；correction routing state 為 `PLANNER_REPLAN`。
- **Execution model**: narrow `B0` exception 下 Plan-Reviewer 先 tree/blob review 七個未提交
  planning artifacts 並寫 correction-plan review record；Independent Implementer 原樣將 record
  加七個 reviewed artifacts commit 成 `B0`，其非 subject。只有其後單一 non-merge `S1` declared
  implementation commit 建立 immutable subject；Tester `T1`、再 Reviewer `V1` 各自 attest `S1`；
  僅以 `S1..V1` 驗證後停止於 Human boundary。
- **Allowed transitions**:
  - `needs-rework` -> `creator-in-progress`
  - `creator-in-progress` -> `review-ready`
  - `review-ready` -> `reviewer-in-progress`
  - `reviewer-in-progress` -> `approved|needs-rework`
  - `approved` -> `creator-in-progress|publish-in-progress`
  - `publish-in-progress` -> `pr-open|merged`
  - `pr-open` -> `needs-rework|merged`
  - `merged` -> terminal
- **Correction routing**: correction review `needs-rework` 保持 topic `needs-rework`
  並要求新的 Planner-frozen direction。final correction implementation review
  `needs-rework` 使 new chain 無效；不得用 patch、extra descendant 或 prior evidence 修復。

## Artifact Paths

| Artifact | Path | Write owner | Decision authority | Role |
| --- | --- | --- | --- | --- |
| Governance | `AGENTS.md` | Implementer | Planner | Observer / Dispatcher runtime governance and frozen-provenance boundary |
| Planner custom agent | `.codex/agents/planner.toml` | Implementer | Planner | Planner-only routing and correction authority |
| Implementer custom agent | `.codex/agents/implementer.toml` | Implementer | Planner | Implementer scope and evidence-only commit boundary |
| Repo workflow | `plan/agent-handoff-workflow.md` | Plan-Creator | Planner | Canonical correction routing and Human stop boundary |
| Shared topic-plan contract | `plan/topic-plan-contract.md` | Plan-Creator | Planner | Parent/current-truth and correction-artifact contract |
| Plan-Creator skill | `.agents/skills/plan-creator/SKILL.md` | Implementer | Planner | Correction-aware authoring contract |
| Plan-Creator checklist | `.agents/skills/plan-creator/checklist.md` | Implementer | Planner | Correction-plan validation |
| Plan-Creator template | `.agents/skills/plan-creator/templates/topic-plan-template.md` | Implementer | Planner | Exact correction prompts |
| Plan-Reviewer skill | `.agents/skills/plan-reviewer/SKILL.md` | Implementer | Planner | Independent correction review protocol |
| Plan-Reviewer checklist | `.agents/skills/plan-reviewer/checklist.md` | Implementer | Planner | Correction review checks |
| Plan-Reviewer reference | `.agents/skills/plan-reviewer/reference.md` | Implementer | Planner | Current truth / retention / subject guidance |
| Plan-Reviewer examples | `.agents/skills/plan-reviewer/examples.md` | Implementer | Planner | Bounded high-correction examples |
| Python workflow | `.agents/skills/python-implementation-workflow/SKILL.md` | Implementer | Planner | Bounded workflow alignment |
| Python template | `.agents/skills/python-plan-authoring/templates/canonical-python-topic-plan-template.md` | Implementer | Planner | Bounded workflow alignment |
| Governance contract test | `tests/test_observer_dispatcher_governance_contract.py` | Implementer | Planner | Executable expanded-schema checks |
| Topic plan | `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md` | Plan-Creator | Planner | Parent current execution contract |
| Topic specification | `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md` | Plan-Creator | Planner | Parent current execution contract |
| Step tracker | `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md` | Plan-Creator | Planner | Parent current execution contract |
| Correction plan | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-plan.md` | Plan-Creator | Planner | Retained bounded correction delta |
| Correction step | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-step.md` | Plan-Creator | Planner | Retained bounded correction delta |
| Correction review log | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-review-log.md` | Plan-Reviewer | Plan-Reviewer verdict; Planner route | Required independent, pre-implementation correction-plan review |
| Correction Tester evidence | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-tester-evidence.md` | Tester | Tester factual result; Planner route | First evidence-only descendant |
| Correction implementation review | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-implementation-review-log.md` | Reviewer | Reviewer verdict; Planner route | Second/final evidence-only descendant |
| Frozen normal provenance | `plan/observer-dispatcher-governance/observer-dispatcher-governance.review-log.md` | Historical (no write) | None | Never current routing, Tester or Reviewer evidence |
| Frozen normal provenance | `plan/observer-dispatcher-governance/observer-dispatcher-governance.planning-review-evidence.md` | Historical (no write) | None | Never current routing, Tester or Reviewer evidence |
| Frozen normal provenance | `plan/observer-dispatcher-governance/observer-dispatcher-governance.tester-evidence.md` | Historical (no write) | None | Never current routing, Tester or Reviewer evidence |
| Frozen normal provenance | `plan/observer-dispatcher-governance/observer-dispatcher-governance.implementation-review-log.md` | Historical (no write) | None | Never current routing, Tester or Reviewer evidence |
| Frozen recovery provenance | `plan/observer-dispatcher-governance/observer-dispatcher-governance.recovery-planning-review-evidence.md` | Historical (no write) | None | Never current routing, Tester or Reviewer evidence |
| Frozen recovery provenance | `plan/observer-dispatcher-governance/observer-dispatcher-governance.recovery-tester-evidence.md` | Historical (no write) | None | Never current routing, Tester or Reviewer evidence |
| Frozen recovery provenance | `plan/observer-dispatcher-governance/observer-dispatcher-governance.recovery-implementation-review-log.md` | Historical (no write) | None | Never current routing, Tester or Reviewer evidence |

`README.md`、`VERSION`、`.github/copilot-instructions.md`、`.github/agents/**`、`src/**`、
docs、其他 tests 與 summary 均不在 write scope。未列 path 需先由 Planner 修復 parent plan。

## Implementation Steps

1. Implementer 對齊 `AGENTS.md`、兩份 custom-agent TOML、workflow / shared contract、
   列出的 Plan-Creator / Plan-Reviewer / Python surfaces，使其共用 expanded
   Observer / Dispatcher、high-correction、frozen-provenance 與 immutable-subject rules。
2. Implementer 新增 `tests/test_observer_dispatcher_governance_contract.py`，以 direct
   file-content assertions 驗證 exact paths、role separation、conditional artifacts、
   old-provenance exclusion、new subject reset 與 two-descendant invariant；不得替代
   existing direct-import regression tests。
3. Implementer 僅在 schema-complete approved `correction-review-log.md` 已先被原樣固化為
   evidence-only pre-implementation commit 後完成 declared scope；該 review-evidence commit
   不是 subject。其後唯一一個完成 declared implementation 的 non-merge commit 才建立
   replacement immutable `implementation_subject_sha`；不得寫 correction review / Tester /
   Reviewer evidence。

## Validation / Acceptance Checks

- All declared implementation surfaces use the same Planner-only authority, Human-only
  lifecycle, frozen `.github/agents/**`, high-correction and legacy-evidence semantics.
- `tests/test_observer_dispatcher_governance_contract.py` verifies exact roles/paths, five
  conditional correction artifacts, parent-current versus correction-historical truth,
  immutable subject reset and exactly two ordered post-subject evidence paths.
- New Tester state is `pending` until the new subject exists. Tester then records subject
  verification, exact command/results, the new test, repository validation, timestamp and
  `passing|failing`; no prior Tester record may satisfy this gate.
- `correction-review-log.md` is the schema-complete `correction-plan` review record defined in
  the shared contract. It lists exactly the seven planning artifacts and is written and committed
  as an evidence-only pre-implementation prerequisite; its commit is not the subject. Only
  `approved` authorizes implementation to start, after which the single non-merge declared
  implementation commit creates the replacement immutable `implementation_subject_sha`.
- The final reviewer record carries the same `S1` subject SHA, `T1` Tester path/revision/`passing`
  and shared reviewer fields. `git diff --name-status S1..V1` must be exactly the two new correction
  Tester / Reviewer evidence paths with no merge; `HEAD` is not an accepted verification endpoint.
- Parent sync and independent reviews must pass before correction resolution. Retain all
  correction artifacts; then stop, with no publish, PR action, merge, release, tag, summary
  or self-approval.

## Reviewer Handoff

Current correction pre-implementation gate:

- The sole correction-review record path is
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-review-log.md`.
  An independent Plan-Reviewer is its sole writer.
- Under the narrow `B0` exception and before any declared implementation path changes, the
  Plan-Reviewer must independently tree/blob review each of these seven **uncommitted** planning
  artifacts at one exact reviewed tree SHA:
  `plan/agent-handoff-workflow.md`, `plan/topic-plan-contract.md`,
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md`,
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md`,
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md`,
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-plan.md`, and
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-step.md`.
- The record must be a single schema-complete `correction-plan` JSON object with `reviewed_tree_sha`
  and exactly one path/blob revision per artifact, under
  `plan/topic-plan-contract.md#current-topic-correction-evidence-schemas`, with an `approved`
  verdict. Only an independent Implementer, under existing Human commit authorization, may commit
  that approved record unchanged together with the seven reviewed artifacts as `B0`; `B0` is not a
  subject, and implementation may begin only after that commit.

```json
{
  "reviewed_artifacts": [
    {
      "path": "<exact repo-visible path>",
      "revision": "<latest reviewed revision or head>"
    }
  ],
  "review_basis": "<independent review basis>",
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "copilot_feedback_triage": {
    "ADDRESS": [],
    "DISCUSS": [],
    "SKIP": []
  },
  "timestamp": "<RFC 3339 timestamp>"
}
```

Current correction evidence additionally uses the complete three-object schemas in
`plan/topic-plan-contract.md#current-topic-correction-evidence-schemas`; those schemas are the
authoritative field contract for correction review, Tester evidence and final implementation review.

## Post-merge / release actions

- No merge, release, VERSION bump, tag, post-merge sync, PR action or summary is authorized.
  The final correction implementation-review record is a terminal Human boundary; every
  later lifecycle action needs new explicit Human direction.

## Open Questions / Unresolved Items

- Correction review, replacement subject, new Tester evidence and new independent
  implementation review are pending. Existing evidence is frozen provenance and cannot
  answer those gates.
