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
| In-Scope | local immutable opaque `RuntimeReuseKey`（identity-only key semantics）；`RuntimeRegistry[RuntimeT]`、`RuntimeRetention[RuntimeT]` Protocol；`Available`、`Missing`、`Unavailable`、`Retained`、`NotRetained` outcomes；locked module taxonomy、direct-module contract tests、alias-aware BC-independence regression；completed C12/R12 provenance；以及 C13 的 chained-assignment RED→green correction、bounded Archify evidence correction 與新的 evidence/classification route。 |
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
- C5→V3 的 architecture/dataflow gate 與 production source contracts 是 frozen provenance。C8/C9/C10 是 frozen、unapproved
  predecessor planning provenance，沒有 routing authority。C11 必須在既有 source ancestor 上重用既有事實，不能回寫、
  重建或聲稱 source-absent 的 historical RED→green 順序。
- C11 的兩個 isolated executable RED assertions已經在同一 immutable assertion subject 覆蓋五項 regression：opaque／unhashable／
  custom-equality token 不觸發 equality/hash；直接 `importlib.import_module`；直接 `__import__`；`importlib` 或
  `builtins.__import__` alias／module-alias；以及 LRC `ModelIdentity`／Identity `RuntimeReuseKey` duplicate semantic
  type。BC parser 必須解析 aliases；assertions 在 current source ancestor 執行並以 T11 如實收集，不能假稱
  expected-nonzero、green-source authorization 或以 mapper、shared type 或跨 BC import 規避。C11/R11/S11/T11/V11 現為
  completed frozen provenance，C12 不得重新審核、修改或以其替代自己的 candidate／receipt。
- C12 只處理 planning state 與 current PR snapshot `73644c2b88257832e1b4d8bedaf516b803c2ee3a` 的 factual triage contract。
  F `PRRT_kwDOUJTij86jnBpk`／comment `4043480108` 以及 architecture/ACL ownership 只能 `DISCUSS`、Human-only
  `human-check`；其餘 current factual threads 只能 `SKIP`，不可被 C12 宣稱已修正、回覆或 resolve。
- C13 是 Human-authorized planning successor。它保留原 mission／scope／Protocol contract，僅重建 review-required
  evidence chain：collection-success、actual assertion-failing chained-assignment RED test-only subject → factual
  failing Tester evidence → new green immutable subject with all-simple-name assignment-target repair → passing Tester
  evidence → approved independent Reviewer evidence → Planner Phase 4.5 → new classification。不得重播或改寫 historical
  `e2e125` evidence；RED failing evidence 不授權 Reviewer record、publish、reply、resolve 或 merge。
- C13 green subject 同時只可修正 ten allowlisted Archify artifacts 的 retain input `RuntimeReuseKey + runtime`、
  `Retained(runtime)`／`NotRetained(runtime)` labels、edge placement 及 four-viewport containment；不得改變
  protocol-only boundary 或暗示 concrete backend、DI、runtime lifecycle。

## Boundaries / Exclusions

| Category | Exact contract |
| --- | --- |
| ReadOnly | `src/deterministic_response_cache/identity/**`、`response_reuse/**`、`model_execution/**`、`provider_adapter/**`、root `__init__.py`、`loaded_runtime_cache/.gitkeep`、五個 existing source modules、`pyproject.toml`、`README.md`、version metadata、workflow contracts、`.github/agents/**`，以及 Human-owned `docs/business-capability-architecture.md`、`docs/evolution-roadmap.md`、`docs/architecture/business-capability/architecture-brief.md`、`docs/architecture/business-capability/index.html`、`docs/architecture/business-capability/scene.js`。F／ACL threads stay Human-only. |
| Written | C13 Plan-Reviewer receipt、RED/green SHA-bound Tester evidence 與 green SHA-bound Independent Reviewer evidence；each writer creates it and Implementer commits each unchanged as a sole evidence-only commit. |
| Modify | C13 candidate only the five planning artifacts; RED only `tests/test_loaded_runtime_cache_bc_independence.py`; green only that test plus the ten exact dataflow paths listed in Artifact Paths. |
| Deleted | 無；不得刪除 `.gitkeep`、existing tests 或既有 artifacts。 |

## Status / Allowed Transitions

- **Current**: `c13-planning-candidate-ready-for-commit`。C12 candidate
  `41d51072901cfd205ebc91644036e6695b1fe81c` 與其 approved R12 receipt-only commit
  `d738e91eb20869709d605fe7f879b340c9614b6a` 已提交，且 receipt 的 SHA-bound path 是
  `plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-41d51072901cfd205ebc91644036e6695b1fe81c.json`。
  C11 `55ad5d48c8e638bc5a81f3d0fecfc5a5f35e963c`、R11
  `01da31b11dcc8013f03a773ad9e9042c8bb527bf`、S11
  `e9934dc7bb7b4f81098e635b5f0257c56da659a0`、T11
  `86a5cd54bec9d687d8d7f1738e9376435d3d1abf`、V11
  `73644c2b88257832e1b4d8bedaf516b803c2ee3a` 均為 completed frozen provenance。C8/C9/C10 是 frozen、unapproved
  predecessor；C5→V3 也是 frozen provenance，均不能作 C13 routing authority。
- **Execution model**: C13 candidate-only commit → independent SHA-bound approved C13 Plan-Reviewer receipt →
  receipt-only commit → collection-success / assertion-failing RED test-only immutable subject → failing factual
  Tester evidence-only commit → new green immutable subject → passing Tester evidence-only commit → approved
  Independent Reviewer evidence-only commit → Planner Phase 4.5 → new independent thread classification. F／ACL
  Human-check threads remain open and cannot be processed by this route.
- **Allowed transitions**: `planned` → `planning-candidate-committed` → `plan-review-in-progress` →
  `plan-review-receipt-committed` → `implementation-in-progress` → `tester-in-progress` →
  `tester-evidence-committed` → `reviewer-in-progress` → `reviewer-evidence-committed` → `approved` →
  `publish-in-progress` → `pr-open` → `merged` (Human only). A `needs-rework` verdict returns only to a new
  planning candidate or a new immutable implementation subject as applicable; no stale evidence may route.

## Artifact Paths

| Artifact | Path | Write owner | Decision authority and role |
| --- | --- | --- | --- |
| Requirements | `analysis/loaded-runtime-cache/requirements.md` | Plan-Creator | C13 candidate-only planning artifact. |
| Technical specification | `analysis/loaded-runtime-cache/technical-spec.md` | Plan-Creator | C13 candidate-only planning artifact. |
| Topic plan | `plan/loaded-runtime-cache/loaded-runtime-cache.plan.md` | Plan-Creator | C13 routing contract; no SHA/outcome prefill. |
| Topic specification | `plan/loaded-runtime-cache/loaded-runtime-cache.spec.md` | Plan-Creator | C13 acceptance and error scenarios. |
| Step tracker | `plan/loaded-runtime-cache/loaded-runtime-cache.step.md` | Plan-Creator | C13 phase truth only. |
| Plan-review receipt | `plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<planning-candidate-40-hex-sha>.json` | Independent Plan-Reviewer writes; Implementer commits unchanged alone | SHA-bound normal-plan verdict. |
| C13 RED test subject | `tests/test_loaded_runtime_cache_bc_independence.py` | Implementer | Only after approved C13 receipt; collection-success, actual assertion-failing chained-assignment regression. |
| C13 green subject | `tests/test_loaded_runtime_cache_bc_independence.py` | Implementer | New immutable subject; handles all-simple-name chained assignment targets. |
| C13 dataflow evidence | `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.json`; `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.html`; `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.validation.json`; `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.delivery.json`; `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.json`; `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.html` | Implementer | Green subject only; truthful Archify validate/deliver/visual-check evidence. |
| C13 existing captures | `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.1440x900.dark.png`; `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.1440x900.light.png`; `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.2048x1320.dark.png`; `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.2048x1320.light.png` | Implementer | Green subject only; exactly these four existing capture paths. |
| Architecture authority | `docs/business-capability-architecture.md` | None — ReadOnly | Human-only overlap / merge coordination; C11 must not rewrite it. |
| Architecture authority | `docs/evolution-roadmap.md` | None — ReadOnly | Human-only overlap / merge coordination; C11 must not rewrite it. |
| Architecture authority | `docs/architecture/business-capability/architecture-brief.md` | None — ReadOnly | Human-only overlap / merge coordination; C11 must not rewrite it. |
| Architecture authority | `docs/architecture/business-capability/index.html` | None — ReadOnly | Human-only overlap / merge coordination; C11 must not rewrite it. |
| Architecture authority | `docs/architecture/business-capability/scene.js` | None — ReadOnly | Human-only overlap / merge coordination; C11 must not rewrite it. |
| Other Archify evidence | every `docs/architecture/loaded-runtime-cache/**` path not named above | None — ReadOnly | C13 must not broaden its dataflow correction allowlist. |
| Completed C11/R11/S11/T11/V11 records | C11/R11/S11/T11/V11 exact committed paths and SHAs named in Status | None — ReadOnly | Immutable completed provenance; no C12 routing reuse. |
| Plan-review receipt (R12) | `plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-41d51072901cfd205ebc91644036e6695b1fe81c.json` | None — ReadOnly | Approved R12 verdict and nonempty fixed-snapshot triage, committed alone in `d738e91eb20869709d605fe7f879b340c9614b6a`. |

Every unlisted path is read-only. The fixed-name legacy plan-review receipt from the abandoned lineage is historical,
frozen provenance only: it is not an artifact of C11, must not be created or overwritten, and has no routing
authority. Each current or successor candidate uses only the SHA-bound template above; no candidate SHA is prefilled.
Legacy fixed-name T1／V1 evidence, including the `6110cb…` Tester and `44e477…` Reviewer lineage, is likewise frozen:
T3／V3 and C5 provenance must never be overwritten, reused, or inferred as C11 facts.

### Review and evidence schemas

- SHA-bound Plan-review receipt is one JSON object with exactly `verdict`, `blocking_issues`,
  `copilot_feedback_triage`. `verdict` is `approved|needs-rework`; `blocking_issues` is an array of objects with
  exactly `issue`, `file`, `fix`; triage has exactly `ADDRESS`／`DISCUSS`／`SKIP` arrays. Only a committed approved
  receipt for the committed candidate can authorize implementation routing.
- C11 creates no RED-evidence JSON. Its isolated executable assertions run against the existing source ancestor; their
  actual command results belong only in T11. A failing result is `failing` T11, never an expected-failing authorization.
- Tester evidence is exactly one JSON object whose top-level keys are `schema_version`, `topic`,
  `implementation_subject_commit`, `status`, `commands`, `recorded_by` and no others. `schema_version` is integer
  `1`; `topic` is `loaded-runtime-cache`; `implementation_subject_commit` is the same immutable subject's full
  40-character lowercase hexadecimal SHA; `status` is `passing|failing`; `commands` is a non-empty array whose every
  entry has only non-empty string `command` and integer `exit_code`; `recorded_by` is `Tester`. `passing` requires
  every exit code to be `0`; `failing` requires at least one non-zero exit code. Malformed, uncommitted,
  cross-topic, cross-subject, abbreviated-SHA, legacy fixed-name path, or status/command-inconsistent evidence fails
  closed. T11 is written only at its versioned SHA-bound artifact path.
- Independent review evidence is exactly one JSON object whose top-level keys are `schema_version`, `topic`,
  `implementation_subject_commit`, `tester_evidence_commit`, `verdict`, `blocking_issues`, `recorded_by` and no
  others. `schema_version` is integer `1`; `topic` is `loaded-runtime-cache`; both subject references are full
  40-character lowercase hexadecimal SHAs; `tester_evidence_commit` is the sole evidence-only commit containing
  committed same-topic, same-subject passing Tester evidence; `verdict` is `approved|needs-rework`; `blocking_issues`
  is a string array that is empty exactly for `approved` and non-empty for `needs-rework`; `recorded_by` is
  `Independent Reviewer`. Reviewer may consume only that committed passing T11 evidence; malformed, legacy fixed-name,
  or unmatched input fails closed and must not produce V11 Reviewer evidence. V11 is written only at its versioned
  SHA-bound artifact path.

### C12 fixed-snapshot triage schema

R12 的 receipt 仍是 one JSON object，top-level keys 恰為 `verdict`、`blocking_issues`、
`copilot_feedback_triage`。本 C12 route 中 triage 三個 arrays 的合計不可為空；每個 triage entry 恰有
`thread`、`comment`、`finding`、`commit`、`basis`、`disposition` 六個 non-empty factual fields。`thread` 是完整 PR
thread node id，`comment` 是 decimal GitHub comment id，`commit` 是 full 40-hex committed SHA；`basis` 必須可由 fixed
snapshot 或 named frozen provenance 驗證，`disposition` 必須是 `DISCUSS` 或 `SKIP`。任何缺漏、空 triage、future SHA、
abbreviated SHA、未驗證 basis，或把 Human-check 寫成 resolved 都 fail closed。

R12 必須完整涵蓋此固定 snapshot（head `73644c2b88257832e1b4d8bedaf516b803c2ee3a`）的下列 current unresolved
threads。此表是 required factual coverage，不是 C12 對 source／test／docs 的修改授權：

| thread | comment | finding | factual commit / basis | required disposition |
| --- | --- | --- | --- | --- |
| `PRRT_kwDOUJTij86jnBpk` | `4043480108` | F：跨 topic declared-path overlap | snapshot plan 與 five architecture authority paths | `DISCUSS` — Human-only `human-check`; no reply/resolve authorization |
| `PRRT_kwDOUJTij86kQ95O` | `4060023123` | business-capability flow lacks external ACL node | architecture/ACL authority is ReadOnly and overlaps another topic | `DISCUSS` — same Human-only `human-check` |
| `PRRT_kwDOUJTij86kQe90` | `4059838910` | individual dynamic-import bypass coverage | S11 `e9934dc7bb7b4f81098e635b5f0257c56da659a0` has isolated parametrized cases | `SKIP` — factual C11 coverage; no C12 code claim |
| `PRRT_kwDOUJTij86kQe94` | `4059838915` | historical RED collection failure | C11 route expressly freezes historical RED evidence; T11/V11 are factual current evidence | `SKIP` — frozen historical provenance |
| `PRRT_kwDOUJTij86kQ948` | `4060023096` | subject/evidence ancestry | `e9934dc7bb7b4f81098e635b5f0257c56da659a0` → `86a5cd54bec9d687d8d7f1738e9376435d3d1abf` → `73644c2b88257832e1b4d8bedaf516b803c2ee3a` | `SKIP` — factual completed C11 chain |
| `PRRT_kwDOUJTij86kQ95C` | `4060023103` | assignment dynamic-import alias | S11 alias fixed-point analysis is committed provenance | `SKIP` — factual C11 coverage; no C12 code claim |
| `PRRT_kwDOUJTij86kQ95K` | `4060023118` | retention outcome label placement | frozen Archify evidence is ReadOnly in C12 | `SKIP` — no C12 artifact mutation |
| `PRRT_kwDOUJTij86knEY7` | `4068738285` | C11 subject/evidence ancestry | same linear S11→T11→V11 commits above | `SKIP` — factual completed C11 chain |
| `PRRT_kwDOUJTij86knEY_` | `4068738291` | chained assignment import alias | S11 fixed-point alias analysis is committed provenance | `SKIP` — factual current-source evidence; no C12 code claim |
| `PRRT_kwDOUJTij86knEZB` | `4068738293` | retention dataflow runtime input | frozen Archify evidence is ReadOnly in C12 | `SKIP` — no C12 artifact mutation |

## Python implementation metadata

### Non-goals

- 不建立 `ModelIdentity -> RuntimeReuseKey` mapper、ACL implementation，或任何跨 BC import。
- 不建立 Registry／Retention concrete class、DI composition、backend，或 runtime lifecycle／provider management。
- 不新增 root re-export、package facade、dynamic import、`sys.modules` substitution、dependency、README、VERSION、
  release、tag、merge 或 post-merge action。

### Current Context

Identity BC、Response Reuse、Model Execution 與 Provider Adapter 都是相鄰但獨立的 bounded context；本 topic 的
five source contracts、architecture authority 與 Archify dataflow 已存在於 current source ancestor。`pyproject.toml`
已鎖定 Python 3.12、strict Pyright、Ruff 與 pytest。C11/R11/S11/T11/V11 已完成並 frozen；C12 只使 planning state
與 fixed-snapshot triage 可審核，並不新增 implementation work。architecture-path overlap 保留給 Human review／merge
coordination，不能由本 topic writer 擴張路徑或自行解決。

### Requirements

1. 只在 locked taxonomy 定義 local `RuntimeReuseKey`、同步 generic Protocol 與 immutable outcomes；不建立 consumer
   或 concrete implementation。
2. Registry key 與 runtime payload 都必須以同一 instance opaque handoff；沒有 key-field inspection、mapping 或
   runtime lifecycle side effect；key token 不可成為 `str`／hash API 或由 `repr` 暴露，且 unhashable/custom-equality
   token 不得被 key equality/hash 呼叫。
3. expected registry lookup failure、`Missing`、`Unavailable`、unexpected exception 與 retention outcomes 必須可區分。
4. C11 的 two-test subject、T11、V11 已完成且 ReadOnly；C12 不改寫 source、tests、architecture／Archify evidence 或
   direct-module imports。
5. C12 R12 receipt 必須以 nonempty six-field factual triage 完整覆蓋 fixed snapshot；F 與 architecture/ACL ownership
   保持 `DISCUSS`／Human-only `human-check`，其餘 entries 是 `SKIP`。

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

**Written:** C12 candidate does not write evidence; only a later independent R12 receipt may use its SHA-bound path.

**Modified:** only the five C12 planning artifacts.

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
- **Regression:** the two C11 isolated executable assertions must directly exercise all five regressions: opaque/unhashable/custom-equality
  token identity-only semantics; direct `importlib.import_module`; direct `__import__`; `importlib` or
  `builtins.__import__` alias/module-alias use; and LRC `ModelIdentity`／Identity `RuntimeReuseKey` duplicate semantic
  types. The alias-aware parser rejects those cross-BC paths while `tests/test_package_import.py` preserves existing
  import behavior.
- **Sequencing:** C5 architecture/dataflow and C11/R11/S11/T11/V11 commits are frozen provenance. C12 has no source or
  test subject; its R12 triage is a plan-review artifact only, and it cannot replace a future independent classification.
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

Revert only the C12 five-artifact planning candidate without modifying C11/R11/S11/T11/V11 or C5→V3 frozen provenance.
Leave read-only source, tests, architecture, `.gitkeep`, root package, configuration, adjacent BCs and evidence history
untouched.

## Implementation Steps

1. Preserve C11/R11/S11/T11/V11 and C5→V3 provenance unchanged; verify it only as read-only context.
2. Commit C12 as exactly the five declared planning artifacts; no source, test, architecture, Archify or evidence path
   may appear in its diff.
3. Independent Plan-Reviewer writes a versioned R12 receipt with the complete nonempty factual triage table above;
   Implementer commits it unchanged alone.
4. Planner Phase 4.5 alignment 已完成。其 pass 只授權獨立 Reviewer 進行 PR-thread classification；不授權 reply／resolve，
   不處理 F／architecture-ACL Human-check，也不授權 merge。

## Validation / Acceptance Checks

- Verify committed C12 `41d51072901cfd205ebc91644036e6695b1fe81c` names exactly the five planning artifacts and excludes source, tests, architecture,
  Archify artifacts and evidence paths.
- Verify the fixed C11 chain is linear: S11 `e9934dc7bb7b4f81098e635b5f0257c56da659a0` → T11
  `86a5cd54bec9d687d8d7f1738e9376435d3d1abf` → V11 `73644c2b88257832e1b4d8bedaf516b803c2ee3a`.
- Committed R12 `d738e91eb20869709d605fe7f879b340c9614b6a` must provide all ten table entries with six factual fields, two
  `DISCUSS` Human-check entries and eight `SKIP` entries. It does not claim a PR reply or resolution.

## Reviewer Handoff

```json
{
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "copilot_feedback_triage": {
    "ADDRESS": [],
    "DISCUSS": [
      {"thread":"PRRT_kwDOUJTij86jnBpk","comment":"4043480108","finding":"F: declared-path overlap","commit":"73644c2b88257832e1b4d8bedaf516b803c2ee3a","basis":"five architecture authority paths overlap another topic","disposition":"DISCUSS — Human-only human-check"},
      {"thread":"PRRT_kwDOUJTij86kQ95O","comment":"4060023123","finding":"external ACL boundary in architecture authority","commit":"73644c2b88257832e1b4d8bedaf516b803c2ee3a","basis":"architecture/ACL ownership is ReadOnly and overlaps another topic","disposition":"DISCUSS — Human-only human-check"}
    ],
    "SKIP": [
      {"thread":"PRRT_kwDOUJTij86kQe90","comment":"4059838910","finding":"per-bypass dynamic-import coverage","commit":"e9934dc7bb7b4f81098e635b5f0257c56da659a0","basis":"isolated parametrized C11 cases","disposition":"SKIP"},
      {"thread":"PRRT_kwDOUJTij86kQe94","comment":"4059838915","finding":"historical RED collection","commit":"73644c2b88257832e1b4d8bedaf516b803c2ee3a","basis":"C11 freezes historical RED and records current factual T11/V11","disposition":"SKIP"},
      {"thread":"PRRT_kwDOUJTij86kQ948","comment":"4060023096","finding":"evidence ancestry","commit":"73644c2b88257832e1b4d8bedaf516b803c2ee3a","basis":"linear S11→T11→V11 provenance","disposition":"SKIP"},
      {"thread":"PRRT_kwDOUJTij86kQ95C","comment":"4060023103","finding":"assignment alias","commit":"e9934dc7bb7b4f81098e635b5f0257c56da659a0","basis":"committed fixed-point alias analysis","disposition":"SKIP"},
      {"thread":"PRRT_kwDOUJTij86kQ95K","comment":"4060023118","finding":"retention label placement","commit":"73644c2b88257832e1b4d8bedaf516b803c2ee3a","basis":"Archify evidence is ReadOnly in C12","disposition":"SKIP"},
      {"thread":"PRRT_kwDOUJTij86knEY7","comment":"4068738285","finding":"C11 evidence ancestry","commit":"73644c2b88257832e1b4d8bedaf516b803c2ee3a","basis":"linear S11→T11→V11 provenance","disposition":"SKIP"},
      {"thread":"PRRT_kwDOUJTij86knEY_","comment":"4068738291","finding":"chained assignment alias","commit":"e9934dc7bb7b4f81098e635b5f0257c56da659a0","basis":"committed C11 alias-analysis provenance","disposition":"SKIP"},
      {"thread":"PRRT_kwDOUJTij86knEZB","comment":"4068738293","finding":"retention runtime input","commit":"73644c2b88257832e1b4d8bedaf516b803c2ee3a","basis":"Archify evidence is ReadOnly in C12","disposition":"SKIP"}
    ]
  }
}
```

## C13 Successor Route (authoritative for current execution)

### C13 exact implementation sequence

1. Implementer commits C13 as exactly the five declared planning artifacts. No candidate SHA, receipt path, subject,
   evidence, test result, or verdict is written in advance.
2. Independent Plan-Reviewer reviews that committed candidate and writes a fresh SHA-bound receipt at
   `plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<planning-candidate-40-hex-sha>.json`.
   Implementer commits unchanged approved receipt alone. `needs-rework` ends this route without a subject.
3. Implementer creates the first new immutable RED subject containing only
   `tests/test_loaded_runtime_cache_bc_independence.py`. It must collect successfully and actually fail one
   chained-assignment import-alias assertion. It does not replay, rewrite, or relabel historical `e2e125` evidence.
4. Tester writes a new SHA-bound factual Tester evidence record for that RED subject. Its non-zero command makes
   `status: failing`; Implementer commits it unchanged alone. Independent Reviewer must fail closed and write no
   review evidence for that failing subject.
5. Implementer creates a distinct green immutable subject containing only the BC-independence test plus the ten exact
   C13 dataflow artifacts. The parser correction covers all simple-name assignment targets in chained assignments.
   The dataflow correction names retain inputs `RuntimeReuseKey + runtime`, labels both returned outcomes with runtime,
   and truthfully updates validate/deliver/visual-check receipts plus only the four existing capture PNGs.
6. Tester records green-subject factual passing evidence at a new SHA-bound path; Implementer commits it unchanged
   alone. Independent Reviewer then consumes only that committed passing evidence and writes new SHA-bound approved
   review evidence; Implementer commits it unchanged alone.
7. Planner performs Phase 4.5 on the green subject, then routes a new independent current-thread classification.
   Classification alone may identify individually bounded replies/resolutions. F and ACL threads remain Human-only
   open `human-check`; no C13 role may resolve them.

### C13 validation / acceptance

- Candidate diff names exactly the five planning artifacts; a new receipt is SHA-bound and committed alone.
- RED test command collects and reaches its actual chained-assignment assertion failure; its Tester evidence records
  the real non-zero exit code and cannot be used as green/reviewer authorization.
- Green regression covers `a = b = importlib.import_module`-style all-simple-name targets and remains a direct-import
  parser test: no `importlib`/`__import__`/`sys.modules` production workaround, no cross-BC import, no source change.
- The green diff is exactly its declared test plus the ten C13 dataflow artifacts. It names retain input
  `RuntimeReuseKey + runtime`, labels `Retained(runtime)` and `NotRetained(runtime)`, passes Archify showcase
  validation/delivery, and records containment at 1440×900, 1600×1000, 1920×1080, 2048×1320.
- The five Human-owned architecture authority paths are absent from every C13 implementation/evidence diff. F and ACL
  remain unresolved Human-only threads.

### C13 reviewer handoff

```json
{
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "copilot_feedback_triage": {"ADDRESS": [], "DISCUSS": [], "SKIP": []}
}
```

The receipt is review-only. For C13, all three triage arrays remain empty: thread classification occurs only after the
green subject's passing Tester/approved Reviewer chain and Phase 4.5. A `needs-rework` receipt must instead carry
non-empty exact `issue`/`file`/`fix` blocking objects. Neither form may predeclare candidate/subject SHA, factual test
outcome, PR reply, thread resolution, Human review, or merge.

## Post-merge / release actions

No repository release action is required. Human alone decides merge; this non-stable topic has no README, VERSION,
release-note, tag or post-merge action.

## Open Questions / Unresolved Items

`package-topology-skeleton-replay` 與本 topic 的五份 architecture authority docs 存在 declared-path ownership
overlap。此為 Human-only unresolved `human-check`：僅能在 Human review／merge coordination 處置；本 topic 不得自行
解決、變更 locked mission／scope 或改寫既定 architecture path。Concrete `ModelIdentity -> RuntimeReuseKey`
conversion and Registry／Retention implementation remain deferred to future, separately planned integration／DI topics.

## Workflow State Contract

- current_step: c13-planning-candidate-ready-for-commit
- next_step: c13-candidate-only-commit
- status: IN_PROGRESS
