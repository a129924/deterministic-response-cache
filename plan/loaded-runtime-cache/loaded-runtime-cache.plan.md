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
| In-Scope | local immutable opaque `RuntimeReuseKey`（identity-only key semantics）；`RuntimeRegistry[RuntimeT]`、`RuntimeRetention[RuntimeT]` Protocol；`Available`、`Missing`、`Unavailable`、`Retained`、`NotRetained` outcomes；locked module taxonomy、direct-module contract tests、alias-aware BC-independence regression；completed C12/R12 provenance；以及 C14 的 chained-assignment RED→green correction、truthful bounded Archify evidence correction 與新的 evidence/classification route。 |
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
- C13 `a623981989f3363a4b225319a432c3a9d8e28b96`、R13 `cf91b55f80f1764e040c95c822ae55b290e3699c`、RED `3ba583bed8c367b756e2cb450e468f1274d04193`、failing evidence `c4f229f14d3c4c38d40cdda8ad0429712e0ae189` 和 green `ade584e7eb63a7846a23c073c06a802ff99ff6cf`
  是 frozen provenance；最後一者是 `needs-rework`，沒有 routing authority。C14 是 Human-authorized planning successor；
  它保留原 mission／scope／Protocol contract，僅重建 review-required
  evidence chain：collection-success、actual assertion-failing chained-assignment RED test-only subject → factual
  failing Tester evidence → new green immutable subject with all-simple-name assignment-target repair → passing Tester
  evidence → approved independent Reviewer evidence → Planner Phase 4.5 → new classification。不得重播或改寫 historical
  `e2e125` evidence；RED failing evidence 不授權 Reviewer record、publish、reply、resolve 或 merge。
- C14 green subject 的 dataflow allowlist 是 Artifact Paths 所列十個 path 的唯一集合；它只納入由本次 JSON／HTML
  delivery／visual-check 真實 byte-changed 的 subset。`validation.json` 或 `visual-check.html` 若 byte-identical 必須
  ReadOnly，不得人為改寫。它修正 retain input `RuntimeReuseKey + runtime`、`Retained(runtime)`／
  `NotRetained(runtime)` labels、edge placement 及 four-viewport containment；不得改變
  protocol-only boundary 或暗示 concrete backend、DI、runtime lifecycle。

## Boundaries / Exclusions

| Category | Exact contract |
| --- | --- |
| ReadOnly | `src/deterministic_response_cache/identity/**`、`response_reuse/**`、`model_execution/**`、`provider_adapter/**`、root `__init__.py`、`loaded_runtime_cache/.gitkeep`、五個 existing source modules、`pyproject.toml`、`README.md`、version metadata、workflow contracts、`.github/agents/**`，以及 Human-owned `docs/business-capability-architecture.md`、`docs/evolution-roadmap.md`、`docs/architecture/business-capability/architecture-brief.md`、`docs/architecture/business-capability/index.html`、`docs/architecture/business-capability/scene.js`。F／ACL threads stay Human-only. |
| Written | C14 Plan-Reviewer receipt、RED/green SHA-bound Tester evidence 與 green SHA-bound Independent Reviewer evidence；each writer creates it and Implementer commits each unchanged as a sole evidence-only commit. |
| Modify | C14 candidate only the five planning artifacts; RED only `tests/test_loaded_runtime_cache_bc_independence.py`; green only that test plus the truthful byte-changed subset of the ten-path dataflow allowlist in Artifact Paths. |
| Deleted | 無；不得刪除 `.gitkeep`、existing tests 或既有 artifacts。 |

## Status / Allowed Transitions (C14 frozen historical provenance)

- **Historical C14 state**: `c14-phase-4.5-thread-classification-pending`。C14 的 committed factual chain 是 candidate
  `4d78eaf997847eb3b872c4c609ba23f19c6e5dc5` → approved Plan-Reviewer receipt-only commit
  `033fa34ca27a9c924c7fc95b9aa9c87c33b24217` → collection-success / assertion-failing RED subject
  `6acbbe6d3f9b98566def9448afa760e095833a0b` → failing Tester evidence-only commit
  `287781cee3b7f5603d6ea58059ab3b9782d7e806` → green subject
  `5201c30e604c8fd9cc84bd6d05c00c6b61575612` → passing Tester evidence-only commit
  `6a9a543b1fb4c1389c1c5474e50995440a046dcd` → approved Independent Reviewer evidence-only commit
  `4632380fa1b254046d04a6b92c9d9912836e7ee1`。其後只待 Planner Phase 4.5 與 fresh independent current-thread
  classification；F／ACL 維持 Human-only `human-check`。本次只是在已提交 receipt/evidence 後依 Human 授權同步 state，
  不建立新的 candidate、Plan-Reviewer receipt 或任何 PR reply／resolution claim。C12 candidate
  `41d51072901cfd205ebc91644036e6695b1fe81c` 與其 approved R12 receipt-only commit
  `d738e91eb20869709d605fe7f879b340c9614b6a` 已提交，且 receipt 的 SHA-bound path 是
  `plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-41d51072901cfd205ebc91644036e6695b1fe81c.json`。
  C11 `55ad5d48c8e638bc5a81f3d0fecfc5a5f35e963c`、R11
  `01da31b11dcc8013f03a773ad9e9042c8bb527bf`、S11
  `e9934dc7bb7b4f81098e635b5f0257c56da659a0`、T11
  `86a5cd54bec9d687d8d7f1738e9376435d3d1abf`、V11
  `73644c2b88257832e1b4d8bedaf516b803c2ee3a` 均為 completed frozen provenance。C8/C9/C10 是 frozen、unapproved
  predecessor；C5→V3 也是 frozen provenance，均不能作 C14 routing authority。C13 `a623981989f3363a4b225319a432c3a9d8e28b96`、R13 `cf91b55f80f1764e040c95c822ae55b290e3699c`、RED
  `3ba583bed8c367b756e2cb450e468f1274d04193`、failing evidence `c4f229f14d3c4c38d40cdda8ad0429712e0ae189`、與 `ade584e7eb63a7846a23c073c06a802ff99ff6cf` 亦均 frozen；`ade584e7…` 是
  `needs-rework`。
- **Execution model**: C14 candidate-only commit → independent SHA-bound approved C14 Plan-Reviewer receipt →
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
| Requirements | `analysis/loaded-runtime-cache/requirements.md` | Plan-Creator | C14 candidate-only planning artifact. |
| Technical specification | `analysis/loaded-runtime-cache/technical-spec.md` | Plan-Creator | C14 candidate-only planning artifact. |
| Topic plan | `plan/loaded-runtime-cache/loaded-runtime-cache.plan.md` | Plan-Creator | C14 routing contract; no SHA/outcome prefill. |
| Topic specification | `plan/loaded-runtime-cache/loaded-runtime-cache.spec.md` | Plan-Creator | C14 acceptance and error scenarios. |
| Step tracker | `plan/loaded-runtime-cache/loaded-runtime-cache.step.md` | Plan-Creator | C14 phase truth only. |
| Plan-review receipt | `plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<planning-candidate-40-hex-sha>.json` | Independent Plan-Reviewer writes; Implementer commits unchanged alone | SHA-bound normal-plan verdict. |
| C14 RED test subject | `tests/test_loaded_runtime_cache_bc_independence.py` | Implementer | Only after approved C14 receipt; collection-success, actual assertion-failing chained-assignment regression. |
| C14 RED Tester evidence | `plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<red-subject-40-hex-sha>.json` | Tester writes; Implementer commits unchanged alone | Exact factual schema; `failing` requires at least one non-zero command exit; no Reviewer record is permitted. |
| C14 green subject | `tests/test_loaded_runtime_cache_bc_independence.py` | Implementer | New immutable subject; handles all-simple-name chained assignment targets. |
| C14 green Tester evidence | `plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<green-subject-40-hex-sha>.json` | Tester writes; Implementer commits unchanged alone | Exact factual schema; `passing` requires all command exits to be zero. |
| C14 green review evidence | `plan/loaded-runtime-cache/loaded-runtime-cache.implementation-review-log-<green-subject-40-hex-sha>.json` | Independent Reviewer writes; Implementer commits unchanged alone | May consume only the committed matching green `passing` Tester evidence. |
| C14 dataflow allowlist | `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.json`; `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.html`; `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.validation.json`; `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.delivery.json`; `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.json`; `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.html` | Implementer | Sole ten-path allowlist with the four captures below; green subject includes only the truthful byte-changed subset. Byte-identical `.validation.json`／`.visual-check.html` are ReadOnly. |
| C14 existing captures | `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.1440x900.dark.png`; `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.1440x900.light.png`; `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.2048x1320.dark.png`; `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.2048x1320.light.png` | Implementer | Part of sole ten-path allowlist; include only truthful changed captures. |
| Architecture authority | `docs/business-capability-architecture.md` | None — ReadOnly | Human-only overlap / merge coordination; C11 must not rewrite it. |
| Architecture authority | `docs/evolution-roadmap.md` | None — ReadOnly | Human-only overlap / merge coordination; C11 must not rewrite it. |
| Architecture authority | `docs/architecture/business-capability/architecture-brief.md` | None — ReadOnly | Human-only overlap / merge coordination; C11 must not rewrite it. |
| Architecture authority | `docs/architecture/business-capability/index.html` | None — ReadOnly | Human-only overlap / merge coordination; C11 must not rewrite it. |
| Architecture authority | `docs/architecture/business-capability/scene.js` | None — ReadOnly | Human-only overlap / merge coordination; C11 must not rewrite it. |
| Other Archify evidence | every `docs/architecture/loaded-runtime-cache/**` path not named above | None — ReadOnly | C14 must not broaden its dataflow correction allowlist. |
| Completed C11/R11/S11/T11/V11 records | C11/R11/S11/T11/V11 exact committed paths and SHAs named in Status | None — ReadOnly | Immutable completed provenance; no C12 routing reuse. |
| Plan-review receipt (R12) | `plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-41d51072901cfd205ebc91644036e6695b1fe81c.json` | None — ReadOnly | Approved R12 verdict and nonempty fixed-snapshot triage, committed alone in `d738e91eb20869709d605fe7f879b340c9614b6a`. |

Every unlisted path is read-only. The fixed-name legacy plan-review receipt from the abandoned lineage is historical,
frozen provenance only: it is not an artifact of C11, must not be created or overwritten, and has no routing
authority. Each current or successor candidate uses only the SHA-bound template above; no candidate SHA is prefilled.
Legacy fixed-name T1／V1 evidence, including the `6110cb…` Tester and `44e477…` Reviewer lineage, is likewise frozen:
T3／V3 and C5 provenance must never be overwritten, reused, or inferred as C11 facts.

For C14, the currently observed truthful green paths are the BC-independence test, dataflow JSON／HTML, delivery JSON,
visual-check JSON, and the four existing capture PNGs. They are factual worktree provenance, not a requirement to
rewrite every allowlisted path; `.validation.json` and `.visual-check.html` remain ReadOnly when their rebuild is
byte-identical.

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

**Written:** C14 only: (1) the independent Plan-Reviewer receipt at
`plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<planning-candidate-40-hex-sha>.json`; (2) the
RED factual Tester record at
`plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<red-subject-40-hex-sha>.json`; (3) the green
factual Tester record at
`plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<green-subject-40-hex-sha>.json`; and (4) the green
Independent Reviewer record at
`plan/loaded-runtime-cache/loaded-runtime-cache.implementation-review-log-<green-subject-40-hex-sha>.json`. The
respective independent writer writes each record; only an Implementer may commit it unchanged in its own sole
evidence-only commit. No Reviewer record exists for the failing RED subject.

**Modified:** C14 candidate changes exactly the five planning artifacts. The RED subject changes only
`tests/test_loaded_runtime_cache_bc_independence.py`. The later green subject changes only that test plus the truthful
byte-changed subset of the ten-path dataflow allowlist listed in `Artifact Paths`; byte-identical
`.validation.json`／`.visual-check.html` stay ReadOnly.

**ReadOnly:** all Identity, Response Reuse, Model Execution, Provider Adapter, root-package, five existing source
modules, configuration, workflow-contract and `.github/agents/**` paths; every unlisted Archify path; C5→V3,
C11→V11, C12→R12 and `9aa656b13fdc36492273c97a62eb9d422a1b64b5` (unapproved `needs-rework` provenance); and the
five Human-owned architecture-authority paths enumerated in `Boundaries / Exclusions`.

### Test Plan

- **C14 RED:** after a committed approved C14 Plan-Reviewer receipt, run the direct-import regression from the
  one-file RED subject. Collection must succeed and the chained-assignment import-alias assertion must actually fail;
  Tester records the actual non-zero exit code in the RED SHA-bound record. It is factual failure, never
  expected-failing authorization, and fails closed to a new green subject only.
- **C14 green:** a distinct subject must cover every all-simple-name target in a chained import-alias assignment,
  remain a direct parser regression, and pass without `importlib`, `__import__`, `sys.modules`, source, or cross-BC
  workaround. Tester records actual zero exits in the green SHA-bound record.
- **C14 dataflow:** validate and deliver at showcase quality, then record containment for 1440×900, 1600×1000,
  1920×1080 and 2048×1320. The diagram must name `RuntimeReuseKey + runtime`, `Retained(runtime)`, and
  `NotRetained(runtime)` with unobscured synchronous outcome edges.
- **Evidence gate:** an Independent Reviewer may consume only a committed, same-topic, same-green-subject `passing`
  Tester record. A failing, malformed, uncommitted, cross-subject, abbreviated-SHA, overwritten, or non-sole evidence
  record fails closed. C11→V11, C12→R12 and C13 are provenance only, not C14 test authority.

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

Before a C14 candidate receipt is approved, revert only the five-artifact C14 planning candidate. After approval,
revert only the immutable C14 subject or its sole C14 evidence commit that requires repair and restart the applicable
C14 route with a new subject SHA. Never rewrite, delete, or reuse C5→V3, C11→V11, C12→R12, C13, or
`9aa656b13fdc36492273c97a62eb9d422a1b64b5` provenance. Leave all Human-owned architecture authority, unlisted
paths, source contracts, configuration, and adjacent BCs untouched.

## Implementation Steps

1. Preserve C5→V3, C11→V11, C12→R12, C13 `a623981989f3363a4b225319a432c3a9d8e28b96`→`ade584e7eb63a7846a23c073c06a802ff99ff6cf`, and `9aa656b13fdc36492273c97a62eb9d422a1b64b5` solely as frozen provenance.
2. Implementer commits C14 as exactly the five planning artifacts; it predeclares no candidate SHA, receipt, subject,
   evidence, test result, or verdict.
3. Independent Plan-Reviewer writes a new SHA-bound `approved` receipt for that committed C14 candidate; Implementer
   commits it unchanged alone. `needs-rework` stops before any C14 subject.
4. Implementer creates the one-file RED immutable subject; Tester writes a factual `failing` SHA-bound RED record;
   Implementer commits it unchanged alone. No Reviewer may write or consume a failing RED record.
5. Implementer creates a distinct green subject limited to the declared test and truthful byte-changed subset of the
   ten-path dataflow allowlist. Tester writes
   factual `passing` green evidence; Implementer commits it unchanged alone.
6. Independent Reviewer consumes only that committed passing green evidence, writes the SHA-bound green review record,
   and Implementer commits it unchanged alone. Planner then performs Phase 4.5 and routes fresh thread classification.
   F／ACL remain open Human-only `human-check`.

## Validation / Acceptance Checks

- C14 candidate names exactly the five planning artifacts and has no prefilled SHA, receipt, subject, evidence,
  result, or approval. Its receipt is fresh, SHA-bound, `approved`, and committed alone.
- RED evidence has the exact Tester schema, a full 40-hex RED subject SHA, a non-empty command list with at least one
  non-zero exit, and `status: failing`; it has no Reviewer companion record.
- Green evidence has the exact Tester schema, the same full 40-hex green subject SHA, non-empty all-zero commands and
  `status: passing`; its sole evidence commit is the only input to the exact-schema green Reviewer record.
- The green subject modifies the declared test plus only its truthful byte-changed subset of the ten-path dataflow
  allowlist; byte-identical `.validation.json`／`.visual-check.html` remain ReadOnly. It passes direct-import
  regression and Archify showcase validate/deliver plus the four required viewport containment checks.
- F and ACL remain unresolved Human-only `human-check`; neither C14 receipt/evidence nor Phase 4.5 directly replies to
  or resolves a PR thread.

## Frozen C12 receipt schema (provenance only)

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

## C14 Successor Route (frozen historical provenance)

### C14 truthful implementation sequence

1. Implementer commits C14 as exactly the five declared planning artifacts. No candidate SHA, receipt path, subject,
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
5. Implementer creates a distinct green immutable subject containing only the BC-independence test plus the truthful
   byte-changed subset of the sole ten-path C14 dataflow allowlist. The parser correction covers all simple-name
   assignment targets in chained assignments.
   The dataflow correction names retain inputs `RuntimeReuseKey + runtime`, labels both returned outcomes with runtime,
   and truthfully updates validate/deliver/visual-check artifacts plus only changed existing capture PNGs. A
   byte-identical `.validation.json` or `.visual-check.html` is not included and remains ReadOnly.
6. Tester records green-subject factual passing evidence at a new SHA-bound path; Implementer commits it unchanged
   alone. Independent Reviewer then consumes only that committed passing evidence and writes new SHA-bound approved
   review evidence; Implementer commits it unchanged alone.
7. Planner performs Phase 4.5 on the green subject, then routes a new independent current-thread classification.
   Classification alone may identify individually bounded replies/resolutions. F and ACL threads remain Human-only
   open `human-check`; no C14 role may resolve them.

### C14 validation / acceptance

- Candidate diff names exactly the five planning artifacts; a new receipt is SHA-bound and committed alone.
- RED test command collects and reaches its actual chained-assignment assertion failure; its Tester evidence records
  the real non-zero exit code and cannot be used as green/reviewer authorization.
- Green regression covers `a = b = importlib.import_module`-style all-simple-name targets and remains a direct-import
  parser test: no `importlib`/`__import__`/`sys.modules` production workaround, no cross-BC import, no source change.
- The green diff is its declared test plus only the truthful byte-changed subset of the ten C14 dataflow paths. It names retain input
  `RuntimeReuseKey + runtime`, labels `Retained(runtime)` and `NotRetained(runtime)`, passes Archify showcase
  validation/delivery, and records containment at 1440×900, 1600×1000, 1920×1080, 2048×1320.
- The five Human-owned architecture authority paths are absent from every C14 implementation/evidence diff. F and ACL
  remain unresolved Human-only threads.

## Reviewer Handoff

```json
{
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "copilot_feedback_triage": {"ADDRESS": [], "DISCUSS": [], "SKIP": []}
}
```

The receipt is review-only. For C14, all three triage arrays remain empty: thread classification occurs only after the
green subject's passing Tester/approved Reviewer chain and Phase 4.5. A `needs-rework` receipt must instead carry
non-empty exact `issue`/`file`/`fix` blocking objects. Neither form may predeclare candidate/subject SHA, factual test
outcome, PR reply, thread resolution, Human review, or merge.

The Plan-Reviewer must verify that any C14 green artifact named by its successor route belongs to the sole ten-path
allowlist and was truthfully byte-changed by JSON／HTML delivery／visual-check; a byte-identical `.validation.json` or
`.visual-check.html` remains ReadOnly and is not a missing-artifact defect.

For both C14 Tester records, the JSON object has exactly `schema_version`, `topic`,
`implementation_subject_commit`, `status`, `commands`, `recorded_by`. `schema_version` is integer `1`; `topic` is
`loaded-runtime-cache`; the subject is the respective full 40-character lowercase hexadecimal subject SHA;
`recorded_by` is `Tester`; and `commands` is non-empty, with each object having only non-empty string `command` and
integer `exit_code`. `passing` requires every exit to be `0`; `failing` requires at least one non-zero exit. The RED
path is bound to the RED SHA and must be `failing`; the green path is bound to the distinct green SHA and must be
`passing`. Any extra/missing key, wrong status, abbreviated SHA, path collision, uncommitted record, cross-topic or
cross-subject reference, or non-sole evidence commit fails closed.

The C14 green review record is one JSON object with exactly `schema_version`, `topic`,
`implementation_subject_commit`, `tester_evidence_commit`, `verdict`, `blocking_issues`, `recorded_by`.
`schema_version` is integer `1`; both references are full 40-character lowercase hexadecimal SHAs; `recorded_by` is
`Independent Reviewer`; `verdict` is `approved|needs-rework`; and `blocking_issues` is a string array, empty exactly
for `approved` and non-empty for `needs-rework`. The `tester_evidence_commit` must be the committed sole
evidence-only commit containing the same-topic, same-green-subject `passing` Tester record. Independent Reviewer must
fail closed and produce no record for the RED `failing` evidence or any malformed/mismatched input.

## Post-merge / release actions

No repository release action is required. Human alone decides merge; this non-stable topic has no README, VERSION,
release-note, tag or post-merge action.

## Open Questions / Unresolved Items

`package-topology-skeleton-replay` 與本 topic 的五份 architecture authority docs 存在 declared-path ownership
overlap。此為 Human-only unresolved `human-check`：僅能在 Human review／merge coordination 處置；本 topic 不得自行
解決、變更 locked mission／scope 或改寫既定 architecture path。Concrete `ModelIdentity -> RuntimeReuseKey`
conversion and Registry／Retention implementation remain deferred to future, separately planned integration／DI topics.

## Workflow State Contract

- current_step: c16-plan-authoring
- next_step: Implementer commits the five C16 planning artifacts
- status: IN_PROGRESS

## C15 Mixed-Assignment Successor Route (authoritative for current execution)

### Goal / Outcome

C15 preserves the established Loaded Runtime Cache protocol-first mission and only repairs the static
BC-independence regression's mixed `ast.Assign` alias semantics: preserve direct simple-name targets and ignore
direct attribute/non-simple targets. It does not change Registry, Retention, outcomes, source taxonomy, public API,
or BC boundaries.

### Scope, boundaries, and non-goals

| Field | Contract |
| --- | --- |
| In-Scope | exactly five C15 planning artifacts; fresh test-only RED→green correction in `tests/test_loaded_runtime_cache_bc_independence.py`; SHA-bound versioned receipt/evidence templates; C15 Tester/Reviewer/Phase 4.5/classification sequence. |
| Out-of-Scope | production source, protocols/API, Registry backend, DI, lifecycle, mapper/ACL, other BC, Archify, business architecture, PR reply/resolve/publish/merge/release. |
| ReadOnly | every unlisted path, all source, all docs/architecture, workflow contracts, prior records, C14, `37d7233e7231151c0dac6aaa1a7820bff746ffdc`, F/ACL thread ownership. |
| Written | future versioned Plan-Reviewer receipt, RED/green Tester evidence, and green independent Reviewer evidence only; each is written by its designated role then committed unchanged alone by Implementer. |
| Modified | candidate: exactly the five planning artifacts; RED/green subjects: only `tests/test_loaded_runtime_cache_bc_independence.py`. |
| Deleted | none. |

No recursive destructuring, AST execution/evaluation, dynamic import, `importlib`/`__import__`/`sys.modules`
substitution, runtime introspection, cross-BC import, source workaround, architecture change, or Human-only PR action
is permitted. This is non-stable-library work: no README, VERSION, release note, tag, or post-merge action.

### Locked decisions / Python implementation metadata

- **Async-planning status:** exempt — static synchronous AST test analysis only; no async boundary, lifecycle,
  concurrency, cancellation, timeout, or external I/O decision.
- **Module/package placement:** only `tests/test_loaded_runtime_cache_bc_independence.py` after planning approval.
- **New public API / interface / breaking change / dependencies:** no / no / no / no.
- **Error handling:** factual assertion outcomes flow to Tester evidence; no production exception behavior changes.
- **Typing:** retain existing Python 3.12 test typing; no `Any`, cast, dynamic typing workaround, or runtime inspection.
- For one `ast.Assign`, inspect direct `assignment.targets` only. Every direct `ast.Name` is a local alias. A direct
  `ast.Attribute` or other non-simple target is ignored, without traversing its children.
- `load = holder.loader = importlib.import_module` therefore retains `load` only. A later direct `load(...)` must
  stay detectable; `holder.loader` must never become a local alias.
- C14 and `37d7233e7231151c0dac6aaa1a7820bff746ffdc` are frozen nonrouting provenance. They establish no C15 fact.
- F／ACL/business-architecture threads remain open Human-only `human-check`; C15 evidence/classification never
  replies to, resolves, approves, merges, releases, or post-merges them.

### Status / allowed transitions

**Current state:** `c15-phase-4.5-alignment-pending`. The committed C15 chain is
`eadd406409a02dc1c283e7ff9740815f4c9e4596` →
`d8e759ea0bdd70ca7d6eca4dc030f11879c59c25` →
`2e9cabd5d21c0ef4c9a9929efedf8efc2a776e6a` →
`94e6d6f73b85efa5a5895e7eadb4aa9aa24089ee` →
`7dab2b9742bd19f962bef99be83b40b978f87f0f` →
`475e3c953f6551bef5834d0bf350d5c79449a43e` →
`cee5097c176b4321a0d9bc2e810caf7d3425d0f1`.
It completes C15 planning, the SHA-bound approved Plan-Reviewer receipt, RED subject/evidence, green subject/passing
Tester evidence, and independent green review evidence. Planner Phase 4.5 alignment is pending. This post-receipt
state tracking neither creates C16 nor creates a new receipt or evidence; it does not process any PR thread.

This C15 section supersedes every earlier C14 current-state, artifact-path,
implementation-step, validation, handoff, and workflow-state claim for routing; those C14 sections remain historical
provenance only.

`planned` → `planning-candidate-committed` → `plan-review-in-progress` → `plan-review-receipt-committed` →
`implementation-in-progress` → `tester-in-progress` → `tester-evidence-committed` → `reviewer-in-progress` →
`reviewer-evidence-committed` → `approved` → `phase-4.5-aligned` → `thread-classification-pending`.

The first implementation subject is collection-success/assertion-failing RED and receives factual `failing` Tester
evidence only. It cannot receive Reviewer evidence. A distinct green subject receives factual `passing` Tester
evidence then independent approved Reviewer evidence; only that green chain may reach Phase 4.5.

### Artifact paths

| Artifact | Exact path | Write owner | Contract |
| --- | --- | --- | --- |
| Requirements | `analysis/loaded-runtime-cache/requirements.md` | Plan-Creator | C15 candidate only. |
| Technical specification | `analysis/loaded-runtime-cache/technical-spec.md` | Plan-Creator | C15 candidate only. |
| Topic plan | `plan/loaded-runtime-cache/loaded-runtime-cache.plan.md` | Plan-Creator | C15 routing contract. |
| Topic specification | `plan/loaded-runtime-cache/loaded-runtime-cache.spec.md` | Plan-Creator | C15 acceptance contract. |
| Step tracker | `plan/loaded-runtime-cache/loaded-runtime-cache.step.md` | Plan-Creator | C15 phase truth only. |
| Plan-review receipt | `plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<planning-candidate-40-hex-sha>.json` | Independent Plan-Reviewer; Implementer commits unchanged alone | Fresh approved receipt. |
| RED subject / green subject | `tests/test_loaded_runtime_cache_bc_independence.py` | Implementer | Separate immutable test-only subjects. |
| RED Tester evidence | `plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<red-subject-40-hex-sha>.json` | Tester; Implementer commits unchanged alone | Factual failing record only. |
| Green Tester evidence | `plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<green-subject-40-hex-sha>.json` | Tester; Implementer commits unchanged alone | Same-subject passing record only. |
| Green review evidence | `plan/loaded-runtime-cache/loaded-runtime-cache.implementation-review-log-<green-subject-40-hex-sha>.json` | Independent Reviewer; Implementer commits unchanged alone | Consumes only committed matching passing green evidence. |

All versioned paths are templates. No future candidate SHA, receipt, subject SHA, evidence, result, or approval is
prefilled or created by this candidate.

### Implementation steps

1. Implementer commits exactly the five C15 planning artifacts.
2. Independent Plan-Reviewer writes a fresh approved SHA-bound receipt; Implementer commits it unchanged alone.
3. Implementer creates a fresh RED test-only subject with the mixed-assignment assertion; collection succeeds and it
   factually fails. Tester records non-zero evidence; Implementer commits it unchanged alone.
4. Implementer creates distinct green test-only subject: direct `ast.Name` targets are preserved, direct non-simple
   targets are ignored, and no recursion/prohibited mechanism is introduced.
5. Tester records passing green evidence; Implementer commits it unchanged alone. Independent Reviewer records
   approved matching green review evidence; Implementer commits it unchanged alone.
6. Planner runs Phase 4.5 then routes fresh independent thread classification; Human-only boundaries remain open.

### Validation / acceptance checks

- RED collects, then its mixed-assignment assertion exits non-zero and is recorded exactly as `failing`.
- Green targeted regression passes and proves `load` remains an alias while `holder.loader` does not.
- Tuple/list/starred/subscript/attribute and all other non-simple targets are not recursively traversed or retained.
- Both implementation commits modify only the declared test file. No source, docs, architecture, dynamic import,
  runtime introspection, or cross-BC change occurs.
- Tester and Reviewer records satisfy the exact existing schemas, full SHA-bound paths, same-subject relation, and
  sole evidence-only commit ordering.

### Reviewer handoff

The independent Plan-Reviewer verifies exactly five candidate paths, absence of prefilled future facts, the direct
`ast.Name`/ignored non-simple-target contract, fresh C15 sequence, test-only implementation paths, frozen C14/`37d723`
provenance, and Human-only F/ACL/business-architecture boundary. It writes exactly one JSON object with `verdict`,
`blocking_issues`, `copilot_feedback_triage` at the candidate-SHA versioned path. Its receipt has no PR resolution
authority.

### Post-merge / release actions

None; Human-only merge/release/post-merge remains outside C15.

### Open questions / unresolved items

None for C15 planning. F／ACL/business architecture remains an intentional Human-only boundary.

## C16 C15 Thread-Classification Receipt Successor (authoritative for current execution)

### Goal / Outcome

C16 establishes the missing immutable, auditable receipt contract for independently classifying the seven unresolved
PR #7 threads against the already approved C15 chain. It does not change the Loaded Runtime Cache capability or repair
any finding itself.

### Scope, boundaries, and non-goals

| Field | Contract |
| --- | --- |
| In-Scope | exactly five C16 planning artifacts; C16 candidate/independent Plan-Reviewer receipt; one fixed C15-bound classification receipt; later exact reply/resolve only for pairs classified `REPLY_AND_RESOLVE`. |
| Out-of-Scope / Non-Goal | production source, tests, Protocol/API, Registry backend, DI, runtime lifecycle, mapper/ACL implementation, all docs/architecture/Archify, C15 evidence rewrite, new RED/green work, merge/release/post-merge. |
| ReadOnly | every unlisted path; all earlier C15/C14/C12 provenance; the two Human-only threads; every PR thread unless the committed classification receipt marks that exact pair `REPLY_AND_RESOLVE`. |
| Written | standard C16 Plan-Reviewer receipt, then only `loaded-runtime-cache.thread-classification-receipt-7dab2b9742bd19f962bef99be83b40b978f87f0f.json`. |
| Modified | C16 candidate: exactly the five planning artifacts. The classification receipt is a new evidence file only. |
| Deleted | none. |

### Locked evidence and classification schema

The binding C15 facts are subject `7dab2b9742bd19f962bef99be83b40b978f87f0f`, passing Tester-evidence commit
`475e3c953f6551bef5834d0bf350d5c79449a43e`, approved implementation-review-evidence commit
`cee5097c176b4321a0d9bc2e810caf7d3425d0f1`, and PR snapshot `7e525b1ad8dc77c25b0b11a467f6b1f24884ecd3`.
They must be complete 40-character lower-case hexadecimal committed ancestor facts; none may be replaced, abbreviated,
or inferred from chat.

The one classification receipt path is exact and non-overwritable:
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-7dab2b9742bd19f962bef99be83b40b978f87f0f.json`.
Independent Reviewer is its sole writer; Implementer is the sole committer and must commit it unchanged in a sole
evidence-only commit. It must have exactly these top-level keys:

```json
{
  "schema_version": 1,
  "topic": "loaded-runtime-cache",
  "implementation_subject_commit": "7dab2b9742bd19f962bef99be83b40b978f87f0f",
  "tester_evidence_commit": "475e3c953f6551bef5834d0bf350d5c79449a43e",
  "implementation_review_evidence_commit": "cee5097c176b4321a0d9bc2e810caf7d3425d0f1",
  "pr_head_commit": "7e525b1ad8dc77c25b0b11a467f6b1f24884ecd3",
  "classifications": [],
  "recorded_by": "Independent Reviewer"
}
```

`classifications` must ultimately contain exactly these seven pairs, and every entry must have exactly `thread`,
`comment`, `outcome`, `reply`: `PRRT_kwDOUJTij86kQ95O`/`4060023123`,
`PRRT_kwDOUJTij86kqiZu`/`4070096548`, `PRRT_kwDOUJTij86kqiZ5`/`4070096561`,
`PRRT_kwDOUJTij86lAR8J`/`4078761983`, `PRRT_kwDOUJTij86lAR8P`/`4078761993`,
`PRRT_kwDOUJTij86lAR8T`/`4078761998`, `PRRT_kwDOUJTij86lAR8Y`/`4078762005`.
`outcome` is `REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK`. A non-empty `reply` is allowed only for
`REPLY_AND_RESOLVE`; `ADDRESS` and `HUMAN_CHECK` require JSON `null`. ACL
`PRRT_kwDOUJTij86kQ95O`/`4060023123` and business-architecture
`PRRT_kwDOUJTij86kqiZ5`/`4070096561` are locked `HUMAN_CHECK`/`null`; the other five outcomes and replies are not
prefilled and remain the independent Reviewer's decision.

### Status / allowed transitions

**Current state:** `c16-plan-authoring`. C15 is completed frozen routing evidence only; C16 supersedes its pending
Phase 4.5/classification claim. The allowed route is `planned` → `planning-candidate-committed` →
`plan-review-receipt-committed` → `classification-review-in-progress` →
`classification-receipt-committed` → (`reply-resolve` for exact `REPLY_AND_RESOLVE` pairs | new Planner successor
for `ADDRESS` | `human-check` for `HUMAN_CHECK`). C16 has no RED, green, Tester, or implementation-review phase.

### Artifact paths and execution steps

| Artifact | Exact path | Write owner | Contract |
| --- | --- | --- | --- |
| Requirements | `analysis/loaded-runtime-cache/requirements.md` | Plan-Creator | C16 candidate only. |
| Technical specification | `analysis/loaded-runtime-cache/technical-spec.md` | Plan-Creator | C16 candidate only. |
| Topic plan | `plan/loaded-runtime-cache/loaded-runtime-cache.plan.md` | Plan-Creator | C16 routing contract. |
| Topic specification | `plan/loaded-runtime-cache/loaded-runtime-cache.spec.md` | Plan-Creator | C16 acceptance contract. |
| Step tracker | `plan/loaded-runtime-cache/loaded-runtime-cache.step.md` | Plan-Creator | C16 phase truth. |
| Plan-review receipt | `plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<c16-candidate-40-hex-sha>.json` | Independent Plan-Reviewer; Implementer commits unchanged alone | Fresh approved C16 planning receipt. |
| Classification receipt | `plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-7dab2b9742bd19f962bef99be83b40b978f87f0f.json` | Independent Reviewer; Implementer commits unchanged alone | C15-bound seven-pair factual classification. |

1. Implementer commits exactly the five C16 planning artifacts.
2. Independent Plan-Reviewer writes an approved, candidate-SHA-bound C16 receipt; Implementer commits it unchanged
   alone. A `needs-rework` receipt routes no classification.
3. Independent Reviewer validates the four bound C15 facts and writes the sole classification receipt, with exact
   seven pairs and no prefilled result for the five independent decisions.
4. Implementer commits that receipt unchanged alone. Only then may Planner route an Implementer to reply and resolve
   an exact `REPLY_AND_RESOLVE` pair. `ADDRESS` returns to Planner; `HUMAN_CHECK` stays open.

### Validation / acceptance checks

- C16 candidate modifies only the five declared planning artifacts and has a fresh approved Plan-Reviewer receipt.
- Classification receipt has exactly its declared path, top-level keys, writer, full-SHA bindings, and seven unique
  thread/comment pairs.
- ACL `4060023123` and business-architecture `4070096561` are `HUMAN_CHECK` with JSON `null` reply; no actor replies
  to or resolves either thread.
- Only a committed same-snapshot `REPLY_AND_RESOLVE` entry authorizes one factual reply and resolve for its exact pair;
  `ADDRESS` never masquerades as resolved.

### Reviewer handoff

The independent Plan-Reviewer checks C16's five-path candidate scope, C15 bindings, exact schema/value space,
Human-only pair locks, and absence of outcomes/replies for the other five pairs. Independent Reviewer then classifies
only the seven listed current pairs; it cannot modify code or PR state.

### Post-merge / release actions

None. Human-only merge/release/post-merge remains outside C16.

## C17 ADDRESS remediation successor (authoritative for current routing)

### Goal / outcome

C17 remediates only C16 `ADDRESS` findings `4078761993` and `4078762005`: it closes the static scanner's
`getattr`-derived `importlib`/`sys` alias bypass with fresh RED→green evidence, and corrects the topic dataflow to
show the actual `RuntimeRegistry.lookup -> RuntimeT | None` protocol. It does not make the diagram proof of a
concrete runtime backend.

### Scope / boundaries

| Field | Contract |
| --- | --- |
| In-Scope | five C17 planning artifacts; fresh test-only RED/failing Tester evidence; distinct green test plus byte-truthfully changed subset of the named ten-path dataflow allowlist; fresh green passing Tester/approved Reviewer evidence; Phase 4.5 then independent classification. |
| Out-of-Scope | production source, Protocol/API, concrete Registry/Retention, mapper/ACL, every other BC, backend/DI/lifecycle, README/public-surface, version/release/tag/merge/post-merge, and every PR reply/resolution. |
| ReadOnly | `README.md`, all public surfaces, all source outside the named test, architecture authority, C15/C16 artifacts/evidence, and all non-C17 threads. `4078761998` is Human-only `human-check`. |
| Written | future SHA-bound Plan-Reviewer receipt, RED/green Tester evidence, and green Reviewer evidence only; designated writer creates it and Implementer commits unchanged alone. |
| Modify | candidate: exactly five planning artifacts; RED: only `tests/test_loaded_runtime_cache_bc_independence.py`; green: that test plus only actual byte-changed files from the named dataflow allowlist. |
| Deleted | none. |

### Locked decisions / Python implementation metadata

- **Async-planning status:** exempt — static AST regression and static dataflow generation have no async boundary,
  lifecycle, concurrency, cancellation, timeout, or external runtime-I/O decision.
- **Module placement / API / interface / breaking / dependencies:** named test plus named dataflow allowlist / no / no
  / no / no.
- **Error and typing:** RED's failed assertion is factual evidence; preserve Python 3.12 `ast` static analysis with
  no `Any`, runtime access, dynamic import, AST evaluation, or source workaround.
- Recognise only `getattr(<known importlib|sys alias>, <literal import_module|modules>)` assignment aliases; a later
  local alias use is rejected. Do not evaluate arbitrary expressions or recursive-destructure targets.
- Dataflow labels must say `RuntimeRegistry.lookup(key: RuntimeReuseKey) -> RuntimeT | None`. Never draw
  `Available`/`Missing` as lookup returns, a mapper, or an implemented backend/lifecycle/ACL.
- C15/C16 are frozen input. No future C17 SHA, evidence/result, classification, reply, resolution or approval is
  prefilled.

### Status / allowed transitions

**Historical C17 state:** `c17-phase-4.5-aligned / independent-classification-pending`. The committed C17 chain is candidate
`dc55f1a6a32ceabf48490e952af2b9fd71b9efd3` → approved Plan-Reviewer receipt-only commit
`35ccbd6` → collection-success/assertion-failing RED subject `7ec3b57` → failing Tester-evidence-only commit
`3c9c9b8` → green test/dataflow subject `708091b` → delivery-receipt-only commit `7ceb340` → passing
Tester-evidence-only commit `b58cb1` → approved Independent Reviewer evidence-only commit
`edbae51`. This is Human-authorized post-receipt state tracking only. C18 supersedes its pending classification
routing; C17 creates no additional candidate, receipt, Tester/Reviewer evidence, PR reply, or thread resolution.
`4078761998`, ACL, and business-architecture boundaries remain Human-only/open. Any path
violation, malformed evidence, non-zero/skipped Archify result, or `needs-rework` fails closed and cannot authorize
a reply/resolution.

### Artifact paths / execution steps

| Artifact | Exact path | Write owner | Contract |
| --- | --- | --- |
| Candidate | `analysis/loaded-runtime-cache/requirements.md`; `analysis/loaded-runtime-cache/technical-spec.md`; `plan/loaded-runtime-cache/loaded-runtime-cache.plan.md`; `plan/loaded-runtime-cache/loaded-runtime-cache.spec.md`; `plan/loaded-runtime-cache/loaded-runtime-cache.step.md` | Plan-Creator | Exactly these five paths. |
| Receipt | `plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<c17-candidate-40-hex-sha>.json` | Independent Plan-Reviewer / Implementer | Fresh approved receipt, then unchanged sole commit. |
| RED/green test | `tests/test_loaded_runtime_cache_bc_independence.py` | Implementer | RED only test; green test plus truthful dataflow subset. |
| Tester/review evidence | `plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<subject-40-hex-sha>.json`; `plan/loaded-runtime-cache/loaded-runtime-cache.implementation-review-log-<green-subject-40-hex-sha>.json` | Tester / Independent Reviewer / Implementer | Existing exact schema, full SHA bindings and separate sole commits. |
| Dataflow allowlist | `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.json`; `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.html`; `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.validation.json`; `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.delivery.json`; `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.json`; `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.html`; `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.1440x900.dark.png`; `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.1440x900.light.png`; `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.2048x1320.dark.png`; `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.2048x1320.light.png` | Implementer | validate → deliver → visual-check; green only includes byte-changed outputs. |

1. Commit only the candidate; write/commit an approved SHA-bound receipt unchanged alone.
2. Create the test-only RED for the prescribed `getattr` bypass; record/commit factual failing evidence alone.
3. Create a distinct green scanner repair, regenerate the allowlisted dataflow as validate → deliver → visual-check,
   and include only byte-changed output files.
4. Commit matching passing Tester evidence, then matching approved Independent Reviewer evidence, each unchanged alone.
5. Planner performs Phase 4.5; a new Independent Reviewer classification alone decides a reply/resolve for either
   C17 pair. README/public-surface, ACL and business-architecture threads stay Human-only/open.

### Validation / reviewer handoff / release

- RED collects and fails; green rejects local aliases derived from known `importlib`/`sys` aliases with literal
  `import_module`/`modules`, preserving prior direct/chained/mixed regression tests.
- The diagram has the exact `lookup` union return; validate is 9/9, zero errors/warnings; deliver succeeds; visual
  check is not skipped and contains 1440×900, 1600×1000, 1920×1080, 2048×1320 facts. `README.md` stays unmodified.
- Plan-Reviewer checks candidate scope/no future facts; Independent Reviewer checks same-subject passing evidence,
  test/dataflow boundaries and factual Archify receipts. Neither replies, resolves, approves PRs or merges.
- No release action; Human alone owns merge/release/post-merge.

## C18 C17 Current-Head Classification Successor (authoritative current routing)

C18 only classifies an immutable current-head snapshot. It preserves the Loaded Runtime Cache mission, C17 chain and
all locked boundaries. It creates no RED/green/code/docs/Archify/README work; every unlisted path is ReadOnly.

| Field | Contract |
| --- | --- |
| In-Scope | Exactly five C18 planning artifacts; a standard candidate-SHA-bound Plan-Reviewer receipt; one immutable C17-bound classification receipt; later exact reply/resolve only where its committed entry is `REPLY_AND_RESOLVE`. |
| Out-Of-Scope | Implementation, tests, source, dataflow, architecture, README, lifecycle, new evidence chain, release, merge and post-merge. |
| ReadOnly | All unlisted paths, C17/C16 and predecessor evidence, every thread unless its C18 committed receipt entry permits reply/resolve. |
| Written | Standard C18 Plan-Reviewer receipt; then only the one C17-bound classification receipt. |
| Modified | Candidate: only the five planning artifacts. Classification receipt: one new evidence file only. |
| Deleted | None. |

### C18 immutable receipt contract

The candidate is planning-only and cannot prefill candidate SHA, receipt verdict, classification result, reply or
resolution. After it is committed, Independent Plan-Reviewer writes a standard approved receipt at
`plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<planning-candidate-40-hex-sha>.json`; only
Implementer may commit it unchanged alone. That receipt authorizes classification only.

Independent Reviewer alone writes
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-7ceb3409d6d8b9ff3dc51485c3588f502bdff882.json`.
Only Implementer may commit it unchanged in a sole evidence-only commit. Its top-level keys are exactly
`schema_version`, `topic`, `implementation_subject_commit`, `tester_evidence_commit`,
`implementation_review_evidence_commit`, `pr_head_commit`, `classifications`, `recorded_by`; its immutable values
bind subject `7ceb3409d6d8b9ff3dc51485c3588f502bdff882`, passing Tester commit
`b58cb1e330fe12ccc80a8f39b875a61ea6024067`, approved Reviewer commit
`edbae51a0ee86cff498d6caf4e6aa78b58962a82`, PR head
`bf63a3c6a0533ad0f367305deff029eddc2b18be`, schema `1`, topic `loaded-runtime-cache`, and writer
`Independent Reviewer`.

`classifications` contains exactly eleven entries with only `thread`, `comment`, `outcome`, `reply` each. Exact pair
set: `PRRT_kwDOUJTij86jnBpk`/`4043480108`, `PRRT_kwDOUJTij86jqdPV`/`4044836129`,
`PRRT_kwDOUJTij86jqdPZ`/`4044836136`, `PRRT_kwDOUJTij86kOjjo`/`4059094458`,
`PRRT_kwDOUJTij86kQ95O`/`4060023123`, `PRRT_kwDOUJTij86kqiZu`/`4070096548`,
`PRRT_kwDOUJTij86kqiZ5`/`4070096561`, `PRRT_kwDOUJTij86lAR8J`/`4078761983`,
`PRRT_kwDOUJTij86lAR8P`/`4078761993`, `PRRT_kwDOUJTij86lAR8T`/`4078761998`,
`PRRT_kwDOUJTij86lAR8Y`/`4078762005`. F, ACL, business architecture and README are respectively the first, fifth,
seventh and tenth pair and are locked `HUMAN_CHECK` with JSON `null` reply. The committed receipt classifies each
of the other seven as `REPLY_AND_RESOLVE` with its exact non-empty factual reply.

`REPLY_AND_RESOLVE` needs a non-empty factual reply and is the only classification that lets Implementer reply and
resolve the exact pair. `ADDRESS` and `HUMAN_CHECK` require `null`; `ADDRESS` returns to Planner, while
`HUMAN_CHECK` remains open. Any schema/path/SHA/ancestor/sole-commit/pair/nullability defect fails closed.

### C18 status / transition / handoff

The committed C18 evidence chain is candidate
`f4f27899eb34976776d4cd6baeb4fd971715edd3` → approved Plan-Reviewer receipt-only commit
`4cd60b2794493b54c8cb9b5b1b4b48b2c04261a0` → independent classification-receipt-only commit
`a4054d23823dd446a0d5ee6ad1cd52ac8430c80c`.

Current state is `c18-exact-reply-resolve-pending`. The seven committed `REPLY_AND_RESOLVE` pairs are
`PRRT_kwDOUJTij86jqdPV`/`4044836129`, `PRRT_kwDOUJTij86jqdPZ`/`4044836136`,
`PRRT_kwDOUJTij86kOjjo`/`4059094458`, `PRRT_kwDOUJTij86kqiZu`/`4070096548`,
`PRRT_kwDOUJTij86lAR8J`/`4078761983`, `PRRT_kwDOUJTij86lAR8P`/`4078761993`, and
`PRRT_kwDOUJTij86lAR8Y`/`4078762005`; only these exact receipt replies/resolutions are pending.

`PRRT_kwDOUJTij86jnBpk`/`4043480108`, `PRRT_kwDOUJTij86kQ95O`/`4060023123`,
`PRRT_kwDOUJTij86kqiZ5`/`4070096561`, and `PRRT_kwDOUJTij86lAR8T`/`4078761998` remain
`HUMAN_CHECK`, open, and without reply/resolution authority. New open threads `PRRT_kwDOUJTij86lCkFr` and
`PRRT_kwDOUJTij86lCkFu` are outside the immutable C18 receipt and remain unclassified; no action is authorized
for either.

This is Human-authorized post-receipt state tracking only. It creates no C19, candidate, receipt, new evidence,
actual reply, resolution, merge, release, post-merge, Human review, or action for an unclassified thread.

## C19 Current-Head Reconciliation Classification Successor (authoritative current routing)

C19 supersedes C18 only for fresh current-head classification. It preserves the Loaded Runtime Cache mission, C17/C18
provenance and all locked boundaries; it creates no code, test, dataflow, architecture, README or direct PR action
until an exact committed receipt authorizes it.

| Field | Contract |
| --- | --- |
| In-Scope | Exactly five C19 planning artifacts; standard candidate-SHA-bound Plan-Reviewer receipt; one immutable C17-bound current-head classification/reconciliation receipt; later exact reply/resolve only for its committed `REPLY_AND_RESOLVE` entry. |
| Out-Of-Scope | Implementation, source, tests, dataflow, architecture, README, lifecycle, new C17 evidence, release, merge and post-merge. |
| ReadOnly | All unlisted paths; C17/C18 and predecessor artifacts; every thread outside an exact C19 committed `REPLY_AND_RESOLVE` entry. |
| Written | Standard C19 Plan-Reviewer receipt, then one C19 classification receipt. |
| Modified | Candidate: only the five planning artifacts. Classification: only one new receipt file. |
| Deleted | None. |

### C19 immutable receipt contract

The candidate must not prefill its SHA, review verdict, classification outcome, reply or resolution. After a committed
approved standard Plan-Reviewer receipt, Independent Reviewer alone writes
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-7ceb3409d6d8b9ff3dc51485c3588f502bdff882-3e803a507b2dfa74efdf71164c260da172aadb81.json`; Implementer alone commits it unchanged in a
sole evidence-only commit. The eight exact top-level keys are `schema_version`, `topic`,
`implementation_subject_commit`, `tester_evidence_commit`, `implementation_review_evidence_commit`,
`pr_head_commit`, `classifications`, `recorded_by`, binding schema `1`, topic `loaded-runtime-cache`, C17 subject
`7ceb3409d6d8b9ff3dc51485c3588f502bdff882`, Tester commit `b58cb1e330fe12ccc80a8f39b875a61ea6024067`, Reviewer
commit `edbae51a0ee86cff498d6caf4e6aa78b58962a82`, and current PR head
`3e803a507b2dfa74efdf71164c260da172aadb81`.

`classifications` contains exactly five entries with only `thread`, `comment`, `outcome`, `reply`: new pairs
`PRRT_kwDOUJTij86lCkFr`/`4079664571`, `PRRT_kwDOUJTij86lCkFu`/`4079664575`,
`PRRT_kwDOUJTij86lDH2-`/`4079885261`, `PRRT_kwDOUJTij86lDH3C`/`4079885267`, and reconciliation pair
`PRRT_kwDOUJTij86lAR8Y`/`4078762005`. The future Independent Reviewer alone determines all first-four
outcomes/replies. For `lAR8Y`, it first verifies current GitHub state and may record `ALREADY_RESOLVED` with `null`
only if it evidences existing resolution; otherwise it independently classifies the pair. General outcomes are
`REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK`; `ALREADY_RESOLVED` is exclusive to `lAR8Y`. Only
`REPLY_AND_RESOLVE` has a non-empty factual reply and authorizes an exact reply/resolution; all other outcomes use
`null`, while `ADDRESS` returns to Planner and Human checks stay open.

F `PRRT_kwDOUJTij86jnBpk`/`4043480108`, ACL `PRRT_kwDOUJTij86kQ95O`/`4060023123`, business
`PRRT_kwDOUJTij86kqiZ5`/`4070096561`, and README `PRRT_kwDOUJTij86lAR8T`/`4078761998` remain excluded
Human-only locks: they are not C19 receipt entries and must not be replied to or resolved. Any malformed keys,
role/path/SHA/head/ancestor/sole-commit defect, incorrect pair count, invalid enum, or invalid reply nullability
fails closed.

### C19 transition / handoff

`planned` → C19 candidate-only commit → independent approved Plan-Reviewer receipt-only commit → independent C19
classification receipt-only commit → Planner classification routing. The receipt alone may route exact
`REPLY_AND_RESOLVE` entries to Implementer; it never approves PR, merge, release or post-merge.

## C20 C19 ADDRESS Remediation Successor (authoritative current routing)

C20 supersedes C19 only for remediation of its two `ADDRESS` entries. It preserves the Loaded Runtime Cache mission,
protocol-first boundary and all prior evidence as frozen provenance.

| Field | Contract |
| --- | --- |
| Goal | Resolve the two C19 findings without changing identity ownership, runtime lifecycle, public API, or PR authority. |
| In-Scope | A foreign `ModelIdentity` `ImportFrom`-alias static scanner regression; distinct expected lookup-failure signal in the topic dataflow; C20 candidate/receipt/RED/green/Tester/Reviewer/one two-pair classification chain. |
| Out-Of-Scope | Mapper, source protocol change, concrete registry/backend, lifecycle, Identity BC change, new semantic type, README, root export, merge, release, post-merge and Human review. |
| ReadOnly | Every unlisted path, all prior C17–C19 records, all production source, README/public surfaces, architecture index, threads outside C20's two pairs, and all existing Human-only locks. |
| Written | Standard C20 Plan-Reviewer receipt; red Tester evidence; green Tester evidence; green independent Reviewer evidence; one C20 classification receipt. |
| Modified | Candidate: exactly five planning artifacts. RED: exactly `tests/test_loaded_runtime_cache_bc_independence.py`. Green: that test plus only byte-truthfully changed members of the ten named dataflow outputs. |
| Deleted | None. |

### C20 locked implementation contract

`PRRT_kwDOUJTij86lCkFu` / `4079664575` is resolved only by presenting
`RuntimeRegistryLookupUnavailable` as a separate expected Registry lookup-failure signal alongside—not inside or
translated from—the normal `RuntimeRegistry.lookup(key: RuntimeReuseKey) -> RuntimeT | None` contract. No mapper to
`Available`、`Missing`、`Unavailable` or another outcome is permitted.

`PRRT_kwDOUJTij86lDH2-` / `4079885261` is resolved only by a pure-AST test/scanner regression that rejects the
foreign semantic `ImportFrom` shape `from deterministic_response_cache.identity.contracts import ModelIdentity as
LocalModelIdentity`. The check must treat the imported symbol's source semantic name as authoritative even when a
local alias changes its binding name. It must not evaluate source, dynamically import, inspect module state, or expand
the rule to unrelated imports.

The exact dataflow allowlist is the ten paths named in the C20 technical specification. Their JSON/HTML/receipt/image
bytes must arise from validate → deliver → visual-check in order. `validate` must be showcase 9/9 with zero errors and
warnings; visual-check must be non-skipped and cover all four desktop viewports. Exact output may be included only
when changed by the corresponding command; otherwise it stays ReadOnly.

### C20 evidence and classification contract

The route is: five-artifact candidate-only commit → independent approved standard Plan-Reviewer receipt-only commit
→ test-only collection-success/assertion-failing RED subject → factual failing Tester evidence-only commit → distinct
green subject → factual passing Tester evidence-only commit → approved independent Reviewer evidence-only commit →
Planner Phase 4.5 → independent C20 classification receipt-only commit. C20 candidate planning pre-fills none of the
candidate SHA, verdicts, subject SHA, evidence result, PR head, classification outcome, reply or resolution.

The final receipt path is
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-<c20-green-subject-40-hex-sha>.json`.
Independent Reviewer is its only writer; Implementer is its only committer, unchanged and alone. It has the exact
eight top-level keys and exact two entries specified in the technical specification. `REPLY_AND_RESOLVE` is the only
actionable outcome and requires an exact non-empty factual reply; `ADDRESS` and `HUMAN_CHECK` use `null`, return to
Planner or remain open, respectively. No other thread is authorized by C20.

### C20 committed post-review state

The complete committed C20 chain is: planning candidate
`77835c29b90304cff9b0c3193bde4c297ec96612` → approved Plan-Reviewer receipt
`8a31db2d9ccccaf46363d714be457a0cd4700a3e` → RED subject
`f87bb1a9580a08196989374e069a82cccafd6c72` → failing Tester evidence
`55e91c9ff3a785af3279d8ebd9e3dfd3d69bc2a3` → green subject
`fa1468301af1906a05ee31ba0d267d2270d7af5f` → passing Tester evidence
`6423f55b6dbcde5bee190ef86dc8c31f5c27c94e` → approved independent Reviewer evidence
`3d0dc9fbb0e9da6d742ac20856b8aac6b0a3035e`.

This is factual post-review state only. C20 is `phase-4.5-alignment-pending`: Planner must first verify that the
actual PR head includes this committed chain and perform Phase 4.5 alignment. Only then may an Independent Reviewer
write the already-defined C20 green-subject-bound, exact-two-pair classification receipt for
`lCkFu`/`4079664575` and `lDH2-`/`4079885261`; Implementer may commit that receipt unchanged and alone. This
state alignment creates no C21, no contract change, and no authorization to reply to or resolve a thread.

## C21 C20 Current-Head Single-Pair Classification Successor (authoritative current routing)

C21 supersedes C20 only for a fresh, immutable classification of
`PRRT_kwDOUJTij86ldYVf`/`4090457782`. It preserves the Loaded Runtime Cache mission, protocol-first boundary,
completed C20 chain, all predecessor provenance and all Human-only locks.

| Field | Contract |
| --- | --- |
| Goal | Independently classify exactly one previously unclassified current-head thread, without changing product behavior or PR authority before a committed exact receipt permits it. |
| In-Scope | Exactly five C21 planning artifacts; standard candidate-SHA-bound Plan-Reviewer receipt; one C20-subject/current-head-bound immutable classification receipt; later exact reply/resolve only if its committed entry is `REPLY_AND_RESOLVE`. |
| Out-Of-Scope | Implementation, source, tests, dataflow, architecture, README, lifecycle, new C20 evidence, release, merge, post-merge and Human review. |
| ReadOnly | Every unlisted path; C20 and predecessor records; every thread except the one exact C21 receipt entry; all existing Human-only locks. |
| Written | Standard C21 Plan-Reviewer receipt, then one C21 classification receipt. |
| Modified | Candidate: exactly the five planning artifacts. Classification: one new receipt file only. |
| Deleted | None. |

### C21 immutable receipt contract

Candidate planning cannot prefill its SHA, review verdict, classification outcome, reply or resolution. After a
committed approved standard Plan-Reviewer receipt, Independent Reviewer alone writes
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-fa1468301af1906a05ee31ba0d267d2270d7af5f-a1aae44897c0f0b0ac52f1ca1697554c2f79cdb5.json`.
Implementer alone commits it unchanged in a sole evidence-only commit. The exact eight top-level keys are
`schema_version`, `topic`, `implementation_subject_commit`, `tester_evidence_commit`,
`implementation_review_evidence_commit`, `pr_head_commit`, `classifications`, `recorded_by`; they bind schema `1`,
topic `loaded-runtime-cache`, C20 subject `fa1468301af1906a05ee31ba0d267d2270d7af5f`, Tester-evidence commit
`6423f55b6dbcde5bee190ef86dc8c31f5c27c94e`, Reviewer-evidence commit
`3d0dc9fbb0e9da6d742ac20856b8aac6b0a3035e`, and PR head
`a1aae44897c0f0b0ac52f1ca1697554c2f79cdb5`.

`classifications` contains exactly one entry with only `thread`, `comment`, `outcome`, `reply`, for
`PRRT_kwDOUJTij86ldYVf`/`4090457782`. Independent Reviewer alone determines
`REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK`; candidate planning supplies neither outcome nor reply.
`REPLY_AND_RESOLVE` requires a non-empty factual reply and is the only outcome that permits Implementer to reply and
resolve this exact pair. `ADDRESS` and `HUMAN_CHECK` require JSON `null`; `ADDRESS` returns to Planner and
`HUMAN_CHECK` remains open. All other threads and Human-only locks are excluded. Any key, role, path, SHA, ancestor,
sole-commit, pair-count, enum or nullability defect fails closed.

### C21 transition / handoff

`planned` → C21 candidate-only commit → independent approved Plan-Reviewer receipt-only commit → independent C21
classification receipt-only commit → Planner classification routing. This receipt may route only its exact committed
`REPLY_AND_RESOLVE` entry to Implementer; it never approves PR, merge, release or post-merge.

## C22 C20 Current-Head Dual-Pair Classification Successor (authoritative current routing)

C22 supersedes C21 only for a fresh, immutable classification of
`PRRT_kwDOUJTij86ldeVI`/`4090495760` and `PRRT_kwDOUJTij86ldeVO`/`4090495770`. It preserves the Loaded Runtime Cache
mission, protocol-first boundary, completed C20 chain, all predecessor provenance and all Human-only locks.

| Field | Contract |
| --- | --- |
| Goal | Independently classify exactly two previously unclassified current-head threads, without changing product behavior or PR authority before a committed exact receipt permits it. |
| In-Scope | Exactly five C22 planning artifacts; standard candidate-SHA-bound Plan-Reviewer receipt; one C20-subject/current-head-bound immutable two-pair classification receipt; later exact reply/resolve only if its committed entry is `REPLY_AND_RESOLVE`. |
| Out-Of-Scope | Implementation, source, tests, dataflow, architecture, README, lifecycle, new C20 evidence, release, merge, post-merge and Human review. |
| ReadOnly | Every unlisted path; C20/C21 and predecessor records; every thread except the two exact C22 receipt entries; all existing Human-only locks and new `PRRT_kwDOUJTij86ld9Ai`. |
| Written | Standard C22 Plan-Reviewer receipt, then one C22 classification receipt. |
| Modified | Candidate: exactly the five planning artifacts. Classification: one new receipt file only. |
| Deleted | None. |

### C22 immutable receipt contract

Candidate planning cannot prefill its SHA, review verdict, classification outcome, reply or resolution. After a
committed approved standard Plan-Reviewer receipt, Independent Reviewer alone writes
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-fa1468301af1906a05ee31ba0d267d2270d7af5f-0991c56ec7e562ea512449bda1a41118dbc48203.json`.
Implementer alone commits it unchanged in a sole evidence-only commit. The exact eight top-level keys are
`schema_version`, `topic`, `implementation_subject_commit`, `tester_evidence_commit`,
`implementation_review_evidence_commit`, `pr_head_commit`, `classifications`, `recorded_by`; they bind schema `1`,
topic `loaded-runtime-cache`, C20 subject `fa1468301af1906a05ee31ba0d267d2270d7af5f`, Tester-evidence commit
`6423f55b6dbcde5bee190ef86dc8c31f5c27c94e`, Reviewer-evidence commit
`3d0dc9fbb0e9da6d742ac20856b8aac6b0a3035e`, and PR head
`0991c56ec7e562ea512449bda1a41118dbc48203`.

`classifications` contains exactly two entries with only `thread`, `comment`, `outcome`, `reply`, for
`PRRT_kwDOUJTij86ldeVI`/`4090495760` and `PRRT_kwDOUJTij86ldeVO`/`4090495770`. Independent Reviewer alone determines
`REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK`; candidate planning supplies neither outcome nor reply.
`REPLY_AND_RESOLVE` requires a non-empty factual reply and is the only outcome that permits Implementer to reply and
resolve the matching exact pair. `ADDRESS` and `HUMAN_CHECK` require JSON `null`; `ADDRESS` returns to Planner and
`HUMAN_CHECK` remains open. F `PRRT_kwDOUJTij86jnBpk`/`4043480108`, ACL
`PRRT_kwDOUJTij86kQ95O`/`4060023123`, business `PRRT_kwDOUJTij86kqiZ5`/`4070096561`, and README
`PRRT_kwDOUJTij86lAR8T`/`4078761998` remain excluded Human-only locks. New `PRRT_kwDOUJTij86ld9Ai` is likewise
excluded, remains open and is not action-authorized. Any key, role, path, SHA, ancestor, sole-commit, pair-count,
enum or nullability defect fails closed.

### C22 transition / handoff

`planned` → C22 candidate-only commit → independent approved Plan-Reviewer receipt-only commit → independent C22
classification receipt-only commit → Planner classification routing. This receipt may route only its exact committed
`REPLY_AND_RESOLVE` entries to Implementer; it never approves PR, merge, release or post-merge.

## C23 C22 ADDRESS Remediation Successor (authoritative current routing)

C23 is the sole bounded successor for C22 ADDRESS pairs `PRRT_kwDOUJTij86ldeVI`/`4090495760` and
`PRRT_kwDOUJTij86ldeVO`/`4090495770`. It consumes only C22 classification receipt commit
`a9065a8332119930347214f07f2980d655d8d314` at
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-fa1468301af1906a05ee31ba0d267d2270d7af5f-0991c56ec7e562ea512449bda1a41118dbc48203.json`,
bound to C20 subject `fa1468301af1906a05ee31ba0d267d2270d7af5f`, passing Tester evidence
`6423f55b6dbcde5bee190ef86dc8c31f5c27c94e`, approved Reviewer evidence
`3d0dc9fbb0e9da6d742ac20856b8aac6b0a3035e`, and C22 PR head `0991c56ec7e562ea512449bda1a41118dbc48203`.
It preserves all prior immutable facts and cannot treat C22 planning, chat, branch or worktree state as a substitute
for its own committed evidence chain.

| Field | Contract |
| --- | --- |
| Goal | Correct only the two independently classified defects, then independently classify only those same two current-head pairs. |
| In-Scope | Five C23 planning artifacts; standard Plan-Reviewer receipt; RED/failing Tester; distinct green/passing Tester; independent green review; current-head two-pair classification; eventual exact reply/resolve only for committed `REPLY_AND_RESOLVE`. |
| Out-Of-Scope / Non-Goal | Production behavior beyond scanner/dataflow correction; mapper; outcome conversion; concrete backend; DI; runtime lifecycle; Model Execution; Provider Adapter; ACL; merge, release and post-merge. |
| ReadOnly | Every unlisted path and predecessor artifact; the four Human-only pairs F/ACL/business/README; `ld9Ai`/`4090688118`; every thread except the two C23 entries. |
| Written | Candidate planning artifacts; one standard Plan-Reviewer receipt; SHA-bound RED/green Tester evidence; green independent review evidence; one green-subject/current-head classification receipt. |
| Modified | RED: scanner test only. Green: scanner test plus dataflow JSON/HTML and only byte-truthfully changed pre-existing validation/delivery/visual-check evidence. |
| Deleted | None. |

### C23 locked remediation contract

The dataflow contract remains `RuntimeRegistry.lookup(key: RuntimeReuseKey) -> RuntimeT | None`; the sole permitted
expected-failure relationship is `RuntimeRegistry -> RuntimeRegistryLookupUnavailable`. There is no lookup edge to
`Available`, `Missing`, `Unavailable` or any mapper. The graph remains protocol-only and cannot imply a concrete
backend, DI, lifecycle, execution, provider or ACL.

The static scanner must reject `(load := importlib.import_module)(...)`. It parses only `ast.NamedExpr` direct
simple-name target/value; it must neither recurse through targets nor execute a fixture/dynamic import. Existing
mixed-assignment semantics are locked: `load = holder.loader = importlib.import_module` retains `load` and ignores
the attribute target.

Candidate → independent approved Plan-Reviewer receipt → receipt-only commit → collection-success/assertion-failing
RED → factual failing Tester evidence-only commit → distinct green → factual passing Tester evidence-only commit →
independent approved/needs-rework green review evidence-only commit is mandatory. Every candidate/evidence path is
fresh, SHA-bound and immutable; only its prescribed writer may write it and only Implementer may make its unchanged
sole commit. Any missing, stale, malformed, cross-subject or non-sole record fails closed.

After Planner verifies an approved green chain and actual current PR head, Independent Reviewer alone may write the
eight-key immutable classification receipt only at
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-<c23-green-subject-40-hex-sha>-<current-pr-head-40-hex-sha>.json`;
Implementer alone may unchanged-sole-commit it. Its top-level keys are exactly `schema_version`, `topic`,
`implementation_subject_commit`, `tester_evidence_commit`, `implementation_review_evidence_commit`,
`pr_head_commit`, `classifications`, `recorded_by`, binding integer `1`, `loaded-runtime-cache`, the C23 green
subject, its passing Tester/review evidence commits, actual current PR head, exactly two entries, and `Independent
Reviewer`. Each entry has only `thread`, `comment`, `outcome`, `reply`, for exactly `ldeVI`/`4090495760` and
`ldeVO`/`4090495770`; `outcome` is only `REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK`. Only committed
`REPLY_AND_RESOLVE` with a non-empty factual reply permits Implementer to reply and resolve that exact pair;
`ADDRESS` and `HUMAN_CHECK` remain JSON `null`, returning to Planner/open respectively. F `jnBpk`/`4043480108`, ACL
`kQ95O`/`4060023123`, business `kqiZ5`/`4070096561`, README `lAR8T`/`4078761998`, and `ld9Ai`/`4090688118` are
excluded/open; the first four are Human-only locks.

## C24 C23 Current-Head Dual-Pair Classification Successor (authoritative current routing)

C24 supersedes C23 only for fresh classification of `PRRT_kwDOUJTij86lfQl9`/`4091213935` and
`PRRT_kwDOUJTij86lfQmF`/`4091213944`. It consumes immutable C23 subject
`240c694fa5078dc1d35f154f7a85b06381db2e47`, passing Tester evidence `dabce082058805281990c52b12352b87c2b46801`, approved
Reviewer evidence `489752c727aa86cfaf49038cc2ed6dfddf33ba2d`, C23 classification provenance and current PR head
`e5872d5dfb2018743b1f7e319551d52f25f5ef02`.

| Field | Contract |
| --- | --- |
| Goal | Independently classify only the two new current-head pairs, with no product or PR authority change before an exact committed receipt. |
| In-Scope | Exactly five planning artifacts; a standard candidate-SHA-bound Plan-Reviewer receipt; one fixed-subject/current-head-bound C24 classification receipt; later exact action only if classified `REPLY_AND_RESOLVE`. |
| Out-Of-Scope / Non-Goal | Implementation, source, tests, dataflow, docs/architecture, README, PR authority, Human review, merge, release and post-merge. |
| ReadOnly | Every unlisted path; C23 and predecessor evidence; C23 resolved pairs; F/ACL/business/README Human-only locks; `ld9Ai`; every thread except the two exact C24 entries. |
| Written | Standard C24 Plan-Reviewer receipt, then one C24 classification receipt. |
| Modified | Candidate: exactly the five planning artifacts. Classification: one new receipt only. |
| Deleted | None. |

### C24 immutable receipt contract

Candidate planning pre-fills neither candidate SHA, review verdict, classification outcome, reply nor resolution. After a
committed approved standard Plan-Reviewer receipt, Independent Reviewer alone writes
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-240c694fa5078dc1d35f154f7a85b06381db2e47-e5872d5dfb2018743b1f7e319551d52f25f5ef02.json`; Implementer alone commits it unchanged in a sole evidence-only commit.
Its exact eight top-level keys are `schema_version`, `topic`, `implementation_subject_commit`, `tester_evidence_commit`,
`implementation_review_evidence_commit`, `pr_head_commit`, `classifications`, `recorded_by`, binding `1`,
`loaded-runtime-cache`, the fixed C23 subject/Tester/Reviewer/head facts, exactly two entries and `Independent Reviewer`.
Entries have exactly `thread`, `comment`, `outcome`, `reply` for only `lfQl9`/`4091213935` and `lfQmF`/`4091213944`.
Reviewer independently selects `REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK`; only exact committed
`REPLY_AND_RESOLVE` with a non-empty factual reply permits the corresponding reply/resolve. `ADDRESS` and `HUMAN_CHECK`
require JSON `null` and return to Planner/open state. Any binding, schema, writer, pair, enum, nullability or sole-commit
defect fails closed.

### C24 transition / handoff

`planned` → C24 candidate-only commit → independent approved Plan-Reviewer receipt-only commit → independent C24
classification receipt-only commit → Planner routing. This never approves a PR, merge, release or post-merge.

## C25 lfQl9 Static Attribute-base NamedExpr Remediation Successor (authoritative current routing)

C25 is the only bounded successor for C24 `ADDRESS` pair `PRRT_kwDOUJTij86lfQl9`/`4091213935`. It preserves the
Loaded Runtime Cache mission, protocol-first boundary and all predecessor provenance. It neither reopens C24 nor
authorizes action on `lfQmF` or any other thread.

| Field | Contract |
| --- | --- |
| Goal | Statically reject `(loader := importlib).import_module(...)` without expanding the scanner or any BC boundary. |
| In-Scope | Exactly five C25 planning artifacts; standard candidate-SHA-bound Plan-Reviewer receipt; RED/failing Tester; distinct green/passing Tester; independent green review; one actual-current-head one-pair classification chain for `lfQl9` only. |
| Out-Of-Scope / Non-Goal | Production behavior; docs/dataflow; recursive parsing; execution; dynamic import; runtime introspection; direct-name NamedExpr, mixed assignment, `getattr`, `sys.modules`; PR reply/resolution before classification; merge, release and post-merge. |
| ReadOnly | Every unlisted path; all predecessor artifacts/evidence; production source; docs/dataflow; `lfQmF`/`4091213944`; F/ACL/business/README Human-only locks; `ld9Ai`; all other threads. |
| Written | Standard C25 Plan-Reviewer receipt; SHA-bound RED/green Tester evidence; green independent review evidence; one C25 green-subject/current-head classification receipt. |
| Modified | Candidate: exactly five planning artifacts. RED and green: only `tests/test_loaded_runtime_cache_bc_independence.py`. |
| Deleted | None. |

### C25 locked remediation contract

The sole scanner repair recognises a direct `ast.Attribute` with an `ast.NamedExpr` base only where the NamedExpr has a
direct `ast.Name` target, its value resolves to a known `importlib` module alias, and the attribute is
`import_module`. It catches `(loader := importlib).import_module(...)` using static syntax only. It must not recurse
through NamedExpr targets or expressions, execute any fixture/AST, dynamically import or introspect runtime modules.
The direct-name NamedExpr path and existing mixed-assignment rule (retain direct simple-name targets, ignore attribute
targets) remain unchanged, as do `getattr` and `sys.modules` handling.

Candidate → independent approved Plan-Reviewer receipt → receipt-only commit → collection-success/assertion-failing
RED subject → factual failing Tester evidence-only commit → distinct green subject → factual passing Tester
evidence-only commit → independent approved green review evidence-only commit → Planner actual-current-head verification
→ one-pair independent classification receipt-only commit is mandatory. All candidate/evidence paths are fresh,
immutable and SHA-bound; C25 planning pre-fills no SHA, verdict, outcome, reply or resolution.

After Planner's actual-head verification, Independent Reviewer alone may write
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-<c25-green-subject-40-hex-sha>-<actual-current-pr-head-40-hex-sha>.json`.
Implementer alone may unchanged-sole-commit it. Its exact eight top-level keys are `schema_version`, `topic`,
`implementation_subject_commit`, `tester_evidence_commit`, `implementation_review_evidence_commit`, `pr_head_commit`,
`classifications`, `recorded_by`; it contains exactly one `thread`, `comment`, `outcome`, `reply` entry for
`lfQl9`/`4091213935`. Reviewer independently selects `REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK`; only an exact committed
`REPLY_AND_RESOLVE` with non-empty factual reply can authorize later action. All other results remain Planner/open
paths. Any binding, schema, writer, pair, enum, nullability or sole-commit defect fails closed.

### C25 transition / handoff

`planned` → C25 candidate-only commit → independent approved Plan-Reviewer receipt-only commit → RED/failing evidence
→ green/passing evidence → independent approved review evidence → Planner actual-head verification → independent C25
classification receipt-only commit → Planner routing. C25 does not itself reply, resolve, approve, merge, release or
post-merge.

## C26 Current-Head Seven-Pair Classification Successor (authoritative current routing)

C26 supersedes C25 only for a fresh, independent classification of the exact seven current-head pairs below. It
preserves the Loaded Runtime Cache mission, protocol-first boundary, C25 evidence and every locked decision. It creates
no code, test, documentation, dataflow, architecture, reply or resolution until its exact committed receipt authorizes
later routing.

| Field | Contract |
| --- | --- |
| Goal | Independently classify exactly seven new/open current-head pairs without changing product behavior or PR authority before a committed exact receipt. |
| In-Scope | Exactly five C26 planning artifacts; standard candidate-SHA-bound Plan-Reviewer receipt; one C25-subject/current-head-bound immutable seven-pair classification receipt; later exact action only for a committed `REPLY_AND_RESOLVE` entry. |
| Out-Of-Scope / Non-Goal | Implementation, source, tests, docs, dataflow, architecture, README, lifecycle, PR approval, Human review, merge, release and post-merge. |
| ReadOnly | Every unlisted path; C25 and predecessor artifacts; C25 `lfQl9`; all threads other than the exact seven receipt entries; Human-only `jnBpk`, `kQ95O`, `kqiZ5`, `lAR8T`, `lfQmF`. |
| Written | Standard C26 Plan-Reviewer receipt, then one C26 classification receipt. |
| Modified | Candidate: exactly the five planning artifacts. Classification: one new receipt only. |
| Deleted | None. |

### C26 immutable receipt contract

Candidate planning pre-fills neither candidate SHA, review verdict, classification outcome, reply nor resolution. After a
committed approved standard Plan-Reviewer receipt, Independent Reviewer alone writes
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-13f987a41119590621671c429293cf549055672b-8bd9460950237c48c9befb73a1c5b80d084e88ae.json`; Implementer alone commits it unchanged in a sole evidence-only commit.
Its exact eight top-level keys are `schema_version`, `topic`, `implementation_subject_commit`, `tester_evidence_commit`,
`implementation_review_evidence_commit`, `pr_head_commit`, `classifications`, `recorded_by`, binding `1`,
`loaded-runtime-cache`, C25 subject `13f987a41119590621671c429293cf549055672b`, Tester evidence
`e85f936505a323e6c84c02e90f4c4114e39b6505`, Reviewer evidence
`24d5141332cbc4dcf7a87dea7f134207a16ab37e`, current-head base
`8bd9460950237c48c9befb73a1c5b80d084e88ae`, exactly seven entries and `Independent Reviewer`.

Each entry has exactly `thread`, `comment`, `outcome`, `reply`; its pair set is exactly
`ld9Ai`/`4090688118`, `lfYsF`/`4091265104`, `lfYsH`/`4091265108`, `lfYsK`/`4091265115`, `m8u00`/`4129370918`,
`m8u04`/`4129370926`, `m8u09`/`4129370931`. Reviewer independently selects
`REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK`. Only exact committed `REPLY_AND_RESOLVE` with a non-empty factual reply may
permit the matching reply/resolve. `ADDRESS` and `HUMAN_CHECK` require JSON `null` and return to Planner/open state.
Any binding, schema, writer, pair, enum, nullability, staleness or sole-commit defect fails closed.

### C26 transition / handoff

`planned` → C26 candidate-only commit → independent approved Plan-Reviewer receipt-only commit → independent C26
classification receipt-only commit → Planner routing. This never approves a PR, merge, release or post-merge.

## C27 Bounded Architecture-Document Conflict-Resolution Successor (authoritative current routing)

C27 follows C26 committed classification receipt `31ab754aae443f702fa4ccc028d53a6c687e48aa` and is the sole route for the PR's five architecture-document
conflicts. It is a factual three-way integration, not an architecture redesign: it may use only merge-base facts at
`37d433e198a955f0710ecd5335666760aa86a20c`, Loaded Runtime Cache facts at
`442cc9461854d3909345edb26d1434bfaaa1b86e`, Model Execution facts at
`5f483a05e63c9dc8f3c63b04a63c8adec3ed2e28`, and dev-head facts at
`1501f380f20492c71275474f800fdaaffbf0a76a`.

| Field | Contract |
| --- | --- |
| Goal | Resolve only the five displayed architecture-document conflicts while retaining both already-committed capability facts. |
| In-Scope | Five C27 planning artifacts; standard candidate-SHA-bound Plan-Reviewer receipt; one immutable integration subject limited to the five conflict files; same-subject Tester evidence; independent Reviewer evidence; Planner Phase 4.5; existing draft PR push update. |
| Out-Of-Scope / Non-Goal | New architecture, contracts, BC wiring, Runtime Cache backend/lifecycle/mapper/Identity import, Model Execution provider behavior, source, tests, PR-thread action, PR approval, merge, release and post-merge. |
| ReadOnly | Every unlisted path; C26 and predecessor records; all classified and Human-only PR threads; Runtime Cache and Model Execution code/contracts outside the five documents. |
| Written | Standard C27 Plan-Reviewer receipt; after the five-file integration subject only, Tester writes `plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<c27-integration-subject-40-hex-sha>.json` bound to that full subject SHA; after its passing sole evidence-only commit, Independent Reviewer writes `plan/loaded-runtime-cache/loaded-runtime-cache.implementation-review-log-<c27-integration-subject-40-hex-sha>.json` bound to the same full subject SHA. Implementer alone commits each unchanged record in its own sole evidence-only commit. |
| Modified | Candidate: exactly the five planning artifacts. Integration subject: only `docs/architecture/business-capability/architecture-brief.md`, `docs/architecture/business-capability/index.html`, `docs/architecture/business-capability/scene.js`, `docs/business-capability-architecture.md`, and `docs/evolution-roadmap.md`. |
| Deleted | None. |

### C27 locked integration facts

The resolved documents must preserve Loaded Runtime Cache as protocol-only, with no direct Identity BC import, mapper,
concrete backend, or runtime lifecycle. They must preserve Model Execution as provider-neutral coordination contracts.
Their wiring is future work and must not be portrayed as present implementation. A conflict marker, dropped committed
fact, added decision, or an edit outside the exact five-file allowlist fails closed.

### C27 transition / handoff

`planned` → C27 candidate-only commit → Plan-Reviewer writes an independent approved candidate-SHA-bound receipt →
Implementer commits that receipt unchanged alone → five-file immutable integration subject → Tester writes factual
evidence at `loaded-runtime-cache.tester-evidence-<c27-integration-subject-40-hex-sha>.json` → Implementer commits
that same-subject evidence unchanged alone → Independent Reviewer writes review evidence at
`loaded-runtime-cache.implementation-review-log-<c27-integration-subject-40-hex-sha>.json` only after consuming the
committed same-subject passing evidence → Implementer commits that review unchanged alone → Planner Phase 4.5 → bounded
push updating the existing draft PR. C27 never authorizes thread reply/resolution, PR approval, merge, release, or
post-merge.

## C28 Post-C27 Eight-Pair Repair and Classification Successor (authoritative current routing)

C28 supersedes C27 only after its committed factual chain: repaired candidate
`2dac62be230fe3daf6c259389c93a6e29cfa7006` → integration subject
`21747f2a24dedc2d18eaf2fbd6c8bc0bb0670585` → passing Tester evidence
`294f7fb5ea0502236c277e545ba9e2dc311596e3` → approved Reviewer evidence
`190c41bb3480753f78bdf97c778583bee0f6ff2f`. C25 green and C26 receipt facts are frozen C28 inputs. C28 repairs and
later independently classifies exactly the four C26 `ADDRESS` pairs `lfYsH`/`4091265108`, `lfYsK`/`4091265115`,
`m8u04`/`4129370926`, `m8u09`/`4129370931`, plus unclassified `m82WL`/`4129419161`, `m82WS`/`4129419173`,
`m9eUV`/`4129677944`, `m9eUY`/`4129677947`. It makes no disposition or PR action before its own committed receipt.

| Field | Contract |
| --- | --- |
| Goal | Close the eight bounded non-Human review findings without changing the Loaded Runtime Cache mission, protocol-first boundary, or architecture decisions. |
| In-Scope | Five C28 planning artifacts; standard Plan-Reviewer receipt; RED/green test and bounded source/dataflow correction; SHA-bound Tester/Reviewer evidence; actual-current-head eight-pair classification receipt; later exact action only for committed `REPLY_AND_RESOLVE`. |
| Out-Of-Scope / Non-Goal | New BC wiring, backend, mapper, lifecycle, Identity import, execution, provider behavior, PR approval, merge, release and post-merge. |
| ReadOnly | Every unlisted path and thread; all predecessor artifacts; Human-only `jnBpk`, `kQ95O`, `kqiZ5`, `lAR8T`, `lfQmF`. |
| Written | Standard C28 Plan-Reviewer receipt; RED/green Tester evidence; green Independent Reviewer evidence; one C28 classification receipt. |
| Modified | Candidate: exactly the five planning artifacts. RED: only `tests/test_loaded_runtime_cache_bc_independence.py` and `tests/test_loaded_runtime_cache_contracts.py`. Green: those tests; `src/deterministic_response_cache/loaded_runtime_cache/runtime_reuse/registry/runtime_reuse_key.py`; and only the truthful byte-changed subset of the ten C14 dataflow paths already enumerated in `Artifact Paths` above. |
| Deleted | None. |

### C28 locked repair contract

The candidate aligns C25/C26/C27 tracking states solely from committed facts and predeclares no candidate SHA, receipt
verdict, subject SHA, result, PR head, classification outcome, reply or resolution. After its independently approved
receipt, RED must collect then factually fail for direct `getattr(importlib, "import_module")` callable use, direct
`getattr(sys, "modules")` module-cache access, `import importlib.<child>` top-level binding, a forbidden callable in
either `IfExp` assignment branch, and readable `RuntimeReuseKey` construction-token state. No RED Reviewer record exists.

Green preserves static AST-only analysis and all locked earlier shapes while recognising just those direct forms.
`RuntimeReuseKey` remains immutable with instance-identity semantics but must not expose its uninterpreted token through
a readable instance attribute. The dataflow's truthful changed subset must add `RuntimeRegistry.retain(key, runtime) ->
None` input/completion information separately from `RuntimeRetention` outcomes, without depicting a backend, mapper,
lifecycle, or cross-BC wiring. Validation/delivery/visual-check evidence must remain truthful; byte-identical artifacts
are ReadOnly.

### C28 immutable classification / handoff

**Historical C28 state:** `pr-open / exact eight-pair reply-and-resolve completed`。Planner 已依 committed approved review 完成 Phase 4.5 alignment。
已提交的 candidate `2de07fc0732f617fbbaccd67245fec3db883686a` → approved Plan-Reviewer receipt
`e3664935458a4c6b6a9db6a61f4287c16cc14703` → RED subject
`7de94edc65630f9b62815083cb0c0ddd501a8bca` → factual failing Tester evidence
`64068f0a566fd3bdaa7729dabec325c800fccd6a` 之後，green review rework 最終形成 immutable subject
`e4734aaa7d630542e13c37920593602fe8eb64cd` → passing Tester evidence-only commit
`b310dd12666aba754b55b0e1d6af5d9520696582` → approved Independent Reviewer evidence-only commit
`79b8095864ec8ed54db4ef107dbd06a33cdfab87`。bounded push 與 actual-current-PR-head
`d9d851df9d5a17503f5503bb8f400f7fbc3137f4` verification 已完成。Independent Reviewer 的 eight-pair
classification receipt 已原樣以 sole evidence-only commit `e41235af9eee729b151a06dfeaa36137c58e156b`
提交並推送；其 exact eight entries 全為 `REPLY_AND_RESOLVE`，Planner 已據此 routing。
receipt path 為
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-e4734aaa7d630542e13c37920593602fe8eb64cd-d9d851df9d5a17503f5503bb8f400f7fbc3137f4.json`。
`2d204b070cc9701cfdce31940cbfe377403f1894` 是 preceding tracking commit，並非 PR action evidence。其後 Implementer／Planner
live 核實八個 exact receipt reply 與 `isResolved: true`：`lfYsH`→`4140433910`、`lfYsK`→`4140435052`、
`m8u04`→`4140436064`、`m8u09`→`4140436858`、`m82WL`→`4140437667`、`m82WS`→`4140438539`、
`m9eUV`→`4140439397`、`m9eUY`→`4140440128`。C29 僅同步已核實 post-commit facts。

Candidate-only commit → independent approved SHA-bound Plan-Reviewer receipt-only commit → RED/failing Tester
evidence-only commit → distinct green/passing Tester evidence-only commit → independent approved green review
evidence-only commit → Planner actual-current-head verification → independent C28 classification receipt-only commit →
Planner routing. The final receipt path is
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-<c28-green-subject-40-hex-sha>-<actual-current-pr-head-40-hex-sha>.json`.
It has exactly `schema_version`, `topic`, `implementation_subject_commit`, `tester_evidence_commit`,
`implementation_review_evidence_commit`, `pr_head_commit`, `classifications`, `recorded_by`; its exactly eight entries
have only `thread`, `comment`, `outcome`, `reply` for the listed pair set. Independent Reviewer alone selects
`REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK`; only the former has a non-empty factual reply and can later authorize the
matching exact reply/resolve. All other replies are JSON `null`; malformed, stale, non-sole, cross-subject, wrong-head,
wrong-writer or wrong-pair evidence fails closed.

## C29 Three-File Architecture Conflict Integration Successor (authoritative current routing)

### Goal / Outcome and Scope

C29 承接 C28 completed eight-pair actions，解除 PR 與 dev 的三檔 architecture conflict。原 mission、Runtime reuse
protocol、outcomes、測試策略、Architecture Visualization、follow-up missions 延續既有定義。analysis strict mode 延續，
以下 contract 同步五份 artifacts。本次是 non-stable-library document integration；README／VERSION／release 不變。

| Field | Contract |
| --- | --- |
| Goal | 整合 dev 已提交 tree，三個衝突檔保留雙方 committed facts，更新 PR mergeability。 |
| In-Scope | 五份 planning artifacts、Plan-Reviewer receipt、完整 dev parent integration、三檔手動解衝、同 subject Tester／Reviewer evidence、Phase 4.5、bounded push、唯讀 PR audit。 |
| Out-Of-Scope / Non-Goal | 新架構決策、backend／DI／mapper／lifecycle／execution wiring、thread classification／reply／resolve、Human PR approval／merge、release／post-merge。 |
| ReadOnly | predecessor evidence；三檔之外禁止手動修改；五個 Human-only locks 與五個未分類 pairs 保持 open；dev worktree 不寫入。 |
| Written | 下列 immutable SHA-bound receipts，指定 writer 寫入、Implementer 各自 unchanged sole evidence-only commit。 |
| Modify | candidate 僅五份 artifacts；integration 手動解衝僅三檔，其他 dev tree 自動 parent integration；Phase 4.5 僅 plan／step factual alignment。 |
| Deleted | 無手動刪除；dev committed tree 的 automatic changes 屬 parent integration，不授權額外手動刪除。 |
| TestCase | parent topology、three-file manual-delta、no conflict markers、facts preservation、document/scene consistency、同 subject evidence schema／actor order、PR actual head／mergeability audit。 |

### Locked Decisions / Boundaries

來源固定 `dev@d6ff74ddf65c615f65eeba252e648784252a2bfd`，已整合 base
`1501f380f20492c71275474f800fdaaffbf0a76a`。first parent 是 integration 開始前實際已提交 feature HEAD，需記錄
完整 SHA；second parent 恰為上述 dev SHA。其他 dev committed changes 可由 merge 自動帶入，並非三檔 allowlist
違規；禁止對其手動修改。candidate／receipt／subject SHA、result／verdict 都不得預填。

三檔保留 feature committed Loaded Runtime Cache protocol-only、Model Execution provider-neutral coordination facts，
以及 dev committed Response Reuse fixed-codec／bytes-envelope facts；不重開 BC 獨立性、無 concrete runtime backend／DI／
mapper／lifecycle 與未實作 BC wiring 等邊界。不創造跨 BC 關係；若 committed facts 不能共存而需新決策，human-check。
三檔 source of truth／render representation 必須一致，沒有新 Archify／dataflow delivery authority。

### Status / Allowed Transitions / Artifact Paths

**Historical C29 state:** `pr-open / bounded publish and audit completed`。已提交 candidate
`bd465e53614594ce2d4739cac19d28d17927986c`，approved Plan-Reviewer receipt sole commit
`b3e9b0f242632be4280553f0bed64214020e167f`，integration subject
`9c6ec737e9a900e2bcd1a02f2a6808bcb91e73aa`，passing Tester evidence sole commit
`31e727d96d4e0843714dca1c7898ac93da9c33ef`，approved independent review sole commit
`fc12dea6be989aaecfdfc71a86fa1b330256fffe`。Phase 4.5 factual plan／step alignment 已完成；bounded push 與
actual PR head／mergeability／thread audit 已完成，audited head `ee2825c785aad152e5785a021acdb68e3056e84d`。既定順序：candidate-only commit → independent approved
Plan-Reviewer receipt → receipt-only commit → `creator-in-progress` integration subject → `tester-in-progress` →
committed passing evidence → `review-ready`／independent review → committed approved evidence → Planner Phase 4.5 →
`publish-in-progress` bounded push → `pr-open` audit。`needs-rework` 回 Implementer，以新 subject 重走 Tester／Reviewer。
feature integration merge 是本次 bounded subject，不授權 Human-only PR merge。

| Exact path | Writer / role | Authority |
| --- | --- | --- |
| `analysis/loaded-runtime-cache/requirements.md` | Plan-Creator / intent | C29 contract |
| `analysis/loaded-runtime-cache/technical-spec.md` | Plan-Creator / execution spec | C29 contract |
| `plan/loaded-runtime-cache/loaded-runtime-cache.plan.md` | Plan-Creator / plan, later factual alignment | Planner route |
| `plan/loaded-runtime-cache/loaded-runtime-cache.spec.md` | Plan-Creator / acceptance | C29 contract |
| `plan/loaded-runtime-cache/loaded-runtime-cache.step.md` | Plan-Creator / tracker, later factual alignment | Planner route |
| `plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<c29-candidate-40-hex-sha>.json` | Independent Plan-Reviewer / standard verdict | committed candidate |
| `docs/architecture/business-capability/architecture-brief.md` | Implementer / manual resolution | approved C29 receipt |
| `docs/architecture/business-capability/index.html` | Implementer / manual resolution | approved C29 receipt |
| `docs/architecture/business-capability/scene.js` | Implementer / manual resolution | approved C29 receipt |
| `plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<c29-integration-subject-40-hex-sha>.json` | Tester / factual checks | immutable subject |
| `plan/loaded-runtime-cache/loaded-runtime-cache.implementation-review-log-<c29-integration-subject-40-hex-sha>.json` | Independent Reviewer / verification | committed passing same-subject evidence |

SHA substitutions are deterministic full lowercase 40-hex commit facts only. Versioned paths are immutable, never
overwritten. Automatic dev tree changes are bounded by the exact committed parent, not a manual wildcard writer path.

### Implementation Steps / Validation / Evidence Contract

1. Implementer commits only five artifacts. Independent Plan-Reviewer reviews committed candidate and writes standard
   JSON with exactly `verdict`, `blocking_issues`, `copilot_feedback_triage` (`ADDRESS`, `DISCUSS`, `SKIP`). Only an approved
   receipt committed unchanged alone opens integration.
2. Implementer integrates fixed dev parent in feature worktree, resolves only three manual paths, records actual parents
   and commits one immutable merge subject. Verify markers absent, both committed fact sets preserved, and no extra manual
   edits relative to automatic merge result. Integration subject includes full automatic dev tree, not merely three-file diff.
3. Tester checks actual topology, manual-delta bounds, facts, document/scene consistency and relevant existing regressions.
   Tester alone writes exact six-key JSON: `schema_version` (integer `1`), `topic` (`loaded-runtime-cache`),
   `implementation_subject_commit` (full subject SHA), `status` (`passing|failing`), `commands` (nonempty array, each object
   exactly nonempty string `command` and integer `exit_code`), `recorded_by` (`Tester`). Passing requires all zero;
   failing at least one nonzero. Implementer commits unchanged Tester evidence as the sole path, no planning/source mix.
4. Independent Reviewer consumes only committed same-subject passing Tester evidence, verifies integration and actor
   order, and writes exact seven-key JSON: `schema_version` (integer `1`), `topic` (`loaded-runtime-cache`),
   `implementation_subject_commit` (same full SHA), `tester_evidence_commit` (full sole evidence commit SHA),
   `verdict` (`approved|needs-rework`), `blocking_issues` (string array; empty for approved, nonempty for needs-rework),
   `recorded_by` (`Independent Reviewer`). Implementer unchanged-sole-commits it separately after Tester commit.
   No committed passing evidence means no review record; no evidence may share another evidence or subject commit.
5. Approved committed review permits Planner Phase 4.5 factual plan／step alignment, existing-PR bounded push and actual
   head／mergeability／thread audit. Schema／writer／SHA／non-sole commit／topology／scope／fact failures fail closed.

### Reviewer Handoff / Post-merge / Unresolved Items

Machine-consumable planning handoff is the standard three-key receipt above; implementation handoff is the seven-key
same-subject review record. C29 authorizes no classification, reply, resolve, PR approval／merge, release, post-merge,
tag or final summary.

Human-only/open: `jnBpk`/`4043480108`, `kQ95O`/`4060023123`, `kqiZ5`/`4070096561`, `lAR8T`/`4078761998`,
`lfQmF`/`4091213944`. Unclassified/open: `m-94E`/`4130289778`, `m-94K`/`4130289786`, `nXkrM`/`4140364926`,
`nXrAw`/`4140406331`, `nXrA0`/`4140406337`. These are observations without disposition; later Planner routing required.

## C30 Current-Head Seven-Pair Classification Successor (authoritative current routing)

Historical C30：`classification committed / exact permitted replies completed`。C30 只分類 exact seven pairs；承接 completed C29 factual
publish／audit 與固定 S `9c6ec737e9a900e2bcd1a02f2a6808bcb91e73aa`、T `31e727d96d4e0843714dca1c7898ac93da9c33ef`、
V `fc12dea6be989aaecfdfc71a86fa1b330256fffe`、audited head `ee2825c785aad152e5785a021acdb68e3056e84d`。

| Field | Contract |
| --- | --- |
| Goal / In-Scope | Current-head-bound independent classification of seven pairs, followed only by individually authorized exact actions. |
| Out-Of-Scope / Non-Goal | New implementation／RED／green／architecture decisions／source／tests／dataflow changes, Human PR approval／merge／release／post-merge. |
| Modify | `analysis/loaded-runtime-cache/requirements.md`, `analysis/loaded-runtime-cache/technical-spec.md`, `plan/loaded-runtime-cache/loaded-runtime-cache.plan.md`, `plan/loaded-runtime-cache/loaded-runtime-cache.spec.md`, `plan/loaded-runtime-cache/loaded-runtime-cache.step.md`: Plan-Creator only. |
| Written | Independent Plan-Reviewer standard receipt and Independent Reviewer fixed classification receipt below; Implementer alone commits each unchanged separately. |
| ReadOnly | Predecessor evidence, dev worktree, all unlisted paths／threads, five Human-only locks. |
| Deleted | None. |
| TestCase | Exact SHA／head／pair／writer／schema／enum／nullability／sole commit checks; invalid evidence fails closed. |

Exact pairs：`m-94E`/`4130289778`、`m-94K`/`4130289786`、`nXkrM`/`4140364926`、`nXrAw`/`4140406331`、
`nXrA0`/`4140406337`、`nXzEu`/`4140459575`、`nXzE1`/`4140459585`。No prefilled outcomes／replies／resolutions。

### Artifact paths / writer / ordering

Implementer commits exactly five planning artifacts in a non-merge candidate-only commit. Independent Plan-Reviewer
alone writes `plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<c30-candidate-40-hex-sha>.json`;
standard exact keys `verdict`, `blocking_issues`, `copilot_feedback_triage`, approved requires empty blockers and
needs-rework nonempty, triage `ADDRESS|DISCUSS|SKIP`. Implementer unchanged sole evidence-only commits approved receipt.
Planner then checks committed C29 S/T/V and actual audited head. Independent Reviewer alone writes immutable
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-9c6ec737e9a900e2bcd1a02f2a6808bcb91e73aa-ee2825c785aad152e5785a021acdb68e3056e84d.json`.
Exact eight-key schema: `schema_version`, `topic`, `implementation_subject_commit`, `tester_evidence_commit`,
`implementation_review_evidence_commit`, `pr_head_commit`, `classifications`, `recorded_by`; values bind integer `1`,
this topic, fixed S/T/V/head above, exactly seven entries and `Independent Reviewer`. Each entry exactly `thread`,
`comment`, `outcome`, `reply`; outcome `REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK`. Only REPLY_AND_RESOLVE has nonempty
factual string reply; other replies JSON null. Full technical-spec C30 schema／fail-closed rules apply.
Implementer alone unchanged sole evidence-only commits classification receipt separately; Planner then routes only
exact committed REPLY_AND_RESOLVE entries for Implementer factual reply／resolve. ADDRESS needs bounded repair route;
HUMAN_CHECK remains open. Wrong／stale head, pair, writer, schema, SHA, ordering or overwritten receipt fails closed.

### Human boundary / unresolved items

`jnBpk`/`4043480108`、`kQ95O`/`4060023123`、`kqiZ5`/`4070096561`、`lAR8T`/`4078761998`、
`lfQmF`/`4091213944` remain Human-only/open. C30 classification does not authorize their actions or Human approval／
merge／release／post-merge. Original mission／protocol／outcomes／visualization／follow-ups remain unchanged.

## C31 Five-ADDRESS Bounded Repair Successor（authoritative current routing）

### Goal / Outcome / Scope

Current：`publish-in-progress / bounded push pending`。C31 已完成 Phase 4.5 factual alignment；
committed candidate `6604b7a41a679d6c85fc90bcc5d4ca6ab621e3c7` → approved planning receipt
`854878afd7dd0ea1ba8866c07a616bdeac7a5785` → RED subject
`d84ea7b410ff4811806bdeebba568c5ee88fc399` → failing Tester evidence
`d68196a308b2f2fd333f0838cdb29fe8ce7a260e` → green subject
`4448c9d144db74787f8c1947b51064e291552a6a` → passing Tester evidence
`7787c8b8edb760df6f81f44182bb146f8730c69d` → approved independent review
`b75242afc8fcf211c4b0e1aebe20fc410f567d6f`。Tracking commit、push、live audit、classification
與逐項 thread action 尚未完成；不預填其 head、結果或 verdict。C30 classification sole commit
`005ec865f216de9f63f7dbfdd8df424d78a03afa` is completed predecessor evidence. Live completed replies:
`m-94E`/`4130289778`→`4140750473`、`nXrAw`/`4140406331`→`4140753564`; both resolved.
C31 addresses only `m-94K`/`4130289786`, `nXkrM`/`4140364926`, `nXrA0`/`4140406337`,
`nXzEu`/`4140459575`, `nXzE1`/`4140459585`; outcomes/replies/resolutions remain unchosen until independent classification.

| Field | Contract |
| --- | --- |
| Goal / In-Scope | Complete the existing static independence scanner cases and terminate the Miss edge at future integration, consistent with committed architecture-brief point 6. |
| Modify | Plan-Creator only five standard planning files. RED Implementer only `tests/test_loaded_runtime_cache_bc_independence.py`; green Implementer only that file, `docs/architecture/business-capability/scene.js`, `docs/architecture/business-capability/index.html`. |
| Written | Independent Plan-Reviewer, Tester, Independent Reviewer evidence at immutable full-SHA paths below; only Implementer commits each unchanged alone. |
| ReadOnly | dev worktree, predecessor evidence, architecture-brief, unlisted paths and threads. |
| Deleted | None. |
| Out-Of-Scope / Non-Goal | Runtime/library source/API changes; executing imports/source; arbitrary Python evaluation; new architecture/ACL/wiring/backend/DI/lifecycle; Human PR approval/merge/release/post-merge. |
| TestCase | Paired tuple/list simple-name aliases with attribute exclusion; builtins getattr assigned/direct import callable; positional/kw-only default bindings; forbidden callable in positional/keyword call arguments; benign controls; Miss endpoint and scene/inline agreement; exact evidence bounds. |

### Locked Decisions / Boundaries

The technical-spec C31 is execution authority. Destructuring pairs matching RHS elements with corresponding simple-name
targets, including nested paired tuple/list literals; ignore attributes without losing sibling names. No star/iterable
inference. `getattr` on known builtins aliases with literal `__import__` covers assigned/direct calls. Actual positional
and keyword-only function defaults bind forbidden callables to corresponding parameters. Call argument and keyword
values cover static forbidden callable passing to executor.submit/map, including direct expressions and retained aliases;
ordinary callables remain allowed. Prior direct imports, fixtures, mocks, assertions and scanner behavior persist.
Scene Miss stops at labelled future integration boundary per architecture-brief point 6. Minimal endpoint-related node,
edge, label/geometric changes and inline scene synchronization only; independent Runtime/Execution contract facts stay
intact. No new implemented handoff or architecture decision. No stable-library surface, README/VERSION or release changes.

### Artifact Paths / Status / Implementation Steps

Planning paths (Plan-Creator only): `analysis/loaded-runtime-cache/requirements.md`,
`analysis/loaded-runtime-cache/technical-spec.md`, `plan/loaded-runtime-cache/loaded-runtime-cache.plan.md`,
`plan/loaded-runtime-cache/loaded-runtime-cache.spec.md`, `plan/loaded-runtime-cache/loaded-runtime-cache.step.md`.
Implementer commits these alone as non-merge candidate; Independent Plan-Reviewer writes only
`plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<c31-candidate-40-hex-sha>.json`.
Standard three-key handoff below: `blocking_issues` is an array of objects with exactly `issue`, `file`, `fix` keys,
each a nonempty string; approved requires an empty array and needs-rework requires a nonempty array.
Implementer sole-commits approved receipt.

After Planner routing, Implementer commits RED only in declared test file. Tester writes factual failing evidence only
`plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<c31-red-subject-40-hex-sha>.json`; Implementer
unchanged-sole-commits it. Distinct green subject only uses three declared paths. Tester writes factual passing evidence
only `plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<c31-green-subject-40-hex-sha>.json`;
Implementer unchanged-sole-commits it. Both use exact six-key schema in technical-spec C31, actual command exit codes.
Only committed passing same-subject evidence permits Independent Reviewer to write
`plan/loaded-runtime-cache/loaded-runtime-cache.implementation-review-log-<c31-green-subject-40-hex-sha>.json`, exact
seven-key schema binding green subject and sole Tester commit. Implementer later sole-commits review unchanged.
Needs-rework requires new green subject, Tester, independent review. No future SHA/results/verdict/head are prefilled.
Approved review → Planner Phase 4.5 factual plan/step alignment → separate tracking commit → bounded push → live audit.
Implementation remains creator-in-progress → tester-in-progress → review-ready → reviewer-in-progress → approved or
needs-rework; approved → publish-in-progress → pr-open. Human alone approves/merges PR; no release/post-merge action.

Independent Reviewer then writes only
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-<c31-green-subject-40-hex-sha>-<actual-current-pr-head-40-hex-sha>.json`.
Exact eight keys `schema_version`, `topic`, `implementation_subject_commit`, `tester_evidence_commit`,
`implementation_review_evidence_commit`, `pr_head_commit`, `classifications`, `recorded_by`; bind integer 1, this topic,
actual S/T/V/head full SHAs, five entries and Independent Reviewer. Entries exactly `thread`, `comment`, `outcome`, `reply`
for five listed pairs; enum `REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK`; nonempty factual reply only for REPLY_AND_RESOLVE,
otherwise null. Implementer unchanged-sole-commits receipt. Planner routes each permitted exact reply/resolve thereafter;
ADDRESS needs bounded repair, HUMAN_CHECK stays open. Wrong/stale head, scope, writer, schema, SHA, pair, ordering,
non-sole commit or overwritten evidence fails closed. Full deterministic schema authority: technical-spec C31.

### Validation / Acceptance / Reviewer Handoff

RED cases collect and fail for declared behavior. Green scoped pytest plus existing runtime contract regressions pass;
paired target alignment, attribute exclusion, benign controls, JS syntax, scene/inline equality and endpoint semantics
are verified. Independent review checks actual subject bounds, no source execution/new wiring and same-subject evidence.

```json
{
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "copilot_feedback_triage": {"ADDRESS": [], "DISCUSS": [], "SKIP": []}
}
```

### Post-merge / Open Questions / Unresolved Items

No release/post-merge action. `nYQqw`/`4140648790` unclassified/open, five Human-only pairs `jnBpk`/`4043480108`,
`kQ95O`/`4060023123`, `kqiZ5`/`4070096561`, `lAR8T`/`4078761998`, `lfQmF`/`4091213944` excluded/open.
New decisions or out-of-scope requirements return Planner/human boundary. Original mission, scope, protocol, outcomes,
testing strategy, Architecture Visualization and follow-up missions persist.
