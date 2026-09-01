---
topic: observer-dispatcher-governance
phase: pr-open
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
  追加固定 reviewer-handoff JSON object 作為最後 nonblank NDJSON line；verdict 僅以
  review log 為 authority，不在本 tracker 改寫。
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

- [X] 1. Implementer 已完成 PR #1 的 current draft；PR #1 維持 `pr-open` / Ready。
  Ready 不等同 independent implementation approval、human merge approval 或已 merge。
- [ ] 2. **Actor:** Tester — **Action:** 對 PR #1 current head 執行 declared checks，並
  先寫入
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.tester-evidence.md`。
  record 必須含 `pr_number`、`head_sha`、`actor: Tester`、每項 `command` / `result`
  與 `verdict: passing|failing`；目前沒有 evidence，故不可標記完成。
- [ ] 3. **Actor:** Reviewer — **Action:** 僅在同一 PR #1 head 的 Tester
  `verdict: passing` evidence 存在後，寫入
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.implementation-review-log.md`。
  record 必須 reference tester evidence，並獨立給出 `approved|needs-rework`、
  `blocking_issues` 及 `copilot_feedback_triage` verdict；目前沒有 independent verdict，
  故不可標記完成。
- [ ] 4. **Actor:** Reviewer — **Action:** 完成 step 2 與 3 的同-head evidence gate 後，
  處理 PR #1 已 addressed threads。此 reviewer-comments replan 為 pending；不得在
  evidence 前處理 threads，亦不得視 Ready 為 merge approval。

## Publish / Human Boundary

- [X] **Actor:** Implementer — **Action:** 已在既有 human authorization 下完成 bounded
  commit、push 並開啟 PR #1；PR #1 目前為 Ready 的 `pr-open`，非 merge approval。
- [ ] **Actor:** Human — **Action:** draft PR 開啟後執行 human review、merge、
  post-merge、release（若有）與 close summary；其他角色不得自行執行。

## Handoff / Gate Notes

- `plan-authoring`、planning artifact commit、independent `plan-review`、review
  evidence progression commit 與 Planner preflight 均已完成；preflight evidence 為 commit
  `490066f6753271181d289abdd593f119bd9ef48c`
  (`docs(governance): confirm observer plan preflight`)；此前歷史漏記在此作 bounded
  correction，且不要求重新執行 planning evidence 或 preflight。
- topic 的 current state 為 `pr-open`：PR #1 維持 Ready，但 Ready 不是 independent
  implementation approval、human merge approval 或已 merge。既有 step 對 Tester、
  Reviewer 及 Phase 4.5 的完成敘述並非 declared evidence，不可回填為完成。
- current corrective sequence 是 Tester first 寫入 passing evidence，Reviewer second
  reference 同一 PR head evidence 並給出 independent `approved|needs-rework` verdict，
  才可處理已 addressed threads；這個 reviewer-comments replan 以及兩份 evidence 均為
  pending。
- Plan-Reviewer 的 verdict 只存在 declared review log 的最後 nonblank NDJSON line，
  本 tracker 不重述或取代該 verdict。
- `GOAL.md` 不是 active topic 或 phase authority。routing 必須由 Planner 根據
  plan、required step tracker 與 review log 判定。
- `.github/agents/**` 是 frozen provenance；不得修改，亦不得作 runtime / routing
  dependency。
- `step-creator` role-model conflict 不屬本 topic；已 out-of-scope defer 至新 topic
  `step-creator-role-model-alignment`，不得重開既有 topic。
