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
| In-Scope | local immutable opaque `RuntimeReuseKey`（identity-only key semantics）；`RuntimeRegistry[RuntimeT]`、`RuntimeRetention[RuntimeT]` Protocol；`Available`、`Missing`、`Unavailable`、`Retained`、`NotRetained` outcomes；locked module taxonomy、direct-module contract tests、alias-aware BC-independence regression、五份 architecture authority 同步與 Archify dataflow evidence，以及 architecture-first → RED test-only → green-subject 的固定順序。 |
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
- implementation 順序不可重排：先僅同步 architecture authority 與 dataflow 並完成 visual gate，再只新增兩個
  預期失敗的 RED tests 並先提交 immutable RED-test-only subject；其後才執行 locked expected-nonzero command，將
  full-SHA-bound RED JSON 以 sole evidence-only commit 提交，最後才建立新的 immutable green implementation subject。
  RED subject 不得含 production source 或 evidence；RED evidence-only commit 不得含 tests 或 production source，亦不得
  以之前的 `6110cb…`／`44e477…` evidence routing。
- C5 的兩個 RED tests 必須先失敗並在同一 immutable subject 覆蓋五項 regression：opaque／unhashable／
  custom-equality token 不觸發 equality/hash；直接 `importlib.import_module`；直接 `__import__`；`importlib` 或
  `builtins.__import__` alias／module-alias；以及 LRC `ModelIdentity`／Identity `RuntimeReuseKey` duplicate semantic
  type。BC parser 必須解析 aliases；green subject 才能修正，且不以 mapper、shared type 或跨 BC import 規避。

## Boundaries / Exclusions

| Category | Exact contract |
| --- | --- |
| ReadOnly | `src/deterministic_response_cache/identity/**`、`response_reuse/**`、`model_execution/**`、`provider_adapter/**`、root `__init__.py`、`loaded_runtime_cache/.gitkeep`、existing source/tests、`pyproject.toml`、`README.md`、version metadata、workflow contracts、`.github/agents/**`。 |
| Written | 五個 new Python modules、`tests/test_loaded_runtime_cache_contracts.py`、`tests/test_loaded_runtime_cache_bc_independence.py`、Archify JSON／HTML／validation／delivery／visual-check receipt、contact sheet 與四張 specified PNG sidecars。 |
| Modify | `docs/business-capability-architecture.md`、`docs/evolution-roadmap.md`、`docs/architecture/business-capability/architecture-brief.md`、`scene.js`、`index.html`；只同步 protocol-only capability 與 boundaries。 |
| Deleted | 無；不得刪除 `.gitkeep`、existing tests 或既有 artifacts。 |

## Status / Allowed Transitions

- **Current**: `reviewer-evidence-committed`。C5 planning candidate `505c30609f5d65030a2eda740d8135b768cc06ca`
  已經獨立 Plan-Reviewer 核准並由 receipt-only commit `c870dd06ae47c2a8d3832604f349126f026ee1e6` 記錄；後續
  architecture-only、RED-test-only、RED evidence-only、green implementation、T3 與 V3 都已依序提交。V3 receipt
  `1c2330c618a8e76aa6512fd100a6ac26f38e1c85` 已獨立核准同一 green subject
  `1b5e4cfbd740c1e7fa10eef43221d7198f530547`。下一步是 Planner Phase 4.5 alignment；該 gate、PR thread
  classification／resolution 與 F Human-check 均尚未完成。planning artifacts 不預填或推測任何後續 candidate SHA 或
  receipt。
- **Execution model**: committed planning candidate → independent Plan-Reviewer receipt → receipt-only commit →
  architecture-contract-only commit and passing dataflow gate → RED-test-only subject commit → factual locked
  expected-nonzero command → SHA-bound RED evidence-only commit → new immutable green implementation subject →
  versioned Tester evidence → Tester evidence-only commit → versioned
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
| Contract tests | `tests/test_loaded_runtime_cache_contracts.py` **Add** | Implementer | RED-test-only then green validation; direct-module type／outcome／opaque-handoff and unhashable/custom-equality-token identity-semantics tests. |
| BC-independence tests | `tests/test_loaded_runtime_cache_bc_independence.py` **Add** | Implementer | RED-test-only then green validation; alias-aware rejection of direct import, direct `importlib.import_module`, direct `__import__`, `importlib`／`builtins.__import__` alias/module-alias bypasses, and duplicate semantic types. |
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
| RED test evidence | `plan/loaded-runtime-cache/loaded-runtime-cache.red-test-evidence-<red-test-subject-40-hex-sha>.json` | Implementer writes after the committed RED subject; Implementer commits unchanged alone | SHA-bound expected-failing command facts in a sole evidence-only commit; no tests or production source. |
| Tester evidence (T3) | `plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<implementation-subject-40-hex-sha>.json` | Tester writes; Implementer commits unchanged alone | New SHA-bound same-green-subject factual validation. |
| Independent review evidence (V3) | `plan/loaded-runtime-cache/loaded-runtime-cache.implementation-review-log-<implementation-subject-40-hex-sha>.json` | Independent Reviewer writes; Implementer commits unchanged alone | New SHA-bound record consuming committed passing T3 evidence. |

Every unlisted path is read-only. The fixed-name legacy plan-review receipt from the abandoned lineage is historical,
frozen provenance only: it is not an artifact of C5, must not be created or overwritten, and has no routing
authority. Each current or successor candidate uses only the SHA-bound template above; no candidate SHA is prefilled.
Legacy fixed-name T1／V1 evidence, including the `6110cb…` Tester and `44e477…` Reviewer lineage, is likewise frozen:
T3／V3 must use the new versioned paths above and never overwrite, reuse, or infer facts from it.

### Review and evidence schemas

- SHA-bound Plan-review receipt is one JSON object with exactly `verdict`, `blocking_issues`,
  `copilot_feedback_triage`. `verdict` is `approved|needs-rework`; `blocking_issues` is an array of objects with
  exactly `issue`, `file`, `fix`; triage has exactly `ADDRESS`／`DISCUSS`／`SKIP` arrays. Only a committed approved
  receipt for the committed candidate can authorize implementation routing.
- RED test evidence is one JSON object with exactly `schema_version`, `topic`, `red_test_subject_commit`, `status`,
  `commands`, `recorded_by`. It uses `schema_version: 1`, topic `loaded-runtime-cache`, a full 40-character lowercase
  hexadecimal SHA resolving to the already committed RED-test-only subject, status `expected-failing`, a non-empty
  array of non-empty command strings and integer exit codes containing at least one non-zero exit code, and
  `recorded_by: Implementer`. The subject contains exactly the two declared RED tests and neither production source
  nor evidence. Only after that subject exists may Implementer run the factual locked expected-nonzero command and
  write the filename-bound JSON; Implementer then commits the unchanged JSON in a sole evidence-only commit containing
  neither tests nor production source. Malformed, path/SHA-mismatched, uncommitted, same-commit/self-referential, or
  status/command-inconsistent RED evidence fails closed and cannot authorize green work.
- Tester evidence is exactly one JSON object whose top-level keys are `schema_version`, `topic`,
  `implementation_subject_commit`, `status`, `commands`, `recorded_by` and no others. `schema_version` is integer
  `1`; `topic` is `loaded-runtime-cache`; `implementation_subject_commit` is the same immutable subject's full
  40-character lowercase hexadecimal SHA; `status` is `passing|failing`; `commands` is a non-empty array whose every
  entry has only non-empty string `command` and integer `exit_code`; `recorded_by` is `Tester`. `passing` requires
  every exit code to be `0`; `failing` requires at least one non-zero exit code. Malformed, uncommitted,
  cross-topic, cross-subject, abbreviated-SHA, legacy fixed-name path, or status/command-inconsistent evidence fails
  closed. T3 is written only at its versioned SHA-bound artifact path.
- Independent review evidence is exactly one JSON object whose top-level keys are `schema_version`, `topic`,
  `implementation_subject_commit`, `tester_evidence_commit`, `verdict`, `blocking_issues`, `recorded_by` and no
  others. `schema_version` is integer `1`; `topic` is `loaded-runtime-cache`; both subject references are full
  40-character lowercase hexadecimal SHAs; `tester_evidence_commit` is the sole evidence-only commit containing
  committed same-topic, same-subject passing Tester evidence; `verdict` is `approved|needs-rework`; `blocking_issues`
  is a string array that is empty exactly for `approved` and non-empty for `needs-rework`; `recorded_by` is
  `Independent Reviewer`. Reviewer may consume only that committed passing T3 evidence; malformed, legacy fixed-name,
  or unmatched input fails closed and must not produce V3 Reviewer evidence. V3 is written only at its versioned
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
   runtime lifecycle side effect；key token 不可成為 `str`／hash API 或由 `repr` 暴露，且 unhashable/custom-equality
   token 不得被 key equality/hash 呼叫。
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

**Written:** the five source modules, two declared contract/regression tests, the separately committed versioned RED
evidence, and versioned T3／V3 evidence in `Artifact Paths`, plus the ten declared Archify source/delivery/visual-
evidence artifacts.

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
- **Regression:** the same two RED tests must first fail on all five C5 regressions: opaque/unhashable/custom-equality
  token identity-only semantics; direct `importlib.import_module`; direct `__import__`; `importlib` or
  `builtins.__import__` alias/module-alias use; and LRC `ModelIdentity`／Identity `RuntimeReuseKey` duplicate semantic
  types. The alias-aware parser rejects those cross-BC paths while `tests/test_package_import.py` preserves existing
  import behavior.
- **Sequencing:** five architecture authority files and dataflow evidence form the first implementation commit; only
  after its passing visual gate may the immutable RED-test-only subject containing exactly two tests be committed.
  The locked expected-nonzero command runs after that commit; its filename- and SHA-bound JSON is then committed alone
  as RED evidence, and only then may the immutable green source subject be created.
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
4. Only after Step 3 passes, add exactly the two declared RED tests and commit that immutable RED-test-only subject.
   It contains no production source or evidence, and fails on all five C5 regressions: opaque token identity-only
   semantics, direct `importlib.import_module`, direct `__import__`, alias/module-alias `importlib`／`builtins.__import__`,
   and duplicate semantic types. Only after it is committed, execute the locked expected-failing command and write its
   factual full-SHA-bound JSON at the versioned RED path.
5. Commit the unchanged RED JSON as a sole evidence-only commit containing neither tests nor production source. Green
   work remains forbidden until this separate evidence commit exists.
6. Only after that evidence commit exists, create the new immutable green implementation subject: add the five locked
   Python contract modules, preserve BC separation, direct-module surface, `.gitkeep`, opaque non-exposing
   identity-only key behavior, alias-aware BC independence and no-concrete-implementation boundary.
7. Run locked format, pyright, targeted／full pytest and direct-import regression against the green subject. Tester
   records actual results at a new versioned T3 path only after that immutable subject exists; Independent Reviewer
   then consumes committed passing T3 evidence at a new versioned V3 path.

## Validation / Acceptance Checks

- `node /Users/andrew/.codex/skills/archify/bin/archify.mjs validate dataflow docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.json --quality showcase --json` must report 9/9, zero composition errors and zero warnings.
- Only after that pass, run `node /Users/andrew/.codex/skills/archify/bin/archify.mjs deliver dataflow docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.json docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.html --quality showcase --json`.
- Then run `node /Users/andrew/.codex/skills/archify/bin/archify.mjs visual-check docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.html --repo-root /Users/andrew/code/python/deterministic-response-cache.worktrees/agent-20260917-loaded-runtime-cache --json`; its 1440×900, 1600×1000, 1920×1080 and 2048×1320 containment must pass. A non-zero or skipped Archify result stops the gate.
- Only after the three architecture commands pass, commit exactly the two declared tests as the immutable RED-test-only
  subject, with no production source or evidence. Only after that commit exists, execute `uv run pytest
  tests/test_loaded_runtime_cache_contracts.py tests/test_loaded_runtime_cache_bc_independence.py -v`; record its
  expected non-zero result in `loaded-runtime-cache.red-test-evidence-<red-test-subject-40-hex-sha>.json`, where the
  filename and `red_test_subject_commit` are the committed subject's full SHA. Commit that JSON unchanged as a sole
  evidence-only commit with no tests or production source; only then is green work allowed.
- After the new green source subject exists, run `uv run ruff format --check src/deterministic_response_cache/loaded_runtime_cache tests/test_loaded_runtime_cache_contracts.py tests/test_loaded_runtime_cache_bc_independence.py`.
- Then run `uv run ruff check src/deterministic_response_cache/loaded_runtime_cache tests/test_loaded_runtime_cache_contracts.py tests/test_loaded_runtime_cache_bc_independence.py` and `uv run pyright src/deterministic_response_cache/loaded_runtime_cache tests/test_loaded_runtime_cache_contracts.py tests/test_loaded_runtime_cache_bc_independence.py`.
- Then run `uv run pytest tests/test_loaded_runtime_cache_contracts.py tests/test_loaded_runtime_cache_bc_independence.py -v`, `uv run pytest -v`, and `uv run pytest tests/test_package_import.py tests/test_loaded_runtime_cache_bc_independence.py -v`; the last command verifies direct-import regression including direct `importlib.import_module`, direct `__import__`, alias/module-alias `importlib`／`builtins.__import__`, duplicate semantic types, and `sys.modules` substitution.
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

- current_step: reviewer-evidence-committed
- next_step: planner-phase-4.5-alignment-pending
- status: IN_PROGRESS
