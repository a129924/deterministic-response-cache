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
