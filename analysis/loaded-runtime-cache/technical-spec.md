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
