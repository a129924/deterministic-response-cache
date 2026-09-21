# Loaded Runtime Cache — Requirements

## Goal

交付獨立、protocol-first 的 Loaded Runtime Cache BC，使外部 integration／ACL 已提供的本地
`RuntimeReuseKey` 可用於描述「以何種 key 定位可重用 runtime」的契約。本 topic 只定義
runtime lookup／retention 的 Protocol 與 outcome contracts；不建立 runtime、backend、composition 或跨 BC
整合。

## Business outcome

- Registry lookup 可表達 reusable runtime 已存在或缺失；reuse outcome vocabulary 保留
  `Available(runtime)`、`Missing()` 與 `Unavailable()`。
- `registry/runtime_registry_port.py` 擁有 expected lookup operational-failure signal
  `RuntimeRegistryLookupUnavailable`；Registry 在此預期失敗時原樣 raise 該 signal。
  `lookup/lookup_outcome.py` 擁有 `Unavailable()` semantic contract；本 topic 不建立 signal-to-outcome
  consumer、adapter 或 orchestration。
- Runtime retention 可表達 `Retained(runtime)` 或 `NotRetained(runtime)`，且失敗時原 runtime 仍由
  呼叫端持有。
- `RuntimeReuseKey` 是本 BC 的 local semantic type，與 Identity BC 的 `ModelIdentity` 不同；兩個 BC
  不得直接互相 import。
- `RuntimeReuseKey` 只可由本 BC 外的 integration／ACL 建立並交入；本 BC 不公開 token 語意，不接受
  `str`／hash 作為 API，不讀取 token，且其 `repr` 不得暴露 token。
- `RuntimeReuseKey` 的定位以 key instance identity 為準；opaque token 即使是 unhashable 或自訂 equality，也不得
  觸發 token 的 equality 或 hash。此限制保護 opaque boundary，而非為 token 建立比較語意。

## In-Scope

- immutable opaque `RuntimeReuseKey`、generic synchronous `RuntimeRegistry[RuntimeT]` 與
  `RuntimeRetention[RuntimeT]` Protocol，以及 lookup／retention outcomes。
- direct-module contract tests、BC-independence regression、architecture authority 同步，以及 Archify
  `dataflow` design evidence 和其 locked visual evidence paths。
- architecture authority 與 dataflow contract 必須先同步、validate／deliver／visual-check 成功，才可進入
  RED test-only gate。RED subject 必須先作為僅含兩個 tests 的 immutable commit；其後才可執行 locked
  expected-nonzero command、以該已提交 subject 的完整 SHA 寫入獨立 RED evidence，並將 JSON 單獨提交。只有
  RED evidence-only commit 已存在後才可建立新的 immutable green implementation subject。
- 明確列出 Goal、Non-Goal、In-Scope、Out-Of-Scope、ReadOnly、Written、Deleted、Modify 與 TestCase，
  作為後續 Python implementation 的 bounded contract。
- 兩個已宣告 test modules 必須在同一個 immutable RED-test-only subject 先涵蓋並失敗以下五項 regression：
  opaque／unhashable／custom-equality token 的 identity-only key semantics；直接 `importlib.import_module` 跨 BC；
  直接 `__import__` 跨 BC；`importlib` 或 `builtins.__import__` alias／module-alias 跨 BC；以及任一 BC 宣告對方
  semantic type（LRC 的 `ModelIdentity` 或 Identity 的 `RuntimeReuseKey`）。這五項只在 green subject 修正，且
  BC regression parser 必須解析 aliases。

## Out-Of-Scope / Non-Goal

- `ModelIdentity -> RuntimeReuseKey` mapping、mapper、ACL implementation，及所有跨 BC direct import。
- concrete Registry／Retention implementation、DI composition、backend、runtime lifecycle、runtime
  initialization／download／unload／execution 或 provider-specific management。
- Response Reuse、Model Execution、Provider Adapter、TTL、eviction、locking、concurrency、retry、timeout、
  metrics、tracing、root re-export、package facade、dynamic import 與 compatibility layer。

## Acceptance intent

- Runtime Registry port 必須恰以 `RuntimeReuseKey` 接受 lookup／retain；key instance 僅 opaque
  pass-through，不讀取、拆解、序列化、字串化、hash、canonicalize、驗證或重解語意。
- Registry hit／missing 分別以 `RuntimeT`／`None` 回傳；`Missing()`、
  `RuntimeRegistryLookupUnavailable` 與 `Unavailable()` contract 必須可區分。non-expected exception
  原樣 propagate；tests 不得測試 signal-to-`Unavailable()` mapper。
- `ModelIdentity -> RuntimeReuseKey` 轉換只可存在於兩個 BC 外、未實作的 integration／ACL boundary；本 topic
  不描繪成既有實作。
- Architecture Visualization 必須以繁體中文 authored labels 描繪 ACL boundary、lookup／retention outcomes 和
  非責任邊界；它補強設計與 review，不可取代 code contracts 或 tests。
- dataflow 的 retain input 必須明示 `RuntimeReuseKey`；dashed relationship 僅代表明確 async flow，絕不可
  用於 synchronous retain failure。圖仍須標示 protocol-only，不暗示 concrete backend、DI 或 lifecycle。

## Constraints

- 本 topic 的 Git lineage label 是 Human-authorized exception
  `feat/andrew/runtime-reuse-protocol`；它只標示 lineage，不能建立第二 topic、替代 slug、選擇 candidate 或
  作為 routing evidence。
- `package-topology-skeleton-replay` 與本 topic 對 architecture files 的 overlap 只在 Human review／merge
  coordination 處理，不能擴張或改寫本 topic scope。
- 若實作需要未列 artifact path、跨 BC import，或 taxonomy 無法唯一支撐本 plan 的固定路徑，必須停止並返回
  Planner。
- 後續 Tester／Independent Reviewer evidence 必須以同一 immutable implementation subject 的完整 40-hex SHA
  fail-closed 綁定；evidence schema、committing order 與 passing／approved invariants 以 topic plan 的
  `Review and evidence schemas` 為唯一 execution contract。
- 新的 Tester／Independent Reviewer receipts 必須採新的 SHA-bound、不可覆寫路徑；不得寫入或重用舊
  `6110cb…`／`44e477…` lineage 的 fixed-name evidence。
- RED evidence 也必須採新的 SHA-bound、不可覆寫 path，且其 `red_test_subject_commit` 只可指向已提交的
  RED-test-only subject；不得讓同一 commit 同時含 RED tests 與 evidence，亦不得預填或自我引用其 commit SHA。
- C5 candidate 只能含這五份 planning artifacts，並會由後續 Implementer 帶到沒有任何 Loaded Runtime Cache
  artifacts 的乾淨 `origin/dev` base；不得攜帶舊 source、tests、architecture、evidence 或 receipts。candidate
  commit action 完成後，下一 gate 恆為 Independent Plan-Reviewer；planning text 不得預填 SHA 或 receipt。
