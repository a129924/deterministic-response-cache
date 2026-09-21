# loaded-runtime-cache

## Goal / Outcome

Analysis strict mode：`analysis/loaded-runtime-cache/technical-spec.md` 是 execution-facing source of truth，
`requirements.md` 是 business-intent guardrail；本 plan 完整映射兩者及 Human 確認的 locked decisions。

建立獨立、protocol-first 的 Loaded Runtime Cache BC。完成後 repository 具備 local `RuntimeReuseKey`、generic
synchronous Runtime Registry／Retention ports，以及 reusable-runtime lookup／retention outcome contracts；它不建立
concrete backend、DI composition 或 runtime lifecycle。

本 topic 的 Git lineage label 是 Human-authorized exception `feat/andrew/runtime-reuse-protocol`。它只標示
lineage，不能建立第二 topic、替代 slug、選擇 candidate 或作為 routing evidence。

## Scope

| Field | Contract |
| --- | --- |
| In-Scope | local immutable opaque `RuntimeReuseKey`（identity-only key semantics）；`RuntimeRegistry[RuntimeT]`、`RuntimeRetention[RuntimeT]` Protocol；`Available`、`Missing`、`Unavailable`、`Retained`、`NotRetained` outcomes；locked module taxonomy、direct-module contract tests、alias-aware BC-independence regression、已提交 architecture/dataflow evidence 的重用，以及 C8 兩個 isolated executable RED assertions 與 fresh T8/V8 evidence chain。 |
| Out-Of-Scope | Identity BC direct import、`ModelIdentity -> RuntimeReuseKey` mapping／mapper／ACL implementation、concrete Registry／Retention／lookup class、DI、backend、runtime initialization／download／unload／execution、provider management、Response Reuse、Model Execution、Provider Adapter、TTL、eviction、locking、concurrency、retry、timeout、metrics、tracing。 |
| Non-Goal | root re-export、package facade、dynamic import、`sys.modules` substitution、`service.py`、`utils.py`、`common.py`、README、version、release、tag、merge、post-merge。 |

## Locked Decisions

- Identity BC 與 Loaded Runtime Cache 是獨立 BC，任一方向均不得 import 對方 module。`ModelIdentity` 與
  `RuntimeReuseKey` 是語意不同的 local types，不得 re-export、duplicate 或跨 BC 假裝共用。
- integration／ACL boundary 決定 `RuntimeReuseKey` token／mapping；Loaded Runtime Cache 只 opaque pass-through，
  不讀取、拆解、序列化、字串化、hash、canonicalize、驗證、推測或重新詮釋 key。token 不是 public API，不能以
  `str`／hash 代替，且 `repr` 不得暴露 token。key 採 instance identity semantics；unhashable 或 custom-equality
  token 的 equality／hash 不得被呼叫。
- `RuntimeRegistry.lookup` 回傳 `RuntimeT | None`，`retain` 回傳 `None`；`RuntimeRetention.retain` 回傳
  `Retained[RuntimeT] | NotRetained[RuntimeT]`。port-owned expected signal 是
  `RuntimeRegistryLookupUnavailable`；outcome-owned `Unavailable` 與此 signal 分離，本 topic 不增加 mapper。
- module placement 固定為 `<bc>/<topic>/<child-topic>/<module>.py`。這是 non-stable-library topic，沒有 README
  row、VERSION bump、release note 或 release action。
- architecture-path overlap 僅在 Human review／merge coordination 處理；不授權改另一 topic artifacts。
- C5→V3 的 architecture/dataflow gate 與 production source contracts 是 frozen provenance。C8 必須在既有 source
  ancestor 上重用它們，不能回寫、重建或聲稱 source-absent 的 historical RED→green 順序。
- C8 的兩個 isolated executable RED assertions 必須在同一 immutable assertion subject 覆蓋五項 regression：opaque／unhashable／
  custom-equality token 不觸發 equality/hash；直接 `importlib.import_module`；直接 `__import__`；`importlib` 或
  `builtins.__import__` alias／module-alias；以及 LRC `ModelIdentity`／Identity `RuntimeReuseKey` duplicate semantic
  type。BC parser 必須解析 aliases；assertions 在 current source ancestor 執行並以 T8 如實收集，不能假稱
  expected-nonzero、green-source authorization 或以 mapper、shared type 或跨 BC import 規避。

## Boundaries / Exclusions

| Category | Exact contract |
| --- | --- |
| ReadOnly | `src/deterministic_response_cache/identity/**`、`response_reuse/**`、`model_execution/**`、`provider_adapter/**`、root `__init__.py`、`loaded_runtime_cache/.gitkeep`、五個 existing source modules、`pyproject.toml`、`README.md`、version metadata、workflow contracts、`.github/agents/**`、五份 architecture authority 與既有 Archify artifacts。 |
| Written | C8 versioned T8／V8 evidence paths；C8 不新增 source、architecture 或 Archify artifact。 |
| Modify | 僅 `tests/test_loaded_runtime_cache_contracts.py` 與 `tests/test_loaded_runtime_cache_bc_independence.py`，各加入一個 isolated executable assertion。 |
| Deleted | 無；不得刪除 `.gitkeep`、existing tests 或既有 artifacts。 |

## Status / Allowed Transitions

- **Current**: `planning-candidate-committed`。C8 是以現行 source ancestor 為基礎的五-file planning correction；
  C5→V3 是 frozen provenance，不能作 C8 routing。C8 candidate 已提交，且 planning artifacts 不預填 candidate SHA 或
  receipt。下一 gate 是 independent Plan-Reviewer review pending；只有該 reviewer 的 approved receipt 被獨立提交後，
  才可建立兩-path isolated-assertion implementation subject。
- **Execution model**: C8 committed planning candidate → independent Plan-Reviewer receipt → receipt-only commit →
  two-path isolated executable assertion subject against existing source ancestor → versioned T8 Tester evidence →
  T8 evidence-only commit → versioned V8 independent Reviewer evidence → V8 evidence-only commit → Planner Phase 4.5
  alignment → bounded PR thread classification／reply／resolution → Human review／merge。
- **Allowed transitions**: `planned` → `planning-candidate-committed` → `plan-review-in-progress` →
  `plan-review-receipt-committed` → `implementation-in-progress` → `tester-in-progress` →
  `tester-evidence-committed` → `reviewer-in-progress` → `reviewer-evidence-committed` → `approved` →
  `publish-in-progress` → `pr-open` → `merged` (Human only). A `needs-rework` verdict returns only to a new
  planning candidate or a new immutable implementation subject as applicable; no stale evidence may route.

## Artifact Paths

| Artifact | Path | Write owner | Decision authority and role |
| --- | --- | --- | --- |
| Requirements | `analysis/loaded-runtime-cache/requirements.md` | Plan-Creator | Business-intent guardrail; planning candidate only. |
| Technical specification | `analysis/loaded-runtime-cache/technical-spec.md` | Plan-Creator | Execution-facing contract; planning candidate only. |
| Topic plan | `plan/loaded-runtime-cache/loaded-runtime-cache.plan.md` | Plan-Creator | Canonical executable contract; planning candidate only. |
| Topic specification | `plan/loaded-runtime-cache/loaded-runtime-cache.spec.md` | Plan-Creator | Acceptance and TestCase contract. |
| Step tracker | `plan/loaded-runtime-cache/loaded-runtime-cache.step.md` | Plan-Creator; later Implementer only for implementation checkmarks | Topic-local progression truth. |
| Plan-review receipt | `plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<planning-candidate-40-hex-sha>.json` | Independent Plan-Reviewer writes; Implementer commits unchanged alone | SHA-bound normal-plan verdict. |
| Existing source contracts | five locked `src/deterministic_response_cache/loaded_runtime_cache/runtime_reuse/**` modules | None — ReadOnly | C5 green subject provenance; C8 must not modify them. |
| Contract tests | `tests/test_loaded_runtime_cache_contracts.py` **Modify** | Implementer | Add exactly one isolated executable assertion; no existing assertion behavior changes. |
| BC-independence tests | `tests/test_loaded_runtime_cache_bc_independence.py` **Modify** | Implementer | Add exactly one isolated executable assertion; preserve alias-aware regression behavior. |
| Existing architecture/dataflow | five listed architecture authority files and `docs/architecture/loaded-runtime-cache/**` | None — ReadOnly | C5 architecture provenance reused without edit or re-delivery. |
| Tester evidence (T8) | `plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<implementation-subject-40-hex-sha>.json` | Tester writes; Implementer commits unchanged alone | New SHA-bound factual validation of the C8 assertion subject. |
| Independent review evidence (V8) | `plan/loaded-runtime-cache/loaded-runtime-cache.implementation-review-log-<implementation-subject-40-hex-sha>.json` | Independent Reviewer writes; Implementer commits unchanged alone | New SHA-bound record consuming committed passing T8 evidence. |

Every unlisted path is read-only. The fixed-name legacy plan-review receipt from the abandoned lineage is historical,
frozen provenance only: it is not an artifact of C8, must not be created or overwritten, and has no routing
authority. Each current or successor candidate uses only the SHA-bound template above; no candidate SHA is prefilled.
Legacy fixed-name T1／V1 evidence, including the `6110cb…` Tester and `44e477…` Reviewer lineage, is likewise frozen:
T3／V3 and C5 provenance must never be overwritten, reused, or inferred as C8 facts.

### Review and evidence schemas

- SHA-bound Plan-review receipt is one JSON object with exactly `verdict`, `blocking_issues`,
  `copilot_feedback_triage`. `verdict` is `approved|needs-rework`; `blocking_issues` is an array of objects with
  exactly `issue`, `file`, `fix`; triage has exactly `ADDRESS`／`DISCUSS`／`SKIP` arrays. Only a committed approved
  receipt for the committed candidate can authorize implementation routing.
- C8 creates no RED-evidence JSON. Its isolated executable assertions run against the existing source ancestor; their
  actual command results belong only in T8. A failing result is `failing` T8, never an expected-failing authorization.
- Tester evidence is exactly one JSON object whose top-level keys are `schema_version`, `topic`,
  `implementation_subject_commit`, `status`, `commands`, `recorded_by` and no others. `schema_version` is integer
  `1`; `topic` is `loaded-runtime-cache`; `implementation_subject_commit` is the same immutable subject's full
  40-character lowercase hexadecimal SHA; `status` is `passing|failing`; `commands` is a non-empty array whose every
  entry has only non-empty string `command` and integer `exit_code`; `recorded_by` is `Tester`. `passing` requires
  every exit code to be `0`; `failing` requires at least one non-zero exit code. Malformed, uncommitted,
  cross-topic, cross-subject, abbreviated-SHA, legacy fixed-name path, or status/command-inconsistent evidence fails
  closed. T8 is written only at its versioned SHA-bound artifact path.
- Independent review evidence is exactly one JSON object whose top-level keys are `schema_version`, `topic`,
  `implementation_subject_commit`, `tester_evidence_commit`, `verdict`, `blocking_issues`, `recorded_by` and no
  others. `schema_version` is integer `1`; `topic` is `loaded-runtime-cache`; both subject references are full
  40-character lowercase hexadecimal SHAs; `tester_evidence_commit` is the sole evidence-only commit containing
  committed same-topic, same-subject passing Tester evidence; `verdict` is `approved|needs-rework`; `blocking_issues`
  is a string array that is empty exactly for `approved` and non-empty for `needs-rework`; `recorded_by` is
  `Independent Reviewer`. Reviewer may consume only that committed passing T8 evidence; malformed, legacy fixed-name,
  or unmatched input fails closed and must not produce V8 Reviewer evidence. V8 is written only at its versioned
  SHA-bound artifact path.

## Python implementation metadata

### Non-goals

- 不建立 `ModelIdentity -> RuntimeReuseKey` mapper、ACL implementation，或任何跨 BC import。
- 不建立 Registry／Retention concrete class、DI composition、backend，或 runtime lifecycle／provider management。
- 不新增 root re-export、package facade、dynamic import、`sys.modules` substitution、dependency、README、VERSION、
  release、tag、merge 或 post-merge action。

### Current Context

Identity BC、Response Reuse、Model Execution 與 Provider Adapter 都是相鄰但獨立的 bounded context；本 topic 的
five source contracts、architecture authority 與 Archify dataflow 已存在於 current source ancestor。`pyproject.toml`
已鎖定 Python 3.12、strict Pyright、Ruff 與 pytest。C8 是新的 planning correction candidate，必須由獨立
Plan-Reviewer 審查；architecture-path overlap 保留給 Human review／merge coordination，不能由本 topic writer 擴張
路徑或自行解決。

### Requirements

1. 只在 locked taxonomy 定義 local `RuntimeReuseKey`、同步 generic Protocol 與 immutable outcomes；不建立 consumer
   或 concrete implementation。
2. Registry key 與 runtime payload 都必須以同一 instance opaque handoff；沒有 key-field inspection、mapping 或
   runtime lifecycle side effect；key token 不可成為 `str`／hash API 或由 `repr` 暴露，且 unhashable/custom-equality
   token 不得被 key equality/hash 呼叫。
3. expected registry lookup failure、`Missing`、`Unavailable`、unexpected exception 與 retention outcomes 必須可區分。
4. C8 只修改兩個 declared test paths，保留既有 source、architecture／Archify evidence 與 direct-module imports。
5. C8 不回寫歷史 RED→green 門檻；它在 current source ancestor 建立可執行的 isolated assertions，並以新的 T8/V8
   same-subject evidence chain 做事實驗證。

### Decisions

- Async-planning status: exempt — cite exemption evidence: this topic defines synchronous pure Protocol and immutable
  contracts only; it introduces no async boundary, resource lifecycle, concurrency, external I/O, timeout, retry,
  cancellation, or runtime ownership.
- Module/package placement: exactly `loaded_runtime_cache/runtime_reuse/{registry,lookup,retention}/` under `src/`,
  with each responsibility in its locked direct module.
- New public API: yes, direct-module contract APIs only: `RuntimeReuseKey`, `RuntimeRegistry`, `RuntimeRetention`,
  `RuntimeRegistryLookupUnavailable`, and the declared outcome types; no root or package facade export.
- Interface changes: no existing interface changes; add the synchronous `RuntimeRegistry[RuntimeT]` and
  `RuntimeRetention[RuntimeT]` Protocol contracts exactly as specified.
- Breaking changes allowed: no; existing package and direct-import behavior remain unchanged.
- New dependencies: no; use only the existing Python standard library and declared development tooling.
- Error-handling strategy: Registry raises only its expected `RuntimeRegistryLookupUnavailable` signal for expected
  lookup operational failure; no mapper is introduced, `Missing` is never used for failure, and unexpected exceptions
  propagate unchanged.
- Typing strategy: Python 3.12 strict Pyright, generic `Protocol` and `TypeVar`, immutable typed value/outcome
  contracts, no `Any`, cast, runtime introspection, dynamic import, or cross-BC type import.

### Public Contract / API Changes

New direct-module APIs are limited to the five declared modules. `RuntimeRegistry[RuntimeT]` exposes
`lookup(key: RuntimeReuseKey) -> RuntimeT | None` and `retain(key: RuntimeReuseKey, runtime: RuntimeT) -> None`.
`RuntimeRetention[RuntimeT].retain(key, runtime)` returns `Retained[RuntimeT] | NotRetained[RuntimeT]`. These are new
protocol contracts, not concrete behavior, dependency composition, or a stable root-package facade.

### Affected Files / Modules

**Written:** only versioned T8／V8 evidence in `Artifact Paths`.

**Modified:** only the two declared test modules, each with one isolated executable assertion.

**ReadOnly:** all Identity, Response Reuse, Model Execution, Provider Adapter, root-package, five existing source
modules, architecture/Archify artifacts, configuration, workflow-contract and `.github/agents/**` paths enumerated
in `Boundaries / Exclusions`.

### Test Plan

- **Happy path:** typed fakes prove Registry hit and same-instance `RuntimeReuseKey` pass-through; retention outcomes
  retain the original runtime instance.
- **Invalid input:** no key validation is in scope; a non-expected fake exception propagates unchanged rather than
  being classified.
- **Edge case:** missing (`None`), expected `RuntimeRegistryLookupUnavailable`, `Unavailable`, and retention failure
  remain distinct without a signal-to-outcome mapper.
- **Regression:** the two C8 isolated executable assertions must directly exercise all five regressions: opaque/unhashable/custom-equality
  token identity-only semantics; direct `importlib.import_module`; direct `__import__`; `importlib` or
  `builtins.__import__` alias/module-alias use; and LRC `ModelIdentity`／Identity `RuntimeReuseKey` duplicate semantic
  types. The alias-aware parser rejects those cross-BC paths while `tests/test_package_import.py` preserves existing
  import behavior.
- **Sequencing:** C5 architecture/dataflow and green-source commits are frozen reusable provenance. After C8's approved
  receipt, only the two test paths form the C8 assertion subject; fresh T8 then V8 bind that same subject. No new
  expected-nonzero or green-source gate exists.
- **Backward compatibility:** the implementation subject contains only declared paths; no root facade, initializer,
  dependency/configuration, or adjacent-BC change appears.

### TestCase

The executable Given/When/Then scenarios and Error / Edge Cases are maintained in
`plan/loaded-runtime-cache/loaded-runtime-cache.spec.md`; its scenarios are the acceptance source for the two declared
test modules and the Archify evidence gate.

### Risks

- A concrete consumer or backend would collapse the protocol-only boundary and expand scope.
- Treating expected operational failure as `None` would conflate unavailable registry state with a miss.
- The five architecture authority files overlap another topic's declared paths; only Human coordinates merge-time
  resolution, and this topic must not rewrite that ownership decision.

### Rollback Plan

Revert only the C8 two-test assertion subject and its successor evidence commits without modifying C5→V3 frozen
provenance. Leave read-only source, architecture, `.gitkeep`, root package, configuration, adjacent BCs and planning /
evidence history untouched.

## Implementation Steps

1. Preserve C5→V3 source and architecture provenance unchanged; verify it only as read-only context.
2. After C8's independently approved, committed Plan-Reviewer receipt, add one isolated executable assertion to each
   declared test module. The single C8 subject contains exactly those two modified paths, no production source,
   architecture, Archify artifact or evidence.
3. Run the locked checks against that committed subject. The assertions are executable validation against the current
   source ancestor, not expected-failing historical RED evidence.
4. Tester writes factual T8 for that exact subject; an Implementer commits it unchanged alone.
5. Independent Reviewer consumes only committed passing T8 and writes V8; an Implementer commits it unchanged alone.
6. Planner then performs Phase 4.5 alignment. Only its pass authorizes independent PR-thread classification; no C8
   action resolves F Human-check or authorizes merge.

## Validation / Acceptance Checks

- Run `uv run ruff format --check tests/test_loaded_runtime_cache_contracts.py tests/test_loaded_runtime_cache_bc_independence.py`.
- Run `uv run ruff check tests/test_loaded_runtime_cache_contracts.py tests/test_loaded_runtime_cache_bc_independence.py` and `uv run pyright src/deterministic_response_cache/loaded_runtime_cache tests/test_loaded_runtime_cache_contracts.py tests/test_loaded_runtime_cache_bc_independence.py`.
- Run `uv run pytest tests/test_loaded_runtime_cache_contracts.py tests/test_loaded_runtime_cache_bc_independence.py -v`, `uv run pytest -v`, and `uv run pytest tests/test_package_import.py tests/test_loaded_runtime_cache_bc_independence.py -v`.
- All commands must exit zero for passing T8. All changes must match the two test paths; no deletion, source,
  architecture or unlisted edit. The assertions prove same-instance opaque handoff and alias-aware BC independence
  without exposing a token or introducing dynamic-import substitution.

## Reviewer Handoff

```json
{
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "copilot_feedback_triage": {
    "ADDRESS": [],
    "DISCUSS": [],
    "SKIP": []
  }
}
```

## Post-merge / release actions

No repository release action is required. Human alone decides merge; this non-stable topic has no README, VERSION,
release-note, tag or post-merge action.

## Open Questions / Unresolved Items

`package-topology-skeleton-replay` 與本 topic 的五份 architecture authority docs 存在 declared-path ownership
overlap。此為 Human-only unresolved `human-check`：僅能在 Human review／merge coordination 處置；本 topic 不得自行
解決、變更 locked mission／scope 或改寫既定 architecture path。Concrete `ModelIdentity -> RuntimeReuseKey`
conversion and Registry／Retention implementation remain deferred to future, separately planned integration／DI topics.

## Workflow State Contract

- current_step: plan-review-pending
- next_step: independent-plan-review
- status: REVIEW_PENDING
