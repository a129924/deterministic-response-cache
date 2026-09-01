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
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.recovery-planning-review-evidence.md`。
  該 path 必須只含一個完整 shared `Reviewer Handoff` machine-JSON record，且
  `reviewed_artifacts` 恰好涵蓋 plan、spec、step、`plan/agent-handoff-workflow.md` 與
  `plan/topic-plan-contract.md` 的 latest revisions。`needs-rework` 保持 current
  `needs-rework` status，後續 replan 只能等待新的 Human authorization。
- [ ] 3. **Actor:** Independent Implementer — **Action:** 僅在 step 2 為 `approved` 時，
  建立唯一 planning-evidence commit，固化 step 1 的五個 replan artifacts 與 recovery
  planning-review evidence。此 commit SHA 是 immutable `implementation_subject_sha`；不得
  push、修改 legacy evidence、修改其他 topic、建立新 PR head、處理 threads 或執行任何
  human-only lifecycle action。
- [ ] 4. **Actor:** Tester -> Independent Implementer — **Action:** Tester 僅對 immutable
  `implementation_subject_sha` 執行 declared checks，並寫入
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.recovery-tester-evidence.md`。
  record 必須含相同完整 subject SHA、`actor: Tester`、每項 `command` / `result`、subject
  verification、RFC 3339 timestamp 與 `verdict: passing|failing`。若固化，Implementer 只能
  建立此單一路徑的 evidence-only child commit；不得 push 或夾帶其他 path。
- [ ] 5. **Actor:** Reviewer -> Independent Implementer — **Action:** 僅在 step 4 對相同
  subject 有 `passing` record 時，Reviewer 寫入
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.recovery-implementation-review-log.md`。
  JSON 必須含相同 `implementation_subject_sha`、Tester path / revision / passing verdict，及
  完整 shared `Reviewer Handoff` fields。若固化，Implementer 只能建立此單一路徑的第二個
  evidence-only linear child commit；最後以 `git diff --name-status
  <implementation_subject_sha>..HEAD` 驗證恰好兩個 recovery implementation evidence paths
  且 range 無 merge。此步完成後停止；不得 push、處理 threads、merge、post-merge、release、
  tagging 或 final summary。

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
  `df137326363cce4f68e43124156731a50cf29a03` 的 planning-review、Tester 與 Reviewer
  evidence 都是 frozen, superseded provenance；本 tracker 不宣稱新的 Tester、Reviewer
  或 Phase 4.5 completion。
- corrective sequence 是 Human-authorized Plan-Creator first 完成 exact five-path replan，
  independent Plan-Reviewer second 寫入 recovery planning-review JSON，independent
  Implementer third 建立唯一 planning-evidence commit。該 commit 是 immutable
  `implementation_subject_sha`。Tester fourth attest subject 並只能產生第一個
  evidence-only descendant；Reviewer fifth reference passing Tester record、attest 同一
  subject，並只能產生第二個 evidence-only descendant。最終 range 必須無 merge，且
  `git diff --name-status <implementation_subject_sha>..HEAD` 恰好只有兩個 recovery
  implementation evidence paths。若 step 2 `needs-rework`，維持 `needs-rework`；所有
  future steps 均 pending。
- 此 recovery sequence 到 step 5 即停止：不 push、建立新 PR head、處理 threads、merge、
  post-merge、release、tagging 或 final summary。legacy policy、migration、reader 與
  compatibility 維持 defer；本 topic 不修改其他 topic。
- `GOAL.md` 不是 active topic 或 phase authority。routing 必須由 Planner 根據
  plan、required step tracker 與 review log 判定。
- `.github/agents/**` 是 frozen provenance；不得修改，亦不得作 runtime / routing
  dependency。
- `step-creator` role-model conflict 不屬本 topic；已 out-of-scope defer 至新 topic
  `step-creator-role-model-alignment`，不得重開既有 topic。
