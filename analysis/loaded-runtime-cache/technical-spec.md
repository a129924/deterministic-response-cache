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

Current：`c37-planning-draft`。本輪同 static BC independence scanner mission，
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
兩pair待IndependentReviewer分類；所有remaininglocked／grammaritems保持open。
No release／post-mergeactions。

```json
{"verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]}}
```

## C45 Current-Head Seven-Pair Classification（completed predecessor routing）

C45 draft-time／pending／Current 字樣保留為 predecessor snapshot；已提交 final alignment
`36431ed89757d17a1965fda018b2fb028625b905` 與下方 C46 為 actual current routing，非 C45 未完成證據。

### Goal / Outcome / Scope / Locked Decisions

Current：`c45-planning-draft`。Human 明確授權且 Planner 已選定此 classification-only successor；
僅對以下七個 exact suffix thread/comment pairs 作獨立 current-head classification，
不預填 outcomes／replies／resolutions，不授權任何 grammar／code／architecture 修改。

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
C45 唯一 current route；未分類七筆現由此 bounded successor 授權獨立分類，不自定 outcome。

已存在 requirements／technical-spec，採 strict analysis priority；
本五檔同步同一 C45 contract，technical-spec 為 execution-facing authority，
requirements 保留 original mission／business intent guardrail，非新 topic。
本輪唯讀核 PR head 為上述 fixed head、MERGEABLE／CLEAN；七筆 suffix/comment 對應且仍 open；
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
本七筆待 Independent Reviewer；八 Human-only／兩 grammar ADDRESS 保持 open。
No release／post-merge actions。

```json
{"verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]}}
```

Workflow state：current_step=c45-plan-authoring；next_step=bounded-candidate-commit；
status=COMPLETE（draft handoff only，非 approved／classification／topic-complete）。

## C46 Current-Head Five-Pair Classification（completed predecessor routing）

C46 pending／draft-time／Current 字樣保留 predecessor provenance；actual final alignment
`c0175a8627550a9bc01cdd05c859df70cb819856` 已提交／推送，下方 C47 唯一 current route。

### Goal / Outcome / Scope / Locked Decisions

Current：`planned`。Human 明確授權、Planner 選定 C46 classification-only successor，
只建立以下 exact-five 的獨立 current-head classification contract；不預填 verdict／outcome／reply／resolve，
不授權 code／grammar／architecture 修改。

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
五筆目前 open、source unchanged、S/T/V ancestors 與 fresh receipt path 已由 Planner preflight 核實；
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
Unresolved：五筆待獨立分類；原 9 HUMAN_CHECK／5 ADDRESS open；
其他未列新 pairs inventory-only。本輪無 release／post-merge actions。

Reviewer Handoff：
```json
{"verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]}}
```
Workflow state：current_step=c46-plan-authoring；next_step=bounded-candidate-commit；
status=COMPLETE（draft handoff only，非 approval／classification／publish／topic-complete）。

## C47 Bounded Six-Pair Scanner Repair（completed predecessor routing）

C47 draft-time／pending／Current字樣保留當時provenance；finalexact-twoalignment
`ad175fb5d4e3167a30c3d4aad922a8357a401430` 已提交／推送，下方C48唯一currentroute。

### Goal / Outcome / Scope / Locked Decisions

Current：`planned`。Human 授權此同-topic bounded repair successor；只修下列六 ADDRESS，
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
無release／postmergeaction。Unresolved：六fix尚未RED／green／T／V，七pairs待獨立分類；
十二Human仍open。Scope drift／contract conflict conservative交Planner／Human，不擴設計。

```json
{"verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]}}
```
Workflow state：current_step=c47-plan-authoring；next_step=bounded-candidate-commit；
status=COMPLETE（draft handoff only，非approval／implementation／gate／publish／topic-complete）。

## C48 Current-Head Twelve-Pair Human-Disposition Classification（completed predecessor routing）

C48 draft-time Current／pending 字樣為 frozen nonrouting provenance；final alignment 已於
`dcc8e5b717300c8c9b07bb698dbd1a3da2977cbc` commit／push，C49 是唯一 current route。

### Goal / Outcome / Scope / Locked Decisions

Current：`planned`。Human 明確指示「如果有 human lock 部分直接留言＋resolve」，
Planner 已判定足以啟動本同-topic classification-only successor，不要求重複泛稱 Human 確認。
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
Unresolved：十二待獨立分類與exactpermittedactions；o7gvv仍ADDRESS，parameterFIX未授權。
No release／post-mergeactions，所有futurecandidateSHA／verdict／outcomes／reply／resolution不得預填。

```json
{"verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]}}
```
Workflow state：current_step=c48-plan-authoring；next_step=bounded-candidate-commit；
status=COMPLETE（draft handoff only，非approval／classification／actions／topic-complete）。

## C49 Current-Head Four-Pair Classification（completed predecessor routing）

C49 final factual alignment commit／normal push `5afaf53d264466deca22b4858c09177ca112d922` 已完成；
C50 是唯一 current route，C49 draft-time／pending 字樣為 frozen nonrouting provenance。

### Goal / Scope / Locked Decisions

Current：`planned`；step phase：`plan-authoring`；existing PR #7 保持 pr-open。
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
Open Questions：四筆 independent outcomes 尚未產生；o7gvv parameter 修復未授權。
此輪無 code 設計待補；若分類要求 scope 外修復，ADDRESS／HUMAN_CHECK 留 open，Human 一次決定。
Post-merge／release actions：none；Human alone PR review／merge／release／post-merge／tag。

Reviewer handoff schema（不是預填 receipt）：
```json
{"verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]}}
```
Workflow state：current_step=c49-plan-authoring；next_step=bounded-candidate-commit；
status=COMPLETE（draft handoff only，非approval／classification／actions／topic-complete）。

## C50 Bounded Four-ADDRESS Repair（completed predecessor routing）

C50finalalignment `9a8b46fa72a9800622349b049cc03d06b57e5f9f` 已normalcommit／push；
C51是唯一currentclassificationroute，C50pending／Current字樣onlyhistoricalsnapshot。

### Goal / Outcome / Scope

Current：`planned`；phase：`plan-authoring`。C50 是本 topic 唯一 current repair route；
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
Workflow state：current_step=c50-plan-authoring；next_step=bounded-candidate-commit；
status=COMPLETE（draft handoff only，非approval／implementation／evidencegate／topiccomplete）。

## C51 Current-Head Three-Pair Classification（completed predecessor routing）

C51finalalignment `165087337ac5dea9fdbd307021c322ca7226c2e9` 已normalcommit／push，
C52是唯一currentrepairroute；C51pending／Current字樣onlyfrozenprovenance。

### Goal / Outcome / Scope / Locked Decisions

Current：`planned`；phase：`plan-authoring`；existing PR #7 保持 pr-open。
C51 是唯一 current classification-only route；C50 及較早 Current／pending 字樣是 frozen nonrouting provenance。
Goal／In-Scope：以固定已發布 head 與同 subject passing Tester／approved Independent Reviewer evidence，
獨立分類下列三筆 actual original comments，再只處置 committed REPLY_AND_RESOLVE 的 exact pairs。
本輪不授權修復，不預判 addressed／非必要；需要新增 semantics／code scope 時一次交 Human 決定。
原 mission／scope／outcomes／Registry protocol／API／Architecture Visualization／follow-up missions 不變。
Analysis strict mode：technical-spec 為 execution-facing truth，requirements 為 intent guardrail；
本 C51 共同契約逐字同步 standard-five，後續 ONLYplan／step factual alignment 不重開 candidate chain。

Out-Of-Scope／Non-Goal：code／grammar／match-pattern／container resolver／pyi scanner 修復或新增 RED／green／T／V；
architecture／README／public API／dependencies／typing contract／shared governance contract 變更；
解除十二 locks、merge／release／post-merge／tag／重寫歷史／新 PR。
ReadOnly：src／tests／uv.lock／pyproject／architecture／Archify／README／VERSION／contracts／原 S/T/V／old receipts；
不得執行 source／fixture、不以 importlib／__import__／sys.modules substitution 取代 direct imports。
Written／Modify：candidate只有如下五份 planning artifacts，由 Plan-Creator 唯一 author；
後續 final alignment 只有 plan／step。Deleted：none。
- `analysis/loaded-runtime-cache/requirements.md`
- `analysis/loaded-runtime-cache/technical-spec.md`
- `plan/loaded-runtime-cache/loaded-runtime-cache.plan.md`
- `plan/loaded-runtime-cache/loaded-runtime-cache.spec.md`
- `plan/loaded-runtime-cache/loaded-runtime-cache.step.md`

dev worktree／其他paths不動；非唯一agent，不revert他人成果。
三 rejected untracked immutable receipts保留、不stage／改寫／刪除／當routingauthority；
fresh receipts不可覆寫任何已存在path，即使uncommitted或rejected。
原十二 semantic／grammar／architecture／README locks全部保持；C48不修改處置非解除requirements。
C50 canonical六completed implementationsteps保留歷史completion，不新增fake codepending，不借其subject建立新code結果。
Stable-library intent absent；README／VERSION／release metadata不改。
Python metadata保留；Async-planning status: exempt — cite exemption evidence: classification／tracking-only，
不引入asynccode／I/O／lifecycle／concurrency／timeout；無newpublic API、interface、breakingchange、
dependency、error-policy或typing策略變更。既有七decisions／directimports／fixtures／mock／assertions不變。

### Actual Fixed Facts / Exact Three Inputs

C50 final factual alignment commit／normal push：
`9a8b46fa72a9800622349b049cc03d06b57e5f9f`。
固定 actual reviewed PR head 即該full40SHA；authoring時local／origin／PR一致、
OPEN／MERGEABLE／CLEAN，tracked/indexclean、三 rejected preserved。
Fixed same S：`4aff14e3009f46ba82ee5fe78a11ca05a635db37`；
passing T sole：`6da6292e8a7a2aac726fcca90bfc559cc8ae9928`；
approved V sole：`7281f494597e3253de0170b0257a3302c2fcde8c`。
Planner已核實上述同-S evidence、ancestry／source unchanged；
此為無code變更C51 classification可消費sameS authority，不授權新implementation或跨subjectreuse。
C50四authorizedfindings修復／replyresolve完成，existingimmutable evidence與actions不重做。
以下輸入已唯讀核 actual original body／IDs／path；三筆目前open，outcome尚未判定：

| Thread suffix | Comment string | Actual original input（非修復授權／預定outcome） |
| --- | --- | --- |
| `pu_ja` | `4202486092` | P2：match mapping capture如 case {"factory": ModelIdentity}: ModelIdentity()（Identity對称RuntimeReuseKey）可建立foreign semantic binding；建議遍歷ast.Match* capture names與兩BC regression。原target commit 5afaf53d264466deca22b4858c09177ca112d922，path tests/test_loaded_runtime_cache_bc_independence.py。 |
| `pu_jo` | `4202486109` | P2：(__import__,)[0]("identity")、[importlib.import_module][0]("identity")或constant-keydictlookup漏forbiddencallable；建議靜態tuple/listindex／dictkeyelement後遞迴existingresolver並排除dynamicindex/key。原target commit 5afaf53d264466deca22b4858c09177ca112d922，path同test；不得偷換成C50已修namespace.get。 |
| `pu_j0` | `4202486122` | P2：三current-source checks _direct_imports_from／_uses_dynamic_import_substitution／_declares_forbidden_semantic_type目前rglob("*.py")可能忽略.pyi跨BCimport／declaration；建議同掃.py/.pyi與兩BC regression。原target commit 5afaf53d264466deca22b4858c09177ca112d922，path同test；本輪不改scanningsuffix。 |

Reviewer independently查current committedfacts，不把原留言或historicaltarget當通過evidence，
不以「topic已久」預設R&R；新unlistedpairs inventory-only，不分類／留言／resolve。
C50修復能力不覆蓋新增semantics時只能ADDRESS／HUMAN_CHECK、reply null/open；實際判定由獨立Reviewer。

### Artifact Paths / SHA-Bound Immutable Schemas / Sole Writers

Independent Plan-Reviewer唯一writer：
`plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<actual-C51-candidate-full40SHA>.json`。
actualexact-fivecandidateLOCALcommit後才展開freshpath，不預fillcandidate SHA/verdict。
exact 3 keys verdict／blocking_issues／copilot_feedback_triage；
verdict approved|needs-rework；blocking_issues object array，entry恰non-emptystringissue／file／fix，
approved []、needs-rework至少一項；triage恰ADDRESS／DISCUSS／SKIP arrays。
Plan-Reviewer只審committedcandidate、寫receipt不commit；approved才Implementer unchangedsoleLOCALreceiptcommit。
candidate／approvedreceipt分類前均LOCAL，不push改fixed remotehead。

Independent Reviewer唯一classificationwriter：
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-4aff14e3009f46ba82ee5fe78a11ca05a635db37-9a8b46fa72a9800622349b049cc03d06b57e5f9f.json`。
fresh immutablepath；exact8top-levelkeys：schema_version／topic／implementation_subject_commit／
tester_evidence_commit／implementation_review_evidence_commit／pr_head_commit／classifications／recorded_by。
schema_version integer1；topic loaded-runtime-cache；
fourSHAs必各精確fixedS／passingT／approvedV／reviewedPRheadfull40lowercasehex；
recorded_by Independent Reviewer。
classifications恰三entries，exact-three上述pairs各一次；每entry恰thread／comment／outcome／reply。
thread suffixstring（不要fullPRRTID），commentstring；
outcome REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK，非預填。
REPLY_AND_RESOLVE必non-emptyoriginalfactualreply，有currentcommittedfacts支持；
ADDRESS／HUMAN_CHECK必null、open。沒有codefixauthority不得以回覆補成已修。
Reviewer只寫freshreceipt，不commit／留言；Implementer原樣soleclassificationevidence-onlycommit／normalpush，
不混planning／code／other evidence。正常hooks，C28noverify等subject-local歷史授權不可沿用。
所有candidate／receipt commits non-merge、sole named diff與schema／writer由actualGitfacts驗；
wrongSHA／topic／writer／schema／extraentry／overwrite／nonsolecommit failclosed，回Planner不自改contract。

### Ordered Route / TestCase / Validation / Stop Conditions

1. Plan-Creatorexact-five draft → Plannerpreflight → Implementerexact-fiveLOCALcandidate-onlycommit。
2. IndependentPlan-ReviewerfreshSHAreceipt → approved才ImplementerunchangedsoleLOCALreceiptcommit。
3. Planner核fixedPRhead、same-ScommittedpassingT／approvedV、ancestry／sourceunchanged、freshpath，
   head drift不改選新head，不推定gate。
4. IndependentReviewerexact-threeimmutableclassification → Implementerunchangedsoleclasscommit／normalpush。
5. Planner核committedclassification及descendantssourceunchanged後只routeexactR&Rpairs；
   Implementer原文reply／resolve前重新核現況防duplicate，記actualreplyID／resolvedfact。
   ADDRESS／HUMAN_CHECKopen，不擴scope；Human-requiredchoices一次彙整。
6. Plan-CreatorONLYplan／stepfinalactualfacts／已完成workflow才[X] →
   Implementerseparatenormalcommit／push → 一次full-paginationaudit → human-check；PR7pr-open。
   finalalignment完成由actualGitfacts證，不預fill自己commit／push／SHA或新增selfcheckbox／candidate-loop。
   newunlistedinventory-only，不無限追bot新留言。

TestCase／Acceptance Criteria：
- Happy path：approvedcandidate＋same-STV＋fixedhead＋exact-threeindependentreceipt，只有actualR&Ractions。
- Invalid input：wrongkeys／types／shortSHA／uncommittedevidence／wrongpair／solepath／writer failclosed。
- Edge case：historicaltarget／stub／literalcontainer／matchcapture建議不等於既有修復，classification不得偷換語意。
- Regression：C50 sameS/T/V／六completedcanonicalsteps／sourceblobs／十二locks／oldreceipts不變。
- Backward compatibility：API／protocol／outcomes／directimports／Archify／Pythonmetadata不變，沒有新codebehavior。
Given actualthreecomments及approvedplanningreceipt，Whenindependentreviewer核fixedfacts，
Thenexact3classifications由evidence決定，非按想收束預定。
GivenADDRESS／HUMAN_CHECK，Thenreplynull／threadopen；GivenfactualR&R且committedreceipt，Then才能originalreplyresolve。
Givenhead/source/evidencedrift，Then停相應gate交Planner，不自改head／schema／scope。
上述兼specBehavioralScenarios／ErrorEdgeCases，C51不添加REDtests或解決尚未授權codefinding。

Planningvalidation：
`git diff --check`；
`python .agents/skills/plan-step-tracker/scripts/step_tracker.py check_impl_steps_succeeded loaded-runtime-cache`
應exit0＝C50既有六completed，非C51codegate。
Actualread-onlychecks：
`git rev-parse HEAD`、`git status --short`；
`git merge-base --is-ancestor 4aff14e3009f46ba82ee5fe78a11ca05a635db37 9a8b46fa72a9800622349b049cc03d06b57e5f9f`，
同核fixedT／V ancestry；
`git diff 4aff14e3009f46ba82ee5fe78a11ca05a635db37 9a8b46fa72a9800622349b049cc03d06b57e5f9f -- src tests`，
`git show --format=fuller --stat <actual-evidence-commit>`、actualnamedsolepath與JSONschemachecks。
分類前read-onlyPRhead／fullpaginationthreads核actualfixedstate，不將分支或chat當routingauthority。
缺required evidence／source或headdrift／scope或contractconflict回Planner，禁止偷修contract或擴code。

### Risks / Rollback / Open Questions / Reviewer Handoff

Risks：把match／container／pyi新semantics當既有fix、預設outcome、oldhead／跨subjectevidence、
replyduplicate／solecommit污染、自指state loop。
Rollback：onlyboundedstandard-fiveplanningrework或必要freshimmutableplanning successor，
保留submittedcandidate／receipt／sameSTV；不broadreset、overwriteevidence、codefix或清三rejected。
OpenQuestions：design none；threeindependentoutcomes尚未產生，若需修復則Human一次明確scope選擇。
Post-merge／releaseactions：none；HumanalonePRreview／merge／release／postmerge／tag；
boundedclassification／threadresolution不等於Humanapproval／workflowclose。
```json
{"verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]}}
```
此為IndependentPlanReviewerhandoffschema，不是Creatorreceipt／approval。
Workflowstate：current_step=c51-plan-authoring；next_step=bounded-candidate-commit；
status=COMPLETE（draftonly，非approval／classification／actions／topic-complete）。

## C52 Bounded Three-ADDRESS Repair（completed predecessor routing）

C52finalalignment `5bf16409d19df472eb17f9fb2150c95b47df1478` 已normalcommit/push，
C53唯一currentclassificationroute，C52pending／Current字樣only歷史snapshot。

### Goal / Outcome / Scope

Current：`planned`；phase：`plan-authoring`；existing PR #7 pr-open。
C52是唯一current repair route，Human明確授權下列三必要finding的bounded修復；
C51及更早Current／pending字樣是frozen nonrouting provenance，不建立C52 execution approval。
原Loaded Runtime Cache mission／scope／outcomes／Registry protocol／API／Architecture Visualization／follow-up missions不變。
Analysis strict mode：technical-spec為execution-facingtruth、requirements為intentguardrail；
本C52契約逐字同步standard-five，後續ONLYplanstep factualalignment不重開candidatechain。

| Exact pair | Goal／In-Scope：唯一test-module repair |
| --- | --- |
| `pu_ja/4202486092` | match patterns 的 genuine binding slots：MatchAs.name、MatchStar.name、MatchMapping.rest及nestedpatterns，兩BCforeign semantic-name ownership；不是patternclass／keyword／value refs。 |
| `pu_jo/4202486109` | directtuple/list可確定integerindex、directdict可確定literalkey，取selectedelement後遞迴existingforbiddenaliasresolver／既有USE；未選取或unusedcallable不新增拒絕。 |
| `pu_j0/4202486122` | 原三current-source scanners同時discover .py／.pyi，對兩suffix沿用全部existingrules；不新增productionstub或stubgrammar。 |

In-Scope：only `tests/test_loaded_runtime_cache_bc_independence.py` 的三repair＋isolated RED/control fixtures，
newimmutableRED／green S／same-S independentT/V、exact-threefixedpublishedheadclassification／permittedactions。
Out-Of-Scope／Non-Goal：其他scannergrammar、任意eval／dynamicindex/key／slice／unpack／containeralias／
orderedbinding／CFG／comprehensionaliasinference／新semanticrules；
productioncode／stub／API／README／VERSION／dependencies／uv.lock／architecture／Archify／sharedcontract；
解除十二locks、merge／release／postmerge／tag／重寫歷史／新PR。
ReadOnly：allother source/tests/config/contracts/oldreceipts/architecture/Archify，舊fixtures／mocks／assertions／directimports保持。
Written／Modify：candidate exact-fiveplanning由Plan-Creator唯一author、implementationonlysingledeclaredtest，
freshindependentevidence如後表；Deleted：none。
devworktree不動，非唯一agent不revertothers；三rejecteduntrackedimmutable不stage／改寫／刪除／當routingauthority。

### Locked Decisions / Boundaries

1. Match：只檢查真正capture binding slot，MatchAs／MatchStar 的name、MatchMapping的rest，
   遞迴nestedpatterns至同類slots，LoadedRuntimeCache禁localModelIdentity、Identity禁localRuntimeReuseKey。
   Pattern MatchClass.cls／kwd_attrs、MatchValue／mappingkey／ordinaryreference不是capturebinding；
   不因出現相同reference額外判ownership違規、不執行matchsubject／guard／pattern或source。
2. Literalcontainer：只在directtuple/list/dict字面container、可確定selector／selectedposition／key時，
   將selected AST element遞迴existingresolver，仍依後續forbiddenUSE；
   unselectedforbiddencallable／unusedpossession合法，不新增全container fail-closed／possessionban。
   不解析arbitrarycallresult／mapping／containeralias／dynamicselector／slice／unpacking；
   dictduplicatekeys、無法確定的key／collision／position不推論，不選last-wins、不以保守拒絕假裝確定。
   不為此創造另一keygrammar或重解identity。缺失／out-of-range不推定selectedforbiddencallable。
3. .pyi：只對 _direct_imports_from、_uses_dynamic_import_substitution、
   _declares_forbidden_semantic_type 擴filediscovery的suffix集合為 .py＋.pyi；
   同existingparse／imports／dynamicimport／semanticownership規則，不新增stubsyntaxexemption／grammar／productionstubs，
   不執行fixturesource、不以dynamicimport或sys.modules替代directimports。
4. 原十二semantic／grammar／architecture／READMElocks維持；exact-two getattrs／comprehensionalias／
   nestedForalias／ordered-scope等不擴張。C48 Human不修改處置非解除requirements。
5. 下列七筆仍inventory-only／open，不分類／修復／留言／resolve：
   `pvzDA/4202824859`、`pvzDF/4202824865`、`pvzDH/4202824868`、
   `pv59N/4202868919`、`pv59R/4202868923`、`pv59T/4202868925`、`pv59V/4202868928`。
   後續newunlisted同樣onlyinventory，不借C52授權擴scope。
6. 不改localRuntimeReuseKey／RuntimeRegistry／RuntimeRetention／outcomes／taxonomy／publicsurface；
   productionprotocol-only／Identityauthority／BCindependence／Archify交付不變。
   超過explicitpath／scope或需要新lockeddecision即交Planner／Human，不猜需求。

### Actual Base / Status / Allowed Transitions

Authoringbase actualHEAD：`165087337ac5dea9fdbd307021c322ca7226c2e9`，
C51 completedclassification／finalalignment frozenhistory。
C51 candidate `3f317223c880349e9071cfdc7d21daef044bd8a6`、
approvedreceiptsole `a1e8e95baa045ed2814d418fb3c3e92012f6ab86`、
classificationsolepush `9dc60be5877a4af00277f3238cff2b7e9ac9a04c`；
三ADDRESS已分類、尚未修復，不能把分類completed當三requirementsdone。
Plannerfreshsnapshot：134threads／124resolved／10open（本三ADDRESS＋七inventory-only），
不猜auditUTC或預填C52candidate／futureSHA／結果。
舊S `4aff14e3009f46ba82ee5fe78a11ca05a635db37`、
T `6da6292e8a7a2aac726fcca90bfc559cc8ae9928`、
V `7281f494597e3253de0170b0257a3302c2fcde8c` 只作C50predecessor，
C52新subject必獨立建立新same-S T/V，禁止借舊evidence背書。

planned → committedcandidate／independentapprovedreceiptsoleLOCAL → creator-in-progress test-onlyRED →
independentTesteractualfailingRED／soleT → distinctgreencreator-in-progress →
tester-in-progressnewS passingT／sole → review-readyfactualalignment／canonicalCLI0 →
independentreviewer-in-progress → approved|needs-rework。
needs-rework交boundedImplementer新immutableS，完整同-ST/V重走；不得覆寫evidence／借舊subject。
approved → PlannerPhase4.5factualalignment → publish-in-progress → existingPR7pr-open →
actualfixedpublishedheadexact-threeclassification → individuallypermittedactions → finalfacts／human-check。
Planningapproval非executionapproval，Reviewer非HumanPRreviewer；
只有Human PRapproval／merge，無directpublish-in-progress→merged。

### Artifact Paths / Owners / Immutable Schemas / Sole Commits

Plan-Creator exact-fivecandidatepaths；review-ready／Phase4.5／finalalignmentONLYplan／step：
- `analysis/loaded-runtime-cache/requirements.md`
- `analysis/loaded-runtime-cache/technical-spec.md`
- `plan/loaded-runtime-cache/loaded-runtime-cache.plan.md`
- `plan/loaded-runtime-cache/loaded-runtime-cache.spec.md`
- `plan/loaded-runtime-cache/loaded-runtime-cache.step.md`

ImplementeronlyRED/greenModify `tests/test_loaded_runtime_cache_bc_independence.py`。
ReadOnlyvalidationinput `tests/test_loaded_runtime_cache_contracts.py`、`pyproject.toml`；
unlistedpaths—includingproduction .pyi—不可write。
Evidenceparameters只在actualcommittedfull40lowercasehexSHA存在後展開freshpath；
不能symbolicHEAD／short／futureSHA／pre-filledoutcome；existingpaths不overwrite，包括rejecteduncommitted。
各independentwriter只寫自己record不commit；Implementer原樣、各自soleevidence-onlynon-mergecommit，
不與implementation／planning／anotherreceipt同commit。Namedsolepath／schema／subject／writer以actualGitfacts核。

IndependentPlanReviewerwriter：
`plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<actual-C52-candidate-full40SHA>.json`。
exact3keys verdict／blocking_issues／copilot_feedback_triage；
verdictapproved|needs-rework，blocking_issuesobjectarray（entry恰non-emptyissue／file／fixstrings），
approved[]／needs-reworknonempty，triage恰ADDRESS／DISCUSS／SKIParrays。
Committedexact-fiveLOCALcandidate才review，不commit；approved才Implementer unchangedsoleLOCALreceipt。
candidate／approval先LOCAL、不推head。

IndependentTesterREDwriter：
`plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<actual-C52-RED-full40SHA>.json`；
greenwriter：
`plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<actual-C52-green-S-full40SHA>.json`。
exact6keys schema_version／topic／implementation_subject_commit／status／commands／recorded_by；
integer1／loaded-runtime-cache／actualRED或newgreenS／passing|failing／Tester。
commandsnon-emptyarray，entry恰commandnon-emptystring／exit_codeinteger；
passing只全部actual0，failing至少一actualnonzero。
REDcollection／controls必0，三originalfindingrejectingtests genuineassertionfail，
不是parse／collection／importerror；尤其pyi各scanner正向fixture必同規則可parse。
REDfactualfailure不是expected-failingpass，failingT不得交Reviewer寫reviewevidence。
Tester獨立實测immutableS、不commit；Implementer unchangedsolefailing／passingT各別commit。

IndependentReviewerwriter：
`plan/loaded-runtime-cache/loaded-runtime-cache.implementation-review-log-<actual-C52-green-S-full40SHA>.json`。
exact7keys schema_version／topic／implementation_subject_commit／tester_evidence_commit／
verdict／blocking_issues／recorded_by；integer1／loaded-runtime-cache／sameactualnewS／
same-ScommittedsolepassingT fullSHA／approved|needs-rework／stringarray；recorded_by 必為 `Independent Reviewer`。
approvedblockers[]，needs-rework至少一string；未committed／failing／cross-S／malformedT failclosed，
不得產V。Reviewer只independentreview/write，不commit；Implementer unchangedsoleV。

Independentclassificationwriter：
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-<actual-C52-green-S-full40SHA>-<actual-reviewed-published-PR-head-full40SHA>.json`。
newpassingT／approvedV／Phase4.5normalpublishactualcommit後由Planner核fixedhead才展開freshpath。
exact8keys schema_version／topic／implementation_subject_commit／tester_evidence_commit／
implementation_review_evidence_commit／pr_head_commit／classifications／recorded_by。
integer1／loaded-runtime-cache／actualnewS／same-SpassingT／same-SapprovedV／actualfixedreviewedpublishedhead／
recorded_by 必為 `Independent Reviewer`。classifications恰三entries各exactpair一次，entryexactthread／comment／outcome／reply；
suffixstring／commentstring；outcomeREPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK不預定。
R&R須non-emptyoriginalfactualreply支持actualfix；ADDRESS／HUMAN_CHECKreplynull且open。
Reviewer只寫、不留言commit；Implementer unchangedsoleclasscommit／normalpush。
後續sourceunchanged／headancestry／actualcommittedreceipt由Planner核exactactionsgate。
Wrongkeys／SHA／topic／writer／pair／solecommit／overwrite／drift failclosed，回Planner不改contract。

### Python implementation metadata（C52 current bounded profile）

#### Non-goals
- 不改productioncontracts／stub／API／Identityauthority／ArchitectureVisualization。
- 不新增dynamicindex/key／slice／unpack／containeralias／arbitraryeval／duplicate-keylastwins或failclosed策略。
- 不改十二locks／七inventory-only，不擴其他scannergrammar或orderedbinding／comprehensionalias。
- 不新增dependency／config／uv.lock／README／VERSION／release／merge，dev不write。

#### Current Context / Requirements
既有semantichelper未遍歷match genuinecaptures；forbiddenaliasresolver尚未選directliteralcontainerelement；
三scannerfilediscovery只.py會略.pyi。C52只補三已授權、可單獨RED重現的缺口。
各原finding都有isolatedrejectingfixture；pyi覆蓋兩BC三checks。舊ASTrules全部保留，
selectedelement與forbiddenUSE依existingresolver，privatehelperrepresentation由Implementerbounded選擇。
不能靠弱化assertions／跳tests／executingsource／dynamicimport達green。

#### Decisions
- Async-planning status: exempt — cite exemption evidence: 同步ast.parse／ast.walk／filesuffixdiscovery及fixtures，
  無asyncboundary／resourceownership／I/Oconcurrency／timeout／retry／cancellation／lifecycle變更，
  即使existingAST含asyncsyntax也只parse不execute。
- Module/package placement: only `tests/test_loaded_runtime_cache_bc_independence.py` scanner／isolatedfixtures。
- NewpublicAPI: no，no newmodule/packageexports／productionstub。
- Interfacechanges: no productioninterfacechanges，只三declaredscannerbehavior。
- Breakingchangesallowed: no，existingdirectimports／fixtures／mocks／assertions／negativeboundaries保持。
- Newdependencies: no，existingast／pytest／Ruff／strictPyright；uv.lock不改。
- Error-handlingstrategy: existingparse/assertionfailure與propagation保持，不swallowerrors／改outcomes；
  不確定containerselector不推論，不用failclosed拒絕未確定forbiddenUSE。
- Typingstrategy: Python3.12strictPyright、preciseASTtypes／typedhelper，noAny／dynamicimport／sys.modules substitution。

#### Public Contract / API Changes / Affected Files
No public/productioncontractchange；onlydeclaredsingleimplementationtestpath。
Candidateinspectpaths：同test、ReadOnlycontractstest／pyproject；allsourceincludingstubs ReadOnly。
Planning／freshSHAevidenceowners前表明定，Deletednone。

#### Test Plan / TestCase
- Happypath：兩BCmatchas／matchstar／mappingrest＋nestedcaptures；
  directtuple/list確定integerindex／directdictunique確定literalkey選forbiddencallable後USE；
  .pyi對兩BC三existingchecks沿existing規則reject。
- Invalidinput：dynamicindex/key／slice／unpack／unknowncontainer／missingkey／outofrange；
  duplicate-key／uncertaincollision／position不推論，不用語法error冒充RED。
- Edgecase：nestedpatterncapturevsclass／keyword／value refs；
  selectedordinaryelementvsunselectedforbiddencallable、unusedliteralcallablepossession；
  dictionarykey不確定無新lastwins/failclosed；py與pyi同existinggrammar/parserfailurepolicy。
- Regression：所有existingfixtures／mocks／assertions／directimports、十二locks／C50boundedgetattr／namespaceget／
  arguments／comprehensionsemantic／modulealternatives／sys.modulesbehavior不變；
  realpassing兩檔pytest／Ruff／strictPyright。
- Backwardcompatibility：productionprotocol／outcomes／API／taxonomy／ArchitectureVisualization／BCauthority不变，
  無newproductionstub，fixturesource不執行。
Givenoldscanner＋originalthreepositivefixtures，WhenREDparse，Thencollection／controls0且各findinggenuineassertionsfail。
Givennewboundedscanner，Whenselectedliteralknownforbiddencallable後USE／genuineforeigncapture／pyistub違existingrules，
Then正確reject；Givenunknown/uncertain/unselected/unused／patternreferences，Then本輪不新增誤拒。
Givennew-ScommittedpassingT／approvedV及actualpublishedhead，Then才能exact-threeindependentclassifications，
不能以完成code勾選直接resolve。
以上即specAcceptanceCriteria／BehavioralScenarios／ErrorEdgeCases，co-artifact非第二Pythonplan。

#### Risks / Rollback Plan
Risks：把patternreference當capture、整container拒絕、duplicatekeylastwins臆測／不確定碰撞推論、
.py／.pyi規則歧異、REDparsefailure、oldsubjectreuse／stalehead／duplicate replies／selftrackingloop。
Rollback：onlysingledeclaredtestbounded修回且newimmutableS重走T/V；planning只declaredfive經Plannerroute；
所有committedcandidate／RED／S/T/V／receipts保持，不broadreset／overwrite／改contracts／清三rejected；
normalhooks，不沿用C28noverify subject-local授權。

### Implementation Steps（source for canonical completion gate）

1. C52 在 `tests/test_loaded_runtime_cache_bc_independence.py` 新增三原finding的isolated RED/control fixtures（兩BCmatchcapture、selectedliteralcallable、兩BC三scanner .pyi），testnames含c52、rejecting另含rejects、controls不含rejects；只新增fixtures，不修scanner、不執行source，collection/controls0且三類genuineassertionfail。
2. C52 在 `tests/test_loaded_runtime_cache_bc_independence.py` 遍歷nestedmatchpatterns的MatchAs.name／MatchStar.name／MatchMapping.rest genuinebinding，依兩BCforeignsemanticownership；排除class／keyword／value refs，不求值pattern或subject/guard，不改旧assertions。
3. C52 在 `tests/test_loaded_runtime_cache_bc_independence.py` 對directtuple/list確定integerindex／directdict確定literalkey取selectedelement後遞迴existingforbiddenaliasresolver與USE；未選／unusednegative保持，不推dynamic/slice/unpack/alias/arbitraryeval或duplicatekey／uncertaincollision／position，不新增lastwins／failclosed。
4. C52 在 `tests/test_loaded_runtime_cache_bc_independence.py` 將三existingcurrent-source scannersdiscover suffix擴為.py＋.pyi並原樣沿existingrules，對兩BC各三checks設regression，不新增stubgrammar／productionstub或fixtureexecution。
5. C52 在 `tests/test_loaded_runtime_cache_bc_independence.py` 保留existingdirectimports／fixtures／mocks／assertions／十二locks，實際通過sameimmutablegreenS兩檔pytest／Ruff／strictPyright；完成需same-ScommittedpassingT實證，review／publish／class/actions非implementationcompletion。

### Validation / Acceptance / Ordered Evidence Chain

IndependentTesterREDcommands：
```bash
uv run --frozen pytest -p no:tach tests/test_loaded_runtime_cache_bc_independence.py -k c52 --collect-only -q
uv run --frozen pytest -p no:tach tests/test_loaded_runtime_cache_bc_independence.py -k 'c52 and not rejects' -q
uv run --frozen pytest -p no:tach tests/test_loaded_runtime_cache_bc_independence.py -k c52 -q
```
REDgenuineassertionfail／collectioncontrols0→factualfailingT；parse/collectionfailure、controlsnonzero或需求未RED不得稱gate。
Greenactualcommands：
```bash
uv run --frozen pytest -p no:tach tests/test_loaded_runtime_cache_bc_independence.py tests/test_loaded_runtime_cache_contracts.py -q
uv run --frozen ruff check tests/test_loaded_runtime_cache_bc_independence.py tests/test_loaded_runtime_cache_contracts.py
uv run --frozen pyright tests/test_loaded_runtime_cache_bc_independence.py tests/test_loaded_runtime_cache_contracts.py
```
1. Exact-fiveplanningdraft→Planner→LOCALexact-fivecandidate→independentfreshPlanReviewerreceipt→approvedsoleLOCALcommit。
2. Test-onlyREDsinglepath→independentTesterfailingfactualrecord→solefailingTcommit→boundedgreennewimmutableSsinglepath。
3. IndependentTestersame-Sactualpassingrecord→solepassingTcommit；不借C50evidence／不把expectedfail當pass。
4. PlanCreatorONLYplanstepreview-readyfactualalignment→ImplementerseparateLOCALalignmentcommit→PlannercanonicalCLIactual0
   →IndependentReviewerconsumecommittedsame-SpassingT寫freshV→Implementer unchangedsoleapprovedV。
5. PlannerPhase4.5→PlanCreatorONLYplanstepfactualalignment→Implementerseparatenormalcommit／push existingPR7。
6. Planner核actualfixedpublishedhead／newS/T/V／sourceunchanged→IndependentReviewerexact-threefreshclassification
   →Implementer unchangedsoleclassnormalcommit／push→PlannerrouteonlycommittedR&R。
7. ImplementeronlyexactR&Roriginalreply／resolve，重核避免duplicate、記actualreplyID／resolvedfacts；
   ADDRESS／HUMAN_CHECKopen，scope-requiredHumanchoice一次彙整；七inventory-only不得act。
8. PlanCreatorONLYplanstepfinalactualfacts（真完成才[X]，需求未修不勾）→Implementerseparatenormalcommit／push
   →singlefull-paginationaudit→human-check。No future ownSHA／commitpush預填／selfcheckbox-loop，
   不為bot新留言無限續修，newunlistedinventory-only。
各stageactualGitfullSHA／namedsolepath／schema／sourcebounds檢查、`git diff --check`；
`python .agents/skills/plan-step-tracker/scripts/step_tracker.py check_impl_steps_succeeded loaded-runtime-cache`
draftactualexit1=五pending，review-ready才actual0。
Headdrift／sourcedrift／required evidence欠缺／wrongwriter/schema/solecommit／scope或contractdrift停相應gate交Planner，
不改candidate／head／contract或自算approval。普通hooks，失敗不自行noverify。

### Open Questions / Reviewer Handoff / Post-merge

C52D1non-trivial：三AST/filediscovery behavior與完整newsubject-boundchain；requiredspec／step同candidate。
七decisions、non-goals、五testcategories、scope/writer/schema皆明定；designnone。
Unknownselectors／duplicatekeys／collision不推論已固定，不需要補新dictionaryprecedence決策。
actualcandidate／RED／newS／T/V／publishedhead／classifications／replyids/results尚未產生，不預fill。
七inventory-only與十二locks不變，scope外requirements onlyinventory／Human一次決定。
Post-merge／releaseactionsnone；HumanalonePRreview／merge／release／postmerge／tag；reviewapproval不等於merge。
```json
{"verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]}}
```
Independenthandoffschema非Creator預填receipt。
Workflowstate：current_step=c52-plan-authoring；next_step=bounded-candidate-commit；
status=COMPLETE（draftonly，非executionapproval／evidencegate／topiccomplete）。

## C53 Current-Head Eight-Pair Classification（completed predecessor routing）

C53finalalignment `d8e723985791665583444d2ea1d1c18237d3246c` 已normalcommit/push，
C54唯一currentrepairroute；C53pending/Current字樣onlyfrozenhistory。

### Goal / Outcome / Scope / Locked Decisions

Current：`planned`；phase：`plan-authoring`；existingPR7pr-open。
C53是唯一currentclassification-onlyroute；C52及更早records為completed/frozenprovenance。
Goal／In-Scope：以fixedpublishedhead與同-ScommittedpassingT／approvedV，獨立分類下列eightactualpairs，
只對committedREPLY_AND_RESOLVEexactpairs留言原文與resolve。Outcomes不預設，不用「想收束」視為修復。
原mission／scope／outcomes／Registryprotocol／API／ArchitectureVisualization／follow-upmissions不變。
Analysisstrictmode：technical-specexecution-facingtruth／requirementsintentguardrail，
本C53共同契約逐字同步standard-five；finalalignmentONLYplanstep。

Out-Of-Scope／Non-Goal：code／grammar／architecture／publicAPI／typing／dependencies／README／VERSION／
uv.lock／repositorycontracts／十二locks修改；新RED／S／T／V／語意修復、merge／release／postmerge／tag／新PR／重寫history。
ReadOnly：allsource／tests／config／oldcandidate/receipt／fixedSTV／architecture／Archify／sharedcontracts。
Written／Modify：Plan-Creatorcandidateonlyexact-five；finalalignmentonlyplanstep；Deletednone。
- `analysis/loaded-runtime-cache/requirements.md`
- `analysis/loaded-runtime-cache/technical-spec.md`
- `plan/loaded-runtime-cache/loaded-runtime-cache.plan.md`
- `plan/loaded-runtime-cache/loaded-runtime-cache.spec.md`
- `plan/loaded-runtime-cache/loaded-runtime-cache.step.md`
dev／unlistedpaths不動；非唯一agent不revertothers；三rejecteduntrackedimmutable不stage／改寫／刪除／當authority。
十二semantic／grammar／architecture／READMElocks不變；classification不解除locks或批准未授權修復。
C52canonicalfivecompletedimplementation保留歷史completion，不新增fakecodepending／跨subjectreuse。
Pythonmetadata／七decisions保留，noAPI/interface/breakingchange/dependency/errorstrategy/typingchange。
Async-planning status: exempt — cite exemption evidence: classification／tracking-only，无asynccode／lifecycle／I/Oconcurrency變更。
Stablelibraryintentabsent，不改README／VERSION或releasepolicy。

### Actual Fixed Facts / Exact Inputs

Authoringbase／fixedreviewedPRhead `5bf16409d19df472eb17f9fb2150c95b47df1478`：
C52finalactualalignment已normalcommit／push，local／origin／PR一致、OPEN／MERGEABLE／CLEAN、
tracked/indexclean、三rejected保留。Plannerfreshsnapshot135threads／127resolved／8open，不猜UTC。
FixedS `2bb82f062657d8c9dd0686743c8ee46e247926d4`；
passingTsole `ff0a3bf6c52facc266682eea2068c305791ad257`；
approvedVsole `2047839048bcd1ac6b2af915f78f38ff294f0013`。
Planner已核sameSTV／actualancestry／sourceunchanged；無code改動C53可消費sameSevidence，
不背書newsubject／historicalalternativehistory或把舊evidence改成新evidence。
C52三exactactions保留，不重覆。八原始留言已唯讀核body／ID／originaltarget，分類輸入非修復契約：

| Thread suffix | Comment string | Actual original input（outcome由IndependentReviewer決定） |
| --- | --- | --- |
| `pvzDA` | `4202824859` | P2：PEP695 class/function/typealias的type_params（TypeVar／TypeVarTuple／ParamSpec）建立foreignsemanticbinding；建議兩BCregression。 |
| `pvzDF` | `4202824865` | P2：sys.__dict__["modules"]／.get("modules")未納既有sys.modulessurface，建議namespacecachelookupregression。 |
| `pvzDH` | `4202824868` | P2：BoolOp選出的forbiddencallable如False or importlib.import_module後USE或map，建議operandalternatives；非既有IfExp修復授權。 |
| `pv59N` | `4202868919` | P2：vars(importlib)["import_module"]／vars(builtins)["__import__"]lookup漏檢，建議knownmodulevarslookup。 |
| `pv59R` | `4202868923` | P2：ExceptHandler.name的foreignsemanticbinding，建議兩BCregression。 |
| `pv59T` | `4202868925` | P2：不同branch import同localname最後覆寫module，建議保留finiteimportmodulealternatives及branchorderregression；本輪不實作。 |
| `pv59V` | `4202868928` | P2：functionreturnforbiddencallable再immediateUSE漏檢，建議boundedreturnresolution及unusednegative；本輪不授權call-graph或return推論。 |
| `pwUaF` | `4203037740` | P1：alleges historical0a3f417e…／parentd6ff74dd…無C52S/T/Vancestry且co-addedimplementation/evidence；獨立核完整currentfixedheadgraph／solecommits，不因歷史shorttarget將currentapproval補成合法或一概失效。 |

前七path tests/test_loaded_runtime_cache_bc_independence.py；前三originaltarget9a8b46fa72a9800622349b049cc03d06b57e5f9f、
後四165087337ac5dea9fdbd307021c322ca7226c2e9；
pwUaF原path為same-S implementationreviewlog，originaltarget5bf16409d19df472eb17f9fb2150c95b47df1478。
目前eightopen；Reviewer核currentevidence，不預定必要性／已修復／HUMAN。
新unlistedinventory-only，不分類／回覆／resolve；scope外修復／lockedsemantics需要Human一次決定。

### Artifact Paths / Immutable Schemas / Sole Writers

IndependentPlanReviewerwriter：
`plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<actual-C53-candidate-full40SHA>.json`。
Actualexact-fiveLOCALcandidatecommit後展開freshpath，不預填SHA/verdict。
Exact3keys verdict／blocking_issues／copilot_feedback_triage；
approved|needs-rework，blocking_issuesobjectsarray（each恰issue／file／fixnon-emptystrings），
approved[]／needs-rework至少一項，triage恰ADDRESS／DISCUSS／SKIParrays。
PlanRevieweronlyreview/write、不commit；approved才Implementer unchangedsoleLOCALreceiptcommit。
candidate／approvedreceipt分類前LOCAL，不推fixedremotehead。Freshpath不得overwriteexisting或rejectedreceipt。

IndependentReviewerclassificationwriter：
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-2bb82f062657d8c9dd0686743c8ee46e247926d4-5bf16409d19df472eb17f9fb2150c95b47df1478.json`。
Exact8keys schema_version／topic／implementation_subject_commit／tester_evidence_commit／
implementation_review_evidence_commit／pr_head_commit／classifications／recorded_by。
Integer1／topic loaded-runtime-cache／exactfixedS/T/V/head full40lowercasehex；recorded_by `Independent Reviewer`。
Classifications恰8entries，各上述pair一次；each恰thread／comment／outcome／reply。
Suffixstring（非fullPRRTID）、commentstring；outcome REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK，independently判定。
R&Rreplynon-emptyoriginalfactualreply、currentcommittedfacts支持；ADDRESS／HUMANreplynull／open。
不能用留言補未授權fix／historicapproval。Revieweronlyfreshwrite、不commit或留言；
Implementerunchangedsoleclassnon-mergeevidence-onlycommit／normalpush，不混planning/code/anotherreceipt。
所有solepath/schema/writer/subject以actualGitfacts驗，missing／wrong／crosssubject／shortSHA／overwrite failclosed。

### Ordered Route / Validation / TestCase

1. PlanCreatorstandard5draft→Plannerpreflight→Implementerexact5LOCALcandidate-onlycommit。
2. IndependentPlanReviewerfreshSHAreceipt→approved才ImplementerunchangedsoleLOCALreceipt。
3. Plannerfixedhead／committedsamepassingT/approvedV／ancestry/sourceunchanged／freshpathgate，
   不自行換head或補推gate，無新RED／implementation／Tester／Vphase。
4. IndependentReviewerexact8class→Implementerunchangedsoleclassnormalcommit／push。
5. Planner核committedreceipt／sourceunchangeddescendants後只routeexactR&Ractions；
   Implementeroriginalreplyresolve前重核防duplicate，記actualID／resolvedfacts。
   ADDRESS／HUMANopen，Humanrequirements一次彙整。
6. PlanCreatorONLYplanstepfinalfactualalignment，真completedworkflow才[X]／未fixrequirements不虛勾
   →Implementerseparatenormalcommit／push→singlefullpaginationaudit→human-check。
   No futureownSHA/commitpush預填／selfcheckbox-loop，新unlistedinventoryonly，PR7pr-open、不追bot無限續修。
Normalhooks，C28noverify等歷史subject-only授權不可沿用，blockingerror回Planner不繞過。

TestCase／Acceptance：
- Happy：approvedreceipt／sameSTV/fixedhead/exact8class支持onlyindividualfactualR&Ractions。
- Invalid：wrongkeys/type/writer/pair/SHA/solepath/receiptfailclosed。
- Edge：historical0a3f417e allegation不等於currentfixedheadgraph；technicalinput不等於newgrammar授權。
- Regression：canonicalC52fivecompleted／sameSTV/sourceblobs/十二locks/oldreceipts保持。
- Compatibility：productionAPI/protocol/outcomes/directimports/fixtures/assertions/Archify/Pythonmetadata不變。
Givenapprovedcandidate/eightactualcomments，Whenindependentcurrentfactsreview，Thenexact8outcomes由evidence决定非預设。
GivenADDRESS/HUMAN，Thenreplynull/threadopen；GivencommittedfactualR&R，Then才能originalreplyresolve。
Givenhead/source/schema/solepathdrift或requiredevidence欠缺，Thenfailclosed交Planner、不自改contract。
上述亦specAcceptanceCriteria／BehavioralScenarios／ErrorEdgeCases，no executablefix或新tests。

Planningactualchecks：`git diff --check`；
`python .agents/skills/plan-step-tracker/scripts/step_tracker.py check_impl_steps_succeeded loaded-runtime-cache`
應0＝C52existingfivecompletion，非C53codeapproval。
Read-onlyactual `git rev-parse HEAD`／`git status --short`／namedsolecommit/JSONchecks；
`git merge-base --is-ancestor 2bb82f062657d8c9dd0686743c8ee46e247926d4 5bf16409d19df472eb17f9fb2150c95b47df1478`
以及同T/Vancestry；
`git diff 2bb82f062657d8c9dd0686743c8ee46e247926d4 5bf16409d19df472eb17f9fb2150c95b47df1478 -- src tests`；
分類前重新read-onlyPRhead／fullthreads/allcomments。
真正scope/contract/lockeddecision新選擇一次交Human，不guess/nonroutingchat代evidence。

### Risks / Rollback / Open Questions / Reviewer Handoff

Risks：預設outcomes、historicshorttarget冒充currentgraph、scopegrammardrift／跨subject／stalehead、
duplicate replies／evidencesolecommit污染／selftrackingloop。
Rollback：onlyboundedstandard5planningrework或必要freshimmutablecandidate；不broadreset／overwrite／sourcefix，
oldreceipts/STV／三rejected保留。
OpenQuestions：designnone；八independentoutcomes待實際分類、超scope必要修復Human一次選擇。
Post-merge/release:none；HumanalonePRreview/merge/release/postmerge/tag。
```json
{"verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]}}
```
Independenthandoffschema，非Creatorapprovalreceipt。
Workflowstate：current_step=c53-plan-authoring；next_step=bounded-candidate-commit；
status=COMPLETE（draftonly，非classification/actions/Humanapproval/topiccomplete）。

## C54 Bounded Seven-ADDRESS Repair（authoritative current routing）

### Goal / Outcome / Scope

Current：`planned`；phase：`plan-authoring`；existingPR7pr-open。
C54是唯一currentrepairroute，Human已明確授權下列七boundedrepairs，
C53與較早records為completed/frozenprovenance。原LoadedRuntimeCachemission／scope／outcomes／
Registryprotocol／API／ArchitectureVisualization／follow-upmissions不變，不另開topic或Pythonplan。
Analysisstrictmode：technical-specexecution-facingtruth／requirementsintentguardrail；
本共同契約逐字同步standard-five，之後ONLYplanstep factualalignment不再開candidatechain。

In-Scope／Goal：唯一testmodule的七scanner缺口及isolated RED/controls，
新immutableRED／greenS／same-SindependentT/V／normalpublish／actualfixedheadexact-sevenclassification及permittedactions。
Out-Of-Scope／Non-Goal：其他code/grammar／任意eval/truthiness／CFG/branchfeasibility/orderedscope／arbitrarycallgraph/
argsubstitution／asyncfactory/generator／productionAPI/stubs/architecture/README/VERSION/dependency/config/uv.lock/
repositorycontracts/十二locks變更／newunlistedrepair、merge/release/postmerge/tag、新PR或historyrewrite。
ReadOnly：allsource、其他tests、config、contracts、oldreceipts/STV、architecture/Archify；
existingdirectimports/fixtures/mocks/assertions不變。Deletednone。
Written／Modify：PlanCreator候選onlystandard5，Implementerimplementationonly
`tests/test_loaded_runtime_cache_bc_independence.py`，independentfreshSHAevidence依後表。
devworktree不write；非唯一agent不revertothers；三rejecteduntrackedimmutable保留，
不stage/overwrite/delete或当routingauthority，所有unlistedpaths停Planner。

### Locked Seven Behavior Contracts / TestCase Inputs

| Exact pair | Bounded behavior（不得重開decision或擴grammar） |
| --- | --- |
| `pvzDA/4202824859` | PEP695 genuineTypeVar／TypeVarTuple／ParamSpec的name，ClassDef／FunctionDef／AsyncFunctionDef／TypeAlias.type_params；兩BCforeignsemanticownership。 |
| `pvzDF/4202824865` | knownsysName/既有modulealias.__dict__ directliteral "modules" subscript或既有exact-onepos/no-keywords/default .get，解析原sys.modulessurface／existingcacheUSE。 |
| `pvzDH/4202824868` | BoolOp僅明確literaltruth／knowncallable所選取/可確定reachableexistingforbiddencallable後USE，dead False and／True or不誤拒，unusednegative。 |
| `pv59N/4202868919` | knownbarebuiltin vars(knownmodule)exact-onepos/no-keywords，directliteralnamespace沿原surfaces與existingUSE。 |
| `pv59R/4202868923` | ExceptHandler.name的genuineforeignlocalbinding，except及except*；不把exceptiontypereferences當binding。 |
| `pv59T/4202868925` | same simple local import binding的有限knownmodulealternatives，branchorderinvariant／existentialexistingUSE；unusednegative。 |
| `pv59V/4202868928` | directFunctionDef body single directReturn knowncallable、directlocal-namefactorycall後immediateUSE；return-but-unusednegative。 |

1. Typeparameters只檢查ast.TypeVar／ast.TypeVarTuple／ast.ParamSpec genuine.name；
   bounds／constraints／references不作新binding、不求值或重新解讀Identity。
   LoadedRuntimeCache不得localModelIdentity，Identity不得localRuntimeReuseKey；普通names／references保留。
2. Sysnamespace僅knownsysreceiver及literalmodules，沿existingnamespace subscript／boundedgetgrammar，
   unknownreceiver／dynamickey／ordinarynamespaceentry不推論、不增加保守拒絕；
   不擴.get default/keywords或既有getattr exact-twoarity鎖。
3. BoolOp只用明確literaltruth或已知callable的確定truth／短路selected/reachableoperands判existingUSE；
   deadoperand不得因含forbiddencallable而拒絕，unusedpossession合法。
   Unknowntruth不做CFG／eval／arbitrarytruthiness，不推branchfeasibility／orderedbindings；
   不執行fixture，不把AST中「出現」callable當USE。控制True or／False and與ordinaryselectednegative。
4. Vars僅knownbarebuiltin `vars`、knownmoduleName/既有alias、exact-onepos/no-keywords；
   只正規化已確定namespace後沿existingdirectliteralnamespace/surfaces/USE，
   unknownreceiver／arbitrarycallresult／mapping／dynamickey不推論，
   不新增vars getteralias/call-resultgrammar或重開getattrarity／scope-shadowing鎖。
5. Except／except* onlyast.ExceptHandler.name字串本地binding，兩BC對稱；
   exceptiontype／tuple exceptionrefs、ordinaryhandlername不是foreignbinding。不執行handler。
6. Importalternatives只同simplelocalimportbinding中的有限knownmodules，
   任一alternative＋既有forbiddenUSE作existential判定，換branch/statementorder不掉alternative；
   不建立pathfeasibility／CFG／ordered-scope／stalealiasinvalidation或arbitrarymoduleimport推論，
   unusedmodule/callablepossession不新增拒絕。
7. Factory僅directFunctionDef、唯一bodystatement直接Return已知callable，
   經directlocal-namefactorycall後immediateexistingforbiddenUSE（不是只return/只持有）。
   不做argument substitution、decorator、async/generator、multipleReturn/otherbodyStatements、
   recursion、arbitrarycallgraph/callresultresolution或sourceexecution。
   任何不在此bounded形狀的factory不由本修正推論，returned-but-unusednegative保持。
8. 十二semantic/grammar/architecture/READMElocks不變；不新增crossBCimports／mapper／backend／DI/lifecycle；
   directimports、所有existingfixtures/mocks/assertions、productionprotocol/outcomes／Archify不變。
   Newunlistedonlyinventory／open，不分類/修復/留言/resolve；超scope或新lockeddecision一次交Human。

### Actual Base / Status / Allowed Transitions

Actualauthoringbase `d8e723985791665583444d2ea1d1c18237d3246c`，
C53finalalignment已normalcommit/push；Plannerfreshsnapshot135threads/128resolved/7open，
exact七ADDRESS均必要未修，不猜auditUTC／預填C54candidate/SHA/results。
C53candidate `ce4f9682da4192caca3fc4079245fc172dfd65a8`、
approvedreceiptsole `2b43688a8c8e458cdd778ae834183861ffff1189`、
classificationsolepush `477094c768e857a768407b6a2faf0e23a57f08d9` frozenfacts。
舊S `2bb82f062657d8c9dd0686743c8ee46e247926d4`、
T `ff0a3bf6c52facc266682eea2068c305791ad257`、
V `2047839048bcd1ac6b2af915f78f38ff294f0013` 是C52predecessorhistory，
不能為C54newsubject充當passingT／approvedV。
C52canonicalfivecompleted歷史保留，C54newcanonicalninesteps pending不繼承completion。

planned→LOCALcommittedcandidate／independentapprovedreceiptsole→creator-in-progress test-onlyRED
→independentTesterfactualfailingTsole→distinctgreennewS→tester-in-progress same-SpassingTsole
→review-readyfactualalignment/CLI0→independentreviewer-in-progress→approved|needs-rework。
needs-rework onlyboundedImplementer/newS/完整sameSTV重走，不覆寫evidence或以舊subject救gate。
approved→PlannerPhase4.5factualalignment→publish-in-progress→existingPR7pr-open
→actualfixedpublishedheadexact-sevenclass→per-pairpermittedactions→finalfacts/human-check。
Planningapproval非executionapproval；Reviewer非HumanPRreviewer；
publish-in-progress不得直接merged，HumanalonePRapproval/merge/release/postmerge/tag。

### Artifact Paths / Owners / Immutable Schemas

PlanCreatoronlycandidateexact5，review-ready/Phase4.5/finalstatealignment ONLYplanstep：
- `analysis/loaded-runtime-cache/requirements.md`
- `analysis/loaded-runtime-cache/technical-spec.md`
- `plan/loaded-runtime-cache/loaded-runtime-cache.plan.md`
- `plan/loaded-runtime-cache/loaded-runtime-cache.spec.md`
- `plan/loaded-runtime-cache/loaded-runtime-cache.step.md`
ImplementeronlyRED/green `tests/test_loaded_runtime_cache_bc_independence.py`；
contractstests/pyproject為ReadOnlyvalidationinputs，src/uv.lock/其他paths不動。
Evidenceparameters只actualcommittedfull40lowercasehex後展開freshpath；
不symbolicHEAD／shortSHA／future結果預填／overwrite任何existingpath（含rejecteduncommitted）。
每independentwriter只寫自己的record、不commit；Implementer unchangedsoleevidence-onlynonmergecommit，
不與planning／implementation／另一evidence混commit，actualnamedsolepath/schema/writer/subject逐一核。

IndependentPlanReviewer：
`plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<actual-C54-candidate-full40SHA>.json`。
Exact3keys verdict／blocking_issues／copilot_feedback_triage；
approved|needs-rework，blocking_issuesobjectarray(each恰issue/file/fix non-emptystrings)，
approved[]／needs-reworknonempty；triage恰ADDRESS/DISCUSS/SKIParrays。
Committedexact5LOCALcandidate才review，approved才unchangedsoleLOCALreceiptcommit、不先push。

IndependentTesterRED：
`plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<actual-C54-RED-full40SHA>.json`；
IndependentTestergreen：
`plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<actual-C54-green-S-full40SHA>.json`。
Exact6keys schema_version/topic/implementation_subject_commit/status/commands/recorded_by；
integer1／loaded-runtime-cache／actualRED或newgreenS／passing|failing／`Tester`；
commandsnon-emptyarray(each恰commandnon-emptystring／exit_codeinteger)。
Passing只有全部actual0，failing至少一actualnonzero。
REDcollection/controls必0，七原finding各有genuineassertionfailure，不parse/import/collectionfailure；
failingRED不寫Reviewerevidence、不當expected-failingpass。Tester真實獨立測immutable subject，
Implementer unchangedsolefailing/passingT各自commit，不借C52evidence。

IndependentReviewer：
`plan/loaded-runtime-cache/loaded-runtime-cache.implementation-review-log-<actual-C54-green-S-full40SHA>.json`。
Exact7keys schema_version/topic/implementation_subject_commit/tester_evidence_commit/
verdict/blocking_issues/recorded_by；integer1／loaded-runtime-cache／sameactualnewS／
committedsame-SsolepassingT fullSHA／approved|needs-rework／stringarray／`Independent Reviewer`。
Approvedblockers[]，needs-reworknonempty；missing/failing/uncommitted/crossS/malformedT failclosed，
不得產V。Reviewer獨立審、不commit；Implementer unchangedsoleV。

Independentclassification：
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-<actual-C54-green-S-full40SHA>-<actual-reviewed-published-PR-head-full40SHA>.json`。
NewpassingT/approvedV/Phase4.5normalpublish後，Planner核actualfixedhead才展開freshpath；
exact8keys schema_version/topic/implementation_subject_commit/tester_evidence_commit/
implementation_review_evidence_commit/pr_head_commit/classifications/recorded_by；
integer1／loaded-runtime-cache／newS/sameT/sameV/actualfixedpublishedheadfull40hex，
recorded_by `Independent Reviewer`。
Classifications exact7entries上表pairs各一次，entry恰thread/comment/outcome/reply；
threadsuffixstring、commentstring；outcome REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK，獨立判、不預設。
R&Rreplynon-emptyoriginalfactualreply，ADDRESS/HUMANnull且open；
Revieweronlywrite、不留言commit，Implementer unchangedsoleclassnormalcommit/push。
Planner核committedreceipt/sourceunchangeddescendants後才exactactions。
Wrongschema/writer/SHA/topic/pair/solecommit、overwrite/drift停gate交Planner，不自改contract。

### Python implementation metadata（C54 current bounded profile）

#### Non-goals
- 不改productionAPI/protocol/outcomes/Identityauthority/Archify/backend/lifecycle。
- 不執行source、arbitrarytruthiness/eval、CFG/feasibility/orderedscope、arbitrarycallgraph/argument substitution。
- 不改十二locks/unknowngrammar/newunlisted、README/VERSION/dependencies/config/uv.lock/sharedcontracts。
- 不merge/release/historyrewrite/新PR，不動dev或otheragentfiles。

#### Current Context / Requirements
現有testscanner尚未涵蓋七已獨立分類ADDRESS：typeparameterbindings、
sysnamespace、BoolOpselectedforbiddenUSE、varsnamespace、exceptionnamebinding、
finitebranch-importaliases、boundedfactoryreturnedcallable。
只補上表七exactscope，privateASThelperrepresentation由Implementerbounded選擇，
原knownsurface/USE/negativebounds和pureparse不变。
七positive需求各有isolatedgenuineRED，全部七類依兩BCsourceboundary對稱驗證，semantic ownership亦對稱；
不得削弱assertions/fixtures、skipregression或動態載入達green。

#### Decisions
- Async-planning status: exempt — cite exemption evidence: 同步ASTscanner/testfixtures，
  AsyncFunctionDef只檢type_params syntax，except*只binding；不執行source或引入asyncboundary/
  lifecycle/resourceownership/I/Oconcurrency/timeout/retry/cancellation；asyncfactory明確排除。
- Module/packageplacement: only `tests/test_loaded_runtime_cache_bc_independence.py` existingscanner/isolatedfixtures。
- NewpublicAPI: no，no newproductionmodule/stub/packageexport。
- Interfacechanges: no productionchanges，只七declaredscannerbehavior。
- Breakingchangesallowed: no，preserveexistingdirectimports/fixtures/mocks/assertions/negativecontrols。
- Newdependencies: no，existingast/pytest/Ruff/strictPyright，uv.lock不改。
- Error-handlingstrategy: existingparse/assertionexceptionpropagation保持，不swallowerrors；unknowntruth/
  factory/receiver不推論，不新增failclosed／possession拒絕，不改RuntimeRegistryoutcomes。
- Typingstrategy: Python3.12strictPyright、preciseASTtypedhelpers/noAny，
  noimportlib/__import__/sys.modules substitution。

#### Public Contract / API Changes / Affected Files
No public/productioncontractchanges；onlydeclaredtestpath。
Inspectsamefile、ReadOnlycontractstest/pyproject；planning/evidenceexactowners依前表，
Deletednone，otherpaths及sourceReadOnly。

#### Test Plan / TestCase
- Happy：兩BCPEP695三typeparamkind／definitionkinds、sysliteralnamespace/subscript/get/cacheUSE；
  literalshort-circuitBoolOpselectedknowncallableUSE、knownbarevarsnamespaceUSE；
  except/except*namebindings、branchorder-swappedfiniteimportalternatives、singleReturndirectfactoryimmediateUSE。
- Invalid：unknowntruth/receiver/module/factory、dynamicnamespacekey/default/keywords/wrongarity；
  不在factoryshape（decorator/async/generator/多Return/其他statement/argsubstitution/recursion），不誤parsefailure為RED。
- Edge：True or／False and deadforbiddenoperand、unusedcallable、ordinaryselected；
  typebound/class/reference與exceptionreference不是binding、branchorderinvariant、
  returned-but-unusednegative，knownmodulealternatives依existingUSE不CFG。
- Regression：所有existingdirectimports/fixtures/mocks/assertions、twelve locks、C52captures/literalcontainers/.py/.pyi、
  C50getattr/namespace/arguments/comprehensionsemantic/alternatives/sys.modules規則保持；
  realpassing兩scopedpytest檔/Ruff/strictPyright。
- Backwardcompatibility：runtimeprotocol/outcomes/Identityindependence/taxonomy/publicsurface/Archify不變，
  fixture source不執行，no productionstub或dependency。
Givenoldscanner/sevenoriginalpositivefixtures，WhenREDparse，Thencollection/controls0且七findinggenuineassertionfail。
Givenboundedgreen，Whengenuineforeignbinding／確定selectedforbiddenUSE／boundedfactoryimmediateUSE，
Thenreject；Givenreferences/dead/unused/unknown/excludedshape，Then本修正不新增誤拒/推論。
GivennewScommittedpassingT/approvedV與actualpublishedhead，Thenonlyindependentexact7classification可routeactions。
以上亦specAcceptance/GWT/ErrorEdgeCases，requiredspec/step非第二plan。

#### Risks / Rollback
Risks：死operand誤拒、未知truthiness/sourceexecution、有限modulealternatives遺失、
factory擴callgraph/parameters/scope、refs誤作bindings、C52evidence替newS、
REDparseerror、stalehead/duplicate回复/selftrackingloop。
Rollback：onlysingledeclaredtestboundedfix/newimmutableS完整T/V；planningonlystandard5經Planner，
保留allcommittedcandidate/RED/S/T/V/receipts，不broadreset/overwrite/contractfix/清三rejected；
ordinaryhooks，C28noverify subject-only授權不可沿用。

### Implementation Steps（source for canonical completion gate）

1. C54 在 `tests/test_loaded_runtime_cache_bc_independence.py` 新增七originalfindingisolated RED/benigncontrols；names含c54、rejecting另含rejects、controls不含rejects，只新增tests不修scanner/不execute，collection/controls0、七類genuineassertionfail。
2. C54 在 `tests/test_loaded_runtime_cache_bc_independence.py` 檢PEP695 genuineTypeVar/TypeVarTuple/ParamSpec names於ClassDef/FunctionDef/AsyncFunctionDef/TypeAlias.type_params，兩BCsemanticownership；不檢bound/reference語意或eval。
3. C54 在 `tests/test_loaded_runtime_cache_bc_independence.py` 納knownsysName/modulealias.__dict__literalmodules subscript/既有exact-onepos/no-keyword-default.get為existing sys.modules cacheUSE；unknown/ordinarynegative保持。
4. C54 在 `tests/test_loaded_runtime_cache_bc_independence.py` 解析BoolOp明確literaltruth/knowncallable所選或可確定reachableexistingforbiddenUSE，deadFalseand/Trueor與unused不誤拒；unknowntruth無CFG/eval/arbitrarytruthiness。
5. C54 在 `tests/test_loaded_runtime_cache_bc_independence.py` 將knownbarebuiltinvars(knownmodule)exact-onepos/no-keywords之directliteralnamespace沿originalsurfaces/USE，不推unknownreceiver/callresult/mapping/dynamickey或改getattraritylocks。
6. C54 在 `tests/test_loaded_runtime_cache_bc_independence.py` 檢ExceptHandler.name的except/except* genuinebinding、兩BC對稱，不把exceptionrefs當binding或執行handler。
7. C54 在 `tests/test_loaded_runtime_cache_bc_independence.py` 保存same simplelocalimport之finiteknownmodulealternatives，branchorderinvariant existentialexistingUSE、unusednegative保持；不CFG/feasibility/orderedscope推論。
8. C54 在 `tests/test_loaded_runtime_cache_bc_independence.py` 支援directFunctionDef單一directReturn knowncallable、directlocal-namefactorycall後immediateUSE；排除argsubstitution/decorator/async/generator/multiReturn/otherstatements/recursion/arbitrarycallgraph/callresult/execution，returnunusednegative保持。
9. C54 在 `tests/test_loaded_runtime_cache_bc_independence.py` 保留所有existingdirectimports/fixtures/mocks/assertions/十二locks，對sameimmutablegreenS真通過兩檔pytest/Ruff/strictPyright，完成需sameScommittedpassingT證明；review/publish/class/actions不是此completiongate。

### Validation / Ordered Evidence Chain

IndependentTesterREDactual：
```bash
uv run --frozen pytest -p no:tach tests/test_loaded_runtime_cache_bc_independence.py -k c54 --collect-only -q
uv run --frozen pytest -p no:tach tests/test_loaded_runtime_cache_bc_independence.py -k 'c54 and not rejects' -q
uv run --frozen pytest -p no:tach tests/test_loaded_runtime_cache_bc_independence.py -k c54 -q
```
Collection/controls0＋七originalgenuineassertionfail才factualfailingREDrecord；parseerror/controlsnonzero/需求未紅不宣稱REDgate。
IndependentTestergreenactual：
```bash
uv run --frozen pytest -p no:tach tests/test_loaded_runtime_cache_bc_independence.py tests/test_loaded_runtime_cache_contracts.py -q
uv run --frozen ruff check tests/test_loaded_runtime_cache_bc_independence.py tests/test_loaded_runtime_cache_contracts.py
uv run --frozen pyright tests/test_loaded_runtime_cache_bc_independence.py tests/test_loaded_runtime_cache_contracts.py
```
1. PlanCreatorexact5draft→Planner→ImplementerLOCALexact5candidate-onlycommit
   →IndependentPlanReviewerfreshreceipt→approvedsoleLOCALcommit，無code/evidence/push混candidate。
2. Implementertest-onlyREDsinglepath→IndependentTesteractualfailingrecord→unchangedsolefailingT
   →boundedgreennewSsinglepath；不借C52passing/approvedevidence。
3. IndependentTestersameSactualgreenpassingrecord→Implementer unchangedsolepassingT。
4. PlanCreatorONLYplanstepreview-readyfactualalignment→ImplementerseparateLOCALalignmentcommit→PlannercanonicalCLI0
   →IndependentReviewerconsumecommittedsameSpassingT/writefreshV→Implementer unchangedsoleapprovedV。
5. PlannerPhase4.5→PlanCreatorONLYplanstepfactualalignment→Implementerseparatenormalcommit/push existingPR7。
6. Planner核actualfixedpublishedhead/newSTV/unchangedsource→IndependentReviewerexact7freshclass
   →Implementer unchangedsoleclassnormalcommit/push→PlannerrouteonlycommittedfactualR&R。
7. Implementerexactoriginalreply/resolve前核現況防duplicate、記actualreplyID/resolved；ADDRESS/HUMANopen，
   scope-requiredchoices一次交Human，不把codecompletion勾選當threadsapproval。
8. PlanCreatorONLYplanstepfinalfacts（真完成workflow才[X]、未fixrequirements不虛勾）
   →Implementerseparatenormalcommit/push→singlefullpaginationaudit→human-check。
   No ownfutureSHA/commitpush預填/selfcheckbox-loop/newcandidatechain；newunlistedonlyinventory，不無限追bot。
ActualGitfullSHA/parent/namedsolepath/blob/JSON/sourcebounds逐階驗；`git diff --check`；
`python .agents/skills/plan-step-tracker/scripts/step_tracker.py check_impl_steps_succeeded loaded-runtime-cache`
draftexit1=ninepending，review-ready才actual0。
Normalhooks，失敗不noverify；head/source/evidence/schema/writer/solepath/scope/contractdrift停相應gate，
交Planner，不改head/candidate/contract或自行算approval。

### Open Questions / Reviewer Handoff / Post-merge

C54D1non-trivial：七scannerbehaviors、finitealternatives/shortcircuit/boundedfactory/完整newsubjectchain，
requiredspec/step同步，不需Human重複確認已授權bounds。
七decisions/async-exempt/non-goals/五testcategories/fullschemas皆明定，designnone。
Actualcandidate/RED/newS/T/V/head/outcomes/replies/testresults未產生，不預填。
Twelve locks/newunlistedonlyinventory不變；scope外新選擇一次Human。
Postmerge/releaseactions:none；HumanalonePRreview/merge/release/postmerge/tag，
IndependentReviewerapproval非Humanapproval。
```json
{"verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]}}
```
Independenthandoffschema非Creatorreceipt。
Workflowstate：current_step=c54-plan-authoring；next_step=bounded-candidate-commit；
status=COMPLETE（draftonly，非executionapproval/evidencegate/topiccomplete）。
