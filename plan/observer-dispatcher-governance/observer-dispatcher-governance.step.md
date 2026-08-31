---
topic: observer-dispatcher-governance
phase: publish-in-progress
created: 2026-08-31
---

# observer-dispatcher-governance — Step Tracking

## Workflow Stages

- [X] plan-authoring
- [X] planning-artifact-commit
- [X] plan-review
- [X] implementation
- [X] testing
- [X] code-review
- [ ] publish
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

## Implementation Steps

- [X] 1. Implementer 已依 approved topic plan 修改 `AGENTS.md`、建立 `GOAL.md`，並
  保留既有 tests 的 direct-import 行為。implementation diff 僅含這兩個 manifest
  允許的 paths；實作 authoring 已完成並交付獨立 Reviewer。
- [X] 2. Tester 已執行 declared repository checks，確認 allowed path set 與
  import-preservation compliance；所有 declared checks 均通過，且 worktree diff
  僅為 `AGENTS.md` 與 `GOAL.md`。
- [X] 3. Reviewer 已獨立審核 bounded implementation，並完成 review routing；latest
  implementation verdict 為 `approved`，故交由 Planner 做 Phase 4.5 contract
  alignment。
- [X] 4. Planner 已在 implementation Reviewer `approved` 後完成 Phase 4.5；確認無
  contract drift，並 route `publish-in-progress`。

## Publish / Human Boundary

- [ ] **Actor:** Implementer — **Action:** 在 independent review、Planner Phase 4.5、
  Tester evidence 與既有 human authorization 都通過後，將已驗證 topic changes
  commit by topic、push 並開啟 draft PR。
- [ ] **Actor:** Human — **Action:** draft PR 開啟後執行 human review、merge、
  post-merge、release（若有）與 close summary；其他角色不得自行執行。

## Handoff / Gate Notes

- `plan-authoring`、planning artifact commit、independent `plan-review`、review
  evidence progression commit 與 Planner preflight 均已完成；topic 現為
  `publish-in-progress`。preflight evidence 為 commit
  `490066f6753271181d289abdd593f119bd9ef48c`
  (`docs(governance): confirm observer plan preflight`)；此前歷史漏記在此作 bounded
  correction，且不要求重新執行 planning evidence 或 preflight。
- Implementer 已完成 bounded authoring，Tester 已完成 declared checks 並確認 allowed
  path set 與 direct-import preservation；independent implementation Reviewer 的 latest
  verdict 為 `approved`，且 Planner 已完成 Phase 4.5 contract alignment，確認無
  contract drift。故 topic 已真實轉為 `publish-in-progress`；下一關仍是 Implementer
  在既有 human authorization 下完成 bounded commit、push 與 draft PR。draft PR 尚未
  開啟，human review 仍為 pending。
- Plan-Reviewer 的 verdict 只存在 declared review log 的最後 nonblank NDJSON line，
  本 tracker 不重述或取代該 verdict。
- `GOAL.md` 不是 active topic 或 phase authority。routing 必須由 Planner 根據
  plan、required step tracker 與 review log 判定。
- `.github/agents/**` 是 frozen provenance；不得修改，亦不得作 runtime / routing
  dependency。
