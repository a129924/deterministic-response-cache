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

## Mandatory execution order

1. 先同步五份 architecture authority，並 author／validate／deliver／visual-check dataflow。任何 architecture 或
   visual gate 非 passing／skipped 都停止，不得建立測試或 production source。
2. architecture gate 通過後，僅新增兩個 RED tests 並先將它們提交為 immutable RED-test-only subject；該 commit
   不得包含 production source 或 RED evidence。subject commit 存在後才執行 locked expected-nonzero command，並以
   subject 的完整 SHA 寫入 versioned RED evidence JSON；其後以 sole evidence-only commit 提交該 JSON，commit 不得
   包含 tests 或 production source。
3. 只有 RED evidence-only commit 已存在後，才建立新的 immutable green implementation subject，納入五個 production
   modules 與使 RED tests 通過的 bounded changes。兩個 RED tests 必須先失敗並涵蓋五項 regression：opaque token 的
   identity-only key semantics（包含 unhashable/custom-equality token）、直接 `importlib.import_module`、直接
   `__import__`、alias/module-alias `importlib` 或 `builtins.__import__`、以及跨 BC duplicate semantic type
   (`ModelIdentity`／`RuntimeReuseKey`)；green subject 才能以五個 production modules 修正它們。Tester 和 Independent
   Reviewer evidence 僅能綁定此新 subject。

## Deterministic validation evidence boundary

RED evidence is a separate factual record, not part of the RED-test-only subject. It has exactly
`schema_version`, `topic`, `red_test_subject_commit`, `status`, `commands`, `recorded_by`; it uses
`schema_version: 1`, topic `loaded-runtime-cache`, a full 40-hex lowercase SHA that resolves to the already committed
RED-test-only subject, status `expected-failing`, a non-empty command / integer-exit-code list with at least one
non-zero exit code, and `recorded_by: Implementer`. Its immutable path is
`loaded-runtime-cache.red-test-evidence-<red-test-subject-40-hex-sha>.json`; Implementer writes it after the factual
locked command and commits it unchanged in a sole evidence-only commit containing neither tests nor production source.
Malformed, extra-key, abbreviated, uncommitted, cross-topic, path/SHA-mismatched, self-referential, or
status/command-inconsistent RED evidence fails closed and cannot authorize green work.

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

The successor records must be written only to immutable versioned paths
`loaded-runtime-cache.tester-evidence-<implementation-subject-40-hex-sha>.json` and
`loaded-runtime-cache.implementation-review-log-<implementation-subject-40-hex-sha>.json`. They must not overwrite,
reuse, or be inferred from the legacy `6110cb…` Tester or `44e477…` Reviewer evidence lineage.

## C5 candidate routing constraint

C5 只包含 `analysis/loaded-runtime-cache/{requirements,technical-spec}.md` 與
`plan/loaded-runtime-cache/loaded-runtime-cache.{plan,spec,step}.md` 五份 planning artifacts。後續 routing 必須將它
帶到沒有任何 Loaded Runtime Cache artifacts 的乾淨 `origin/dev` base；C5 不得攜帶舊 source、tests、architecture、
RED／Tester／Reviewer evidence 或 receipts。candidate commit 已完成後只能由 Independent Plan-Reviewer 建立新的
SHA-bound receipt；本文件不預填 candidate SHA 或 receipt。
