# Loaded Runtime Cache — Technical Specification

## Boundary model

Loaded Runtime Cache 和 Identity BC 是獨立 BC。Identity BC 擁有 `ModelIdentity`（「這是哪個模型」）；
Loaded Runtime Cache 擁有 `RuntimeReuseKey`（「以何種本地 key 定位可重用 runtime」）。兩者既不相同、
不 re-export，也不以 direct import、duplicate type、dynamic import 或 `sys.modules` substitution 假裝共用。此禁令
同時涵蓋直接 `importlib.import_module`、直接 `__import__`，以及 `importlib` 或 `builtins.__import__` 的 alias／
module-alias 呼叫。

外部 integration／ACL boundary（本 topic 不實作）如有需要，才負責將確認的 model identity 映射成
`RuntimeReuseKey`。Loaded Runtime Cache 接收 key 後只原樣傳遞；它不觀察 key 的欄位或語意。
`RuntimeReuseKey` construction token 不是本 BC 的 public contract：它只由該 external boundary 建立，不能以
`str`、hash 或可序列化 token 取代。任何 implementation 的 `repr` 亦不得暴露 token。

## Executable contract surface

`RuntimeT` 是已初始化、可保留的實際 runtime，例如 model object、inference engine 或 provider session。
所有 contracts 為 synchronous generic Protocol／immutable outcome type；不引入 concrete class 或 DI composition。

```python
class RuntimeRegistry[RuntimeT](Protocol):
    def lookup(self, key: RuntimeReuseKey) -> RuntimeT | None: ...

    def retain(self, key: RuntimeReuseKey, runtime: RuntimeT) -> None: ...


class RuntimeRetention[RuntimeT](Protocol):
    def retain(
        self,
        key: RuntimeReuseKey,
        runtime: RuntimeT,
    ) -> Retained[RuntimeT] | NotRetained[RuntimeT]: ...
```

- `RuntimeReuseKey` 是 nominal、immutable、opaque type；其 construction token 由 external integration／ACL 決定，
  且只作為 external boundary 的 construction detail。lookup／retention logic、ports 與 tests 均不得讀取或斷言
  token 內部欄位，並不得把 `str` 或 hash 納入 API 或由 `repr` 暴露。key 的相等／hash 行為不得委派到 token：即使
  token unhashable 或自訂 equality，key 仍採 instance identity semantics，且不得呼叫 token equality／hash。
- `Available[RuntimeT](runtime)`、`Missing()`、`Unavailable()` 是 lookup outcome contracts；
  `Retained[RuntimeT](runtime)`、`NotRetained[RuntimeT](runtime)` 是 retention outcomes。
- `registry/runtime_registry_port.py` 擁有 expected lookup operational-failure signal
  `RuntimeRegistryLookupUnavailable`。Registry 在該預期失敗時原樣 raise；`RuntimeT | None` 只代表
  hit／missing。`lookup/lookup_outcome.py` 擁有 `Unavailable()`；本 topic 不提供兩者 mapping。
- `RuntimeRetention` 是 outcome-facing reuse protocol。若未來確認可替換 dependency／DI 需求，另開 topic 實作
  例如 `RegistryRuntimeRetention`；本 topic 不預先宣告或實作該 class。

## Fixed module taxonomy

新增 modules 必須只在下列 BC／topic／child-topic paths；不新增 package initializer、root export 或 facade：

```text
src/deterministic_response_cache/loaded_runtime_cache/runtime_reuse/
  registry/runtime_reuse_key.py
  registry/runtime_registry_port.py
  lookup/lookup_outcome.py
  retention/runtime_retention.py
  retention/retain_outcome.py
```

registry 只放 local key 與 Registry internal port；lookup 只放 lookup outcomes；retention 只放 Retention
Protocol 與 retention outcomes。不得使用 `service.py`、`utils.py`、`common.py`，或把不同 child-topic 的
port、outcome、application logic、adapter 平鋪於 topic package root。

## Behavioral / error constraints

1. lookup／retain key parameter 恰為 `RuntimeReuseKey`，不接受 `object`、`str`、hash 或 `ModelIdentity`
   placeholder。
2. Registry hit 是 `RuntimeT`，missing 是 `None`；port 不負責 runtime construction、download、initialization、
   unload 或 execution。
3. `RuntimeRetention` success／failure outcomes 都攜帶同一 `runtime` instance。
4. Loaded Runtime Cache 不得 import `deterministic_response_cache.identity` 或其任何 module；Identity BC 同樣
   不得 import Loaded Runtime Cache。BC-independence regression 必須覆蓋 direct import、直接
   `importlib.import_module`、直接 `__import__`、`importlib` 或 `builtins.__import__` alias／module-alias，以及
   `sys.modules` substitution，且 parser 必須解析 aliases，不能以其中任一方式規避。
5. expected lookup failure 的唯一 signal 是 `RuntimeRegistryLookupUnavailable`，不得以 `Missing()`、
   `Unavailable()` 或 silent swallow 代替；non-expected exceptions 原樣 propagate。
6. Python target 維持 3.12，strict pyright；不新增 dependency、`Any`、cast 或 runtime introspection。

## Archify contract

資料流圖使用 `backend` 作為 Archify 的結構／視覺分類，但 label 必須明寫
`Loaded Runtime Cache protocol（contract only）`，並以圖說或 relationship label 明示
`僅 Protocol；無 concrete backend、DI、runtime lifecycle`。ACL node 為外部／未實作 boundary，不代表 mapper、
backend 或 lifecycle 已交付。authors labels 使用繁體中文；不設定 `meta.locale`，並如實揭露 viewer UI fallback
為英文。retain 的 input relationship 必須明示 `RuntimeReuseKey`；dashed relationship 僅能表示明確 async
flow，synchronous retain failure 必須使用非-dashed outcome relationship。最終必須是 showcase 9/9、0 composition
errors、0 warnings，後續才 deliver，並 visual-check 四個 desktop viewports。

## Completed C11 execution order

1. C5→V3 已提交的 architecture authority、dataflow delivery／visual evidence 與 source contracts 均是 frozen
   provenance。C8、C9 與 C10 是 frozen、unapproved predecessor planning provenance，沒有 routing authority。C11 在既有
   source ancestor 上進行；不得重跑為新的 architecture gate、不得改寫五份 authority path，
   也不得假裝重新經歷 source-absent 的 RED→green 歷程。
2. C11 approved Plan-Reviewer receipt committed 後，Implementer 只可修改
   `tests/test_loaded_runtime_cache_contracts.py` 與
   `tests/test_loaded_runtime_cache_bc_independence.py`，各新增一個 isolated executable RED assertion。它們在現行
   source ancestor 可執行，並覆蓋 opaque-key identity、direct `importlib.import_module`、direct `__import__`、
   alias/module-alias bypass 和 duplicate semantic type 的五類 regression。
3. 該兩-path assertion subject 是新的 immutable implementation subject；它不得包含 production source、architecture
   或 evidence。其命名中的 RED 只識別 review repair，並不代表 expected-nonzero 或 historical red failure。Tester 對
   相同 subject 建立 T11，Independent Reviewer 只在 committed passing T11 後建立 V11；V11 approved 後才可進入 Planner
   Phase 4.5 與 thread classification。

## Deterministic validation evidence boundary

There is no C11 RED-evidence artifact. The assertions are factual executable regression checks against the existing
source ancestor. Their commands and exit codes are recorded only in T11 after the immutable assertion subject exists.
A failing command is `failing` Tester evidence and returns only to Implementer; it cannot be renamed
`expected-failing`, converted into green-work authorization, or used to rewrite frozen C5→V3 provenance.

Tester only records factual evidence for one immutable implementation subject. Its JSON has exactly
`schema_version`, `topic`, `implementation_subject_commit`, `status`, `commands`, `recorded_by`; it uses
`schema_version: 1`, topic `loaded-runtime-cache`, a full 40-hex subject SHA, `passing|failing`, a non-empty command /
integer-exit-code list, and `recorded_by: Tester`. Passing requires every exit code be zero; failing requires at least
one non-zero exit code.

Independent Reviewer can consume only the separately committed, same-topic, same-subject passing Tester evidence. Its
JSON has exactly `schema_version`, `topic`, `implementation_subject_commit`, `tester_evidence_commit`, `verdict`,
`blocking_issues`, `recorded_by`; it uses `schema_version: 1`, full 40-hex subject and Tester-evidence commit SHAs,
`approved|needs-rework`, a string blocker list that is empty only for approved, and
`recorded_by: Independent Reviewer`. Malformed, extra-key, mismatched, uncommitted, failing, or abbreviated evidence
fails closed; it cannot yield Reviewer evidence or implementation routing.

The C11 successor records must be written only to immutable versioned paths
`loaded-runtime-cache.tester-evidence-<implementation-subject-40-hex-sha>.json` and
`loaded-runtime-cache.implementation-review-log-<implementation-subject-40-hex-sha>.json`. They must not overwrite,
reuse, or be inferred from C5/T3/V3 or legacy `6110cb…` Tester／`44e477…` Reviewer evidence lineage.

## Completed C11 candidate routing constraint

C11 只包含 `analysis/loaded-runtime-cache/{requirements,technical-spec}.md` 與
`plan/loaded-runtime-cache/loaded-runtime-cache.{plan,spec,step}.md` 五份 planning artifacts。後續 routing 必須將它
帶到現行 source ancestor；C11 不得攜帶 source、tests、architecture、Tester／Reviewer evidence 或 receipts。C11
candidate-only commit、R11 receipt、S11、T11 和 V11 都已完成；它們現在是 immutable frozen provenance，不再是
current routing authority。

## Completed C12 review-triage provenance

C12 was the completed planning successor and only modified
`analysis/loaded-runtime-cache/{requirements,technical-spec}.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.{plan,spec,step}.md`。它不得修改 production source、tests、architecture
authority、Archify source／receipt、既有 evidence 或 PR thread state。C12 candidate commit 完成後，唯一下一 gate 是
independent R12 Plan-Reviewer receipt；本文件不預填 candidate SHA 或 receipt path。

R12 必須審核固定 PR snapshot commit
`73644c2b88257832e1b4d8bedaf516b803c2ee3a`，並在非空 `copilot_feedback_triage` 中以 factual entry 完整覆蓋每個
current unresolved thread。每個 entry 恰有 `thread`、`comment`、`finding`、`commit`、`basis`、`disposition`；`commit`
只能是固定 snapshot 或可驗證的 completed C11/R11/S11/T11/V11 provenance commit，不能使用 abbreviated SHA 或
future commit。F `PRRT_kwDOUJTij86jnBpk`／comment `4043480108` 與 architecture/ACL thread
`PRRT_kwDOUJTij86kQ95O`／comment `4060023123` 必須列於 `DISCUSS`，disposition 為 Human-only `human-check`；其餘
snapshot entries 列於 `SKIP`，且不得假裝已由 C12 修改、reply 或 resolve。

## C14 truthful-artifact correction execution contract

1. C13 candidate `a623981989f3363a4b225319a432c3a9d8e28b96`、R13 `cf91b55f80f1764e040c95c822ae55b290e3699c`、RED `3ba583bed8c367b756e2cb450e468f1274d04193`、failing evidence `c4f229f14d3c4c38d40cdda8ad0429712e0ae189` 與
   `ade584e7eb63a7846a23c073c06a802ff99ff6cf` are frozen provenance; the last is `needs-rework` and cannot route.
   C14 candidate is planning-only and changes exactly the five planning artifacts. It contains no candidate SHA,
   receipt path, implementation subject SHA, evidence, test result, or approval outcome. Independent Plan-Reviewer
   must create a fresh SHA-bound `approved` receipt; Implementer commits that unchanged receipt alone.
2. The first C14 implementation subject is a RED test-only subject that changes only
   `tests/test_loaded_runtime_cache_bc_independence.py`. It must collect successfully and contain an assertion that
   actually fails for a chained assignment import-alias bypass. It neither replays nor rewrites historical `e2e125`
   evidence. Tester records the actual non-zero command result in a new SHA-bound failing evidence record; no
   Reviewer evidence may be created from failing Tester evidence.
3. A later new green immutable subject changes only that same BC-independence test and a truthful changed subset of
   this sole allowed Archify artifact set: `loaded-runtime-cache.dataflow.json`, `.html`, `.validation.json`, `.delivery.json`,
   `.visual-check.json`, `.visual-check.html`, `.visual-check.1440x900.dark.png`,
   `.visual-check.1440x900.light.png`, `.visual-check.2048x1320.dark.png`, and
   `.visual-check.2048x1320.light.png`, all below `docs/architecture/loaded-runtime-cache/`. A byte-identical
   rebuild of `.validation.json` or `.visual-check.html` remains ReadOnly and must not be rewritten merely to fill
   the allowlist.
4. The green test repair must reject every chained-assignment import alias whose assignment targets are all simple
   names; it must not introduce dynamic import, runtime introspection, or a source/BC-boundary workaround. Archify
   dataflow must show retain inputs `RuntimeReuseKey + runtime`, return labels `Retained(runtime)` and
   `NotRetained(runtime)`, corrected edge placement, and truthful validate/deliver/visual-check receipts. Visual-check
   must cover containment at 1440×900, 1600×1000, 1920×1080, and 2048×1320; only the four listed existing PNG
   captures may be updated.
5. The five Human-owned architecture authority paths remain read-only. F and ACL threads remain open Human-only
   `human-check`. After a passing green Tester evidence commit and approved independent Reviewer evidence commit,
   Planner performs Phase 4.5 then routes a new independent thread classification; neither correction evidence nor
   Phase 4.5 resolves a thread directly.

## C14 evidence schemas and fail-closed ordering

The C14 RED factual record path is
`plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<red-subject-40-hex-sha>.json`. The green factual
record uses `loaded-runtime-cache.tester-evidence-<green-subject-40-hex-sha>.json`, and only the green review record
uses `loaded-runtime-cache.implementation-review-log-<green-subject-40-hex-sha>.json`. Every placeholder is the
respective immutable subject's full 40-character lowercase hexadecimal SHA; no fixed-name, predecessor, abbreviated,
or overwritable path is valid.

Tester alone writes each factual JSON object with exactly `schema_version`, `topic`, `implementation_subject_commit`,
`status`, `commands`, `recorded_by`. Values must be integer `1`, `loaded-runtime-cache`, that full subject SHA,
`passing|failing`, a non-empty array of objects containing only non-empty string `command` and integer `exit_code`, and
`Tester`. `passing` requires all exits `0`; `failing` requires at least one non-zero exit. Thus the RED subject must
produce a committed `failing` record and the distinct green subject must produce a committed `passing` record.

Only Implementer may commit a Tester or review record, unchanged and in its own sole evidence-only commit. Independent
Reviewer may write only the green JSON object with exactly `schema_version`, `topic`, `implementation_subject_commit`,
`tester_evidence_commit`, `verdict`, `blocking_issues`, `recorded_by`; the two references are full 40-hex SHAs,
`verdict` is `approved|needs-rework`, `blocking_issues` is a string array empty exactly for `approved`, and
`recorded_by` is `Independent Reviewer`. It may consume only the committed sole evidence-only green Tester commit with
same topic, same subject, and `passing` status. Failing RED evidence, malformed JSON, any extra/missing key, wrong
role, wrong path, uncommitted or non-sole evidence, cross-subject/topic evidence, or an abbreviated SHA fails closed;
it produces no Reviewer record and no next gate.

C5→V3, C11→V11, C12→R12 and
`9aa656b13fdc36492273c97a62eb9d422a1b64b5` are immutable provenance only. The last is an unapproved
`needs-rework` planning record and cannot supply a C14 candidate, Plan-Reviewer receipt, implementation subject, or
evidence authority.

## C15 mixed-assignment execution contract (current routing)

C15 supersedes C14 only as current routing. It preserves all existing Loaded Runtime Cache protocol and BC
independence constraints. Its sole implementation file is
`tests/test_loaded_runtime_cache_bc_independence.py`.

For one `ast.Assign`, static alias collection inspects direct `assignment.targets` only. Each direct `ast.Name` is a
local alias. Each direct `ast.Attribute` or other non-simple target is ignored; no target is recursively traversed.
Thus `load = holder.loader = importlib.import_module` retains `load` and excludes `holder.loader`, so a later direct
`load(...)` invocation remains detectable. The correction is static syntax analysis only: AST execution/evaluation,
dynamic import, `importlib`／`__import__`／`sys.modules` substitution, runtime introspection, source edits and cross-BC
imports are forbidden.

C15 order is strict: five-artifact candidate (no future SHA/outcome prefill) → independent approved receipt at
`loaded-runtime-cache.plan-review-receipt-<planning-candidate-40-hex-sha>.json` → receipt-only commit → fresh
collection-success/assertion-failing RED test-only subject → factual `failing` Tester evidence at
`loaded-runtime-cache.tester-evidence-<red-subject-40-hex-sha>.json` → distinct green test-only subject → factual
`passing` Tester evidence at `loaded-runtime-cache.tester-evidence-<green-subject-40-hex-sha>.json` → approved
independent review evidence at `loaded-runtime-cache.implementation-review-log-<green-subject-40-hex-sha>.json` →
Planner Phase 4.5 → fresh independent thread classification. All paths are templates only; no SHA is prefilled.
Tester/reviewer schemas and sole-evidence-commit requirements remain as defined above; a failing RED record produces
no Reviewer record.

C14 and `37d7233e7231151c0dac6aaa1a7820bff746ffdc` are frozen nonrouting provenance. F／ACL/business architecture
remain Human-only `human-check`; no C15 artifact or phase may reply, resolve, approve, merge, release or post-merge.

## C16 immutable C15 thread-classification receipt contract

C16 is a planning-only successor. Its candidate changes exactly the five planning artifacts and must receive a fresh,
committed, candidate-SHA-bound `approved` Plan-Reviewer receipt before classification. It creates no RED/green subject,
Tester record, implementation-review record, source, test, documentation, architecture, Archify, PR reply, resolution,
publish, merge, release or post-merge action.

After that approved planning receipt, only Independent Reviewer may write the one JSON object at
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-7dab2b9742bd19f962bef99be83b40b978f87f0f.json`.
Only Implementer may commit that exact unchanged file, in one sole evidence-only commit. The object top-level keys are
exactly `schema_version`, `topic`, `implementation_subject_commit`, `tester_evidence_commit`,
`implementation_review_evidence_commit`, `pr_head_commit`, `classifications`, `recorded_by`. Their values are exactly:
integer `1`; `loaded-runtime-cache`; C15 subject
`7dab2b9742bd19f962bef99be83b40b978f87f0f`; Tester-evidence commit
`475e3c953f6551bef5834d0bf350d5c79449a43e`; implementation-review-evidence commit
`cee5097c176b4321a0d9bc2e810caf7d3425d0f1`; PR snapshot
`7e525b1ad8dc77c25b0b11a467f6b1f24884ecd3`; an array of exactly seven entries; and `Independent Reviewer`.

Every classification entry has exactly `thread`, `comment`, `outcome`, `reply`. The seven `thread`/`comment` pairs are
exactly `PRRT_kwDOUJTij86kQ95O`/`4060023123`, `PRRT_kwDOUJTij86kqiZu`/`4070096548`,
`PRRT_kwDOUJTij86kqiZ5`/`4070096561`, `PRRT_kwDOUJTij86lAR8J`/`4078761983`,
`PRRT_kwDOUJTij86lAR8P`/`4078761993`, `PRRT_kwDOUJTij86lAR8T`/`4078761998`, and
`PRRT_kwDOUJTij86lAR8Y`/`4078762005`, with no duplicate or extra pair. `outcome` is exactly one of
`REPLY_AND_RESOLVE`, `ADDRESS`, `HUMAN_CHECK`. `reply` is a non-empty string only for `REPLY_AND_RESOLVE`; it is JSON
`null` for `ADDRESS` and `HUMAN_CHECK`. The ACL pair `4060023123` and business-architecture pair `4070096561` are
locked `HUMAN_CHECK` with `reply: null`; Independent Reviewer must independently classify the other five pairs and
the candidate must not prefill their outcome/reply.

Malformed keys, wrong writer, wrong/full-SHA mismatch, altered sole evidence, uncommitted evidence, a missing/extra
pair, a forbidden reply, or a reference that is not a committed C15 ancestor fails closed. A committed classification
receipt only routes exact `REPLY_AND_RESOLVE` pairs to an Implementer for that exact reply and resolution. Any
`ADDRESS` returns routing to Planner for a new successor; `HUMAN_CHECK` stays open and is never replied to or resolved.

## C17 ADDRESS-remediation execution contract

C16's committed classification receipt is frozen C17 input. C17 addresses only `4078761993` and `4078762005`; it
does not change C15/C16 records, public surface, or any other disposition. `4078761998` is explicitly Human-only:
`README.md` is ReadOnly.

The route is five candidate artifacts → independently written/sole-committed candidate-SHA-bound approved receipt →
test-only collection-success/assertion-failing RED subject → sole factual failing Tester evidence → distinct green
subject → sole passing Tester evidence → sole approved Independent Reviewer evidence → Planner Phase 4.5 → new
independent classification. RED changes only `tests/test_loaded_runtime_cache_bc_independence.py`; green changes that
test and only byte-truthfully changed paths from the explicit dataflow allowlist. No stage preclaims reply/resolve.

The test scanner must statically recognise a direct assignment expression of the form
`getattr(<known-importlib-or-sys-module-alias>, <literal-forbidden-attribute>)`: `import_module` for `importlib`,
`modules` for `sys`. A later local alias use is rejected. It may not evaluate `getattr`/AST, dynamically import,
inspect runtime modules, recurse arbitrary expressions, alter production source, or replace direct imports.

The sole documentation allowlist is:

- `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.json`
- `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.html`
- `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.validation.json`
- `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.delivery.json`
- `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.json`
- `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.html`
- `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.1440x900.dark.png`
- `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.1440x900.light.png`
- `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.2048x1320.dark.png`
- `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.2048x1320.light.png`

Regenerate rather than hand-edit evidence: `archify validate dataflow … --quality showcase --json`, then
`archify deliver dataflow … --quality showcase --json`, then `archify visual-check … --repo-root <repository-root>
--json`. Validate must be 9/9, zero composition errors/warnings; visual-check must be non-skipped and record
1440×900, 1600×1000, 1920×1080 and 2048×1320. Byte-identical output remains ReadOnly; non-zero or skipped fails
closed. Authored labels retain `RuntimeRegistry.lookup(key: RuntimeReuseKey) -> RuntimeT | None`; no
`Available`/`Missing` lookup return or mapper is shown.

Existing full-SHA Tester/Independent Reviewer schemas and sole-evidence commits apply unchanged; C17 must not
prefill a SHA, result or verdict.

## C18 current-head classification receipt contract

C18 是唯一的 C17 post-evidence classification successor。它只建立五份 planning artifacts 的 candidate、標準
candidate-SHA-bound Plan-Reviewer receipt，以及一份 C17-bound classification receipt；不建立或修改 implementation
subject、Tester/Reviewer evidence、source、tests、docs、Archify、README、PR reply 或 resolution。

Candidate committed 後，Independent Plan-Reviewer 的唯一 receipt template 是
`plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<planning-candidate-40-hex-sha>.json`；僅
approved receipt 的 unchanged sole receipt-only commit 可路由 classification。Independent Reviewer 之唯一
classification writer path 是
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-7ceb3409d6d8b9ff3dc51485c3588f502bdff882.json`；
僅 Implementer 可將它 unchanged 且作 sole evidence-only commit 提交。

classification JSON has exactly `schema_version`, `topic`, `implementation_subject_commit`,
`tester_evidence_commit`, `implementation_review_evidence_commit`, `pr_head_commit`, `classifications`,
`recorded_by`. Its fixed values are integer `1`, `loaded-runtime-cache`, subject
`7ceb3409d6d8b9ff3dc51485c3588f502bdff882`, Tester commit
`b58cb1e330fe12ccc80a8f39b875a61ea6024067`, Reviewer commit
`edbae51a0ee86cff498d6caf4e6aa78b58962a82`, PR head
`bf63a3c6a0533ad0f367305deff029eddc2b18be`, an exactly eleven-entry `classifications` array, and
`Independent Reviewer`.

Each entry has exactly `thread`, `comment`, `outcome`, `reply`. Its exact eleven pair set is:

1. `PRRT_kwDOUJTij86jnBpk` / `4043480108` (F; locked `HUMAN_CHECK`, `null`)
2. `PRRT_kwDOUJTij86jqdPV` / `4044836129`
3. `PRRT_kwDOUJTij86jqdPZ` / `4044836136`
4. `PRRT_kwDOUJTij86kOjjo` / `4059094458`
5. `PRRT_kwDOUJTij86kQ95O` / `4060023123` (ACL; locked `HUMAN_CHECK`, `null`)
6. `PRRT_kwDOUJTij86kqiZu` / `4070096548`
7. `PRRT_kwDOUJTij86kqiZ5` / `4070096561` (business architecture; locked `HUMAN_CHECK`, `null`)
8. `PRRT_kwDOUJTij86lAR8J` / `4078761983`
9. `PRRT_kwDOUJTij86lAR8P` / `4078761993`
10. `PRRT_kwDOUJTij86lAR8T` / `4078761998` (README; locked `HUMAN_CHECK`, `null`)
11. `PRRT_kwDOUJTij86lAR8Y` / `4078762005`

The other seven outcomes and replies are deliberately not planned. Independent Reviewer determines them in the
committed receipt. `REPLY_AND_RESOLVE` requires a non-empty factual reply; `ADDRESS` and `HUMAN_CHECK` require
JSON `null`. Only an exact committed `REPLY_AND_RESOLVE` entry lets Implementer leave that exact reply and resolve
that exact thread. `ADDRESS` returns to Planner; each `HUMAN_CHECK` stays open. Missing/extra keys or pairs,
wrong role/path/reference, non-ancestor evidence, non-sole commit, invalid enum, or invalid reply nullability fails
closed.

## C19 current-head reconciliation classification receipt contract

C19 supersedes C18 only as current routing. It is planning-only and creates a fresh standard Plan-Reviewer receipt
plus one C17-bound current-head classification/reconciliation receipt. It creates or modifies no implementation
subject, Tester/Reviewer evidence, source, test, documentation, architecture, Archify, README, PR reply or
resolution before its exact committed classification entry authorizes that action.

The C19 candidate is exactly the five planning artifacts and pre-fills no candidate SHA, verdict, classification
outcome, reply or resolution. After a committed approved standard candidate-SHA-bound Plan-Reviewer receipt, only
Independent Reviewer may write
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-7ceb3409d6d8b9ff3dc51485c3588f502bdff882-3e803a507b2dfa74efdf71164c260da172aadb81.json`.
Only Implementer may commit that unchanged file in one sole evidence-only commit.

The receipt has exactly `schema_version`, `topic`, `implementation_subject_commit`, `tester_evidence_commit`,
`implementation_review_evidence_commit`, `pr_head_commit`, `classifications`, `recorded_by`. Their values bind
schema `1`, topic `loaded-runtime-cache`, C17 subject `7ceb3409d6d8b9ff3dc51485c3588f502bdff882`, Tester-evidence
commit `b58cb1e330fe12ccc80a8f39b875a61ea6024067`, review-evidence commit
`edbae51a0ee86cff498d6caf4e6aa78b58962a82`, current PR head `3e803a507b2dfa74efdf71164c260da172aadb81`, exactly five
classifications, and writer `Independent Reviewer`.

Each classification has only `thread`, `comment`, `outcome`, `reply`; its exact pair set is
`PRRT_kwDOUJTij86lCkFr`/`4079664571`, `PRRT_kwDOUJTij86lCkFu`/`4079664575`,
`PRRT_kwDOUJTij86lDH2-`/`4079885261`, `PRRT_kwDOUJTij86lDH3C`/`4079885267`, and
`PRRT_kwDOUJTij86lAR8Y`/`4078762005`. For the first four pairs, Independent Reviewer alone chooses
`REPLY_AND_RESOLVE`, `ADDRESS`, or `HUMAN_CHECK`; the candidate supplies no outcome or reply. For `lAR8Y`, Reviewer
first reconciles its GitHub current state. It may use `ALREADY_RESOLVED` only if that observed state proves resolution;
that outcome requires `reply: null`, is exclusive to `lAR8Y`, and authorizes no action. Otherwise it independently
selects one general outcome. `REPLY_AND_RESOLVE` requires a non-empty factual reply; every other outcome requires
`null`. The four pre-existing Human-only pairs are excluded and remain untouched/open. Any malformed, extra, stale,
non-sole, cross-subject, wrong-head, wrong-pair, invalid-enum or invalid-nullability record fails closed.

## C20 C19 ADDRESS remediation execution contract

C20 is the only bounded successor for C19 `ADDRESS` pairs `lCkFu`/`4079664575` and `lDH2-`/`4079885261`. Its
candidate is exactly the five planning artifacts. A standard immutable
`loaded-runtime-cache.plan-review-receipt-<planning-candidate-40-hex-sha>.json` approved receipt must be written by
Independent Plan-Reviewer and unchanged-sole-committed by Implementer before any C20 implementation subject.

The RED subject modifies only `tests/test_loaded_runtime_cache_bc_independence.py`, collects successfully, and makes
two newly introduced assertions fail: (1) a temporary Loaded Runtime Cache source containing
`from deterministic_response_cache.identity.contracts import ModelIdentity as LocalModelIdentity` is rejected as a
foreign semantic-type alias, and (2) the topic dataflow contract contains a distinct
`RuntimeRegistryLookupUnavailable` expected-failure signal rather than treating it as the `RuntimeT | None` lookup
union. RED Tester evidence is factual, SHA-bound and `failing`; it is not Reviewer evidence.

The distinct green subject may modify only that test and these exact topic dataflow outputs:

1. `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.json`
2. `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.html`
3. `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.validation.json`
4. `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.delivery.json`
5. `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.json`
6. `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.html`
7. `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.1440x900.dark.png`
8. `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.1440x900.light.png`
9. `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.2048x1320.dark.png`
10. `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.2048x1320.light.png`

The JSON must retain the normal lookup contract `RuntimeRegistry.lookup(key: RuntimeReuseKey) -> RuntimeT | None`
and add a distinct expected-failure signal labelled `RuntimeRegistryLookupUnavailable`; no flow, node, label or card
may connect/translate that signal to `Available`、`Missing`、`Unavailable` or any mapper. The scanner check is AST-only
and only forbids an `ImportFrom` from the Identity BC that imports `ModelIdentity`, including an `as` local alias; it
does not execute a fixture, use `importlib`/`__import__`/`sys.modules`, or redefine Identity semantics.

All generated artifacts must be byte-truthful command outputs: `archify validate dataflow … --quality showcase --json`
must report 9/9, 0 composition errors and 0 warnings; only then may `deliver` run, followed by non-skipped
`visual-check … --repo-root <repository-root> --json` that records 1440×900, 1600×1000, 1920×1080 and 2048×1320.
Unchanged listed output remains ReadOnly; hand editing receipts or sidecars is forbidden.

After a same-subject passing Tester evidence commit, approved independent Reviewer evidence commit, and Planner
Phase 4.5 alignment, Independent Reviewer alone may write the immutable
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-<c20-green-subject-40-hex-sha>.json`.
It has exactly eight top-level keys: `schema_version`, `topic`, `implementation_subject_commit`,
`tester_evidence_commit`, `implementation_review_evidence_commit`, `pr_head_commit`, `classifications`, and
`recorded_by`; it binds C20's actual full SHA facts and has exactly two entries, each with only `thread`, `comment`,
`outcome`, `reply`, for `lCkFu`/`4079664575` and `lDH2-`/`4079885261`. Independent Reviewer alone chooses
`REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK`; only the first has a non-empty factual reply. Implementer alone may
unchanged-sole-commit the receipt. No outcome, reply, PR head, subject or evidence SHA is prefilled by C20 planning.

## C21 current-head single-pair classification receipt contract

C21 is planning-only and is the sole successor authorized to classify
`PRRT_kwDOUJTij86ldYVf`/`4090457782` at current head `a1aae44897c0f0b0ac52f1ca1697554c2f79cdb5`. It consumes only C20
subject `fa1468301af1906a05ee31ba0d267d2270d7af5f`, passing Tester-evidence commit
`6423f55b6dbcde5bee190ef86dc8c31f5c27c94e`, and approved implementation-review-evidence commit
`3d0dc9fbb0e9da6d742ac20856b8aac6b0a3035e`; it creates no implementation subject, Tester/Reviewer evidence, source,
test, documentation, architecture, Archify, PR reply or resolution before its exact committed classification entry
authorizes action.

The C21 candidate is exactly the five planning artifacts and pre-fills no candidate SHA, verdict, classification
outcome, reply or resolution. After a committed approved standard candidate-SHA-bound Plan-Reviewer receipt, only
Independent Reviewer may write
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-fa1468301af1906a05ee31ba0d267d2270d7af5f-a1aae44897c0f0b0ac52f1ca1697554c2f79cdb5.json`.
Only Implementer may commit that unchanged file in one sole evidence-only commit.

The receipt has exactly `schema_version`, `topic`, `implementation_subject_commit`, `tester_evidence_commit`,
`implementation_review_evidence_commit`, `pr_head_commit`, `classifications`, `recorded_by`. Their values bind
schema `1`, topic `loaded-runtime-cache`, the four C20/current-head full 40-hex SHAs above, exactly one
classification, and writer `Independent Reviewer`. Its one entry has only `thread`, `comment`, `outcome`, `reply`
and is exactly `PRRT_kwDOUJTij86ldYVf`/`4090457782`. Independent Reviewer alone chooses
`REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK`; only `REPLY_AND_RESOLVE` has a non-empty factual reply. Every other outcome
uses JSON `null`. Only the exact committed `REPLY_AND_RESOLVE` entry permits Implementer to leave that exact reply
and resolve that exact thread. `ADDRESS` returns to Planner; `HUMAN_CHECK` remains open. Any malformed, extra,
stale, non-sole, cross-subject, wrong-head, wrong-pair, invalid-enum or invalid-nullability record fails closed.

## C22 current-head dual-pair classification receipt contract

C22 is planning-only and is the sole successor authorized to classify
`PRRT_kwDOUJTij86ldeVI`/`4090495760` and `PRRT_kwDOUJTij86ldeVO`/`4090495770` at current head
`0991c56ec7e562ea512449bda1a41118dbc48203`. It consumes only C20 subject
`fa1468301af1906a05ee31ba0d267d2270d7af5f`, passing Tester-evidence commit
`6423f55b6dbcde5bee190ef86dc8c31f5c27c94e`, and approved implementation-review-evidence commit
`3d0dc9fbb0e9da6d742ac20856b8aac6b0a3035e`; it creates no implementation subject, Tester/Reviewer evidence, source,
test, documentation, architecture, Archify, PR reply or resolution before its exact committed classification entry
authorizes action.

The C22 candidate is exactly the five planning artifacts and pre-fills no candidate SHA, verdict, classification
outcome, reply or resolution. After a committed approved standard candidate-SHA-bound Plan-Reviewer receipt, only
Independent Reviewer may write
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-fa1468301af1906a05ee31ba0d267d2270d7af5f-0991c56ec7e562ea512449bda1a41118dbc48203.json`.
Only Implementer may commit that unchanged file in one sole evidence-only commit.

The receipt has exactly `schema_version`, `topic`, `implementation_subject_commit`, `tester_evidence_commit`,
`implementation_review_evidence_commit`, `pr_head_commit`, `classifications`, `recorded_by`. Their values bind
schema `1`, topic `loaded-runtime-cache`, the four C20/current-head full 40-hex SHAs above, exactly two
classifications, and writer `Independent Reviewer`. Each entry has only `thread`, `comment`, `outcome`, `reply`; its
exact pair set is `PRRT_kwDOUJTij86ldeVI`/`4090495760` and `PRRT_kwDOUJTij86ldeVO`/`4090495770`. Independent Reviewer
alone chooses `REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK`; only the first has a non-empty factual reply. Every other
outcome uses JSON `null`. Only the exact committed `REPLY_AND_RESOLVE` entry permits Implementer to leave that exact
reply and resolve that exact thread. `ADDRESS` returns to Planner; `HUMAN_CHECK` remains open.

F `PRRT_kwDOUJTij86jnBpk`/`4043480108`, ACL `PRRT_kwDOUJTij86kQ95O`/`4060023123`, business
`PRRT_kwDOUJTij86kqiZ5`/`4070096561`, README `PRRT_kwDOUJTij86lAR8T`/`4078761998`, and new
`PRRT_kwDOUJTij86ld9Ai` are excluded from C22 and remain open; the four former pairs are Human-only locks. Any
malformed, extra, stale, non-sole, cross-subject, wrong-head, wrong-pair, invalid-enum or invalid-nullability record
fails closed.

## C23 bounded ADDRESS remediation contract

C23 remediates only C22 ADDRESS pairs `PRRT_kwDOUJTij86ldeVI`/`4090495760` and
`PRRT_kwDOUJTij86ldeVO`/`4090495770`. It consumes only committed C22 classification receipt
`a9065a8332119930347214f07f2980d655d8d314` at
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-fa1468301af1906a05ee31ba0d267d2270d7af5f-0991c56ec7e562ea512449bda1a41118dbc48203.json`,
which binds C20 subject `fa1468301af1906a05ee31ba0d267d2270d7af5f`, passing Tester evidence
`6423f55b6dbcde5bee190ef86dc8c31f5c27c94e`, approved Reviewer evidence
`3d0dc9fbb0e9da6d742ac20856b8aac6b0a3035e`, and C22 PR head `0991c56ec7e562ea512449bda1a41118dbc48203`.
The candidate is exactly the five planning artifacts and creates no source, test, dataflow, receipt, evidence, PR
reply or resolution fact. An Independent Plan-Reviewer writes a fresh approved candidate-SHA-bound standard receipt;
Implementer commits that unchanged file alone before any implementation.

The RED subject must collect successfully and fail an assertion for both defects: the dataflow must retain
`RuntimeRegistry.lookup(key: RuntimeReuseKey) -> RuntimeT | None` and only the expected-failure relationship
`RuntimeRegistry -> RuntimeRegistryLookupUnavailable`, with no lookup connection to `Available`, `Missing`,
`Unavailable` or any mapper; the static BC-independence scanner must reject the alias created by
`(load := importlib.import_module)(...)`. The scanner parses only an `ast.NamedExpr` direct `ast.Name` target and its
value. It preserves the existing direct-assignment rule that retains `load` but ignores `holder.loader` in
`load = holder.loader = importlib.import_module`; it executes neither fixture nor dynamic import.

Tester records a new full-SHA-bound factual `failing` RED record. Only after its unchanged sole evidence-only commit
may Implementer create a distinct green subject. Green is limited to the scanner test and the dataflow JSON/HTML plus
only byte-truthfully changed existing validation/delivery/visual-check artifacts. It cannot create a mapper, backend,
DI composition, lifecycle, execution, provider or ACL behavior. Tester writes the full-SHA-bound passing green record;
Independent Reviewer consumes only that committed passing record and writes an approved/needs-rework green review
record. Implementer commits each evidence file unchanged and alone. The normal Tester/review schemas, writer roles,
full-SHA binding, status invariants and sole-evidence commit rules remain mandatory.

Only after Planner verifies the approved green chain and actual current PR head can Independent Reviewer write a new
immutable C23 classification receipt at
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-<c23-green-subject-40-hex-sha>-<current-pr-head-40-hex-sha>.json`.
Only Implementer may unchanged-sole-commit it. It has exactly `schema_version`, `topic`,
`implementation_subject_commit`, `tester_evidence_commit`, `implementation_review_evidence_commit`,
`pr_head_commit`, `classifications`, `recorded_by`; these bind integer `1`, `loaded-runtime-cache`, the C23 green
subject, its passing Tester/review evidence commits, the actual current full head, exactly two classifications, and
`Independent Reviewer`. Each classification has exactly `thread`, `comment`, `outcome`, `reply`, for only
`ldeVI`/`4090495760` and `ldeVO`/`4090495770`; `outcome` is only
`REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK`. Only `REPLY_AND_RESOLVE` has a non-empty factual reply and can authorize the
corresponding exact reply/resolve. `ADDRESS` and `HUMAN_CHECK` use JSON `null` reply and remain Planner/open paths.

The four Human-only pairs F/ACL/business/README and `ld9Ai`/`4090688118` are excluded, ReadOnly and open; no C23
artifact, evidence or action may classify, reply to, resolve or otherwise alter them.

## C24 current-head classification technical contract

C24 is planning-only. It consumes C23 subject `240c694fa5078dc1d35f154f7a85b06381db2e47`, passing Tester
`dabce082058805281990c52b12352b87c2b46801`, approved Reviewer `489752c727aa86cfaf49038cc2ed6dfddf33ba2d`, C23 classification
provenance/current PR head `e5872d5dfb2018743b1f7e319551d52f25f5ef02`, and only classifies
`PRRT_kwDOUJTij86lfQl9`/`4091213935` and `PRRT_kwDOUJTij86lfQmF`/`4091213944`.

The candidate is exactly the five planning artifacts and pre-fills no future SHA, verdict, outcome, reply or resolution.
An Independent Plan-Reviewer writes an approved standard SHA-bound receipt; only Implementer commits it unchanged alone.
Then only Independent Reviewer may write
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-240c694fa5078dc1d35f154f7a85b06381db2e47-e5872d5dfb2018743b1f7e319551d52f25f5ef02.json`.
It has exactly `schema_version`, `topic`, `implementation_subject_commit`, `tester_evidence_commit`,
`implementation_review_evidence_commit`, `pr_head_commit`, `classifications`, `recorded_by`; binding integer `1`, topic,
the fixed C23 facts, exactly two entries and `Independent Reviewer`. Each entry has only `thread`, `comment`, `outcome`,
`reply`. `outcome` is only `REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK`; only the first has a non-empty factual reply and
permits exact Implementer reply/resolve. The other outcomes require `reply: null`; `ADDRESS` returns to Planner and
`HUMAN_CHECK` stays open. Implementer commits the receipt unchanged alone; all malformed/stale/non-sole records fail closed.

C23 resolved pairs are frozen. F/ACL/business/README Human-only pairs and `ld9Ai` remain ReadOnly/open exclusions;
C24 cannot modify source, tests, docs, architecture, PR state, those threads, or any unlisted path.

## C25 lfQl9 static Attribute-base NamedExpr remediation contract

C25 is the sole bounded remediation successor for C24 `ADDRESS` pair
`PRRT_kwDOUJTij86lfQl9`/`4091213935`. It changes exactly five planning artifacts as its candidate; after independent
approved review, both RED and green subjects change only
`tests/test_loaded_runtime_cache_bc_independence.py`. It does not prefill any future SHA, verdict, test result,
PR head, classification outcome, reply or resolution.

The RED regression must collect and fail for `(loader := importlib).import_module(...)`. The green repair is limited to
static recognition of a direct `ast.Attribute` whose `value` is an `ast.NamedExpr` with direct `ast.Name` target, whose
value resolves to a known `importlib` module alias, and whose `attr` is `import_module`. It must not recursively process
the NamedExpr target or expression, execute a fixture/AST, dynamically import, or introspect runtime modules. Direct-name
NamedExpr detection, mixed assignment's simple-name-only target handling, `getattr`, and `sys.modules` handling are
frozen and must remain unchanged.

The exact order is candidate-only commit → independent standard candidate-SHA-bound approved Plan-Reviewer receipt →
receipt-only commit → collection-success/assertion-failing RED test subject → full-SHA-bound factual failing Tester
evidence-only commit → distinct green test subject → full-SHA-bound factual passing Tester evidence-only commit →
approved independent green review evidence-only commit → Planner verification of actual current PR head → one-pair
independent classification receipt-only commit. Tester and Independent Reviewer schemas, writer separation, full SHA
binding, and unchanged sole-evidence commit rules remain exactly as already defined. Failing RED evidence cannot produce
Reviewer evidence or authorize green work outside this route.

After the approved green chain and actual current head are verified, only Independent Reviewer may write
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-<c25-green-subject-40-hex-sha>-<actual-current-pr-head-40-hex-sha>.json`.
Its top-level keys are exactly `schema_version`, `topic`, `implementation_subject_commit`, `tester_evidence_commit`,
`implementation_review_evidence_commit`, `pr_head_commit`, `classifications`, `recorded_by`; it binds schema `1`,
topic `loaded-runtime-cache`, actual C25 green-chain facts/current head, exactly one entry, and `Independent Reviewer`.
The one entry has only `thread`, `comment`, `outcome`, `reply` and is exactly `lfQl9`/`4091213935`. Outcome is only
`REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK`; only the first carries a non-empty factual reply. The others require JSON
`null`. Implementer alone may commit the receipt unchanged in a sole evidence-only commit. Any malformed/stale/non-sole
or cross-subject record fails closed.

Production source, docs, dataflow, all predecessor evidence, `lfQmF`/`4091213944`, F/ACL/business/README Human-only
locks, `ld9Ai`, every other thread and every unlisted path are ReadOnly. C25 does not itself reply, resolve, approve a
PR, merge, release or post-merge.

## C26 current-head seven-pair classification technical contract

C26 is planning-only. It binds C25 immutable green subject
`13f987a41119590621671c429293cf549055672b`, passing Tester evidence commit
`e85f936505a323e6c84c02e90f4c4114e39b6505`, approved Independent Reviewer evidence commit
`24d5141332cbc4dcf7a87dea7f134207a16ab37e`, and actual current-head base
`8bd9460950237c48c9befb73a1c5b80d084e88ae`. The candidate changes exactly the five planning artifacts and supplies
no future candidate SHA, Plan-Reviewer verdict, classification outcome, reply or resolution. An Independent
Plan-Reviewer writes the standard approved candidate-SHA-bound receipt; only Implementer commits it unchanged alone.

Then only Independent Reviewer may write
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-13f987a41119590621671c429293cf549055672b-8bd9460950237c48c9befb73a1c5b80d084e88ae.json`.
Only Implementer may commit that unchanged receipt in one sole evidence-only commit. Its JSON object top-level keys
are exactly `schema_version`, `topic`, `implementation_subject_commit`, `tester_evidence_commit`,
`implementation_review_evidence_commit`, `pr_head_commit`, `classifications`, `recorded_by`; values bind integer `1`,
`loaded-runtime-cache`, the listed C25 subject/evidence facts, the listed current-head base, exactly seven entries and
`Independent Reviewer`. Each entry has only `thread`, `comment`, `outcome`, `reply`, with this exact pair set and no
duplicates or extras: `ld9Ai`/`4090688118`, `lfYsF`/`4091265104`, `lfYsH`/`4091265108`, `lfYsK`/`4091265115`,
`m8u00`/`4129370918`, `m8u04`/`4129370926`, `m8u09`/`4129370931`.

`outcome` is exactly `REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK`. Only `REPLY_AND_RESOLVE` has a non-empty factual
`reply` and may later authorize the exact matching Implementer reply/resolve. `ADDRESS` and `HUMAN_CHECK` require
`reply: null` and route to Planner/open respectively. A malformed, missing, extra, stale, cross-subject, wrong-head,
wrong-writer, invalid-enum/nullability, or non-sole record fails closed and authorizes no action.

F/ACL/business/README Human-only locks `jnBpk`/`4043480108`, `kQ95O`/`4060023123`, `kqiZ5`/`4070096561`,
`lAR8T`/`4078761998`, and `lfQmF`/`4091213944` remain open exclusions. C25 `lfQl9`/`4091213935`, every unlisted
thread, and all source, tests, docs, architecture, dataflow, README, PR authority, merge, release and post-merge
actions are ReadOnly.

## C27 architecture-document conflict-resolution technical contract

C27 is a planning-only successor after committed C26 classification receipt `31ab754aae443f702fa4ccc028d53a6c687e48aa`. It is bounded to a manual
three-way textual integration of facts already committed at merge base `37d433e198a955f0710ecd5335666760aa86a20c`,
Loaded Runtime Cache fact `442cc9461854d3909345edb26d1434bfaaa1b86e`, Model Execution fact
`5f483a05e63c9dc8f3c63b04a63c8adec3ed2e28`, and dev head `1501f380f20492c71275474f800fdaaffbf0a76a`. No candidate,
receipt, integration subject, verification result, or verdict is prefilled.

The candidate changes exactly the five planning artifacts. After an independently written approved standard
candidate-SHA-bound Plan-Reviewer receipt is committed unchanged and alone, the sole integration implementation
subject may manually edit only these exact conflict paths:

1. `docs/architecture/business-capability/architecture-brief.md`
2. `docs/architecture/business-capability/index.html`
3. `docs/architecture/business-capability/scene.js`
4. `docs/business-capability-architecture.md`
5. `docs/evolution-roadmap.md`

The resolved files retain both committed facts without inventing their relationship: Loaded Runtime Cache remains a
protocol-only boundary with no Identity direct import, mapper, backend, or runtime lifecycle; Model Execution remains
provider-neutral coordination contracts; their wiring remains future work. Conflict markers, omitted committed facts,
new architecture choices, and every path outside the five-file allowlist fail closed.

Only after the five-file immutable integration subject is committed, Tester writes the normal full-SHA-bound factual
evidence at the authoritative exact path
`plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<c27-integration-subject-40-hex-sha>.json`; only an
Implementer commits that unchanged record in its own sole evidence-only commit. Independent Reviewer may consume only
that committed `passing` evidence for the same integration-subject full SHA and writes the normal same-subject review
evidence at the authoritative exact path
`plan/loaded-runtime-cache/loaded-runtime-cache.implementation-review-log-<c27-integration-subject-40-hex-sha>.json`;
only an Implementer commits that unchanged record in a later, separate sole evidence-only commit. Following approved
review, Planner Phase 4.5 is required before an Implementer may push the existing draft PR update. C27 does not
classify, reply to, or resolve a PR thread, and does not authorize PR approval, merge, release, or post-merge.

## C28 post-C27 eight-pair repair and classification technical contract

C28 is the sole successor for four C26 `ADDRESS` pairs — `lfYsH`/`4091265108`, `lfYsK`/`4091265115`,
`m8u04`/`4129370926`, `m8u09`/`4129370931` — and the four unclassified pairs `m82WL`/`4129419161`, `m82WS`/`4129419173`,
`m9eUV`/`4129677944`, `m9eUY`/`4129677947`. Its committed input provenance is C25 green
`13f987a41119590621671c429293cf549055672b`, C26 classification receipt
`31ab754aae443f702fa4ccc028d53a6c687e48aa`, C27 repaired candidate
`2dac62be230fe3daf6c259389c93a6e29cfa7006`, integration subject
`21747f2a24dedc2d18eaf2fbd6c8bc0bb0670585`, passing Tester evidence
`294f7fb5ea0502236c277e545ba9e2dc311596e3`, and approved Reviewer evidence
`190c41bb3480753f78bdf97c778583bee0f6ff2f`. These are factual inputs only; no C28 future SHA, verdict, result,
classification, reply or resolution is prefilled.

The C28 candidate changes exactly the five planning artifacts and aligns C25/C26/C27 tracker facts from their committed
records. An independently written standard candidate-SHA-bound approved Plan-Reviewer receipt is committed unchanged
and alone before implementation. The RED subject changes only
`tests/test_loaded_runtime_cache_bc_independence.py` and `tests/test_loaded_runtime_cache_contracts.py`; it must collect
and actually fail for the four static scanner gaps and for readable `RuntimeReuseKey` token state. Tester writes only
factual full-SHA-bound failing evidence; no Reviewer record is permitted for RED.

The distinct green subject may change only those two tests,
`src/deterministic_response_cache/loaded_runtime_cache/runtime_reuse/registry/runtime_reuse_key.py`, and the truthful
byte-changed subset of the existing ten dataflow artifacts under `docs/architecture/loaded-runtime-cache/`:
`loaded-runtime-cache.dataflow.json`, `.html`, `.validation.json`, `.delivery.json`, `.visual-check.json`,
`.visual-check.html`, and the 1440×900/2048×1320 dark/light capture PNGs. It must statically reject direct callable
`getattr(importlib, "import_module")`, direct module-cache base `getattr(sys, "modules")`, `import importlib.<child>`
through Python's top-level `importlib` binding, and an assignment RHS `IfExp` when either branch reaches a forbidden
callable. It must not execute fixture source, dynamically import, inspect runtime modules, recursively broaden AST
handling, or change the locked simple-name mixed-assignment behavior. `RuntimeReuseKey` preserves immutable
instance-identity semantics without inspecting, serializing, hashing or exposing its construction token through a
readable instance attribute. The dataflow explicitly presents `RuntimeRegistry.retain(key, runtime) -> None`, including
key/runtime inputs and completion, separately from `RuntimeRetention` outcome flows and without a backend/lifecycle/
mapper/wiring claim.

Tester writes passing evidence only for the green full SHA; Independent Reviewer consumes only its committed,
same-subject passing evidence and writes an approved or needs-rework same-subject review record. Implementer commits
each unchanged record in a separate sole evidence-only commit. After Planner verifies the actual current PR head, only
Independent Reviewer may write
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-<c28-green-subject-40-hex-sha>-<actual-current-pr-head-40-hex-sha>.json`.
It has exactly `schema_version`, `topic`, `implementation_subject_commit`, `tester_evidence_commit`,
`implementation_review_evidence_commit`, `pr_head_commit`, `classifications`, `recorded_by`; it binds schema `1`, this
topic, the new green/evidence/head facts, exactly eight entries, and `Independent Reviewer`. Every entry has exactly
`thread`, `comment`, `outcome`, `reply`; the pair set is exactly the eight pairs named above. Only
`REPLY_AND_RESOLVE` has a non-empty factual reply and can authorize later exact action; `ADDRESS` and `HUMAN_CHECK`
have JSON `null` replies and return to Planner/open state. Every malformed, extra, stale, cross-subject, wrong-head,
wrong-writer, invalid-enum/nullability, or non-sole record fails closed.

`jnBpk`/`4043480108`, `kQ95O`/`4060023123`, `kqiZ5`/`4070096561`, `lAR8T`/`4078761998`, and `lfQmF`/`4091213944` remain
Human-only/open exclusions. All unlisted paths, threads, predecessor artifacts, PR approval, merge, release and
post-merge are ReadOnly.

## C29 Three-File Architecture Conflict Integration Technical Contract (current route)

C29 planning candidate changes exactly requirements／technical-spec／topic plan／spec／step. Prior C28 actions are completed
live facts, not contents of preceding tracking commit `2d204b070cc9701cfdce31940cbfe377403f1894`; eight resolved replies are
`lfYsH`→`4140433910`, `lfYsK`→`4140435052`, `m8u04`→`4140436064`, `m8u09`→`4140436858`,
`m82WL`→`4140437667`, `m82WS`→`4140438539`, `m9eUV`→`4140439397`, `m9eUY`→`4140440128`.

Full dev parent is exactly `d6ff74ddf65c615f65eeba252e648784252a2bfd`; already-integrated base is
`1501f380f20492c71275474f800fdaaffbf0a76a`. Subject is a feature-worktree integration merge: actual preintegration feature
HEAD is recorded as first parent full SHA, fixed dev SHA as second parent. All other dev committed tree changes enter
automatically. Manual edits are limited exactly to `docs/architecture/business-capability/architecture-brief.md`,
`docs/architecture/business-capability/index.html`, `docs/architecture/business-capability/scene.js`. Compare manual delta
against automatic merge results; three-file restriction is not a restriction on automatic dev-parent tree changes.

Preserve committed Loaded Runtime Cache protocol-only and Model Execution provider-neutral coordination facts alongside
dev Response Reuse fixed-codec／bytes-envelope facts. Preserve BC independence, no concrete runtime backend／DI／mapper／
lifecycle or implemented BC wiring. Document and scene representations agree. No new architecture decision, dataflow
delivery, source/test change or extra manual edit; conflicting facts requiring a new decision return human-check.

Independent Plan-Reviewer writes only
`plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<c29-candidate-40-hex-sha>.json` with standard exact
`verdict`, `blocking_issues`, `copilot_feedback_triage` keys and triage `ADDRESS`, `DISCUSS`, `SKIP`. Implementer commits
approved receipt unchanged alone before creating integration subject. No future SHA／verdict／result is prefilled.

Tester alone writes `plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<c29-integration-subject-40-hex-sha>.json`
only after subject commit. Exact keys: `schema_version` integer `1`, `topic` string `loaded-runtime-cache`,
`implementation_subject_commit` full subject SHA, `status` enum `passing|failing`, `commands` nonempty array of objects
with exactly nonempty string `command` and integer `exit_code`, `recorded_by` string `Tester`. Passing requires every
exit code zero; failing requires at least one nonzero. Commands factually verify topology, manual scope, no markers,
committed facts, document/scene consistency and relevant regressions. Implementer unchanged-sole-commits evidence.

Independent Reviewer only after committed same-subject passing Tester evidence writes
`plan/loaded-runtime-cache/loaded-runtime-cache.implementation-review-log-<c29-integration-subject-40-hex-sha>.json`.
Exact keys: `schema_version` integer `1`, `topic` string `loaded-runtime-cache`, `implementation_subject_commit` same full
subject SHA, `tester_evidence_commit` full sole Tester commit SHA, `verdict` enum `approved|needs-rework`, `blocking_issues`
string array (approved empty, needs-rework nonempty), `recorded_by` string `Independent Reviewer`. Verify scope, facts,
actual parents and ordering. Implementer commits unchanged alone in a later separate evidence-only commit. Neither
record shares a commit with planning／implementation／other evidence; versioned full lowercase 40-hex paths are immutable.

Approved committed review → Planner Phase 4.5 factual plan/step alignment → bounded existing PR push → actual head／
mergeability／thread audit. Failure in writer/path/schema/SHA/topology/scope/facts/order fails closed; needs-rework creates
new subject and repeats Tester／Reviewer. C29 grants no thread classification／reply／resolve or Human PR merge／approval.
Original mission／protocol／outcomes／visualization／follow-ups unchanged; no README／VERSION／release／post-merge action.

Human-only/open `jnBpk`/`4043480108`, `kQ95O`/`4060023123`, `kqiZ5`/`4070096561`, `lAR8T`/`4078761998`,
`lfQmF`/`4091213944`; unclassified/open `m-94E`/`4130289778`, `m-94K`/`4130289786`, `nXkrM`/`4140364926`,
`nXrAw`/`4140406331`, `nXrA0`/`4140406337`. No disposition supplied; all predecessor evidence stays ReadOnly.

## C30 Current-Head Seven-Pair Classification Technical Contract (current route)

C29 factual publish／audit 已完成，audited PR head 為 `ee2825c785aad152e5785a021acdb68e3056e84d`。
C30 classification-only successor 固定消費 integration subject
`9c6ec737e9a900e2bcd1a02f2a6808bcb91e73aa`、passing Tester sole commit
`31e727d96d4e0843714dca1c7898ac93da9c33ef`、approved independent review sole commit
`fc12dea6be989aaecfdfc71a86fa1b330256fffe`。沒有新 implementation subject／RED／green。

Plan-Creator 只修改五個 standard planning artifacts。Implementer 建立 non-merge candidate-only commit；
獨立 Plan-Reviewer 只寫 `plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<c30-candidate-40-hex-sha>.json`，
exact three keys `verdict`、`blocking_issues`、`copilot_feedback_triage`，verdict `approved|needs-rework`，approved
blockers 空、needs-rework nonempty，triage 使用 `ADDRESS|DISCUSS|SKIP`。Implementer 將 approved receipt 原樣 sole
evidence-only commit。不得預填 candidate SHA、verdict、classification outcome、reply 或 resolution。

Planner 核對 committed C29 triple 與 PR audited head 後，Independent Reviewer 唯一可寫 immutable path：
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-9c6ec737e9a900e2bcd1a02f2a6808bcb91e73aa-ee2825c785aad152e5785a021acdb68e3056e84d.json`。
exact top-level keys：`schema_version`、`topic`、`implementation_subject_commit`、`tester_evidence_commit`、
`implementation_review_evidence_commit`、`pr_head_commit`、`classifications`、`recorded_by`。
Values 分別固定 integer `1`、`loaded-runtime-cache`、上述 S／T／V／head full SHA、exact seven entries、
`Independent Reviewer`。每個 entry exact keys `thread`、`comment`、`outcome`、`reply`；pair set 恰為
`m-94E`/`4130289778`、`m-94K`/`4130289786`、`nXkrM`/`4140364926`、`nXrAw`/`4140406331`、
`nXrA0`/`4140406337`、`nXzEu`/`4140459575`、`nXzE1`/`4140459585`。
Outcome enum `REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK`；僅 `REPLY_AND_RESOLVE` reply 為 nonempty factual string，
其餘必為 JSON null。Implementer 原樣 separate sole evidence-only commit receipt，Planner 才可 route exact reply／resolve；
ADDRESS 回 Planner 的 bounded repair route，HUMAN_CHECK 保持 open。Planning approval 本身不授權 thread actions。

Wrong／stale head、extra／missing pair、malformed keys／enum／nullability、wrong writer／SHA、非 sole commit、overwrite
或跨 topic evidence 均 fail closed。五個 Human-only/open exclusions：`jnBpk`/`4043480108`、`kQ95O`/`4060023123`、
`kqiZ5`/`4070096561`、`lAR8T`/`4078761998`、`lfQmF`/`4091213944`。未列 paths／threads 全部 ReadOnly。
C30 不作新 architecture／source／test／dataflow 修改，不授權 Human approval／merge／release／post-merge。

## C31 Five-ADDRESS Bounded Repair Technical Contract（current route）

C30 已提交 classification `005ec865f216de9f63f7dbfdd8df424d78a03afa`；兩個 REPLY_AND_RESOLVE live completed：
`m-94E` reply `4140750473`、`nXrAw` reply `4140753564`。C31 exact ADDRESS pairs 僅
`m-94K`/`4130289786`、`nXkrM`/`4140364926`、`nXrA0`/`4140406337`、`nXzEu`/`4140459575`、`nXzE1`/`4140459585`。

### Scope／locked static contracts

Plan-Creator only modifies the five standard planning artifacts. RED Implementer only changes
`tests/test_loaded_runtime_cache_bc_independence.py`; green Implementer only changes that file and
`docs/architecture/business-capability/scene.js`, `docs/architecture/business-capability/index.html`.
No runtime/library source, extra tests, architecture-brief, renderer, dataflow or uv.lock delta is authorized.
The existing direct imports, fixtures, mocks, assertions and prior scanner behaviors remain regression requirements.

1. Paired literal tuple/list assignment destructuring binds each matching RHS element to its corresponding simple-name
   target (including nested paired tuple/list shapes). Never flatten all RHS values onto all targets. Attribute targets
   are ignored; retain a simple target beside an attribute. Existing chained-assignment simple-name handling survives.
   Starred/unpacking inference and arbitrary iterable evaluation are outside this bounded static repair.
2. Static `getattr` on known builtins module aliases with literal `__import__` resolves the forbidden callable, whether
   assigned then called or called directly; existing importlib/sys getattr handling survives. No source is executed.
3. For positional and keyword-only function defaults, align AST defaults with their actual parameter names and retain
   a statically resolvable forbidden callable binding. Detect invocation through that parameter, preserving existing
   assignment/conditional/walrus aliases. Do not add runtime scope evaluation or arbitrary interprocedural inference.
4. Reject a statically recognized forbidden import callable passed as a call positional argument or keyword value,
   covering executor.submit and map invocation shapes, direct expressions and retained aliases. Ordinary callables
   remain accepted; inspect expressions statically without executing executor/map or imported source.
5. Per committed `architecture-brief.md` point 6, the Response Reuse Miss edge terminates at a clearly labelled future
   integration boundary, not Loaded Runtime Cache. Preserve existing independent Runtime/Execution contracts and future
   wiring facts. Scene and index inline scene must match; only bounded node/edge/label/geometric adjustments necessary
   for that endpoint are allowed. No implemented cross-BC handoff, mapper or new architecture decision is claimed.

### Candidate／RED／green／same-subject evidence

Implementer commits exactly five planning files in one non-merge candidate-only commit. Independent Plan-Reviewer alone
writes `plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<c31-candidate-40-hex-sha>.json`, exact keys
`verdict`, `blocking_issues`, `copilot_feedback_triage`; verdict `approved|needs-rework`, `blocking_issues` is an array
of objects with exactly `issue`, `file`, `fix` keys, each a nonempty string. It is empty for `approved` and nonempty
for `needs-rework`; triage exact `ADDRESS`, `DISCUSS`, `SKIP` arrays. Implementer commits approved receipt unchanged alone.
No candidate/subject SHA, future result, verdict, PR head, reply or classification outcome is prefilled.

After committed approval and Planner routing, Implementer commits a distinct non-merge RED test subject in the one
allowed test file. Tester factually verifies new cases collect and fail for the declared missing behaviors (not syntax,
dependency or unrelated failures), writing only
`plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<c31-red-subject-40-hex-sha>.json`.
Implementer unchanged-sole-commits failing evidence before green; no independent approval is made for RED.
Implementer then commits a distinct bounded green subject in the three allowed files. Tester alone writes
`plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<c31-green-subject-40-hex-sha>.json`.
Both Tester JSON records have exact keys `schema_version`, `topic`, `implementation_subject_commit`, `status`,
`commands`, `recorded_by`: integer `1`, string `loaded-runtime-cache`, actual corresponding full SHA,
`passing|failing`, nonempty array of exact `command` nonempty string／`exit_code` integer objects, `Tester`.
Passing requires every command exit 0; failing requires a nonzero exit. No claimed results substitute for actual runs.
Green checks cover the scoped pytest file and existing runtime contract regressions, JS syntax, scene/inline consistency
and Miss endpoint, three-path diff bounds, and preservation of prior contracts. Verification may read existing tools
and tests but cannot modify them. Implementer unchanged-sole-commits green Tester evidence.

Only then Independent Reviewer consumes committed passing same-green-subject Tester evidence and writes
`plan/loaded-runtime-cache/loaded-runtime-cache.implementation-review-log-<c31-green-subject-40-hex-sha>.json`.
Exact keys: `schema_version` integer `1`, `topic` string `loaded-runtime-cache`, `implementation_subject_commit`
same full green SHA, `tester_evidence_commit` actual full sole passing Tester commit SHA, `verdict`
`approved|needs-rework`, `blocking_issues` string array (approved empty; needs-rework nonempty), `recorded_by`
`Independent Reviewer`. Implementer unchanged-sole-commits it separately. Needs-rework requires new green subject and
new full Tester/review sequence. Every evidence path is immutable, full lowercase 40-hex SHA-bound; no evidence shares
a commit with planning, implementation or another evidence. Approved committed review permits Planner Phase 4.5 factual
plan/step alignment, separate tracking commit, bounded push and live actual PR head/mergeability/thread audit.

### Current-head classification／actions

After approved committed green evidence and live-head audit, Independent Reviewer alone writes
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-<c31-green-subject-40-hex-sha>-<actual-current-pr-head-40-hex-sha>.json`.
Exact top-level keys: `schema_version`, `topic`, `implementation_subject_commit`, `tester_evidence_commit`,
`implementation_review_evidence_commit`, `pr_head_commit`, `classifications`, `recorded_by`; bind integer `1`, this
topic, actual green subject／sole passing Tester commit／sole approved review commit／audited current PR head full SHAs,
exactly five entries, `Independent Reviewer`. Each entry exactly `thread`, `comment`, `outcome`, `reply` with the five
pairs above (string IDs), outcome `REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK`. Only REPLY_AND_RESOLVE has nonempty factual
string reply; otherwise reply null. Implementer unchanged-sole-commits classification separately; Planner then routes
individual committed REPLY_AND_RESOLVE entries for Implementer exact reply/resolve. ADDRESS requires new bounded route;
HUMAN_CHECK remains open. No pending approval or implementation result authorizes thread actions.

Wrong/stale head, wrong writer/path/key/enum/nullability/SHA/pair, overwritten or non-sole evidence, widening scope or
skipping actor order fails closed. Predecessor evidence/dev worktree/all other paths remain ReadOnly; Deleted none.
`nYQqw`/`4140648790` unclassified/open and five Human-only pairs `jnBpk`/`4043480108`, `kQ95O`/`4060023123`,
`kqiZ5`/`4070096561`, `lAR8T`/`4078761998`, `lfQmF`/`4091213944` are excluded/open. No PR approval, Human merge,
release, post-merge, README/VERSION changes. Original mission/protocol/outcomes/visualization/follow-ups persist.

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
及 assignment-retained callable bypass。Current：`c33-plan-authoring`。
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

No release／post-merge actions。本輪唯一 pending implementation 是 qualified known-builtins getattr；
starred `nZI5n` 與上述 Human-only five 留在 human-check/open，unlisted threads 不可回覆／resolve。

## C34 Current-Head Three-Pair Classification Successor（authoritative current routing）

### Goal / Outcome / Scope

Current：`c34-planning-draft`。Goal／In-Scope：僅獨立分類三個新 pairs
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
