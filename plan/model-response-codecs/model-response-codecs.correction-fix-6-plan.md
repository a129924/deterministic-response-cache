# model-response-codecs — correction fix-6 plan

## Trigger / bounded goal

截至 committed HEAD `66de1646462e9fc0d978e1a986fcb928f752cf38`，fix-5 已有 exact-seven planning candidate `ea38d4404e5509047d5d3c20acdbdfad0ec5a049`、approved Plan-Reviewer receipt sole commit `fc1524c91f7d1d5d663bdbbe958aa66cbff8f480`、immutable implementation subject `a6e5db20005c55f2c10a978001f0c0380811c2da`、passing Tester evidence sole commit `8a1689c62407f7929bf9cb7f905964d549d8512a`、approved Independent Reviewer evidence sole commit `66de1646462e9fc0d978e1a986fcb928f752cf38`，parent Implementation Steps 1–21 已完成。Parent plan/step 仍把 fix-5 寫成 plan authoring、evidence 尚未產生，阻斷 Planner Phase 4.5 alignment。

本 correction 只同步 canonical planning status 與 handoff。fix-5 的 Q chain、Goal、Response Reuse BC/Identity/Store 邊界、公開 VO/codec/outcome、Arrow IPC、DataFrame.equals、optional imports、archify、已提交 subject/evidence 均不變。截至上述 HEAD，PR #11 為 OPEN/Ready，remote head `b66f77d6382b22b147e556e270e233a8abb62fe5`；任何後續 phase、head 與 thread 狀態均以 Planner 當下 committed evidence、Git 與 live PR 核對為準。本輪 live thread 查詢未成功，不能預判目前 thread identity 或 resolution。

## Exact paths / ownership

| Artifact | Exact path / action | Sole author | Authority |
| --- | --- | --- | --- |
| Parent plan | `plan/model-response-codecs/model-response-codecs.plan.md` **Modify** | Plan-Creator | 同步 Current、Written/Modify、active handoff 與 gate 文字 |
| Parent step | `plan/model-response-codecs/model-response-codecs.step.md` **Modify** | Plan-Creator | 五個 fix-5 Actionable rows 完成標記、frontmatter/Handoff/Gate 同步；Implementation Steps 1–21 原文不變 |
| Fix-6 correction plan | `plan/model-response-codecs/model-response-codecs.correction-fix-6-plan.md` **Add** | Plan-Creator | 本輪 exact-four scope 與 receipt schema |
| Fix-6 correction step | `plan/model-response-codecs/model-response-codecs.correction-fix-6-step.md` **Add** | Plan-Creator | 本輪 status gate checkpoints |
| Fix-6 Plan-Reviewer receipt | `plan/model-response-codecs/model-response-codecs.correction-fix-6-plan-review-log.json` **Add, after committed candidate only** | Independent Plan-Reviewer | 唯一 active extended receipt；Implementer 原樣 sole one-path evidence-only commit |

Plan-Creator 只 author 上述前四檔；Implementer 只可將這四檔作一個 non-merge exact-four planning candidate commit，first parent 必須是 `66de1646462e9fc0d978e1a986fcb928f752cf38`。新 receipt path 在 authoring 時不存在。Analysis、spec、code、tests、docs/archify、fix-5/更早 planning 與全部舊 evidence 均 read-only；本 correction 不建立新 implementation subject、Tester evidence 或 Independent Reviewer evidence，也不增 code Implementation Steps。若須第五 planning path 或新產品決策，停回 Planner。

## Active extended Plan-Reviewer receipt schema

Independent Plan-Reviewer 僅於 exact-four candidate 已提交且 clean 時寫一個 JSON object，top-level keys **恰為** `schema_version`, `topic`, `correction_id`, `candidate`, `reviewed_artifacts`, `first_parent_admission`, `review_basis`, `verdict`, `blocking_issues`, `copilot_feedback_triage`, `route_authorization`, `recorded_by`，共十二鍵。

- `schema_version` 為 integer `1`；`topic` 為 `model-response-codecs`；`correction_id` 為 `fix-6`；`recorded_by` 為 `Independent Plan-Reviewer`。
- `candidate` 恰為 `{commit_sha,tree_sha,active}`，SHA 為 actual full lowercase 40-hex；僅 approved 時 `active: true`，needs-rework 時 false。
- `reviewed_artifacts` 恰有四個 `{path,blob_sha}`，對應上表前四個 exact paths，blob SHA 皆為 actual full lowercase 40-hex。
- `first_parent_admission` 恰為 `{parent_sha,non_merge,name_status}`；`parent_sha` 必為 `66de1646462e9fc0d978e1a986fcb928f752cf38`，`non_merge: true`；`name_status` 恰有四個 `{status,path}`，依 actual Git lexical order，兩 M、兩 A，無其他路徑。
- `review_basis` 恰為 `{workflow_contract,topic_plan_contract,checkout}`，前兩者分別是 `plan/agent-handoff-workflow.md`、`plan/topic-plan-contract.md`，checkout 為 actual clean candidate full SHA。
- `verdict` 只能 `approved|needs-rework`；`blocking_issues` 為 `{issue,file,fix}` array，approved 為空、needs-rework 至少一項；`copilot_feedback_triage` 恰為 `{ADDRESS,DISCUSS,SKIP}` arrays，各項依既有 Plan-Reviewer contract 的欄位，無 feedback 時為空 array。
- `route_authorization` 在 approved 時恰為 `{next_phase:"phase-4.5-recheck",scope:"existing-fix-5-Q-chain-only"}`，只容許 Planner 依已提交 fix-5 subject/Tester/Reviewer evidence 重做 Phase 4.5 alignment；它不授權新 subject、重跑 Tester/Reviewer、push、thread resolve 或 Human approval。Needs-rework 時為 `null`，無 active candidate 或下一 phase authority。

Plan-Reviewer 不 commit、不 route。Implementer 原樣只提交此 receipt 一個 path 的 sole evidence-only commit，其 direct parent 必須是 exact-four candidate。Planner 核對 actual parent/tree/blob/name-status 與 committed approved receipt 後，才重核既有 fix-5 Phase 4.5；若 alignment 通過且既有 Human authorization 有效，才可另派 bounded push 更新 PR #11，並於新 remote head 後交 Independent Reviewer 分類 still-open exact threads。任何 needs-rework 都停回 Planner/Plan-Creator 建下一輪新 paths，不覆寫 fix-6 receipt。Human 保有 PR review/merge/release/post-merge 權限。

## Review input / acceptance

本輪 Plan-Reviewer review-input allowlist 僅上述 exact-four planning artifacts、`plan/agent-handoff-workflow.md`、`plan/topic-plan-contract.md`、`.agents/skills/plan-creator/SKILL.md`、`.agents/skills/plan-reviewer/SKILL.md`、committed fix-5 candidate/receipt/subject/Tester/Reviewer evidence 與其 Git binding，以及已記錄的 feedback（若有）。需檢查 parent plan 與 step 的 fix-5 chain/21 個完成 marker、active fix-6 handoff、舊 evidence immutable、fix-5 publish/thread tail pending 與沒有 code scope 擴張。PR live facts 只作 Planner 後續 recheck，不能取代 receipt 或 Q evidence。
