# loaded-runtime-cache

C50 is the sole current bounded repair route；original mission及舊records不變。
Current implementation metadata、path／schema／ordered gates 以文末 C50 契約為準；
canonical Implementation Steps 只有 C50 六項，舊 C47 七項移入 completed historical section。

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

本原 mission／historical profile保留；C50 bounded current Python profile在文末 C50 section，
不從原 public API／C14 metadata 推導本輪新增權限。

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

C50 current implementation completion gate；下列六項依 new-S committed passing T 實際完成，不繼承舊 C47 completed。
1. C50 在 `tests/test_loaded_runtime_cache_bc_independence.py` 新增四 original findings 的 isolated RED fixtures及benign controls；新測試名稱含 c50，rejecting 名稱另含 rejects、controls不含 rejects。只新增tests，不修scanner、不執行fixture source，collection／controls須pass、四類genuineassertionfail。
2. C50 在 `tests/test_loaded_runtime_cache_bc_independence.py` 補 FunctionDef／AsyncFunctionDef／Lambda 的全部 ast.arguments local-name semantic syntax，兩BC ownership適用；不判annotation／default／scope，不改既有assertions。
3. C50 在 `tests/test_loaded_runtime_cache_bc_independence.py` 沿existing simple-name assignment固定點保留known directly imported builtins.getattr getter identity；lookup仍exact-two-pos/no-keywords／knownmodule／literalattribute／existingUSE，不新增持有拒絕或arbitrary getter。
4. C50 在 `tests/test_loaded_runtime_cache_bc_independence.py` 補known module Name／existingalias.__dict__.get的directstringliteral／exact-one-pos/no-keywords/default解析，只三既有forbidden import-callables後續USE；unknown/dynamic/ordinary/missing/unused controls不誤拒，不推namespacealias或arbitrarymapping。
5. C50 在 `tests/test_loaded_runtime_cache_bc_independence.py` 將全部 ast.comprehension.target交existingName／Tuple／List／Starred semantic-name traversal，ignoreAttribute，含list/set/dict/generator及asyncTARGETSYNTAX；不擴comprehensionaliasinference／RHSiterable／orderedscope／fixtureexecution。
6. C50 在 `tests/test_loaded_runtime_cache_bc_independence.py` 保留所有舊direct imports／fixtures／mocks／assertions與十二locks，對sameimmutablegreen S實際通過兩 scoped pytest檔／Ruff／strict Pyright；未完成前canonicalsteps保持pending，不將review／publish／classification算作implementationsteps。

Reviewer／Tester evidence／publish／classification／thread actions另依C50 lifecycle，非implementation completion。

## Historical Implementation Steps — C47（completed nonrouting provenance）

C47 completed implementation provenance：七項[X]依 new-green-S committed passing T；C48 class-only不新增codepending，舊 S/T/V frozen history保留。
1. C47 在 `tests/test_loaded_runtime_cache_bc_independence.py` 新增 isolated RED fixtures／benign controls，六個 authorized repair pairs 各有獨立 rejecting assertion；名稱含 c47，rejecting 名稱另含 rejects。保留 scanner、既有 fixtures／direct imports／assertions，不執行 fixture source。
2. C47 在 `tests/test_loaded_runtime_cache_bc_independence.py` 納入 known module.__dict__[direct string literal] 的既有 forbidden import-callable lookup／alias 後續 USE，保留 unknown receiver／dynamic key／generic namespace／unused possession controls。
3. C47 在 `tests/test_loaded_runtime_cache_bc_independence.py` 納入 known forbidden import-callable.__call__ 的既有 USE 判定，保留 ordinary callable／arbitrary attribute／unused possession controls。
4. C47 在 `tests/test_loaded_runtime_cache_bc_independence.py` 保留既有 IfExp 兩個 branch 的全部 finite known module alternatives，以任一 alternative＋後續 existing forbidden surface USE 作 existential 判定；不求值 branch condition，不作 ordered scope／CFG／iterable 推論。
5. C47 在 `tests/test_loaded_runtime_cache_bc_independence.py` 將 For／AsyncFor TARGET 交既有 Name／Tuple／List／Starred foreign semantic-name syntax traversal，忽略 attribute targets；不新增 AsyncFor／nested For alias inference，不解析 RHS iterable。
6. C47 在 `tests/test_loaded_runtime_cache_bc_independence.py` 檢查 import LOCAL binding 的 foreign semantic name（asname 優先；無 alias 的 Import 使用 first segment）；保留既有 Identity semantic source-name 禁則與 benign source-name／attribute controls。
7. C47 在 `tests/test_loaded_runtime_cache_bc_independence.py` 將 With／AsyncWith optional_vars 交相同 foreign semantic target-name traversal，忽略 attribute targets，不求值 context manager；保留所有舊 regression 並實際通過 scoped pytest／Ruff／strict Pyright。

Reviewer／Tester evidence／publish／classification／thread actions 另依 C47 lifecycle，不是此 completion gate。

## Historical Implementation Steps — C42（completed nonrouting provenance）

C42 completed implementation；以下四項已有同 subject committed passing Tester evidence；C43不新增implementationsteps。
1. C42 在 `tests/test_loaded_runtime_cache_bc_independence.py` 新增 isolated RED fixtures，涵蓋三個 original comments、module-order／tuple-list／single-multi alternatives、兩BC sync-async definition names及benign controls；不修scanner、不執行fixturesource。
2. C42 在 `tests/test_loaded_runtime_cache_bc_independence.py` 將 importlib.__import__ direct/imported/assigned aliases 的後續使用纳入既有forbidden-callable detection；保留getter bounds及unused-callable controls。
3. C42 在 `tests/test_loaded_runtime_cache_bc_independence.py` 的 semantic declaration check 納入 FunctionDef/AsyncFunctionDef definition NAME，兩BC foreign names受既有ownership assertion約束，普通names/string/attribute不誤判。
4. C42 在 `tests/test_loaded_runtime_cache_bc_independence.py` 保存既有syncFor/simpletarget/directtuple-list/nonstar elements的全部knownmodule alternatives，依任一alternative與後續use構成既有forbidden surface判定；保留既有regressions与controls，scopedpytest/Ruff/strictPyright須actualpassing。

Reviewer／publish／classification／thread actions 是後續 workflow，不是 implementation completion。

## Historical Implementation Steps — C40（completed nonrouting provenance）

C40 completed implementation 的以下四項已由 committed green subject／passing Tester evidence 完成；C41 不新增 implementation steps。
1. C40 建立 isolated RED fixtures，涵蓋原兩個 comments、tuple/list prefix/suffix/star positions、
   attribute siblings、For literal/post-use 與 unused/unknown/async controls，不執行 source。
2. C40 starred assignment 僅建立 direct literal RHS 的確定 simple-name prefix/suffix aliases；
   不推論 starred container、不展開 RHS starred、不建立 attribute alias。
3. C40 synchronous For 僅對 simple-name target/direct tuple-list literal 明列 elements，
   使用既有 known-forbidden resolver 建立 alias，後續 use 依既有 detector 判定。
4. C40 保留所有 existing non-star/default/walrus/getattr/semantic/direct-import regressions，
   green 完整 scoped tests/Ruff/strict Pyright passing，不新增 unused-callable binding 拒絕。

Reviewer/publish/classification/thread actions 是後續 workflow，不與 implementation completion 混同。

## Historical Implementation Steps — C37（completed nonrouting provenance）

C37 為唯一 active implementation；完成事實由 immutable green subject 與 committed passing Tester evidence 綁定。
1. C37 semantic-name target checks recursively inspect syntactic tuple/list/nested/starred targets only，
   excluding attribute targets and RHS/alias/iterable inference。
2. C37 direct-name NamedExpr semantic checks retain all existing declared detectors。
3. C37 direct known-builtins imported getattr local/asname detection retains exact-two-positional/no-keyword/
   known-module/literal-attribute bounds and existing forbidden set, without arbitrary callable alias inference。
4. C37 isolated foreign/benign/attribute/non-builtins regressions preserve direct imports, fixtures/assertions,
   bare/qualified getattr and no-star alias behavior; actual scoped tests/Ruff/strict Pyright pass。

Reviewer／publish／classification／thread actions 屬後續 workflow，尚未宣稱完成。

## Historical Implementation Steps — C11–C14（frozen nonrouting provenance）

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

## C31 Five-ADDRESS Bounded Repair Successor（completed predecessor routing）

### Goal / Outcome / Scope

Historical C31：`pr-open / five exact thread actions completed`。C31 已完成 Phase 4.5 factual alignment；
committed candidate `6604b7a41a679d6c85fc90bcc5d4ca6ab621e3c7` → approved planning receipt
`854878afd7dd0ea1ba8866c07a616bdeac7a5785` → RED subject
`d84ea7b410ff4811806bdeebba568c5ee88fc399` → failing Tester evidence
`d68196a308b2f2fd333f0838cdb29fe8ce7a260e` → green subject
`4448c9d144db74787f8c1947b51064e291552a6a` → passing Tester evidence
`7787c8b8edb760df6f81f44182bb146f8730c69d` → approved independent review
`b75242afc8fcf211c4b0e1aebe20fc410f567d6f`。Tracking commit `851dedef3aa4e0f1bdfdb34ed39f2c6518fd8892`、
push、live audit、classification sole commit `9bdea139d9c3d79a8ae413333c9e15e877c42a30` 與五個 actions 已完成；
exact completed replies 見 C32 factual record。C30 classification sole commit
`005ec865f216de9f63f7dbfdd8df424d78a03afa` is completed predecessor evidence. Live completed replies:
`m-94E`/`4130289778`→`4140750473`、`nXrAw`/`4140406331`→`4140753564`; both resolved.
C31 addresses only `m-94K`/`4130289786`, `nXkrM`/`4140364926`, `nXrA0`/`4140406337`,
`nXzEu`/`4140459575`, `nXzE1`/`4140459585`; independent classification and permitted replies/resolutions 已完成。

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

## C32 Current-Head Three-Pair Classification Successor（completed predecessor routing）

C31 已完成 committed S `4448c9d144db74787f8c1947b51064e291552a6a`、
passing T `7787c8b8edb760df6f81f44182bb146f8730c69d`、
approved V `b75242afc8fcf211c4b0e1aebe20fc410f567d6f`；C31 classification sole commit／audited PR head
`9bdea139d9c3d79a8ae413333c9e15e877c42a30`。C31 五個已回覆且 resolved 的事實：
`m-94K`→`4141037841`、`nXkrM`→`4141038098`、`nXrA0`→`4141038268`、
`nXzEu`→`4141038483`、`nXzE1`→`4141038696`。

C32 exact pairs 僅 `nYQqw`/`4140648790`、`nZI5l`/`4141010658`、
`nZI5n`/`4141010661`。Committed candidate `42ec2293d306546df06529996bc63adb058b3eee`、
approved receipt commit `6a3271af13443c1b794c28038a68d4c158163071`、classification sole commit
`83ffddf831da3f4ecb26656a96bc6aeb28ef98d5` 為 completed predecessor facts。
`nYQqw` 已回覆 `4141149003` 並 resolved；另外兩 pairs 為 ADDRESS，後续權限僅見 C33。
五個 Human-only pairs `jnBpk`/`4043480108`、`kQ95O`/`4060023123`、
`kqiZ5`/`4070096561`、`lAR8T`/`4078761998`、`lfQmF`/`4091213944` 排除/open。
舊 rejected receipt `loaded-runtime-cache.plan-review-receipt-a46241e4245957cd820eae13fd2bf22ab0a9226d.json`
是 frozen nonrouting provenance，不能覆寫、提交作本輪 approval 或重新使用。
### Goal／Scope／Boundaries／Acceptance

Goal／In-Scope：僅依 C31 verified facts 分類三個新 pairs，再執行 individually authorized exact actions。
Modify：Plan-Creator 僅上述五份 planning artifacts。Written：獨立 Plan-Reviewer standard receipt 與
Independent Reviewer fixed classification receipt；只有 Implementer 可原樣分別 sole-commit。
ReadOnly：dev worktree、predecessor evidence、其他 paths／threads、Human-only locks。
Deleted：無。Out-Of-Scope／Non-Goal：新 implementation、RED/green、source/tests/diagram/runtime/API、
architecture/ACL/backend/DI/lifecycle 決策、README/VERSION、PR approval／Human merge／release／post-merge。
TestCase：full SHA/committed evidence/live head/exact pair/schema/writer/order/sole commit/immutability checks；
invalid evidence fails closed。No stable-library surface or release changes。原 mission、scope、outcomes、
Runtime Registry protocol、測試策略、Architecture Visualization 與 follow-up missions 全部保留。

### Status／Allowed Transitions

Historical state：`c32-completed`。C31 是 completed frozen predecessor route。C32 five-file candidate → independent
Plan-Reviewer approved receipt → separate sole receipt commit → Planner fixed-triple/head verification → independent
three-pair classification → separate sole classification commit → bounded push/live audit → per-pair actions → human-check。
No candidate SHA、future verdict／result／reply 預填。只有 Human 可 PR approval／merge／release／post-merge。

### Exact artifact／schema／writer／sole-commit contract

Plan-Creator 僅修改 `analysis/loaded-runtime-cache/requirements.md`、
`analysis/loaded-runtime-cache/technical-spec.md`、`plan/loaded-runtime-cache/loaded-runtime-cache.plan.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.step.md`。Implementer 將這五檔以獨立 non-merge candidate-only commit 提交。
Independent Plan-Reviewer 唯一可寫
`plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<c32-candidate-40-hex-sha>.json`；
exact keys `verdict`、`blocking_issues`、`copilot_feedback_triage`；verdict `approved|needs-rework`。
Blockers 是 exact `issue`、`file`、`fix` nonempty string objects array；approved 必為空，
needs-rework 必非空。Triage exact `ADDRESS`、`DISCUSS`、`SKIP` arrays。
Implementer 原樣 separate sole evidence-only commit approved receipt；Planner 核對 committed C31 S/T/V
與 live audited fixed PR head 後，Independent Reviewer 唯一可寫 immutable path：

`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-4448c9d144db74787f8c1947b51064e291552a6a-9bdea139d9c3d79a8ae413333c9e15e877c42a30.json`

JSON 為單一 object，top-level keys 恰為 `schema_version`、`topic`、
`implementation_subject_commit`、`tester_evidence_commit`、`implementation_review_evidence_commit`、
`pr_head_commit`、`classifications`、`recorded_by`。分別為 integer `1`、
string `loaded-runtime-cache`、上述固定 S/T/V/head 完整 lowercase 40-hex SHA、
exact three-entry array、string `Independent Reviewer`。Entry keys 恰為 `thread`、`comment`、
`outcome`、`reply`；thread/comment 為上述 exact pairs string IDs、每 pair 各一次。
Outcome enum `REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK`；僅 REPLY_AND_RESOLVE reply 為 nonempty factual string，
其餘 reply 必為 JSON null。Implementer 原樣以 separate sole evidence-only commit 提交 classification receipt。
Planner 才能依 committed entries 派 Implementer 對 exact REPLY_AND_RESOLVE 留指定 factual reply 並 resolve；
ADDRESS 回 bounded repair route，HUMAN_CHECK 保持 open。Planning approval 本身不授權 thread actions。

Wrong/stale live PR head、wrong S/T/V binding、extra/missing pair/key、wrong writer/schema/enum/nullability、
overwrite、非 sole evidence commit、跨 topic evidence 或跳過 actor ordering 一律 fail closed。
Planning candidate commits 留在 local 到 classification 完成後 bounded push，不以未分類的新 PR head 取代 fixed head。

### Reviewer Handoff

```json
{"verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]}}
```

## C33 Qualified Builtins getattr Repair Successor（completed predecessor routing）

C32 classification 已由 committed receipt 將 `nZI5l`/`4141010658` 分為 ADDRESS；
`nYQqw`/`4140648790` 已回覆 `4141149003` 並 resolved。C32 為 completed predecessor routing。
C33 僅修正 `nZI5l`/`4141010658`；`nZI5n`/`4141010661` 的 starred argument
問題留在 human-check/open，與五個既有 Human-only pairs `jnBpk`/`4043480108`、
`kQ95O`/`4060023123`、`kqiZ5`/`4070096561`、`lAR8T`/`4078761998`、
`lfQmF`/`4091213944` 一律排除。舊 rejected receipt
`plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-a46241e4245957cd820eae13fd2bf22ab0a9226d.json`
保持 frozen nonrouting provenance；不可覆寫或作 approval。

### Goal / Outcome / Scope

Goal／In-Scope：既有 static BC-independence scanner 識別 known builtins module 的 qualified
`getattr` 與其 module alias，在既有 forbidden attribute lookup 範圍內拒絕 direct invocation
及 assignment-retained callable bypass。Historical state：`c33-completed`。
Modify：Plan-Creator 僅五份標準 planning artifacts；Implementer RED 與 green 均僅
`tests/test_loaded_runtime_cache_bc_independence.py`。Written：獨立 Plan-Reviewer／Tester／
Independent Reviewer evidence at C33 immutable SHA-bound paths below，僅 Implementer 原樣 sole-commit。
ReadOnly：dev worktree、所有 predecessor evidence、source、architecture／visualization、其他 paths／threads。
Deleted：無。Out-Of-Scope／Non-Goal：starred arguments／任意 iterable inference、general callable inference、
source/import execution、新 architecture／ACL／mapper／wiring／backend／DI／lifecycle、production API、
README／VERSION、PR approval／merge／release／post-merge。無 stable-library surface 或 release change。
TestCase：qualified direct／module-alias／assignment callable regressions、bare getattr preservation、
benign len／unknown-receiver controls、exact path／writer／schema／SHA／sole evidence ordering。

### Locked Decisions / Boundaries

Execution authority 是 technical-spec 本 C33 section。維持既有 bare `getattr` 行為；
額外只接受 `ast.Attribute` callee，其 attribute 是 `getattr`、receiver 是 simple-name 且
existing module alias map 明確解析為 `builtins`。例如 `builtins.getattr`、
`bi.getattr`（`import builtins as bi`）與既有 alias map 已知的 module assignment alias。
不將未知 receiver 或任意同名方法視為 builtins。延續 exactly two positional arguments、
no keyword arguments、simple-name module target、literal string attribute 與既有 forbidden set：
`builtins.__import__`、`importlib.import_module`、`sys.modules`。不增加第三/default argument、
star／iterable expansion、general-purpose interpretation、callable getattr alias inference 或動態 execution。
維持 existing direct imports、fixtures、mocks、assertions 與所有先前 scanner regressions。
原 mission、scope、outcomes、Runtime Registry reuse protocol、測試策略、Architecture Visualization
與 follow-up missions 不變。

### Artifact Paths / Implementation Steps / Allowed Transitions

Plan-Creator 在 feature worktree 只修改：
`analysis/loaded-runtime-cache/requirements.md`、
`analysis/loaded-runtime-cache/technical-spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.plan.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.step.md`。
Implementer 獨立 non-merge exact-five candidate-only commit 後，Independent Plan-Reviewer 唯一寫
`plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<c33-candidate-40-hex-sha>.json`。
Exact keys：`verdict`、`blocking_issues`、`copilot_feedback_triage`。
Verdict `approved|needs-rework`；blockers 是 exact `issue`／`file`／`fix` nonempty string objects
array，approved 空、needs-rework 非空；triage exact `ADDRESS`／`DISCUSS`／`SKIP` arrays。
Implementer 原樣 separate sole evidence-only commit approved receipt；Planner 才可 route RED。

Implementer only test-file non-merge RED subject → Tester actual collection-success／declared-behavior failure →
failing evidence → Implementer unchanged sole evidence-only commit → distinct test-file-only green subject →
Tester actual scoped pytest and existing runtime contract regressions → passing evidence → Implementer unchanged
sole evidence-only commit → Independent Reviewer same-subject review → Implementer unchanged sole approved
review commit → Planner Phase 4.5 → Plan-Creator factual plan／step alignment → Implementer separate tracking
commit／bounded push → actual PR-head audit → Independent Reviewer single-pair classification → Implementer
sole receipt commit／bounded push → Planner exact action route → Implementer factual reply／resolve／live audit。
creator-in-progress → tester-in-progress → review-ready → reviewer-in-progress → approved or needs-rework；
approved → publish-in-progress → pr-open。Needs-rework 必須新的 green subject 與完整 Tester／Reviewer chain。
Planning approval 不授權 thread actions。Human alone PR approval／merge／release／post-merge。

Tester 唯一寫
`plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<c33-red-subject-40-hex-sha>.json` 或
`plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<c33-green-subject-40-hex-sha>.json`，
對應各自實際 immutable subject。Exact six keys `schema_version`、`topic`、
`implementation_subject_commit`、`status`、`commands`、`recorded_by`：
integer `1`、string `loaded-runtime-cache`、actual full lowercase 40-hex SHA、
`passing|failing`、nonempty array of exact `command` nonempty string／`exit_code` integer objects、`Tester`。
passing 要求全部實際 exit codes 為 0；failing 至少一個 nonzero，RED 需確認為新增指定行為失敗，
不可用 syntax／dependency／無關 failure 代替。Tester 不 commit；Implementer 原樣分別 sole-commit。

Independent Reviewer 只消費 committed passing same-green-subject Tester evidence，唯一寫
`plan/loaded-runtime-cache/loaded-runtime-cache.implementation-review-log-<c33-green-subject-40-hex-sha>.json`。
Exact seven keys `schema_version` integer `1`、`topic` string `loaded-runtime-cache`、
`implementation_subject_commit` same actual full green SHA、`tester_evidence_commit` actual full sole passing
Tester commit SHA、`verdict` `approved|needs-rework`、`blocking_issues` string array
(approved 空／needs-rework 非空)、`recorded_by` string `Independent Reviewer`。
Reviewer 不 commit；Implementer 原樣 separate sole evidence-only commit。

### Validation / Acceptance / Current-Head Classification

RED covers qualified known builtins direct calls、imported module alias、module-assignment alias、retrieved callable
assignment，目標覆蓋既有 forbidden set；benign `len` 與 unknown receiver 不誤判。
Green scoped independence pytest 與既有 loaded-runtime-cache contract regressions passing，確認 bare getattr、
原 tests direct-import behavior、one-file subject bounds。Evidence 必須實際 command facts；不預填任何 future
candidate／subject／commit／verdict／result／PR head／reply／resolution。

已提交 approved review 與 Phase 4.5／push／actual-head audit 後 Independent Reviewer 唯一可寫：
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-<c33-green-subject-40-hex-sha>-<actual-current-pr-head-40-hex-sha>.json`。
Exact eight top-level keys `schema_version`、`topic`、`implementation_subject_commit`、
`tester_evidence_commit`、`implementation_review_evidence_commit`、`pr_head_commit`、
`classifications`、`recorded_by`。Values integer `1`、string `loaded-runtime-cache`、
actual full lowercase 40-hex S／sole passing T commit／sole approved V commit／audited PR head、
exact one-entry array、`Independent Reviewer`。Entry exact `thread`、`comment`、
`outcome`、`reply`；string IDs `nZI5l`／`4141010658`；
outcome `REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK`，只有 REPLY_AND_RESOLVE reply 為 nonempty factual
string，其餘為 JSON null。Implementer 原樣 separate sole evidence-only commit，Planner 方可 route
exact committed REPLY_AND_RESOLVE entry 的指定 reply／resolve；ADDRESS 要 bounded repair，
HUMAN_CHECK 保持 open。所有 receipts immutable；wrong/stale head、binding、path、key、writer、SHA、
pair、enum、nullability、order、non-sole commit 或 overwritten evidence fail closed。

### Reviewer Handoff / Post-merge / Unresolved Items

```json
{"verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]}}
```

No release／post-merge actions。C33 qualified known-builtins getattr implementation 與獨立 verification 已提交：
candidate `05a37198c667a845f3370c4d25b859337edf6548`；
approved Plan-Reviewer receipt commit `d9092bedad9794f968b69dbbfe6412c11bdc0cbf`；
RED subject `3e1b05f72508f856e68ba61bd9669496309d811a`；
failing Tester evidence commit `21185456b8d6afed0832fc6c78dd547dad1e9f72`；
green subject `82e3dc7efa04d7a432568e254ffca82bc3337ecd`；
passing Tester evidence commit `eff8eb2f5f554d6eb01f57fcf5755cddcab4adfe`；
approved Independent Reviewer evidence commit `d29da7b8a855b3887c9bcbb7183b1db0cd744043`。
Planner 已 route Phase 4.5；本次 Plan-Creator factual plan／step alignment 完成。
Separate tracking commit `be7f374efdda4eb8ce4fe945108ab8399a903a13`、bounded push／actual PR-head audit、single-pair classification
與 sole commit `e17956b4d83ba81129cc7787d145436e7f73fd95`／push 已完成；
`nZI5l` 已留 reply `4141461698` 並 resolved。
starred `nZI5n` 與上述 Human-only five 留在 human-check/open，unlisted threads 不可回覆／resolve。

## C34 Current-Head Three-Pair Classification Successor（completed predecessor routing）

### Goal / Outcome / Scope

Historical state：`c34-completed`。Goal／In-Scope：僅獨立分類三個新 pairs
`nZm9b`/`4141203131`、`nZm9d`/`4141203134`、`nZm9h`/`4141203139`；
不預填分類結果、reply 或 resolution。本輪固定使用同 topic committed C33
S `82e3dc7efa04d7a432568e254ffca82bc3337ecd`、
passing T commit `eff8eb2f5f554d6eb01f57fcf5755cddcab4adfe`、
approved V commit `d29da7b8a855b3887c9bcbb7183b1db0cd744043`，
與 audited PR head `e17956b4d83ba81129cc7787d145436e7f73fd95`。

C33 已提交 verification chain；其 classification sole commit 為
`e17956b4d83ba81129cc7787d145436e7f73fd95`；`nZI5l`/`4141010658`
已留 reply `4141461698` 並 resolved。C32 committed candidate
`42ec2293d306546df06529996bc63adb058b3eee`、approved receipt commit
`6a3271af13443c1b794c28038a68d4c158163071`、classification sole commit
`83ffddf831da3f4ecb26656a96bc6aeb28ef98d5` 為 completed predecessor facts；
`nYQqw` 已留 reply `4141149003` 並 resolved。C32／C33 皆為 completed
predecessor routing，本 C34 section 取代其未完成 tracking 敘述作 current routing。

### Locked Decisions / Boundaries / Exclusions

六個 Human-only pairs `jnBpk`/`4043480108`、`kQ95O`/`4060023123`、
`kqiZ5`/`4070096561`、`lAR8T`/`4078761998`、
`lfQmF`/`4091213944`、starred-argument `nZI5n`/`4141010661`
均排除，保持 human-check/open。舊 rejected receipt
`loaded-runtime-cache.plan-review-receipt-a46241e4245957cd820eae13fd2bf22ab0a9226d.json`
是 frozen nonrouting provenance，不覆寫、不提交為本輪 approval、不重新使用。

Modify：Plan-Creator 僅五份 standard planning artifacts。Written：獨立
Plan-Reviewer candidate-bound receipt 與 Independent Reviewer fixed classification receipt。
Deleted：無。ReadOnly：dev worktree、既有 source/tests/diagram、predecessor evidence、
所有未列 pairs 與六個 Human locks。Out-Of-Scope／Non-Goal：新 implementation、
RED/green、runtime/API/backend/DI/lifecycle、architecture/ACL 決策、README/VERSION、
PR approval／Human merge／release／post-merge。原 mission、scope、outcomes、
Runtime Registry protocol、測試策略、Architecture Visualization、follow-up missions
全部維持；無 stable-library surface 或 release 變更。

### Status / Allowed Transitions / Artifact Paths / Implementation Steps

Plan-Creator 僅於 feature worktree 修改：
`analysis/loaded-runtime-cache/requirements.md`、
`analysis/loaded-runtime-cache/technical-spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.plan.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.step.md`。
Implementer 建立 exact-five non-merge candidate-only commit；Independent Plan-Reviewer
只審該 committed candidate，唯一寫
`plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<c34-candidate-40-hex-sha>.json`。
單一 JSON object exact keys `verdict`、`blocking_issues`、`copilot_feedback_triage`；
verdict `approved|needs-rework`；blockers 為 exact `issue`／`file`／`fix`
nonempty string objects array，approved 空、needs-rework 非空；triage 為 exact
`ADDRESS`／`DISCUSS`／`SKIP` arrays。Implementer 原樣 separate sole
evidence-only commit approved receipt。未 approved 不可分類。

Planner 核對 committed fixed S/T/V 與 live fixed PR head 後，Independent Reviewer
唯一可寫 immutable path：
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-82e3dc7efa04d7a432568e254ffca82bc3337ecd-e17956b4d83ba81129cc7787d145436e7f73fd95.json`。

JSON object top-level keys 恰為 `schema_version`、`topic`、
`implementation_subject_commit`、`tester_evidence_commit`、
`implementation_review_evidence_commit`、`pr_head_commit`、
`classifications`、`recorded_by`。Values 分別是 integer `1`、
string `loaded-runtime-cache`、上述固定 S/T/V/head 完整 lowercase 40-hex SHA、
exact three-entry array、string `Independent Reviewer`。
Each entry exact keys `thread`、`comment`、`outcome`、`reply`；
thread/comment 是上述三個 exact pairs 的 string IDs，每 pair 恰一次。
Outcome enum `REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK`；只有
REPLY_AND_RESOLVE reply 是 nonempty factual string，其餘 reply 必為 JSON null。
Reviewer 不 commit；Implementer 原樣 separate sole evidence-only commit classification，
再 bounded push。Planning commits 保持 local 到分類完成，不先改變 fixed live PR head。

Planner 才可依 committed classification route exact REPLY_AND_RESOLVE entry；
Implementer 留該指定 factual reply 並 resolve exact thread，之後 live audit。
ADDRESS 回 bounded repair route；HUMAN_CHECK 保持 open。Planning approval 不授權
reply/resolve。Sequence：candidate → independent approved planning receipt →
sole receipt commit → fixed-triple/live-head verification → independent classification →
sole classification commit → bounded push → exact per-pair actions → human-check。
publish-in-progress 只可進 pr-open；Human alone PR approval／merge／release／post-merge。

### Validation / Acceptance / TestCase

Verify committed same-topic S/T/V、passing Tester／approved Reviewer、full SHA、live head、
exact paths/pairs/key sets/schema/writers/enum/nullability/ordering/sole commits/immutability。
Wrong/stale head、wrong binding、extra/missing key/pair、wrong writer、overwrite、非 sole commit、
跳過 actor order 或跨 topic evidence 一律 fail closed。No new implementation or RED/green；
不預填 future candidate SHA、verdict、classification outcome、reply 或 resolution。

### Reviewer Handoff / Post-merge / Unresolved Items

```json
{"verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]}}
```

本輪三個 pairs 尚待獨立分類。六個 Human-only pairs 保持 open；
unlisted threads 不可回覆／resolve。No release／post-merge actions。

## C35 Current-Head Five-Pair Classification Successor（needs-rework predecessor routing）

### Goal / Outcome / Scope

Historical state：`c35-classification-needs-rework`。Goal／In-Scope：僅獨立分類五個新 pairs
`naZCW`/`4141524912`、`naZCY`/`4141524919`、`na5mB`/`4141737461`、
`na5mE`/`4141737466`、`na5mM`/`4141737476`；
不預填分類結果、reply 或 resolution。本輪固定使用同 topic committed C33
S `82e3dc7efa04d7a432568e254ffca82bc3337ecd`、
passing T commit `eff8eb2f5f554d6eb01f57fcf5755cddcab4adfe`、
approved V commit `d29da7b8a855b3887c9bcbb7183b1db0cd744043`，
與 audited PR head `71545af8c0d6f87ea4f43bf28d380edfed75aa82`。

C33 已提交 verification chain；其 classification sole commit 為
`e17956b4d83ba81129cc7787d145436e7f73fd95`；`nZI5l`/`4141010658`
已留 reply `4141461698` 並 resolved。C32 committed candidate
`42ec2293d306546df06529996bc63adb058b3eee`、approved receipt commit
`6a3271af13443c1b794c28038a68d4c158163071`、classification sole commit
`83ffddf831da3f4ecb26656a96bc6aeb28ef98d5` 為 completed predecessor facts；
`nYQqw` 已留 reply `4141149003` 並 resolved。C32／C33 皆為 completed
predecessor routing。C34 candidate `8ef5a690669b654a16343c091ccb7617eeb04011`、
approved planning receipt commit `2ecd41b08fe91d875b3607bda45f52b1386eff85`、
classification sole commit `71545af8c0d6f87ea4f43bf28d380edfed75aa82` 已提交。
`nZm9b`/`4141203131` 已留 reply `4141853147` 並 resolved；
`nZm9d`/`4141203134`、`nZm9h`/`4141203139` 為 ADDRESS，尚未修復，
本輪不授權其 implementation 或 resolution。C34 是 completed predecessor routing。
既有 For lock 保留，不新增 For handling、alias inference 或相關 implementation。
本 C35 section 取代其未完成 tracking 敘述作 current routing。

### Locked Decisions / Boundaries / Exclusions

六個 Human-only pairs `jnBpk`/`4043480108`、`kQ95O`/`4060023123`、
`kqiZ5`/`4070096561`、`lAR8T`/`4078761998`、
`lfQmF`/`4091213944`、starred-argument `nZI5n`/`4141010661`
均排除，保持 human-check/open。舊 rejected receipt
`loaded-runtime-cache.plan-review-receipt-a46241e4245957cd820eae13fd2bf22ab0a9226d.json`
是 frozen nonrouting provenance，不覆寫、不提交為本輪 approval、不重新使用。

Modify：Plan-Creator 僅五份 standard planning artifacts。Written：獨立
Plan-Reviewer candidate-bound receipt 與 Independent Reviewer fixed classification receipt。
Deleted：無。ReadOnly：dev worktree、既有 source/tests/diagram、predecessor evidence、
所有未列 pairs 與六個 Human locks。Out-Of-Scope／Non-Goal：新 implementation、
RED/green、runtime/API/backend/DI/lifecycle、architecture/ACL 決策、README/VERSION、
PR approval／Human merge／release／post-merge。原 mission、scope、outcomes、
Runtime Registry protocol、測試策略、Architecture Visualization、follow-up missions
全部維持；無 stable-library surface 或 release 變更。

### Status / Allowed Transitions / Artifact Paths / Implementation Steps

Plan-Creator 僅於 feature worktree 修改：
`analysis/loaded-runtime-cache/requirements.md`、
`analysis/loaded-runtime-cache/technical-spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.plan.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.step.md`。
Implementer 建立 exact-five non-merge candidate-only commit；Independent Plan-Reviewer
只審該 committed candidate，唯一寫
`plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<c35-candidate-40-hex-sha>.json`。
單一 JSON object exact keys `verdict`、`blocking_issues`、`copilot_feedback_triage`；
verdict `approved|needs-rework`；blockers 為 exact `issue`／`file`／`fix`
nonempty string objects array，approved 空、needs-rework 非空；triage 為 exact
`ADDRESS`／`DISCUSS`／`SKIP` arrays。Implementer 原樣 separate sole
evidence-only commit approved receipt。未 approved 不可分類。

Planner 核對 committed fixed S/T/V 與 live fixed PR head 後，Independent Reviewer
唯一可寫 immutable path：
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-82e3dc7efa04d7a432568e254ffca82bc3337ecd-71545af8c0d6f87ea4f43bf28d380edfed75aa82.json`。

JSON object top-level keys 恰為 `schema_version`、`topic`、
`implementation_subject_commit`、`tester_evidence_commit`、
`implementation_review_evidence_commit`、`pr_head_commit`、
`classifications`、`recorded_by`。Values 分別是 integer `1`、
string `loaded-runtime-cache`、上述固定 S/T/V/head 完整 lowercase 40-hex SHA、
exact five-entry array、string `Independent Reviewer`。
Each entry exact keys `thread`、`comment`、`outcome`、`reply`；
thread/comment 是上述五個 exact pairs 的 string IDs，每 pair 恰一次。
Outcome enum `REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK`；只有
REPLY_AND_RESOLVE reply 是 nonempty factual string，其餘 reply 必為 JSON null。
Reviewer 不 commit；Implementer 原樣 separate sole evidence-only commit classification，
再 bounded push。Planning commits 保持 local 到分類完成，不先改變 fixed live PR head。

Planner 才可依 committed classification route exact REPLY_AND_RESOLVE entry；
Implementer 留該指定 factual reply 並 resolve exact thread，之後 live audit。
ADDRESS 回 bounded repair route；HUMAN_CHECK 保持 open。Planning approval 不授權
reply/resolve。Sequence：candidate → independent approved planning receipt →
sole receipt commit → fixed-triple/live-head verification → independent classification →
sole classification commit → bounded push → exact per-pair actions → human-check。
publish-in-progress 只可進 pr-open；Human alone PR approval／merge／release／post-merge。

### Validation / Acceptance / TestCase

Verify committed same-topic S/T/V、passing Tester／approved Reviewer、full SHA、live head、
exact paths/pairs/key sets/schema/writers/enum/nullability/ordering/sole commits/immutability。
Wrong/stale head、wrong binding、extra/missing key/pair、wrong writer、overwrite、非 sole commit、
跳過 actor order 或跨 topic evidence 一律 fail closed。No new implementation or RED/green；
不預填 future candidate SHA、verdict、classification outcome、reply 或 resolution。

### Reviewer Handoff / Post-merge / Unresolved Items

```json
{"verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]}}
```

本輪五個 pairs 尚待獨立分類。六個 Human-only pairs 保持 open；
unlisted threads 不可回覆／resolve。No release／post-merge actions。

## C36 Replacement Five-Pair Classification Successor（completed predecessor routing）

### Goal / Outcome / Scope / Locked Decisions

Historical state：`c36-completed`。僅為 C35 needs-rework 建立新的獨立 classification
receipt，不作 implementation。C35 candidate `0e9c84959ec602dbc117413613ce6afd371b6822`
與 approved planning receipt commit `53b19a478f23a31de6183510cc6569901f9f66f9`
是已提交事實；其未提交 classification receipt 使用 full PRRT thread IDs，
不符合 suffix ID contract，屬 rejected nonrouting provenance。原 path
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-82e3dc7efa04d7a432568e254ffca82bc3337ecd-71545af8c0d6f87ea4f43bf28d380edfed75aa82.json`
保留原樣，不覆寫、不提交作有效 evidence、不重用其 outcomes。

本輪 exact pairs 僅 `naZCW`/`4141524912`、`naZCY`/`4141524919`、
`na5mB`/`4141737461`、`na5mE`/`4141737466`、`na5mM`/`4141737476`。
thread 欄位必為這五個 suffix IDs，不是 full PRRT node IDs；comment 為上述 string IDs。
固定 S `82e3dc7efa04d7a432568e254ffca82bc3337ecd`、
passing T commit `eff8eb2f5f554d6eb01f57fcf5755cddcab4adfe`、
approved V commit `d29da7b8a855b3887c9bcbb7183b1db0cd744043`、
live audited head `71545af8c0d6f87ea4f43bf28d380edfed75aa82`。
不得预填新 candidate SHA、verdict、outcomes、replies 或 resolutions。

### Boundaries / Exclusions

In-Scope／Goal：replacement receipt contract 與 independent five-pair classification。
Modify：Plan-Creator 僅以下五個 artifacts。Written：獨立 review／classification receipts。
ReadOnly：dev、source/tests/diagram/governance、舊 receipts、unlisted pairs。Deleted：無。
Out-Of-Scope／Non-Goal：implementation、RED/green、新 architecture/runtime/API/ACL/backend/DI/lifecycle
決策、README/VERSION、PR approval／merge／release／post-merge。
六 Human-only pairs `jnBpk`/`4043480108`、`kQ95O`/`4060023123`、
`kqiZ5`/`4070096561`、`lAR8T`/`4078761998`、
`lfQmF`/`4091213944`、`nZI5n`/`4141010661` 保持 excluded/open。
`nZm9d`/`4141203134` 與 `nZm9h`/`4141203139` ADDRESS 尚未修復，
既有 For boundary/lock 保持，本輪不授權其修改或 resolve。
原 mission、scope、outcomes、Runtime Registry protocol、測試策略、
Architecture Visualization、follow-up missions 維持，無 stable-library/release 變更。

### Status / Allowed Transitions / Artifact Paths / Implementation Steps

Plan-Creator 僅 feature worktree：
`analysis/loaded-runtime-cache/requirements.md`、
`analysis/loaded-runtime-cache/technical-spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.plan.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.step.md`。
Implementer exact-five non-merge candidate-only commit；Independent Plan-Reviewer 唯一寫
`plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<c36-candidate-40-hex-sha>.json`。
單一 JSON object exact keys `verdict`、`blocking_issues`、`copilot_feedback_triage`；
verdict `approved|needs-rework`，blockers exact `issue`/`file`/`fix` nonempty
string objects array，approved 空、needs-rework 非空；triage exact `ADDRESS`/`DISCUSS`/`SKIP` arrays。
Implementer 原樣 sole evidence-only commit approved receipt；Planner 核對 fixed S/T/V/live head，
Independent Reviewer 才獨立重新分類，唯一寫全新 replacement path：

`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-82e3dc7efa04d7a432568e254ffca82bc3337ecd-71545af8c0d6f87ea4f43bf28d380edfed75aa82-c36-<c36-candidate-40-hex-sha>.json`

Template variable 必為本輪實際 committed exact-five candidate full lowercase 40-hex SHA；
同一值也綁定本輪 Plan-Reviewer receipt filename。Candidate 未提交前不預填。
此 path 不重用 C35 path，writer 寫入前確認從未存在；immutable 禁止覆寫。
Classification JSON top-level exact eight keys `schema_version`、`topic`、
`implementation_subject_commit`、`tester_evidence_commit`、
`implementation_review_evidence_commit`、`pr_head_commit`、
`classifications`、`recorded_by`；values 為 integer `1`、string `loaded-runtime-cache`、
上述 fixed full S/T/V/head、exact five-entry array、string `Independent Reviewer`。
每 entry exact `thread`、`comment`、`outcome`、`reply`，每上述 suffix pair 恰一次。
Outcome enum `REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK`；
僅 REPLY_AND_RESOLVE reply 為 nonempty factual string，其餘 JSON null。
Reviewer 不 commit；Implementer 原樣 separate sole evidence-only commit，bounded push。
Planning commits 留 local 到 fixed live-head classification 完成後才 push。

Sequence：new candidate → independent approved Plan-Reviewer receipt → sole receipt commit →
fixed-triple/live-head verification → independent NEW classification → sole classification commit →
bounded push → Planner exact-action route → Implementer 指定 factual reply/resolve/live audit。
不沿用 rejected outcomes；planning approval 不授權 thread actions。
ADDRESS 回 bounded repair，HUMAN_CHECK 保持 open；只對 committed REPLY_AND_RESOLVE entries 執行。
publish-in-progress 只可進 pr-open；Human alone PR approval／merge／release／post-merge。

### Validation / Acceptance / TestCase / Reviewer Handoff / Unresolved Items

Verify exact five suffix IDs/pairs、same-topic committed S/T/V、passing/approved evidence、
fixed live head、fresh candidate-bound path、schema/writers/enum/nullability/actor order/
sole commits/immutability。Wrong/stale binding、full PRRT IDs、extra/missing pairs/keys、
overwriting/reusing old receipt、prefilled outcomes、非 sole commit 一律 fail closed。
```json
{"verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]}}
```
五 pairs 尚待 new independent classification；六 Human locks 與 For boundary 保持 open。
No release/post-merge actions。

## C37 Static BC Independence Scanner Repair（completed predecessor routing）

### C37 Committed Approval Facts / Phase 4.5 Alignment

Historical alignment state：`c37-publish-in-progress`。Actual Git facts：
candidate `a8cb80d6fdcfe0adef0e63d9bfb1c42df78d0d52`；
approved planning receipt commit `337a31a35427b1221dd2e64d8d1c9ad3a006c78a`；
RED subject `622a67473c9db74b586e8171bcf0b7dab3489941`；
failing Tester sole commit `9b985c4ac7f3faf17fe6405e5d4602cb7453a78d`；
green subject `6bb8ee90895b566c3def0eb161cce51c14b0e601`；
passing Tester sole commit `437f40788fe1b37b2bcd4698624a478d8e959a13`。
approved Independent Reviewer sole evidence commit
`6328c5a585eb9f4c884b80f8a526a4c09dd68d62` 已提交，綁定同 green S 與 passing T。
Planner 已核 same-subject approval gate，Phase 4.5 factual alignment 完成。
Separate alignment commit `84a3b0e5220d8efeaffa6e7a887797c5edc248aa`／bounded push、
actual PR-head audit、three-pair classification sole commit
`8e881573d497f4489a760acc4adbb0b221141721`／push 與三個指定 reply／resolve 已完成，
actual reply IDs 見 C38 factual record。此為已發生事實，不預填新 route 的 head/outcome。
不因 approval／alignment 虛勾舊 C14 classification。
本兩檔 alignment 僅記 actual committed facts，未變更 approved scope/schema/contract，
不建立新 candidate chain。舊 provenance/receipts／六 Human／For locks 保留。


### C37 Risks / Rollback

Risks：recursive semantic-target traversal 可能誤擴張 existing alias inference；
必須只檢查 target-side tuple/list/starred 的 local semantic names，不配對或讀取 RHS，
attribute targets 維持 non-local。直接 imported builtins getattr 可能誤判任意同名 callable；
僅接受 known-builtins import local/asname 與既有 exact-two-positional/no-keyword/
known-module/literal-attribute bounds。NamedExpr 新 semantic check 可能遮蔽既有 detectors；
保留其 regression assertions，並以 benign/attribute/non-builtins controls 排除 false positives。
Scoped tests、Ruff、strict Pyright 與 independent review 驗證上述風險。

Rollback：僅對本輪五份 planning artifacts 的尚未核准差異作 bounded planning repair，
或对 `tests/test_loaded_runtime_cache_bc_independence.py` 的本輪 immutable test subject
作新的 bounded repair commit；不得 broad reset、改 frozen C14 scope 或覆寫舊 evidence。
Implementation needs-rework／回修須建立新的 immutable subject，重新執行 Tester →
passing evidence sole commit → Independent Reviewer → review sole commit，再走後續 alignment/
classification route。已提交或 rejected receipts 原樣保留 nonrouting provenance，包括
本輪先前 needs-rework Plan-Reviewer receipt；六 Human locks／For boundary 保持。


### C37 Executable Validation Commands / Configuration

RED 新增 tests function names 必含 `c37`，指定 forbidden/foreign regressions 另含
`rejects`；benign/attribute/non-builtins controls 不含 rejects，確保 collection/control/failure
selection 可直接驗證且 nonempty。這是既有三項 bounded fixtures 的命名，不新增行為。
Tester 在各自 immutable subject 實際執行並記錄：
- RED collection：`uv run --frozen pytest -p no:tach tests/test_loaded_runtime_cache_bc_independence.py -k c37 --collect-only -q`，
  必須成功並確認三項 declared regression/control coverage。
- RED benign controls：`uv run --frozen pytest -p no:tach tests/test_loaded_runtime_cache_bc_independence.py -k 'c37 and not rejects' -q`，
  必須 passing，不能以 unrelated failure 充作 RED。
- RED declared behavior failure：`uv run --frozen pytest -p no:tach tests/test_loaded_runtime_cache_bc_independence.py -k c37 -q`，
  必須 actual assertion failure，對應新增 foreign-target／walrus／imported-getattr behavior。
- Green complete scanner/runtime regressions：
  `uv run --frozen pytest -p no:tach tests/test_loaded_runtime_cache_bc_independence.py tests/test_loaded_runtime_cache_contracts.py -q`。
- Scoped Ruff：
  `uv run --frozen ruff check tests/test_loaded_runtime_cache_bc_independence.py tests/test_loaded_runtime_cache_contracts.py`。
- Scoped strict Pyright：
  `uv run --frozen pyright tests/test_loaded_runtime_cache_bc_independence.py tests/test_loaded_runtime_cache_contracts.py`。

`-p no:tach` 明確停用 tach selection/filter，確保列出的 tests 真正執行；
沿 C33 committed passing Tester evidence 的相同 green invocation。
Config authority：`pyproject.toml` 的 `[tool.pyright]`（Python 3.12、strict、
extraPaths src）、`[tool.pytest.ini_options]`（strict config/markers 與既有 coverage）、
`[tool.ruff]`／`[tool.ruff.lint]`（py312、line-length 100、ALL）、
`[tool.ruff.lint.per-file-ignores]`（test S101）。不改 config。
Commands 是待執行 contract，不是預填結果；所有 passing evidence 需上述實際 exit code 0，
RED failing evidence 需 actual declared assertion nonzero。


### Python implementation metadata（canonical python-implementation-plan profile）

- Async-planning status：exempt — 本輪僅同步 static AST test analysis，沒有 async boundary、
  external I/O、resource lifecycle、concurrency、timeout/retry/cancellation 或 runtime ownership。
- Module/package placement：僅 `tests/test_loaded_runtime_cache_bc_independence.py`。
- New public API：no，既有 direct-module API 不變。
- Interface changes：no，既有 Protocol signatures 不變。
- Breaking changes allowed：no，保留既有 direct imports/fixtures/mocks/assertions。
- New dependencies：no，僅既有 standard-library ast 與 pytest tooling。
- Error-handling strategy：scanner 的 factual assertion failures 交 Tester；不改 production exceptions。
- Typing strategy：保留現有 Python 3.12 test typing；不用 Any/cast/dynamic import/runtime introspection。
- Non-goals：不做 RHS destructuring/alias/iterable inference；不擴張 For/star-call handling；
  不修改 production source/API；不建立 backend/DI/lifecycle；不更改 architecture 或 Human locks。
- Test categories：happy path（指定 foreign semantic target／forbidden getter 被發現）；
  edge cases（nested tuple/list/starred targets、import asname、direct walrus）；
  failure paths（RED declared assertion failures，排除 collection/dependency errors）；
  forbidden behaviors（不執行 source、不讀 RHS 推論、不把 attributes/unknown getter 視為 local imports）；
  regression preservation（direct imports/fixtures/mocks/assertions、bare/qualified getter、
  no-star alias behavior、既有 scanner/runtime contract tests）。


### Goal / Outcome / Scope / Locked Decisions

Historical draft state：`c37-planning-draft`。本輪同 static BC independence scanner mission，
僅修正三個 ADDRESS pairs：`nZm9h`/`4141203139`、
`naZCY`/`4141524919`、`na5mM`/`4141737476`。
C36 candidate `8a35890310d788d7834be035e891bb0b53baa96d`、
approved planning receipt commit `55a65a036b20ad566d8a9a9fa410f33f5393fc2c`、
classification sole commit `8306cf004eb86ac26da016a009d73da0582bc0be`
均已提交。已 reply/resolved：`naZCW`→`4142061895`、
`na5mB`→`4142062611`、`na5mE`→`4142063556`。
C36 completed predecessor routing，本 C37 取代其 current routing。

### Boundaries / In-Scope / Out-Of-Scope / Goal / Non-Goal

Implementation sole path：`tests/test_loaded_runtime_cache_bc_independence.py`。
1. Assignment-target semantic-name checks recursively inspect only syntactic
   `ast.Tuple`/`ast.List` elements and `ast.Starred.value`, including nested targets；
   each `ast.Name` target applies the existing opposite-BC semantic-name rule。
   Attribute targets 不算 local names；不讀 RHS 配對、不推論 aliases/iterables/values。
   既有 alias inference 與其 direct-name/no-star 行為維持，不因本 semantic-name check 擴張。
2. `ast.NamedExpr` 的 direct-name target 套用既有 foreign semantic-name detector；
   不移除或改寫其他已宣告 detectors，不以 RHS 推論 semantic identity。
3. 直接 `from builtins import getattr`（含 `asname`）所建立的 local callable
   可用於既有 literal attribute check。限定 import 的 known-builtins module，
   callee 為該 local simple-name，exact two positional args、no keywords，
   first arg simple-name module 且 existing map 已知、second arg literal string。
   forbidden set 維持 `builtins.__import__`、`importlib.import_module`、
   `sys.modules`。不推論任意 getter assignment/callable alias，不展開 star/iterable；
   bare/qualified known-builtins getattr 既有行為維持。

ReadOnly：dev、source/docs/governance/diagram、舊 evidence、其他 threads。
Modify：五個 planning artifacts；RED/green 僅上述 test path。Written：各 actor 的
SHA-bound immutable evidence。Deleted：無。Out-Of-Scope／Non-Goal：source/API/runtime/
registry/backend/DI/lifecycle、new architecture/ACL、README/VERSION、PR approval/merge/release/post-merge。
六 Human-only pairs `jnBpk`/`4043480108`、`kQ95O`/`4060023123`、
`kqiZ5`/`4070096561`、`lAR8T`/`4078761998`、
`lfQmF`/`4091213944`、`nZI5n`/`4141010661` 保持 excluded/open。
`nZm9d`/`4141203134` For boundary/lock 保留，不授權 repair/resolve。
兩份既有 untracked rejected receipts 保留原樣 nonrouting provenance，不覆寫、不提交。
原 mission/scope/outcomes/Runtime Registry protocol/測試策略/Architecture Visualization/
follow-up missions 維持；無 stable-library/release changes。

### Artifact Paths / Status / Allowed Transitions / Implementation Steps

Plan-Creator 只在 feature worktree 修改五個 exact artifacts：
`analysis/loaded-runtime-cache/requirements.md`、
`analysis/loaded-runtime-cache/technical-spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.plan.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.step.md`。
Implementer exact-five non-merge candidate-only commit；Independent Plan-Reviewer 唯一寫
`plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<c37-candidate-40-hex-sha>.json`。
Single JSON exact keys `verdict`、`blocking_issues`、`copilot_feedback_triage`；
verdict approved|needs-rework，blockers exact issue/file/fix nonempty string objects array
(approved 空／needs-rework 非空)，triage exact ADDRESS/DISCUSS/SKIP arrays。
Implementer 原樣 separate sole evidence-only commit approved receipt，Planner 才 route RED。

Implementer sole-test-path RED subject（只加 isolated regression fixtures/assertions，未修 detector）→
Tester actual collection-success and declared-behavior failure evidence → Implementer sole evidence commit →
distinct sole-test-path green subject → Tester scoped scanner and existing runtime contract regression evidence →
Implementer sole passing evidence commit → Independent Reviewer same-subject committed passing-evidence review →
Implementer sole approved review commit → Planner Phase 4.5 → Plan-Creator factual plan/step alignment →
Implementer separate alignment commit/push → actual PR-head audit → Independent Reviewer new three-pair
classification → Implementer sole classification commit/push → Planner exact actions →
Implementer factual replies/resolutions/live audit。
creator-in-progress → tester-in-progress → review-ready → reviewer-in-progress → approved|needs-rework；
needs-rework 要新 subject 與完整 Tester/Reviewer chain；
approved → publish-in-progress → pr-open。Human alone approval/merge/release/post-merge。

Tester 唯一寫
`plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<c37-red-subject-40-hex-sha>.json`
或 `plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<c37-green-subject-40-hex-sha>.json`。
Exact six keys schema_version/topic/implementation_subject_commit/status/commands/recorded_by；
integer 1、string loaded-runtime-cache、actual subject full lowercase 40-hex SHA、
passing|failing、nonempty array of exact command(nonempty string)/exit_code(integer) objects、
string Tester。Passing 要所有 actual exit codes 0；failing 至少一個 nonzero，
RED 須新增 declared assertion failure，不可 syntax/dependency/無關 failure。
Tester 不 commit；Implementer 原樣各自 separate sole evidence-only commit。

Independent Reviewer 只消費 committed passing same-green-subject evidence，唯一寫
`plan/loaded-runtime-cache/loaded-runtime-cache.implementation-review-log-<c37-green-subject-40-hex-sha>.json`。
Exact seven keys schema_version/topic/implementation_subject_commit/tester_evidence_commit/
verdict/blocking_issues/recorded_by：integer 1、loaded-runtime-cache、same actual full green SHA、
actual full sole passing T commit SHA、approved|needs-rework、string array
(approved 空／needs-rework 非空)、Independent Reviewer。
Reviewer 不 commit；Implementer 原樣 separate sole evidence-only commit。

### Validation / Acceptance / TestCase

RED fixtures 以 original comment examples 的 isolated source strings 作靜態 AST assertions，
不 exec fixture source。兩 BC foreign/benign names、tuple/list/nested/starred targets、
attribute-only controls；walrus foreign/benign controls；
direct imported/asname getattr 對 __import__/import_module/sys.modules forbidden controls，
benign attributes/non-builtins imports controls。保留 existing direct imports、fixtures/mocks/assertions、
bare/qualified getattr、no-star iterable alias behavior 與其他 regressions。
Green 須 actual scoped independence pytest 與 existing loaded-runtime-cache contract regressions passing；
Reviewer 驗證只改 sole test path、semantic-target recursion 與 alias inference 分離、
walrus detectors preservation、getter import bounds，無動態執行。

### Current-Head Classification / Reviewer Handoff / Unresolved Items

Full chain committed/pushed 且 audit 後 Independent Reviewer 唯一寫
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-<c37-green-subject-40-hex-sha>-<actual-current-pr-head-40-hex-sha>.json`。
Exact eight keys schema_version/topic/implementation_subject_commit/tester_evidence_commit/
implementation_review_evidence_commit/pr_head_commit/classifications/recorded_by；
integer 1、loaded-runtime-cache、actual full same S/sole passing T/sole approved V/audited head SHA、
exact three-entry array、Independent Reviewer。Each entry exact thread/comment/outcome/reply；
上述 three pairs 各一次，thread 必為 suffix IDs、comment string IDs，
outcome REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK；僅 REPLY_AND_RESOLVE reply nonempty factual string，
其餘 JSON null。Reviewer 不 commit；Implementer 原樣 separate sole evidence-only commit。
Planner 才可 route exact REPLY_AND_RESOLVE replies/resolutions；ADDRESS 回 bounded repair，
HUMAN_CHECK 保持 open。Planning approval 不授權 thread actions。
All paths immutable/fresh；wrong/stale SHA/head/binding/schema/pair/writer/order/non-sole commit
或 overwritten receipt fail closed。禁止預填 future SHA/verdict/result/classification/reply/resolution。

```json
{"verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]}}
```
三 pairs 待 bounded repair/verification；六 Human-only 與 For lock 保持 open。
No release/post-merge actions。

## C38 Current-Head Single-Pair Classification（completed predecessor routing）

### Goal / Outcome / Scope / Locked Decisions

Historical state：`c38-completed`。僅獨立分類 `nb1DH`/`4142124006`，
不預填 outcome/reply/resolution，不重走 implementation evidence chain。
固定 committed S `6bb8ee90895b566c3def0eb161cce51c14b0e601`、
passing T commit `437f40788fe1b37b2bcd4698624a478d8e959a13`、
approved V commit `6328c5a585eb9f4c884b80f8a526a4c09dd68d62`、
audited live PR head `8e881573d497f4489a760acc4adbb0b221141721`。

C36 committed candidate `8a35890310d788d7834be035e891bb0b53baa96d`、
approved planning receipt commit `55a65a036b20ad566d8a9a9fa410f33f5393fc2c`、
classification sole commit `8306cf004eb86ac26da016a009d73da0582bc0be`；
已 reply/resolved：`naZCW`→`4142061895`、`na5mB`→`4142062611`、
`na5mE`→`4142063556`。C36 分出的 remaining ADDRESS 修復權限已交 C37，
故其 exact permitted actions/route completed，不代表當時所有 ADDRESS 已修復。
C37 committed review approval／Phase 4.5 alignment、separate alignment commit
`84a3b0e5220d8efeaffa6e7a887797c5edc248aa`／push、actual-head audit、
classification sole commit `8e881573d497f4489a760acc4adbb0b221141721`／push 與三個
exact replies/resolutions 均完成：`nZm9h`→`4142431864`、
`naZCY`→`4142432793`、`na5mM`→`4142433541`。
C36/C37 completed predecessor routing；其早期 pending statements 僅當時 frozen provenance，
本節 committed facts 與 trackers 是目前狀態，不能沿用過時 pending 作 current routing。

### Boundaries / Exclusions / Risks / Rollback

Goal／In-Scope：一個 suffix thread/comment pair 的 independent classification。
Modify：五份 standard planning artifacts。Written：independent review/classification receipts。
ReadOnly：dev、source/tests/docs/diagram/governance、舊 evidence、unlisted threads。
Deleted：無。Out-Of-Scope／Non-Goal：implementation、RED/green、新 API/runtime/backend/DI/lifecycle/
architecture/ACL 決策、README/VERSION、PR approval／Human merge／release／post-merge。
七個 Human-only pairs `jnBpk`/`4043480108`、`kQ95O`/`4060023123`、
`kqiZ5`/`4070096561`、`lAR8T`/`4078761998`、
`lfQmF`/`4091213944`、`nZI5n`/`4141010661`、
For `nZm9d`/`4141203134` excluded/open。三份 untracked rejected receipts 保留原樣
nonrouting provenance，不提交為本輪 evidence、不覆寫。原 mission/scope/outcomes/
Runtime Registry protocol/測試策略/Architecture Visualization/follow-up missions 維持，
无 stable-library/release 變更。
Risks：過時 tracking、full PRRT IDs／suffix mismatch、stale head 或 reused receipt。
Rollback：bounded planning repair 或新 immutable replacement receipt route，保留已提交／rejected
evidence，不 broad reset、不覆寫 evidence、不虛勾歷史 classification。

### Status / Allowed Transitions / Artifact Paths / Implementation Steps

Plan-Creator 只在 feature worktree 修改
`analysis/loaded-runtime-cache/requirements.md`、
`analysis/loaded-runtime-cache/technical-spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.plan.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.step.md`。
Implementer exact-five non-merge candidate-only commit；Independent Plan-Reviewer 唯一寫
`plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<c38-candidate-40-hex-sha>.json`。
Exact three keys `verdict`/`blocking_issues`/`copilot_feedback_triage`；
verdict approved|needs-rework；blockers exact issue/file/fix nonempty string objects array，
approved 空／needs-rework 非空；triage exact ADDRESS/DISCUSS/SKIP arrays。
Implementer 原樣 separate sole evidence-only commit approved receipt；
Planner 核 committed fixed S/T/V/live head 後 Independent Reviewer 唯一寫全新 immutable path：
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-6bb8ee90895b566c3def0eb161cce51c14b0e601-8e881573d497f4489a760acc4adbb0b221141721.json`。

Single JSON exact eight keys `schema_version`、`topic`、
`implementation_subject_commit`、`tester_evidence_commit`、
`implementation_review_evidence_commit`、`pr_head_commit`、
`classifications`、`recorded_by`；values integer 1、string loaded-runtime-cache、
上述 fixed full lowercase 40-hex S/T/V/head、exact one-entry array、Independent Reviewer。
Entry exact thread/comment/outcome/reply；thread string suffix `nb1DH`，comment string
`4142124006`；outcome REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK；
僅 REPLY_AND_RESOLVE reply 為 nonempty factual string，其餘 JSON null。
Reviewer 不 commit；Implementer 原樣 separate sole evidence-only commit classification，
bounded push，Planner 方可 route exact committed REPLY_AND_RESOLVE factual reply/resolve/live audit。
ADDRESS 回 bounded repair；HUMAN_CHECK 保持 open。Planning approval 不授權 thread actions。

Sequence：candidate → independent approved receipt → sole receipt commit →
fixed-triple/live-head verification → independent single-pair classification →
sole classification commit → bounded push → Planner exact permitted actions → live audit/human-check。
Planning commits 留 local 至 fixed live-head classification 完成，不提前改 live head。
publish-in-progress 僅進 pr-open；Human alone approval/merge/release/post-merge。

### Validation / Acceptance / TestCase / Reviewer Handoff / Unresolved Items

Actual committed S/T/V/passing/approved/full-SHA/live-head verification、fresh path、
exact suffix pair/eight-key schema/writers/enum/nullability/actor order/sole commits/immutability。
Wrong/stale binding、full PRRT ID、extra/missing keys/pairs、overwrite、非 sole commit
一律 fail closed。不預填 future candidate SHA/verdict/classification/reply/resolution。
```json
{"verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]}}
```
`nb1DH` 已 reply `4142548955`／resolved；七 Human-only threads 保持 open。No release/post-merge actions。

## C39 Current-Head Single-Pair Classification（completed predecessor routing）

### Goal / Outcome / Scope / Locked Decisions

Historical state：`c39-completed`。僅獨立分類 `ncxdC`/`4142518115`，
不預填 outcome/reply/resolution，不重走 implementation evidence chain。
固定 committed S `6bb8ee90895b566c3def0eb161cce51c14b0e601`、
passing T commit `437f40788fe1b37b2bcd4698624a478d8e959a13`、
approved V commit `6328c5a585eb9f4c884b80f8a526a4c09dd68d62`、
audited live PR head `e8c9c6d94b90e79d92a20c20dee7f23cf4035b17`。

C36 committed candidate `8a35890310d788d7834be035e891bb0b53baa96d`、
approved planning receipt commit `55a65a036b20ad566d8a9a9fa410f33f5393fc2c`、
classification sole commit `8306cf004eb86ac26da016a009d73da0582bc0be`；
已 reply/resolved：`naZCW`→`4142061895`、`na5mB`→`4142062611`、
`na5mE`→`4142063556`。C36 分出的 remaining ADDRESS 修復權限已交 C37，
故其 exact permitted actions/route completed，不代表當時所有 ADDRESS 已修復。
C37 committed review approval／Phase 4.5 alignment、separate alignment commit
`84a3b0e5220d8efeaffa6e7a887797c5edc248aa`／push、actual-head audit、
classification sole commit `8e881573d497f4489a760acc4adbb0b221141721`／push 與三個
exact replies/resolutions 均完成：`nZm9h`→`4142431864`、
`naZCY`→`4142432793`、`na5mM`→`4142433541`。
C36/C37 completed predecessor routing；其早期 pending statements 僅當時 frozen provenance，
本節 committed facts 與 trackers 是目前狀態，不能沿用過時 pending 作 current routing。


C38 completed candidate `e1e331f21c478ccdbdaa2cfb51c6d209c69c9f6e`、
approved receipt commit `774d03c4ccbca1f402905844c16d11424b41bdd3`、
classification sole commit／pushed head `e8c9c6d94b90e79d92a20c20dee7f23cf4035b17`；
`nb1DH`/`4142124006` 已 reply `4142548955`／resolved。
C38 是 completed predecessor routing，本 C39 為唯一 current route。

### Boundaries / Exclusions / Risks / Rollback

Goal／In-Scope：一個 suffix thread/comment pair 的 independent classification。
Modify：五份 standard planning artifacts。Written：independent review/classification receipts。
ReadOnly：dev、source/tests/docs/diagram/governance、舊 evidence、unlisted threads。
Deleted：無。Out-Of-Scope／Non-Goal：implementation、RED/green、新 API/runtime/backend/DI/lifecycle/
architecture/ACL 決策、README/VERSION、PR approval／Human merge／release／post-merge。
七個 Human-only pairs `jnBpk`/`4043480108`、`kQ95O`/`4060023123`、
`kqiZ5`/`4070096561`、`lAR8T`/`4078761998`、
`lfQmF`/`4091213944`、`nZI5n`/`4141010661`、
For `nZm9d`/`4141203134` excluded/open。三份 untracked rejected receipts 保留原樣
nonrouting provenance，不提交為本輪 evidence、不覆寫。原 mission/scope/outcomes/
Runtime Registry protocol/測試策略/Architecture Visualization/follow-up missions 維持，
无 stable-library/release 變更。
Risks：過時 tracking、full PRRT IDs／suffix mismatch、stale head 或 reused receipt。
Rollback：bounded planning repair 或新 immutable replacement receipt route，保留已提交／rejected
evidence，不 broad reset、不覆寫 evidence、不虛勾歷史 classification。

### Status / Allowed Transitions / Artifact Paths / Implementation Steps

Plan-Creator 只在 feature worktree 修改
`analysis/loaded-runtime-cache/requirements.md`、
`analysis/loaded-runtime-cache/technical-spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.plan.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.step.md`。
Implementer exact-five non-merge candidate-only commit；Independent Plan-Reviewer 唯一寫
`plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<c39-candidate-40-hex-sha>.json`。
Exact three keys `verdict`/`blocking_issues`/`copilot_feedback_triage`；
verdict approved|needs-rework；blockers exact issue/file/fix nonempty string objects array，
approved 空／needs-rework 非空；triage exact ADDRESS/DISCUSS/SKIP arrays。
Implementer 原樣 separate sole evidence-only commit approved receipt；
Planner 核 committed fixed S/T/V/live head 後 Independent Reviewer 唯一寫全新 immutable path：
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-6bb8ee90895b566c3def0eb161cce51c14b0e601-e8c9c6d94b90e79d92a20c20dee7f23cf4035b17.json`。

Single JSON exact eight keys `schema_version`、`topic`、
`implementation_subject_commit`、`tester_evidence_commit`、
`implementation_review_evidence_commit`、`pr_head_commit`、
`classifications`、`recorded_by`；values integer 1、string loaded-runtime-cache、
上述 fixed full lowercase 40-hex S/T/V/head、exact one-entry array、Independent Reviewer。
Entry exact thread/comment/outcome/reply；thread string suffix `ncxdC`，comment string
`4142518115`；outcome REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK；
僅 REPLY_AND_RESOLVE reply 為 nonempty factual string，其餘 JSON null。
Reviewer 不 commit；Implementer 原樣 separate sole evidence-only commit classification，
bounded push，Planner 方可 route exact committed REPLY_AND_RESOLVE factual reply/resolve/live audit。
ADDRESS 回 bounded repair；HUMAN_CHECK 保持 open。Planning approval 不授權 thread actions。

Sequence：candidate → independent approved receipt → sole receipt commit →
fixed-triple/live-head verification → independent single-pair classification →
sole classification commit → bounded push → Planner exact permitted actions → live audit/human-check。
Planning commits 留 local 至 fixed live-head classification 完成，不提前改 live head。
publish-in-progress 僅進 pr-open；Human alone approval/merge/release/post-merge。

### Validation / Acceptance / TestCase / Reviewer Handoff / Unresolved Items

Actual committed S/T/V/passing/approved/full-SHA/live-head verification、fresh path、
exact suffix pair/eight-key schema/writers/enum/nullability/actor order/sole commits/immutability。
Wrong/stale binding、full PRRT ID、extra/missing keys/pairs、overwrite、非 sole commit
一律 fail closed。不預填 future candidate SHA/verdict/classification/reply/resolution。
```json
{"verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]}}
```
`ncxdC` 已 reply `4142682597`／resolved；當時七 Human-only locks 為 historical boundary。
其中兩 binding locks 的解除僅見 C40 explicit contract；其餘五 locks 保持open。


## C40 Literal-Only Starred Assignment / For Binding Repair（completed predecessor routing）

### C40 Committed Approval Facts / Phase 4.5 Alignment

Historical state：`c40-completed`。Actual committed candidate
`077884842c5e97e27ea3ece914764096ff42afff`；
approved Plan-Reviewer receipt commit `e030601e8cffdbb8a550d456caad61b3c06f327f`；
RED subject `a11f4b6f2ad364b2bc255397931657cce4eb568f`；
failing Tester sole commit `f3aeb5317f829f182c595967d491c666c2e5e92b`；
green subject `29db32481975381ef71c03ce616a32559963f323`；
passing Tester sole commit `020777486cf6b4acd6981e5d7ac542315ff19984`。
本兩檔 state alignment 只記 committed facts，canonical 四項 implementation 已完成。
Independent Reviewer approved sole evidence commit
`25d2f96286b0f0b36432a1452cb3823bddf4cb9d` 已提交，綁定上述同 green S／passing T。
Planner 已核 verification gate，Phase 4.5 factual alignment 完成。
Separate alignment commit／bounded push、actual-head audit／classification、classification sole
commit／push、exact reply／resolve 已完成；actual commits／reply IDs 見 C41 facts。
Scope/schema/five Human locks/old provenance 不變，不建立新 candidate chain。


### Goal / Outcome / Scope / Locked Decisions

Historical draft state：`c40-planning-draft`。Human 授權 bounded contract exceptions，採 literal-only
binding，exact two pairs `nZI5n`/`4141010661`、`nZm9d`/`4141203134`。
Implementation sole path `tests/test_loaded_runtime_cache_bc_independence.py`；
只擴張下列兩項 static alias-binding contract，後續 use 的 forbidden detection 沿既有規則。
C39 completed candidate `880e6c1e5ffcd4b707b46431975f0459c645e09a`、
approved receipt commit `358394d8f3feaf89ba430acb5c968f0398f328f0`、
classification sole commit `238fb87654507b7f44d230493e2e8e068166da5d`；
`ncxdC`/`4142518115` 已 reply `4142682597`／resolved。
C39/C40 均為 completed predecessor routing；本段是 historical C40 contract，current route 見 C41。

### Boundaries / In-Scope / Out-Of-Scope / Semantic Contract

1. Starred assignment：direct tuple/list target，恰一個 starred target，RHS 是 direct
   tuple/list literal 且不含 RHS starred expansion。當 literal 元素數 >= non-star target 數，
   只配對確定位置的 prefix/suffix direct simple-name targets 至對應 RHS expressions，
   prefix 從前、suffix 從尾；starred target 在前／中／後皆同規則。
   Attribute sibling 不建立 local alias，但保留其他確定 simple-name siblings。
   不推論 starred-container 內容/alias、不推論 arbitrary iterable、不展開 RHS starred；
   非配對／不足元素不建立此新增 binding。既有 non-star nested literal pairing 維持。
2. Synchronous `ast.For`：target 為 direct `ast.Name`，iter 為 direct tuple/list literal，
   明列各 non-star element 用 existing known-forbidden resolver resolve 成 target 的 alias。
   只記已知 forbidden module/callable binding；不 execute loop、不 general-evaluate elements、
   不推論 unknown/arbitrary iterable，不擴張 AsyncFor/comprehension/generator expression。
   literal 內 RHS starred 不展開，相關未知 branch 不建立新增 binding。

只解除這兩個 literal-only exceptions 的既有 no-star/iterable binding 限制；
其餘 prohibition 保留。Alias acquisition 本身不新增拒絕：
unused callable bindings、ordinary/empty/nonpaired bindings 應接受；
後續已知 forbidden callable/module use 依既有 detector 拒絕。
`sys.modules` access 等 independently forbidden rules 保留，不能以 unused-binding
control 壓制。既有 non-star paired/default/walrus/getattr/semantic checks、direct imports、
fixtures/mocks/assertions 全部保留，fixtures 僅 AST static parsing 不 execution。

Goal／In-Scope：這兩項 binding bypass 與對應 meaningful RED/green controls。
Modify：五份 planning artifacts；RED/green sole test file。Written：declared actor evidence。
Deleted：無。ReadOnly：dev/source/docs/architecture/diagram/governance/README/VERSION/
舊 evidence與unlisted threads。Out-Of-Scope／Non-Goal：general interpreter/control flow/
iterable expansion、starred container alias、其他 callable inference、production runtime/API/backend/DI/
lifecycle、architecture/ACL、PR approval/merge/release/post-merge。
剩餘五 Human-only locks `jnBpk`/`4043480108`、`kQ95O`/`4060023123`、
`kqiZ5`/`4070096561`、`lAR8T`/`4078761998`、`lfQmF`/`4091213944`
保持 excluded/open。此前兩個 binding locks 僅依本 C40 exact scope 解除，不影響其他決策。
舊 rejected receipts 原樣 nonrouting，不覆寫／提交為本輪 evidence。
原 mission/scope/outcomes/Runtime Registry protocol/Architecture Visualization/follow-up missions 維持。

### Python implementation metadata（canonical python-implementation-plan profile）

- Async-planning status：exempt — synchronous static AST analysis；AsyncFor 不是新增 inference target，
  無 async runtime boundary、I/O/lifecycle/concurrency/timeout/retry/cancellation。
- Module/package placement：sole `tests/test_loaded_runtime_cache_bc_independence.py`。
- New public API：no。
- Interface changes：no，production Protocol contracts 不變。
- Breaking changes allowed：no，preserve既有 regression behaviors。
- New dependencies：no，existing ast/pytest/tooling only。
- Error-handling strategy：actual assertion failures交Tester，不改 production errors。
- Typing strategy：existing Python 3.12 strict test typing，不用 Any/cast/dynamic import/runtime inspection。
- Non-goals：no execution／general iterable inference；no starred-container alias；
  no AsyncFor/comprehension/generator inference；no source/API/architecture changes。
- Test categories：happy path（確定 literal bindings 的後續 forbidden use）；
  edge cases（tuple/list、star 前中後、prefix/suffix/attribute siblings）；
  failure paths（original two comment fixtures獨立 declared RED assertion failure）；
  forbidden behaviors（no fixture execution、no RHS-starred/unknown iterable inference、
  no rejection solely from unused callable）；
  regression preservation（non-star/default/walrus/getattr/semantic/direct imports/assertions）。

### Risks / Rollback

Risks：prefix/suffix indexing 錯誤、attribute sibling污染local map、starred-container/
RHS expansion誤推論、For binding 被當成即時 violation、unknown/async iterables被誤拒絕。
以 positional edge/unused/ordinary/empty/unpaired/unknown controls 與舊 regressions驗證；
independent review 檢查 literal-only bounds、existing resolver reuse與use-based detection。
Rollback：僅本五檔planning bounded repair，或 sole test path 新 immutable repair subject；
不得 broad reset、改 frozen predecessor原文scope或覆寫 evidence。Green needs-rework 須新
immutable S 重走 Tester/passing sole evidence/Independent Reviewer/sole review/alignment/classification。
舊 evidence與五Human locks保留。

### Artifact Paths / Status / Allowed Transitions / Implementation Steps

Plan-Creator feature worktree exact-five only：
`analysis/loaded-runtime-cache/requirements.md`、
`analysis/loaded-runtime-cache/technical-spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.plan.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.step.md`。
Implementer exact-five non-merge candidate-only commit → Independent Plan-Reviewer 唯一寫
`plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<c40-candidate-40-hex-sha>.json`。
Single object exact verdict/blocking_issues/copilot_feedback_triage；
verdict approved|needs-rework，blockers exact issue/file/fix nonempty string objects array
(approved空／needs-rework非空)，triage exact ADDRESS/DISCUSS/SKIP arrays。
Implementer 原樣 separate sole evidence-only approved receipt commit，Planner 才可route RED。

Implementer sole-test-path RED subject（new isolated assertions，未修detector）→
Tester collection/control/declared-failure evidence → Implementer sole failing evidence commit →
distinct sole-test-path green S → Tester actual scoped passing evidence →
Implementer sole passing evidence commit → Independent Reviewer same-S committed passing review →
Implementer sole approved review commit → Planner Phase4.5 → Plan-Creator factual plan/step alignment →
Implementer separate alignment commit/push → actual PR-head audit → Independent Reviewer exact-two
classification → Implementer sole classification commit/push → Planner exact actions →
Implementer specified replies/resolutions/live audit。
creator-in-progress→tester-in-progress→review-ready→reviewer-in-progress→approved|needs-rework；
approved→publish-in-progress→pr-open；needs-rework 要新S与完整 chain。
Human alone PR approval/merge/release/post-merge。

Tester 唯一寫
`plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<c40-red-subject-40-hex-sha>.json`
或 `plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<c40-green-subject-40-hex-sha>.json`。
Exact six keys schema_version/topic/implementation_subject_commit/status/commands/recorded_by；
integer1、loaded-runtime-cache、actual full lowercase40hex subject SHA、passing|failing、
nonempty array of exact command(nonempty string)/exit_code(integer) objects、Tester。
Passing 要全部actual0；failing至少一nonzero，RED需指定新增 assertion failure，
不可syntax/dependency/無關錯誤。Tester不commit；Implementer各自原樣separate sole commit。

Independent Reviewer僅消費committed passing same-greenS，唯一寫
`plan/loaded-runtime-cache/loaded-runtime-cache.implementation-review-log-<c40-green-subject-40-hex-sha>.json`。
Exact seven keys schema_version/topic/implementation_subject_commit/tester_evidence_commit/
verdict/blocking_issues/recorded_by：integer1、loaded-runtime-cache、same fullgreenS、
actual full sole passingTcommit、approved|needs-rework、stringarray(approved空／needs-rework非空)、
Independent Reviewer。Reviewer不commit；Implementer原樣separate sole commit。

### Validation / Acceptance / TestCase / Executable Commands

RED含兩 original comment fixtures各自 isolated source；
assignment tuple/list、star前中後、確定 prefix/suffix simple-name與attribute siblings；
For directtuple/list明列known forbidden elements及後續use。Controls：
unused callable bindings、ordinary/empty/unpaired targets、RHSstarred／unknown iterable、
AsyncFor/comprehension/generator 不新增inference拒絕；sys.modules獨立禁則仍測。
New tests names含 `c40`，forbidden cases另含 `rejects`，benign controls不含rejects。
在對應immutable subject實際執行：
- RED collection：`uv run --frozen pytest -p no:tach tests/test_loaded_runtime_cache_bc_independence.py -k c40 --collect-only -q`。
- RED controls：`uv run --frozen pytest -p no:tach tests/test_loaded_runtime_cache_bc_independence.py -k 'c40 and not rejects' -q`。
- RED declaredfailure：`uv run --frozen pytest -p no:tach tests/test_loaded_runtime_cache_bc_independence.py -k c40 -q`。
- Green scanner/runtime regressions：
  `uv run --frozen pytest -p no:tach tests/test_loaded_runtime_cache_bc_independence.py tests/test_loaded_runtime_cache_contracts.py -q`。
- Ruff：`uv run --frozen ruff check tests/test_loaded_runtime_cache_bc_independence.py tests/test_loaded_runtime_cache_contracts.py`。
- Strict Pyright：`uv run --frozen pyright tests/test_loaded_runtime_cache_bc_independence.py tests/test_loaded_runtime_cache_contracts.py`。
No:tach 保證明列tests真正執行；config reference `pyproject.toml` [tool.pytest.ini_options]、
[tool.pyright](Python3.12 strict)、[tool.ruff]/[tool.ruff.lint](py312/ALL)/testS101ignore。
Collection/control成功；RED actual declaredfailure；green全部actual0，
不預填results或擴config。

### Current-Head Classification / Reviewer Handoff / Unresolved Items

完整review/alignment/push與audit後 Independent Reviewer唯一寫fresh immutable
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-<c40-green-subject-40-hex-sha>-<actual-current-pr-head-40-hex-sha>.json`。
Exact eight keys schema_version/topic/implementation_subject_commit/tester_evidence_commit/
implementation_review_evidence_commit/pr_head_commit/classifications/recorded_by；
integer1、loaded-runtime-cache、actualfullsameS/solepassingT/soleapprovedV/auditedhead、
exacttwo-entryarray、Independent Reviewer。Entry exactthread/comment/outcome/reply，
string suffixIDs `nZI5n`/`4141010661`、`nZm9d`/`4141203134` 各一次，
outcome REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK；只有REPLY_AND_RESOLVE reply
nonempty factualstring，其餘JSONnull。Reviewer不commit，Implementer unchangedseparate sole
classification commit/push，Planner才routeexactpermitted replies/resolutions；ADDRESSboundedrepair、
HUMAN_CHECKopen。Planning approval不是threadactionauthority。
Wrong/staleSHA/head/binding/schema/pair/writer/order/nonsole/overwrite一律failclosed，
不得預填futureSHA/verdict/outcome/reply/resolution。

```json
{"verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]}}
```
兩 pairs 的 C40 repair/verification 與 exact actions 已完成，actual facts 見 C41；五Human-only保持open。

## C41 Current-Head Six-Pair Classification（completed predecessor routing）

### Goal / Outcome / Scope / Locked Decisions

Historical draft state：`c41-planning-draft`。僅在既有 passing／approved C40 subject 上，獨立分類以下
六個 exact suffix thread/comment pairs；不預填 outcomes／replies，也不因留言建議新增 implementation 要求。
固定 implementation subject `29db32481975381ef71c03ce616a32559963f323`、
passing Tester sole commit `020777486cf6b4acd6981e5d7ac542315ff19984`、
approved Independent Reviewer sole commit `25d2f96286b0f0b36432a1452cb3823bddf4cb9d`、
audited live PR head `36d7c96b19efded4b177dfd943647a05afcc872f`。
上述 S/T/V 是 same-topic／same-subject committed evidence，不建立新 RED／green subject 或重走 C40 chain。

| Thread suffix | Comment ID | Classification input（非預定 outcome／修復要求） |
| --- | --- | --- |
| `ndeMj` | `4142807469` | C39 tracker 與 committed facts 核對。 |
| `ndeMo` | `4142807482` | importlib.__import__ direct／imported／assigned aliases。 |
| `ndeMt` | `4142807492` | 三個 positional arguments 的 getattr default 建議。 |
| `n2sm3` | `4153137673` | Starred literal 確定 prefix／suffix 的 nested tuple/list binding 建議。 |
| `n2sm8` | `4153137682` | FunctionDef／AsyncFunctionDef foreign semantic definition names。 |
| `n2sm-` | `4153137690` | For literal 的多個 module bindings 與最後 element 覆寫問題。 |

C41 僅授權分類；既有 exact-two-positional-getattr 與 C40 direct-simple-name target
locks 不因 classification、ADDRESS、一般 Execution Authorized 或本 successor 自動解除。
若建議涉及 locked grammar／scope 變更，Planner 須保守判定 Human boundary，不可逕行實作。
五個 Human-only pairs `jnBpk`/`4043480108`、`kQ95O`/`4060023123`、
`kqiZ5`/`4070096561`、`lAR8T`/`4078761998`、`lfQmF`/`4091213944`
仍 excluded/open；不擴張其 classification／reply／resolve 權限。

### Committed Predecessor Facts / Tracking Alignment

C39 candidate `880e6c1e5ffcd4b707b46431975f0459c645e09a`、
approved planning receipt sole commit `358394d8f3feaf89ba430acb5c968f0398f328f0`、
classification sole commit `238fb87654507b7f44d230493e2e8e068166da5d`；
`ncxdC`/`4142518115` 已 reply `4142682597`／resolved，C39 tracker 已完成。
C40 candidate `077884842c5e97e27ea3ece914764096ff42afff`、
approved planning receipt sole commit `e030601e8cffdbb8a550d456caad61b3c06f327f`、
RED subject `a11f4b6f2ad364b2bc255397931657cce4eb568f`、
failing Tester sole commit `f3aeb5317f829f182c595967d491c666c2e5e92b`；
green S／passing T／approved V 如上，Phase 4.5 alignment 完成，
separate alignment commit／push `27cbddf7cff89f19fee5f8a5a4b4b06da133d84f`，
actual-head audit／exact-two classification sole commit／push
`36d7c96b19efded4b177dfd943647a05afcc872f`。
`nZI5n`/`4141010661` 已 reply `4153169815`／resolved；
`nZm9d`/`4141203134` 已 reply `4153172943`／resolved。
本輪唯讀 remote 核對三筆 isResolved=true／上述 reply IDs，且 PR #7
head 為上述 fixed head、MERGEABLE／CLEAN。
C39/C40 completed predecessor routing；早期 pending／current 字樣僅當時 frozen provenance，
C41 是 completed predecessor route，current route 見 C42；這些是已發生事實，不是未來 gate 的預填。

### Boundaries / Exclusions / Risks / Rollback

Goal／In-Scope：six-pair independent current-head classification 及上述 factual tracking alignment。
Modify：五個 standard planning artifacts。Written：declared independent planning／classification receipts。
ReadOnly：dev、source/tests/docs/diagram/governance、README/VERSION、舊 evidence 與 unlisted threads。
Deleted：無。Out-Of-Scope／Non-Goal：任何 implementation／RED／green、新 scanner grammar、
production API/runtime/backend/DI/lifecycle、architecture/ACL、PR approval/merge/release/post-merge。
原 mission、scope、outcomes、Runtime Registry protocol、測試策略、Architecture Visualization、
follow-up missions 不變；本 successor 無 stable-library／release 變更。
三個 existing untracked rejected receipts 保留原樣 nonrouting，不覆寫、不提交為本輪 evidence。
Risks：過時 tracking、stale head、錯誤 suffix/comment binding、把 ADDRESS 當成 locked-scope 寫入權限。
Rollback：只 bounded planning repair 或新的 immutable successor receipt route；不 broad reset、
不覆寫 committed evidence、不虛勾尚未分類／回覆／resolve 的本六筆。

### Status / Allowed Transitions / Artifact Paths / Actor Sequence

Plan-Creator 僅 feature worktree 修改
`analysis/loaded-runtime-cache/requirements.md`、
`analysis/loaded-runtime-cache/technical-spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.plan.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.step.md`。
Implementer exact-five non-merge candidate-only commit → Independent Plan-Reviewer 唯一寫
`plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<c41-candidate-40-hex-sha>.json`。
Single object exact verdict/blocking_issues/copilot_feedback_triage；verdict approved|needs-rework；
blockers 為 exact issue/file/fix nonempty string objects array（approved空／needs-rework非空）；
triage 為 exact ADDRESS/DISCUSS/SKIP arrays。
Implementer unchanged separate sole evidence-only commit approved receipt；Planner 核 fixed S/T/V
same-subject passing／approved／actual live head 後，Independent Reviewer 唯一寫 fresh immutable path：
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-29db32481975381ef71c03ce616a32559963f323-36d7c96b19efded4b177dfd943647a05afcc872f.json`。

Classification 為 single JSON object，exact eight keys schema_version/topic/
implementation_subject_commit/tester_evidence_commit/implementation_review_evidence_commit/
pr_head_commit/classifications/recorded_by；values integer1、loaded-runtime-cache、
上述 fixed full lowercase40hex S/T/V/head、exact six-entry array、Independent Reviewer。
每個 entry 恰 thread/comment/outcome/reply；thread/comment 均 string，上列 suffix/comment
各一次，不用 full PRRT IDs。Outcome REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK；
僅 REPLY_AND_RESOLVE reply 為 nonempty factual string，其餘 JSON null。
Reviewer 不 commit；Implementer unchanged separate sole evidence-only classification commit／bounded push；
Planner 才 route exact committed REPLY_AND_RESOLVE reply／resolve／live audit。
ADDRESS 回 Planner bounded repair 判定，不能解除 locks；HUMAN_CHECK 保持open。
Planning approval 不授權 thread action；C41 candidate／approved receipt 留 local 至 fixed-head classification
完成，不提前 push 改 remote head。分類後只含 planning／receipt 的 pushed descendants 不改 reviewed source；
若實際 reviewed head／S/T/V 不符，停止，由 Planner 判定新 immutable route，不能偷換 binding 或覆寫 receipt。
publish-in-progress 只可進 pr-open；Human alone PR approval／merge／release／post-merge。

### Validation / Acceptance / TestCase / Reviewer Handoff / Unresolved Items

核 committed fixed S/T/V、same-subject passing／approved、fresh path 不存在、
live head 精確一致、六個 pair／schema／writers／enum/nullability／sole commit／actor order。
Wrong/stale SHA/head、extra/missing key/pair、wrong writer、overwrite、非 sole evidence commit fail closed。
本輪不新增 implementation steps，不重跑或預填新的 Tester／Reviewer implementation evidence；
canonical C40 completed implementation 及既有 direct imports／fixtures／mocks／assertions 保留。
不預填 future candidate SHA／verdict／六筆 outcome／reply／resolution。
本六筆已獨立分類，permitted action／ADDRESS handoff／Human boundary facts 見 C42；no release／post-merge action。

```json
{"verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]}}
```

Workflow state：current_step=c41-plan-authoring；next_step=bounded-candidate-commit；
status=COMPLETE（historical draft handoff only，非 topic-complete）。

## C42 Bounded Scanner Repair（completed predecessor routing）

### C42 Committed Approval Facts / Phase 4.5 Alignment

Historical state：`c42-completed`。Actual committed candidate
`b24291c8b2e9fba9faecf202617cee04165030d0`；
approved Plan-Reviewer sole receipt commit `6d5937edfbe9b5f82e359e939860c2c0c356ec4c`；
RED subject `c9f1a21e84c9c8a19010cdeace24a16075e459c3`；
failing Tester sole commit `84cd02121104d1f8d44a100670d87918ae7b934d`；
green implementation subject `528de65144f0bdaf7a38831562b37f75fe8057ff`；
passing Tester sole commit `6eafc4b60f727f36539a9c17d32b3e4162b1d868`。
RED collection／benign controls actual exit0，declared RED regression command actual exit1；
same-green-subject passing Tester 已提交，scoped pytest／Ruff／strict Pyright 三項 actual exit0。
已核 immutable RED fixtures、green sole-test-path changes 與上述 committed evidence，
canonical 四項 implementation steps 已完成，僅用 C42 facts，不借 C40 evidence。
Committed review-ready alignment `ea40c746b960830c6d90dacdf9bf6c0d76611838` 後，
Independent Reviewer 已 approved，blocking_issues 空；
unchanged sole review evidence commit `307361d621fbad9f9eabd8373b6e38816a3a3cc4`，
綁定上述 same green S／committed passing T。Planner 已核 same-subject verification gate，
本 plan／step Phase4.5 factual alignment 完成。
Separate alignment commit／bounded push、actual-head audit／classification、sole classification
commit／push、exact reply／resolve 已完成；actual commits與reply IDs見C43 facts。
Scope、schemas、兩新增與五舊 Human-only locks 及三份 rejected untracked provenance 不變。


### Goal / Outcome / Scope / Locked Decisions

Historical draft state：`c42-planning-draft`。同一 static BC-independence scanner repair mission，
exact three pairs `ndeMo`/`4142807482`、`n2sm8`/`4153137682`、
`n2sm-`/`4153137690`。RED／green implementation sole path
`tests/test_loaded_runtime_cache_bc_independence.py`；不改 production source。
本契約只補下面三項漏檢，不建立 general interpreter 或新的 callable-possession 禁則。

1. `importlib.__import__`：與既有禁止動態匯入 callable 相同的 use semantics，
   辨識 direct module attribute、imported alias（含 renamed import）及 assignment-retained alias
   的後續 forbidden 使用。保留既有 direct/imported/assigned module aliases 與 callback-use 規則，
   不因單純持有未使用 callable 就新增拒絕；不擴 getattr arity／keywords／receiver／literal bounds。
2. Foreign semantic definition NAME：既有 BC ownership assertion 納入
   `ast.FunctionDef`／`ast.AsyncFunctionDef` 的 `name`；
   Loaded Runtime Cache 的 `ModelIdentity` 與 Identity 的 `RuntimeReuseKey`
   均視為該 BC 建立 foreign semantic binding。不是任意 string、attribute、parameter、
   reference／return expression 或普通函式名稱的語意推測。
   既有 class/type-alias/import/assignment/walrus semantic checks 保留。
3. Sync For finite known MODULE alternatives：僅既有 `ast.For` direct simple-name target、
   direct tuple/list literal 的明列 non-star elements，保留經既有 resolver 可確定的
   所有 known module alternatives（builtins/importlib/sys），不能只留下最後 element。
   同一 target 的有限已知 alternatives 與後續使用匹配：任一 alternative 與該 use
   構成既有 forbidden callable/module-cache surface 才依既有 detector 拒絕。
   Tuple/list、順序交換或 ordinary/unknown element 不得抹除已取得的 known alternative；
   單一 known element 維持原有行為。可由 Implementer 選有限集合表示或獨立 bounded resolver，
   但 observable semantics 固定為「保存所有可確定 alternatives，再作 existential forbidden-use 判斷」。
   不作 loop execution、source evaluation、general CFG、statement-order／branch feasibility 推論、
   arbitrary iterable 解析或 RHS starred expansion；不擴 AsyncFor/comprehension/generator inference。
   未使用的 module/callable binding 或沒有 forbidden use 的 ordinary/unknown bindings不新增拒絕。
   現存 independently forbidden `sys.modules` access 不因 unused controls 被壓制。

`ndeMt`/`4142807492` 三參數 getattr 與 `n2sm3`/`4153137673`
nested starred prefix/suffix pairing 保持 Human-check/open；
exact-two-positional-getattr 與 C40 starred direct-simple-name target locks 不變。
五個舊 Human-only pairs `jnBpk`/`4043480108`、`kQ95O`/`4060023123`、
`kqiZ5`/`4070096561`、`lAR8T`/`4078761998`、`lfQmF`/`4091213944`
亦 excluded/open。本三項 repair 不解除其他 locked decisions。

### C41 Committed Facts / Predecessor Alignment

C41 candidate `8af6b530ca750cff9a29522b04868db20eeac9bf`、
approved Plan-Reviewer sole receipt commit `eb884726c9b1ae7fbc392517940914780b4b7a73`、
six-pair classification sole commit／pushed head
`fa1ebe9a55cb8e2d3244ff488a2d4b48b865f6c7`。
Actual classifications：`ndeMj` REPLY_AND_RESOLVE，
`ndeMo`／`n2sm8`／`n2sm-` ADDRESS，
`ndeMt`／`n2sm3` HUMAN_CHECK。
`ndeMj`/`4142807469` 已 reply `4153327923`／resolved；
本輪唯讀 remote 核對 isResolved=true／該 reply ID，PR #7 head 為上述 pushed head，
MERGEABLE／CLEAN。C41 permitted action已完成、三ADDRESS交本C42、兩Human-check維持open，
故 C41 是 completed predecessor routing，不表示其 ADDRESS 已修復。
C39/C40 facts、evidence 與原 literal-only contract 保留；不重建或覆寫其 evidence chain。
C42 completed predecessor routing；current route見C43，舊 current／pending statements 是當時 frozen provenance。

### Boundaries / In-Scope / Out-Of-Scope / ReadOnly / Written / Deleted / Modify / Goal / Non-Goal

Goal／In-Scope：上述三項 scanner 漏檢與 meaningful RED／green／benign regression controls。
Modify：五份 standard planning artifacts；RED／green sole test path。
Written：下列各 actor 專屬 immutable receipts／evidence。
Deleted：無。ReadOnly：dev、production source、其他 tests、docs/architecture/diagram、
governance/contracts、README/VERSION/configuration、舊 evidence 與未列 threads。
Out-Of-Scope／Non-Goal：新增 getter grammar、nested starred alias pairing、general CFG／evaluation／
iterable expansion、任何 model/runtime/backend/DI/lifecycle/API／architecture/ACL、
PR approval／merge／release／post-merge。三份 existing rejected untracked receipts 原樣保留。
原 mission/scope/outcomes/Runtime Registry protocol/Architecture Visualization/follow-up missions 不變；
existing direct imports、fixtures、mocks、assertion behavior 及 current-source regressions 全部保留。
Fixtures 僅 ast static parsing，不能執行 fixture source、用動態 import 或 sys.modules substitution
繞過真正 direct-import regression；無 stable-library／release 變更。

### Python implementation metadata（本 bounded repair 的 canonical profile）

- Async-planning status：exempt — synchronous static AST analysis；AsyncFunctionDef 僅語法 name 檢查，
  不引入 async runtime boundary、I/O/resources/lifecycle/concurrency/cancellation/timeout/retry；
  AsyncFor/comprehension/generator 不擴 inference。
- Module/package placement：sole `tests/test_loaded_runtime_cache_bc_independence.py` existing scanner helpers。
- New public API：no。
- Interface changes：no，production Protocol／outcome contracts 不變。
- Breaking changes allowed：no，preserve existing regression behaviors與兩個新增Human locks。
- New dependencies：no，existing ast/pytest/tooling。
- Error-handling strategy：actual AST/assertion failures由Tester如實記錄，不改 production exceptions。
- Typing strategy：existing Python3.12 strict Pyright；finite known alternatives需明確 typed，
  不引入 Any/cast/dynamic import/source execution。
- Non-goals：no arbitrary iterable/CFG/branch feasibility；no getter-arity/nested-starred extension；
  no production API/runtime/architecture changes。
- Current Context／Requirements：既有 scalar module-alias map 會遺失 For multi-element alternatives；
  importlib.__import__ 不在 current forbidden callable membership；
  semantic definition scan 尚未涵蓋 FunctionDef/AsyncFunctionDef names。
  三者按上述固定語意補齊，不把任何 ADDRESS 建議當成無限擴張授權。
- Public Contract/API Changes：none。
- Affected Files：planning exact-five；implementation sole test path；evidence paths下列明列。
- Test Plan：Happy path（每 original fixture後續forbidden use獨立攔截）；
  Invalid input/failure paths（meaningful RED assertion failure，不以syntax/dependency error充數）；
  Edge cases（direct/imported/assigned aliases、兩BC/syncasyncdefinitions、
  tuple/list/multi/single/order-swapped module alternatives）；
  Regression（所有existing scanner/current-source與runtimecontract tests、directimports/fixtures/mocks/assertions）；
  Backward compatibility（unused／ordinary／unknown／RHSstarred／AsyncFor controls維持排除，
  exact-two getattr與directsimple target bounds維持）。
- Risks：alternative被scalar最後值覆寫、unordered集合錯誤取單一值、unknown branch消掉known、
  possession誤當use、foreign-name誤判string/attribute、擴至CFG／getter／nestedstarred。
- Rollback：只本五planning檔bounded repair，或 sole test path新的immutable repairsubject；
  不 broad reset、不改 C40 原contract、不覆寫舊 evidence。needs-rework 新S重走全部T/V sequence。

### Artifact Paths / Status / Allowed Transitions / Actor Sequence

Plan-Creator feature worktree exact-five only：
`analysis/loaded-runtime-cache/requirements.md`、
`analysis/loaded-runtime-cache/technical-spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.plan.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.step.md`。
Implementer exact-five non-merge candidate-only commit → Independent Plan-Reviewer唯一寫
`plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<c42-candidate-40-hex-sha>.json`。
Single object exact verdict/blocking_issues/copilot_feedback_triage；
approved|needs-rework；blockers exact issue/file/fix nonempty-string objects array，
approved空／needs-rework非空；triage exact ADDRESS/DISCUSS/SKIP arrays。
Implementer unchanged separate sole approved receipt commit，Planner才可route RED。

Implementer sole-test-path RED（新isolated assertions，尚未修scanner）→ Tester actual
collection/control/declared-failure evidence → Implementer sole failing evidence commit →
distinct sole-test-path green S → Tester actual scoped passing evidence →
Implementer sole passing evidence commit → Independent Reviewer same-S committed passing review →
Implementer sole approved review commit → Planner Phase4.5 → Plan-Creator factual plan/step alignment →
Implementer separate alignment commit/push → actual PR-head audit →
Independent Reviewer exact-three classification → Implementer sole classification commit/push →
Planner exact permitted actions → Implementer指定reply/resolve/liveaudit。
creator-in-progress→tester-in-progress→review-ready→reviewer-in-progress→approved|needs-rework；
approved→publish-in-progress→pr-open；needs-rework要新S及完整chain。
Human alone PR approval/merge/release/post-merge。

Tester唯一寫
`plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<c42-red-subject-40-hex-sha>.json`
或 `plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<c42-green-subject-40-hex-sha>.json`。
Exact six keys schema_version/topic/implementation_subject_commit/status/commands/recorded_by；
integer1、loaded-runtime-cache、actualfullsubject、passing|failing、
nonempty array of exact command(nonemptystring)/exit_code(integer) objects、Tester。
Passing全部actual0；failing至少一nonzero；RED必須新增指定assertionfailure，
不可syntax/dependency/無關failure。Tester不commit；Implementer每份原樣separate sole evidence commit。
Independent Reviewer僅消費committedpassing samegreenS，唯一寫
`plan/loaded-runtime-cache/loaded-runtime-cache.implementation-review-log-<c42-green-subject-40-hex-sha>.json`。
Exact seven keys schema_version/topic/implementation_subject_commit/tester_evidence_commit/verdict/
blocking_issues/recorded_by；integer1、loaded-runtime-cache、sameactualfullgreenS、
actualfullsolepassingTcommit、approved|needs-rework、stringarray(approved空／needs-rework非空)、
Independent Reviewer。Reviewer不commit；Implementer原樣separate soleapprovedreviewcommit。
不得預填任何futurecandidate/RED/green/evidence/headSHA、verdict、result、classification/reply/resolution。

### Validation / Acceptance / TestCase / Executable Commands

New tests names含 `c42`；forbidden regressions另含 `rejects`，benign controls不含rejects。
Each original comment fixture獨立覆蓋；importlib.__import__ direct/importedrenamed/assignmentalias、
unusedcallable和ordinarycontrol；兩BC的sync/asyncforeigndefinitionnames，
benignlocalnames與只含foreignstring/attribute的普通functionscontrols。
For tuple/list、importlib/builtins/sys既有knownmodule用例、moduleorder交換、
multi/singleelement、後續既有aliasuse，不僅最後element生效；
unused/ordinary/unknown/RHSstarred/AsyncFor controls及noexecution。
Independent sys.modules rule保留，不以unusedcontrol取消該既有禁則。
三posgetter與nestedstarred不能因本輪被當成新增拒絕；保留既有controls。

在各immutable subject實際執行：
- RED collection：`uv run --frozen pytest -p no:tach tests/test_loaded_runtime_cache_bc_independence.py -k c42 --collect-only -q`。
- RED controls：`uv run --frozen pytest -p no:tach tests/test_loaded_runtime_cache_bc_independence.py -k 'c42 and not rejects' -q`。
- RED declaredfailure：`uv run --frozen pytest -p no:tach tests/test_loaded_runtime_cache_bc_independence.py -k c42 -q`。
- Green scanner/runtime regressions：
  `uv run --frozen pytest -p no:tach tests/test_loaded_runtime_cache_bc_independence.py tests/test_loaded_runtime_cache_contracts.py -q`。
- Ruff：`uv run --frozen ruff check tests/test_loaded_runtime_cache_bc_independence.py tests/test_loaded_runtime_cache_contracts.py`。
- Strict Pyright：`uv run --frozen pyright tests/test_loaded_runtime_cache_bc_independence.py tests/test_loaded_runtime_cache_contracts.py`。
No:tach確保declaredtests真正執行；config authority `pyproject.toml`
[tool.pytest.ini_options]/[tool.pyright](Python3.12strict)/[tool.ruff]/[tool.ruff.lint](py312/ALL)/testS101ignore。
Collection/controls須actualsuccess、REDactualdeclaredassertionfailure、
green全部actual0；不預填outcomes，不改config以繞過checks。

### Current-Head Classification / Reviewer Handoff / Unresolved Items

完整greenverification/alignment/push與actualaudit後，Independent Reviewer唯一寫freshimmutable
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-<c42-green-subject-40-hex-sha>-<actual-current-pr-head-40-hex-sha>.json`。
Exact eight keys schema_version/topic/implementation_subject_commit/tester_evidence_commit/
implementation_review_evidence_commit/pr_head_commit/classifications/recorded_by；
integer1、loaded-runtime-cache、actualfullsameS/solepassingT/soleapprovedV/auditedhead、
exactthreeentryarray、Independent Reviewer。
Entry exactthread/comment/outcome/reply；stringsuffixIDs `ndeMo`/`4142807482`、
`n2sm8`/`4153137682`、`n2sm-`/`4153137690` 各一次。
Outcome REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK；
僅REPLY_AND_RESOLVE reply為nonemptyfactualstring，其餘JSONnull。
Reviewer不commit；Implementerunchangedseparate soleclassification commit/push；
Planner才routeexactcommittedpermittedreply/resolve，ADDRESSboundedrepair、HUMAN_CHECKopen。
Planning approval不授權thread actions。Wrong/stale SHA/head/topic/subject/pair/schema/writer/order/
nonsole/overwrite全部failclosed，不覆寫receipt，不跨topic借evidence。
Three pairs的C42 repair/verification與exactactions已完成，actualfacts見C43；七Human-only保持open。
所有 subject／evidence／candidate／PR-head bindings 均須 actual full lowercase 40-hex SHA，
禁止 abbreviated／symbolic／nonexistent／cross-subject bindings。

### Acceptance Criteria / Behavioral Scenarios / Error / Edge Cases

- Given `import importlib; importlib.__import__(...)` 或 imported／assigned alias，
  When scanner檢查後續forbiddenuse，Then辨識為既有dynamic-import substitution；
  unusedcallable不因持有而拒絕。
- Given runtime-cache AST `def ModelIdentity(...): ...` 或 Identity AST
  `async def RuntimeReuseKey(...): ...`（及兩BC對稱sync/async cases），
  When既有ownership assertion掃描definitionNAME，Then辨識foreignsemanticbinding；
  普通functionnames或foreignstring/attribute不算此新增declaration。
- Given `import importlib; import builtins; for loader in (importlib, builtins): ...`
  且loopbody後續使用 `loader.import_module(...)`（original conditional-use fixture），
  When scanner以所有確定knownmodulealternatives判定existingforbiddenuse，
  Thenimportlibalternative不能被尾端builtins覆寫，交換order／list亦同；
  不推論conditionalfeasibility，不因單純持有alternatives而拒絕。
- Unknown/arbitraryiterable／RHSstarred／AsyncFor不建立本輪新增inference；
  既有sys.modules禁則、exact-two getter、directsimple starredtarget與其他assertions保留。

```json
{"verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]}}
```

## C43 Current-Head Six-Pair Classification（completed predecessor routing）

### Goal / Outcome / Scope / Locked Decisions

Historical draft state：`c43-planning-draft`。僅對下列六個 exact suffix thread/comment pairs 建立
independent current-head classification；不新增 scanner grammar／code／architecture decisions，
不預填 outcome／reply／resolution。
固定 same-topic implementation subject `528de65144f0bdaf7a38831562b37f75fe8057ff`、
passing Tester sole commit `6eafc4b60f727f36539a9c17d32b3e4162b1d868`、
approved Independent Reviewer sole commit `307361d621fbad9f9eabd8373b6e38816a3a3cc4`、
audited live PR head `39e689ee482aa2277d158bf2dc9952369b0c03b1`。

| Thread suffix | Comment ID | Classification input（非預定 outcome／修復要求） |
| --- | --- | --- |
| `n23dL` | `4153205657` | C40 tracker 與 committed classification facts。 |
| `n23dS` | `4153205667` | C40 evidence ancestor-chain comment／current Git facts。 |
| `n23da` | `4153205676` | Known module __dict__ literal-lookup grammar 建議。 |
| `n23df` | `4153205681` | Registry／future runtime preparation integration boundary 建議。 |
| `n3P7r` | `4153360172` | C41 tracker 與 committed classification facts。 |
| `n3P71` | `4153360189` | Forbidden callable __call__ grammar 建議。 |

本輪分類不授權 __dict__ lookup／__call__ grammar 或 Registry preparation architecture實作；
ADDRESS 仍須 Planner bounded repair 判定，不解除 locked scope／ownership。
七個 Human-only pairs `ndeMt`/`4142807492`、`n2sm3`/`4153137673`、
`jnBpk`/`4043480108`、`kQ95O`/`4060023123`、
`kqiZ5`/`4070096561`、`lAR8T`/`4078761998`、`lfQmF`/`4091213944`
excluded/open；不因分類或一般 Execution Authorized 擴其權限。

### C40 / C41 / C42 Committed Facts / Tracking Alignment

C40 candidate `077884842c5e97e27ea3ece914764096ff42afff`、
approved planning receipt sole commit `e030601e8cffdbb8a550d456caad61b3c06f327f`、
RED `a11f4b6f2ad364b2bc255397931657cce4eb568f`、
failing T `f3aeb5317f829f182c595967d491c666c2e5e92b`、
green S `29db32481975381ef71c03ce616a32559963f323`、
passing T `020777486cf6b4acd6981e5d7ac542315ff19984`、
approved V `25d2f96286b0f0b36432a1452cb3823bddf4cb9d`、
alignment／push `27cbddf7cff89f19fee5f8a5a4b4b06da133d84f`、
classification sole commit／push `36d7c96b19efded4b177dfd943647a05afcc872f`；
`nZI5n`→reply`4153169815`、`nZm9d`→reply`4153172943` 均resolved。
C41 candidate `8af6b530ca750cff9a29522b04868db20eeac9bf`、
approved planning receipt sole commit `eb884726c9b1ae7fbc392517940914780b4b7a73`、
classification sole commit／push `fa1ebe9a55cb8e2d3244ff488a2d4b48b865f6c7`；
`ndeMj`→reply`4153327923` resolved，三 ADDRESS 修復交 C42、兩 HUMAN_CHECK 保持open；
C41 completed 只表示其 permitted actions／handoff 已完成，不虛勾 ADDRESS／HUMAN 需求。

C42 candidate `b24291c8b2e9fba9faecf202617cee04165030d0`、
approved planning receipt sole commit `6d5937edfbe9b5f82e359e939860c2c0c356ec4c`、
RED `c9f1a21e84c9c8a19010cdeace24a16075e459c3`、
failing T `84cd02121104d1f8d44a100670d87918ae7b934d`；
same green S／passing T／approved V 如上，
review-ready alignment `ea40c746b960830c6d90dacdf9bf6c0d76611838`，
Phase4.5 alignment／push `0e5d804777827122ebff2e3d757f572ceb028b83`，
actual-head audit／exact-three classification sole commit／push
`39e689ee482aa2277d158bf2dc9952369b0c03b1`。
`ndeMo`/`4142807482`→reply`4153739445`、
`n2sm8`/`4153137682`→reply`4153741053`、
`n2sm-`/`4153137690`→reply`4153743070`，均remote isResolved=true。
C42 verification與exact permitted actions已完成；C40/C41/C42 completed predecessor routing，
early pending/current 字樣是當時 frozen provenance，C43 completed，current route見C44。
核對時 PR #7 head為上述 audited head、MERGEABLE／CLEAN。

針對 `n23dS`，本輪 current Git 唯讀查證 C40 full S/T/V 均為上述 audited head ancestor：
三次 `git merge-base --is-ancestor <C40-full-S-or-T-or-V> 39e689ee482aa2277d158bf2dc9952369b0c03b1`
各 exit0。留言提及 `30b1e898…` 在 local 無可解析 commit，未取得完整 SHA／歷史 tree；
不猜 full SHA、parent、合法性或歷史結論。此為分類輸入，非預判 Reviewer outcome。
不得以 current ancestry 推論 unavailable historic revision 合法，也不重寫任何 evidence chain。

### Boundaries / Exclusions / Risks / Rollback

Goal／In-Scope：six-pair current-head classification 及上述 factual tracking alignment。
Modify：五份 standard planning artifacts。Written：declared independent planning／classification receipts。
ReadOnly：dev、source/tests/docs/diagram/governance、README/VERSION/configuration、
舊 evidence 與 unlisted threads。Deleted：無。
Out-Of-Scope／Non-Goal：implementation／RED／green、任何新 scanner grammar、runtime/API/backend/
DI/lifecycle、architecture/ACL、PR approval／merge／release／post-merge。
三份 rejected untracked receipts 保留原樣 nonrouting，不覆寫、不提交為本輪 evidence。
原 mission/scope/outcomes/Runtime Registry protocol/測試策略/Architecture Visualization/
follow-up missions 不變；無 stable-library／release 變更。
Risks：過時 tracking、stale head、錯誤 suffix binding、用 unavailable history 猜 verdict、
將 ADDRESS 誤認新 code／architecture 權限。
Rollback：bounded planning repair 或新 immutable successor route，不 broad reset、
不覆寫 evidence、不虛勾未執行的六筆分類／reply／resolve。

### Artifact Paths / Status / Allowed Transitions / Actor Sequence

Plan-Creator feature worktree exact-five：
`analysis/loaded-runtime-cache/requirements.md`、
`analysis/loaded-runtime-cache/technical-spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.plan.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.step.md`。
Implementer exact-five non-merge candidate-only commit → Independent Plan-Reviewer 唯一寫
`plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<c43-candidate-40-hex-sha>.json`。
Single object exact verdict/blocking_issues/copilot_feedback_triage；
verdict approved|needs-rework；blockers exact issue/file/fix nonempty string objects array，
approved空／needs-rework非空；triage exact ADDRESS/DISCUSS/SKIP arrays。
Implementer unchanged separate sole evidence-only approved receipt commit；
candidate／approved receipt 留 LOCAL，直到 fixed-head classification 寫完，不提前 push 改 remote head。
Planner 核 committed fixed S/T/V same-subject passing／approved及actual live head，
Independent Reviewer 唯一寫 fresh immutable exact path：
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-528de65144f0bdaf7a38831562b37f75fe8057ff-39e689ee482aa2277d158bf2dc9952369b0c03b1.json`。

Classification single JSON object，exact eight keys schema_version/topic/
implementation_subject_commit/tester_evidence_commit/implementation_review_evidence_commit/
pr_head_commit/classifications/recorded_by；
integer1、loaded-runtime-cache、上述fixedfull S/T/V/head、exactsixentryarray、Independent Reviewer。
所有candidate／subject／evidence／head bindings均actualfull lowercase40hex SHA，
禁止symbolic／abbreviated／nonexistent／cross-subject。
Entries exactthread/comment/outcome/reply；thread/comment string為上述suffix/comment各一次，
不用fullPRRT IDs；outcome REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK，
僅REPLY_AND_RESOLVE reply是nonemptyfactualstring，其餘JSONnull。
Reviewer不commit；Implementer unchangedseparate soleclassification commit／normalboundedpush，
Planner才可routeexactcommittedREPLY_AND_RESOLVE原樣factualreply／resolve／liveaudit。
ADDRESS返Planner boundedrepair判定；HUMAN_CHECK保持open。
Planning approval不是thread actionauthority；classification與reply／resolve是分離routes。
Push後僅planning／receipt descendants不改reviewedsource；actualhead或binding不符一律停Planner，
不可偷換fixedhead、覆寫receipt或推論newscope。
publish-in-progress只進pr-open；Human alone PRapproval／merge／release／post-merge。

### Validation / Acceptance / TestCase / Reviewer Handoff / Unresolved Items

核actualcommittedfixed S/T/V／same-subject passing／approved、freshpath不存在、
liveheadexact一致、sixpair/schema/writers/enum/nullability/solecommits/immutability/actororder。
Wrong/stalebinding、extra/missingkeys/pairs、wrongwriter、overwrite、nonsolecommit全部failclosed。
不新增implementationsteps／tests／T或V，不預填futurecandidateSHA／verdict／sixoutcomes/replies/resolutions。
canonicalC42四項completedimplementation與oldregressions/directimports/fixtures/mocks/assertions保留。
本六筆已分類且permittedactions完成，outcomes／openADDRESS及Humanfacts見C44；no release／post-mergeaction。

```json
{"verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]}}
```

Workflow state：current_step=c43-plan-authoring；next_step=bounded-candidate-commit；
status=COMPLETE（historical draft handoff only，非topic-complete）。

## C44 Current-Head Two-Pair Classification（completed predecessor routing）

### C44 Committed Completion Facts / Final Human-Check Alignment

Historical state：`c44-human-check`。C44 candidate `3a4adef853bd7ebb3561e0b4eeecfe25e8fc8d3f`、
approved Plan-Reviewer sole receipt commit `83257c3c5e0540d6808cdcecd76c1410a0828b5d`、
exact-two classification sole commit／push `d824243e255da5522c05685346ee35405d7af9cb` 已完成。
`n4SJW`/`4153779058`→reply`4154037586`、
`n4SJg`/`4153779072`→reply`4154039479`，均remote isResolved=true。
C43 classification sole commit `46406ee3451fc354565611640a542affae60c5ba` 與
`n23dL`→reply`4153895957`、`n23dS`→reply`4153897570`、
`n3P7r`→reply`4153899337` 的resolved facts再核一致。
本兩檔finalfactualalignment沿既有statealignment授權，不新candidate／receiptchain，
不改scope／grammar／architecture／source／tests／evidence。下方分類時fixedhead契約是frozen provenance；
current facts以本節actualcommittedrecords／liveaudit為準，非要求再做一輪classification。

As-of audit：`2026-10-01 09:49:52 UTC`（Asia/Taipei `2026-10-01 17:49:52`）。
PR #7 head `d824243e255da5522c05685346ee35405d7af9cb`，MERGEABLE／CLEAN。
Complete pagination取得100＋13 threads，末頁hasNextPage=false，latesttotalCount=113；
97 resolved／16 open。Audit開始時totalCount=112／15open，期間新增下列`n4_wT`；
如實記latestfacts，不把舊112snapshot當current。
剩餘16open為8Human-only＋2grammarADDRESS＋6尚未分類：
- Human-only：`jnBpk`/`4043480108`、`kQ95O`/`4060023123`、
  `kqiZ5`/`4070096561`、`lAR8T`/`4078761998`、`lfQmF`/`4091213944`、
  `ndeMt`/`4142807492`、`n2sm3`/`4153137673`、`n23df`/`4153205681`。
- Grammar ADDRESS：`n23da`/`4153205676` (__dict__ lookup)、
  `n3P71`/`4153360189` (__call__)；未實作，不虛勾完成或解除lockedscope。
- UNCLASSIFIED `n4uld`/`4153959185`：留言提出 `58ccea6d…` historic ancestry，
  未取得可核fullrevision／historicfacts，不猜合法性。
- UNCLASSIFIED `n4ulj`/`4153959197`：C43 tracker pending建議。
- UNCLASSIFIED `n4uln`/`4153959205`：IfExp finite branch module alternatives建議。
- UNCLASSIFIED `n4ulr`/`4153959210`：For/AsyncFor foreign semantic-name targets建議。
- UNCLASSIFIED `n4uly`/`4153959219`：reassignment stale alias／binding order建議。
- UNCLASSIFIED `n4_wT`/`4154067364`：audit期間新增C44 tracker alignment建議。

上述UNCLASSIFIED只是actualcomment inventory，沒有IndependentReviewer outcome，
不等同ADDRESS／HUMAN_CHECK／REPLY_AND_RESOLVE，不給reply／resolve或新grammar權限。
未因tracker已同步而resolve未分類thread，不追puretrackingcandidatechain、不推翻lockeddecision。
七先前locks與新增Registryarchitecturelock保持open；PR未merge，Humanreview／merge／release未完成。
Plan-Creator factualalignment已以 `b3d372d0cc8ae90d3269f09ffc88546a6acc8bf7` exact-two separatecommit／boundedpush完成；
該事實依C45核實，三份rejecteduntrackedprovenance原樣保留。


### Goal / Outcome / Scope / Locked Decisions

Historical draft state：`c44-planning-draft`。只分類 exact suffix pairs
`n4SJW`/`4153779058`（current C42 S/T/V ancestry facts，不追認 unavailable history）及
`n4SJg`/`4153779072`（current C42 tracker／committed classification／actions facts）。
不新增 implementation／grammar／architecture，未預填 outcomes／replies／resolutions。
固定 same-topic C42 implementation subject `528de65144f0bdaf7a38831562b37f75fe8057ff`、
passing Tester sole commit `6eafc4b60f727f36539a9c17d32b3e4162b1d868`、
approved Independent Reviewer sole commit `307361d621fbad9f9eabd8373b6e38816a3a3cc4`、
audited live PR head `46406ee3451fc354565611640a542affae60c5ba`。
不建立新 code／tests／Tester／implementation Reviewer subject。

### Committed Predecessor Facts / Tracking Alignment

C43 candidate `369dd7e3c48b1eeb49f71e0fcded338a54ac69e6`、
approved planning receipt sole commit `619b6260bb3c03a6f3ce532fbec314b2fb4a2987`、
six-pair classification sole commit／push `46406ee3451fc354565611640a542affae60c5ba`。
已執行 exact REPLY_AND_RESOLVE：
`n23dL`/`4153205657`→reply`4153895957`、
`n23dS`/`4153205667`→reply`4153897570`、
`n3P7r`/`4153360172`→reply`4153899337`，均 remote isResolved=true。
兩 ADDRESS `n23da`/`4153205676`（__dict__ lookup）、
`n3P71`/`4153360189`（__call__）仍待 bounded scope／grammar 處置；
`n23df`/`4153205681` Registry preparation architecture 為 HUMAN_CHECK/open。
C43 completed只表示classification／permittedactions／handoff完成，不把ADDRESS/HUMAN需求標完成。
C42 actual classification commit `39e689ee482aa2277d158bf2dc9952369b0c03b1`，
three replies/resolutions及completedtracker facts見C43，原C40/C41/C42 evidence／contract保留。
C43／C44皆completed predecessor；current route見C45。Early pending/current字樣是frozenprovenance。
本輪核對PR #7 head為上述auditedhead、MERGEABLE／CLEAN。

C42上述full S/T/V各自對auditedhead的
`git merge-base --is-ancestor <C42-full-S-or-T-or-V> 46406ee3451fc354565611640a542affae60c5ba`
actual exit0。留言的 `0cb9d842…` local無可解析commit，未取得fullSHA／historic tree，
不猜fullSHA／parent／合法性；currentancestry不能追認unavailablehistoricrevision。
此facts僅分類輸入，不是Reviewer outcome預填。

### Boundaries / Exclusions / Risks / Rollback

Goal／In-Scope：exact-two independent classification與已提交facts alignment。
Modify：五份standardplanningartifacts；分類／actions後的statealignment僅plan/step。
Written：declaredindependentplanning／classificationreceipts。Deleted：無。
ReadOnly：dev、source/tests/docs/diagram/governance、README/VERSION/configuration、
oldevidence與unlistedthreads。Out-Of-Scope／Non-Goal：任何newgrammar/code/architecture/runtime/
backend/DI/lifecycle/API、PRapproval/merge/release/post-merge。
八Human-only：`ndeMt`/`4142807492`、`n2sm3`/`4153137673`、
`n23df`/`4153205681`、`jnBpk`/`4043480108`、`kQ95O`/`4060023123`、
`kqiZ5`/`4070096561`、`lAR8T`/`4078761998`、`lfQmF`/`4091213944`
及上述兩grammarADDRESS均保持open，不因分類或generalexecution解除。
原mission/scope/outcomes/Registryprotocol/測試策略/ArchitectureVisualization/follow-ups不變，
無stable-library／release變更；三份rejecteduntrackedreceipts原樣nonrouting。
Risks：stalehead、錯pair、historicrevision猜測、tracking追逐新candidate、虛勾locked需求。
Rollback：boundedplanningrepair或必要newimmutableclassificationroute，不broadreset／覆寫evidence。

### Artifact Paths / Status / Allowed Transitions / Actor Sequence

Plan-Creator僅featureworktree exact-five：
`analysis/loaded-runtime-cache/requirements.md`、
`analysis/loaded-runtime-cache/technical-spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.plan.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.step.md`。
Implementerexact-five non-mergecandidate-onlycommit →
IndependentPlan-Reviewer唯一寫
`plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<c44-candidate-40-hex-sha>.json`。
Singleobjectexact verdict/blocking_issues/copilot_feedback_triage；approved|needs-rework；
blockers exactissue/file/fix nonemptystringobjectsarray(approved空/needs-rework非空)，
triageexactADDRESS/DISCUSS/SKIParrays。
Implementerunchangedseparate soleapprovedreceiptcommit；candidate／approvedreceipt留LOCAL，
直到fixedheadclassification寫完，不提前push改remotehead。
Planner核actualcommittedfixedsameS/T/V/passing/approved/livehead；
IndependentReviewer唯一寫freshimmutableexactpath：
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-528de65144f0bdaf7a38831562b37f75fe8057ff-46406ee3451fc354565611640a542affae60c5ba.json`。

SingleJSONobjectexacteightkeys schema_version/topic/implementation_subject_commit/
tester_evidence_commit/implementation_review_evidence_commit/pr_head_commit/classifications/recorded_by；
integer1、loaded-runtime-cache、上述fixedfull S/T/V/head、exacttwoentryarray、Independent Reviewer。
AllSHAactualfull lowercase40hex，不接受abbreviated/symbolic/nonexistent/crosssubject。
Entryexactthread/comment/outcome/reply，suffix/comment strings上述兩pair各一次，
不用fullPRRTIDs；outcomeREPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK，
只有REPLY_AND_RESOLVE reply為nonemptyfactualstring，其餘JSONnull。
Reviewer不commit；Implementerunchangedseparate soleclassificationcommit／normalboundedpush；
Planner才routeexactcommittedREPLY_AND_RESOLVE原樣reply／resolve／liveaudit。
ADDRESS回Plannerboundedscope判定；HUMAN_CHECK保持open。
Planningapproval不是threadactionauthority；分類與reply／resolve是不同routes。
Livehead／fixedbinding不符則停Planner，不偷換head或覆寫receipt。
Publish-in-progress僅進pr-open；Humanaloneapproval／merge／release／post-merge。

### Post-Classification Factual State Alignment / Human Boundary

沿Human既有「committedcandidate／receipt Gitfacts為routingauthority」與receipt後statealignment授權，
C44 classification solecommit／push及exactpermittedactions實際完成後，
Planner可routePlan-Creator僅改
`plan/loaded-runtime-cache/loaded-runtime-cache.plan.md`／
`plan/loaded-runtime-cache/loaded-runtime-cache.step.md`，
記actualclassificationcommit、outcomes、實際reply／resolve／auditfacts，
僅將真正完成actions標[X]；Implementer可separate statealignmentcommit／boundedpush。
該factualalignment不建立新candidate／Plan-Reviewerreceiptchain、不新增分類或scope權限。
沒有C44committedclassification及actualactionsfacts之前不得預勾。
完成後以Gitfacts進human-check，八locks與兩grammarADDRESS仍open；
若audit發現futureunclassifiedpairs，只如實列未分類，不冒稱已處理，
不為puretracking另外建立candidatechain，不推翻lockeddecision。
Human需要決定的remainingitems一次彙整，非自動mergeapproval。

### Validation / Acceptance / TestCase / Reviewer Handoff / Unresolved Items

核actualfixedsameS/T/V、passing／approved、freshpath、liveheadexact、
two pair/schema/writer/enum/nullability/immutable/solecommit/order。
Wrong/stalebinding、extra/missingkeys/pairs、overwrite、nonsolecommit全部failclosed。
CanonicalC42implementation與既有tests/directimports/fixtures/mocks/assertions保留，
本輪不新增implementationsteps／T/V，不預填futurecandidateSHA/verdict/outcomes/replies/resolutions。
兩pair的IndependentReviewer分類及exactactions已完成，actualfacts見本節finalalignment；所有remaininglocked／grammaritems保持open。
No release／post-mergeactions。

```json
{"verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]}}
```

## C45 Current-Head Seven-Pair Classification（completed predecessor routing）

C45 draft-time／pending／Current 字樣保留為 predecessor snapshot；已提交 final alignment
`36431ed89757d17a1965fda018b2fb028625b905` 與下方 C46 為 actual current routing，非 C45 未完成證據。

### Goal / Outcome / Scope / Locked Decisions

Current：`human-check`。C45 七筆 independent classification／sole commit／push 與三筆
permitted reply／resolve 已完成；remaining Human／ADDRESS／UNCLASSIFIED 保持 open。
以下保留七筆 input 與原 bounded contract，不授權任何 grammar／code／architecture 修改。

| Thread suffix（string） | Comment ID（string） | 分類輸入，非修復要求或預定 outcome |
| --- | --- | --- |
| `n4uld` | `4153959185` | 留言提及 historic `58ccea6d…` ancestry，僅依可核 facts 判斷，不猜歷史合法性。 |
| `n4ulj` | `4153959197` | C43 tracker／committed classification facts。 |
| `n4uln` | `4153959205` | IfExp finite branch module alternatives 建議。 |
| `n4ulr` | `4153959210` | For／AsyncFor foreign semantic-name targets 建議。 |
| `n4uly` | `4153959219` | Reassignment stale alias／binding order 建議。 |
| `n4_wT` | `4154067364` | C44 tracker／committed classification facts。 |
| `n5MVU` | `4154146529` | Import alias 的 local foreign semantic-name binding 建議。 |

固定同 topic／同 subject C42 green S `528de65144f0bdaf7a38831562b37f75fe8057ff`、
passing Tester sole commit `6eafc4b60f727f36539a9c17d32b3e4162b1d868`、
approved Independent Reviewer sole commit `307361d621fbad9f9eabd8373b6e38816a3a3cc4`、
audited live PR head `b3d372d0cc8ae90d3269f09ffc88546a6acc8bf7`。
本輪不建立新 implementation／Tester／implementation Reviewer subject；分類不是新的 code 設計。
既有 no-evaluation／bounded grammar／statement-order exclusions 不因 ADDRESS 或一般 Execution
Authorized 自動解除；任何需變更 locked scope 的 finding 仍交 Planner／Human 判定。

### Committed Predecessor Facts / Planning Priority

C44 candidate `3a4adef853bd7ebb3561e0b4eeecfe25e8fc8d3f`、
approved planning receipt sole commit `83257c3c5e0540d6808cdcecd76c1410a0828b5d`、
classification sole commit／push `d824243e255da5522c05685346ee35405d7af9cb`；
exact replies `n4SJW`→`4154037586`、`n4SJg`→`4154039479` 已 resolved，
C43 三筆 resolved facts 保留。C44 final plan／step factual alignment 已以 separate commit
`b3d372d0cc8ae90d3269f09ffc88546a6acc8bf7` 提交／推送，named diff 僅 plan／step。
C44 是 completed predecessor route（非所有 remaining requirements 完成），
其 `2026-10-01 09:49:52 UTC` audit snapshot 原樣作歷史事實，不冒稱本輪 current audit。
C45 唯一 current route；本七筆已由 immutable committed classification 分類，見下方 actual facts。

已存在 requirements／technical-spec，採 strict analysis priority；
本五檔同步同一 C45 contract，technical-spec 為 execution-facing authority，
requirements 保留 original mission／business intent guardrail，非新 topic。
Planning 時唯讀核 PR head 為上述 fixed head、MERGEABLE／CLEAN；七筆當時仍 open；
same-S passing Tester 三 commands exit0 與 approved independent review／空 blockers records 存在。
不以 current facts 追認 unavailable historic revision；無可核 full SHA／tree 時如實記未驗證交 Reviewer，
不猜 parent／ancestry／合法性，也不重寫其歷史或 evidence chain。

### Boundaries / In-Scope / Out-Of-Scope / ReadOnly / Written / Deleted / Modify / Non-Goal

In-Scope／Goal：exact-seven current-head classification 契約與 predecessor factual tracking alignment。
Modify：五份 standard planning artifacts；post-actions factual state alignment 僅 plan／step。
Written：下列 Independent Plan-Reviewer／Independent Reviewer 專屬 receipts。
ReadOnly：dev、production source／tests、docs／diagram／governance contracts、
README／VERSION／configuration、舊 evidence、未列 threads。Deleted：無。
Out-Of-Scope／Non-Goal：新 code／grammar／architecture；新 implementation／T／V chain；
backend／DI／runtime lifecycle／API／ACL；PR approval／merge／release／post-merge。
三份 rejected untracked receipts 原樣保留，不覆寫、不提交為本輪 evidence。
原 mission／scope／outcomes／Registry protocol／測試策略／Architecture Visualization／follow-ups 不變，
無 stable-library／release 變更。
八 Human-only `ndeMt`/`4142807492`、`n2sm3`/`4153137673`、
`n23df`/`4153205681`、`jnBpk`/`4043480108`、`kQ95O`/`4060023123`、
`kqiZ5`/`4070096561`、`lAR8T`/`4078761998`、`lfQmF`/`4091213944`
及兩 grammar ADDRESS `n23da`/`4153205676`、`n3P71`/`4153360189` 維持 open；
C45 不重新分類或解除這十筆。
既有 canonical Python metadata／C42 completed implementation steps 保留；
Async-planning status：exempt — 本輪只規劃分類／tracking，不改任何 async code／boundary／lifecycle。

### Status / Allowed Transitions / Artifact Paths / Actor Sequence

Plan-Creator 唯一 writer，僅 feature worktree exact-five：
`analysis/loaded-runtime-cache/requirements.md`、
`analysis/loaded-runtime-cache/technical-spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.plan.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.step.md`。
Implementer exact-five non-merge candidate-only commit → Independent Plan-Reviewer 唯一寫
`plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<c45-candidate-40-hex-sha>.json`。
Single object exact verdict／blocking_issues／copilot_feedback_triage；
verdict approved|needs-rework，blockers 為 exact issue/file/fix nonempty-string objects array
（approved 空／needs-rework 非空），triage exact ADDRESS/DISCUSS/SKIP arrays。
Implementer 原樣 separate sole evidence-only approved receipt commit；
candidate／approved receipt 留 LOCAL，直到 fixed-head classification 寫完，不提前 push 改 remote head。
Planner 核 same-topic／same-S committed passing T／approved V 與 actual live head，
Independent Reviewer 唯一寫 fresh immutable exact path：
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-528de65144f0bdaf7a38831562b37f75fe8057ff-b3d372d0cc8ae90d3269f09ffc88546a6acc8bf7.json`。

Receipt 必為 single JSON object，top-level 恰八 keys：
schema_version／topic／implementation_subject_commit／tester_evidence_commit／
implementation_review_evidence_commit／pr_head_commit／classifications／recorded_by。
Values：integer 1、loaded-runtime-cache、上述 fixed full S/T/V/head、
exact-seven-entry array、`Independent Reviewer`。
每 entry 恰 thread／comment／outcome／reply；thread／comment 為上表 suffix／comment strings 各一次，
不用 full PRRT IDs；outcome 為 REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK；
僅 REPLY_AND_RESOLVE reply 為 nonempty factual string，其餘 JSON null。
SHA bindings 均 actual full lowercase 40-hex，不接受 abbreviated／symbolic／不存在／cross-subject。
Reviewer 不 commit；Implementer 原樣 separate sole evidence-only classification commit／normal bounded push。
Planner 才 route exact committed REPLY_AND_RESOLVE 原文 reply／resolve／live audit；
ADDRESS 回 bounded scope 判定，HUMAN_CHECK 保持 open。
Planning approval 不授權 thread actions；classification 與 reply／resolve 是分離 routes。
若 fixed head／same-S binding／schema／pair／writer／order／fresh-path／sole-commit 不符，一律 fail closed；
不偷換 reviewed head、不覆寫 receipt、不跨 topic 借 evidence。Publish-in-progress 只可進 pr-open，
Human alone approval／merge／release／post-merge。

### Post-Actions Factual State Alignment / Human Boundary

C45 classification sole commit／push 與 exact permitted actions 實際完成後，
沿既有 Human state-alignment authority，Planner 可 route Plan-Creator 僅修改 plan／step，
記 actual committed receipt／outcomes／reply IDs／resolved／as-of audit facts，只標真正完成項 [X]；
Implementer separate factual-alignment commit／bounded push，不建立新 tracking candidate／receipt chain。
然後依 Git facts 進 human-check，一次彙整 remaining needs。
新 unlisted pairs 只如實 inventory／UNCLASSIFIED，不給 outcome／reply／resolve 權限，
不為 pure tracking 追新 candidate chain，不推翻 locked scope。
不得預填 C45 future candidate SHA／verdict／classification outcomes／reply／resolution／alignment commit。

### Validation / Acceptance / TestCase / Risks / Rollback / Unresolved Items

Acceptance：exact-five candidate、同 topic／同 S committed passing／approved evidence、
fixed live head、fresh immutable receipt、exact eight keys／seven entries／suffix string pairs、
enum／nullability／writers／actor sequence／unchanged sole commits 都可核。
Given 固定 evidence／head 與七筆 input，When independent classification，
Then 只產生七筆 factual outcomes；Given 未列或 locked item，Then 不新增處理權限。
Stale／unknown historical facts 只能如實未驗證，不猜歷史合法性。
無新增 implementation steps／tests／T／V；既有 direct imports／fixtures／mocks／assertions 保留。
Risks：stale head／錯誤 pairs、historic facts 推測、ADDRESS 被視為 scope 擴張、
tracking loop。Rollback：只 bounded planning repair 或必要 fresh immutable successor route；
不 broad reset、不覆寫／刪除 receipts，不更改既有實作與 locked decisions。
本七筆 independent classification 已完成；原八 Human-only／兩 grammar ADDRESS 保持 open，
另有三 ADDRESS／一 HUMAN_CHECK 與兩筆 unlisted inventory，均不授權修復或 resolve。
No release／post-merge actions。

```json
{"verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]}}
```

Workflow state：current_step=human-check；next_step=bounded-alignment-commit-push；
status=COMPLETE（factual draft handoff only，非 alignment commit／push 或 topic-complete）。

### C45 Committed Classification / Post-Actions Facts（as-of snapshot）

Candidate `9f0bd60c7d8dc43807771b1c93d9674f1c3da50e` exact-five；approved planning receipt
sole commit `996e1a6b0d5363954a4b560f7bff2e84efc06b42`；classification sole commit／push
`c45be35f8ef1d812e910c8726800a735a005a153`。Receipt 保留原 fixed S/T/V/head bindings；
C42 source／same-subject passing Tester／approved Independent Reviewer 未改，未新增 implementation chain。

| Pair | Committed outcome | Actual action／remaining state |
| --- | --- | --- |
| `n4uld/4153959185` | REPLY_AND_RESOLVE | Reply `4180760739` exists；resolved=true。 |
| `n4ulj/4153959197` | REPLY_AND_RESOLVE | Reply `4180761306` exists；resolved=true。 |
| `n4uln/4153959205` | ADDRESS | IfExp module alternatives，open；未授權 grammar 修復。 |
| `n4ulr/4153959210` | ADDRESS | For／AsyncFor foreign-name target syntax，open；未授權修復。 |
| `n4uly/4153959219` | HUMAN_CHECK | Ordered binding／scope invalidation，open；locked scope 未解除。 |
| `n4_wT/4154067364` | REPLY_AND_RESOLVE | Reply `4180761812` exists；resolved=true。 |
| `n5MVU/4154146529` | ADDRESS | Local import binding semantic name，open；未授權修復。 |

唯讀 live snapshot `2026-10-05 04:45:47 UTC`：PR head
`c45be35f8ef1d812e910c8726800a735a005a153`，MERGEABLE／CLEAN；完整 pagination 共 116 threads，
100 resolved／16 open = 9 HUMAN_CHECK（原八項加 n4uly）／5 ADDRESS（原兩項加本三項）／2 UNCLASSIFIED。
Unlisted `o6Apd/4180774145`、`o6Apj/4180774151` 僅 inventory，未分類／未回覆／未 resolve。
此 snapshot 固定 as-of，非未來零 open 保證；三份 rejected untracked receipts 原樣保留。
本次只對 plan／step 作 factual state alignment；其餘三份 planning artifacts 的 draft-time state
屬 committed candidate snapshot，不取代此欄 actual Git facts。不新增 tracking candidate／receipt chain。
Historical alignment separate commit／bounded push 已以
`36431ed89757d17a1965fda018b2fb028625b905` 完成；
其完成由 actual Git facts 判定，不新增自指 checkbox／追補 alignment loop。

## C46 Current-Head Five-Pair Classification（completed predecessor routing）

C46 pending／draft-time／Current 字樣保留 predecessor provenance；actual final alignment
`c0175a8627550a9bc01cdd05c859df70cb819856` 已提交／推送，下方 C47 唯一 current route。

### Goal / Outcome / Scope / Locked Decisions

Current：`human-check`。C46 exact-five 獨立分類／sole commit／push 與唯一 permitted
reply／resolve 已完成；下列保留原分類 input／bounded contract，actual outcomes 見本節末。
Remaining HUMAN_CHECK／ADDRESS 保持 open，不授權 code／grammar／architecture 修改。

| Thread suffix（string） | Comment ID（string） | 分類輸入，非修復要求／預定 outcome |
| --- | --- | --- |
| `o6Apd` | `4180774145` | C45 tracker 與已提交分類狀態是否一致。 |
| `o6Apj` | `4180774151` | 同步 comprehension 的 literal alias／既有 benign control 建議。 |
| `o6M73` | `4180852189` | 巢狀 tuple/list For target 的 module alias 建議。 |
| `o6M75` | `4180852193` | With／AsyncWith optional_vars foreign semantic-name 建議。 |
| `o6M76` | `4180852196` | RuntimeRegistry backend semantic kind／architecture evidence 建議。 |

Fixed C42 S `528de65144f0bdaf7a38831562b37f75fe8057ff`，
passing Tester sole commit `6eafc4b60f727f36539a9c17d32b3e4162b1d868`，
approved Independent Reviewer sole commit `307361d621fbad9f9eabd8373b6e38816a3a3cc4`，
audited PR head `36431ed89757d17a1965fda018b2fb028625b905`。
Planning 時五筆 open、source unchanged、S/T/V ancestors 與 fresh receipt path 已由 Planner preflight 核實；
不得偷換 reviewed head，也不得以 unavailable historic SHA 推測歷史合法性。

### Predecessor Facts / Analysis Priority / Boundaries

C45 candidate `9f0bd60c7d8dc43807771b1c93d9674f1c3da50e`、
approved receipt sole commit `996e1a6b0d5363954a4b560f7bff2e84efc06b42`、
classification sole commit／push `c45be35f8ef1d812e910c8726800a735a005a153`，
三筆 replies `4180760739`／`4180761306`／`4180761812` 已 resolved。
C45 exact-two final factual-alignment commit／push
`36431ed89757d17a1965fda018b2fb028625b905` 已完成；C45 是 completed predecessor route，
非所有 remaining requirements 完成。其 2026-10-05 04:45:47 UTC snapshot 保留為 as-of 歷史事實，
不冒稱 C46 current thread total；old pending／draft labels 僅 provenance，C46 為唯一 current route。
Existing requirements／technical-spec 均存在，採 strict analysis priority；五檔同步此 bounded contract，
technical-spec 是 execution-facing authority，requirements 保留 original mission／business-intent guardrail。
不改 original mission／scope／outcomes／Registry protocol／tests／Architecture Visualization／follow-ups。

In-Scope／Goal：exact-five classification 契約與既有 C45 actual facts alignment。
Modify：五份 standard planning artifacts；post-actions alignment 僅 plan／step。
Written：下列各獨立 writer 專屬 immutable receipts。Deleted：無。
ReadOnly：dev、production source／tests、docs／architecture／diagram／governance、
README／VERSION／configuration、既有 receipts／evidence、未列 threads。
Out-Of-Scope／Non-Goal：code／grammar／architecture 修改；新 implementation／Tester／V；
backend／DI／runtime lifecycle／API／ACL；PR approval／merge／release／post-merge。
原 9 HUMAN_CHECK（八 locks 加 `n4uly/4153959219`）與 5 ADDRESS（原
`n23da/4153205676`、`n3P71/4153360189` 加 `n4uln/4153959205`、
`n4ulr/4153959210`、`n5MVU/4154146529`）保持 open，不在本五筆重新分類／解除。
ADDRESS 不擴張授權；grammar／statement-order／architecture locks 必須保守交 Planner／Human。
三份 rejected untracked receipts 原樣保留，不覆寫／刪除／提交，不作 routing evidence。
No stable-library surface／release timing change；README／VERSION 無變更。

### Artifact Paths / Status / Actor Sequence / Receipt Contracts

Plan-Creator 唯一 writer，只在 feature worktree 修改 exact-five：
`analysis/loaded-runtime-cache/requirements.md`、
`analysis/loaded-runtime-cache/technical-spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.plan.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.step.md`。
Implementer exact-five non-merge candidate-only commit，candidate 保持 LOCAL；
Independent Plan-Reviewer 唯一寫 candidate SHA-bound fresh immutable path
`plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<c46-candidate-full-40-hex-sha>.json`。
Single object 恰 verdict／blocking_issues／copilot_feedback_triage；
verdict approved|needs-rework；blocking_issues 為 exact issue/file/fix nonempty-string objects array，
approved 空／needs-rework 非空；triage 恰 ADDRESS/DISCUSS/SKIP arrays。
Candidate SHA 只能在 actual commit 後填入 path，不預填 future SHA／approval。
Implementer 原樣 approved receipt separate sole evidence-only commit，保持 LOCAL；
needs-rework 不能 route classification；回 Planner，不 self-close candidate。
Planner 核 same-topic／same-S passing T／approved V 與 fixed live head 後，
Independent Reviewer 唯一寫 fresh immutable path：
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-528de65144f0bdaf7a38831562b37f75fe8057ff-36431ed89757d17a1965fda018b2fb028625b905.json`。

Classification single JSON object，top-level 恰八 keys：
schema_version／topic／implementation_subject_commit／tester_evidence_commit／
implementation_review_evidence_commit／pr_head_commit／classifications／recorded_by。
Values 分別 integer 1、loaded-runtime-cache、上述 fixed S/T/V/head、
exact-five array、`Independent Reviewer`。各 entry 恰 thread／comment／outcome／reply；
thread／comment 恰上述 suffix／ID strings，各一次，不使用 full PRRT IDs；
outcome REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK。僅 REPLY_AND_RESOLVE 的 reply
為 nonempty factual string；ADDRESS／HUMAN_CHECK reply 必為 JSON null。
全 SHA 為 actual lowercase 40-hex；missing／extra keys、pair／binding／head／writer／order／fresh path
或 sole-commit 不符即 fail closed，不覆寫任何 receipt，不跨 topic 借 evidence。
Reviewer 不 commit；Implementer 原樣 classification separate sole evidence-only commit，
之後 normal bounded push（候選／approved receipt 不提前 push 改變 fixed live head）。
Planner 才 route committed REPLY_AND_RESOLVE exact original reply／resolve／live audit；
ADDRESS／HUMAN_CHECK 保持 open，需修復另經 bounded scope 判定，非本分類直接實作。
Planning approval 非 thread-action authority；Q／classification 非 Human PR approval。
Publish-in-progress 只能 pr-open；Human-only merge／release／post-merge 不授權。

### Post-Actions Alignment / Validation / TestCase / Human Boundary

Exact permitted actions 實際完成後，Plan-Creator ONLY plan／step 記 actual candidate／receipt
commits、outcomes、reply IDs／resolved、固定一次 as-of full-pagination snapshot；
只將真正完成項標 [X]。Implementer separate exact-two factual-alignment commit／bounded push，
不新增 tracking candidate／receipt chain，不預填自我 SHA 或未完成 publish。
Final alignment commit／push 以 actual Git facts 判定，不建立自指 checkbox／補 commit 循環。
然後 human-check，一次彙整 remaining needs；new unlisted pairs 只 inventory／UNCLASSIFIED，
不追加 classification／reply／resolve 權限，不等待新 bot comments 追無限 snapshot。

Given same-S committed passing／approved evidence、fixed head、exact-five input，
When Independent Reviewer classification，Then 只產生五筆符合 exact schema 的 factual outcomes。
Given stale head／不明 historic facts／未列 thread，Then fail closed／如實未驗證／inventory-only，
不得推測合法性或擴張 scope。無新 tests／RED／green／Tester／implementation review；
canonical C42 four implementation steps 與 direct imports／fixtures／mocks／assertions 原樣保留。
Validation commands：`git diff --check`；
`python .agents/skills/plan-step-tracker/scripts/step_tracker.py check_impl_steps_succeeded loaded-runtime-cache`；
各角色依 actual Git facts 核 candidate exact-five、sole receipts、full SHA ancestry／source unchanged，
並以唯讀 PR head 與 thread pagination 核對 fixed head／exact actions。
Async-planning status：exempt — classification／factual tracking-only，沒有 async code／lifecycle／concurrency 變更。
七項 decisions 均 unchanged：不新增模組／public API／interface／breaking change／dependency；
error handling 是 schema／binding／route fail closed，不改 Python exception boundary；
typing 是固定 JSON string／integer／array／nullability，不改 Python annotations。
TestCase categories：happy exact-five、invalid schema/binding、edge stale head／historic unknown、
regression original locks／evidence unchanged、backward compatibility API／tests untouched。
Risks：stale head、ADDRESS 被誤作修復授權、draft-time provenance 冒作 current state、tracking loop。
Rollback：只 bounded planning repair 或必要 fresh immutable successor；不 broad reset、
不覆寫 receipts，不修改既有實作／locked decisions。
Unresolved：五筆分類已完成；原 9 HUMAN_CHECK／5 ADDRESS，加本三 HUMAN_CHECK／一 ADDRESS，
均 open。未列新 pairs inventory-only；本 fixed snapshot 無新增 unlisted。本輪無 release／post-merge actions。

Reviewer Handoff：
```json
{"verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]}}
```
Workflow state：current_step=human-check；next_step=bounded-alignment-commit-push；
status=COMPLETE（factual-alignment draft handoff only，非自身 commit／push／topic-complete）。

### C46 Committed Classification / Post-Actions Facts（fixed as-of snapshot）

Actual exact-five candidate `dd1d78f6be0903aa1576d1350ac88311da836148`；
approved planning receipt sole commit `40d7cc3d144be466acc914171dc817670b7ebb6f`；
classification unchanged sole commit／normal push `296232ccb70b8346c392894e58aa07722c8bccd8`。
Receipt 原 fixed C42 S/T/V 與 reviewed head `36431ed89757d17a1965fda018b2fb028625b905`
保持不變；不以後續 publish head 偷換 reviewed head，source／tests／implementation evidence 未改。

| Pair | Committed outcome | Actual action／remaining state |
| --- | --- | --- |
| `o6Apd/4180774145` | REPLY_AND_RESOLVE | 原 receipt reply 已發布，reply ID `4181279778`，resolved=true。 |
| `o6Apj/4180774151` | HUMAN_CHECK | Comprehension literal alias scope，open；既有 grammar lock 未解除。 |
| `o6M73/4180852189` | HUMAN_CHECK | Nested For target inference，open；direct simple-name target lock 未解除。 |
| `o6M75/4180852193` | ADDRESS | With／AsyncWith foreign semantic-name syntax，open；本輪不授權修復。 |
| `o6M76/4180852196` | HUMAN_CHECK | RuntimeRegistry architecture semantic kind，open；architecture ownership／locked decision 未解除。 |

Planner 已核固定 audit snapshot `2026-10-05T06:31:52Z`：119 threads，
101 resolved／18 open = 12 HUMAN_CHECK（原九項＋o6Apj／o6M73／o6M76）
／6 ADDRESS（原五項＋o6M75），沒有新增 unlisted pairs。
本 snapshot 固定 as-of，非未來零 open 保證；不等待 bot 追新 audit。
Completed classification／permitted action 不代表 open requirements／Human PR review／merge 已完成。
Current／step phase 為 human-check；其餘三份 planning artifacts 保留 committed candidate snapshot，
本 plan／step actual facts 不改其契約，不建立新 tracking candidate／receipt chain。
本次僅 exact-two factual-alignment draft；尚由 Implementer separate commit／bounded push，
不預填自身 alignment SHA／不宣稱已提交，不新增自指 completion checkbox。
三份 rejected untracked receipts 原樣保留，無新 code／grammar／architecture／contract 變更。

## C47 Bounded Six-Pair Scanner Repair（completed predecessor routing）

C47 draft-time／pending／Current字樣保留當時provenance；finalexact-twoalignment
`ad175fb5d4e3167a30c3d4aad922a8357a401430` 已提交／推送，下方C48唯一currentroute。

### Goal / Outcome / Scope / Locked Decisions

Current：`human-check`。新 same-S approval／Phase4.5 normal publish／exact-seven classification
與六 permitted reply／resolve已完成，既有 PR #7 pr-open；十二 Human locks＋o7gvv ADDRESS仍open，非merge approval。
Human 授權此同-topic bounded repair successor；只修下列六 ADDRESS，
RED／green sole implementation path `tests/test_loaded_runtime_cache_bc_independence.py`。
不更動 production API／BC contract；修復後必須完整新的 immutable S／T／V chain，
C42 passing evidence 只作 predecessor provenance，不為 C47 新 subject 背書。

| Pair（suffix／comment strings） | 授權 bounded repair，非已完成 outcome |
| --- | --- |
| `n23da/4153205676` | Known module.__dict__[direct string literal] forbidden import-callable lookup 的後續 USE。 |
| `n3P71/4153360189` | Known forbidden import-callable.__call__ 的後續 USE。 |
| `n4uln/4153959205` | Existing IfExp 兩 branch 的 finite known module alternatives＋existential forbidden USE。 |
| `n4ulr/4153959210` | For／AsyncFor foreign semantic-name TARGET syntax，非 runtime alias inference。 |
| `n5MVU/4154146529` | Import 的 LOCAL foreign semantic-name binding，保留原 source-name 禁則。 |
| `o6M75/4180852193` | With／AsyncWith optional_vars foreign semantic-name TARGET syntax。 |

另 `o7gvv/4181373623`（function／lambda parameter-name 建議）ONLY 在新的 passing S/T/V
與 actual published head 後獨立分類；不加入 RED repair requirement，不擴 semantic detector 至 parameters。

Observable semantics：
1. Namespace lookup 僅 known module receiver 的 `.__dict__` 與 direct string literal key，
   辨識 existing forbidden import-callable surface，沿既有確定 alias／subsequent USE 規則。
   Unknown receiver、dynamic key、generic namespace／ordinary entry 不新增 inference／拒絕；
   只持有未使用 forbidden callable 不因本輪新增拒絕，existing sys.modules 禁則獨立保留。
2. `.__call__` 只在 receiver 已是 known forbidden import callable 時納入既有 USE 判定；
   不把任意 attributes 或普通 callable 的 __call__ 視為 forbidden，不以 possession 代替 USE。
3. IfExp 只擴既有 finite known module alternatives 保存，兩 branch 不能 tail／first-value 覆蓋另一
   known alternative；ordinary／unknown branch 不抹除已確定 known alternative。
   判斷固定為「任一 finite known alternative 與該後續 use 組成 existing forbidden surface」，
   不評估 condition／branch feasibility，不推論 CFG、binding order 或 lexical scope invalidation。
   Representation 可有限集合／bounded contexts／bounded resolver，由 Implementer 選；不是 general interpreter。
4. For／AsyncFor 只在 semantic ownership check 掃 TARGET，沿既有 Name／Tuple／List／Starred
   traversal，忽略 Attribute。這不擴 callable/module aliases、iterable parsing 或 async execution。
5. Import／ImportFrom 的 LOCAL binding 使用 asname（若有），無 asname 的 Import 用 name first segment，
   ImportFrom 用 imported name；兩 BC 的 foreign semantic local names 均被攔截。
   Existing Identity BC ModelIdentity source-name import 禁則保留，即使 renamed local alias 也不得弱化。
   不從 dotted attribute／任意 string／foreign source spelling 猜 type semantics。
6. With／AsyncWith 只掃 each optional_vars TARGET，相同既有 target-name traversal；
   absent optional_vars／ordinary name／attribute target benign，不求值 context manager 或返回值。
本輪所有 fixtures 僅 AST 靜態 parse；不 exec／eval source，不解析 arbitrary iterable。

### Predecessor Facts / Analysis Priority / Boundaries

Baseline actual head `c0175a8627550a9bc01cdd05c859df70cb819856` 是 C46 exact-two
final factual-alignment commit／push；Planner 已核 local／origin／PR 一致、OPEN／MERGEABLE／CLEAN，
tracked／index clean（只有原三 rejected untracked），snapshot 120 threads／101 resolved／19 open。
C46 candidate `dd1d78f6be0903aa1576d1350ac88311da836148`、
approved receipt sole `40d7cc3d144be466acc914171dc817670b7ebb6f`、
classification sole／push `296232ccb70b8346c392894e58aa07722c8bccd8`，
唯一 original reply `4181279778` 已 resolved；C46 是 completed predecessor，不等於全部需求完成。
C42 S `528de65144f0bdaf7a38831562b37f75fe8057ff`、T
`6eafc4b60f727f36539a9c17d32b3e4162b1d868`、V
`307361d621fbad9f9eabd8373b6e38816a3a3cc4` 作 immutable history，
C47 必須建立自己的 RED／green subject、Tester、Independent Reviewer。
Existing analysis 兩檔存在，採 strict priority；technical-spec execution-facing authority，
requirements 是 original mission／business guardrail，五檔同步此明確 Human authorized C47 scope。
C47 唯一 current route；early draft-time／pending／Current 字樣是 frozen nonrouting provenance。

Goal／In-Scope：上述六項 bounded scanner repair、meaningful RED／green controls、完整驗證鏈，
及後續 exact-seven classification（六 repair pairs＋o7gvv ONLY classify）。
Modify：planning exact-five／RED-green sole test path；review-ready／Phase4.5／final factual alignment 僅 plan／step。
Written：下列角色各自的 fresh immutable evidence。Deleted：無。
ReadOnly：dev、production source、其他 tests（runtime contracts 只驗證不改）、architecture／diagrams／docs、
README／VERSION、governance／repository contracts、configuration、舊 evidence／未列 threads。
Out-Of-Scope／Non-Goal：production API／runtime／backend／DI／lifecycle／ACL；
getter arity／nested/starred/For alias grammar／comprehension／ordered scope；
architecture／README／ownership／renderer；function／lambda parameters semantic-detector；
PR approval／merge／release／post-merge。Original mission／outcomes／Registry reuse protocol／
Architecture Visualization／follow-ups 保持不變，existing direct imports／fixtures／mocks／assertions 不替換。
三 rejected untracked 原樣保留，不覆寫、不刪除、不提交作本輪 evidence。
No stable-library surface／release-timing 變更，README／VERSION 不動。

原十二 HUMAN_CHECK 全保持 open，不重開決策：
`ndeMt/4142807492`、`n2sm3/4153137673`、`n23df/4153205681`、
`jnBpk/4043480108`、`kQ95O/4060023123`、`kqiZ5/4070096561`、
`lAR8T/4078761998`、`lfQmF/4091213944`、`n4uly/4153959219`、
`o6Apj/4180774151`、`o6M73/4180852189`、`o6M76/4180852196`。
AsyncFor semantic TARGET syntax 不解除 AsyncFor alias-inference lock；
nested semantic TARGET traversal 不解除 nested For／starred alias-inference lock。
既有 exact-two-positional／no-keyword／known receiver／direct literal getattr bounds 不變。
未列新 threads inventory-only；任何 scope 矛盾交 Planner／Human，不補設計。

### Python Implementation Metadata（C47 current bounded profile）

- Async-planning status：exempt — synchronous static AST scanner，AsyncFor／AsyncWith 只 TARGET 語法；
  無 async boundary／I/O／lifecycle／concurrency／timeout／cancellation／retry，不推 async aliases。
- Module/package placement：existing helpers in sole `tests/test_loaded_runtime_cache_bc_independence.py`。
- New public API：no。Interface changes：no。Breaking changes allowed：no。
- New dependencies：no（既有 ast／pytest／project tooling）。
- Error handling：保留 existing assertion／parse／unexpected error 行為；evidence 依 actual exit code，
  未通過 checks fail closed，不能以 syntax／dependency error 冒作 RED；不改 production exception boundary。
- Typing：Python3.12／existing strict Pyright，finite alternatives 明確 typed；不引入 Any／cast、
  dynamic import 或 sys.modules substitution 作迴避手段。
- Non-goals：no general CFG／arbitrary iterable／branch evaluation；no getter／comprehension／ordered scope
  或 parameter-name extension；no production／architecture／README／contract／backend changes。
- Current Context／Requirements：現有 alias resolver 缺 namespace／__call__，IfExp module resolution 可丟另一
  branch；foreign semantic detector 缺 For／AsyncFor、import local binding、With optional_vars。
  六項依固定 bounded semantics 補齊，USE-based detector 不改成 callable possession 禁令。
- Public Contract／API Changes：none；Affected Files：exact-five planning、sole test implementation、
  fresh immutable evidence paths 見下；其餘 files 只有明列 read-only verification。
- Test Plan：Happy path（每六 original finding isolated forbidden use／semantic target rejects）；
  Invalid input／failure（RED meaningful新增 assertion failure，malformed fixture/dependency failure不算）；
  Edge（known aliases／direct literal key／__call__／IfExp both branch order／known＋unknown／
  兩 BC／For AsyncFor／With AsyncWith／nested syntactic targets／import aliases/noaliases）；
  Regression（既有 direct-import／fixture／mock／assertions、current-source boundary 與 runtime tests）；
  Backward compatibility（unknown receiver／dynamic key／ordinary namespace／callable／unused possession、
  attribute targets／普通localname／任意strings及十二 locks controls 不新增拒絕）。
- Risks：possession 被誤作 USE、branch known alternative被覆蓋、semantic TARGET 語法誤作 runtime
  inference、原 source-name禁則被 local binding repair 弱化、parameters scope drift、錯綁舊 C42 evidence。
- Rollback：僅 standard-five bounded planning repair／sole test path 新 immutable repair subject；
  needs-rework 新 S 重走完整 RED／green／Tester／independent Reviewer sequence；
  不 broad reset，不覆寫／刪除 evidence，不修改已鎖 architecture／contract。

### Artifact Paths / Status / Actor Sequence / Immutable Evidence

Plan-Creator 唯一 planning writer，feature worktree exact-five：
`analysis/loaded-runtime-cache/requirements.md`、
`analysis/loaded-runtime-cache/technical-spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.plan.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.step.md`。
Implementer exact-five non-merge candidate-only commit（LOCAL）→ Independent Plan-Reviewer
sole writer fresh candidate-bound
`plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<c47-candidate-full-40-hex-sha>.json`。
Single object exact verdict／blocking_issues／copilot_feedback_triage；
approved|needs-rework；blockers exact issue/file/fix nonempty-string objects array，
approved 空／needs-rework 非空；triage exact ADDRESS/DISCUSS/SKIP arrays。
Implementer unchanged approved receipt sole evidence-only commit（LOCAL）；Planner 才 route RED。
不預填 candidate SHA／verdict；needs-rework 回 Planner，不 self-select／self-close candidate。

Implementer sole-test RED new assertions（scanner 不改）→ independent Tester actual collection／controls／RED
failing evidence → Implementer unchanged sole failing evidence commit → Implementer sole-test bounded green
distinct immutable S → independent Tester same-S actual scoped passing evidence → Implementer unchanged sole T
→ Plan-Creator ONLY plan／step actual review-ready alignment → Implementer separate alignment commit
→ Independent Reviewer same-S committed passing T → Implementer unchanged sole V
→ Planner Phase4.5／Plan-Creator ONLY plan／step actual approval facts alignment
→ Implementer separate alignment commit／normal bounded push → actual published PR-head audit
→ Independent Reviewer exact-seven classification → Implementer unchanged sole class commit／normal push
→ Planner exact permitted reply／resolve／live audit → Plan-Creator ONLY plan／step final factual alignment
→ Implementer separate alignment commit／bounded push → Human boundary。
No direct implementation-to-review shortcut；creator-in-progress→tester-in-progress→review-ready
→reviewer-in-progress→approved|needs-rework；approved→publish-in-progress→pr-open。
Human alone PR approval／merge／release／post-merge；Q gate only verification／classification，不等於 merge approval。

RED 與 green 都 distinct non-merge sole-test immutable subjects；
Tester sole writer 每 subject fresh SHA-bound path
`plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<c47-red-subject-full-40-hex-sha>.json`
或 `plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<c47-green-subject-full-40-hex-sha>.json`。
Single object exact six keys schema_version／topic／implementation_subject_commit／status／commands／recorded_by；
integer 1、loaded-runtime-cache、actual同subject完整40-hex、passing|failing、
nonempty array exact command(nonempty string)／exit_code(integer) objects、Tester。
Passing 全 actual exit0；failing 至少一 nonzero。RED collection／controls exit0，
RED declared regression 至少一新增 assertion fails；無關／syntax／dependency failure 不准替代。
Tester 不 commit；Implementer 原樣每份 separate sole evidence-only commit，
不得與 source／planning／另一份 evidence 共 commit。

Independent Reviewer sole writer fresh
`plan/loaded-runtime-cache/loaded-runtime-cache.implementation-review-log-<c47-green-subject-full-40-hex-sha>.json`。
Single object exact seven keys schema_version／topic／implementation_subject_commit／tester_evidence_commit／
verdict／blocking_issues／recorded_by；integer1、loaded-runtime-cache、same actual green S、
actual full unchanged sole passing T commit、approved|needs-rework、
string array（approved空／needs-rework至少一nonempty issue）、Independent Reviewer。
只能消費同topic／same-S committed passing T，否則 fail closed，不產生 Reviewer evidence。
Reviewer 不 commit；Implementer 原樣 separate sole review-evidence commit，
approved 才 Phase4.5，needs-rework 新 immutable S 完整重走，不借前輪 T/V。

所有 paths 在 actual subject commit 後才以 SHA concrete 化；不能覆寫舊或未提交 receipt；
source／tests／candidate／RED／T／V／alignment diff 與 writer／order不符即停止交 Planner。
Git checks／pre-commit failure 如實 blocker，不移用 C28 no-verify exception／不改配置繞 checks。
所有 SHA 必 actual full lowercase40hex，禁止預填未來 S/T/V／PR head／自身 alignment SHA，
verdict／status／classification outcomes／reply／resolve，禁止以 C42 evidence給新 S 背書。

### Implementation Steps / Validation / Acceptance / TestCase

本輪 canonical Implementation Steps 是 RED＋六 bounded repair；Reviewer／publish／classification 是後續
workflow，不藏在 implementation-completion gate。C42 四 completed steps 原樣 frozen provenance。
新 fixture names 含 c47；rejecting 名稱另含 rejects；benign controls 不含 rejects。
六 finding 各有 isolated fixture；__dict__ direct/imported/assigned known receivers、directstring keys、
__call__ known callable／aliases、IfExp module branch順序交換／known＋unknown／unused；
兩BC For／AsyncFor Name／Tuple／List／Starred targets 與 attribute controls；
Import／ImportFrom asname/noalias/local firstsegment 與既有 ModelIdentity renamed-source rejection；
With／AsyncWith optional_vars syntax、absent optional_vars／ordinary／attribute controls。
o7gvv parameters 只保留現狀與 classification input，不當作本輪新增 rejecting regression。
Fixture source 只寫入 pytest temp paths並 static parse，不執行fixture source／不做 real external I/O。

各 immutable subject actual commands：
- RED collection：`uv run --frozen pytest -p no:tach tests/test_loaded_runtime_cache_bc_independence.py -k c47 --collect-only -q`。
- RED controls：`uv run --frozen pytest -p no:tach tests/test_loaded_runtime_cache_bc_independence.py -k 'c47 and not rejects' -q`。
- RED declared failure：`uv run --frozen pytest -p no:tach tests/test_loaded_runtime_cache_bc_independence.py -k c47 -q`。
- Green：`uv run --frozen pytest -p no:tach tests/test_loaded_runtime_cache_bc_independence.py tests/test_loaded_runtime_cache_contracts.py -q`。
- Ruff：`uv run --frozen ruff check tests/test_loaded_runtime_cache_bc_independence.py tests/test_loaded_runtime_cache_contracts.py`。
- Strict Pyright：`uv run --frozen pyright tests/test_loaded_runtime_cache_bc_independence.py tests/test_loaded_runtime_cache_contracts.py`。
Planning／review-ready factual alignment：
`git diff --check`；`python .agents/skills/plan-step-tracker/scripts/step_tracker.py check_impl_steps_succeeded loaded-runtime-cache`。
Planning時七項 canonical steps pending，CLI exit1是預期／不是通過implementationgate；
review-ready 必全真正[X]且CLI exit0；其餘workflow pending不能隱藏實作未完。
Config authority existing pyproject.toml Python3.12／strictPyright／Ruff；no:tach保證tests實際執行，
不改config／uv.lock／既有 import 行為繞過驗證。

Acceptance／Behavioral Scenarios：
Given authorized bounded surface／local target，When existing static scanner檢查USE／semantic binding，
Then 六項各拒絕既有forbidden行为；Given unusedcallable／unknownreceiver／dynamic key／ordinary names／
attributes／out-of-scope iterables，Then 不因本topic新增拒絕；Given IfExp finiteknownbranches，
Then knownalternative不能被另一branch消掉，不對condition求值。
Given RED collection／controls成功與declared新assertionfailure，When distinct boundedgreen S被實際驗證，
Then passing T只綁此S且獨立Reviewer須消費已提交passingT。Wrong bindings／extra keys／nonsole evidence／
stale head／overwrite fail closed，所有真實 blocker 如實報告，不跳 gate。

### Current-Head Classification / Reviewer Handoff / Unresolved Items

新 green verification／same-S approved V／Phase4.5 alignment／push／actual-head audit 後，
Independent Reviewer 唯一寫 fresh immutable path
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-<c47-green-subject-full-40-hex-sha>-<actual-published-pr-head-full-40-hex-sha>.json`。
Single object exact eight keys schema_version／topic／implementation_subject_commit／tester_evidence_commit／
implementation_review_evidence_commit／pr_head_commit／classifications／recorded_by；
integer1、loaded-runtime-cache、actual full sameS／solepassingT／soleapprovedV／auditedhead、
exact-seven array、Independent Reviewer。各 entry exact thread／comment／outcome／reply；
suffix／comment strings 上表六repairpairs＋`o7gvv/4181373623`各一次，不使用 full PRRT IDs。
REPLY_AND_RESOLVE reply nonempty factual string，其餘 ADDRESS／HUMAN_CHECK 必 JSON null。
Reviewer不commit；Implementerunchangedsoleclasscommit／normalpush；
Planner才routeexactcommittedR&R原文reply／resolve，不任意改reply、不resolveADDRESS/Human。
o7gvv分類不代表新增parameter-detectorimplementation授權；十二Humanlocks／unlisted不分類不resolve。

Final factual alignment ONLYplan／step記actualsubject／evidence／outcomes／reply／resolve與固定一次audit，
只[X]真正完成，不虛勾remainingrequirements。Separatealignmentcommit／push由Gitfacts證明，
不預填自我SHA或自指completioncheckbox、不新增trackingcandidate／receiptchain、不等bot追無限新snapshot。
無release／postmergeaction。Unresolved：七pairs已獨立分類，六authorizedfixes／permittedactions完成；
十二Human＋o7gvv ADDRESS仍open，parameterFIX未授權。Scope drift／contract conflict conservative交Planner／Human，不擴設計。

```json
{"verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]}}
```
Workflow state：current_step=human-check-final-factual-alignment；next_step=bounded-alignment-commit-normal-push；
status=COMPLETE（factual draft handoff only，非自身 commit／review approval／publish／topic-complete）。

### C47 Committed RED / Green / Passing Tester Facts（historical review-ready snapshot）

Candidate `ff32214939ed1bdd5e15f67a01c2a7e981bb4eaa`；
approved Plan-Reviewer unchanged sole commit `11172a4bdef8fe5b83ea3142434cacaf979d5cd9`；
RED sole-test subject `1779e366cafefbc70ad065c9a629dd9dba3b7241`；
failing Tester unchanged sole commit `1be5970152584494ac50c7a585818e30303190e3`；
distinct green sole-test subject `dda13fd64a4075f1cfb691fd3da0fa6230405918`；
passing Tester unchanged sole commit `e584939e9c6101a1acf2fb40494673e96c10d2c9`。
RED evidence 記 collection／controls exit0、declared new assertion command exit1；
same-green-S passing evidence 的 scoped pytest／Ruff／strict Pyright 三 commands actual exit0，
recorded_by=Tester。Planner 已核上述 committed facts，canonical 七項 implementation 依同 S evidence 標 [X]。
舊 C42 T/V 只作 frozen predecessor，不是本 green S passing／review evidence。
本 exact-two review-ready factual draft 不改 source／tests／其他三 planning artifacts／receipts，
不新增 candidate chain；三 rejected untracked 原樣保留。
Next：Implementer separate exact-two factual-alignment commit，之後 independent Reviewer 只能消費
same `dda13fd64a4075f1cfb691fd3da0fa6230405918` 與 committed passing T
`e584939e9c6101a1acf2fb40494673e96c10d2c9`。
Independent Reviewer／V verdict／Phase4.5／push／classification／thread actions 尚 pending；
未預填 V／published head／自身 alignment SHA，不宣稱 review approval 或 publish 已完成。
十二 Human locks 與 o7gvv ONLYclassify／parameter repair exclusion 保持不變。

### C47 Committed Needs-Rework Facts / Existing-Scope Rework Route（frozen predecessor snapshot）

Immutable green S `dda13fd64a4075f1cfb691fd3da0fa6230405918`、
passing T `e584939e9c6101a1acf2fb40494673e96c10d2c9`、
Independent Reviewer needs-rework unchanged sole V commit
`e3a597767270b76edf7c258160ec894057bddd70` 均保留，不覆寫／刪除／重解其 verdict。
Reviewer blocker：step 4 finite known IfExp module alternatives 經 existing simple-name aliases
再進第二 conditional binding 時被 single-valued preserved context 丟失。
Reproducer 只作 AST parse，絕不執行：
```python
import builtins
import importlib

a = builtins if enabled else importlib
b = a
loader = b if enabled else builtins
loader.import_module("identity")
```
Reviewer 獨立 diagnostic detection assertion exit1；舊 prescribed pytest／Ruff／Pyright passing
並不能證明新增 alias-chain regression 成立。Step 4 回 pending；其餘六項原已完成事實保留，
不把舊 passing T 或 C42 evidence 當作新 subject gate。
Scope 不變：只是既有 finite module alternatives 透過 existing simple-name aliases 保存，
再作 existential forbidden USE；不新增 grammar／CFG／binding order／scope invalidation。
六 authorized修復範圍／十二 Human locks／o7gvv ONLYclassify 保持不變，不新 candidate／planning receipt chain。

Plan-Creator 僅此 exact-two factual rework-alignment draft，交 Implementer separate alignment commit；
不預填自我 SHA、不宣稱已提交。之後 sole test path
`tests/test_loaded_runtime_cache_bc_independence.py`：
Implementer 新 isolated RED regression／benign controls（scanner unchanged）→ 新 immutable RED →
independent Tester actual failing evidence → Implementer 原樣 sole failing evidence commit →
Implementer bounded step4 green 新 immutable S → independent Tester same-S 新 passing T →
Implementer 原樣 sole T → ONLYplanstep actual review-ready alignment／separate commit →
Independent Reviewer 消費已提交 same-new-S passing T／fresh V →
Implementer 原樣 sole V → approved 才 Planner Phase4.5／publish／classification。
每 subject evidence 路徑仍為既有 full-SHA templates；新 S 具 fresh immutable
tester-evidence-<new-red-or-green-subject-full-40-hex-sha>.json／
implementation-review-log-<new-green-subject-full-40-hex-sha>.json，
均位於 `plan/loaded-runtime-cache/` 並保留 `loaded-runtime-cache.` prefix。
Tester 六 keys／Independent Reviewer 七 keys／writer／actual exit-code規則與 same-topic／same-S binding
完全沿上述 C47 exact schemas；Tester／Reviewer不commit，Implementer每份原樣sole evidence-only commit。
Wrong／extra key／writer／subject／sole path／ordering／overwrite fail closed；不以 old T/V 背書新 S。
Actual fresh SHA／status／verdict 必等 commit／commands 後記錄，future S/T/V/head、
approval／publish／classification／reply／resolve 全部 pending，不預填。

New fixture marker `c47_rework`；rejecting name 另含 `rejects`，benign controls不含rejects，
原始 alias-chain isolated rejecting regression、branch-order／ordinary／unused controls，
不弱化既有fixtures／assertions／direct imports，source只staticparse。
RED 三命令：
- `uv run --frozen pytest -p no:tach tests/test_loaded_runtime_cache_bc_independence.py -k c47_rework --collect-only -q`。
- `uv run --frozen pytest -p no:tach tests/test_loaded_runtime_cache_bc_independence.py -k 'c47_rework and not rejects' -q`。
- `uv run --frozen pytest -p no:tach tests/test_loaded_runtime_cache_bc_independence.py -k c47_rework -q`。
Collection／controls須actual0，RED須新增指定assertionfailure；syntax／dependencyfailure不是此 gate。
新 green passing T 使用上述 C47 scoped two-file pytest／Ruff／strict Pyright 三完整命令，
全部actual0才passing；step4完成後 canonical CLI須0，當前預期1／one pending。
舊S/T/V frozen history、三rejecteduntracked、dev／其他三planning／source與receipts未改。

### C47 Rework Committed RED / Green / Passing Tester Facts（completed review-ready snapshot）

New RED sole-test subject `158671c9ff7931a831c4081447d445ff12af6706`；
independent failing Tester unchanged sole commit `6dfe55e7b102934679c0ca8f945bdd7c1b364342`；
distinct green sole-test subject `76e80d368bbdec3223c626631bfcd0101ba67d75`；
independent passing Tester unchanged sole commit `157887d31d7e1c819580c96335b2959507df69d4`。
RED c47_rework collection／controls actual exit0、declared assertion command exit1；
同 new-green-S scoped two-file pytest／Ruff／strict Pyright 三命令 actual exit0。
Planner 已核 committed same-S passing T；step4回修完成，canonical七steps[X]，應以 CLI確認0。
此為 review-ready／非 Independent Reviewer approval；新 V／Phase4.5／publish／七筆 classification／
reply／resolve 尚 pending，不預填其 SHA、verdict／outcomes／published head 或自身 alignment commit。
Old S `dda13fd64a4075f1cfb691fd3da0fa6230405918`／T
`e584939e9c6101a1acf2fb40494673e96c10d2c9`／needs-rework V sole commit
`e3a597767270b76edf7c258160ec894057bddd70` 保留 frozen nonrouting history，不覆寫，也不為 new S背書。
Next：Implementer separate exact-two review-ready factual-alignment commit；Independent Reviewer
只可消費同 new S `76e80d368bbdec3223c626631bfcd0101ba67d75` 與 committed passing T
`157887d31d7e1c819580c96335b2959507df69d4`，寫該 new-S fresh immutable review log。
No new candidate chain；六 repair scope／十二 Human locks／o7gvv ONLYclassify不變。
本 draft onlyplan／step，沒有 source／tests／analysis／spec／evidence／dev 或三rejecteduntracked變更；
不預填自身 commit／不宣稱已提交。

### C47 Phase 4.5 Actual Approval Facts / Bounded Publish Alignment（completed pre-publish snapshot）

Green S `76e80d368bbdec3223c626631bfcd0101ba67d75`／passing Tester sole commit
`157887d31d7e1c819580c96335b2959507df69d4`／approved Independent Reviewer unchanged sole commit
`82b09a1e949df5839ee1dd43edda3e4192b3b8d8` 為同-topic／same-subject actual committed triple。
Independent review verdict=approved、blocking_issues=[]，未借舊 S/T/V；
review-ready separate exact-two alignment `f0da9e23d87ef48a2ba6493fab767132bcb7ca43` 已提交。
Planner 已核新 triple 通過 Phase4.5，本 exact-two factual publish-alignment draft 完成，
canonical 七項[X]與 independent implementation review 完成；不是 Human PR approval／merge。
Next pending：Implementer separate exact-two alignment commit＋normal bounded push，
只更新既有 PR #7／origin feature branch，不新增 PR、不 force-push、不 merge。
尚未 push 此 alignment，未預填自身 commit／future PR head／classification receipt concrete path／
七筆 outcomes／reply／resolution；normal push 後唯讀取得 actual published head，
再由獨立 Reviewer 按既有 fresh-path schema綁 new S／上述 T／approved V／actual head 作 exact-seven分類。
十二 Human locks、六 repair scope、o7gvv ONLYclassify 與原 immutable needs-rework history保留。
No new candidate chain／contract／source變更，only plan／step factual draft；三 rejected untracked／dev未動。
Publish-in-progress 僅可成為既有 PR #7 的 pr-open；Human-only review／merge／release／post-merge不授權。

### C47 Final Committed Publish / Classification / Permitted Actions（current human-check）

同 subject S `76e80d368bbdec3223c626631bfcd0101ba67d75`、
passing T `157887d31d7e1c819580c96335b2959507df69d4`、
approved V `82b09a1e949df5839ee1dd43edda3e4192b3b8d8` 保留 actual immutable chain。
Phase4.5 exact-two alignment commit／normal push
`27963d23c5423c338c7223833663a239d2404a5b` 已完成；existing PR #7 是 pr-open，
不是 Human merge approval。獨立 exact-seven classification unchanged sole commit／push
`6d5ef314dab83f62a41216aa2c04bac34a448911` 已完成，
receipt binding 固定 new S／上述T/V／reviewed published head `27963d23c5423c338c7223833663a239d2404a5b`；
後續 class commit head 不偷換 reviewed head，不重寫任何 receipt。

| Classified pair | Committed outcome | Actual permitted action／remaining state |
| --- | --- | --- |
| `n23da/4153205676` | REPLY_AND_RESOLVE | Original receipt reply `4182235985`；resolved=true。 |
| `n3P71/4153360189` | REPLY_AND_RESOLVE | Original receipt reply `4182236452`；resolved=true。 |
| `n4uln/4153959205` | REPLY_AND_RESOLVE | Original receipt reply `4182236964`；resolved=true。 |
| `n4ulr/4153959210` | REPLY_AND_RESOLVE | Original receipt reply `4182237511`；resolved=true。 |
| `n5MVU/4154146529` | REPLY_AND_RESOLVE | Original receipt reply `4182238102`；resolved=true。 |
| `o6M75/4180852193` | REPLY_AND_RESOLVE | Original receipt reply `4182238593`；resolved=true。 |
| `o7gvv/4181373623` | ADDRESS | Classification 完成；parameter-name FIX 未授權／未實作／未resolve，仍open。 |

Planner 已核 fixed full two-page audit snapshot `2026-10-05T08:53:36Z`：
PR #7 head `6d5ef314dab83f62a41216aa2c04bac34a448911`，OPEN／MERGEABLE／CLEAN；
120 threads／107 resolved／13 open = 十二 Human locks＋o7gvv ADDRESS，沒有新 unlisted。
Completed workflow [X]僅表示已核實作驗證／分類／六 permitted actions；不虛勾十三open需求。
Old needs-rework S/T/V frozen nonrouting history原樣保留；original mission／contracts／
十二 locks／o7gvv ONLYclassify邊界不變。不新增 parameter tests／grammar／architecture權限。

Current／phase human-check；本 only plan／step final factual draft尚待 Implementer separate commit／normalpush，
未預填自身 alignment SHA／未宣稱此 draft已提交或push。不新增 candidate／receipt chain、
自指 completion checkbox／alignment循環；此 commit／push是否完成只由 actual Git facts證明。
固定一次 snapshot，不等 bot追新 audit；後續 unlisted inventory-only。
Human-only PR review／merge／release／post-merge不授權；dev／其他paths／三rejecteduntracked未改。

## C48 Current-Head Twelve-Pair Human-Disposition Classification（completed predecessor routing）

C48 draft-time Current／pending 字樣為 frozen nonrouting provenance；final alignment 已於
`dcc8e5b717300c8c9b07bb698dbd1a3da2977cbc` commit／push，C49 是唯一 current route。

### Goal / Outcome / Scope / Locked Decisions

Current：`human-check`。C48 exact-twelve分類／normalpush／Human本PR不修改之原文reply-resolve處置已完成。
Human 明確指示「如果有 human lock 部分直接留言＋resolve」已依獨立分類執行，非實作能力完成／鎖撤除。
本輪 Human 處置是「本 PR 不作該建議修改、如實留言收束其 thread」，
不是實作需求已完成／缺陷已修复，也不撤銷任何 semantic／grammar／architecture lock。
唯獨下列十二 suffix/comment string pairs 可在獨立分類後作 exact permitted actions：

| Thread suffix | Comment ID | Classification input／Human non-implementation disposition |
| --- | --- | --- |
| `jnBpk` | `4043480108` | Cross-topic declared-path ownership／admission。 |
| `kQ95O` | `4060023123` | Architecture／external ACL boundary。 |
| `kqiZ5` | `4070096561` | Architecture scope exclusion。 |
| `lAR8T` | `4078761998` | README／public-surface ownership。 |
| `lfQmF` | `4091213944` | Architecture topology／ownership。 |
| `ndeMt` | `4142807492` | Three-argument getattr grammar。 |
| `n2sm3` | `4153137673` | Nested starred alias pairing。 |
| `n23df` | `4153205681` | 既有 Human-only boundary 建議，本 PR 不修改。 |
| `n4uly` | `4153959219` | Ordered binding／scope invalidation。 |
| `o6Apj` | `4180774151` | Comprehension literal alias inference。 |
| `o6M73` | `4180852189` | Nested For alias target inference。 |
| `o6M76` | `4180852196` | RuntimeRegistry backend semantic kind／renderer decision。 |

`o7gvv/4181373623` ADDRESS 明確排除，保持 open；function／lambda parameter FIX 未授權。
十二項本 PR thread 處置權不延伸至 code／grammar／architecture／README／governance contract，
不重新設計 renderer，不取消既有 boundary 或擴展 scanner。

### Predecessor Facts / Fixed Binding / Analysis Priority

Fixed actual C47 S `76e80d368bbdec3223c626631bfcd0101ba67d75`，
passing Tester sole commit `157887d31d7e1c819580c96335b2959507df69d4`，
approved Independent Reviewer sole commit `82b09a1e949df5839ee1dd43edda3e4192b3b8d8`，
reviewed actual PR head `ad175fb5d4e3167a30c3d4aad922a8357a401430`。
C47 Phase4.5 publish `27963d23c5423c338c7223833663a239d2404a5b`、
exact-seven class sole/push `6d5ef314dab83f62a41216aa2c04bac34a448911`、
六原文 replies／resolved facts保留；final exact-two alignment
`ad175fb5d4e3167a30c3d4aad922a8357a401430` 已提交／normal push。
C47 completed predecessor／old needs-rework S/T/V frozen immutable nonrouting，
不覆寫 receipts，不以其中 historic pending 字樣重開 gate。本輪無新 source／S/T/V，
fixed同topic same-S passing／approved evidence與 unchanged reviewed source支援 classification route，
不是借 evidence為新 implementation背書。C48 唯一 current route。
Existing analysis兩檔存在，採 strict priority；technical-spec execution-facing authority，
requirements business guardrail；本五檔同步 C48 Human disposition，original mission／scope／outcomes／
Registry protocol／tests／Architecture Visualization／follow-ups 不變，非新Python plan。

### In-Scope / Out-Of-Scope / ReadOnly / Written / Deleted / Modify / Goal / Non-Goal

Goal／In-Scope：十二 exact pairs 的 current-head independent classification；
只對 committed REPLY_AND_RESOLVE 留如實 Human non-implementation disposition 原文 reply／resolve。
Modify：standard five planning artifacts；post-actions factual alignment僅plan／step。
Written：下列各獨立角色專屬 immutable receipts。Deleted：無。
ReadOnly：dev／source／tests／docs／diagrams／README／VERSION／governance／repository contract／
configuration／S/T/V／舊 receipts／所有未列 threads。三 rejected untracked原樣保留，不提交／刪除／覆寫。
Out-Of-Scope／Non-Goal：新增 code／grammar／architecture／README／contract／tests／S/T/V；
backend／DI／lifecycle／API／ACL／parameter FIX；PR approval／merge／release／post-merge。
No stable-library surface／release timing變更。舊 semantic locks保留；
thread resolved只表示 Human 本 PR建議處置已執行，不是實作能力／requirement completion。

### Artifact Paths / Status / Actor Sequence / Fresh Immutable Receipts

Plan-Creator唯一writer，feature worktree exact-five：
`analysis/loaded-runtime-cache/requirements.md`、
`analysis/loaded-runtime-cache/technical-spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.plan.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.step.md`。
Standard-five draft → Planner preflight → Implementer exact-five non-merge candidate-only LOCAL commit
→ Independent Plan-Reviewer sole writer fresh immutable candidate SHA-bound path
`plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<c48-candidate-full-40-hex-sha>.json`。
Single object exact verdict／blocking_issues／copilot_feedback_triage；
approved|needs-rework；blocking_issues exact issue/file/fix nonempty-string objects array
（approved空／needs-rework非空）；triage exact ADDRESS/DISCUSS/SKIP arrays。
Implementer 原樣 approved receipt separate sole evidence-only LOCAL commit；
needs-rework不能route，交Planner，不self-select／self-close。
Candidate／approved receipt 保持 LOCAL直到 fixed-head classification完成，
不得先push改 remote reviewed head。Planner核 committed same-topic same-S passing T／approved V、
live head精確上述 fixedhead、source unchanged、fresh path不存在後，
Independent Reviewer sole writer fresh immutable exact path：
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-76e80d368bbdec3223c626631bfcd0101ba67d75-ad175fb5d4e3167a30c3d4aad922a8357a401430.json`。

Classification single object exact eight keys schema_version／topic／implementation_subject_commit／
tester_evidence_commit／implementation_review_evidence_commit／pr_head_commit／classifications／recorded_by：
integer1、loaded-runtime-cache、上述固定actualS/T/V/head、exact-twelvearray、Independent Reviewer。
Entries恰thread／comment／outcome／reply，suffix／comment strings恰表列十二，各一次，不用 full PRRT IDs。
Outcome由Independent Reviewer獨立判REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK，
不預填 outcomes。REPLY_AND_RESOLVE reply須nonempty factual string，逐筆如實說明
Human「此PR不作此修改／本次收束建議thread」處置，並不聲稱修復／需求完成／鎖撤除；
其餘 outcome reply必JSONnull，不可resolve。
Reviewer不commit；Implementer原樣separate sole classification-only commit／normal bounded push。
Planner依committed分類routeexactR&R，Implementer只留receipt原文reply／resolve該exact thread，
核replyID／resolved避免重複。Planning approval不是直接thread action權限；
classification／resolved不是HumanPRapproval／merge，不修改repositorycontract繞gate。
若fixedhead／topic／sameS／schema／pair／writer／order／freshpath／solecommit不符，failclosed交Planner；
不得偷換 binding／overwrite／cross-topic evidence。所有SHA actualfull lowercase40hex。

### Validation / Acceptance / TestCase / Final Factual Alignment / Human Boundary

Acceptance：candidate exactfive／committedapprovedreceipt／sameS passingT＋approvedV／fixedhead unchanged，
fresh immutable path／exacteightkeys／twelveentries／enum／nullability／independentwriters／unchangedsolecommits。
Given fixed evidence/head／十二 input，When Independent Reviewer分類，
Then只產生表列十二 factual entries；GivenHuman nonimplementation disposition，
Then permittedreply不冒稱修復或semantic lock解除。
Invalid：missing/extra key／wrongSHA/topic/pair/writer／nonsolecommit／stalehead／overwrite一律failclosed。
Edge：reply/resolved只核actualfacts，不預填；unlisted/o7gvv無actions。
Regression／Backward compatibility：same-S source／tests／API／locks原樣，既有completed七implementationsteps
保留completed provenance；class-only沒有新RED／green／T／V／fake-codepending。
Python profile只保留existing bounded metadata，不另Pythonplan；
Async-planning status：exempt — classification／tracking-only，無async code或lifecycle change。
Validation commands：`git diff --check`；
`python .agents/skills/plan-step-tracker/scripts/step_tracker.py check_impl_steps_succeeded loaded-runtime-cache`；
各角色以read-only actual Git fullSHA/ancestor/blob/solepath與PR head／thread pagination核fixedfacts。
R&Ractions實際完成後，ONLYplan／step記actualcandidate／receiptcommit／outcomes／replyIDs／resolved、
固定一次fullpaginationas-ofsnapshot，僅[X]已完成workflow；不虛勾未實作requirements。
Implementer separate exact-two finalfactualalignmentcommit／normalpush，完成由Gitfacts證；
不預填自身SHA／自指completioncheckbox／新trackingcandidatechain，不等bot追無限audit。
Thenhuman-check；existingPR7pr-open，不merge／release／postmerge。
Unlisted newpairsinventory-only；o7gvvADDRESS保持open。

Risks：Human decline被誤作fixed、classification outcome預定、locks被錯撤、
stalehead／跨subject／reply重複／trackingloop。
Rollback：只boundedplanningrepair或necessaryfreshimmutable successor，保留oldreceipts／S/T/V；
不broadreset、不覆寫／刪除evidence、不新增code設計。
Unresolved：十二分類／Human處置actions已完成；o7gvv仍ADDRESS／parameterFIX未授權，
兩筆新增unclassified inventory未處理，見下方fixedas-ofsnapshot。
No release／post-mergeactions，所有futurecandidateSHA／verdict／outcomes／reply／resolution不得預填。

```json
{"verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]}}
```
Workflow state：current_step=human-check-final-factual-alignment；next_step=bounded-alignment-commit-normal-push；
status=COMPLETE（factual draft handoff only，非自身commit／push／未實作需求完成／topic-complete）。

### C48 Final Committed Classification / Human Disposition Facts（current human-check）

Actual candidate `7e1f731e5f6b15e5a0ee71c5c9dd9757dcb1f443`；
approved planningreceipt unchanged sole commit `8b4951d61539a84ee9e9f200aa1cca6941165e02`；
Independent Reviewer exact-twelve classification unchanged sole commit／normal push
`c65b44e32d4de544ea4b054b97d5e47a989aa6cc`。
Receipt綁同 S `76e80d368bbdec3223c626631bfcd0101ba67d75`／T
`157887d31d7e1c819580c96335b2959507df69d4`／V
`82b09a1e949df5839ee1dd43edda3e4192b3b8d8`／reviewed head
`ad175fb5d4e3167a30c3d4aad922a8357a401430`，來源與實作evidence未改；
classcommit後的head不偷換reviewedhead。十二committed outcomes均REPLY_AND_RESOLVE，
Implementer已各留receipt原文Human本PR不修改處置，以下replyIDs皆exists／resolved=true／無重複：

| Thread suffix | Actual original reply ID | Actual resolution |
| --- | --- | --- |
| `jnBpk` | `4182462672` | true |
| `kQ95O` | `4182463162` | true |
| `kqiZ5` | `4182463771` | true |
| `lAR8T` | `4182464336` | true |
| `lfQmF` | `4182464973` | true |
| `ndeMt` | `4182465477` | true |
| `n2sm3` | `4182466022` | true |
| `n23df` | `4182466739` | true |
| `n4uly` | `4182467487` | true |
| `o6Apj` | `4182468148` | true |
| `o6M73` | `4182468880` | true |
| `o6M76` | `4182469458` | true |

上述是 Human本PR不作修改之thread處置完成，不是fixed／requirementcomplete／semanticlockremoved；
code／grammar／architecture／README／governancecontract與old immutable history均未改。
Planner核固定fulltwo-pageaudit `2026-10-05T09:23:12Z`：122 threads／119 resolved／3 open，
as-ofhead `c65b44e32d4de544ea4b054b97d5e47a989aa6cc`，既有PR7pr-open，非mergeapproval。
Remaining：`o7gvv/4181373623` ADDRESS／parameterFIX未授權，仍open；
`o93-C/4182313668`、`o93-F/4182313675` 只UNCLASSIFIED inventory，未分類／未回覆／未resolve。
不將此三筆或其他未實作需求虛勾完成，不新增其actions權限。

Current／phasehuman-check；本onlyplanstepfinalfactualdraft尚交Implementer separatecommit／normalpush，
不預填自身alignmentSHA、不宣稱已commit／push，不新增candidate／receiptchain／
自指completioncheckbox／追補alignment循環。自身commit完成只由actualGitfacts證，
snapshot固定一次，不等bot追新audit。三rejecteduntracked／dev／其他paths／舊receipts原樣保留。
Human-only PRreview／merge／release／postmerge不授權。

## C49 Current-Head Four-Pair Classification（completed predecessor routing）

C49 final factual alignment commit／normal push `5afaf53d264466deca22b4858c09177ca112d922` 已完成；
C50 是唯一 current route，C49 draft-time／pending 字樣為 frozen nonrouting provenance。

C49 draft-time／pending 字樣為 nonrouting candidate snapshot；已完成事實以下方 final alignment 為準。

### Goal / Scope / Locked Decisions

Current：`human-check`；step phase：`human-check`；existing PR #7 保持 pr-open。
Goal：以已通過同 subject evidence 的 current head，獨立分類下列四筆 actual comments，
只對 committed REPLY_AND_RESOLVE outcome 執行原文回覆與 resolve。
本 successor 是 classification-only，不授權任何修復、重新設計或繞過 gate。
Analysis strict mode：technical-spec 是 execution-facing truth，requirements 是 intent guardrail；
本共同契約逐字同步 standard five，原 mission／scope／outcomes／Registry protocol／測試策略／
Architecture Visualization／follow-up missions 與 Python metadata 保留不變。

In-Scope：exact-four input inventory、candidate／approved planning receipt、
same-S current-head classification receipt、其 sole commit／normal push 與精確可 resolve actions，
以及最後 only plan／step factual alignment。
Out-Of-Scope／Non-Goal：任何 code／grammar／architecture／README／governance contract 修改；
新 RED／green／Tester／implementation Reviewer chain；解除 semantic locks；
合併、release、post-merge、重寫歷史或建立新 PR。
ReadOnly：既有 source／tests／S/T/V／old receipts／shared contracts／PR #7 facts。
Written／Modify（Plan-Creator 唯一 planning writer）：
- `analysis/loaded-runtime-cache/requirements.md`
- `analysis/loaded-runtime-cache/technical-spec.md`
- `plan/loaded-runtime-cache/loaded-runtime-cache.plan.md`
- `plan/loaded-runtime-cache/loaded-runtime-cache.spec.md`
- `plan/loaded-runtime-cache/loaded-runtime-cache.step.md`

Deleted：none。後續 final alignment 僅上述 plan／step；所有其他 paths、dev worktree、
三份 rejected untracked receipts 不動。非唯一 agent，不 revert 他人成果。
Stable-library intent：absent；README／VERSION／release notes 不改。
Async-planning status：exempt — classification／tracking-only，無 async code／lifecycle 變更；
保留既有七項 Python decisions 與五類 Python test metadata，不另寫 Python plan。
原 canonical 七項 implementation 已完成，保留 C47 completed provenance，不建立 fake code-pending。

### Actual Fixed Facts / Exact Comment Inputs

C48 candidate `7e1f731e5f6b15e5a0ee71c5c9dd9757dcb1f443`、
approved sole receipt `8b4951d61539a84ee9e9f200aa1cca6941165e02`、
classification sole push `c65b44e32d4de544ea4b054b97d5e47a989aa6cc`、
final alignment commit／push `dcc8e5b717300c8c9b07bb698dbd1a3da2977cbc` 是已提交 predecessor facts。
十二 Human threads 的不修改處置已完成，不是 fixed／requirement completed／semantic lock removed。
原十二 semantic／grammar／architecture／README locks 全部維持。
`o7gvv/4181373623` 仍 ADDRESS／open，function／lambda parameter fix 未授權。

Fixed S：`76e80d368bbdec3223c626631bfcd0101ba67d75`；
passing T sole commit：`157887d31d7e1c819580c96335b2959507df69d4`；
approved V sole commit：`82b09a1e949df5839ee1dd43edda3e4192b3b8d8`；
reviewed PR head：`dcc8e5b717300c8c9b07bb698dbd1a3da2977cbc`。
Planner 已核 local／origin／PR 一致、OPEN／MERGEABLE／CLEAN、同 S/T/V actual ancestors、
sole evidence 與 source unchanged；分類前須重新核 fixed head，不以 branch 或 chat 取代 evidence。

| Thread suffix | Comment string | Actual input（分類輸入，不是預定 outcome／修復契約） |
| --- | --- | --- |
| `o93-C` | `4182313668` | P1 alleges historical reviewed ece8db92…／parent d6ff74dd… 未保留目前 S/T/V ancestry，且 co-added implementation 與 evidence；要求保留合法 chain 或重建。Independent Reviewer 核 current full-SHA graph 與 sole commits，不以歷史 short SHA 推定或補成合法。 |
| `o93-F` | `4182313675` | P2：direct imported builtins.getattr 的 getter 經 simple-name assignment，如 resolve→lookup，可能未被 existing alias resolver 保留而漏檢 lookup(importlib, "import_module") 的後續使用。此輪只分類，不執行 fixture、不新增 detector／regression。 |
| `o-rDd` | `4182633560` | P2：known module.__dict__.get("import_module") 的 literal namespace lookup／後續使用可能漏檢；這是 .get lookup，不偷換成 C47 已修的 direct subscript。此輪只分類，不擴 namespace resolver。 |
| `o-rDg` | `4182633565` | P2：comprehension.target 的 foreign semantic name（Loaded Runtime Cache 的 ModelIdentity／Identity 的 RuntimeReuseKey）可能未涵蓋；semantic target syntax 與已鎖定 comprehension dynamic-import alias inference 是不同要求，不得混同或以 disposed thread 假裝修復。此輪不授權兩者修復。 |

四筆 actual comments 已核 open；不預判 technical finding 已處理或非必要。
C48 Human 不修改處置只涵蓋原十二筆，不自動授權拒絕新增 technical findings。
新增 unlisted pairs 只能 inventory，不分類／回覆／resolve。

### Artifact Paths / Immutable Schemas / Sole Writers

Plan-Reviewer 唯一寫入：
`plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<actual-C49-candidate-full40SHA>.json`。
actual candidate 提交後才展開 fresh path；exact three keys：
`verdict`、`blocking_issues`、`copilot_feedback_triage`。
verdict 是 approved|needs-rework；blocking_issues 是 objects array，每 object 恰含
non-empty string issue／file／fix；approved 時 []，needs-rework 時至少一項。
triage 恰 ADDRESS／DISCUSS／SKIP arrays。不得預填 verdict／future candidate SHA。
獨立 Plan-Reviewer 審 committed exact-five candidate，不 commit；Implementer 原樣 sole evidence-only commit。

Independent Reviewer 唯一分類 writer path：
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-76e80d368bbdec3223c626631bfcd0101ba67d75-dcc8e5b717300c8c9b07bb698dbd1a3da2977cbc.json`。
必須 fresh，不 overwrite 舊 evidence。單一 JSON object exact eight top-level keys：
`schema_version`、`topic`、`implementation_subject_commit`、`tester_evidence_commit`、
`implementation_review_evidence_commit`、`pr_head_commit`、`classifications`、`recorded_by`。
schema_version 為 integer 1；topic 為 loaded-runtime-cache；四個 SHA 分別 exact fixed S/T/V/head；
recorded_by 為 Independent Reviewer。classifications 恰四 entries，exact-four pairs 各一次。
每 entry 恰 thread／comment／outcome／reply；thread 是上述 suffix string，comment 是上述 string ID；
outcome 是 REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK，由 Independent Reviewer 獨立判定。
REPLY_AND_RESOLVE 的 reply 必為 non-empty factual original reply，須有 current committed facts 支持；
ADDRESS／HUMAN_CHECK 的 reply 必為 null，保持 open，必要 Human 選擇一次彙整。
不可聲稱未授權修復已完成、偽造 historical approval、混同 target syntax／alias inference，
或因使用者希望收束就預定四筆 R&R。Reviewer 不 commit／不留言。
Implementer 只能原樣以 sole classification evidence-only commit 提交，不混 planning／source／其他 evidence。

### Ordered Route / Acceptance / Validation

1. Plan-Creator exact-five draft → Planner preflight → Implementer exact-five LOCAL candidate commit。
2. Independent Plan-Reviewer fresh SHA-bound receipt → approved 才 Implementer unchanged sole LOCAL receipt commit。
3. Candidate 與 approved receipt 均保持 LOCAL；分類前不 push 改動 reviewed remote head。
4. Planner 核 fixed head、same S/T/V committed passing／approved、ancestry／source unchanged 與 fresh path。
5. Independent Reviewer 寫 exact-four classification → Implementer sole classification commit／normal push。
6. Planner 只以 committed receipt 核 exact R&R action gate；Implementer 原文 reply／resolve 對應 thread，
   記 actual reply IDs／resolved facts，避免 duplicate；ADDRESS／HUMAN_CHECK 不可 resolve。
7. Only plan／step actual final alignment（真完成 workflow 才 [X]，未修復需求不虛勾）→
   separate normal commit／push → 固定一次 full-pagination PR audit → human-check，既有 PR7 pr-open。
   不預填自身 alignment SHA／commit／push，不新 self-completion checkbox 或 tracking candidate 循環。

Acceptance／TestCase：
- Happy path：approved planning receipt＋same-S committed evidence＋exact-four classification，只有 factual R&R actions。
- Invalid input：多／少 keys、wrong writer／pair／string type／SHA／enum、wrong sole commit fail closed。
- Edge case：historic short SHA 查證不足，記 limitation；target syntax 不等於 alias inference，不能偷換分類依據。
- Regression：S/T/V ancestry／source blobs 與 canonical seven completed 不變，o7gvv ADDRESS／十二 locks 保留。
- Backward compatibility：direct imports、mission／protocol／visualization／Python metadata／old immutable receipts 不變。
Given approved candidate receipt 與 fixed head，When 獨立分類，Then exact-four receipt 可供 Planner routing；
Given ADDRESS／HUMAN_CHECK，When actions route，Then thread 仍 open、無 reply／resolve。
Given head drift／source drift／required evidence missing，Then 停在 gate，不改用新 head 或借 evidence。

Planning validation：
`git diff --check`；
`python .agents/skills/plan-step-tracker/scripts/step_tracker.py check_impl_steps_succeeded loaded-runtime-cache`。
各角色 actual Git checks：
`git rev-parse HEAD`、`git status --short`、
`git merge-base --is-ancestor 76e80d368bbdec3223c626631bfcd0101ba67d75 dcc8e5b717300c8c9b07bb698dbd1a3da2977cbc`；
同樣核 fixed T/V ancestry；
`git diff 76e80d368bbdec3223c626631bfcd0101ba67d75 dcc8e5b717300c8c9b07bb698dbd1a3da2977cbc -- src tests`；
`git show --format=fuller --stat <actual-evidence-commit>`／named diff 核 sole path、
JSON schemas／topic／same subject／passing T／approved V；read-only PR head／threads full pagination。
Fresh path 必在 tracked history與工作樹都不存在；head drift、source drift、schema／sole-commit failure、
required evidence missing、scope conflict 即 blocked／交 Planner，不自改 contract 或新增修復設計。

Risks：以 historic allegation 取代 current evidence、錯認 syntax／alias、預定 outcomes、stale head、
跨 subject evidence、scope expansion、duplicate replies 或 self-tracking loop。
Rollback：only bounded exact-five planning repair／必要 fresh immutable successor；
保留已提交 candidate／receipts／S/T/V，不 broad reset、overwrite evidence、修改 implementation。
Open Questions：四筆 independent outcomes 已提交且唯一 permitted action 已完成；
o7gvv 與三筆新 ADDRESS 修復未授權／未實作，仍 open，詳 final facts。
此輪無 code 設計待補；若分類要求 scope 外修復，ADDRESS／HUMAN_CHECK 留 open，Human 一次決定。
Post-merge／release actions：none；Human alone PR review／merge／release／post-merge／tag。

Reviewer handoff schema（不是預填 receipt）：
```json
{"verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]}}
```
Workflow state：current_step=human-check-final-factual-alignment；next_step=bounded-alignment-commit-normal-push；
status=COMPLETE（final factual draft handoff only，非merge approval／topic-complete）。

### C49 Final Committed Classification / Permitted Action Facts（current human-check）

C49 candidate `bd27be3aa20a92829f31ad5bb483ae3a1c3de0c3` 是 exact-five planning-only commit；
approved Plan-Reviewer receipt 的 unchanged sole commit 是
`86c6e2ec81bcd8ed16a79897a836207cbc65c2ae`；
exact-four classification receipt 的 unchanged sole commit／normal push 是
`f74a69376e51913d7287def98191738ce6222020`。
SHA-bound planning receipt 與 classification receipt 已提交，原 S/T/V 與所有 immutable evidence 保留。

| Pair | Committed outcome | Actual disposition |
| --- | --- | --- |
| `o93-C/4182313668` | REPLY_AND_RESOLVE | 已原樣回覆 receipt 原文；reply ID `4202433177`，isResolved=true；只確認 current valid chain，不補成 historical approval。 |
| `o93-F/4182313675` | ADDRESS | getter simple-name assignment alias 未修復／未授權；仍 open。 |
| `o-rDd/4182633560` | ADDRESS | namespace.__dict__.get literal lookup 未修復／未授權；仍 open。 |
| `o-rDg/4182633565` | ADDRESS | comprehension semantic target 未修復／未授權；仍 open，非 comprehension alias-inference lock。 |

Planner／Implementer 核對的完整兩頁 audit as-of `2026-10-07T02:30:16Z`：
124 threads／120 resolved／4 open，沒有新 unlisted pairs；
當時 local／origin／PR head 均為 `f74a69376e51913d7287def98191738ce6222020`，
PR #7 為 OPEN／MERGEABLE／CLEAN，無 merge conflict。
其餘 open 是 `o7gvv/4181373623` ADDRESS：function／lambda parameter-name 修復未授權。
四 ADDRESS 都未修復、未 resolve，不是 requirement completed；必要 scope 決定一次交還 Human。
十二 Human threads 的 C48 不修改處置與原十二 semantic locks 保持不變；
不擴 code／grammar／architecture／README／contract scope，不更改原 mission／protocol／visualization。

Current／step phase 為 human-check，既有 PR #7 保持 pr-open；本 ONLY plan／step final factual draft
待 Implementer separate normal commit／push，完成由 actual Git facts 證明，
不預填自身 alignment SHA／commit／push，不新增自指 checkbox 或 candidate／receipt chain。
analysis／spec 保留 committed C49 candidate snapshot；舊 draft-time／pending 字樣只作 nonrouting provenance。

## C50 Bounded Four-ADDRESS Repair（authoritative current routing）

### Goal / Outcome / Scope

Current：`publish-in-progress`；phase：`publish-in-progress`。C50 是本 topic 唯一 current repair route；
C49 及更早 draft-time／pending／Current 字樣是 frozen nonrouting provenance，不授權 C50 implementation。
Human 已明確授權下表四修復；本修正不取代 original Loaded Runtime Cache mission。
原 mission／scope／outcomes／Runtime Registry reuse protocol／Architecture Visualization／follow-up missions 不變。
Analysis strict mode：technical-spec 為 execution-facing truth、requirements 為 intent guardrail；
本 C50 共同契約逐字同步 standard five，後續只允許已授權 plan／step factual state alignment。
既有 PR #7 pr-open；本輪不新開 PR、不 merge／release／post-merge／tag。

| Exact thread/comment pair | Goal／In-Scope：bounded behavior |
| --- | --- |
| `o7gvv/4181373623` | FunctionDef／AsyncFunctionDef／Lambda 的 ast.arguments 全部本地參數 NAME，依兩 BC foreign semantic-name syntax ownership 判定。 |
| `o93-F/4182313675` | known directly imported builtins.getattr 經 simple-name assignment fixed-point alias，保持 getter identity，依原 bounded lookup／後續 forbidden USE 判定。 |
| `o-rDd/4182633560` | known module Name／existing module alias 的 .__dict__.get(direct string literal)，exact-one positional、no keywords/default；只解析原三 forbidden import-callables，依後續 USE 判定。 |
| `o-rDg/4182633565` | ast.comprehension.target 的 Name／Tuple／List／Starred foreign semantic-name syntax；list／set／dict／generator，含 async target syntax，忽略 Attribute。 |

In-Scope：single-test-path RED／green bounded修復、新 same-S independent Tester／Reviewer evidence、
candidate／approved receipt／Phase4.5 alignment、exact-four independent classification及 permitted actions。
Out-Of-Scope／Non-Goal：source API／grammar或 architecture之外的新需求、跨 BC import／mapper／backend／DI／
runtime lifecycle／execution；comprehension dynamic-import alias inference、arbitrary iterable／CFG／ordered scope；
README／VERSION／dependencies／config／shared contracts／Archify files／十二 semantic locks／新 unlisted 修復。
Deleted：none。非唯一 agent，不 revert 他人成果；dev worktree 不得寫檔。
三 rejected untracked receipts 保持原樣、不 stage／overwrite／delete／用作 routing authority。

### Locked Decisions / Boundaries

1. Parameter syntax：遍歷 FunctionDef／AsyncFunctionDef／Lambda.args 的 posonlyargs、args、vararg、
   kwonlyargs、kwarg 的 ast.arg.arg；Loaded Runtime Cache 禁本地 ModelIdentity，
   Identity 禁本地 RuntimeReuseKey。普通 parameter name／annotation／default 中名稱不是 parameter-name binding；
   不新增 annotation／default 求值、scope modeling、runtime inspection。
2. Getter alias：僅既知 directly imported builtins.getattr（含既有 import asname）沿 simple-name assignment
   fixed-point 傳遞；不是 arbitrary getter alias、不是持有 callable 即違規。
   Getter lookup 保持既有 exact-two positional／no keywords、known module Name／direct string literal／
   existing forbidden surfaces／後續 USE 語意；three-positional／starred／unknown controls 與 locks 不變。
3. Namespace.get：receiver 僅 known module Name／既有 module alias 的直接 .__dict__，
   method 精確 get、exact-one positional、no keywords／default，key 必 direct ast.Constant string。
   僅 `builtins.__import__`、`importlib.__import__`、`importlib.import_module`，
   透過既有 alias／後續 USE 拒絕；unknown receiver／dynamic key／ordinary or missing entry／unused possession
   不因本輪額外拒絕。不得 namespace alias、任意 mapping／default／iterable／call-result inference。
4. Comprehension semantic target：使用既有 Name／Tuple／List／Starred target-name traversal，忽略 Attribute；
   全部 ast.comprehension.target 包括 is_async 的純 AST target syntax。
   這不授權 comprehension dynamic-import alias inference／RHS iterable／generator 執行／ordered scope。
5. 十二原 semantic／grammar／architecture／README locks 維持，包括 exact-two getattr、comprehension alias
   inference 等；C48 Human 不修改處置不代表修復完成或解除鎖。所有既有 direct imports／fixtures／mocks／
   assertions 不變，不以 importlib／__import__／sys.modules substitution 取代 regression。
6. 新 unlisted `pu_ja/4202486092`（match targets）、`pu_jo/4202486109`（container lookup）、
   `pu_j0/4202486122`（pyi scan）只有 inventory、open；不得分類／修復／留言／resolve。
7. implementation 是 scanner 所在唯一 test module 的 bounded repair；production protocols／outcomes／
   taxonomy／public surface／Architecture Visualization 全部 ReadOnly，不新增架構決策。
   不執行 fixture source，不新增跨 BC import；解析不等於執行。

### Status / Allowed Transitions / Actual Predecessor Facts

C49 final exact-two factual alignment 已 commit／normal push：
`5afaf53d264466deca22b4858c09177ca112d922`，C50 authoring base 為該 full SHA。
C49 candidate `bd27be3aa20a92829f31ad5bb483ae3a1c3de0c3`、
approved receipt sole `86c6e2ec81bcd8ed16a79897a836207cbc65c2ae`、
classification sole `f74a69376e51913d7287def98191738ce6222020` 為 immutable predecessor facts。
C49 o93-C reply `4202433177`／resolved 保留；其他四 ADDRESS 現在由 Human 授權 C50 repair，
尚未修復，不能預勾完成。原 S/T/V（S `76e80d368bbdec3223c626631bfcd0101ba67d75`、
T `157887d31d7e1c819580c96335b2959507df69d4`、
V `82b09a1e949df5839ee1dd43edda3e4192b3b8d8`）只作 predecessor provenance；
不能當 C50 new subject passing evidence。
Planner 已核 authoring base local／origin／PR 相同、OPEN／MERGEABLE／CLEAN、tracked/index clean、
三 rejected untracked preserved；本記錄不預填 C50 candidate／subject／evidence SHA 或 outcome。

planned → committed candidate／independent approved Plan-Reviewer sole receipt → creator-in-progress RED →
independent Tester factual failing RED／sole evidence → distinct green creator-in-progress →
tester-in-progress／same-new-S passing sole evidence → review-ready factual alignment／CLI →
independent reviewer-in-progress → approved|needs-rework。
needs-rework 只可 bounded rework，新的 immutable subject 重走同 subject T/V，不覆寫或借舊 evidence。
approved → Planner Phase4.5 factual alignment → publish-in-progress → existing PR7 pr-open →
new-S／actual-published-head classification → exact per-pair actions → final factual alignment／human-check。
publish-in-progress 不可直接 merged；Human alone PR review／merge。
Planning approval 不等於 implementation approval；Reviewer 非 Human PR reviewer。

### Artifact Paths / ReadOnly / Written / Modify / Sole Writers

Plan-Creator 唯一 planning writer（candidate exact-five，final alignment only plan／step）：
- `analysis/loaded-runtime-cache/requirements.md`
- `analysis/loaded-runtime-cache/technical-spec.md`
- `plan/loaded-runtime-cache/loaded-runtime-cache.plan.md`
- `plan/loaded-runtime-cache/loaded-runtime-cache.spec.md`
- `plan/loaded-runtime-cache/loaded-runtime-cache.step.md`

Implementer 唯一 implementation Modify path：`tests/test_loaded_runtime_cache_bc_independence.py`。
RED subject 必 only 此 path、test-only，green subject 也必 only 此 path。
`tests/test_loaded_runtime_cache_contracts.py` 為 ReadOnly regression validation input。
其他 src／tests／config／uv.lock／README／VERSION／architecture／Archify／shared contracts／old receipts ReadOnly；
超出 path／scope 停在 Planner，不猜 path 或修改 repository contract。
Written：以下 fresh immutable SHA-bound evidence，僅 designated independent writer 寫、不 commit；
Implementer 原樣、各自 sole evidence-only commit，不與 planning／implementation／另一 evidence 混 commit。
下列參數只有 actual committed full 40 lowercase hex SHA 已存在後才展開；不得 symbolic HEAD／short SHA／
future SHA／結果預填／overwrite，包括 rejected uncommitted immutable receipts。
同一 evidence commit 必 non-merge；驗實際 named diff 恰 sole path、JSON exact schema、topic／subject／writer。

Plan-Reviewer path：
`plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<actual-C50-candidate-full40SHA>.json`。
exact 3 keys verdict／blocking_issues／copilot_feedback_triage。
verdict approved|needs-rework；blocking_issues object array，每 object 恰 issue／file／fix non-empty strings，
approved 必 []、needs-rework 至少一項；triage 恰 ADDRESS／DISCUSS／SKIP arrays。
Independent Plan-Reviewer 審 committed exact-five LOCAL candidate，不 commit；
approved 才 Implementer unchanged sole LOCAL receipt commit，不先 push。

Tester RED path：
`plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<actual-C50-RED-full40SHA>.json`；
Tester green path：
`plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<actual-C50-green-S-full40SHA>.json`。
exact 6 keys schema_version／topic／implementation_subject_commit／status／commands／recorded_by。
schema_version integer 1；topic loaded-runtime-cache；subject 為該 actual RED 或 green S；
recorded_by Tester；commands non-empty array，每 entry 恰 command non-empty string／exit_code integer。
status passing|failing；passing 只在全部 actual exit_code=0，failing 至少一項 actual nonzero。
RED collection／controls 必 exit0，四原 positive finding 的 rejecting tests 均 genuine assertion failure、
不是 parse／import／collection failure；原樣 sole failing T 後才 green。Failing RED 不寫 Reviewer evidence。
Independent Tester 實測 immutable subject、不 commit；Implementer unchanged sole commit。

Independent Reviewer path：
`plan/loaded-runtime-cache/loaded-runtime-cache.implementation-review-log-<actual-C50-green-S-full40SHA>.json`。
exact 7 keys schema_version／topic／implementation_subject_commit／tester_evidence_commit／verdict／
blocking_issues／recorded_by；integer1／loaded-runtime-cache／same actual green S／sole committed passing T fullSHA；
verdict approved|needs-rework；blocking_issues string array，approved []、needs-rework 非空；
recorded_by Independent Reviewer。只消費 committed same-topic／same-S passing T，
missing／failing／uncommitted／cross-S／wrong schema fail closed、不得產生 Reviewer evidence。
Reviewer 獨立審 implementation，不 commit；Implementer unchanged sole V commit。

Independent classification path：
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-<actual-C50-green-S-full40SHA>-<actual-reviewed-published-PR-head-full40SHA>.json`。
在新同-S passing T／approved V／Phase4.5 alignment normal push 已實際提交、PR head 固定後才展開；
不是 authoring base／舊 C47 S，也不得追新 head 換 receipt。exact 8 keys：
schema_version／topic／implementation_subject_commit／tester_evidence_commit／
implementation_review_evidence_commit／pr_head_commit／classifications／recorded_by。
integer1／loaded-runtime-cache／actual new S／same-S sole passing T／same-S sole approved V／
actual reviewed published PR head；recorded_by Independent Reviewer。
classifications exact-four entries，各上表 pair 恰一次；entry exact thread／comment／outcome／reply。
thread suffix string（不用 full PRRT ID），comment string；outcome REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK。
只有 factual REPLY_AND_RESOLVE 的 reply 為 non-empty original factual reply，
ADDRESS／HUMAN_CHECK 必 null、open；不预定 outcome、不以 user希望收束宣稱修復。
Reviewer only writes fresh classification、不留言／commit；Implementer unchanged sole class commit／normal push。
receipt 後 descendants source unchanged／original head ancestry及 sole-path checks由 Planner 核後才 exact action。

### Python implementation metadata（C50 bounded current profile）

#### Non-goals
- 不改 production runtime contracts／API／BC identity authority／Architecture Visualization。
- 不解除十二 locks、不實作 comprehension dynamic-import alias inference／arbitrary mapping／scope／iterable analysis。
- 不新增 dependency／config／README／VERSION／backend／DI／lifecycle／source execution。
- 不處理新 unlisted／merge／release／重写历史；不修改他人或 dev worktree 檔案。

#### Current Context / Requirements
`tests/test_loaded_runtime_cache_bc_independence.py` 的 _binds_foreign_semantic_name 已涵蓋 import／For／With
target syntax，尚未覆蓋 ast.arguments／ast.comprehension.target；
_aliases_from_imports 已標 known builtins.getattr，但 _resolve_name_alias 排除它，plain assignment 可丟 getter identity；
_resolve_namespace_import_callable 只涵蓋 direct subscript，尚未涵蓋 bounded .get。
C50 僅補四可重現缺口，private resolver representation 由 Implementer bounded選擇，不變更 locked behavior。
每四 original positive finding 都要 isolated genuine RED assertion，green 可判定且 benign controls 通過；
保留舊 fixtures／direct imports／mock／assertions，不以放寬tests或動態載入隱藏 regression。

#### Decisions
- Async-planning status: exempt — cite exemption evidence: 本 module 只同步 ast.parse／ast.walk 檢查
  AsyncFunctionDef／async comprehension TARGET syntax；不執行 fixture，沒有 async boundary、resource ownership、
  I/O、concurrency、timeout／retry／cancellation／runtime lifecycle 改變。
- Module/package placement: only `tests/test_loaded_runtime_cache_bc_independence.py` existing scanner／fixtures。
- New public API: no；不增 package/module/public exports。
- Interface changes: no production interface changes；只擴已宣告四 test-scanner behaviors。
- Breaking changes allowed: no；preserve direct imports與existing authorized behavior／negative bounds。
- New dependencies: no；使用既有 ast／pytest／Ruff／strict Pyright，uv.lock不改。
- Error-handling strategy: 保留既有 assertion／parser exception 語意，真錯誤不吞、不改missing／Unavailable protocol。
- Typing strategy: Python3.12 strict Pyright、既有精確 AST types／typed helpers；no Any／dynamic import／sys.modules substitution。

#### Public Contract / API Changes / Affected Files
No production API change；ReadOnly same protocol/outcomes。Likely affected implementation file only
`tests/test_loaded_runtime_cache_bc_independence.py`；candidate files to inspect：
同 test、ReadOnly `tests/test_loaded_runtime_cache_contracts.py`、`pyproject.toml`。
Exact planning/evidence writer paths依前表；Deleted none。

#### Test Plan / TestCase
- Happy path：兩BC五種parameter位置×def／asyncdef／lambda；known directimport getter plain/chained aliases的後續
  boundedlookup USE；三forbidden namespace.get後續USE；四種comprehension含async target syntax。
- Invalid input：unknown／arbitrary getter，unknown namespace receiver、dynamic key、default／keywords、
  ordinary/missing entry、三posgetattr與starred不擴；不把 source invalid syntax 當成功 RED。
- Edge case：posonly／vararg／kwonly／kwarg；getter alias statement-order permutations用existing固定點，
  不擴ordered-scope語意；unused callable合法；nested Tuple/List/Starred semantic targets，Attribute忽略。
- Regression：舊 C47 及更早 direct imports／fixtures／mock／assertions／callable alternatives／sys.modules detector
  與十二locks保持；scoped兩檔pytest、Ruff、strict Pyright realpass。
- Backward compatibility：runtime direct-module APIs／Identity independence／protocol/outcomes／Archify不變。
Given four original missed fixtures，When RED old scanner parses，Then collection／controls pass且四需求rejecting assertions實際fail。
Given new bounded scanner，When same fixtures／controls在green驗證，Then正確reject四類、controls／全部scopedregression pass。
Given annotation/default ordinarynames／unknown/unused possession，Then本輪不新增誤拒；
Given target attribute或comprehension iterable，Then only authorizedtarget語法，不執行或推論RHS。
Given same-S committed passing T／approved V與fixedpublishedhead，Then Independent Reviewer才能classify exactfour，
不能由勾選implementation自行宣告threads addressed。
上述即 spec Acceptance Criteria／Behavioral Scenarios／Error / Edge Cases C50 co-artifact契約。

#### Risks / Rollback Plan
Risks：getter identity誤當forbidden possession、namespace.get擴任意mapping/default、
semantic target混同alias inference、REDparseerror、cross-subjectevidence／stalehead、
放寬existingassertions、duplicate replies與self-state追蹤loop。
Rollback：只在single test path bounded修回並建立新immutable S重走T/V；
planning修正onlydeclaredfive且經Planner route。保留所有已提交receipt／RED／S／T／V與rejecteduntracked；
不broadreset、覆寫證據、偷改contracts、production或dev。不使用歷史C28 no-verify授權。

### Implementation Steps（source for canonical completion gate）

1. C50 在 `tests/test_loaded_runtime_cache_bc_independence.py` 新增四 original findings 的 isolated RED fixtures及benign controls；新測試名稱含 c50，rejecting 名稱另含 rejects、controls不含 rejects。只新增tests，不修scanner、不執行fixture source，collection／controls須pass、四類genuineassertionfail。
2. C50 在 `tests/test_loaded_runtime_cache_bc_independence.py` 補 FunctionDef／AsyncFunctionDef／Lambda 的全部 ast.arguments local-name semantic syntax，兩BC ownership適用；不判annotation／default／scope，不改既有assertions。
3. C50 在 `tests/test_loaded_runtime_cache_bc_independence.py` 沿existing simple-name assignment固定點保留known directly imported builtins.getattr getter identity；lookup仍exact-two-pos/no-keywords／knownmodule／literalattribute／existingUSE，不新增持有拒絕或arbitrary getter。
4. C50 在 `tests/test_loaded_runtime_cache_bc_independence.py` 補known module Name／existingalias.__dict__.get的directstringliteral／exact-one-pos/no-keywords/default解析，只三既有forbidden import-callables後續USE；unknown/dynamic/ordinary/missing/unused controls不誤拒，不推namespacealias或arbitrarymapping。
5. C50 在 `tests/test_loaded_runtime_cache_bc_independence.py` 將全部 ast.comprehension.target交existingName／Tuple／List／Starred semantic-name traversal，ignoreAttribute，含list/set/dict/generator及asyncTARGETSYNTAX；不擴comprehensionaliasinference／RHSiterable／orderedscope／fixtureexecution。
6. C50 在 `tests/test_loaded_runtime_cache_bc_independence.py` 保留所有舊direct imports／fixtures／mocks／assertions與十二locks，對sameimmutablegreen S實際通過兩 scoped pytest檔／Ruff／strict Pyright；未完成前canonicalsteps保持pending，不將review／publish／classification算作implementationsteps。

### Validation / Acceptance Checks / Ordered Evidence Chain

RED actual commands（Independent Tester，不由 Creator偽造）：
```bash
uv run --frozen pytest -p no:tach tests/test_loaded_runtime_cache_bc_independence.py -k c50 --collect-only -q
uv run --frozen pytest -p no:tach tests/test_loaded_runtime_cache_bc_independence.py -k 'c50 and not rejects' -q
uv run --frozen pytest -p no:tach tests/test_loaded_runtime_cache_bc_independence.py -k c50 -q
```
Collection／controls exit0且原四 positive需求全部meaningfulassertionfail，則記actualfailing RED evidence；
collectionerror／controlsnonzero／部分需求未紅不得假稱REDgate。
Green actual commands：
```bash
uv run --frozen pytest -p no:tach tests/test_loaded_runtime_cache_bc_independence.py tests/test_loaded_runtime_cache_contracts.py -q
uv run --frozen ruff check tests/test_loaded_runtime_cache_bc_independence.py tests/test_loaded_runtime_cache_contracts.py
uv run --frozen pyright tests/test_loaded_runtime_cache_bc_independence.py tests/test_loaded_runtime_cache_contracts.py
```
1. Plan-Creator exact-five draft → Plannerpreflight → Implementer exact-five LOCAL candidatecommit，
   不code/evidence、不push改PRhead → IndependentPlanReviewerfreshSHAreceipt → approvedsoleLOCALcommit。
2. Implementer one-test-path REDsubject → IndependentTesteractualfailingreceipt →
   Implementer unchangedsolefailingT → boundedgreen newimmutableS（onlytestpath）。
3. IndependentTesteractualallgreencommands／passingreceipt → Implementer unchangedsolepassingT。
   不借C47 T/V、不以同角色合併Tester／Reviewer、不把expectedfail當pass。
4. Plan-Creator onlyplan／step actualreviewreadyalignment，[X]只actualimplemented＋same-S passing證明；
   Implementer separatealignmentcommit → Planner canonicalCLI實際0 →
   IndependentReviewer只讀newS＋committedsameS passingT寫freshV → Implementer unchangedsoleV。
5. PlannerPhase4.5 → Plan-Creatoronlyplanstepfactualalignment →
   Implementer separatealignmentnormalcommit／push更新既有PR7（既有Humanpublish授權）。
6. Planner核actualpublishedhead／newS/T/V ancestry／solecommits／sourceunchanged →
   IndependentReviewerfixedheadexact-fourfreshclassification，不预定R&R →
   Implementer unchangedsoleclasscommit／normalpush。
7. Planner只routecommittedR&Rpair → Implementerexactoriginalreply／resolve，先核是否已完成防重覆，
   實記replyID與resolved。ADDRESS／HUMAN_CHECK保持open，不偷偷擴implementation或直接resolve。
8. Plan-CreatorONLYplan／stepfinalactualfacts，未修需求不虛勾 →
   Implementerseparatenormalcommit／push → 一次full-paginationaudit → human-check。
   不預填自己finalalignmentSHA／commitpush或新增selfcheckbox／trackingcandidatechain；
   actualGitfacts證publish，不為bot新增留言无限續修。Unlisted只inventory。
普通hooks／normalpush；新subject不沿用C28noverify，實際hookblocker交Planner不繞過。
每階段以 `git diff --check`、actual40SHA／parent／namedsolepath／JSONschema／sourcebounds檢查；
planning CLI `python .agents/skills/plan-step-tracker/scripts/step_tracker.py check_impl_steps_succeeded loaded-runtime-cache`
draft應exit1（六pending），reviewready才actual0。
Head drift／source drift／missing/invalid required evidence／scope或contractdrift即停相應gate交Planner；
不自改candidate／receipt／head／contract、不自手算approval。

### Reviewer Handoff / Open Questions / Post-merge

C50 D1 verdict：non-trivial — 四ASTscanner行為、fixed-pointgetteridentity、semantic target syntax與完整subject-boundchain；
required spec與step同candidate，不另開topic或Pythonplan。
七 decisions／async-exempt citation／Non-goals／五testcategories／scope／writer／schema已明定，設計疑點 none。
未來classification結果／actualSHA／testresults／threadresolution尚未產生，不預填。
十二locks保持；unlisted三筆open；scope外requirements只inventory／Human一次決定。
Post-merge／release actions：none；Humanalone PRreview／merge／release／postmerge／tag。
```json
{"verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]}}
```
此為independenthandoffschema、非Creator預填receipt。
Workflow state：current_step=c50-phase4.5-factual-alignment；next_step=bounded-alignment-normal-commit-push；
status=COMPLETE（Phase4.5 factual draft handoff only，publish未完成／非Human approval／topiccomplete）。

### C50 Committed RED / New-S Passing Evidence（current review-ready facts）

以下review-ready facts與pending字樣保留當時snapshot；current approval／phase以末尾Phase4.5 facts為準。

C50 exact-five candidate：`579e480c7d2180a235120e0034b5adcffc1642f0`；
approved planning receipt unchanged sole commit：`b1eb6a315664f9bd2ce1bdec0eaf78af9a21612b`。
Test-only RED：`4ce6113d783da3967c55f13bf691b419c5f5bff8`；
factual failing Tester evidence unchanged sole commit：
`a26c3f1b7597903f1b7ee4d3009bf58619f9b9e2`。
RED evidence實記collection／controlsexit0、full c50 exit1；四original rejecting behaviors 的 genuine RED
與既有negative bounds已經 Planner／Tester核對，不以parseerror或expectedfail假裝pass。

New immutable green S：`4aff14e3009f46ba82ee5fe78a11ca05a635db37`；
same-S passing Tester evidence unchanged sole commit：
`6da6292e8a7a2aac726fcca90bfc559cc8ae9928`。
passing T 的三actualcommands（兩scopedpytest檔／Ruff／strictPyright）exit_code均0，writer Tester，
subject精確同newS；不是C47舊subject／旧T/V。
六canonical C50 implementationsteps有同-S passing證據且實際完成；Current／phase review-ready。

本ONLYplan／step factual draft需Implementer separate LOCAL alignmentcommit後，
Planner再核canonicalCLI0並routeIndependent Reviewer。
本記錄不預填自身alignmentSHA／commit結果，不新candidate／receiptchain。
Independent V verdict／V commit、Phase4.5 publish、classification outcome與threadreply／resolve仍pending；
不可由本draft宣告approval或已resolve四threads。原十二locks／新unlisted三筆inventory-only保持。
其餘analysis／spec保留committedcandidate snapshot；先前C50draft-time／pending字樣onlynonroutingprovenance。

### C50 Phase4.5 Alignment / Committed Independent Approval（current publish-in-progress）

Actual review-ready exact-two LOCAL alignment commit：
`f082fab0f47e54d24787122360dfee754ccd6490`。
New S：`4aff14e3009f46ba82ee5fe78a11ca05a635db37`；
same-S passing T sole：`6da6292e8a7a2aac726fcca90bfc559cc8ae9928`；
same-S approved Independent Reviewer V unchanged sole commit：
`7281f494597e3253de0170b0257a3302c2fcde8c`。
V verdict approved／blocking_issues []，writer Independent Reviewer，精確綁同newS與committedpassingT；
不是Human PR approval或merge authorization。六canonicalimplementationsteps完成不變。
Planner核 committed same-S/T/V gate 後route本ONLYplan／step Phase4.5 factual draft。

Current／phase publish-in-progress；本draft需Implementer separate normal alignment commit／push
更新既有PR7，其發布尚未完成，不預填本身SHA／commitpush成功／actualpublishedhead。
發布後由Planner核實actualfixedpublishedhead，IndependentReviewer才依既有C50exact-four分類契約
展開fresh new-S／actual-head classificationpath並獨立判outcomes；不在此預填reply／resolve IDs。
classificationreceipt／solecommit／normalpush／threads actions皆pending。
十二semanticlocks／newunlisted三筆inventory-only保留，production／ArchitectureVisualization／contracts不變。
不新candidate／receiptchain；analysis／spec保留candidate snapshots，earlierpendingfacts為時點provenance。
