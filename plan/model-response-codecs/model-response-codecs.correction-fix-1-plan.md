# model-response-codecs — correction fix-1 plan

## Trigger / Evidence

Immutable implementation subject `5d8873f3088769f1bd8b6da7b42d2ec96b9254f5` 的 Tester evidence sole commit `226b95b2a1c29c7f1103d8f4e11939c29a96f266` 記錄 passing；Independent Reviewer 的 committed `needs-rework` log 是 `plan/model-response-codecs/model-response-codecs.implementation-review-log.json`，sole commit `57e4940150157d3cc73799c20461000eacc6bfe2`。該 log 指出兩個阻礙：

1. `json_response.py` 將非字串 dict key、非有限值、tuple 等已知不支援 JSON 樹當 `EncodeFailureError`，使 protocol 回 `NotCached(ENCODE_FAILURE)`；核准契約要求 `UNSUPPORTED_PAYLOAD`。
2. 既有 codec tests 缺 protocol-level unsupported-tree reason、empty DataFrame、DataFrame record 的 optional codec unavailable、真正 encoder failure 映射及 foreign malformed envelope 的 substantive assertions。

此 correction 是同一 Mission 的 bounded rework；上述舊 evidence 為 immutable nonrouting provenance，不得覆寫、取消或宣稱其 passing 已解 Reviewer blockers。

## Scope

- **Planning candidate named diff（exact four）:** 修改 `plan/model-response-codecs/model-response-codecs.plan.md`、`plan/model-response-codecs/model-response-codecs.step.md`；新增本檔及 `plan/model-response-codecs/model-response-codecs.correction-fix-1-step.md`。由 Implementer 在 Plan-Creator 完成後以單一 non-merge、first-parent commit 提交；無其他 path。
- **Correction implementation subject named diff（exact three，全部 Modify）:** `src/deterministic_response_cache/response_reuse/codecs/json_response.py`、`tests/test_response_reuse_codecs.py`、`tests/test_model_response_codecs_integration.py`。只有 committed approved correction Plan-Reviewer receipt 經 Planner route 後才可建立新 immutable subject。
- **Read-only:** `analysis/model-response-codecs/requirements.md`、`analysis/model-response-codecs/technical-spec.md`、`plan/model-response-codecs/model-response-codecs.spec.md`、原 Plan-Reviewer receipt、原 Tester/Reviewer evidence、`response_reuse/codecs/contract.py`、`selector.py`、`pyarrow_dataframe.py`、`protocol.py`、`outcomes.py`、Store/eligibility、依賴、其他 tests、全部 BC docs/archify 交付、其他 topic；沒有刪除路徑。

## What stays current

- Parent plan 的 Goal、BC、source break、VO、codec Protocol/`@override`、固定 selector、Arrow IPC、`DataFrame.equals`、optional extra、reason 集合、direct imports、archify 與 workflow human boundary 均維持 current truth。
- 原 implementation subject、passing Tester evidence 與 needs-rework Reviewer evidence 是歷史事實，不作本輪 approval 或新 subject 的驗證。原 analysis/spec 保持不變；parent plan/step 同步本次 correction 的當前 scope 與待辦，而不改寫歷史 artifact。

## What changes / Acceptance delta

1. `JsonResponseCodec.encode` 對已知不支援的 JSON 樹丟 `UnsupportedPayloadError`，使既有 selector/protocol 映射為 `NotCached(UNSUPPORTED_PAYLOAD)`；實際 serializer failure 繼續丟 `EncodeFailureError` 並映射 `NotCached(ENCODE_FAILURE)`。不得改 selector/protocol 或擴張 public codec contract。
2. `tests/test_response_reuse_codecs.py` 驗證已知 unsupported 樹與真正 encoder failure 的不同 exception、空 DataFrame 的 Arrow IPC/equals 行為，保留現有 direct imports、fixture/mock/assertions。
3. `tests/test_model_response_codecs_integration.py` 驗證 unsupported 樹的 protocol reason 與 Store 未寫入、DataFrame optional codec unavailable record 的 `NotCached(CODEC_UNAVAILABLE)`、serializer failure 的 `NotCached(ENCODE_FAILURE)`、foreign malformed envelope 的 `Unavailable(INVALID_PAYLOAD)`；測試須有對應 outcome 和無誤寫 Store 的實際 assertion。
4. 既有 JSON-only import、DataFrame hit isolation、未知 codec/壞 bytes、Identity passthrough、docs/archify 行為持續通過；不新增只查 decorator 存在的測試或動態 import 替代。

## Exact correction artifacts / ordering

| Artifact | Exact path | Write owner | Decision authority / order |
| --- | --- | --- | --- |
| Parent plan sync | `plan/model-response-codecs/model-response-codecs.plan.md` | Plan-Creator | 當前 topic execution contract；planning candidate #1 |
| Parent step sync | `plan/model-response-codecs/model-response-codecs.step.md` | Plan-Creator | 保留舊完成步驟與新 pending correction；planning candidate #2 |
| Correction plan | `plan/model-response-codecs/model-response-codecs.correction-fix-1-plan.md` | Plan-Creator | 本輪 trigger/scope/schema authority；planning candidate #3 |
| Correction step | `plan/model-response-codecs/model-response-codecs.correction-fix-1-step.md` | Plan-Creator | 本輪 ordered checkpoints；planning candidate #4 |
| Extended correction Plan-Reviewer receipt | `plan/model-response-codecs/model-response-codecs.correction-fix-1-plan-review-log.json` | Independent Plan-Reviewer | 只審 committed exact-four candidate 後寫；Implementer 原樣 sole evidence-only commit；僅 approved 可供 Planner route |
| Correction Tester evidence | `plan/model-response-codecs/model-response-codecs.tester-evidence.fix-1.json` | Tester | 新 exact-three immutable subject 後記 actual commands/exit codes；Implementer 原樣 sole evidence-only commit |
| Correction implementation review | `plan/model-response-codecs/model-response-codecs.implementation-review-log.fix-1.json` | Independent Reviewer | 僅消費 committed passing 同 subject correction Tester evidence；Implementer 原樣 sole evidence-only commit |

任何新 candidate/subject/evidence 的 SHA、tree、blob 與 verdict 都是未來 post-commit fact；本 plan 不預填。任一未列 path、candidate conflict 或不符 first-parent/sole evidence commit 的狀態停回 Planner。

## Extended Plan-Reviewer receipt schema

Independent Plan-Reviewer 只可在 exact-four candidate 已提交且 clean checkout 可審後寫單一 JSON object。Top-level keys **恰為** `schema_version`、`topic`、`correction_id`、`candidate`、`reviewed_artifacts`、`first_parent_admission`、`review_basis`、`verdict`、`blocking_issues`、`copilot_feedback_triage`、`route_authorization`、`recorded_by`：

- `schema_version` 是 integer `1`；`topic` 是 `model-response-codecs`；`correction_id` 是 `fix-1`；`recorded_by` 是 `Independent Plan-Reviewer`。
- `candidate` 恰有 `commit_sha`、`tree_sha`、`active`。前兩者是實際 committed candidate 的 full lowercase 40-hex；`active` 僅在 approved 時 `true`，needs-rework 時 `false`。
- `reviewed_artifacts` 是以上四個 planning paths 各恰一次的 object array，每項恰有 `path`、`blob_sha`，blob SHA 是該 committed candidate 內實際 full lowercase 40-hex blob。
- `first_parent_admission` 恰有 `parent_sha`、`non_merge`、`name_status`；parent SHA 是 candidate 的實際 full lowercase 40-hex 第一 parent，且此 route 的 candidate 須是舊 Reviewer evidence sole commit `57e4940150157d3cc73799c20461000eacc6bfe2` 的 direct child；`non_merge` 必須為 `true`；`name_status` 是 actual first-parent named diff 的四項 object array，每項恰有 `status`（`M|A`）與 `path`，恰為 parent plan/step 的 `M` 與 correction plan/step 的 `A`，不可混入 code/evidence。
- `review_basis` 恰有 `workflow_contract`、`topic_plan_contract`、`checkout`；兩 contract 值分別為 `plan/agent-handoff-workflow.md`、`plan/topic-plan-contract.md`，checkout 是 actual clean candidate commit full SHA。
- `verdict` 為 `approved|needs-rework`；`blocking_issues` 是 object array，每項恰有 non-empty `issue`、`file`、`fix`；approved 必須空陣列，needs-rework 至少一項。
- `copilot_feedback_triage` 恰有 `ADDRESS`、`DISCUSS`、`SKIP` arrays，分別採現有 normal Plan-Reviewer 的 `{comment,location,why}`、`{comment,optional,why}`、`{comment,why}` shapes；無 feedback 時各為空。
- `route_authorization` 在 approved 時為 object，恰有 `next_phase: "creator-in-progress"`、`next_role: "Implementer"`、`scope: "fix-1-exact-three-subject"`；needs-rework 時為 `null`，不得宣告 active candidate、next phase、subject 或 close authorization。

Implementer 只可將 receipt 原樣以 sole one-path evidence-only commit 提交；Planner 以 actual Git candidate/tree/blob/parent/diff 和 receipt 內容驗證。未提交、needs-rework 或不相符 receipt 均不授權新 subject。若 `fix-1` planning receipt 是 `needs-rework`，該 path/commit 保持 immutable，停回 Planner，由 Plan-Creator 宣告下一輪 bounded correction route 與新的 receipt path；不得覆寫本輪 receipt。

## Tester and Reviewer evidence schemas

- Tester `fix-1` evidence 是單一 JSON object，top-level keys 恰為 `schema_version`、`topic`、`correction_id`、`implementation_subject_commit`、`status`、`commands`、`recorded_by`。`schema_version: 1`、`topic: "model-response-codecs"`、`correction_id: "fix-1"`、`recorded_by: "Tester"`；subject 為新 exact-three non-merge commit 的 full lowercase 40-hex；`commands` 是 non-empty array，每項恰有 non-empty string `command` 與 integer `exit_code`。`passing` 僅在全部 exit code 0；`failing` 至少一個非零。Tester 寫後由 Implementer 原樣 sole one-path evidence-only commit。
- Independent Reviewer `fix-1` evidence 是單一 JSON object，top-level keys 恰為 `schema_version`、`topic`、`correction_id`、`implementation_subject_commit`、`tester_evidence_commit`、`verdict`、`blocking_issues`、`recorded_by`。`schema_version: 1`、同 topic/id、`recorded_by: "Independent Reviewer"`；subject 與 Tester 的 full SHA 相同；`tester_evidence_commit` 為已提交且 sole-path、同 subject、passing 的新 Tester evidence commit full lowercase 40-hex；`verdict: approved|needs-rework`，approved 時 blockers 空 string array，needs-rework 時至少一項。Reviewer 只能在 committed passing Tester evidence 後寫；Implementer 原樣 sole one-path evidence-only commit。
- 兩份新 evidence 都不得與 code、planning artifact、另一份 evidence 或舊 evidence 共用 commit。新 `approved` Reviewer evidence 經 Planner Phase 4.5 對齊後，方可依既有 Human authorization 進 bounded push/draft PR；Human 獨占 review、merge、release、post-merge、tag、final summary。
- 若本輪 Tester `failing` 或 Independent Reviewer `needs-rework`，均停回 Planner；由 Plan-Creator 為下一輪 bounded correction 宣告新的 planning/evidence paths，再經獨立 planning gate。已提交的 `fix-1` Tester／Reviewer evidence 原樣保留為 immutable historical truth，不得覆寫同一 Add path、直接以新 subject 重跑或以舊 passing evidence 關閉新 blocker。

## Parent sync / retention and closure

Parent plan/step 在 exact-four candidate 內同步當前 needs-rework state、exact paths、pending steps、五個 conditional correction artifacts 與新 gate；原 plan/spec 的行為契約仍為 current truth。Correction plan/step 保存本輪 trigger 與歷史路由，不能取代 parent 的當前契約。只有新 exact-three subject、committed passing Tester evidence、committed approved Independent Reviewer evidence 與 Planner Phase 4.5 均成立，才可關閉本輪阻礙；Plan-Creator、Implementer 或 Reviewer 均不得以聊天或此 plan 自行宣稱 gate 完成。
