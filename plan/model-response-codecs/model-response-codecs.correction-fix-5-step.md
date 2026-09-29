---
topic: model-response-codecs
correction: fix-5
phase: correction-plan-authoring
---

# model-response-codecs — correction fix-5 steps

## Frozen predecessor / PR state

- [X] Fix-4 planning candidate、approved Plan-Reviewer receipt `5ff48411db917fded0ed8bcd8ced45b802e68ff1`、subject `9a0eef1845113801c4d250826df4e9a9dee09917`、passing Tester `2cef0406fb401be36563c247ff409bc7ed7dc44c`、approved Independent Reviewer `853628596f177896b09c72a25f1a9f3b6391be46` 與 published head `b66f77d6382b22b147e556e270e233a8abb62fe5` 保持 immutable。
- [X] PR #11 OPEN/Ready、base `dev`、head `b66f77d6382b22b147e556e270e233a8abb62fe5`；thread 1 resolved，2–4 unresolved。Human 已選 JSON 值比較與 DataFrame `.equals`。

## Ordered correction checkpoints

- [X] **Plan-Creator:** 只 M requirements/technical spec/parent plan/spec/step、A fix-5 plan/step；parent active handoff 指唯一 fix-5 extended receipt。既有 Implementation Steps 1–18 [X]，新 19–21 pending。
- [ ] **Implementer:** 以 `b66f77d6382b22b147e556e270e233a8abb62fe5` 為 first parent，提交 exact-seven non-merge planning candidate：五 M、兩 A，無 code/evidence。
- [ ] **Independent Plan-Reviewer:** clean committed candidate 審七個 actual blobs/first parent，依 fix-5 extended schema只寫 `plan/model-response-codecs/model-response-codecs.correction-fix-5-plan-review-log.json`，不 commit/route。
- [ ] **Implementer／Planner:** Implementer 原樣 sole one-path evidence-only commit receipt，direct parent 為 candidate；Planner 僅 route actual binding 的 committed approved。Needs-rework 停回新 bounded correction與新 evidence path。
- [ ] **Implementer:** 只改 fix-5 exact-six source/test paths：JSON lone surrogate decode → `InvalidPayload`、ModelResponse DataFrame `.equals`、JSON 值比較；補 codec/protocol/VO/outcome regressions，建新 immutable subject。
- [ ] **Tester:** 對新 subject 執行 pytest、pyright strict、ruff、JSON-only direct-import regression，僅寫 `plan/model-response-codecs/model-response-codecs.tester-evidence.fix-5.json` actual commands/exits，不 commit。
- [ ] **Implementer:** 原樣 sole evidence-only commit Tester record；failing 停回新 correction，僅 committed passing 同 subject 可交 Reviewer。
- [ ] **Independent Reviewer:** 只消費同 subject committed passing Tester evidence，核 JSON/DF equality、lone surrogate、optional import、scope 與既有 outcomes，僅寫 `plan/model-response-codecs/model-response-codecs.implementation-review-log.fix-5.json`，不 commit。
- [ ] **Implementer:** 原樣 sole evidence-only commit Reviewer record；needs-rework 停回 Planner/Plan-Creator 新 route/new evidence paths，不覆寫 fix-5 evidence。
- [ ] **Planner／Implementer:** 同 subject passing Tester/approved Reviewer evidence 均已提交且 Planner Phase 4.5 alignment 後，依既有 Human authorization bounded push/update Ready PR #11；未通過則不 publish。
- [ ] **Independent Reviewer／Planner:** 對更新後實際 PR head 逐一重新分類目前 unresolved threads 2–4，確認 exact thread identity 與 addressed-and-resolvable；未 addressed 者停回 Planner，新 head/CI 不自行關閉 thread。
- [ ] **Implementer／Human:** Implementer 只對 Reviewer 判 addressed-and-resolvable 的 exact thread 留 bounded reply 並 resolve；thread 1 保持歷史 resolved，不重處理。Human 獨占 PR approval、merge、release、post-merge、tag/final summary。

## Parent mirror / gate

- Parent `## Implementation Steps` 1–18 [X] 是 immutable work history；19–21 與 parent tracker逐字 mirror且 pending。fix-4 approved/published 不能替 fix-5 新 candidate/subject/evidence gate。
- 新 SHA、tree、blob、verdict、thread classification/closure 均只在 actual action 後記錄；chat、branch、PR state 或此 step 不能替代 committed gate evidence。
