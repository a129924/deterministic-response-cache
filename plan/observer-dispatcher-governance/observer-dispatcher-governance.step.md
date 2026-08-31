---
topic: observer-dispatcher-governance
phase: planning-artifact-commit
created: 2026-08-31
---

# observer-dispatcher-governance — Step Tracking

## Workflow Stages

- [X] plan-authoring
- [ ] planning-artifact-commit
- [ ] plan-review
- [ ] implementation
- [ ] testing
- [ ] code-review
- [ ] publish
- [ ] human-review

## Actionable Steps

- [X] **Actor:** Plan-Creator — **Action:** 建立 canonical plan、spec、step，並將
  locked Implementation Dispatch Manifest 放在 `Implementation Steps` 開頭，並完成
  workflow / shared-contract 的 bounded alignment；不得 commit。
- [ ] **Actor:** Implementer — **Action:** 在既有 human topic authorization 下，僅將
  `observer-dispatcher-governance.plan.md`、`.spec.md`、`.step.md`、
  `plan/agent-handoff-workflow.md` 與 `plan/topic-plan-contract.md` 建立為 planning
  artifact commit；不得夾帶 `AGENTS.md`、`GOAL.md` 或 implementation diff。完成後
  topic 才為 `planned` repo-visible contract。
- [ ] **Actor:** Plan-Reviewer — **Action:** 獨立審核已提交 planning baseline 的
  plan、spec、step、shared contract、scope、artifact path 與 workflow alignment；完成時
  在 `plan/observer-dispatcher-governance/observer-dispatcher-governance.review-log.md`
  追加固定 reviewer-handoff JSON object 作為最後 nonblank NDJSON line。
- [ ] **Actor:** Implementer — **Action:** 在 Planner preflight 前，於既有 human
  topic authorization 下建立 review-log-only evidence commit；不得夾帶 implementation
  diff。
- [ ] **Actor:** Planner — **Action:** 只讀 plan、required step tracker 與 review log
  作 preflight；latest JSON verdict 為 `approved` 才可 route `creator-in-progress`。

## Implementation Steps

- [ ] 1. Implementer 依 approved topic plan 修改 `AGENTS.md`、建立 `GOAL.md`，並
  保留既有 tests 的 direct-import 行為。
- [ ] 2. Tester 執行 declared repository checks，確認 allowed path set 與
  import-preservation compliance。
- [ ] 3. Reviewer 獨立審核 bounded implementation，並對 PR comments 做
  classification / routing；若通過，交由 Planner 做 Phase
  4.5 contract alignment。
- [ ] 4. Planner 在 implementation Reviewer `approved` 後執行 Phase 4.5；無 contract
  drift 時才 route `publish-in-progress`。

## Publish / Human Boundary

- [ ] **Actor:** Implementer — **Action:** 在 independent review、Planner Phase 4.5、
  Tester evidence 與既有 human authorization 都通過後，將已驗證 topic changes
  commit by topic、push 並開啟 draft PR。
- [ ] **Actor:** Human — **Action:** draft PR 開啟後執行 human review、merge、
  post-merge、release（若有）與 close summary；其他角色不得自行執行。

## Handoff / Gate Notes

- `plan-authoring` 已完成；下一個必經 gate 是 planning artifact commit。其完成前，
  topic 不是 `planned` repo-visible contract。
- Plan-Reviewer 的 verdict 必須以 declared review log 的最後 nonblank NDJSON line
  符合 `Reviewer Handoff` 固定 JSON object；在其 `approved` 前不得開始 implementation，
  且不得在 plan 自行加入 approval marker。
- `GOAL.md` 不是 active topic 或 phase authority。routing 必須由 Planner 根據
  plan、required step tracker 與 review log 判定。
- `.github/agents/**` 是 frozen provenance；不得修改，亦不得作 runtime / routing
  dependency。
