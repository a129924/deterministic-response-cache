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
- 已存在 source ancestor 的 architecture authority、dataflow JSON、delivery 與 visual-check 是 C11 的 reusable
  committed evidence；C11 不重寫或重新交付它們。C11 以兩個 isolated executable RED assertions 補強現行實作的
  regression coverage；它們在現行 source ancestor 上必須可執行並如實收集結果，不得偽稱 historical red failure、
  expected-nonzero gate 或新的 green-source 前置條件。
- 明確列出 Goal、Non-Goal、In-Scope、Out-Of-Scope、ReadOnly、Written、Deleted、Modify 與 TestCase，
  作為後續 Python implementation 的 bounded contract。
- 兩個已宣告 test modules 必須在同一個 immutable C11 isolated-assertion subject 涵蓋以下五項 regression：
  opaque／unhashable／custom-equality token 的 identity-only key semantics；直接 `importlib.import_module` 跨 BC；
  直接 `__import__` 跨 BC；`importlib` 或 `builtins.__import__` alias／module-alias 跨 BC；以及任一 BC 宣告對方
  semantic type（LRC 的 `ModelIdentity` 或 Identity 的 `RuntimeReuseKey`）。C11 只驗證已存在的實作，且 BC
  regression parser 必須解析 aliases。

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
- C11 的 Tester／Independent Reviewer receipts 必須採新的 SHA-bound、不可覆寫路徑；不得寫入或重用 C5/T3/V3、
  `6110cb…` 或 `44e477…` lineage 的 evidence。
- C11 不建立 RED evidence JSON：現行 source ancestor 已含 contract implementation，故不可誠實地宣稱新的
  expected-nonzero RED failure。isolated assertions 的實際 exit code 改由新的 T11 Tester evidence 收集。
- C8、C9 與 C10 是 frozen、unapproved predecessor planning provenance，沒有 C11 routing authority，也不能重用其
  receipt、implementation 或 evidence。C11 candidate 只能含這五份 planning artifacts，且以既有 Loaded Runtime
  Cache source ancestor 為 parent；不得倒回乾淨 base、刪除既有 source/tests/architecture，或將 frozen C5→V3
  evidence 重用為 C11 routing。

## Completed C12 review-triage provenance

- C11 `55ad5d48c8e638bc5a81f3d0fecfc5a5f35e963c`、R11 receipt commit
  `01da31b11dcc8013f03a773ad9e9042c8bb527bf`、S11
  `e9934dc7bb7b4f81098e635b5f0257c56da659a0`、T11 evidence commit
  `86a5cd54bec9d687d8d7f1738e9376435d3d1abf`，以及 V11 evidence commit
  `73644c2b88257832e1b4d8bedaf516b803c2ee3a` 已完成且全部 frozen。它們只能提供 factual provenance，不能被
  C12 覆寫、重建或作為 C12 receipt／subject。
- C12 的唯一目的，是在固定 PR snapshot `73644c2b88257832e1b4d8bedaf516b803c2ee3a` 建立可審核的 thread-triage
  contract。它只修改五份 planning artifacts，不寫 source、tests、architecture、Archify artifact 或 Tester／Reviewer
  evidence，也不回覆或 resolve thread。
- C12 candidate-only commit、independent R12 SHA-bound Plan-Reviewer receipt、receipt-only commit 與 Planner
  Phase 4.5 alignment 已完成。這些 Git facts 是 frozen provenance；不得由後續 correction 覆寫、重建或當成新的
  candidate／receipt。
- R12 的 `copilot_feedback_triage` 必須非空，並完整覆蓋固定 snapshot 的 current unresolved threads；每個 entry
  都必須有 `thread`、`comment`、`finding`、`commit`、`basis`、`disposition` 六個 factual 欄位。F
  `PRRT_kwDOUJTij86jnBpk`／comment `4043480108` 必須是 `DISCUSS`，並明記 architecture/ACL declared-path
  ownership 是 Human-only `human-check`；其餘 snapshot facts 只能如實列為 `SKIP`，不得以空 triage、推測或
  事後實作取代分類。

## C14 truthful-artifact correction successor

- C13 candidate `a623981989f3363a4b225319a432c3a9d8e28b96`、R13 receipt `cf91b55f80f1764e040c95c822ae55b290e3699c`、RED subject
  `3ba583bed8c367b756e2cb450e468f1274d04193`、其 failing Tester evidence `c4f229f14d3c4c38d40cdda8ad0429712e0ae189`，以及 green subject `ade584e7eb63a7846a23c073c06a802ff99ff6cf` 全為 frozen provenance；`ade584e7…`
  是 `needs-rework`，不得作為任何 C14 routing authority。C14 是唯一 active successor。
- C14 的 purpose 僅修正 C13 的 truthful artifact contract defect：綠色 subject 的 dataflow allowlist 是十個
  已列 path 的唯一允許集合，但 subject 僅納入因本次 JSON／HTML delivery／visual-check 真實重建而 byte-changed 的
  path；不得為湊足集合而人為改寫 byte-identical receipt／HTML。
- C14 candidate 只可修改本 requirements、`technical-spec.md`、topic plan、topic spec 與 step tracker；不得預填
  C14 SHA、receipt path、RED/green subject SHA、Tester evidence、Reviewer evidence 或 outcome。candidate commit 後，
  必須由獨立 Plan-Reviewer 寫新的 SHA-bound `approved` receipt，並由 Implementer 以 sole receipt-only commit
  提交，才可開始 C14 implementation route。
- C14 approved 後，Implementer 先建立 immutable RED subject，且 subject 只修改
  `tests/test_loaded_runtime_cache_bc_independence.py`。RED test 必須 collection-success 且 assertion 實際失敗，
  specifically exercise chained assignment import alias；它不得重播、重寫或宣稱取代 historical `e2e125` evidence。
  Tester 對該 RED subject 如實記錄非零 exit code；failing evidence 只可回到 Implementer 建立新的 green subject。
- 新的 C14 green immutable subject 可修改
  `tests/test_loaded_runtime_cache_bc_independence.py`，以及下列十個既有 dataflow artifacts 中真實變更的 subset：
  `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.json`、`.html`、`.validation.json`、
  `.delivery.json`、`.visual-check.json`、`.visual-check.html`、`.visual-check.1440x900.dark.png`、
  `.visual-check.1440x900.light.png`、`.visual-check.2048x1320.dark.png`、
  `.visual-check.2048x1320.light.png`。它補齊 parser 對 all-simple-name assignment targets 的 chained-assignment
  coverage，並修正 dataflow retain inputs 為 `RuntimeReuseKey + runtime`、`Retained(runtime)`／
  `NotRetained(runtime)` return labels、edge placement，及 1440×900、1600×1000、1920×1080、2048×1320 containment。
  `validation.json` 或 `visual-check.html` 若 rebuild byte-identical，必須維持 ReadOnly。已觀測的真實變更 path 為
  test、dataflow JSON／HTML、delivery JSON、visual-check JSON 與四個既有 PNG captures；此列舉不授權未變更
  path 的人工改寫。
- C14 不得修改五個 Human-owned architecture authority paths：`docs/business-capability-architecture.md`、
  `docs/evolution-roadmap.md`、`docs/architecture/business-capability/architecture-brief.md`、
  `docs/architecture/business-capability/index.html`、`docs/architecture/business-capability/scene.js`。F／ACL
  threads remain open Human-only `human-check`。
- C14 RED Tester evidence 的唯一 path 是
  `plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<red-subject-40-hex-sha>.json`；green Tester
  evidence 使用同一模板但綁定不同的 `<green-subject-40-hex-sha>`；green Reviewer evidence 的唯一 path 是
  `plan/loaded-runtime-cache/loaded-runtime-cache.implementation-review-log-<green-subject-40-hex-sha>.json`。
  Tester 寫 factual evidence、Independent Reviewer 寫 green review record、Implementer 各自以 unchanged sole
  evidence-only commit 提交。RED `failing` record 不得有 Reviewer record。
- 每個 Tester JSON 的 top-level keys 恰為 `schema_version`、`topic`、`implementation_subject_commit`、`status`、
  `commands`、`recorded_by`：integer `1`、topic `loaded-runtime-cache`、full 40-hex lowercase subject SHA、
  `passing|failing`、non-empty command/integer-exit-code list 與 `Tester`。`passing` 僅限全零；`failing` 至少一個
  non-zero。green review JSON 的 top-level keys 恰為 `schema_version`、`topic`、
  `implementation_subject_commit`、`tester_evidence_commit`、`verdict`、`blocking_issues`、`recorded_by`；只可消費
  committed same-topic/same-green-subject passing Tester evidence，且 `approved` 的 blockers 為空、`needs-rework`
  為 non-empty。任一 schema、SHA、path、subject、commit 或 role 不符均 fail closed。
- C5→V3、C11→V11、C12→R12 與
  `9aa656b13fdc36492273c97a62eb9d422a1b64b5` 都是 frozen provenance；最後一者是 unapproved
  `needs-rework` planning provenance，絕非 C14 candidate、receipt 或 implementation routing authority。
