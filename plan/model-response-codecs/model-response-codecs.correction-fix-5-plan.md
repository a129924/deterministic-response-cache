# model-response-codecs — correction fix-5 plan

## Trigger / authority

Human 已決定公開 VO equality 維持值比較：JSON 沿用 Python 值比較，DataFrame 使用 `DataFrame.equals`。Draft PR #11 為 OPEN、Ready、base `dev`、head `b66f77d6382b22b147e556e270e233a8abb62fe5`；fix-4 的 committed approved Plan-Reviewer receipt `5ff48411db917fded0ed8bcd8ced45b802e68ff1`、subject `9a0eef1845113801c4d250826df4e9a9dee09917`、passing Tester evidence `2cef0406fb401be36563c247ff409bc7ed7dc44c`、approved Independent Reviewer evidence `853628596f177896b09c72a25f1a9f3b6391be46` 與後續 head `b66f77d6382b22b147e556e270e233a8abb62fe5` 是 frozen predecessor。Human/Planner 已確認 PR thread 1 resolved、2–4 unresolved；新 subject 完成前不得把 thread 2–4 宣稱 addressed/resolved。舊 initial/fix-1/fix-2/fix-3/fix-4 planning/evidence 不覆寫或重用。

這是同一 Response Reuse BC Mission 的 bounded correction，Goal、Identity opaque boundary、Store ownership、`ModelResponse.value`/`StoredResponse`/兩 id、closed codec results 與 public outcomes、Arrow IPC、`DataFrame.equals` 寫入門檻、DataFrame hit 隔離、optional extra、direct imports、archify 均保留。只補 JSON lone surrogate decode failure 與公開 VO DataFrame equality；不新增 registry、payload 類型、re-export、dynamic import 或 catch-all。

## Exact paths / ownership

- **Planning candidate，exact seven，non-merge first-parent：** **Modify** `analysis/model-response-codecs/requirements.md`、`analysis/model-response-codecs/technical-spec.md`、`plan/model-response-codecs/model-response-codecs.plan.md`、`plan/model-response-codecs/model-response-codecs.spec.md`、`plan/model-response-codecs/model-response-codecs.step.md`；**Add** 本檔、`plan/model-response-codecs/model-response-codecs.correction-fix-5-step.md`。Plan-Creator 只 author 這七檔；Implementer 只提交此七檔。First parent 必為 `b66f77d6382b22b147e556e270e233a8abb62fe5`；candidate SHA/tree/blob/verdict 留待事實產生。
- **Future implementation subject，exact six，全部 Modify：** `src/deterministic_response_cache/response_reuse/codecs/json_response.py`、`src/deterministic_response_cache/response_reuse/model_response.py`、`tests/test_response_reuse_codecs.py`、`tests/test_model_response_codecs_integration.py`、`tests/test_response_reuse_protocol.py`、`tests/test_response_reuse_outcomes.py`。只有 fix-5 committed approved Plan-Reviewer receipt 經 Planner route 才由 Implementer 建新 immutable subject。`outcomes.py`、selector/protocol、DataFrame codec、Store/policy、dependencies、docs/archify、其他 tests 均 read-only；無 Add/Delete implementation path。

## Behavioral delta / test obligation

- `JsonResponseCodec.decode` 對 parseable JSON 中 lone surrogate（value、object key、巢狀）回 `InvalidPayload()`；既有 selector/protocol 將之映 `Unavailable(INVALID_PAYLOAD)`、非 `Hit`/`Miss`，policy 不評估。只處理已知 Unicode 資料錯誤，不使用 catch-all，不更改其他 JSON/DF success/failure 分類。
- `ModelResponse` 保持 frozen/slotted、欄位只 `value`。比較兩個 DataFrame 時以 `.equals` 回布林值；一方為 DataFrame、另一方非 DataFrame 則不相等；JSON dict/list 保留既有 Python 值比較。`Hit`／`Cached` dataclass equality 經 `ModelResponse` 得相同結果，不修改 `outcomes.py`。純 JSON equality 分支不急切載入 pandas/pyarrow；DataFrame 分支只用 direct import，無 `importlib`、`__import__`、`sys.modules` 替換。無新 hashability 承諾。
- Codec tests 用 escaped lone surrogate value/key 驗證 direct `InvalidPayload`；integration/protocol tests 經 stored JSON lookup 驗 `Unavailable(INVALID_PAYLOAD)`、policy 未評估、direct imports；VO/outcomes tests 驗不同 DataFrame instance 相等、不同值不相等、JSON dict/list 值比較、`Hit`/`Cached` 布林 equality、JSON-only 無 optional import。保留既有 fixture/mock/assertions；pyright strict、pytest、ruff 與 base-install JSON-only regression 均由 Tester 記 factual evidence。

## Correction artifacts / ordered gates

| Artifact | Exact path | Sole writer | Order / authority |
| --- | --- | --- | --- |
| Requirements | `analysis/model-response-codecs/requirements.md` | Plan-Creator | Candidate M #1；business guardrail |
| Technical spec | `analysis/model-response-codecs/technical-spec.md` | Plan-Creator | Candidate M #2；execution source of truth |
| Parent plan | `plan/model-response-codecs/model-response-codecs.plan.md` | Plan-Creator | Candidate M #3；current topic contract |
| Parent spec | `plan/model-response-codecs/model-response-codecs.spec.md` | Plan-Creator | Candidate M #4；acceptance authority |
| Parent step | `plan/model-response-codecs/model-response-codecs.step.md` | Plan-Creator | Candidate M #5；progress truth |
| Fix-5 correction plan | `plan/model-response-codecs/model-response-codecs.correction-fix-5-plan.md` | Plan-Creator | Candidate A #6；this schema authority |
| Fix-5 correction step | `plan/model-response-codecs/model-response-codecs.correction-fix-5-step.md` | Plan-Creator | Candidate A #7；ordered checkpoints |
| Fix-5 Plan-Reviewer receipt | `plan/model-response-codecs/model-response-codecs.correction-fix-5-plan-review-log.json` | Independent Plan-Reviewer | After committed exact-seven candidate；Implementer unchanged sole one-path evidence-only commit |
| Fix-5 Tester evidence | `plan/model-response-codecs/model-response-codecs.tester-evidence.fix-5.json` | Tester | After new exact-six subject；Implementer unchanged sole one-path evidence-only commit |
| Fix-5 implementation review | `plan/model-response-codecs/model-response-codecs.implementation-review-log.fix-5.json` | Independent Reviewer | After committed passing same-subject Tester evidence；Implementer unchanged sole one-path evidence-only commit |

Three new evidence paths are distinct and absent at authoring. Each evidence commit contains exactly one unchanged evidence file and no planning/code/other evidence; ordering is Plan-Reviewer → Tester → Independent Reviewer. No future SHA/verdict/closure is prefilled.

## Active extended Plan-Reviewer receipt schema

Independent Plan-Reviewer writes one JSON object only after checking clean committed exact-seven candidate. Top-level keys exactly `schema_version`, `topic`, `correction_id`, `candidate`, `reviewed_artifacts`, `first_parent_admission`, `review_basis`, `verdict`, `blocking_issues`, `copilot_feedback_triage`, `route_authorization`, `recorded_by`.

- `schema_version` integer `1`；`topic` `model-response-codecs`；`correction_id` `fix-5`；`recorded_by` `Independent Plan-Reviewer`。
- `candidate` exactly `{commit_sha,tree_sha,active}` with actual full lowercase 40-hex SHAs；active true only for approved, false for needs-rework。
- `reviewed_artifacts` exactly seven `{path,blob_sha}` entries for the exact-seven paths, actual full lowercase 40-hex blob SHAs。
- `first_parent_admission` exactly `{parent_sha,non_merge,name_status}`；parent SHA `b66f77d6382b22b147e556e270e233a8abb62fe5`，non_merge true，name_status exactly seven `{status,path}` in actual Git lexical order, five M/two A, no other path。
- `review_basis` exactly `{workflow_contract,topic_plan_contract,checkout}` with paths `plan/agent-handoff-workflow.md`、`plan/topic-plan-contract.md` and actual clean candidate checkout full SHA。
- `verdict` `approved|needs-rework`；`blocking_issues` `{issue,file,fix}` array，empty for approved, nonempty for needs-rework。`copilot_feedback_triage` exactly `{ADDRESS,DISCUSS,SKIP}` arrays with entries `{comment,location,why}`、`{comment,optional,why}`、`{comment,why}`，empty arrays if none。
- `route_authorization` only for approved is exactly `{next_phase:"creator-in-progress",next_role:"Implementer",scope:"fix-5-exact-six-subject"}`；for needs-rework null and no active candidate or implementation authority。

Reviewer does not commit/route；Implementer commits unchanged sole receipt with candidate as direct parent。Planner verifies actual Git parent/tree/blob/diff；only committed approved routes。Needs-rework keeps receipt immutable and requires a later bounded correction with new paths。

## Tester / Independent Reviewer evidence schemas

- Tester writes one JSON object top-level exactly `schema_version`, `topic`, `correction_id`, `implementation_subject_commit`, `status`, `commands`, `recorded_by`；fixed schema version `1`、topic、`fix-5`、`Tester`。Subject actual exact-six non-merge full lowercase 40-hex SHA。Commands nonempty array of exactly `{command,exit_code}` with nonempty string/integer；passing only if all exits zero, failing if any nonzero。Tester does not commit；Implementer unchanged sole one-path evidence-only commit。
- Independent Reviewer writes one JSON object top-level exactly `schema_version`, `topic`, `correction_id`, `implementation_subject_commit`, `tester_evidence_commit`, `verdict`, `blocking_issues`, `recorded_by`；fixed schema version `1`、topic、`fix-5`、`Independent Reviewer`。Subject equals committed passing Tester subject full SHA；Tester evidence commit is actual sole evidence-only full SHA。Approved has empty string-array blockers, needs-rework nonempty。Reviewer does not commit；Implementer unchanged sole one-path evidence-only commit。
- Tester failing or Reviewer needs-rework stops Q/Phase 4.5/publish and returns Planner/Plan-Creator for new bounded correction/evidence paths；fix-5 evidence immutable。Only same-subject committed passing Tester, approved Independent Reviewer and Planner Phase 4.5 alignment authorize bounded push/update of PR #11 under existing Human authorization。

## PR review thread handoff

PR #11 is already Ready；thread 1 is resolved, threads 2–4 currently unresolved。After approved fix-5 evidence/Planner alignment and bounded push updates its head, Independent Reviewer alone reclassifies each still-open thread against actual new head and records exact thread identity plus addressed/resolvable status。Only an Implementer may post a bounded reply and resolve the **same exact** thread classified addressed-and-resolvable；it must not resolve by thread number alone, infer closure from code/CI, touch thread 1, approve PR, or merge。Unaddressed threads remain unresolved and route to Planner for another bounded correction；Human retains PR approval/merge/release/post-merge authority。
