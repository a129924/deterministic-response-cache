# model-execution-protocol

## Goal / Outcome

- **Analysis-layer routing:** strict mode。`analysis/model-execution-protocol/technical-spec.md` 是 execution-facing source of truth；`analysis/model-execution-protocol/requirements.md` 是 business-intent guardrail。本 plan 的 implementation scope 只映射該 technical spec。
- 在外部 Response Reuse `Miss()` 後，交付可直接測試的同步 Model Execution 協調契約：使用既有 runtime，或在明確缺失時要求準備，然後執行一次 invocation；成功交回新 response，失敗交回不含 response 的明確結果。

## Scope

- **In scope:** 已交付的 Model Execution BC 同步 ports、outcomes、protocol 與 direct-import 行為測試；Human-directed PR thread `PRRT_kwDOUJTij86lAh0Z` 的 exact-five architecture status correction；本 correction 的 Plan-Reviewer／Tester／Reviewer evidence。
- **Out of scope:** exact-five 以外的既有 BC 或文件變更、Python/test 行為變更、跨 BC composition、真實 runtime/provider 接線、identity/runtime key 映射、response lookup/record、持久化、async、retry、timeout、cancellation 與並行政策。

## Locked Decisions

- 本 topic 是 D1 `non-trivial` Python work；只新增 defining-module public contracts，不建立穩定 facade 或 re-export。這次不改 README、VERSION、release metadata，亦不做 repository release。
- Model Execution 只接收並傳遞 opaque `runtime_request` 與 `invocation`；Identity BC 保有模型與完整請求身分的唯一 authority。Model Execution 不推得 `RuntimeReuseKey`，也不接收 `Miss` 作其內部判斷。
- `RuntimeAccess` port 的 resolve/prepare、`ModelInvoker` port 的 invoke 及其結果皆由 Model Execution 定義，作為可注入、provider-neutral 的本地契約。Loaded Runtime Cache PR #7 的具體 API 尚未鎖定；本 topic 不宣稱相容或直接 import 它。
- 明確 `RuntimeMissing` 才準備；`RuntimeUnavailable`、`RuntimePreparationFailed`、`InvocationFailed` 映射為三種不同 execution failure。port exception 原樣傳播，foreign/`None` result raise `TypeError`。成功 response 以同一 object 交回；失敗沒有 response。
- `protocol.py` 固定由 `execute`、`_prepare_and_invoke`、`_invoke` 分工，各 method 只用一層 `match/case`，不得巢狀。`execute` 只 match resolve 的 ready/missing/unavailable，分別呼叫 `_invoke`、`_prepare_and_invoke`、回傳 runtime unavailable failure；`_prepare_and_invoke` 只 match prepare 的 ready/preparation failed，分別呼叫 `_invoke`、回傳 preparation failure；`_invoke` 只 match invoke 的 succeeded/failed，分別回傳保留原 response object 的 `Executed`、invocation failure。各 method 的 wildcard case 對 `None` 或契約外結果 raise `TypeError`；port exception 原樣傳播、不 retry，每次 `execute` 對各 port 最多呼叫一次。
- 不新增 package `__init__.py`、root export、provider-specific branch、實體 adapter 或 dependency。`model_execution/` 現有 `.gitkeep` 只是 topology marker，不當作功能 module。
- 實際 Loaded Runtime Cache／Provider Adapter 接線需在各自契約穩定後由獨立 topic 規劃；若相依契約與本地 port 語意不符，先回 Planner 確認 scope 與架構，不讓 Implementer 自行調整其他 BC。
- branch/worktree 固定為 `topic/model-execution-protocol` 與 `<repo-parent>/worktrees/model-execution-protocol`；`dev` 只作已驗證 admission base，不承載本 topic writer。
- PR thread `PRRT_kwDOUJTij86lAh0Z` 的 status correction 只更新架構敘述：provider-neutral、同步、可注入的 Model Execution coordination contracts（ports、outcomes、protocol）已實作；Loaded Runtime Cache 實際 wiring／retention/backend、具體 Provider Adapter、cross-BC composition，以及 Response Reuse `Miss`／execution result handoff integration 仍是 future。
- correction implementation subject 只能修改五份 architecture docs；Python、tests 與 public contract 相對 PR HEAD `9a3460b6e4412384ed7e3426ebc32820a46818e6` 必須不變。`scene.js` 是 `index.html` 固定 generated markers 間 scene block 的 source，兩者必須 byte-for-byte mirror。

## Boundaries / Exclusions

- Identity BC 獨占 identity 規則；Response Reuse BC 獨占 lookup、eligibility、record 與其內部 CacheStore；Loaded Runtime Cache 獨占 runtime retention、Runtime Store／Registry 與實際 preparation；Provider Adapter 的具體 integration 仍是獨立可替換邊界。Model Execution 只協調已注入的 runtime 與 invocation ports。
- Plan-Creator 只寫五份 planning artifacts（初稿及其修訂）；Independent Plan-Reviewer 獨立寫對應 planning receipt；Implementer 只提交 bounded candidate、exact-five correction subject 或原樣 evidence；Tester 寫 factual same-subject evidence；Independent Reviewer 消費 committed passing Tester evidence 後寫 review evidence。Observer 不改檔或自行判 gate。
- 既有 direct imports、fixtures、mocks 與 assertions 不得改寫；不使用 `importlib`、`__import__` 或 `sys.modules` 替代 direct-import regression。宣告路徑外的需求回 Planner；架構責任衝突時先確認架構文件。

## Status / Allowed Transitions

- **Immutable predecessor provenance / current amendment:** active predecessor planning candidate `b2847eb2e7ac0ed65a5bef8c33d13cb3248aee99`、approved amendment receipt `5145a59be17a3845da074d88e8530b59bfb45e57`、implementation subject `868df3b338e022371a55a2125b270a52ba1c6874`、passing Tester evidence `12bdfb1b5350ee71e3af70df38a462ce9286fba5`、approved Reviewer evidence `dee1740b73d0274445d0c3967272d0475d82e779` 與 current PR HEAD `9a3460b6e4412384ed7e3426ebc32820a46818e6` 均保留 immutable provenance。Human 已指示處理 thread `PRRT_kwDOUJTij86lAh0Z`，Planner 已將 phase 判為 `planning-amendment-pending` 並派 Plan-Creator；舊 Q／Reviewer evidence 與舊 Phase 4.5 結果都不是本 correction 的 approval。新 planning candidate SHA 與 verdict 不預填。
- **Execution model:** Human-directed PR-comment amendment → five-path planning candidate → independent Plan-Reviewer → sole receipt commit → Planner route → immutable exact-five docs subject → independent Tester → sole Tester-evidence commit → Independent Reviewer → sole Reviewer-evidence commit → Planner Phase 4.5 alignment → push same PR → same-thread reclassification → Implementer bounded reply/resolve only if classified addressed-and-resolvable → Human review/merge。
- **Allowed transitions:**
  - `planned` → `planning-candidate-committed`：Implementer 只提交五份 initial planning artifacts。
  - `planning-candidate-committed` → `plan-review-in-progress`：Planner 派 Independent Plan-Reviewer 審查該 committed candidate。
  - `plan-review-in-progress` → `plan-review-receipt-committed`：Plan-Reviewer 寫對應 committed candidate 的三欄 receipt；Implementer 原樣以 sole evidence-only commit 提交。
  - `plan-review-receipt-committed` → `needs-rework` → `planning-rework-in-progress`：Planner 依 `needs-rework` verdict 派 Plan-Creator；Plan-Creator 只修訂 planning artifacts，Implementer 再提交新的 planning candidate 供獨立複審。
  - `planning-rework-in-progress` → `planning-candidate-committed`：Implementer 只提交修訂後的 planning artifacts，不混入 implementation 或 evidence。
  - `plan-review-receipt-committed`（舊 candidate 的 `approved`）→ `human-directed-amendment-pending` → `planning-amendment-in-progress`：只依 Human 本次明確指示，由 Plan-Creator 在本 topic 已宣告的 planning paths 修訂；舊 candidate/receipt 不得改寫或作新修訂的 routing approval。
  - `planning-amendment-in-progress` → `planning-candidate-committed`：Implementer 只提交本次修訂的 planning artifacts，形成新的 immutable planning candidate；五份 planning artifacts 以該 commit 的 tree 為審查基準，不混入 implementation、舊 receipt 或新 evidence。
  - `planning-candidate-committed` → `plan-review-in-progress` → `plan-review-receipt-committed`（amendment）：Independent Plan-Reviewer 只審新 committed candidate，寫本次專用三欄 receipt；Implementer 原樣以 sole evidence-only commit 提交，且該 commit 的第一 parent 必須是新 candidate commit。Planner 以 Git 的 candidate commit/tree、五份 planning paths/blob 及 sole receipt commit 驗證同一 candidate 的 binding，依 verdict re-route；`needs-rework` 回 Plan-Creator，僅新 `approved` 可再派實作。新 receipt 不覆寫舊 receipt，且任一時點最多一個 active candidate。
  - `plan-review-receipt-committed` → `implementation-in-progress`：只有 Planner 驗證當前 candidate 的 committed `approved` receipt 且沒有待審 amendment，才派 Implementer 建 immutable subject。
  - `implementation-in-progress` → `tester-in-progress`：Implementer 只對四份 implementation paths 建 immutable subject；任何 step progression 另行提交，不混入 subject。
  - `tester-in-progress` → `review-ready`：Tester 只寫同 subject factual evidence；Implementer 以 sole evidence-only commit 原樣提交，且只有 committed `passing` 可供 Reviewer 消費。
  - `review-ready` → `reviewer-in-progress` → `approved|needs-rework`：Independent Reviewer 驗證同 topic、同 subject、passing Tester evidence；其 evidence 由 Implementer 原樣單獨提交。`needs-rework` 返回 Implementer，建立新 subject 並重跑 Tester/Reviewer。
  - `approved` → `publish-in-progress`：Planner Phase 4.5 alignment 與既有 Human authorization 均具備後，Implementer 才可 bounded commit/push/draft PR。
  - `publish-in-progress` → `pr-open` → `merged`：不得從 publish 直接跳 merge；Human 獨占 PR review 與 merge。`merged` 為本 topic terminal。
  - `pr-open` → `human-directed-architecture-amendment-pending` → `planning-amendment-in-progress`：僅針對 exact thread `PRRT_kwDOUJTij86lAh0Z`，由 Plan-Creator 修改五份既有 planning artifacts；predecessor evidence 全部 frozen。
  - `planning-amendment-in-progress` → `planning-candidate-committed` → `plan-review-in-progress`：Implementer 只提交五份 planning artifacts；Independent Plan-Reviewer 只審該 committed candidate。
  - `plan-review-in-progress` → `architecture-amendment-receipt-written` → `architecture-amendment-receipt-committed`：Plan-Reviewer 寫專用 receipt，Implementer 原樣以 sole evidence-only commit 提交；`needs-rework` 回 Plan-Creator，只有 Planner 驗證 committed `approved` receipt 才能 route correction Implementer。
  - `architecture-amendment-receipt-committed` → `architecture-correction-in-progress` → `architecture-correction-subject-committed`：Implementer 建立且只建立 exact-five docs-only immutable subject，不改 Python/tests。
  - `architecture-correction-subject-committed` → `tester-in-progress` → `correction-tester-evidence-committed`：Tester 寫同 subject factual evidence，Implementer 原樣以 sole evidence-only commit 提交；只有 committed `passing` 可供 Reviewer 消費。
  - `correction-tester-evidence-committed` → `reviewer-in-progress` → `correction-review-evidence-committed`：Independent Reviewer 審同一 subject 與 committed passing evidence，Implementer 原樣以 sole evidence-only commit 提交；`needs-rework` 返回 correction Implementer 並以新 subject 重跑 Tester／Reviewer。
  - `correction-review-evidence-committed` → `phase-4.5-alignment` → `same-pr-push`：只有 Planner 對新 candidate、subject、Tester/Reviewer evidence 完成 alignment 且既有 Human authorization仍適用時，Implementer 才 push 到同一 PR；不得 force push、ready/merge。
  - `same-pr-push` → `same-thread-reclassification` → `comment-resolve|human-check`：Independent Reviewer 重新分類 exact thread；只有明確 `addressed-and-resolvable` 才由 Implementer 留 bounded reply 並 resolve exact thread，否則停止 human-check。

## Artifact Paths

| Artifact | Exact path | Write owner | Decision authority / role |
| --- | --- | --- | --- |
| Requirements | `analysis/model-execution-protocol/requirements.md` | Plan-Creator | Human mission 的 business-intent guardrail；initial candidate |
| Technical spec | `analysis/model-execution-protocol/technical-spec.md` | Plan-Creator | 本 topic execution-facing spec；initial candidate |
| Topic plan | `plan/model-execution-protocol/model-execution-protocol.plan.md` | Plan-Creator | Canonical topic workflow contract；initial candidate |
| Topic spec | `plan/model-execution-protocol/model-execution-protocol.spec.md` | Plan-Creator | 可驗證行為契約；initial candidate |
| Step tracker | `plan/model-execution-protocol/model-execution-protocol.step.md` | Plan-Creator 初建；後續各 action owner 更新 | 同 topic step progression；initial candidate |
| Planning review receipt | `plan/model-execution-protocol/model-execution-protocol.plan-review-receipt.json` | Independent Plan-Reviewer | 綁定 actual committed planning candidate；Implementer sole evidence commit |
| Amendment planning review receipt | `plan/model-execution-protocol/model-execution-protocol.amendment-plan-review-receipt.json` | Independent Plan-Reviewer | 僅審本次新 committed planning candidate；Implementer sole evidence commit，Planner 以 Git 驗證 binding |
| Architecture correction plan | `plan/model-execution-protocol/model-execution-protocol.plan.md` | Plan-Creator | 本 parent plan 的本次 amendment section 即 correction-plan authority；不新增 standalone correction plan |
| Architecture correction step | `plan/model-execution-protocol/model-execution-protocol.step.md` | Plan-Creator 初建；後續各 action owner 更新 | 本 parent step 的 reopened route 即 correction-step authority；不新增 standalone correction step |
| Architecture amendment review receipt | `plan/model-execution-protocol/model-execution-protocol.architecture-amendment-plan-review-receipt.json` | Independent Plan-Reviewer | 綁定本次 committed five-path planning candidate；Implementer 原樣 sole evidence commit |
| Runtime/invocation ports | `src/deterministic_response_cache/model_execution/ports.py` | Implementer | 本 plan/spec；immutable implementation subject |
| Port與 execution outcomes | `src/deterministic_response_cache/model_execution/outcomes.py` | Implementer | 本 plan/spec；immutable implementation subject |
| Execution protocol | `src/deterministic_response_cache/model_execution/protocol.py` | Implementer | 本 plan/spec；immutable implementation subject |
| Direct-import tests | `tests/test_model_execution_protocol.py` | Implementer | 本 plan/spec；immutable implementation subject |
| Tester evidence | `plan/model-execution-protocol/model-execution-protocol.tester-evidence.json` | Tester | Actual immutable subject/command/exit code；Implementer sole evidence commit |
| Implementation review log | `plan/model-execution-protocol/model-execution-protocol.implementation-review-log.json` | Independent Reviewer | Same-subject committed passing Tester evidence；Implementer sole evidence commit |
| Architecture source | `docs/business-capability-architecture.md` | Correction Implementer | exact-five subject；同步已實作 coordination 與 future integration 狀態 |
| Evolution roadmap | `docs/evolution-roadmap.md` | Correction Implementer | exact-five subject；同步能力完成度與後續順序 |
| Architecture brief | `docs/architecture/business-capability/architecture-brief.md` | Correction Implementer | exact-five subject；同步文字權責與狀態 |
| Architecture scene source | `docs/architecture/business-capability/scene.js` | Correction Implementer | exact-five subject；`index.html` generated scene 的 source |
| Architecture viewer | `docs/architecture/business-capability/index.html` | Correction Implementer | exact-five subject；marker 間 scene block 必須 exact mirror |
| Architecture correction Tester evidence | `plan/model-execution-protocol/model-execution-protocol.architecture-correction-tester-evidence.json` | Tester | 綁定 exact-five immutable subject；Implementer 原樣 sole evidence commit |
| Architecture correction implementation review | `plan/model-execution-protocol/model-execution-protocol.architecture-correction-implementation-review-log.json` | Independent Reviewer | 僅消費 committed passing correction Tester evidence；Implementer 原樣 sole evidence commit |

`README.md`、`VERSION`、`.github/copilot-instructions.md`、`pyproject.toml`、其他 BC、未列 architecture docs、Python/tests 與 package initializers 均不在本 correction 寫入面。未列 path 必須停止並返回 Planner。上述 parent plan/step 加三個專用 evidence paths 合成此 correction 的 exact five-artifact extension。

### Architecture correction evidence schemas

三份新 evidence 都是單一 JSON object，top-level keys 必須恰為下列 schema 所列；SHA 必須為完整 lowercase 40-hex。缺鍵、多鍵、縮寫 SHA、topic/thread/correction/subject 不一致均 fail closed。

Architecture amendment Plan-Reviewer receipt：

```json
{
  "schema_version": 1,
  "topic": "model-execution-protocol",
  "correction_id": "model-execution-protocol/pr-comment-architecture-status",
  "thread_id": "PRRT_kwDOUJTij86lAh0Z",
  "planning_candidate_commit": "<40-hex five-planning-path candidate>",
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "recorded_by": "Independent Plan-Reviewer"
}
```

`approved` 要求空 `blocking_issues`；`needs-rework` 要求至少一個 non-empty string。Plan-Reviewer 只寫不 commit；Implementer 必須原樣以 sole one-path evidence-only commit 提交，第一 parent 為該 planning candidate。Planner 驗證 candidate 與 receipt commit 的 Git binding 後才可 route。

Architecture correction Tester evidence：

```json
{
  "schema_version": 1,
  "topic": "model-execution-protocol",
  "correction_id": "model-execution-protocol/pr-comment-architecture-status",
  "thread_id": "PRRT_kwDOUJTij86lAh0Z",
  "implementation_subject_commit": "<40-hex exact-five docs subject>",
  "status": "passing|failing",
  "commands": [{"command": "<non-empty command>", "exit_code": 0}],
  "recorded_by": "Tester"
}
```

`commands` 是 non-empty array，各 entry 只能有 non-empty string `command` 與 integer `exit_code`；所有 exit codes 為 `0` 才能 `passing`，`failing` 至少一個 non-zero。Tester 只寫不 commit；Implementer 原樣以 sole one-path evidence-only commit 提交，第一 parent 為 implementation subject。

Architecture correction implementation-review log：

```json
{
  "schema_version": 1,
  "topic": "model-execution-protocol",
  "correction_id": "model-execution-protocol/pr-comment-architecture-status",
  "thread_id": "PRRT_kwDOUJTij86lAh0Z",
  "implementation_subject_commit": "<same 40-hex exact-five docs subject>",
  "tester_evidence_commit": "<40-hex sole passing evidence commit>",
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "recorded_by": "Independent Reviewer"
}
```

Reviewer 只可消費已提交、同 topic/thread/correction/subject 且 `passing` 的 Tester evidence；否則不得寫 log。`approved` 要求空 blockers，`needs-rework` 要求至少一個 non-empty string。Reviewer 只寫不 commit；Implementer 原樣以 sole one-path evidence-only commit 提交，第一 parent 為 Tester evidence commit。

## Python implementation metadata

### Non-goals

- 不整合或修改 Loaded Runtime Cache、Runtime Store／Registry。
- 不實作具體 provider、adapter、模型載入或模型執行 backend。
- 不建立 identity、runtime key 對應、Response Reuse lookup/record 或 end-to-end composition。
- 不加入 async、retry、timeout、concurrency、persistence、new dependency 或 compatibility shim。

### Current Context

predecessor PR HEAD `9a3460b6e4412384ed7e3426ebc32820a46818e6` 已包含 Model Execution 同步 coordination modules 與 tests；五份架構來源仍把整個 capability 呈現為 future，因此需要狹窄 status correction。PR #7 的 Loaded Runtime Cache 契約不在此 topic scope，不能據此指定 import 或 adapter。Python 版本為 3.12，`pyproject.toml` 使用 strict pyright、ruff 與 pytest。

### Requirements

一次 `execute` 至多各呼叫一次 resolve、prepare、invoke；prepare 只處理明確 missing。runtime unavailable、preparation failure 與 invocation failure 各有不含 response 的可辨識結果；成功保留同一 opaque response。所有情境可用 direct imports 與 typed test doubles 驗收。

### Decisions

- Async-planning status: exempt — repo 的 Response Reuse 與本 Mission 均要求同步 protocol；本 topic 不引入 async-capable dependency、I/O、並行、timeout 或 cancellation。
- Module/package placement: 新增 `model_execution/ports.py`、`outcomes.py`、`protocol.py`；不新增 initializer。
- New public API: 兩個 defining-module generic ports、port outcome VOs/unions、`Executed`/`ExecutionFailed` 與 `ModelExecutionProtocol.execute`；精確形狀見同 topic technical spec。
- Interface changes: 不修改任何既有 public interface；新契約僅供直接 module import。
- Breaking changes allowed: 無既有 Model Execution API，故無既有 caller migration 或相容層。
- New dependencies: 無；僅 Python standard library。
- Error-handling strategy: 宣告的 operation failure 映射成 `ExecutionFailed(reason)`；foreign/`None` port result 為 `TypeError`；port exception 原樣傳播。
- Typing strategy: Python 3.12 generic `Protocol`、明確 union 與 frozen/slotted result VOs；不以 `Any`、動態載入或 runtime identity introspection 代替泛型邊界。

### Public Contract / API Changes

`ModelExecutionProtocol(runtime_access, invoker).execute(runtime_request, invocation)` 同步回傳 `Executed(response) | ExecutionFailed(reason)`。`RuntimeAccess.resolve/prepare` 與 `ModelInvoker.invoke` 的合法結果集合、`ExecutionFailureReason` 三個值及 invalid-result 行為均由 technical spec 固定；這是 Model Execution 自有 port，不是 PR #7 的預填 API。

### Affected Files / Modules

Predecessor Written：`src/deterministic_response_cache/model_execution/ports.py`、`src/deterministic_response_cache/model_execution/outcomes.py`、`src/deterministic_response_cache/model_execution/protocol.py`、`tests/test_model_execution_protocol.py`，本 correction 保持其 blobs 不變。Correction Modified：五份 exact architecture paths。Written：三份專用 evidence 依各 phase 產生。Deleted：none。五份 planning artifacts 與各份 evidence 的權責見 `Artifact Paths`。

### Test Plan

- Happy path: ready runtime 直接 invoke；missing 後 ready 再 invoke；response object identity 保留。
- Invalid input: 各 port 回傳 foreign/`None` result 時 `TypeError`，不進入後續動作。
- Edge case: unavailable 不 prepare；preparation failure 不 invoke；各階段 exception 原樣傳播。
- Regression: direct import、既有 Response Reuse/Identity tests、package topology 不受影響。
- Backward compatibility: 無既有 Model Execution API；既有 package import 與 direct-import test 保持通過。

### Risks

PR #7 runtime 契約未穩定，實際接線可能需要 adapter 或新的 cross-BC topic；不能把未確認 API 內建進此 topic。成功 response 對 Model Execution 保持 opaque；它不判定後續 Response Reuse record 是否接受。

### Rollback Plan

在 Human merge 前，任何 rollback 或 superseding correction 只可由獲授權 Implementer 限定於五個 declared architecture paths，必須保持 predecessor `src/`／`tests/` blobs 不變，並保留所有已提交的 planning／evidence provenance；不得授權回退 Python implementation 或 test paths。merge 後任何修復或回退均由 Human 決定，automatic workflow 停止。

## Implementation Steps

1. 新增 `src/deterministic_response_cache/model_execution/outcomes.py`，定義 technical spec 所列 frozen/slotted port 與 execution outcomes、三種 failure reasons，以及精確 union aliases。
2. 新增 `src/deterministic_response_cache/model_execution/ports.py`，定義同步 generic `RuntimeAccess` 與 `ModelInvoker` Protocol，僅 import 本 BC outcomes，不 import Identity、Response Reuse、Loaded Runtime Cache 或 Provider Adapter。
3. 新增 `src/deterministic_response_cache/model_execution/protocol.py`，依 technical spec 以 `execute`、`_prepare_and_invoke`、`_invoke` 各自單層 `match/case` 實作 resolve → conditional prepare → invoke mapping，保留 opaque object identity、限制呼叫次數並拒絕 foreign/`None` results。
4. 新增 `tests/test_model_execution_protocol.py`，以 direct imports 與 typed fakes 驗證 ready、missing、unavailable、preparation failure、invocation failure、invalid port results、exception propagation 與不觸碰其他 BC 的界線。
5. 在 approved architecture-amendment receipt 與 Planner route 後，只修改 exact-five architecture sources，使五者一致區分已實作的 provider-neutral coordination contracts 與仍 future 的 runtime/provider/cross-BC handoff integration。
6. 將更新後 `scene.js` 的完整內容同步到 `index.html` 固定 generated markers 之間，維持 byte-for-byte mirror；不改 viewer 其他程式、幾何或互動行為。

## Validation / Acceptance Checks

- `uv run ruff check src/deterministic_response_cache/model_execution tests/test_model_execution_protocol.py`
- `uv run ruff format --check src/deterministic_response_cache/model_execution tests/test_model_execution_protocol.py`
- `uv run pyright`
- `uv run pytest tests/test_model_execution_protocol.py -q`
- `uv run pytest -q`
- Tester 在 immutable subject 建立後記錄上述實際 command/exit code；Reviewer 驗證 actual diff 僅含四個 implementation paths、三個 method 各只用一層 `match/case` 且分工符合 technical spec、direct imports 與五種情境均成立，沒有讀取 identity 規則、Response Reuse 或 PR #7 未確認 contract。Tester evidence 必須綁定同一 immutable subject；只有 committed passing evidence 可進 Reviewer。
- correction Tester 另驗證 `git diff-tree --no-commit-id --name-status -r <subject>` 恰為五個 `M` paths、`git diff --exit-code 9a3460b6e4412384ed7e3426ebc32820a46818e6 <subject> -- src tests` 為零、五份來源語意一致、technical spec 所列 Python stdlib mirror command 通過、`git diff --check <subject>^ <subject>` 與 `uv run pytest -q` exit code 為零。實際 `<subject>` 只能在 commit 後填入 evidence，不得預填。

## Reviewer Handoff

```json
{
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "copilot_feedback_triage": {"ADDRESS": [], "DISCUSS": [], "SKIP": []}
}
```

此三欄 handoff 是 predecessor general planning review 的 frozen contract。architecture correction 的 Independent Plan-Reviewer 僅審查新提交的 five-path planning candidate，並改用上方 `architecture-amendment-plan-review-receipt.json` exact schema；不得覆寫任何舊 receipt。Implementer 原樣以 sole evidence-only commit 提交，第一 parent 必須是新 candidate commit；Planner 以 Git 驗證 binding。兩種 handoff 都不等於 implementation approval。

## Post-merge / release actions

本 topic 不要求 repository release、VERSION bump、README row 或 tag。`pr-open` 後 PR review/merge、post-merge sync 與 final summary 均由 Human 負責；`merged` 對本 topic 為 terminal。

## Open Questions / Unresolved Items

本 correction 的語意、exact-five paths、mirror 機制與 evidence route 已鎖定，無未決實作選擇。PR #7 Loaded Runtime Cache 的實際 adapter/composition 及跨 BC 整合仍未鎖定，屬後續獨立 topic；若其最終契約與這裡的語意衝突，先返回 Planner/架構確認，不在 correction 中推測。
