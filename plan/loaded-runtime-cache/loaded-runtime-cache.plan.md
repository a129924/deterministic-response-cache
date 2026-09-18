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
| In-Scope | local immutable opaque `RuntimeReuseKey`；`RuntimeRegistry[RuntimeT]`、`RuntimeRetention[RuntimeT]` Protocol；`Available`、`Missing`、`Unavailable`、`Retained`、`NotRetained` outcomes；locked module taxonomy、direct-module contract tests、BC-independence regression、五份 architecture authority 同步與 Archify dataflow evidence，以及 architecture-first → RED test-only → green-subject 的固定順序。 |
| Out-Of-Scope | Identity BC direct import、`ModelIdentity -> RuntimeReuseKey` mapping／mapper／ACL implementation、concrete Registry／Retention／lookup class、DI、backend、runtime initialization／download／unload／execution、provider management、Response Reuse、Model Execution、Provider Adapter、TTL、eviction、locking、concurrency、retry、timeout、metrics、tracing。 |
| Non-Goal | root re-export、package facade、dynamic import、`sys.modules` substitution、`service.py`、`utils.py`、`common.py`、README、version、release、tag、merge、post-merge。 |

## Locked Decisions

- Identity BC 與 Loaded Runtime Cache 是獨立 BC，任一方向均不得 import 對方 module。`ModelIdentity` 與
  `RuntimeReuseKey` 是語意不同的 local types，不得 re-export、duplicate 或跨 BC 假裝共用。
- integration／ACL boundary 決定 `RuntimeReuseKey` token／mapping；Loaded Runtime Cache 只 opaque pass-through，
  不讀取、拆解、序列化、字串化、hash、canonicalize、驗證、推測或重新詮釋 key。token 不是 public API，不能以
  `str`／hash 代替，且 `repr` 不得暴露 token。
- `RuntimeRegistry.lookup` 回傳 `RuntimeT | None`，`retain` 回傳 `None`；`RuntimeRetention.retain` 回傳
  `Retained[RuntimeT] | NotRetained[RuntimeT]`。port-owned expected signal 是
  `RuntimeRegistryLookupUnavailable`；outcome-owned `Unavailable` 與此 signal 分離，本 topic 不增加 mapper。
- module placement 固定為 `<bc>/<topic>/<child-topic>/<module>.py`。這是 non-stable-library topic，沒有 README
  row、VERSION bump、release note 或 release action。
- architecture-path overlap 僅在 Human review／merge coordination 處理；不授權改另一 topic artifacts。
- implementation 順序不可重排：先僅同步 architecture authority 與 dataflow 並完成 visual gate，再僅新增並
  執行預期失敗的 RED tests，最後才建立新的 immutable green implementation subject。RED gate 不得含任何
  production source，亦不得以之前的 `6110cb…`／`44e477…` evidence routing。

## Boundaries / Exclusions

| Category | Exact contract |
| --- | --- |
| ReadOnly | `src/deterministic_response_cache/identity/**`、`response_reuse/**`、`model_execution/**`、`provider_adapter/**`、root `__init__.py`、`loaded_runtime_cache/.gitkeep`、existing source/tests、`pyproject.toml`、`README.md`、version metadata、workflow contracts、`.github/agents/**`。 |
| Written | 五個 new Python modules、`tests/test_loaded_runtime_cache_contracts.py`、`tests/test_loaded_runtime_cache_bc_independence.py`、Archify JSON／HTML／validation／delivery／visual-check receipt、contact sheet 與四張 specified PNG sidecars。 |
| Modify | `docs/business-capability-architecture.md`、`docs/evolution-roadmap.md`、`docs/architecture/business-capability/architecture-brief.md`、`scene.js`、`index.html`；只同步 protocol-only capability 與 boundaries。 |
| Deleted | 無；不得刪除 `.gitkeep`、existing tests 或既有 artifacts。 |

## Status / Allowed Transitions

- **Current**: `planning-candidate-committed`。已存在 planning candidate；下一步由 Independent Plan-Reviewer
  對該 committed candidate 進行獨立審查。planning artifacts 不預填或推測任何 candidate SHA。
- **Execution model**: committed planning candidate → independent Plan-Reviewer receipt → receipt-only commit →
  architecture-contract-only commit and passing dataflow gate → RED-test-only commit and factual RED evidence → new
  immutable green implementation subject → versioned Tester evidence → Tester evidence-only commit → versioned
  independent Reviewer evidence → Reviewer evidence-only commit → Planner Phase 4.5 alignment → bounded publish／draft
  PR → Human review／merge。
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
| Runtime key | `src/deterministic_response_cache/loaded_runtime_cache/runtime_reuse/registry/runtime_reuse_key.py` **Add** | Implementer | Local opaque semantic type only. |
| Registry port | `src/deterministic_response_cache/loaded_runtime_cache/runtime_reuse/registry/runtime_registry_port.py` **Add** | Implementer | Synchronous `RuntimeRegistry` Protocol and expected lookup signal owner. |
| Lookup outcomes | `src/deterministic_response_cache/loaded_runtime_cache/runtime_reuse/lookup/lookup_outcome.py` **Add** | Implementer | Lookup outcome contract owner; no mapper. |
| Retention protocol | `src/deterministic_response_cache/loaded_runtime_cache/runtime_reuse/retention/runtime_retention.py` **Add** | Implementer | `RuntimeRetention` Protocol. |
| Retention outcomes | `src/deterministic_response_cache/loaded_runtime_cache/runtime_reuse/retention/retain_outcome.py` **Add** | Implementer | Retention outcome contract owner. |
| Contract tests | `tests/test_loaded_runtime_cache_contracts.py` **Add** | Implementer | RED-test-only then green validation; direct-module type／outcome／opaque-handoff tests. |
| BC-independence tests | `tests/test_loaded_runtime_cache_bc_independence.py` **Add** | Implementer | RED-test-only then green validation; reject direct import and bypasses. |
| BC text authority | `docs/business-capability-architecture.md` **Modify** | Implementer | Canonical BC responsibility synchronization. |
| Evolution roadmap | `docs/evolution-roadmap.md` **Modify** | Implementer | Topic order and future-boundary synchronization. |
| Architecture brief | `docs/architecture/business-capability/architecture-brief.md` **Modify** | Implementer | Protocol-only and ACL-boundary synchronization. |
| Interactive scene source | `docs/architecture/business-capability/scene.js` **Modify** | Implementer | Interactive visual authority synchronization. |
| Interactive scene mirror | `docs/architecture/business-capability/index.html` **Modify** | Implementer | Embedded scene synchronization. |
| Dataflow source | `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.json` **Add** | Implementer | Archify showcase source. |
| Standalone dataflow | `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.html` **Add** | Implementer | Trusted delivered HTML. |
| Dataflow validation receipt | `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.validation.json` **Add** | Implementer | Final showcase validation receipt. |
| Dataflow delivery receipt | `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.delivery.json` **Add** | Implementer | Final delivery receipt. |
| Visual-check receipt | `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.json` **Add** | Implementer | Desktop containment and capture receipt. |
| Visual contact sheet | `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.html` **Add** | Implementer | Generated visual evidence index. |
| PNG 1440×900 light | `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.1440x900.light.png` **Add** | Implementer | Visual evidence. |
| PNG 1440×900 dark | `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.1440x900.dark.png` **Add** | Implementer | Visual evidence. |
| PNG 2048×1320 light | `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.2048x1320.light.png` **Add** | Implementer | Visual evidence. |
| PNG 2048×1320 dark | `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.2048x1320.dark.png` **Add** | Implementer | Visual evidence. |
| RED test evidence | `plan/loaded-runtime-cache/loaded-runtime-cache.red-test-evidence-<red-test-subject-40-hex-sha>.json` | Implementer writes and commits with only RED-test subject evidence | Expected failing command facts; no production source. |
| Tester evidence (T2) | `plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<implementation-subject-40-hex-sha>.json` | Tester writes; Implementer commits unchanged alone | New SHA-bound same-green-subject factual validation. |
| Independent review evidence (V2) | `plan/loaded-runtime-cache/loaded-runtime-cache.implementation-review-log-<implementation-subject-40-hex-sha>.json` | Independent Reviewer writes; Implementer commits unchanged alone | New SHA-bound record consuming committed passing T2 evidence. |

Every unlisted path is read-only. The fixed-name legacy plan-review receipt from the abandoned lineage is historical,
frozen provenance only: it is not an artifact of candidate C, must not be created or overwritten, and has no routing
authority. Each current or successor candidate uses only the SHA-bound template above; no candidate SHA is prefilled.
Legacy fixed-name T1／V1 evidence, including the `6110cb…` Tester and `44e477…` Reviewer lineage, is likewise frozen:
T2／V2 must use the new versioned paths above and never overwrite, reuse, or infer facts from it.

### Review and evidence schemas

- SHA-bound Plan-review receipt is one JSON object with exactly `verdict`, `blocking_issues`,
  `copilot_feedback_triage`. `verdict` is `approved|needs-rework`; `blocking_issues` is an array of objects with
  exactly `issue`, `file`, `fix`; triage has exactly `ADDRESS`／`DISCUSS`／`SKIP` arrays. Only a committed approved
  receipt for the committed candidate can authorize implementation routing.
- RED test evidence is one JSON object with exactly `schema_version`, `topic`, `red_test_subject_commit`, `status`,
  `commands`, `recorded_by`. It uses `schema_version: 1`, topic `loaded-runtime-cache`, a full 40-character lowercase
  hexadecimal RED-test-subject SHA, status `expected-failing`, a non-empty array of non-empty command strings and
  integer exit codes containing at least one non-zero exit code, and `recorded_by: Implementer`. It is committed only
  with the RED-test-only subject; it cannot contain production source, Tester facts, or green-subject routing facts.
- Tester evidence is exactly one JSON object whose top-level keys are `schema_version`, `topic`,
  `implementation_subject_commit`, `status`, `commands`, `recorded_by` and no others. `schema_version` is integer
  `1`; `topic` is `loaded-runtime-cache`; `implementation_subject_commit` is the same immutable subject's full
  40-character lowercase hexadecimal SHA; `status` is `passing|failing`; `commands` is a non-empty array whose every
  entry has only non-empty string `command` and integer `exit_code`; `recorded_by` is `Tester`. `passing` requires
  every exit code to be `0`; `failing` requires at least one non-zero exit code. Malformed, uncommitted,
  cross-topic, cross-subject, abbreviated-SHA, legacy fixed-name path, or status/command-inconsistent evidence fails
  closed. T2 is written only at its versioned SHA-bound artifact path.
- Independent review evidence is exactly one JSON object whose top-level keys are `schema_version`, `topic`,
  `implementation_subject_commit`, `tester_evidence_commit`, `verdict`, `blocking_issues`, `recorded_by` and no
  others. `schema_version` is integer `1`; `topic` is `loaded-runtime-cache`; both subject references are full
  40-character lowercase hexadecimal SHAs; `tester_evidence_commit` is the sole evidence-only commit containing
  committed same-topic, same-subject passing Tester evidence; `verdict` is `approved|needs-rework`; `blocking_issues`
  is a string array that is empty exactly for `approved` and non-empty for `needs-rework`; `recorded_by` is
  `Independent Reviewer`. Reviewer may consume only that committed passing T2 evidence; malformed, legacy fixed-name,
  or unmatched input fails closed and must not produce V2 Reviewer evidence. V2 is written only at its versioned
  SHA-bound artifact path.

## Python implementation metadata

### Non-goals

- 不建立 `ModelIdentity -> RuntimeReuseKey` mapper、ACL implementation，或任何跨 BC import。
- 不建立 Registry／Retention concrete class、DI composition、backend，或 runtime lifecycle／provider management。
- 不新增 root re-export、package facade、dynamic import、`sys.modules` substitution、dependency、README、VERSION、
  release、tag、merge 或 post-merge action。

### Current Context

Identity BC、Response Reuse、Model Execution 與 Provider Adapter 都是相鄰但獨立的 bounded context；本 topic 的
reserved `loaded_runtime_cache` area 尚未有實作。`pyproject.toml` 已鎖定 Python 3.12、strict Pyright、Ruff 與 pytest。
已存在的 planning candidate 是唯一可供 Independent Plan-Reviewer 審查的 planning state；architecture-path overlap
保留給 Human review／merge coordination，不能由本 topic writer 擴張路徑或自行解決。

### Requirements

1. 只在 locked taxonomy 定義 local `RuntimeReuseKey`、同步 generic Protocol 與 immutable outcomes；不建立 consumer
   或 concrete implementation。
2. Registry key 與 runtime payload 都必須以同一 instance opaque handoff；沒有 key-field inspection、mapping 或
   runtime lifecycle side effect；key token 不可成為 `str`／hash API 或由 `repr` 暴露。
3. expected registry lookup failure、`Missing`、`Unavailable`、unexpected exception 與 retention outcomes 必須可區分。
4. 只寫 declared source、test、architecture 與 Archify evidence paths；維持 BC independence 與 direct-module imports。
5. 先完成 architecture authority／dataflow gate，再做無 production source 的 RED-test-only gate，最後才建立新的
   immutable green implementation subject；不可倒置或將任一 gate 壓縮為舊 evidence。

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

**Written:** the five source modules, two declared contract/regression tests, versioned RED evidence, and versioned
T2／V2 evidence in `Artifact Paths`, plus the ten declared Archify source/delivery/visual-evidence artifacts.

**Modified:** only the five architecture authority files enumerated in `Artifact Paths`.

**ReadOnly:** all Identity, Response Reuse, Model Execution, Provider Adapter, root-package, existing source/test,
configuration, workflow-contract and `.github/agents/**` paths enumerated in `Boundaries / Exclusions`.

### Test Plan

- **Happy path:** typed fakes prove Registry hit and same-instance `RuntimeReuseKey` pass-through; retention outcomes
  retain the original runtime instance.
- **Invalid input:** no key validation is in scope; a non-expected fake exception propagates unchanged rather than
  being classified.
- **Edge case:** missing (`None`), expected `RuntimeRegistryLookupUnavailable`, `Unavailable`, and retention failure
  remain distinct without a signal-to-outcome mapper.
- **Regression:** direct-module imports and BC-independence checks reject cross-BC imports, re-exports and all
  `importlib`、`__import__`、`sys.modules` dynamic-import substitution while `tests/test_package_import.py` preserves
  existing import behavior.
- **Sequencing:** five architecture authority files and dataflow evidence form the first implementation commit; only
  after its passing visual gate may a RED-test-only commit record expected failures, and only then may the immutable
  green source subject be created.
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

Revert the ordered architecture-contract, RED-test-only, and green implementation subjects without modifying their
immutable historical evidence. Leave read-only `.gitkeep`, root package, configuration, adjacent BCs, and planning /
evidence history untouched; a future topic handles any subsequently needed concrete implementation.

## Implementation Steps

1. First synchronize only the five declared architecture authority files; declare external unimplemented ACL mapping
   and retain backend, lifecycle, execution and provider work as future. This architecture-contract-only commit must
   precede every new test and production-source path.
2. Produce then validate／deliver／visual-check the Archify dataflow with Traditional-Chinese labels, no `meta.locale`,
   `quality_profile: showcase`, at most 12 primary nodes, and truthful `backend` visual classification for the
   contract-only Loaded Runtime Cache node. The retain path explicitly receives `RuntimeReuseKey`; dashed routes are
   explicit async only, never synchronous retain failure.
3. After every JSON edit run validate; freeze only a 9/9, zero-error, zero-warning result; then deliver and run
   visual-check at 1440×900, 1600×1000, 1920×1080, 2048×1320. Nonzero or skipped result stops the gate.
4. Only after Step 3 passes, add and execute only the two declared RED tests. This RED-test-only subject contains no
   production source and records actual expected-failing command evidence at its versioned RED path.
5. Only after committed RED evidence, create the new immutable green implementation subject: add the five locked
   Python contract modules, preserve BC separation, direct-module surface, `.gitkeep`, opaque non-exposing key
   behavior, and no-concrete-implementation boundary.
6. Run locked format, pyright, targeted／full pytest and direct-import regression against the green subject. Tester
   records actual results at a new versioned T2 path only after that immutable subject exists; Independent Reviewer
   then consumes committed passing T2 evidence at a new versioned V2 path.

## Validation / Acceptance Checks

- `node /Users/andrew/.codex/skills/archify/bin/archify.mjs validate dataflow docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.json --quality showcase --json` must report 9/9, zero composition errors and zero warnings.
- Only after that pass, run `node /Users/andrew/.codex/skills/archify/bin/archify.mjs deliver dataflow docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.json docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.html --quality showcase --json`.
- Then run `node /Users/andrew/.codex/skills/archify/bin/archify.mjs visual-check docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.html --repo-root /Users/andrew/code/python/deterministic-response-cache.worktrees/agent-20260917-loaded-runtime-cache --json`; its 1440×900, 1600×1000, 1920×1080 and 2048×1320 containment must pass. A non-zero or skipped Archify result stops the gate.
- Only after the three architecture commands pass, execute `uv run pytest tests/test_loaded_runtime_cache_contracts.py tests/test_loaded_runtime_cache_bc_independence.py -v` as the RED-test-only command; its expected non-zero result is recorded in the versioned RED evidence and no production source may be present.
- After the new green source subject exists, run `uv run ruff format --check src/deterministic_response_cache/loaded_runtime_cache tests/test_loaded_runtime_cache_contracts.py tests/test_loaded_runtime_cache_bc_independence.py`.
- Then run `uv run ruff check src/deterministic_response_cache/loaded_runtime_cache tests/test_loaded_runtime_cache_contracts.py tests/test_loaded_runtime_cache_bc_independence.py` and `uv run pyright src/deterministic_response_cache/loaded_runtime_cache tests/test_loaded_runtime_cache_contracts.py tests/test_loaded_runtime_cache_bc_independence.py`.
- Then run `uv run pytest tests/test_loaded_runtime_cache_contracts.py tests/test_loaded_runtime_cache_bc_independence.py -v`, `uv run pytest -v`, and `uv run pytest tests/test_package_import.py tests/test_loaded_runtime_cache_bc_independence.py -v`; the last command verifies direct-import regression including rejection of `importlib`, `__import__`, and `sys.modules` substitution.
- All changes must match Artifact Paths; no deletion or unlisted edit. Typed fakes must prove same-instance handoff,
  distinct failure semantics and retention runtime identity; the diagram must remain truthful about external ACL and
  contract-only boundaries.

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

- current_step: planning-candidate-committed
- next_step: independent-plan-review-pending
- status: PENDING
