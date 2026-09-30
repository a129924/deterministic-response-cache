# model-response-codecs — correction fix-3 plan

## Trigger / authority

Draft PR #11 已 open、base `dev`；Human 要求同一 topic 回修 codec 的預期失敗契約。此為 `pr-open` → `needs-rework` 的 bounded correction，不取消原 Goal、BC、`ModelResponse.value`、`StoredResponse`、兩個 codec id、Arrow IPC、`DataFrame.equals`、DataFrame hit 隔離、optional extra、defining-module direct imports、archify 或原有對外 outcome/reason。`fix-2` 的 approved planning candidate `a45a7d3a31794b9d9ce75c2695efcdee93ebd539`、Plan-Reviewer receipt commit `7277980b9442fc4142b6b9ba11b9e6ecc21ec6cd`、implementation subject `3a1c19f3db126f8f87235c47aaf52a98cdcacb50`、Tester evidence commit `b4021849b92a8e67a9342f10504cfaef049336cc` 與 Independent Reviewer approved evidence commit `7c474f2ff57c4a0af355e8953929f2d856e66424` 均為 immutable predecessor。initial/fix-1/fix-2 receipts、subjects、evidence 不可覆寫或重用。新 planning candidate 的 first parent 固定為 `7c474f2ff57c4a0af355e8953929f2d856e66424`；後續 SHA、tree、blob、verdict 只能事後記錄。

## Exact scope / paths

- **Planning candidate，exact six，non-merge first-parent：** **Modify** `plan/model-response-codecs/model-response-codecs.plan.md`、`plan/model-response-codecs/model-response-codecs.step.md`、`plan/model-response-codecs/model-response-codecs.spec.md`、`analysis/model-response-codecs/technical-spec.md`；**Add** 本檔、`plan/model-response-codecs/model-response-codecs.correction-fix-3-step.md`。唯一 writer Plan-Creator；Implementer 只提交這六檔，不混入 code/evidence。
- **Future implementation subject，exact eight，全部 Modify：** `src/deterministic_response_cache/response_reuse/codecs/contract.py`、`src/deterministic_response_cache/response_reuse/codecs/json_response.py`、`src/deterministic_response_cache/response_reuse/codecs/pyarrow_dataframe.py`、`src/deterministic_response_cache/response_reuse/codecs/selector.py`、`src/deterministic_response_cache/response_reuse/protocol.py`、`tests/test_response_reuse_codecs.py`、`tests/test_model_response_codecs_integration.py`、`tests/test_response_reuse_protocol.py`。Implementer 只在 committed approved fix-3 Plan-Reviewer receipt 經 Planner route 後建立新 immutable subject。`outcomes.py` 與其 enum 值不變；不新增 outcomes file。
- **ReadOnly / Deleted：** `analysis/model-response-codecs/requirements.md`、其餘 source/test/docs/archify/dependency files 與全部歷史 planning/evidence read-only；無刪檔。`codecs.py`、`codecs/__init__.py`、package re-export、動態 registry、`importlib`、`__import__`、`sys.modules` 替換均不建立。

## Fix-3 codec/result contract

`codecs/contract.py` 定義 frozen、slotted、以類別可辨別的封閉結果。`EncodeResult` 恰為 `Encoded(stored: StoredResponse) | UnsupportedPayload | CodecUnavailable | EncodeFailure | RoundTripMismatch`；`DecodeResult[PayloadT]` 恰為 `Decoded(response: ModelResponse[PayloadT]) | UnknownCodec | CodecUnavailable | InvalidPayload`。無多餘 catch-all variant，也不把下層 exception object 放入上層 reason。`ResponseCodec[PayloadT](Protocol)` 仍只有 `codec_id` property、`encode(response: ModelResponse[PayloadT]) -> EncodeResult`、`decode(payload: bytes) -> DecodeResult[PayloadT]` 三 member。成功也包入 `Encoded`／`Decoded`，呼叫端可用 `match/case` 完整辨別；不以 `None`、truthiness 或 exception 代替預期分支。

`JsonResponseCodec(ResponseCodec[JsonPayload])` 與 `PyArrowDataFrameCodec(ResponseCodec[pandas.DataFrame])` 繼續明確繼承，三 member 以 `typing.override` 驗證，property 順序 `@property`、`@override`。具體 codec 對預期成功／失敗**直接回傳結果值**：JSON 不支援樹 → `UnsupportedPayload`，支援樹的 serializer/round-trip encode 問題 → `EncodeFailure`，壞 JSON bytes → `InvalidPayload`；Arrow 轉換／IPC encode 問題 → `EncodeFailure`，`equals` 不通過 → `RoundTripMismatch`，壞 Arrow bytes → `InvalidPayload`。DataFrame encode 接完整 VO，先寫 memory Arrow IPC、立即 decode、再以 `original.equals(decoded)` 擋寫入。Codec 不自行回報 selector 才能判定的未知 id 或 optional module 缺失。

固定 selector 的 `encode_response`／`decode_response` 回傳同一封閉 union：dict/list → JSON，DataFrame → Arrow codec；其他 root → `UnsupportedPayload`；可選 codec import 不可用 → `CodecUnavailable`；unknown/illegal stored id → `UnknownCodec`；合法 id 但 payload 非 bytes 或壞 bytes → `InvalidPayload`。讀取只以保存 id 的 `match/case` 選 decoder，不嗅探 bytes。保持 JSON-only 路徑不急切載入 pandas/pyarrow，分支內 direct imports 與既有可選依賴行為不變。若 pandas 不在環境且無從證實值是 DataFrame，非 JSON root 仍按現有 `UnsupportedPayload` 分流。

`ResponseReuseProtocol` 在 Response Reuse 邊界將上述已知分支映到**既有** `NotCachedReason`／`UnavailableReason`；原 `ModelResponse` 在 record 失敗仍保留，失敗不寫 Store。`Encoded` 才呼叫 Store write；`Decoded` 才交 eligibility policy。`UnknownCodec`／`InvalidPayload` 等 lookup failure 不得變成 `Miss`。Store `NotFound`、Store failure/write failure、policy deny 的既有對外 outcome 保持。`TypeError` 明確保留給 Store read/write 與 eligibility decision 的 contract violation；codec/selector 預期資料問題走回傳值。只攔截已知 JSON/Arrow/pandas 編解碼例外與可選依賴 `ImportError`；不加 `except Exception`、不把程式錯誤或意外 Store/policy exception 包成 expected failure。

## Boundary decision

Observed boundary 是 Response Reuse 內部 codec/selector 到 protocol；決策消費者是 protocol。`UnsupportedPayload`、`CodecUnavailable`、`EncodeFailure`、`RoundTripMismatch` 決定不同 `NotCachedReason`；`UnknownCodec`、`CodecUnavailable`、`InvalidPayload` 決定不同 `UnavailableReason`，因此保留區別。Codec 只描述編解碼結果，protocol 是轉成 Response Reuse 對外 outcome 的唯一翻譯點；CacheStore/Identity/policy 的 authority 與異常傳播不變。這些為 expected failure；Store/policy 違約與非預期 bug 不加入結果 union。

## Conditional correction artifacts / order

| Artifact | Exact path | Sole writer | Order / authority |
| --- | --- | --- | --- |
| Parent plan | `plan/model-response-codecs/model-response-codecs.plan.md` | Plan-Creator | Candidate M #1；current topic contract |
| Parent step | `plan/model-response-codecs/model-response-codecs.step.md` | Plan-Creator | Candidate M #2；progress truth |
| Parent spec | `plan/model-response-codecs/model-response-codecs.spec.md` | Plan-Creator | Candidate M #3；acceptance authority |
| Technical spec | `analysis/model-response-codecs/technical-spec.md` | Plan-Creator | Candidate M #4；strict mode execution authority |
| Fix-3 plan | `plan/model-response-codecs/model-response-codecs.correction-fix-3-plan.md` | Plan-Creator | Candidate A #5；this correction schema authority |
| Fix-3 step | `plan/model-response-codecs/model-response-codecs.correction-fix-3-step.md` | Plan-Creator | Candidate A #6；ordered checkpoints |
| Plan-Reviewer receipt | `plan/model-response-codecs/model-response-codecs.correction-fix-3-plan-review-log.json` | Independent Plan-Reviewer | After committed exact-six candidate；Implementer unchanged sole evidence-only commit |
| Tester evidence | `plan/model-response-codecs/model-response-codecs.tester-evidence.fix-3.json` | Tester | After new exact-eight subject；Implementer unchanged sole evidence-only commit |
| Implementation review | `plan/model-response-codecs/model-response-codecs.implementation-review-log.fix-3.json` | Independent Reviewer | After committed passing same-subject Tester evidence；Implementer unchanged sole evidence-only commit |

Each evidence path is new and distinct; no initial/fix-1/fix-2 path is rewritten. These three evidence commits each contain exactly one unchanged evidence file, no plan/code/other evidence, in the table order. New SHA/verdict/HEAD are not prefilled.

## Active extended Plan-Reviewer receipt schema

Independent Plan-Reviewer writes one JSON object only after checking the clean committed exact-six candidate. Top-level keys exactly `schema_version`, `topic`, `correction_id`, `candidate`, `reviewed_artifacts`, `first_parent_admission`, `review_basis`, `verdict`, `blocking_issues`, `copilot_feedback_triage`, `route_authorization`, `recorded_by`.

- `schema_version` integer `1`; `topic` `model-response-codecs`; `correction_id` `fix-3`; `recorded_by` `Independent Plan-Reviewer`.
- `candidate` exactly `{commit_sha,tree_sha,active}` with actual full lowercase 40-hex SHA; `active` true only for approved, false for needs-rework.
- `reviewed_artifacts` exactly six `{path,blob_sha}` objects for the exact-six planning paths, actual blob full lowercase 40-hex.
- `first_parent_admission` exactly `{parent_sha,non_merge,name_status}`; parent SHA fixed to `7c474f2ff57c4a0af355e8953929f2d856e66424`, non_merge true; name_status exactly six `{status,path}` objects in actual Git lexical order, four M and two A, no other path.
- `review_basis` exactly `{workflow_contract,topic_plan_contract,checkout}` with first two paths `plan/agent-handoff-workflow.md` and `plan/topic-plan-contract.md`, checkout actual clean candidate full SHA.
- `verdict` `approved|needs-rework`; `blocking_issues` array of `{issue,file,fix}`, empty only for approved and nonempty for needs-rework; `copilot_feedback_triage` exactly `{ADDRESS,DISCUSS,SKIP}` arrays with entries `{comment,location,why}`, `{comment,optional,why}`, `{comment,why}` respectively, empty arrays if none.
- `route_authorization` only for approved is exactly `{next_phase:"creator-in-progress",next_role:"Implementer",scope:"fix-3-exact-eight-subject"}`; for needs-rework it is null and there is no active candidate or implementation authority.

Reviewer does not commit/route. Implementer commits unchanged receipt alone with candidate as direct parent. Planner verifies actual Git parent/tree/blob/diff and only committed approved can route. If needs-rework, stop with immutable receipt and ask Planner/Plan-Creator for a new bounded correction route and new evidence paths.

## Tester / Independent Reviewer evidence schemas

- Tester writes exactly one JSON object with top-level keys `schema_version`, `topic`, `correction_id`, `implementation_subject_commit`, `status`, `commands`, `recorded_by`; fixed schema version `1`, topic, `fix-3`, `Tester`. Subject is actual exact-eight non-merge full lowercase 40-hex SHA. Commands are nonempty array of objects each exactly `{command,exit_code}` with nonempty string and integer. Passing only when every exit code is zero; failing requires a nonzero. Tester does not commit; Implementer commits unchanged evidence alone.
- Independent Reviewer writes exactly one JSON object with top-level keys `schema_version`, `topic`, `correction_id`, `implementation_subject_commit`, `tester_evidence_commit`, `verdict`, `blocking_issues`, `recorded_by`; fixed schema version `1`, topic, `fix-3`, `Independent Reviewer`. Subject must equal committed passing Tester subject full SHA; Tester evidence commit must be its actual sole evidence-only full SHA. Verdict approved with empty string-array blockers or needs-rework with nonempty string-array blockers. Reviewer does not commit; Implementer commits unchanged evidence alone.
- Tester failing or Reviewer needs-rework stops Phase 4.5/publish; Planner/Plan-Creator must declare a later correction with fresh evidence paths. Fix-3 evidence stays immutable. Q gate requires same-subject committed passing Tester and approved Independent Reviewer evidence, then Planner Phase 4.5 alignment before bounded push/update of draft PR #11. Human alone reviews/approves/merges/releases.

## Tests / verification

- Direct codec and selector tests assert each expected variant by type and payload: `Encoded`, `Decoded`, `UnsupportedPayload`, `CodecUnavailable`, `EncodeFailure`, `RoundTripMismatch`, `UnknownCodec`, `InvalidPayload`. Exercise JSON and DataFrame success, malformed bytes/id, missing optional deps, lossy JSON, Arrow mismatch, real serializer/Arrow failures. No expected-path `pytest.raises` remains for these variants.
- Protocol integration tests assert every variant maps to the unchanged `NotCached`/`Unavailable` reason and preserves original response/no Store write on record failure; `Miss` only for NotFound/policy deny. Maintain foreign malformed envelope, opaque identity, store/policy contract `TypeError` and exception propagation.
- Preserve existing direct imports/fixtures/mocks and JSON-only import regression; update direct caller fixtures to unwrap `Encoded`/`Decoded` rather than treating result as raw envelope/response. `uv run --extra dataframe pytest`, `uv run --extra dataframe pyright` strict, `uv run --extra dataframe ruff check .` and base-install JSON-only validation. Existing archify artifacts remain read-only; no new visual output is required for this internal failure-contract change.
