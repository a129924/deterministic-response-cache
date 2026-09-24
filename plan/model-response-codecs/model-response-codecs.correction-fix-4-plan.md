# model-response-codecs — correction fix-4 plan

## Trigger / bounded decision

Fix-3 exact-six planning candidate `c67f5c23bc2b6f3a6cb1f6b8e883b9ee77a561d1`、approved Plan-Reviewer sole receipt commit `4389ddc5b83c65ae4e08976c7e270c567ebdec7b`、exact-eight implementation subject `b9a68575b24472a136bc7f3b826c8e7e581250b2`、passing Tester sole evidence commit `2ff945e236aaa76afce61dbac1df62fc860f45c7` 與 Independent Reviewer needs-rework sole log commit `dff896ce0548c8d9c8ae36cabbe60792c9211225` 均已提交且 immutable。Reviewer 唯一 blocker：parseable 深層 JSON 在 `JsonResponseCodec.decode` 的 `_valid_json_tree` 可引發 `RecursionError`，因此未回封閉 `InvalidPayload`，`ResponseReuseProtocol.lookup` 也未回 `Unavailable(INVALID_PAYLOAD)`。Draft PR #11 仍 OPEN base `dev`，origin 仍是舊 fix-2 HEAD；本輪不從 PR state 或舊 approved evidence 推定 fix-4 gate。

本 correction 只補原 fix-3 已批准的 decode failure 契約，不改 Goal、BC、`ModelResponse.value`、`StoredResponse`、兩個 id、closed results/outcomes、Arrow IPC、equals、DataFrame isolation、optional deps、direct imports、archify 或任何對外 reason。Parent spec 與 analysis technical spec 已明列壞 JSON bytes → `InvalidPayload`、protocol → `Unavailable(INVALID_PAYLOAD)`；本輪無需修改兩檔。若發現 acceptance 必須實質改變，停回 Planner 擴 exact allowlist，不自行寫入。

## Exact scope / ownership

- **Planning candidate，exact four，non-merge first-parent：** **Modify** `plan/model-response-codecs/model-response-codecs.plan.md`、`plan/model-response-codecs/model-response-codecs.step.md`；**Add** 本檔、`plan/model-response-codecs/model-response-codecs.correction-fix-4-step.md`。Plan-Creator 唯一 author；Implementer 只提交此四檔。first parent 必須是 `dff896ce0548c8d9c8ae36cabbe60792c9211225`；candidate SHA/tree/blob/verdict 不預填。
- **Future implementation subject，exact four，全部 Modify：** `src/deterministic_response_cache/response_reuse/codecs/json_response.py`、`tests/test_response_reuse_codecs.py`、`tests/test_model_response_codecs_integration.py`、`tests/test_response_reuse_protocol.py`。只在 fix-4 committed approved Plan-Reviewer receipt 經 Planner route 後由 Implementer 建 immutable subject。其他 source/test（含 selector/protocol、parent spec/analysis）、docs/archify/evidence read-only，無 Add/Delete implementation path。
- **Repair：** `JsonResponseCodec.decode` 只將 JSON parsing 與 `_valid_json_tree` 驗證中可預期的深度 `RecursionError` 轉為 `InvalidPayload()`；不 catch-all，不吞未預期程式錯誤。已有合法 JSON 成功結果、其他無效 JSON、encode 分類、Arrow/selector 保持。`ResponseReuseProtocol.lookup` 的既有 `InvalidPayload` → `Unavailable(INVALID_PAYLOAD)` 翻譯不修改。使用 parseable、巢狀深度足以讓 validator 觸發 `RecursionError` 的 bytes 驗證直接 codec 結果與經 Store lookup 的 protocol outcome，且非 `Miss`、policy 不呼叫。

## Boundary classification

Observed boundary 是 JSON decoder 到固定 selector，再到 Response Reuse protocol。接收者 protocol 依 `InvalidPayload` 決定既有 `Unavailable(INVALID_PAYLOAD)`；深層但可 parse 的儲存內容是預期資料失敗，與 unknown codec、optional codec unavailable 不同。`RecursionError` 的有限轉譯只在 JSON parse/validation 區段進行；Store/policy contract `TypeError` 與意外 exception 仍保留原邊界。不引入新的對外 outcome 或 exception taxonomy。

## Conditional correction artifacts / order

| Artifact | Exact path | Sole writer | Authority / order |
| --- | --- | --- | --- |
| Parent plan sync | `plan/model-response-codecs/model-response-codecs.plan.md` | Plan-Creator | Candidate M #1；current topic contract |
| Parent step sync | `plan/model-response-codecs/model-response-codecs.step.md` | Plan-Creator | Candidate M #2；progress truth |
| Fix-4 correction plan | `plan/model-response-codecs/model-response-codecs.correction-fix-4-plan.md` | Plan-Creator | Candidate A #3；scope/schema authority |
| Fix-4 correction step | `plan/model-response-codecs/model-response-codecs.correction-fix-4-step.md` | Plan-Creator | Candidate A #4；ordered checkpoints |
| Fix-4 Plan-Reviewer receipt | `plan/model-response-codecs/model-response-codecs.correction-fix-4-plan-review-log.json` | Independent Plan-Reviewer | Only after committed exact-four candidate；Implementer unchanged sole one-path evidence-only commit |
| Fix-4 Tester evidence | `plan/model-response-codecs/model-response-codecs.tester-evidence.fix-4.json` | Tester | Only after new exact-four implementation subject；Implementer unchanged sole one-path evidence-only commit |
| Fix-4 implementation review | `plan/model-response-codecs/model-response-codecs.implementation-review-log.fix-4.json` | Independent Reviewer | Only after committed passing same-subject Tester evidence；Implementer unchanged sole one-path evidence-only commit |

New evidence paths are distinct and absent at authoring; initial/fix-1/fix-2/fix-3 evidence remains immutable. No evidence is bundled with planning, code, or another evidence file. New SHA, verdict, HEAD and outcome are only post-action facts.

## Active extended Plan-Reviewer receipt schema

Independent Plan-Reviewer writes one JSON object only after checking a clean committed exact-four candidate. Top-level keys exactly `schema_version`, `topic`, `correction_id`, `candidate`, `reviewed_artifacts`, `first_parent_admission`, `review_basis`, `verdict`, `blocking_issues`, `copilot_feedback_triage`, `route_authorization`, `recorded_by`.

- `schema_version` integer `1`; `topic` `model-response-codecs`; `correction_id` `fix-4`; `recorded_by` `Independent Plan-Reviewer`.
- `candidate` exactly `{commit_sha,tree_sha,active}` with actual full lowercase 40-hex SHAs; active true only for approved, false for needs-rework.
- `reviewed_artifacts` exactly four `{path,blob_sha}` entries for the four planning paths, each actual full lowercase 40-hex blob SHA.
- `first_parent_admission` exactly `{parent_sha,non_merge,name_status}`; parent SHA `dff896ce0548c8d9c8ae36cabbe60792c9211225`, non_merge true, name_status exactly four `{status,path}` in actual Git lexical order, two M and two A, no other path.
- `review_basis` exactly `{workflow_contract,topic_plan_contract,checkout}`; contract paths `plan/agent-handoff-workflow.md` and `plan/topic-plan-contract.md`, checkout actual clean candidate full SHA.
- `verdict` `approved|needs-rework`; `blocking_issues` array of `{issue,file,fix}`, empty for approved and nonempty for needs-rework. `copilot_feedback_triage` exactly `{ADDRESS,DISCUSS,SKIP}` arrays; entries respectively `{comment,location,why}`, `{comment,optional,why}`, `{comment,why}`, empty arrays if no feedback.
- `route_authorization` only for approved is exactly `{next_phase:"creator-in-progress",next_role:"Implementer",scope:"fix-4-exact-four-subject"}`; for needs-rework it is null and there is no active candidate or implementation authority.

Reviewer does not commit or route. Implementer commits receipt unchanged as sole evidence-only direct child of candidate; Planner verifies actual Git parent/tree/blob/diff and only committed approved may route. Needs-rework requires Planner/Plan-Creator to declare a later bounded route with new paths; fix-4 receipt stays immutable.

## Tester / Independent Reviewer evidence schemas

- Tester writes one JSON object with top-level keys exactly `schema_version`, `topic`, `correction_id`, `implementation_subject_commit`, `status`, `commands`, `recorded_by`; fixed schema version `1`, topic, `fix-4`, `Tester`. Subject is actual exact-four non-merge full lowercase 40-hex commit SHA. `commands` nonempty array of exactly `{command,exit_code}` objects with nonempty string/integer; passing only if all exit codes zero, failing if any nonzero. Tester does not commit; Implementer commits unchanged sole one-path evidence-only.
- Independent Reviewer writes one JSON object with top-level keys exactly `schema_version`, `topic`, `correction_id`, `implementation_subject_commit`, `tester_evidence_commit`, `verdict`, `blocking_issues`, `recorded_by`; fixed schema version `1`, topic, `fix-4`, `Independent Reviewer`. Subject equals committed passing Tester subject full SHA; Tester evidence commit is actual sole evidence-only full SHA. Verdict approved with empty string-array blockers or needs-rework with nonempty string-array blockers. Reviewer does not commit; Implementer commits unchanged sole one-path evidence-only.
- Tester failing or Reviewer needs-rework stops Phase 4.5/publish and requires a later bounded correction with new evidence paths. Fix-4 evidence remains immutable. Only same-subject committed passing Tester and approved Independent Reviewer plus Planner Phase 4.5 alignment allow bounded push/update Draft PR #11 under existing Human authorization. Human alone reviews, approves, merges, releases.

## Verification

- `tests/test_response_reuse_codecs.py`：直接 `JsonResponseCodec.decode` 使用 parseable 深層 array bytes，確認回 `InvalidPayload` 值而非冒出 `RecursionError`；保留其他 JSON success/invalid cases。
- `tests/test_model_response_codecs_integration.py`、`tests/test_response_reuse_protocol.py`：用同類 stored `StoredResponse(JSON_V1, deep_bytes)` 經 protocol lookup，確認 `Unavailable(INVALID_PAYLOAD)`、非 `Miss`、policy 不評估；保留 Store exception/contract 與原 direct-import fixtures/mocks。新案例限定資料預期失敗，不以 catch-all 讓意外程式錯誤也變成 `InvalidPayload`。
- Tester 對新 subject 跑 `uv run --extra dataframe pytest`、`uv run --extra dataframe pyright` strict、`uv run --extra dataframe ruff check .` 與 JSON-only direct-import 回歸，記 actual exit codes；docs/archify/visual sidecars 僅作 frozen predecessor，不在 fix-4 重新產生。
