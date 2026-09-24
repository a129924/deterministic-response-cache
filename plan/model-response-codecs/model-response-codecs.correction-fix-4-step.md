---
topic: model-response-codecs
correction: fix-4
phase: correction-plan-authoring
---

# model-response-codecs — correction fix-4 steps

## Frozen predecessor

- [X] Fix-3 candidate `c67f5c23bc2b6f3a6cb1f6b8e883b9ee77a561d1`、approved Plan-Reviewer sole commit `4389ddc5b83c65ae4e08976c7e270c567ebdec7b`、subject `b9a68575b24472a136bc7f3b826c8e7e581250b2`、passing Tester sole commit `2ff945e236aaa76afce61dbac1df62fc860f45c7`、Independent Reviewer needs-rework sole commit `dff896ce0548c8d9c8ae36cabbe60792c9211225` 均已提交，絕不覆寫。
- [X] Reviewer 唯一 blocker 是 parseable 深層 JSON 在 `_valid_json_tree` 噴 `RecursionError`，而非回 `InvalidPayload`／對外 `Unavailable(INVALID_PAYLOAD)`。Draft PR #11 OPEN base `dev`；舊 evidence 不授權 fix-4。

## Ordered checkpoints

- [X] **Plan-Creator:** 只修改 parent plan/step、新增本 fix-4 plan/step；原 spec/analysis 不修改。Parent active Reviewer Handoff 指唯一 fix-4 extended receipt，1–16 歷史 steps [X]，17–18 pending。
- [ ] **Implementer:** 以 `dff896ce0548c8d9c8ae36cabbe60792c9211225` 為 first parent 只提交 exact-four non-merge planning candidate：parent plan/step M、本 fix-4 plan/step A。
- [ ] **Independent Plan-Reviewer:** 清潔 committed candidate 上核對四份 actual blobs/first parent，依 fix-4 extended schema 只寫 `plan/model-response-codecs/model-response-codecs.correction-fix-4-plan-review-log.json`，不 commit/route。
- [ ] **Implementer／Planner:** Implementer 原樣 sole one-path evidence-only commit receipt、direct parent 為 candidate；Planner 僅 route actual binding 的 committed approved。Needs-rework 停回新 bounded correction，不覆寫此 receipt。
- [ ] **Implementer:** 僅修改 `json_response.py` 與三個 declared tests，讓 parseable 深層 JSON decode 回 `InvalidPayload`，新增直接 codec 與 protocol regression；不改 selector/protocol、外部 reasons 或其他 code。只建 exact-four immutable subject。
- [ ] **Tester:** 對新 subject 寫 `plan/model-response-codecs/model-response-codecs.tester-evidence.fix-4.json` factual commands/exit codes，不 commit。
- [ ] **Implementer:** 原樣 sole evidence-only commit Tester evidence；failing 停回新 correction，只有 committed passing 同 subject 可交 Reviewer。
- [ ] **Independent Reviewer:** 只消費 committed passing 同 subject Tester evidence，審 blocker/scope/exception boundary；只寫 `plan/model-response-codecs/model-response-codecs.implementation-review-log.fix-4.json`，不 commit。
- [ ] **Implementer:** 原樣 sole evidence-only commit Reviewer evidence；needs-rework 停回 Planner/Plan-Creator 新 route/new evidence paths，不覆寫 fix-4 evidence。
- [ ] **Planner／Implementer:** 僅在同 subject passing Tester、approved Reviewer evidence 已提交及 Planner Phase 4.5 alignment 後，bounded push/update Draft PR #11；Human 獨占 PR review/merge。

## Parent mirror / gate

- Parent `## Implementation Steps` 1–16 [X] 是歷史，不因 fix-3 needs-rework 改標；17–18 與 parent step 逐字 mirror 且保持 pending。
- 新 candidate/subject/evidence SHA、tree/blob/verdict 均留待 actual actions；本 step、chat、branch 或 PR state 不是 gate evidence。
