# response-reuse-eligibility-policy

## Goal / Outcome

- **Analysis-layer routing:** strict mode。`analysis/response-reuse-eligibility-policy/technical-spec.md` 是
  execution-facing source of truth；`analysis/response-reuse-eligibility-policy/requirements.md` 是
  business-intent guardrail。本 plan 100% 映射 technical spec，沒有使用未鎖定的 chat fallback。

### Goal

- 讓同步 `ResponseReuseProtocol.lookup` 在 CacheStore 讀得候選 response 後，以明確且 provider-neutral
  的 eligibility policy 決定是否可安全重用：allow 產生 `Hit(response)`，deny 產生既有 `Miss()`，並維持
  `Unavailable()`、identity opaque boundary 與 record contract。

## Scope

### Non-Goal

- 不建立 concrete/default/provider-specific policy、response schema、deny reason、deny metadata 或 new outcome。
- 不實作 identity rule、CacheStore backend/lifecycle、retention eligibility、TTL/expiry/invalidation/eviction、
  runtime、execution、provider 或 downstream orchestration。
- 不引入 async boundary、resource lifecycle、concurrency、retry、timeout、cancellation、metrics、tracing 或 I/O。
- 不新增 initializer、re-export、facade、dependency、README/VERSION/release/configuration change 或
  compatibility fallback。

### In-Scope

  - 新增 `ReuseAllowed`、`ReuseDenied`、`ReuseEligibilityDecision` 及 generic
    `ReuseEligibilityPolicy[ResponseT]`，且它們只存在於語意目錄
    `response_reuse/eligibility/policy.py`。
  - 令 `ResponseReuseProtocol` 要求 keyword-only `eligibility_policy`，並只在 successful read response
    path 執行一次 evaluate。
  - allow 維持既有 `Hit(response)`；deny 維持既有 `Miss()`；invalid policy result fail closed 為
    `TypeError`；policy exception 原樣傳播。
  - 更新 protocol 與 InMemory integration test construction，並新增 eligibility contract test。

### Out-Of-Scope

  - concrete/default policy、provider-specific rule、response schema、deny reason、deny metadata、新 outcome、
    allow-all fallback 或 compatibility shim。
  - Identity 建立、canonicalization、comparison、serialization、hashing、import 或任何 identity rule。
  - CacheStore backend、channel、persistence、retention、TTL、expiry、invalidation、eviction、capacity 或
    concurrency policy。
  - Loaded Runtime Cache、Model Execution、Provider Adapter、downstream orchestration、async、retry、timeout、
    metrics、tracing、network I/O、README、version、release、migration 或 configuration/dependency change。

### ReadOnly

  - `src/deterministic_response_cache/response_reuse/_cache_store.py`、
    `src/deterministic_response_cache/response_reuse/outcomes.py`、
    `src/deterministic_response_cache/response_reuse/stores/in_memory.py`。
  - `src/deterministic_response_cache/identity/**` 與其 tests、plans、analysis artifacts。
  - `docs/business-capability-architecture.md`、`docs/evolution-roadmap.md`、
    `docs/architecture/business-capability/architecture-brief.md`、
    `docs/architecture/business-capability/scene.js`、
    `docs/architecture/business-capability/index.html`。
  - `src/deterministic_response_cache/__init__.py`、所有既有或可新增的 package `__init__.py`、
    `README.md`、`VERSION`（若存在）、`pyproject.toml`、`uv.lock`、其他 version/configuration/dependency
    declaration、`tests/test_response_reuse_outcomes.py`、`tests/test_package_import.py`，以及除本 plan
    Written／Modified path 外的所有 paths。

### Written

  - `src/deterministic_response_cache/response_reuse/eligibility/policy.py`
  - `tests/test_response_reuse_eligibility.py`

### Modified

  - `src/deterministic_response_cache/response_reuse/protocol.py`
  - `tests/test_response_reuse_protocol.py`
  - `tests/response_reuse/test_in_memory_store.py`

### Deleted

none。

## Locked Decisions

- 本 topic 是 **D1 non-trivial** Python work，且是 **non-stable-library-affecting** topic：不修改
  README、VERSION、release metadata 或 stable public facade；direct defining-module imports 是唯一支援 surface。
- `eligibility/` 提供目錄語意，但不建立 `eligibility/__init__.py`、`response_reuse/__init__.py`、root
  re-export、facade、`__all__` gateway 或 `.gitkeep`。同一 stdlib-only leaf
  `deterministic_response_cache.response_reuse.eligibility.policy` 定義兩個 field-less frozen/slotted decision
  VOs、union 與 generic Protocol；不拆分 additional module。
- dependency direction 固定為 `protocol.py -> eligibility/policy.py`。policy module 不得 import protocol、
  outcomes、CacheStore、Identity 或其他 BC。
- constructor 固定為
  `ResponseReuseProtocol(store: CacheStore[IdentityT, ResponseT], *, eligibility_policy: ReuseEligibilityPolicy[ResponseT])`；
  policy 無 default、必須 keyword-only。這是被允許且有意識的 source break；所有 callers 顯式注入 policy。
- `ReuseEligibilityPolicy.evaluate(self, response: ResponseT, /) -> ReuseEligibilityDecision` 只接收 response。
  它不接收或解讀 identity、store、runtime、provider context。維持 Python 3.12 strict typing，不使用 `Any`、cast 或
  runtime identity inspection。
- lookup 呼叫 `read` 恰好一次。`NotFound()` -> `Miss()`、`CacheStoreFailure()` -> `Unavailable()`、invalid
  `None` read -> 既有固定訊息 `TypeError`、store exception 原樣傳播；這些 paths 的 policy call count 都是 `0`。
- 成功 read 的 response 只被 evaluate 一次、且以同一 object 傳入；`ReuseAllowed()` -> `Hit` 保留同一
  object，`ReuseDenied()` -> `Miss()` 且無 write／response leak／downstream work。`None`、`bool` 與 foreign
  result 一律 `TypeError`，不新增 exact message 且不得套用 truthiness；policy exception 原樣傳播。
- `record` 不呼叫 policy，保留 `Cached`／`NotCached` mapping、identity/response object preservation、foreign
  write-channel `TypeError` 與 exception propagation。
- 本 topic branch 固定為 universal admission authority 所要求的
  `topic/response-reuse-eligibility-policy`，而非一般 `git-branch-naming` pattern；它是已建立的 isolated
  worktree branch，且此 topic 不得重命名或另建 branch。

## Boundaries / Exclusions

- Identity BC 是唯一 identity authority；Response Reuse 只消費 opaque confirmed identity，不能建立、推測
  或重新解讀 identity。
- CacheStore 僅是 Response Reuse 的 internal persistence component；它不得成為頂層 BC，也不管理 identity、
  runtime 或模型執行。
- Response Reuse 不執行模型；Miss 只是 future boundary 交接，不能引入 Loaded Runtime Cache、Model
  Execution 或 Provider Adapter。
- Plan-Creator 只寫五份 initial planning artifacts；Independent Plan-Reviewer 只寫 plan-review receipt；
  Implementer 只提交已授權 bounded candidate、subject 或 evidence；Tester 只寫 factual same-subject evidence；
  Independent Reviewer 只寫 implementation-review evidence。Observer 不得改檔或自行 route gate。
- 所有 artifact/path、public API、module layout、typing、failure mapping 與 test-preservation drift 均停止並
  返回 Planner；不得以 chat、branch、summary、GOAL.md 或 `.github/agents/**` 補推 routing authority。

## Status / Allowed Transitions

- **Current**: `planning-candidate-committed`。initial exact-five non-merge planning candidate
  `cdf4c66ac8534a340118dca50b5e103f22335a25` 已提交並進入 independent plan review；它不等同 planning
  approval 或 implementation authorization。既有 committed plan-review receipt 的 `needs-rework` verdict
  仍是有效、不可歪曲的 review outcome；本修正必須形成新的 planning candidate 並重新獨立審核。
- **Execution model**: isolated topic worktree → five-path planning candidate → independent Plan-Reviewer
  receipt → Planner route → immutable five-path implementation subject → independent Tester evidence → independent
  Reviewer evidence → Planner Phase 4.5 alignment → existing Human-authorized bounded publish → draft PR → Human
  review and merge。此 topic 停在 Human merge boundary，沒有 release action。
- **Allowed transitions**:
  - `planned` -> `planning-candidate-committed`：只有 Implementer 可將恰好五份 initial planning artifacts
    提交為 non-merge planning candidate；不得混入 implementation 或 evidence path。
  - `planning-candidate-committed` -> `plan-review-in-progress`：只有 Planner 可依 committed candidate
    route Independent Plan-Reviewer。
  - `plan-review-in-progress` -> `plan-review-receipt-committed`：Independent Plan-Reviewer 寫 receipt；
    只有 Implementer 可原樣以 sole evidence-only commit 提交它。
  - `plan-review-receipt-committed` -> `needs-rework`：receipt verdict 為 `needs-rework`；Planner 只能將
    scoped rework route 給 Plan-Creator，形成新的 planning candidate 後重新獨立審核。
  - `plan-review-receipt-committed` -> `implementation-in-progress`：只有 committed receipt verdict 為
    `approved`、receipt 的 full SHA candidate binding 正確，且 Planner 選定後。
  - `implementation-in-progress` -> `tester-in-progress`：一個 non-merge immutable subject 恰好變更五個
    implementation paths 後。
  - `tester-in-progress` -> `tester-evidence-committed`：Tester 寫 factual same-subject evidence；獨立
    Implementer 原樣以 sole evidence-only commit 提交。
  - `tester-evidence-committed` -> `reviewer-in-progress`：僅限同 topic、同 subject、committed `passing`
    Tester evidence。
  - `tester-evidence-committed` -> `needs-rework`：同 topic、同 subject 的 committed `failing` Tester
    evidence 必須進入 needs-rework；Planner 只可 route bounded rework 給 Implementer。Implementer 必須建立
    新的 immutable implementation subject，並從獨立 Tester evidence 重新開始；只有該新 subject 的 committed
    passing Tester evidence 才可進入 Independent Reviewer evidence。失敗 subject 的 Tester 或 Reviewer evidence
    一律不得重用。
  - `reviewer-in-progress` -> `reviewer-evidence-committed`：Independent Reviewer 寫 evidence；獨立
    Implementer 原樣以 sole evidence-only commit 提交。
  - `reviewer-evidence-committed` -> `approved`：只有 Planner Phase 4.5 對 committed same-subject
    `approved` review evidence 完成 alignment。
  - `implementation-in-progress|reviewer-in-progress` -> `needs-rework`：以新的 immutable subject 重新走完整
    Tester/Reviewer chain；不得 reuse evidence。
  - `approved` -> `publish-in-progress`：需要既有 Human authorization；`publish-in-progress` -> `pr-open`
    由 Implementer bounded push 與 draft PR；`pr-open` -> `needs-rework|merged` 僅由 Human；`merged` -> terminal。

## Artifact Paths

| Artifact | Exact path | Write owner | Decision authority and role |
| --- | --- | --- | --- |
| Requirements analysis | `analysis/response-reuse-eligibility-policy/requirements.md` | Plan-Creator | Business-intent guardrail；planning candidate input。 |
| Technical specification | `analysis/response-reuse-eligibility-policy/technical-spec.md` | Plan-Creator | Execution-facing source of truth；本 plan 必須 100% 映射它。 |
| Topic plan | `plan/response-reuse-eligibility-policy/response-reuse-eligibility-policy.plan.md` | Plan-Creator | Canonical execution contract、scope/path allowlist 與 workflow gate。 |
| Topic specification | `plan/response-reuse-eligibility-policy/response-reuse-eligibility-policy.spec.md` | Plan-Creator | Acceptance、behavioral 與 error/edge contract。 |
| Step tracker | `plan/response-reuse-eligibility-policy/response-reuse-eligibility-policy.step.md` | Plan-Creator；later Implementer only for `## Implementation Steps` markers | Progression truth；只以 mirrored implementation checkboxes 判定 implementation completion。 |
| Plan-review receipt | `plan/response-reuse-eligibility-policy/response-reuse-eligibility-policy.plan-review-receipt.json` | Independent Plan-Reviewer | 僅在 committed planning candidate 後寫入；Implementer 原樣 sole evidence-only commit；同 candidate full SHA-bound `approved` receipt 才可由 Planner route。 |
| Eligibility policy | `src/deterministic_response_cache/response_reuse/eligibility/policy.py` **Write** | Implementer | 標準庫-only eligibility decisions、union、generic Protocol 與 leaf boundary。 |
| Response Reuse protocol | `src/deterministic_response_cache/response_reuse/protocol.py` **Modify** | Implementer | Required policy injection 與 lookup decision mapping；record contract preserved。 |
| Eligibility tests | `tests/test_response_reuse_eligibility.py` **Write** | Implementer | Direct-import eligibility value, typing and module-boundary regression proof。 |
| Protocol tests | `tests/test_response_reuse_protocol.py` **Modify** | Implementer | Constructor injection、lookup matrix、short-circuit、source-break 與 record no-policy proof。 |
| InMemory integration tests | `tests/response_reuse/test_in_memory_store.py` **Modify** | Implementer | 以 deterministic allow policy 保留既有 Response Reuse/InMemory integration assertions。 |
| Tester evidence | `plan/response-reuse-eligibility-policy/response-reuse-eligibility-policy.tester-evidence.json` | Tester | 只記同一 immutable subject 的 factual command/exit-code evidence；獨立 Implementer 原樣 sole evidence-only commit。 |
| Independent review evidence | `plan/response-reuse-eligibility-policy/response-reuse-eligibility-policy.implementation-review-log.json` | Independent Reviewer | 只消費 committed passing same-subject Tester evidence；獨立 Implementer 原樣 sole evidence-only commit。 |

`README.md`、VERSION/release metadata、`.github/copilot-instructions.md`（若存在）、all package initializers、
configuration/dependency declarations、architecture authority、所有 unlisted paths 均不得修改。任何未列 path、
deletion 或 new module 後綴都必須停止並返回 Planner。

### Review and evidence schemas

- Plan-review receipt 是一個 object，top-level keys 恰為 `schema_version`、`topic`、
  `planning_candidate_commit`、`verdict`、`blocking_issues`、`copilot_feedback_triage`、`recorded_by`。
  `schema_version` 是 integer `1`；`topic` 是 `response-reuse-eligibility-policy`；
  `planning_candidate_commit` 是 reviewer 在 review 後填入的 full 40-hex candidate SHA，planning artifacts
  不得預填；`verdict` 是 `approved|needs-rework`；`blocking_issues` 是 objects array，每項僅有 `issue`、
  `file`、`fix`；`copilot_feedback_triage` 恰有 `ADDRESS`、`DISCUSS`、`SKIP` arrays；`recorded_by` 是
  `Independent Plan-Reviewer`。
- Tester evidence 是 object，top-level keys 恰為 `schema_version`、`topic`、
  `implementation_subject_commit`、`status`、`commands`、`recorded_by`。`status` 是 `passing|failing`；
  `commands` 是 non-empty object array，entries 恰有 non-empty string `command` 與 integer `exit_code`；
  `passing` 要求所有 exit code 是 `0`，`failing` 至少一個非 `0`；`recorded_by` 是 `Tester`。
- Independent review evidence 是 object，top-level keys 恰為 `schema_version`、`topic`、
  `implementation_subject_commit`、`tester_evidence_commit`、`verdict`、`blocking_issues`、`recorded_by`。
  兩個 commit fields 都是同一 subject 相關 full 40-hex SHA；`tester_evidence_commit` 必為 sole committed
  passing Tester evidence commit；`verdict` 是 `approved|needs-rework`；approved 時 `blocking_issues` 是空
  string array；`recorded_by` 是 `Independent Reviewer`。

## Python implementation metadata

### Non-goals

- 不建立 concrete/default/provider-specific policy、response schema、deny reason、deny metadata 或 new outcome。
- 不實作 identity rule、CacheStore backend/lifecycle、retention eligibility、TTL/expiry/invalidation/eviction、
  runtime、execution、provider 或 downstream orchestration。
- 不引入 async boundary、resource lifecycle、concurrency、retry、timeout、cancellation、metrics、tracing 或 I/O。
- 不新增 initializer、re-export、facade、dependency、README/VERSION/release/configuration change 或
  compatibility fallback。

### Current Context

`src/deterministic_response_cache/response_reuse/protocol.py` 目前只將 CacheStore `NotFound`、
`CacheStoreFailure`、`None` 及 response 映射成 lookup outcomes，constructor 只接收 store；它尚未判定已命中
response 是否可安全回傳。`outcomes.py`、`_cache_store.py` 和 InMemory adapter 已是可用 contract，且所有現有
tests 都採 direct imports。架構文件已指定 Response Reuse 承擔 safe reuse decision，並維持 Identity opaque
authority 與 future BC separation。

### Requirements

1. 100% 實作 `analysis/response-reuse-eligibility-policy/technical-spec.md` 的 policy/module/API/lookup/
   record contract，維持 Python 3.12 strict pyright compatibility。
2. 只有兩個 explicit immutable slotted decisions 可成為合法 evaluate result；所有 invalid result fail closed，
   不使用 bool/truthiness。
3. 所有 lookup channel 的 read/evaluate call count、identity/response object identity、outcome mapping 及
   exception propagation 必須可由 tests 驗證。
4. `record` 的每個現有 branch 都不得呼叫 policy，且既有 test direct import、fixture、mock 與 assertion 行為
   維持。
5. immutable implementation subject 必須恰好含五個 declared implementation paths，並維持所有 read-only
   paths、no initializer/no re-export/no dynamic-import contract。

### Decisions

- Async-planning status: exempt — cite exemption evidence: 本 topic 只新增同步 Protocol decision 與純 synchronous CacheStore lookup mapping；沒有 async boundary、resource lifecycle、external I/O concurrency choice、timeout、cancellation、retry 或 sync-to-async conversion。
- Module/package placement: 新 code 僅在
  `src/deterministic_response_cache/response_reuse/eligibility/policy.py`，作為 implicit namespace directory
  的 standard-library-only leaf；`protocol.py` 單向 import 它。
- New public API: yes — direct-module-only `ReuseAllowed`、`ReuseDenied`、`ReuseEligibilityDecision` 與
  `ReuseEligibilityPolicy[ResponseT]`；policy signature 是
  `evaluate(self, response: ResponseT, /) -> ReuseEligibilityDecision`。沒有 initializer/root/facade export。
- Interface changes: yes — `ResponseReuseProtocol.__init__` 變成 required keyword-only
  `eligibility_policy: ReuseEligibilityPolicy[ResponseT]`；`lookup`、`record` 與 outcome unions 不變。
- Breaking changes allowed: yes — constructor omission 與 positional policy 都必須得到 Python `TypeError`；
  所有 current callers 必須明確注入 policy，且不提供 fallback。
- New dependencies: no — 僅 `dataclasses` 與 `typing` 等 Python standard library；不修改 dependency/configuration。
- Error-handling strategy: policy deny 是 value decision `Miss()`；invalid decision 是 `TypeError`，不固定新訊息；
  policy/store exception 原樣傳播；`NotFound`、`CacheStoreFailure`、invalid `None` read 維持既有 mapping。
- Typing strategy: Python 3.12 generic syntax、fully typed Protocol、frozen slotted dataclasses、explicit union；
  禁止 `Any`、cast、truthiness decision、runtime identity inspection。

### Public Contract / API Changes

```python
from deterministic_response_cache.response_reuse.eligibility.policy import (
    ReuseAllowed,
    ReuseDenied,
    ReuseEligibilityDecision,
    ReuseEligibilityPolicy,
)
from deterministic_response_cache.response_reuse.protocol import ResponseReuseProtocol

protocol = ResponseReuseProtocol(
    store,
    eligibility_policy=policy,
)
```

`ReuseAllowed()` 與 `ReuseDenied()` 是唯一有效 policy decision values。`ResponseReuseProtocol` 的 new
keyword-only dependency 是 intentional source break；它只在 successful read response 上呼叫
`evaluate(response)`。沒有新的 lookup/record outcome、package export、Identity/CacheStore public contract、
provider contract 或 default policy。

### Affected Files / Modules

**Written implementation paths:**

- `src/deterministic_response_cache/response_reuse/eligibility/policy.py`
- `tests/test_response_reuse_eligibility.py`

**Modified implementation paths:**

- `src/deterministic_response_cache/response_reuse/protocol.py`
- `tests/test_response_reuse_protocol.py`
- `tests/response_reuse/test_in_memory_store.py`

**Read-only verification paths:**

- `src/deterministic_response_cache/response_reuse/_cache_store.py`
- `src/deterministic_response_cache/response_reuse/outcomes.py`
- `src/deterministic_response_cache/response_reuse/stores/in_memory.py`
- `tests/test_response_reuse_outcomes.py`
- `tests/test_package_import.py`
- `pyproject.toml`
- `docs/business-capability-architecture.md`

### Test Plan

- **Happy path:** policy allow on a store response yields `Hit` holding the exact response and has exactly one
  evaluate call; deterministic allow policy preserves existing InMemory record/lookup integration.
- **Invalid input:** policy `None`、`True`、`False` 及 foreign-object decisions each yield `TypeError` without
  truthiness；omitted/positional policy constructor uses Python `TypeError`。
- **Edge case:** policy deny produces `Miss` without response leak/write；`NotFound`、`CacheStoreFailure`、invalid
  `None` read and store exception each short-circuit with zero policy calls；policy exception is unchanged。
- **Regression:** frozen/slotted decision value semantics、direct defining-module imports、structural Protocol typing、
  existing invalid read/write channel and exception-propagation assertions remain intact。
- **Backward compatibility:** immutable subject diff is exact-five paths；all existing callers explicitly inject
  policy；no package initializer/re-export/dynamic-import/configuration/README/version/future-BC path changes。

### Risks

- 使用 `if decision` 會錯把 foreign truthy/falsy values 視為允許或拒絕，因此必須 explicit match 兩種
  decision type。
- 在 `NotFound`、`CacheStoreFailure`、invalid `None` 或 read exception 之前呼叫 policy，會混淆 storage
  failure/miss semantics 並違反 zero-call contract。
- 新增 initializer 或 re-export 會意外擴張 package public surface；把 policy 拆到額外 module 會違反
  locked semantic leaf layout。
- 忘記把既有 callers 改成 explicit policy injection 會使 intentional constructor source break 造成 type/test
  drift。

### Rollback Plan

完整 revert immutable exact-five-path implementation subject：移除
`src/deterministic_response_cache/response_reuse/eligibility/policy.py` 與
`tests/test_response_reuse_eligibility.py`，並同時還原 protocol 與兩份 existing tests。不得保留部分
constructor/API/module-layout change；所有 read-only paths 不需要 rollback。

## Implementation Steps

1. Create `src/deterministic_response_cache/response_reuse/eligibility/policy.py` as the sole stdlib-only eligibility leaf; add frozen/slotted field-less `ReuseAllowed` and `ReuseDenied`, their explicit union, and generic `ReuseEligibilityPolicy.evaluate(response, /)` without importing protocol, outcomes, CacheStore, Identity, or another BC.
2. Modify `src/deterministic_response_cache/response_reuse/protocol.py` to import the policy contracts one way, require keyword-only `eligibility_policy`, perform the exact successful-read allow/deny/invalid-decision mapping once, and preserve every non-response lookup channel plus all record behavior.
3. Create `tests/test_response_reuse_eligibility.py` with defining-module direct imports that verify decision frozen/slotted/distinct value semantics, union and structural Protocol typing, and the leaf module boundary without dynamic imports.
4. Modify `tests/test_response_reuse_protocol.py` so every constructor injects a typed fake policy while preserving its direct imports, fixtures, mocks, and assertions; add allow, deny, invalid result, policy exception, short-circuit, source-break, response identity, and record zero-call coverage.
5. Modify `tests/response_reuse/test_in_memory_store.py` only to inject a deterministic allow policy at `ResponseReuseProtocol` construction, retaining every existing store behavior, fixture, direct import, and assertion.
6. Run the declared lint, strict type, targeted, full-suite, exact-subject, package-layout, direct-import, and diff-whitespace validations; Tester later records actual commands and exit codes only after the immutable implementation subject exists.

## Validation / Acceptance Checks

### TestCase

| TestCase | Expected outcome | Policy calls |
| --- | --- | ---: |
| `ReuseAllowed` semantics | frozen、slotted、無 `__dict__`、同型 value equality | N/A |
| `ReuseDenied` semantics | frozen、slotted、無 `__dict__`、同型 value equality | N/A |
| Decision distinction | allow/deny 是不同 type 且不相等 | N/A |
| Module boundary | defining-module direct import；只有 `protocol -> policy` dependency | N/A |
| Store response + allow | `Hit` 持有同一 response object | 1 |
| Store response + deny | `Miss()`、無 write、無 response leak/downstream work | 1 |
| Policy returns `None` | `TypeError`，不驗證新 error text | 1 |
| Policy returns `True` / `False` | `TypeError`，不得使用 truthiness | 1 |
| Policy returns foreign object | `TypeError` | 1 |
| Policy raises | 同一 exception 原樣傳播 | 1 |
| `NotFound()` | `Miss()` | 0 |
| `CacheStoreFailure()` | `Unavailable()` | 0 |
| Invalid `None` read | 既有固定訊息的 `TypeError` | 0 |
| Store read raises | 同一 exception 原樣傳播 | 0 |
| Every `record` branch | 維持既有 result 與 assertions | 0 |
| Omitted policy | Python `TypeError` | N/A |
| Positional policy | Python `TypeError` | N/A |
| InMemory integration | 原有 record/lookup/store assertions 通過 | per lookup |

```bash
uv run ruff check src/deterministic_response_cache/response_reuse/eligibility/policy.py src/deterministic_response_cache/response_reuse/protocol.py tests/test_response_reuse_eligibility.py tests/test_response_reuse_protocol.py tests/response_reuse/test_in_memory_store.py
uv run pyright
uv run pytest tests/test_response_reuse_eligibility.py tests/test_response_reuse_protocol.py tests/response_reuse/test_in_memory_store.py tests/test_response_reuse_outcomes.py tests/test_package_import.py -v
uv run pytest -v
test "$(git diff-tree --no-commit-id --name-only -r <implementation-subject-sha> | sort)" = "$(printf '%s\n' 'src/deterministic_response_cache/response_reuse/eligibility/policy.py' 'src/deterministic_response_cache/response_reuse/protocol.py' 'tests/response_reuse/test_in_memory_store.py' 'tests/test_response_reuse_eligibility.py' 'tests/test_response_reuse_protocol.py' | sort)"
test ! -e src/deterministic_response_cache/response_reuse/eligibility/__init__.py
test ! -e src/deterministic_response_cache/response_reuse/__init__.py
! rg -n -e 'importlib' -e '__import__' -e 'sys\.modules' tests/test_response_reuse_eligibility.py tests/test_response_reuse_protocol.py tests/response_reuse/test_in_memory_store.py
git diff --check <implementation-subject-parent-sha> <implementation-subject-sha>
```

The exact-five diff check occurs after the implementation subject commit; all other validations run in the isolated
topic worktree. Tester writes actual factual results; planning artifacts must not prefill SHA, exit code, verdict or
outcome facts.

## Reviewer Handoff

```json
{
  "schema_version": 1,
  "topic": "response-reuse-eligibility-policy",
  "planning_candidate_commit": "<reviewed candidate final full 40-hex SHA written by Independent Plan-Reviewer after review>",
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

The Independent Plan-Reviewer is the sole receipt writer. Implementer alone commits the unchanged receipt as a
sole evidence-only commit. This handoff does not create implementation approval until the receipt is committed,
same-candidate SHA-bound, `approved`, and selected by Planner.

## Post-merge / release actions

No repository release action is authorized or required. After Human merge of the draft PR, Human alone owns
post-merge synchronization, release, tagging and final summary. This non-stable topic changes neither README nor
VERSION.

## Open Questions / Unresolved Items

None. The first-version rule is intentionally the injected provider-neutral policy decision itself; concrete
eligibility rules, retention eligibility, lifecycle policy, composition/DI and all future BC work are separately
planned topics.
