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

- current_step: c15-phase-4.5-alignment-pending
- next_step: Planner C15 Phase 4.5 alignment
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
