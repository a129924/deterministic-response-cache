# model-execution-protocol

## Goal / Outcome

- **Analysis-layer routing:** strict mode。`analysis/model-execution-protocol/technical-spec.md` 是 execution-facing source of truth；`analysis/model-execution-protocol/requirements.md` 是 business-intent guardrail。本 plan 的 implementation scope 只映射該 technical spec。
- 在外部 Response Reuse `Miss()` 後，交付可直接測試的同步 Model Execution 協調契約：使用既有 runtime，或在明確缺失時要求準備，然後執行一次 invocation；成功交回新 response，失敗交回不含 response 的明確結果。

## Scope

- **In scope:** 新增 Model Execution BC 的同步 ports、outcomes 與 protocol，以及一份 direct-import 行為測試；產出本 topic 的 analysis、plan、spec、step、Plan-Reviewer／Tester／Reviewer evidence。
- **Out of scope:** 任何既有 BC 或文件變更、跨 BC composition、真實 runtime/provider 接線、identity/runtime key 映射、response lookup/record、持久化、async、retry、timeout、cancellation 與並行政策。

## Locked Decisions

- 本 topic 是 D1 `non-trivial` Python work；只新增 defining-module public contracts，不建立穩定 facade 或 re-export。這次不改 README、VERSION、release metadata，亦不做 repository release。
- Model Execution 只接收並傳遞 opaque `runtime_request` 與 `invocation`；Identity BC 保有模型與完整請求身分的唯一 authority。Model Execution 不推得 `RuntimeReuseKey`，也不接收 `Miss` 作其內部判斷。
- `RuntimeAccess` port 的 resolve/prepare、`ModelInvoker` port 的 invoke 及其結果皆由 Model Execution 定義，作為可注入、provider-neutral 的本地契約。Loaded Runtime Cache PR #7 的具體 API 尚未鎖定；本 topic 不宣稱相容或直接 import 它。
- 明確 `RuntimeMissing` 才準備；`RuntimeUnavailable`、`RuntimePreparationFailed`、`InvocationFailed` 映射為三種不同 execution failure。port exception 原樣傳播，foreign/`None` result raise `TypeError`。成功 response 以同一 object 交回；失敗沒有 response。
- 不新增 package `__init__.py`、root export、provider-specific branch、實體 adapter 或 dependency。`model_execution/` 現有 `.gitkeep` 只是 topology marker，不當作功能 module。
- 實際 Loaded Runtime Cache／Provider Adapter 接線需在各自契約穩定後由獨立 topic 規劃；若相依契約與本地 port 語意不符，先回 Planner 確認 scope 與架構，不讓 Implementer 自行調整其他 BC。
- branch/worktree 固定為 `topic/model-execution-protocol` 與 `<repo-parent>/worktrees/model-execution-protocol`；`dev` 只作已驗證 admission base，不承載本 topic writer。

## Boundaries / Exclusions

- Identity BC 獨占 identity 規則；Response Reuse BC 獨占 lookup、eligibility、record 與其內部 CacheStore；Loaded Runtime Cache 獨占 runtime retention、Runtime Store／Registry 與實際 preparation；Provider Adapter 的具體 integration 仍是獨立可替換邊界。Model Execution 只協調已注入的 runtime 與 invocation ports。
- Plan-Creator 只寫五份 planning artifacts（初稿及其修訂）；Independent Plan-Reviewer 獨立寫 planning receipt；Implementer 只提交 bounded candidate、implementation subject 或原樣 evidence；Tester 寫 factual same-subject evidence；Independent Reviewer 消費 committed passing Tester evidence 後寫 review evidence。Observer 不改檔或自行判 gate。
- 既有 direct imports、fixtures、mocks 與 assertions 不得改寫；不使用 `importlib`、`__import__` 或 `sys.modules` 替代 direct-import regression。宣告路徑外的需求回 Planner；架構責任衝突時先確認架構文件。

## Status / Allowed Transitions

- **Current at this rework:** 第一個 five-path planning candidate `5f08dbc610a25fc4ae39eaaac20282f9a94e907d` 與 `needs-rework` receipt commit `64ab26c09831b47599543ce74c61733e052bcd44` 已提交；Planner 已派 Plan-Creator 修訂 planning artifacts。後續有效 candidate、phase 與 gate 由 Planner 依最新 committed evidence 判定，不由本段預填。
- **Execution model:** isolated worktree → five-path planning candidate → independent Plan-Reviewer receipt → Planner route → immutable four-path implementation subject → independent Tester evidence → independent Reviewer evidence → Planner Phase 4.5 alignment → 既有 Human authorization 下的 bounded publish/draft PR → Human review/merge。`pr-open` 之後 Human 才能 merge；本 topic 在 merge 後 terminal，無 release action。
- **Allowed transitions:**
  - `planned` → `planning-candidate-committed`：Implementer 只提交五份 initial planning artifacts。
  - `planning-candidate-committed` → `plan-review-in-progress`：Planner 派 Independent Plan-Reviewer 審查該 committed candidate。
  - `plan-review-in-progress` → `plan-review-receipt-committed`：Plan-Reviewer 寫對應 committed candidate 的三欄 receipt；Implementer 原樣以 sole evidence-only commit 提交。
  - `plan-review-receipt-committed` → `needs-rework` → `planning-rework-in-progress`：Planner 依 `needs-rework` verdict 派 Plan-Creator；Plan-Creator 只修訂 planning artifacts，Implementer 再提交新的 planning candidate 供獨立複審。
  - `planning-rework-in-progress` → `planning-candidate-committed`：Implementer 只提交修訂後的 planning artifacts，不混入 implementation 或 evidence。
  - `plan-review-receipt-committed` → `implementation-in-progress`：只有 Planner 驗證 committed `approved` receipt 與其 candidate 對應後，才派 Implementer 建 immutable subject。
  - `implementation-in-progress` → `tester-in-progress`：Implementer 只對四份 implementation paths 建 immutable subject；任何 step progression 另行提交，不混入 subject。
  - `tester-in-progress` → `review-ready`：Tester 只寫同 subject factual evidence；Implementer 以 sole evidence-only commit 原樣提交，且只有 committed `passing` 可供 Reviewer 消費。
  - `review-ready` → `reviewer-in-progress` → `approved|needs-rework`：Independent Reviewer 驗證同 topic、同 subject、passing Tester evidence；其 evidence 由 Implementer 原樣單獨提交。`needs-rework` 返回 Implementer，建立新 subject 並重跑 Tester/Reviewer。
  - `approved` → `publish-in-progress`：Planner Phase 4.5 alignment 與既有 Human authorization 均具備後，Implementer 才可 bounded commit/push/draft PR。
  - `publish-in-progress` → `pr-open` → `merged`：不得從 publish 直接跳 merge；Human 獨占 PR review 與 merge。`merged` 為本 topic terminal。

## Artifact Paths

| Artifact | Exact path | Write owner | Decision authority / role |
| --- | --- | --- | --- |
| Requirements | `analysis/model-execution-protocol/requirements.md` | Plan-Creator | Human mission 的 business-intent guardrail；initial candidate |
| Technical spec | `analysis/model-execution-protocol/technical-spec.md` | Plan-Creator | 本 topic execution-facing spec；initial candidate |
| Topic plan | `plan/model-execution-protocol/model-execution-protocol.plan.md` | Plan-Creator | Canonical topic workflow contract；initial candidate |
| Topic spec | `plan/model-execution-protocol/model-execution-protocol.spec.md` | Plan-Creator | 可驗證行為契約；initial candidate |
| Step tracker | `plan/model-execution-protocol/model-execution-protocol.step.md` | Plan-Creator 初建；後續各 action owner 更新 | 同 topic step progression；initial candidate |
| Planning review receipt | `plan/model-execution-protocol/model-execution-protocol.plan-review-receipt.json` | Independent Plan-Reviewer | 綁定 actual committed planning candidate；Implementer sole evidence commit |
| Runtime/invocation ports | `src/deterministic_response_cache/model_execution/ports.py` | Implementer | 本 plan/spec；immutable implementation subject |
| Port與 execution outcomes | `src/deterministic_response_cache/model_execution/outcomes.py` | Implementer | 本 plan/spec；immutable implementation subject |
| Execution protocol | `src/deterministic_response_cache/model_execution/protocol.py` | Implementer | 本 plan/spec；immutable implementation subject |
| Direct-import tests | `tests/test_model_execution_protocol.py` | Implementer | 本 plan/spec；immutable implementation subject |
| Tester evidence | `plan/model-execution-protocol/model-execution-protocol.tester-evidence.json` | Tester | Actual immutable subject/command/exit code；Implementer sole evidence commit |
| Implementation review log | `plan/model-execution-protocol/model-execution-protocol.implementation-review-log.json` | Independent Reviewer | Same-subject committed passing Tester evidence；Implementer sole evidence commit |

`README.md`、`VERSION`、`.github/copilot-instructions.md`、`pyproject.toml`、其他 BC、architecture docs 與 package initializers 均不在本 topic 寫入面。未列 path 必須停止並返回 Planner；本 topic 不宣告 correction-artifact extension。

## Python implementation metadata

### Non-goals

- 不整合或修改 Loaded Runtime Cache、Runtime Store／Registry。
- 不實作具體 provider、adapter、模型載入或模型執行 backend。
- 不建立 identity、runtime key 對應、Response Reuse lookup/record 或 end-to-end composition。
- 不加入 async、retry、timeout、concurrency、persistence、new dependency 或 compatibility shim。

### Current Context

`src/deterministic_response_cache/model_execution/` 只有預留 topology；Response Reuse 已有同步 `Miss()`，但沒有下游 execution module。PR #7 的 Loaded Runtime Cache 契約不在此 baseline 中，不能據此指定 import 或 adapter。Python 版本為 3.12，`pyproject.toml` 使用 strict pyright、ruff 與 pytest。

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

Written：`src/deterministic_response_cache/model_execution/ports.py`、`src/deterministic_response_cache/model_execution/outcomes.py`、`src/deterministic_response_cache/model_execution/protocol.py`、`tests/test_model_execution_protocol.py`。Modified/Deleted：none。五份 planning artifacts 與三份後續 evidence 的權責見 `Artifact Paths`。

### Test Plan

- Happy path: ready runtime 直接 invoke；missing 後 ready 再 invoke；response object identity 保留。
- Invalid input: 各 port 回傳 foreign/`None` result 時 `TypeError`，不進入後續動作。
- Edge case: unavailable 不 prepare；preparation failure 不 invoke；各階段 exception 原樣傳播。
- Regression: direct import、既有 Response Reuse/Identity tests、package topology 不受影響。
- Backward compatibility: 無既有 Model Execution API；既有 package import 與 direct-import test 保持通過。

### Risks

PR #7 runtime 契約未穩定，實際接線可能需要 adapter 或新的 cross-BC topic；不能把未確認 API 內建進此 topic。成功 response 對 Model Execution 保持 opaque；它不判定後續 Response Reuse record 是否接受。

### Rollback Plan

在 Human merge 前，由獲授權 Implementer 對本 topic 四個 implementation paths 與相關新 tests 作 bounded revert，保留已提交 planning/evidence provenance；不改其他 BC。merge 後由 Human 決定後續修復 topic。

## Implementation Steps

1. 新增 `src/deterministic_response_cache/model_execution/outcomes.py`，定義 technical spec 所列 frozen/slotted port 與 execution outcomes、三種 failure reasons，以及精確 union aliases。
2. 新增 `src/deterministic_response_cache/model_execution/ports.py`，定義同步 generic `RuntimeAccess` 與 `ModelInvoker` Protocol，僅 import 本 BC outcomes，不 import Identity、Response Reuse、Loaded Runtime Cache 或 Provider Adapter。
3. 新增 `src/deterministic_response_cache/model_execution/protocol.py`，依 technical spec 實作 constructor 與 `execute` 的 resolve → conditional prepare → invoke mapping，保留 opaque object identity、限制呼叫次數並拒絕 foreign/`None` results。
4. 新增 `tests/test_model_execution_protocol.py`，以 direct imports 與 typed fakes 驗證 ready、missing、unavailable、preparation failure、invocation failure、invalid port results、exception propagation 與不觸碰其他 BC 的界線。

## Validation / Acceptance Checks

- `uv run ruff check src/deterministic_response_cache/model_execution tests/test_model_execution_protocol.py`
- `uv run ruff format --check src/deterministic_response_cache/model_execution tests/test_model_execution_protocol.py`
- `uv run pyright`
- `uv run pytest tests/test_model_execution_protocol.py -q`
- `uv run pytest -q`
- Tester 在 immutable subject 建立後記錄上述實際 command/exit code；Reviewer 驗證 actual diff 僅含四個 implementation paths，direct imports 與五種情境均成立，沒有讀取 identity 規則、Response Reuse 或 PR #7 未確認 contract。Tester evidence 必須綁定同一 immutable subject；只有 committed passing evidence 可進 Reviewer。

## Reviewer Handoff

```json
{
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "copilot_feedback_triage": {"ADDRESS": [], "DISCUSS": [], "SKIP": []}
}
```

Independent Plan-Reviewer 僅審查已提交的 five-path candidate，依一般 topic 固定三欄契約填寫 verdict、含 `issue`／`file`／`fix` 的 blocking issues 與 Copilot feedback triage；Implementer 原樣以 sole evidence-only commit 提交 receipt。Planner 以 Git 提交歷史和 committed artifacts 驗證 receipt 所對應的 candidate，不以 receipt 額外欄位或聊天推定。此 handoff 不等於 implementation approval。

## Post-merge / release actions

本 topic 不要求 repository release、VERSION bump、README row 或 tag。`pr-open` 後 PR review/merge、post-merge sync 與 final summary 均由 Human 負責；`merged` 對本 topic 為 terminal。

## Open Questions / Unresolved Items

本 topic 自身的協調與 port contract 無未決實作選擇。PR #7 Loaded Runtime Cache 的實際 adapter/composition 及跨 BC 整合仍未鎖定，屬後續獨立 topic；若其最終契約與這裡的語意衝突，先返回 Planner/架構確認，不在 implementation 中推測。
