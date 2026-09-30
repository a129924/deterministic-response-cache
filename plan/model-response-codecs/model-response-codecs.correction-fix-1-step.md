---
topic: model-response-codecs
correction: fix-1
phase: correction-plan-authoring
---

# model-response-codecs — correction fix-1 steps

## Frozen predecessor

- [X] 原 immutable subject `5d8873f3088769f1bd8b6da7b42d2ec96b9254f5` 已有 committed passing Tester evidence `226b95b2a1c29c7f1103d8f4e11939c29a96f266`。
- [X] Independent Reviewer 的 committed `needs-rework` evidence `57e4940150157d3cc73799c20461000eacc6bfe2` 已指出兩個 blocker；舊三份 evidence 均只保留 provenance，不可覆寫或重用。

## Ordered correction checkpoints

- [X] **Plan-Creator:** 只同步 parent plan/step，並建立本 correction plan/step；將 JSON reason 分類及五類缺口鎖定為 exact-three code/test repair。
- [ ] **Implementer:** 只提交四份 planning paths 的 non-merge、first-parent candidate；exact named diff 是 parent plan/step `M`、correction plan/step `A`。
- [ ] **Independent Plan-Reviewer:** 只從 committed clean candidate 審四份 planning artifacts，依 correction plan 的 extended schema 寫 `plan/model-response-codecs/model-response-codecs.correction-fix-1-plan-review-log.json`；不自行 commit/route，不預填 candidate facts/verdict。
- [ ] **Implementer／Planner:** Implementer 原樣 sole evidence-only commit 提交 extended receipt；Planner 只在 actual Git binding 與 committed `approved` 成立時 route exact-three implementation。若 `needs-rework`，停回 Planner／Plan-Creator 另開 bounded correction route 與新 evidence path；本輪 receipt 不覆寫。
- [ ] **Implementer:** 只改 `src/deterministic_response_cache/response_reuse/codecs/json_response.py`、`tests/test_response_reuse_codecs.py`、`tests/test_model_response_codecs_integration.py`，使 known unsupported JSON tree 回 `UNSUPPORTED_PAYLOAD`、真正 serializer failure 回 `ENCODE_FAILURE`，補 substantive edge tests，建新 immutable exact-three subject。
- [ ] **Tester:** 對新 subject 跑 pytest、pyright strict、ruff 與宣告的 relevant regression；只寫 `plan/model-response-codecs/model-response-codecs.tester-evidence.fix-1.json`，記實際 commands/exit codes，不 commit。
- [ ] **Implementer:** 將 Tester evidence 原樣 sole evidence-only commit；若非 committed passing，同 subject Reviewer 不得開始。
- [ ] **Independent Reviewer:** 只消費新 subject 與其 committed passing `fix-1` Tester evidence，審兩個 blocker、contract/path drift，寫 `plan/model-response-codecs/model-response-codecs.implementation-review-log.fix-1.json`，不 commit。
- [ ] **Implementer:** 將 Reviewer evidence 原樣 sole evidence-only commit；若 Tester `failing` 或 Reviewer `needs-rework`，停回 Planner／Plan-Creator 另開 bounded correction route，先宣告新 evidence paths，再由 Implementer 建新 subject 並重跑 Tester/Reviewer；本輪 `fix-1` evidence 保持 immutable，不能 Q/publish。
- [ ] **Planner／Implementer:** 僅在新 committed `approved` evidence 與 Phase 4.5 alignment、既有 Human authorization 俱全時，Implementer bounded push/open draft PR；停於 Human review/merge boundary。

## Parent sync / closure

- Parent plan/step 在本 candidate 保有最新 scope、path allowlist、pending 11–12 與 workflow state；原 analysis/spec 不改。新 subject、Tester/Reviewer evidence 的 full SHA/verdict 均留待各自完成後據實記錄，不在此預填。
- correction artifacts 是本輪歷史記錄，不得代替 parent current truth；只有新 exact-three subject 的 passing Tester 與 approved Independent Reviewer evidence 都已提交、Planner 完成 Phase 4.5，才可判定本輪 blocker 關閉。任何本輪 `needs-rework`／`failing` 都不使用相同 Add evidence paths 重試。Human 獨占 PR review、merge、release、post-merge、tag 與 final summary。
