# response-reuse-protocol — VO Channel Correction Plan

## Goal / Outcome

- **Analysis-layer routing:** strict mode. `analysis/response-reuse-protocol/vo-channel-correction.technical-spec.md`
  是 execution-facing source of truth；`analysis/response-reuse-protocol/vo-channel-correction.requirements.md`
  是 business-intent guardrail。本 correction plan 100% 依此 technical specification，不重開既有 Protocol BC
  或原 implementation subject 的設計決策。
- 將 CacheStore read/write interaction 改為明確 immutable slotted VO channels，並讓
  `ResponseReuseProtocol` 以 `match`／`case` 做完整且 fail-closed 的 outcome mapping。

## Scope

- **In scope**:
  - 僅修改以下四個 implementation paths：
    `src/deterministic_response_cache/response_reuse/_cache_store.py`、
    `src/deterministic_response_cache/response_reuse/protocol.py`、
    `tests/test_response_reuse_protocol.py`、`docs/business-capability-architecture.md`。
  - read contract `ResponseT | NotFound | CacheStoreFailure`、write contract
    `TokenWritten | CacheStoreWriteFailure`、四個 VO 的 immutable/slotted/non-Exception semantics、
    `match`／`case` mapping，以及可偵測 channel-contract violation 的 `TypeError`。

- **Out of scope**:
  - `outcomes.py`、其他 tests、其餘 architecture documents／scene、public exports、package initializer、
    dependencies、Identity、backend、TTL、invalidation、runtime、execution、provider、release 與任何 deletion。
  - 原 implementation、Tester、Reviewer evidence、已推送 branch 與 draft PR 的任何修改、重寫、覆蓋或 rebase。

- **Read-only**: 所有未列為 implementation path 的 repository path；特別包括
  `src/deterministic_response_cache/response_reuse/outcomes.py`、所有既有 plan/spec/step/receipt/evidence、
  `docs/evolution-roadmap.md`、`docs/architecture/business-capability/architecture-brief.md`、
  `docs/architecture/business-capability/scene.js`、`docs/architecture/business-capability/index.html`、
  `tests/test_response_reuse_outcomes.py`、`tests/test_package_import.py`、`README.md`、`VERSION` 與 root exports。
- **Written**: 僅本 correction route 的 planning、review 與 validation evidence paths；implementation 不新增檔案。
- **Modified**: 僅上述四個 implementation paths，且僅可在 approved correction route 的 immutable subject 中修改。
- **Deleted**: none。

## Locked Decisions

- `NotFound`、`CacheStoreFailure`、`TokenWritten`、`CacheStoreWriteFailure` 是四個 immutable slotted VO，
  不繼承 `Exception`；`ResponseT` 和全部 channel 都不得是 `None`。
- `read` 僅以 `ResponseT`、`NotFound`、`CacheStoreFailure` 分別映射 `Hit`、`Miss`、`Unavailable`；`write` 僅以
  `TokenWritten`、`CacheStoreWriteFailure` 分別映射 `Cached(original_response)`、`NotCached(original_response)`。
- `ResponseReuseProtocol` 僅用 `match`／`case` 進行上述 mapping。`ResponseT` 由型別層指定、保持 opaque，且不新增
  runtime response validator：read 的所有 non-`None`、非 channel value 都是合法 `ResponseT` 並映射為 `Hit`；`None`
  與可偵測的明確 channel-contract violation 才 `TypeError`。write 僅允許兩個 VO channels，故其任何其他 return value
  都 `TypeError`。port 所拋出的 exception 不在 value-channel mapping 內，必須 propagate。
- CacheStore 仍是 Response Reuse 的 internal port；identity 與 response 仍是 opaque、未被重新解讀的 values。
- 本 correction 不影響 stable-library surface：`README.md`、`VERSION`、release notes、release timing 都是 no-change。
- 原 topic plan、spec、step、planning receipt、implementation subject、Tester evidence、Reviewer evidence、
  push 與 draft PR 都是 immutable provenance。此 correction 是獨立、candidate-bound route，不能覆寫或混入原 chain。

## Boundaries / Exclusions

- Plan-Creator 只寫此 plan 所列的五份 correction planning artifacts。Independent Plan-Reviewer 只寫 correction
  plan-review receipt。Implementer 只可 commit approved bounded candidates、implementation subject 與 evidence-only
  paths；Tester 只寫 factual Tester evidence；Independent Reviewer 只寫 review evidence。Human-only 的 PR review、
  merge、release、tag、post-merge 與 final summary 不得自動化。
- Implementation subject 不得新增、刪除或修改未列四 paths。任何 scope、contract、path、candidate 或 evidence drift
  必須停止並返回 Planner。

## Status / Allowed Transitions

- **Current**: `correction-plan-authoring`；五份 correction planning artifacts 尚待 Implementer 建立 single planning
  candidate commit。
- **Execution model**: correction planning candidate → independent Plan-Reviewer receipt → receipt-only commit →
  correction implementation subject → independent Tester evidence → Tester-evidence-only commit → Independent Reviewer
  evidence → Reviewer-evidence-only commit → Planner Phase 4.5 alignment → existing Human-authorized bounded publish
  → draft PR → Human review. 本 route 停在 Human boundary，未授權 merge 或 release。
- **Allowed transitions**:
  - `correction-plan-authoring` -> `correction-planning-candidate-committed`：Implementer 只提交本 plan 列出的五份
    correction planning artifacts，建立 non-merge immutable candidate。
  - `correction-planning-candidate-committed` -> `correction-plan-review-in-progress`：只可派 independent
    Plan-Reviewer 審同一 committed candidate。
  - `correction-plan-review-in-progress` -> `correction-plan-review-receipt-committed`：Plan-Reviewer 寫 receipt，
    Implementer 原樣以 sole single-file evidence-only commit 提交。
  - committed `approved` receipt，且其 full 40-hex `planning_candidate_commit` 等於 candidate SHA，才可由 Planner
    route 至 `correction-implementation-in-progress`；`needs-rework` 僅回到 Implementer 建立新 candidate。
  - correction implementation subject -> same-subject Tester → sole Tester-evidence commit → Independent Reviewer →
    sole Reviewer-evidence commit → Planner Phase 4.5。任何 `needs-rework` 必須建立新 immutable subject 並重跑完整 chain。
  - Phase 4.5 與既有 Human publish authorization 通過後，Implementer 才可 push correction branch 並開 draft PR；
    `pr-open` 後僅 Human 可 review、merge、release 或 post-merge。

## Artifact Paths

| Artifact | Exact path | Write owner | Decision authority and role |
| --- | --- | --- | --- |
| Correction requirements | `analysis/response-reuse-protocol/vo-channel-correction.requirements.md` | Plan-Creator | Business-intent guardrail for this correction candidate. |
| Correction technical specification | `analysis/response-reuse-protocol/vo-channel-correction.technical-spec.md` | Plan-Creator | Execution-facing source of truth. |
| Correction plan | `plan/response-reuse-protocol/response-reuse-protocol.vo-channel-correction.plan.md` | Plan-Creator | Canonical correction scope, workflow, and path contract. |
| Correction specification | `plan/response-reuse-protocol/response-reuse-protocol.vo-channel-correction.spec.md` | Plan-Creator | Acceptance and edge-case contract. |
| Correction step tracker | `plan/response-reuse-protocol/response-reuse-protocol.vo-channel-correction.step.md` | Plan-Creator; later Implementer only for `## Implementation Steps` markers | Correction progression truth. |
| Correction plan-review receipt | `plan/response-reuse-protocol/response-reuse-protocol.vo-channel-correction.plan-review-receipt.json` | Independent Plan-Reviewer | Sole writer; exact schema below; Implementer alone commits unchanged as sole single-file evidence-only commit. |
| Correction Tester evidence | `plan/response-reuse-protocol/response-reuse-protocol.vo-channel-correction.tester-evidence.json` | Tester | Same-subject factual evidence; independent Implementer commits unchanged as sole single-file evidence-only commit. |
| Correction implementation review evidence | `plan/response-reuse-protocol/response-reuse-protocol.vo-channel-correction.implementation-review-log.json` | Independent Reviewer | Consumes only committed same-subject passing Tester evidence; independent Implementer commits unchanged as sole single-file evidence-only commit. |
| Internal CacheStore port | `src/deterministic_response_cache/response_reuse/_cache_store.py` **Modify** | Implementer | VO channel contract only. |
| Response Reuse Protocol | `src/deterministic_response_cache/response_reuse/protocol.py` **Modify** | Implementer | `match`／`case` mapping only. |
| Protocol unit tests | `tests/test_response_reuse_protocol.py` **Modify** | Implementer | Direct-import branch mapping proof. |
| BC architecture text | `docs/business-capability-architecture.md` **Modify** | Implementer | Documentation of VO port channel behavior and existing BC boundary. |

All paths not in this table are prohibited. `README.md`, `VERSION`, `.github/copilot-instructions.md`, root exports,
the original topic artifacts/evidence, and all other files are no-change paths. No path is deleted.

### Correction evidence schemas

- The correction plan-review receipt is exactly one JSON object with only
  `schema_version`, `topic`, `planning_candidate_commit`, `verdict`, `blocking_issues`,
  `copilot_feedback_triage`, `recorded_by`. `schema_version` is integer `1`; `topic` is
  `response-reuse-protocol`; `planning_candidate_commit` is written only after review and equals the final full
  40-hex correction planning candidate SHA; `verdict` is `approved|needs-rework`; `blocking_issues` is a string
  array empty only for `approved`; `copilot_feedback_triage` has exactly `ADDRESS`, `DISCUSS`, `SKIP` arrays;
  `recorded_by` is `Independent Plan-Reviewer`.
- The correction Tester evidence is exactly one JSON object with only `schema_version`, `topic`,
  `implementation_subject_commit`, `status`, `commands`, `recorded_by`. It uses schema version `1`, this topic,
  a full 40-hex subject SHA, `passing|failing`, a non-empty `commands` array of objects each containing only a
  non-empty `command` string and integer `exit_code`, and `recorded_by: Tester`. `passing` requires every exit code
  `0`; `failing` requires at least one non-zero exit code.
- The correction implementation-review evidence is exactly one JSON object with only `schema_version`, `topic`,
  `implementation_subject_commit`, `tester_evidence_commit`, `verdict`, `blocking_issues`, `recorded_by`.
  Both SHA fields are full 40-hex and same-subject bound; `tester_evidence_commit` is the sole committed passing
  correction Tester evidence commit; `verdict` is `approved|needs-rework`; `blocking_issues` is a string array,
  empty only for `approved`; `recorded_by` is `Independent Reviewer`.

## Implementation Steps

1. In `_cache_store.py`, replace `Exception`/`None`-sentinel port semantics with the four locked immutable slotted
   VOs and exact generic read/write return unions; do not create a backend or alter public exports.
2. In `protocol.py`, replace exception-driven branching with `match`／`case` over exact read/write channel values;
   return the locked outcomes, preserve opaque object identity, treat every non-`None` nonchannel read value as
   `ResponseT`, and raise `TypeError` only for detectable channel-contract violations.
3. In `tests/test_response_reuse_protocol.py`, preserve direct imports and verify each valid channel, read `None`
   violation, write foreign-value `TypeError`, opaque non-`None` read-response passthrough, exception propagation,
   one port call, and original identity/response preservation.
4. In `docs/business-capability-architecture.md`, describe the VO channel contract without altering BC ownership or
   adding downstream implementation claims.

## Validation / Acceptance Checks

- Candidate planning commit changes exactly the five correction planning artifacts, no receipt/evidence/implementation path.
- Correction implementation subject changes exactly the four listed implementation paths; it is non-merge and distinct
  from the immutable original subject.
- Each VO is frozen and slotted, is not an `Exception`, and no read/write valid channel or `ResponseT` permits `None`.
- Tests prove the five mapping results, propagation of thrown exceptions, `TypeError` for read `None` and foreign
  write values, plus opaque passthrough for every non-`None` nonchannel read response.
- `ResponseReuseProtocol` uses `match`／`case` for all port outcome mapping; tests retain direct imports and introduce
  no `importlib`, `__import__`, or `sys.modules` substitution.
- Run `uv run ruff check src/deterministic_response_cache/response_reuse/_cache_store.py src/deterministic_response_cache/response_reuse/protocol.py tests/test_response_reuse_protocol.py`,
  `uv run pyright src/deterministic_response_cache/response_reuse/_cache_store.py src/deterministic_response_cache/response_reuse/protocol.py tests/test_response_reuse_protocol.py`,
  `uv run pytest tests/test_response_reuse_protocol.py -v`, `uv run pytest tests/test_package_import.py -v`, and
  `uv run pytest -v`; Tester records actual exit codes.
- Planner verifies each receipt/evidence is committed separately, same-subject bound, and approved before publish.

## Reviewer Handoff

```json
{
  "schema_version": 1,
  "topic": "response-reuse-protocol",
  "planning_candidate_commit": "<full 40-hex correction planning candidate SHA written after independent review>",
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "copilot_feedback_triage": {
    "ADDRESS": [],
    "DISCUSS": [],
    "SKIP": []
  },
  "recorded_by": "Independent Plan-Reviewer"
}
```

## Post-merge / release actions

No repository release action is authorized. After a Human merge, Human alone owns post-merge synchronization, release,
tagging, and final summary. This correction has no README or VERSION action.

## Open Questions / Unresolved Items

None. The channel vocabulary, mappings, path allowlist, evidence lifecycle, and Human boundary are locked.
