---
topic: model-response-codecs
correction: fix-2
phase: correction-plan-authoring
---

# model-response-codecs — correction fix-2 steps

## Frozen predecessor

- [X] 原 implementation subject `5d8873f3088769f1bd8b6da7b42d2ec96b9254f5`、passing Tester evidence commit `226b95b2a1c29c7f1103d8f4e11939c29a96f266`、Independent Reviewer needs-rework commit `57e4940150157d3cc73799c20461000eacc6bfe2` 已提交；兩個 code/test blockers 尚未修。
- [X] `fix-1` planning candidate `b51e557c535510c7660a4c17229ed1f0c008c4cf` 與 Plan-Reviewer needs-rework receipt sole commit `4d1a730783d5904f36f5a0a0a43cc69c578a9538` 已提交；`fix-1` 無 approved candidate、新 subject 或 Tester/Reviewer evidence。前述歷史不可覆寫或 route。

## Ordered correction checkpoints

- [X] **Plan-Creator:** 僅同步 parent plan/step 並建立 `fix-2` correction plan/step；parent `## Reviewer Handoff` 已改為 active `fix-2` extended JSON contract，原 substantive Implementation Steps 11–12 保留並改指 `fix-2` gate。
- [ ] **Implementer:** 只以 parent plan/step `M`、`fix-2` correction plan/step `A` 建 exact-four non-merge first-parent planning candidate；不混入 code/evidence。
- [ ] **Independent Plan-Reviewer:** 在 committed clean candidate 上審四份 planning artifacts；依 `fix-2` extended schema 寫 `plan/model-response-codecs/model-response-codecs.correction-fix-2-plan-review-log.json`，不自行 commit/route，不預填 commit/tree/blob/verdict。
- [ ] **Implementer／Planner:** Implementer 原樣 sole evidence-only commit 提交 receipt，其 direct parent 為 exact-four candidate；Planner 只在 actual Git binding 與 committed approved 成立時 route。Needs-rework 停回 Planner／Plan-Creator 另開新路徑，`fix-2` receipt immutable。
- [ ] **Implementer:** 只改 `src/deterministic_response_cache/response_reuse/codecs/json_response.py`、`tests/test_response_reuse_codecs.py`、`tests/test_model_response_codecs_integration.py`，完成 unsupported-tree reason 與五類 substantive edge assertions，保留 direct imports/fixtures，建新 exact-three immutable subject。
- [ ] **Tester:** 對新 subject 跑 pytest、pyright strict、ruff 及相關回歸；只寫 `plan/model-response-codecs/model-response-codecs.tester-evidence.fix-2.json`，記 actual command/exit code，不 commit。
- [ ] **Implementer:** 將 Tester evidence 原樣 sole one-path evidence-only commit；只有 committed passing 才能交 Independent Reviewer，failing 停回 Planner／Plan-Creator 另宣告新 evidence paths。
- [ ] **Independent Reviewer:** 僅消費新 subject 的 committed passing `fix-2` Tester evidence，重新審兩個 blocker、path exactness 與 contract drift，只寫 `plan/model-response-codecs/model-response-codecs.implementation-review-log.fix-2.json`，不 commit。
- [ ] **Implementer:** 將 Reviewer evidence 原樣 sole one-path evidence-only commit；needs-rework 停回 Planner／Plan-Creator 另宣告新路徑，本輪 evidence 不覆寫、不直接重跑，不能 Q/publish。
- [ ] **Planner／Implementer:** 只有新 committed approved Reviewer evidence、Planner Phase 4.5 alignment 與既有 Human authorization 具備，才 bounded push/open draft PR；停於 Human review/merge boundary。

## Parent sync / closure

- Parent plan/step 是 current truth；initial/fix-1 planning/evidence 只保留 immutable history，`fix-1` 未寫 evidence paths 保持 absent。新 candidate/subject/evidence SHA、tree、blob、verdict 均留待各 action 後據實記錄。
- 只有同一新 exact-three subject 的 passing Tester 與 approved Independent Reviewer evidence 均已提交、Planner Phase 4.5 完成，才可關閉原兩個 blockers。Human 獨占 PR review、merge、release、post-merge、tag 與 final summary。
