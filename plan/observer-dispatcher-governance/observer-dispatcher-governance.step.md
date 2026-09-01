---
topic: observer-dispatcher-governance
phase: needs-rework
created: 2026-08-31
---

# observer-dispatcher-governance — Step Tracking

## Workflow Stages

- [X] plan-authoring
- [X] planning-artifact-commit
- [X] plan-review
- [X] implementation
- [ ] testing
- [ ] code-review
- [X] publish
- [ ] human-review
- [ ] bounded-rework

## Actionable Steps

- [X] **Actor:** Plan-Creator — **Action:** 建立 canonical plan、spec、step，並將
  locked Implementation Dispatch Manifest 放在 `Implementation Steps` 開頭，並完成
  workflow / shared-contract 的 bounded alignment；不得 commit。
- [X] **Actor:** Implementer — **Action:** 在既有 human topic authorization 下，僅將
  `observer-dispatcher-governance.plan.md`、`.spec.md`、`.step.md`、
  `plan/agent-handoff-workflow.md` 與 `plan/topic-plan-contract.md` 建立為 planning
  artifact commit；不得夾帶 `AGENTS.md`、`GOAL.md` 或 implementation diff。已由
  `dd6d5a7` (`docs(governance): establish observer dispatcher plan`) 完成；topic 現為
  `planned` repo-visible contract。
- [X] **Actor:** Plan-Reviewer — **Action:** 已獨立審核已提交 planning baseline 的
  plan、spec、step、shared contract、scope、artifact path 與 workflow alignment，並已在
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.review-log.md`
  留下 planning-review record。該既有 review log 是 frozen provenance；本 tracker 不
  重新解讀、遷移或以新的 prospective NDJSON policy 改變它的歷史 evidence meaning。
- [X] **Actor:** Implementer — **Action:** 已在既有 human topic authorization 下，將
  review log 與 progression update 固化為僅含 planning evidence 的 commit；未夾帶
  implementation diff。完成後交給 Planner preflight。
- [X] **Actor:** Planner — **Action:** 已在 committed plan、required step tracker 與
  review log evidence 存在後，只讀三者完成 preflight；latest JSON verdict 為
  `approved`，並已 route `creator-in-progress`。此 preflight 由 commit
  `490066f6753271181d289abdd593f119bd9ef48c`
  (`docs(governance): confirm observer plan preflight`) 證實；本回填不重跑 planning
  evidence 或 preflight。

## Implementation / Evidence Replan

- [ ] 1. **Actor:** Plan-Creator — **Action:** 在本次 Human authorization 下完成 latest
  prospective bounded replan，精確修改 current-topic
  `observer-dispatcher-governance.plan.md`、`.spec.md`、`.step.md`，以及
  `plan/agent-handoff-workflow.md`（Human-only / 不可委派 boundary wording）和
  `plan/topic-plan-contract.md`（future / new review-log prospective-only wording）；
  前二個 shared-contract 路徑與後三個 current-topic artifact 均屬已存在 diff 的 bounded
  repair，並由 Plan-Creator 負責。不得 commit、建立 evidence、遷移或修改任何 legacy
  review / evidence log、建立 reader / compatibility layer，或修改其他 topic。
- [ ] 2. **Actor:** Plan-Reviewer — **Action:** 僅在 step 1 latest replan 完成後，獨立寫入
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.planning-review-evidence.md`。
  該 path 必須只含一個完整 shared `Reviewer Handoff` machine-JSON record：
  `reviewed_artifacts` 恰好涵蓋 plan、spec、step、`plan/agent-handoff-workflow.md` 與
  `plan/topic-plan-contract.md` 的 latest revisions / head，並有 `review_basis`、
  `verdict: approved|needs-rework`、`blocking_issues`、完整 `copilot_feedback_triage`
  （`ADDRESS`、`DISCUSS`、`SKIP` arrays）及 RFC 3339 `timestamp`。只有 `approved` 才可
  進入 step 3；`needs-rework` 保持 current `needs-rework` status，且後續 replan 只能在
  Human 再授權下進行。frozen legacy `review-log.md` 不是此 replan 的 routing authority。
- [ ] 3. **Actor:** Implementer — **Action:** 僅在 step 2 對 latest replan 的 `approved`
  evidence 存在，且既有 Human authorization 仍有效時，commit / push replan，令 PR #1
  產生 new head。不得修改任何 legacy review / evidence log、建立 reader /
  compatibility layer，或修改其他 topic。
- [ ] 4. **Actor:** Tester — **Action:** 只對 step 3 的 PR #1 new head 執行 declared
  checks，並先寫入
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.tester-evidence.md`。
  record 必須含 `pr_number`、`head_sha`、`actor: Tester`、每項 `command` / `result`
  與 `verdict: passing|failing`；舊 head evidence 是 frozen provenance，不能完成 new-head
  gate，故此 step 不可標記完成。
- [ ] 5. **Actor:** Reviewer — **Action:** 僅在同一 PR #1 new head 的 Tester
  `verdict: passing` evidence 存在後，寫入
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.implementation-review-log.md`。
  record 必須 reference tester evidence，並完整符合 shared `Reviewer Handoff`：
  `reviewed_artifacts`（current PR head exact paths / revisions）、`review_basis`、
  `approved|needs-rework`、`blocking_issues`、完整 `copilot_feedback_triage` 及 RFC 3339
  `timestamp`；舊 head record 不能完成 new-head gate，故不可標記完成。
- [ ] 6. **Actor:** Reviewer — **Action:** 完成 step 4 與 5 的同-head evidence gate 後，
  處理 PR #1 已 addressed threads。此 reviewer-comments replan 為 pending；不得在
  evidence 前處理 threads，亦不得視 Ready 為 merge approval。

## Publish / Human Boundary

- [X] **Actor:** Implementer — **Action:** 已在既有 human authorization 下完成 bounded
  commit、push 並開啟 PR #1；PR #1 目前為 Ready 的 `pr-open`，非 merge approval。這是
  historical fact，不能替代 `needs-rework` 的 step 1。
- [ ] **Actor:** Human — **Action:** draft PR 開啟後執行 human review、merge、
  post-merge、release（若有）、tagging 與 final summary；這些 Human-only action 不可
  由重新授權委派，其他角色不得自行執行。

## Handoff / Gate Notes

- `plan-authoring`、planning artifact commit、independent `plan-review`、review
  evidence progression commit 與 Planner preflight 均已完成；preflight evidence 為 commit
  `490066f6753271181d289abdd593f119bd9ef48c`
  (`docs(governance): confirm observer plan preflight`)；此前歷史漏記在此作 bounded
  correction，且不要求重新執行 planning evidence 或 preflight。
- topic execution current state 為 `needs-rework`；PR #1 維持 Ready 的外部 `pr-open`
  fact，但 Ready 不是 independent implementation approval、merge approval 或已 merge。
  existing Tester / Reviewer evidence log 均對舊 head，並在 rework 後的新 same-head gate
  失效；本 tracker 不宣稱新的 Tester、Reviewer 或 Phase 4.5 completion。
- corrective sequence 是 Human-authorized Plan-Creator first 完成 prospective replan（本
  topic plan、spec、step，及 `plan/agent-handoff-workflow.md` 的 Human-only / 不可委派
  wording、`plan/topic-plan-contract.md` 的 future / new review-log prospective-only wording
  與 special evidence topology），independent Plan-Reviewer second 唯一寫入涵蓋五個 latest
  replan artifact revisions / head、完整 shared `Reviewer Handoff` schema 的 `approved`
  planning-review evidence，Implementer third 才 commit /
  push new head，Tester fourth
  寫入該 head 的 passing evidence，Reviewer fifth reference 同一 head evidence 並給出
  independent `approved|needs-rework` verdict，才可處理已 addressed threads。若 step 2
  verdict 為 `needs-rework`，topic 維持 `needs-rework` 且不得進入 commit 或 same-head
  gates；所有 future steps 均為 pending。
- existing `review-log.md` 與 implementation evidence logs 都是 frozen provenance；
  `review-log.md` 不具 current-replan routing authority。新的 planning-review evidence
  僅 prospective 適用於 latest replan；legacy policy、migration、reader 與 compatibility
  明確 defer 至 separate future topic。本 topic 不建立該 topic，也不修改其他 topic。
- `GOAL.md` 不是 active topic 或 phase authority。routing 必須由 Planner 根據
  plan、required step tracker 與 review log 判定。
- `.github/agents/**` 是 frozen provenance；不得修改，亦不得作 runtime / routing
  dependency。
- `step-creator` role-model conflict 不屬本 topic；已 out-of-scope defer 至新 topic
  `step-creator-role-model-alignment`，不得重開既有 topic。
