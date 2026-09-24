# model-response-codecs — correction fix-2 plan

## Trigger / Evidence

原 implementation subject `5d8873f3088769f1bd8b6da7b42d2ec96b9254f5` 的 committed Independent Reviewer log `57e4940150157d3cc73799c20461000eacc6bfe2` 有兩個仍未修正的 blocker：已知 unsupported JSON tree 錯映為 `ENCODE_FAILURE`，以及五類 substantive edge assertions 不足。`fix-1` exact-four planning candidate `b51e557c535510c7660a4c17229ed1f0c008c4cf` 的 Independent Plan-Reviewer extended receipt 已由 sole commit `4d1a730783d5904f36f5a0a0a43cc69c578a9538` 提交，verdict `needs-rework`、`candidate.active=false`、`route_authorization=null`。其唯一 planning blocker 是 parent `## Reviewer Handoff` 仍指 normal initial 三鍵 JSON，與當輪 extended correction schema 矛盾。`fix-1` 沒有取得實作授權，沒有新 implementation subject 或 Tester/Reviewer evidence。

本輪只修 planning handoff 對齊，並保留原兩個 code/test blockers 作未來 exact-three repair；Goal、analysis/spec、BC、Arrow IPC、`DataFrame.equals`、optional extra、outcome 集合、archify 均不變。上述已提交 candidate、receipt、subject/evidence 是 immutable nonrouting provenance；不得覆寫或以 passing Tester 代替 Reviewer approval。

## Scope / exact paths

- **Planning candidate（exact four，non-merge first-parent）:** **Modify** `plan/model-response-codecs/model-response-codecs.plan.md`、`plan/model-response-codecs/model-response-codecs.step.md`；**Add** 本檔及 `plan/model-response-codecs/model-response-codecs.correction-fix-2-step.md`。Implementer 只提交此四檔，first parent 必須是已提交 `fix-1` needs-rework receipt sole commit `4d1a730783d5904f36f5a0a0a43cc69c578a9538`。Plan-Creator 不 commit。
- **Future implementation subject（exact three，全部 Modify）:** `src/deterministic_response_cache/response_reuse/codecs/json_response.py`、`tests/test_response_reuse_codecs.py`、`tests/test_model_response_codecs_integration.py`。僅在 `fix-2` committed approved Plan-Reviewer receipt 經 Planner route 後，由 Implementer 建新 immutable subject；不得改 selector/protocol、其他 source/test/docs/archify。
- **Read-only / absent:** 原 requirements、technical spec、parent spec、initial/fix-1 planning artifacts 與所有已提交 receipt/evidence 均 read-only。`fix-1` Tester/Reviewer evidence paths 從未建立，保持 absent。沒有檔案刪除或其他 topic 變更。

## What stays current / what changes

- Parent plan/spec 的已確認功能與行為契約維持 current truth；原 implementation Reviewer 的兩個 blocker 仍是唯一 future code/test repair。`fix-1` artifacts 與 receipt 只證明上一輪 planning review 的 `needs-rework`，不能 route。
- Parent plan 的 `## Reviewer Handoff` 此輪須以**active `fix-2` extended JSON receipt path 與本檔 schema**為唯一 handoff contract，明列 receipt 的 extended top-level keys；實際 receipt 須在審 committed candidate 後才填 `correction_id: "fix-2"`、candidate/tree/blobs/first-parent facts、verdict/blockers/Copilot triage 與 conditional route authorization。Initial normal 三鍵和 `fix-1` extended receipt 僅留在 Evidence/History 說明，不得仍作當輪 handoff。
- Parent plan/step 將當前 phase、exact-four candidate、五個新 correction artifacts、pending Implementation Steps 11–12 和 gate 改指 `fix-2`；原 1–10 `[X]` 與舊 subject/evidence SHA/verdict 保留，11–12 只改 route/path 指向，實質 repair 不擴張。
- 實作 delta 仍是：已知非字串 key、非有限值、tuple/custom/nested loss 等 unsupported JSON tree 丟 `UnsupportedPayloadError`，使 record 回 `NotCached(UNSUPPORTED_PAYLOAD)` 且不寫 Store；真正 serializer failure 保持 `EncodeFailureError` → `NotCached(ENCODE_FAILURE)`。兩個 codec tests 補 protocol unsupported-tree reason、empty DataFrame、optional DataFrame codec unavailable record、encoder failure、foreign malformed envelope 的 substantive assertions；保留 direct imports、fixtures/mocks 和可沿用 assertion。

## Conditional correction artifact contract

| Artifact | Exact path | Sole writer | Authority / order |
| --- | --- | --- | --- |
| Parent plan sync | `plan/model-response-codecs/model-response-codecs.plan.md` | Plan-Creator | Current topic contract；candidate path #1 |
| Parent step sync | `plan/model-response-codecs/model-response-codecs.step.md` | Plan-Creator | Current progression truth；candidate path #2 |
| `fix-2` correction plan | `plan/model-response-codecs/model-response-codecs.correction-fix-2-plan.md` | Plan-Creator | 本輪 scope/schema authority；candidate path #3 |
| `fix-2` correction step | `plan/model-response-codecs/model-response-codecs.correction-fix-2-step.md` | Plan-Creator | Ordered checkpoints；candidate path #4 |
| `fix-2` extended Plan-Reviewer receipt | `plan/model-response-codecs/model-response-codecs.correction-fix-2-plan-review-log.json` | Independent Plan-Reviewer | 只審 committed exact-four candidate 後寫；Implementer 原樣 sole one-path evidence-only commit；Planner 只 route committed approved |
| `fix-2` Tester evidence | `plan/model-response-codecs/model-response-codecs.tester-evidence.fix-2.json` | Tester | 新 exact-three immutable subject 後寫 actual commands/exit codes；Implementer 原樣 sole one-path evidence-only commit |
| `fix-2` implementation review | `plan/model-response-codecs/model-response-codecs.implementation-review-log.fix-2.json` | Independent Reviewer | 只消費 committed passing 同 subject `fix-2` Tester evidence；Implementer 原樣 sole one-path evidence-only commit |

新 candidate/subject/evidence 的 SHA、tree、blob、HEAD 與 verdict 都是未來 post-commit facts；本 plan、step 與 parent handoff 的 schema template 不填實際結果。未列 path、scope drift、非 sole evidence commit 或 first-parent mismatch 均停回 Planner。

## Active extended Plan-Reviewer receipt schema

Independent Plan-Reviewer 只可在 committed clean exact-four `fix-2` candidate 上寫**一個** JSON object。Top-level keys 恰為 `schema_version`、`topic`、`correction_id`、`candidate`、`reviewed_artifacts`、`first_parent_admission`、`review_basis`、`verdict`、`blocking_issues`、`copilot_feedback_triage`、`route_authorization`、`recorded_by`：

- `schema_version` 是 integer `1`；`topic` 為 `model-response-codecs`；`correction_id` 為 `fix-2`；`recorded_by` 為 `Independent Plan-Reviewer`。
- `candidate` 恰有 `commit_sha`、`tree_sha`、`active`；SHAs 為 actual candidate full lowercase 40-hex，`active` 僅 approved 為 `true`、needs-rework 為 `false`。
- `reviewed_artifacts` 恰四個 object，每項恰有 `path`、`blob_sha`；paths 恰為本輪 parent plan/step、fix-2 correction plan/step，blob 為 candidate tree 中的 actual full lowercase 40-hex。
- `first_parent_admission` 恰有 `parent_sha`、`non_merge`、`name_status`；parent 必為 `4d1a730783d5904f36f5a0a0a43cc69c578a9538`；`non_merge: true`；`name_status` 恰四個 `{status,path}`，按 actual Git name-status lexical order，parent plan/step `M`、fix-2 plan/step `A`，無其他 path。
- `review_basis` 恰有 `workflow_contract`、`topic_plan_contract`、`checkout`；前兩者分別是 `plan/agent-handoff-workflow.md`、`plan/topic-plan-contract.md`，checkout 是 actual clean candidate full SHA。
- `verdict` 是 `approved|needs-rework`；`blocking_issues` 是 `{issue,file,fix}` object array，approved 時空、needs-rework 至少一項。`copilot_feedback_triage` 恰有 `ADDRESS`／`DISCUSS`／`SKIP` arrays，各 entry 分別恰為 `{comment,location,why}`、`{comment,optional,why}`、`{comment,why}`；無 feedback 則空。
- `route_authorization` 只在 approved 為恰含 `next_phase: "creator-in-progress"`、`next_role: "Implementer"`、`scope: "fix-2-exact-three-subject"` 的 object；needs-rework 必為 `null`，無 active candidate、next phase、subject 或 close authorization。

Independent Plan-Reviewer 唯一寫此 receipt，不 commit 或 route。Implementer 原樣以 sole one-path evidence-only commit 提交，direct parent 必須是 exact-four candidate；Planner 驗證實際 Git tree/blob/parent/diff 與內容後，僅 committed approved 可 route。若 needs-rework，保留此 receipt immutable，停回 Planner／Plan-Creator 開下一輪新 artifact/evidence paths，不覆寫本 path。

## Tester / Independent Reviewer evidence schemas

- Tester `fix-2` evidence 為單一 JSON object，top-level keys 恰為 `schema_version`、`topic`、`correction_id`、`implementation_subject_commit`、`status`、`commands`、`recorded_by`。固定 `schema_version: 1`、`topic: "model-response-codecs"`、`correction_id: "fix-2"`、`recorded_by: "Tester"`；subject 是新 exact-three non-merge implementation commit 的 full lowercase 40-hex。`commands` 為 nonempty array，每項恰有 nonempty string `command` 與 integer `exit_code`；`passing` 只在全部 exit_code 0，`failing` 至少一個非零。Tester 寫後由 Implementer 原樣 sole one-path evidence-only commit。
- Independent Reviewer `fix-2` evidence 為單一 JSON object，top-level keys 恰為 `schema_version`、`topic`、`correction_id`、`implementation_subject_commit`、`tester_evidence_commit`、`verdict`、`blocking_issues`、`recorded_by`。固定 `schema_version: 1`、同 topic/id、`recorded_by: "Independent Reviewer"`；subject 與 Tester 相同 full SHA，`tester_evidence_commit` 是同 subject、已提交 passing、sole evidence-only commit full lowercase 40-hex；`verdict: approved|needs-rework`，approved 時 blockers 為空 string array，needs-rework 至少一項。Reviewer 只在 committed passing Tester evidence 後寫；Implementer 原樣 sole one-path evidence-only commit。
- 兩份新 evidence 不與 code、planning artifact、彼此或初始/fix-1 evidence 共用 commit。Tester failing 或 Reviewer needs-rework 均停回 Planner／Plan-Creator 另宣告下一輪 bounded correction 與新 evidence paths；已提交的 fix-2 evidence immutable，不覆寫或重用。

## Parent sync / retention / closure

Parent plan/step 的 active handoff、status、paths、steps 與 gates 在 exact-four candidate 內同步；本檔／correction step 保留本輪歷史 trigger，不取代 parent current truth。只有新 exact-three subject、同 subject committed passing Tester evidence、committed approved Independent Reviewer evidence 與 Planner Phase 4.5 alignment 都成立，才可視本輪 blocker 關閉並依既有 Human authorization 進 bounded push/draft PR。Human 獨占 PR review、merge、release、post-merge、tag、final summary。
