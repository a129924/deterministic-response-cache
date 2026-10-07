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

## C15 mixed-assignment planning successor

Human 已授權 C15 作為新的 planning successor。C15 保留既有 Loaded Runtime Cache mission、scope、Protocol contract、
testing strategy 與 Human boundary；它只取代 current routing，不重寫 C14 provenance。

- `ast.Assign` alias collection 只看 `assignment.targets` 的直接 children：每個直接 `ast.Name` 是 local alias；
  `ast.Attribute` 或任何其他 non-simple target 一律忽略，且不得遞迴解構 target。
- `load = holder.loader = importlib.import_module` 必須保留 `load`，忽略 `holder.loader`。此為 test-side static
  AST contract；不得執行 AST、動態 import、runtime introspection、source workaround 或 cross-BC import。
- C15 candidate 只可修改五份 planning artifacts。獨立 Plan-Reviewer 於 candidate committed 後，才可在
  `loaded-runtime-cache.plan-review-receipt-<planning-candidate-40-hex-sha>.json` 寫 fresh approved receipt；
  Implementer 必須 unchanged sole receipt-only commit。
- C15 RED 與 green subjects 都只能修改 `tests/test_loaded_runtime_cache_bc_independence.py`。RED 必須 collect 成功
  並 actual assertion-fail，Tester 寫 fresh SHA-bound `failing` evidence；其後才可建立 distinct green subject、
  passing Tester evidence、approved independent Reviewer evidence、Planner Phase 4.5 和 fresh classification。
- `37d7233e7231151c0dac6aaa1a7820bff746ffdc` 與完整 C14 chain 是 frozen nonrouting provenance，不得作 C15
  candidate、receipt、subject、evidence、approval 或 next role。F／ACL／business architecture 持續是 Human-only
  `human-check`，C15 不得 reply、resolve、merge 或 release。

## C16 C15 thread-classification receipt successor

Human 已授權 C16 作為只處理 C15 post-Q PR-thread classification 的 planning successor。C16 取代 C15 的 current
routing，但不重寫 C15 chain、Protocol、implementation、tests、architecture 或既有 receipt/evidence。

- C16 candidate 只可修改本 requirements、`technical-spec.md`、topic plan、topic spec 與 step tracker。獨立
  Plan-Reviewer 必須先以標準 candidate-SHA-bound path 寫 fresh `approved` receipt，且 Implementer 必須以 unchanged
  sole receipt-only commit 提交；該 receipt 只授權 C16 classification，不授權新 source/test/docs work。
- C15 immutable facts 固定為 subject `7dab2b9742bd19f962bef99be83b40b978f87f0f`、passing Tester evidence commit
  `475e3c953f6551bef5834d0bf350d5c79449a43e`、approved implementation-review evidence commit
  `cee5097c176b4321a0d9bc2e810caf7d3425d0f1`，以及 classification snapshot
  `7e525b1ad8dc77c25b0b11a467f6b1f24884ecd3`。任一不相符、非祖先、縮寫或未提交 reference 一律 fail closed。
- classification receipt 的唯一 immutable path 是
  `plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-7dab2b9742bd19f962bef99be83b40b978f87f0f.json`。
  Independent Reviewer 是唯一 writer；Implementer 是唯一可將其原樣以 sole evidence-only commit 提交者。receipt
  不可覆寫、不可與 candidate、Plan-Reviewer receipt、source/test/docs 或其他 evidence 共用 commit。
- receipt 僅能列 seven exact current unresolved pairs：
  `PRRT_kwDOUJTij86kQ95O`/`4060023123`、`PRRT_kwDOUJTij86kqiZu`/`4070096548`、
  `PRRT_kwDOUJTij86kqiZ5`/`4070096561`、`PRRT_kwDOUJTij86lAR8J`/`4078761983`、
  `PRRT_kwDOUJTij86lAR8P`/`4078761993`、`PRRT_kwDOUJTij86lAR8T`/`4078761998`、
  `PRRT_kwDOUJTij86lAR8Y`/`4078762005`。ACL `4060023123` 和 business-architecture `4070096561` 固定為
  `HUMAN_CHECK`、`reply: null`，不得回覆或 resolve；其餘五組在 receipt 實際由 Independent Reviewer 寫入前一律不
  預填 outcome 或 reply。
- only `REPLY_AND_RESOLVE` may authorize a subsequent Implementer to leave that exact factual reply and resolve that
  exact thread. `ADDRESS` must return to Planner for a new bounded successor with no reply/resolve. `HUMAN_CHECK`
  remains open with `reply: null`; C16 never approves, merges, releases or post-merges.

## C17 bounded ADDRESS successor

C17 is the sole successor for C16 `ADDRESS` pairs `PRRT_kwDOUJTij86lAR8P`/`4078761993` and
`PRRT_kwDOUJTij86lAR8Y`/`4078762005`. It preserves the protocol-first mission and C15/C16 immutable facts; it does
not rewrite their receipts/evidence or treat chat as routing evidence.

- `4078761993` requires a fresh collection-success/assertion-failing **test-only** RED subject and distinct green
  subject in `tests/test_loaded_runtime_cache_bc_independence.py`. The static scanner must reject local aliases from
  `getattr` of known `importlib`/`sys` module aliases and the literal forbidden surface (`import_module`/`modules`).
  It must not execute AST, call runtime `getattr`, use dynamic import, inspect runtime modules, modify source, or
  cross BC boundaries. Fresh factual RED Tester, green Tester, and green Independent Reviewer evidence are required.
- `4078762005` may change only the topic-owned Loaded Runtime Cache dataflow JSON/HTML and their byte-truthfully
  regenerated validation, delivery and visual-check evidence. It must show
  `RuntimeRegistry.lookup(key: RuntimeReuseKey) -> RuntimeT | None`, not `Available`/`Missing` as lookup outcomes,
  and must not imply a mapper, concrete backend, DI, lifecycle, Model Execution, Provider Adapter, or ACL.
- `PRRT_kwDOUJTij86lAR8T`/`4078761998` is a Human-only README/public-surface `human-check`; `README.md` is ReadOnly
  and C17 neither selects nor changes it. ACL/business-architecture and every non-C17 pair remain open.
- C17 candidate scope is exactly these five planning artifacts. It needs a fresh approved candidate-SHA-bound
  Plan-Reviewer receipt before implementation. No candidate, receipt, subject, evidence, outcome, validation,
  delivery, visual, reply, resolution, merge, release, or post-merge fact is prefilled.

## C18 C17 current-head classification successor

Human 已授權 C18 作為只處理 C17 completed evidence chain 的 current-head PR-thread classification planning
successor。C18 不重寫 C17 chain、不新增 implementation、RED／green、Tester／Reviewer evidence，也不修改 source、
tests、architecture、Archify、README、PR 或 thread state。

- C18 candidate 只可修改本 requirements、`technical-spec.md`、topic plan、topic spec 與 step tracker。candidate
  不得預填自身 SHA、Plan-Reviewer verdict、classification outcome、reply 或 resolution。
- candidate committed 後，獨立 Plan-Reviewer 必須在標準 immutable path
  `plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<planning-candidate-40-hex-sha>.json`
  寫 approved receipt；僅 Implementer 可原樣以 sole receipt-only commit 提交。該 receipt 只授權 C18 classification。
- C18 classification receipt 的唯一 immutable path 是
  `plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-7ceb3409d6d8b9ff3dc51485c3588f502bdff882.json`。
  它固定綁定 subject `7ceb3409d6d8b9ff3dc51485c3588f502bdff882`、passing Tester evidence commit
  `b58cb1e330fe12ccc80a8f39b875a61ea6024067`、approved implementation-review evidence commit
  `edbae51a0ee86cff498d6caf4e6aa78b58962a82` 與 PR head
  `bf63a3c6a0533ad0f367305deff029eddc2b18be`。Independent Reviewer 是唯一 writer；僅 Implementer 可原樣以
  sole evidence-only commit 提交；不得覆寫、合併或與其他檔案共用 commit。
- receipt 必須是唯一 JSON object，top-level keys 恰為 `schema_version`、`topic`、
  `implementation_subject_commit`、`tester_evidence_commit`、`implementation_review_evidence_commit`、
  `pr_head_commit`、`classifications`、`recorded_by`。值分別是 integer `1`、`loaded-runtime-cache`、上述四個
  full 40-hex SHA、exactly eleven-entry array、`Independent Reviewer`。每個 entry 的 keys 恰為
  `thread`、`comment`、`outcome`、`reply`；`outcome` 只可為 `REPLY_AND_RESOLVE`、`ADDRESS`、`HUMAN_CHECK`，
  且只有前者有 non-empty reply，其他兩者必為 JSON `null`。
- exact pair set 是 F `PRRT_kwDOUJTij86jnBpk`/`4043480108`、
  `PRRT_kwDOUJTij86jqdPV`/`4044836129`、`PRRT_kwDOUJTij86jqdPZ`/`4044836136`、
  `PRRT_kwDOUJTij86kOjjo`/`4059094458`、ACL `PRRT_kwDOUJTij86kQ95O`/`4060023123`、
  `PRRT_kwDOUJTij86kqiZu`/`4070096548`、business `PRRT_kwDOUJTij86kqiZ5`/`4070096561`、
  `PRRT_kwDOUJTij86lAR8J`/`4078761983`、`PRRT_kwDOUJTij86lAR8P`/`4078761993`、README
  `PRRT_kwDOUJTij86lAR8T`/`4078761998`、`PRRT_kwDOUJTij86lAR8Y`/`4078762005`，不得缺漏、重複或加入其他 pair。
  F／ACL／business／README 四組固定為 `HUMAN_CHECK` 且 `reply: null`，永遠保持 open。其餘七組直到 Independent
  Reviewer 實際寫入 receipt 前不得預填 outcome 或 reply。
- 僅 committed C18 receipt 中 exact `REPLY_AND_RESOLVE` pair 可授權 Implementer 留下該 entry 的 exact factual reply
  並 resolve 該 exact thread。`ADDRESS` 必回到 Planner 建立新 successor；`HUMAN_CHECK` 不得 reply／resolve。錯誤
  writer、path、schema、SHA、ancestor、sole-commit、pair set 或 nullability 一律 fail closed。

## C19 C17 current-head reconciliation classification successor

Human 已授權 C19 作為 C18 後唯一的 current-head classification planning successor。它只處理四個 C18 之後
未分類的 thread/comment pairs，以及 `lAR8Y` 的 current-state reconciliation；它不重寫 C17/C18 chain、既有
receipt/evidence、source、tests、docs、Archify、README、PR 或 thread state。

- C19 candidate 只可修改本 requirements、`technical-spec.md`、topic plan、topic spec 與 step tracker。candidate
  不得預填自身 SHA、Plan-Reviewer verdict、任一 classification outcome、reply 或 resolution。
- candidate committed 後，獨立 Plan-Reviewer 必須在標準 immutable path
  `plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<planning-candidate-40-hex-sha>.json`
  寫 approved receipt；僅 Implementer 可原樣以 sole receipt-only commit 提交。該 receipt 只授權 C19 classification。
- C19 classification receipt 的唯一 immutable path 是
  `plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-7ceb3409d6d8b9ff3dc51485c3588f502bdff882-3e803a507b2dfa74efdf71164c260da172aadb81.json`。
  它固定綁定 C17 subject `7ceb3409d6d8b9ff3dc51485c3588f502bdff882`、passing Tester evidence commit
  `b58cb1e330fe12ccc80a8f39b875a61ea6024067`、approved implementation-review evidence commit
  `edbae51a0ee86cff498d6caf4e6aa78b58962a82` 與 current PR head
  `3e803a507b2dfa74efdf71164c260da172aadb81`。Independent Reviewer 是唯一 writer；僅 Implementer 可原樣以
  sole evidence-only commit 提交；不得覆寫或與任何其他檔案共用 commit。
- receipt 必須是唯一 JSON object，top-level keys 恰為 `schema_version`、`topic`、
  `implementation_subject_commit`、`tester_evidence_commit`、`implementation_review_evidence_commit`、
  `pr_head_commit`、`classifications`、`recorded_by`。其固定值為 integer `1`、`loaded-runtime-cache`、上述
  four full 40-hex SHA、exactly five-entry array、`Independent Reviewer`。每個 entry 的 keys 恰為
  `thread`、`comment`、`outcome`、`reply`。
- exact pair set 僅為 `PRRT_kwDOUJTij86lCkFr`/`4079664571`、`PRRT_kwDOUJTij86lCkFu`/`4079664575`、
  `PRRT_kwDOUJTij86lDH2-`/`4079885261`、`PRRT_kwDOUJTij86lDH3C`/`4079885267` 與
  `PRRT_kwDOUJTij86lAR8Y`/`4078762005`。前四組 outcome/reply 一律由 Independent Reviewer 在 future receipt
  獨立決定，不得由 candidate 預填。`lAR8Y` 必須先核對 GitHub current state：只有 Reviewer 在 receipt 寫入時可
  驗證其已 resolved，才可記為 `ALREADY_RESOLVED`／`reply: null`；否則亦由 Reviewer 獨立選擇一般 outcome。
  `REPLY_AND_RESOLVE` 需 non-empty factual reply；`ADDRESS`、`HUMAN_CHECK` 與 `ALREADY_RESOLVED` 均需 JSON
  `null` reply。`ALREADY_RESOLVED` 只可用於 `lAR8Y`，且不授權任何 thread action。
- F `PRRT_kwDOUJTij86jnBpk`/`4043480108`、ACL `PRRT_kwDOUJTij86kQ95O`/`4060023123`、business
  `PRRT_kwDOUJTij86kqiZ5`/`4070096561`、README `PRRT_kwDOUJTij86lAR8T`/`4078761998` 是既有 Human-only locks，
  不在 C19 pair set 中，保持 open、不得 reply 或 resolve。僅 committed C19 receipt 的 exact
  `REPLY_AND_RESOLVE` entry 可授權 Implementer 留下該 exact factual reply 並 resolve 該 exact thread；
  `ADDRESS` 返回 Planner，`HUMAN_CHECK` 保持 open。任何錯誤 writer、path、schema、SHA、ancestor、sole-commit、
  pair set、enum 或 nullability 一律 fail closed。

## C20 C19 ADDRESS remediation successor

Human 已授權 C20，且它是 C19 兩個 `ADDRESS` pair 的唯一 remediation successor：
`PRRT_kwDOUJTij86lCkFu`/`4079664575` 與 `PRRT_kwDOUJTij86lDH2-`/`4079885261`。它不重寫 C17–C19 的
candidate、receipt、subject 或 classification，也不將任一舊 receipt 當成 C20 routing authority。

- `lCkFu` 僅要求 topic-owned dataflow 明確表達 `RuntimeRegistryLookupUnavailable` 是 Registry expected
  lookup failure signal；它必須與 `RuntimeRegistry.lookup(key: RuntimeReuseKey) -> RuntimeT | None` 的正常
  union return 分開呈現，且不得描繪、實作或暗示 signal-to-`Unavailable`、`Missing` 或其他 outcome 的 mapper。
- `lDH2-` 僅要求 BC-independence scanner 對
  `from deterministic_response_cache.identity.contracts import ModelIdentity as <local-name>` 這種 foreign
  semantic-type `ImportFrom` local alias 做純 AST 靜態拒絕。它不得執行來源、dynamic import、讀取 runtime module，
  或將此規則擴張到非 `ModelIdentity`／非 Identity BC 的一般 import。
- C20 candidate 只可修改本 requirements、`technical-spec.md`、topic plan、topic spec 與 step tracker；不得
  預填 candidate SHA、Plan-Reviewer verdict、RED/green subject、Tester/Reviewer 結果、classification outcome、
  reply 或 resolution。它必須先有新的 candidate-SHA-bound approved Plan-Reviewer receipt。
- RED subject 只可修改 `tests/test_loaded_runtime_cache_bc_independence.py`，必須 collect 成功並以兩個新 contract
  assertions 實際失敗：foreign `ImportFrom` semantic alias 被拒絕，及 dataflow 有獨立 expected failure signal。
  Tester 寫同 subject、factual `failing` evidence；其後才可建立 distinct green subject。
- green subject 只可修改同一 test 與 C20 technical specification 列出的 exact ten dataflow outputs；僅有
  byte-truthfully changed outputs 才可納入。
  必須先 validate（showcase 9/9、0 errors、0 warnings），再 deliver，最後 non-skipped visual-check（1440×900、
  1600×1000、1920×1080、2048×1320）；任一 non-zero、warning/error、skipped 或 hand-edited evidence 都 fail closed。
- green passing Tester evidence、approved independent Reviewer evidence 與 Planner Phase 4.5 後，才可建立 C20
  current-head classification receipt。該 receipt 只含上述兩個 exact pairs；Independent Reviewer 決定
  `REPLY_AND_RESOLVE`、`ADDRESS` 或 `HUMAN_CHECK`，candidate 不得預填 outcome/reply。只有 committed exact
  `REPLY_AND_RESOLVE` 才可讓 Implementer 對該 pair 留 factual reply 並 resolve。
- 所有未列路徑、所有既有 candidate/receipt/evidence、source/public API、README、architecture index、其他 dataflow
  artifacts、所有其他 PR threads 與全部既有 Human-only locks 都是 ReadOnly。C20 不授權 merge、release、post-merge 或
  Human review。

## C21 current-head single-pair classification successor

Human 已授權 C21 作為 C20 之後唯一的 current-head classification successor。它只處理
`PRRT_kwDOUJTij86ldYVf`/`4090457782`，並固定消費 C20 immutable subject
`fa1468301af1906a05ee31ba0d267d2270d7af5f`、passing Tester evidence commit
`6423f55b6dbcde5bee190ef86dc8c31f5c27c94e`、approved independent Reviewer evidence commit
`3d0dc9fbb0e9da6d742ac20856b8aac6b0a3035e` 及 current PR head
`a1aae44897c0f0b0ac52f1ca1697554c2f79cdb5`。它不重寫 C20 或任何 predecessor evidence、source、tests、docs、
Archify、README、PR 或 thread state。

- C21 candidate 只可修改本 requirements、`technical-spec.md`、topic plan、topic spec 與 step tracker；不得預填自身
  SHA、Plan-Reviewer verdict、classification outcome、reply 或 resolution。candidate committed 後，獨立
  Plan-Reviewer 必須先在標準 immutable path
  `plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<planning-candidate-40-hex-sha>.json` 寫 approved
  receipt，且僅 Implementer 可原樣以 sole receipt-only commit 提交。
- C21 classification receipt 的唯一 immutable path 是
  `plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-fa1468301af1906a05ee31ba0d267d2270d7af5f-a1aae44897c0f0b0ac52f1ca1697554c2f79cdb5.json`。
  Independent Reviewer 是唯一 writer；僅 Implementer 可原樣以 sole evidence-only commit 提交；不得覆寫、重用
  C20 receipt 或與其他檔案共用 commit。
- receipt 必須是唯一 JSON object，top-level keys 恰為 `schema_version`、`topic`、
  `implementation_subject_commit`、`tester_evidence_commit`、`implementation_review_evidence_commit`、
  `pr_head_commit`、`classifications`、`recorded_by`。固定值為 integer `1`、`loaded-runtime-cache`、上述四個完整
  40-hex SHA、exactly one-entry array、`Independent Reviewer`。唯一 entry 的 keys 恰為 `thread`、`comment`、
  `outcome`、`reply`，且固定為 `PRRT_kwDOUJTij86ldYVf`/`4090457782`。
- Independent Reviewer 在 future receipt 獨立決定 `REPLY_AND_RESOLVE`、`ADDRESS` 或 `HUMAN_CHECK`，candidate 不得
  預填 outcome 或 reply。僅 `REPLY_AND_RESOLVE` 可有 non-empty factual reply，並授權 Implementer 對該 exact pair
  留下該 reply 並 resolve；`ADDRESS` 和 `HUMAN_CHECK` 必為 JSON `null`，前者返回 Planner、後者保持 open。所有其他
  threads、既有 Human-only locks 與未列路徑維持 ReadOnly。任何錯誤 writer、path、schema、SHA、ancestor、sole-commit、
  pair set、enum 或 nullability 一律 fail closed。

## C22 current-head dual-pair classification successor

Human 已授權 C22 作為 C21 後唯一的 current-head classification successor。它只處理
`PRRT_kwDOUJTij86ldeVI`/`4090495760` 與 `PRRT_kwDOUJTij86ldeVO`/`4090495770`，並固定消費 C20 immutable subject
`fa1468301af1906a05ee31ba0d267d2270d7af5f`、passing Tester evidence commit
`6423f55b6dbcde5bee190ef86dc8c31f5c27c94e`、approved independent Reviewer evidence commit
`3d0dc9fbb0e9da6d742ac20856b8aac6b0a3035e` 及 current PR head
`0991c56ec7e562ea512449bda1a41118dbc48203`。它不重寫 C20/C21 或任何 predecessor evidence、source、tests、docs、
Archify、README、PR 或 thread state。

- C22 candidate 只可修改本 requirements、`technical-spec.md`、topic plan、topic spec 與 step tracker；不得預填自身
  SHA、Plan-Reviewer verdict、classification outcome、reply 或 resolution。candidate committed 後，獨立
  Plan-Reviewer 必須先在標準 immutable path
  `plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<planning-candidate-40-hex-sha>.json` 寫 approved
  receipt，且僅 Implementer 可原樣以 sole receipt-only commit 提交。
- C22 classification receipt 的唯一 immutable path 是
  `plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-fa1468301af1906a05ee31ba0d267d2270d7af5f-0991c56ec7e562ea512449bda1a41118dbc48203.json`。
  Independent Reviewer 是唯一 writer；僅 Implementer 可原樣以 sole evidence-only commit 提交；不得覆寫、重用
  C20/C21 receipt 或與其他檔案共用 commit。
- receipt 必須是唯一 JSON object，top-level keys 恰為 `schema_version`、`topic`、
  `implementation_subject_commit`、`tester_evidence_commit`、`implementation_review_evidence_commit`、
  `pr_head_commit`、`classifications`、`recorded_by`。固定值為 integer `1`、`loaded-runtime-cache`、上述四個完整
  40-hex SHA、exactly two-entry array、`Independent Reviewer`。每個 entry 的 keys 恰為 `thread`、`comment`、
  `outcome`、`reply`，且 exact pair set 僅為 `PRRT_kwDOUJTij86ldeVI`/`4090495760` 與
  `PRRT_kwDOUJTij86ldeVO`/`4090495770`。
- Independent Reviewer 在 future receipt 獨立決定 `REPLY_AND_RESOLVE`、`ADDRESS` 或 `HUMAN_CHECK`，candidate 不得
  預填 outcome 或 reply。僅 `REPLY_AND_RESOLVE` 可有 non-empty factual reply，並授權 Implementer 對該 exact pair
  留下該 reply 並 resolve；`ADDRESS` 和 `HUMAN_CHECK` 必為 JSON `null`，前者返回 Planner、後者保持 open。
  F `PRRT_kwDOUJTij86jnBpk`/`4043480108`、ACL `PRRT_kwDOUJTij86kQ95O`/`4060023123`、business
  `PRRT_kwDOUJTij86kqiZ5`/`4070096561` 與 README `PRRT_kwDOUJTij86lAR8T`/`4078761998` 是 Human-only locks；它們不在
  C22 pair set 中，保持 open、不得 reply 或 resolve。新 `PRRT_kwDOUJTij86ld9Ai` 亦明確排除於 C22 receipt，保持
  open、未分類且不得 action。所有其他 threads 與未列路徑維持 ReadOnly。任何錯誤 writer、path、schema、SHA、ancestor、
  sole-commit、pair set、enum 或 nullability 一律 fail closed。

## C23 bounded ADDRESS remediation successor

C23 是 C22 對 `PRRT_kwDOUJTij86ldeVI`/`4090495760` 與
`PRRT_kwDOUJTij86ldeVO`/`4090495770` 的 ADDRESS 結果之唯一 bounded remediation successor。它保留既有 mission、
protocol-first boundary，且只能消費 committed C22 classification receipt
`a9065a8332119930347214f07f2980d655d8d314` 的
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-fa1468301af1906a05ee31ba0d267d2270d7af5f-0991c56ec7e562ea512449bda1a41118dbc48203.json`。
該 receipt 固定綁定 C20 subject `fa1468301af1906a05ee31ba0d267d2270d7af5f`、passing Tester evidence
`6423f55b6dbcde5bee190ef86dc8c31f5c27c94e`、approved Reviewer evidence
`3d0dc9fbb0e9da6d742ac20856b8aac6b0a3035e` 與 C22 PR head
`0991c56ec7e562ea512449bda1a41118dbc48203`；不改寫任何 predecessor candidate、receipt 或 evidence，亦不將 chat、branch
或工作樹狀態視為 routing authority。

- Dataflow 修正只可使圖忠實保留
  `RuntimeRegistry.lookup(key: RuntimeReuseKey) -> RuntimeT | None`，以及唯一的 expected-failure edge
  `RuntimeRegistry → RuntimeRegistryLookupUnavailable`。不得把 Registry lookup 連到
  `Available`、`Missing`、`Unavailable` 或 mapper，也不得暗示 concrete backend、DI、runtime lifecycle、Model
  Execution、Provider Adapter 或 ACL implementation。
- BC-independence AST scanner 修正只可偵測
  `(load := importlib.import_module)(...)` 的 walrus alias bypass。scanner 僅解析 `ast.NamedExpr` 的直接 simple-name
  `target` 與其 `value`；它不得遞迴拆解、執行 fixture、執行 dynamic import 或 import runtime module。既有 mixed-assignment
  規則維持：`load = holder.loader = importlib.import_module` 保留 simple-name `load`、忽略 attribute target
  `holder.loader`。
- C23 candidate 只可修改本 requirements、`technical-spec.md`、topic plan、topic spec 與 step tracker，且不得預填
  candidate SHA、Plan-Reviewer verdict、RED/green subject SHA、Tester/Reviewer outcome、current head、classification
  outcome、reply 或 resolution。candidate committed 後，Independent Plan-Reviewer 必須在標準
  `loaded-runtime-cache.plan-review-receipt-<candidate-40-hex-sha>.json` 寫 fresh approved receipt；僅 Implementer 可
  原樣以 sole receipt-only commit 提交。
- approved receipt 後，Implementer 必須先建立 collection-success/assertion-failing RED subject，再由 Tester 寫同 subject
  SHA-bound factual `failing` evidence，並由 Implementer 原樣 sole evidence-only commit。只有該 committed failing evidence
  可路由 distinct green subject。green subject 只可修改 BC scanner test 與 dataflow JSON/HTML 及其真實變更的既有
  validation/delivery/visual-check evidence；Tester 必須寫 same-green-subject `passing` evidence，Implementer 單獨提交；
  Independent Reviewer 只可消費該 committed passing evidence 並寫 approved/needs-rework review record，再由 Implementer
  單獨提交。任何 evidence 的 schema、writer、path、SHA、subject、sole-commit 或 status 不符皆 fail closed。
- 僅在 Planner 確認 C23 approved green chain 與 actual current PR head 後，Independent Reviewer 可在唯一 immutable path
  `plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-<c23-green-subject-40-hex-sha>-<current-pr-head-40-hex-sha>.json`
  寫 future classification receipt；只有 Implementer 可原樣以 sole evidence-only commit 提交。其 JSON object top-level keys
  恰為 `schema_version`、`topic`、`implementation_subject_commit`、`tester_evidence_commit`、
  `implementation_review_evidence_commit`、`pr_head_commit`、`classifications`、`recorded_by`：值分別綁定 integer `1`、
  `loaded-runtime-cache`、C23 green subject、該 green subject 的 passing Tester/review evidence commits、actual current PR
  head、exactly two classifications 與 `Independent Reviewer`。每個 classification entry 的 keys 恰為 `thread`、`comment`、
  `outcome`、`reply`，且 pair set 僅為 `ldeVI`/`4090495760` 與 `ldeVO`/`4090495770`；outcome 僅可為
  `REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK`。只有 `REPLY_AND_RESOLVE` 可有 non-empty factual reply 並授權 Implementer 對該
  exact thread reply/resolve；`ADDRESS` 與 `HUMAN_CHECK` 必為 JSON `null`，分別回到 Planner／保持 open。
- F `PRRT_kwDOUJTij86jnBpk`/`4043480108`、ACL `PRRT_kwDOUJTij86kQ95O`/`4060023123`、business
  `PRRT_kwDOUJTij86kqiZ5`/`4070096561`、README `PRRT_kwDOUJTij86lAR8T`/`4078761998` 與
  `PRRT_kwDOUJTij86ld9Ai`/`4090688118` 是 C23 ReadOnly/open/unclassified boundary；前四者是 Human-only locks。

## C24 current-head dual-pair classification successor

C24 是 C23 classification provenance `e5872d5dfb2018743b1f7e319551d52f25f5ef02` 後唯一的 planning-only successor，
只分類 NamedExpr module-alias scanner gap `PRRT_kwDOUJTij86lfQl9`/`4091213935` 與 topology stale executable-module
statement `PRRT_kwDOUJTij86lfQmF`/`4091213944`。它固定消費 C23 subject
`240c694fa5078dc1d35f154f7a85b06381db2e47`、passing Tester `dabce082058805281990c52b12352b87c2b46801`、approved Reviewer
`489752c727aa86cfaf49038cc2ed6dfddf33ba2d`、current PR head `e5872d5dfb2018743b1f7e319551d52f25f5ef02`，以及 C23 receipt
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-240c694fa5078dc1d35f154f7a85b06381db2e47-489752c727aa86cfaf49038cc2ed6dfddf33ba2d.json`。

- Candidate 僅修改五份 planning artifacts，不得預填 candidate SHA、Plan-Reviewer verdict、classification outcome、reply
  或 resolution。獨立 Plan-Reviewer 在 `loaded-runtime-cache.plan-review-receipt-<candidate-40-hex-sha>.json` 寫 approved
  receipt；僅 Implementer 可原樣 sole receipt-only commit。
- 獨立 Reviewer 之後唯一可寫
  `plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-240c694fa5078dc1d35f154f7a85b06381db2e47-e5872d5dfb2018743b1f7e319551d52f25f5ef02.json`；僅 Implementer 可原樣 sole evidence-only commit。JSON top-level keys
  恰為 `schema_version`、`topic`、`implementation_subject_commit`、`tester_evidence_commit`、
  `implementation_review_evidence_commit`、`pr_head_commit`、`classifications`、`recorded_by`，固定綁定 integer `1`、
  `loaded-runtime-cache`、上述 subject/evidence/head facts、exactly two entries 與 `Independent Reviewer`。entry keys 恰為
  `thread`、`comment`、`outcome`、`reply`，pair set 僅為 `lfQl9`/`4091213935` 與 `lfQmF`/`4091213944`。
- Reviewer 獨立決定 `REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK`；僅 committed `REPLY_AND_RESOLVE` 有 non-empty factual reply
  並只授權該 exact pair 的 reply/resolve。`ADDRESS` 與 `HUMAN_CHECK` 必為 JSON `null`，分別回到 Planner／保持 open；任一
  writer/path/SHA/schema/pair/enum/nullability/sole-commit defect 都 fail closed。
- C23 resolved `ldeVI`/`4090495760`、`ldeVO`/`4090495770` frozen；F/ACL/business/README 四個 Human-only pairs 與
  `ld9Ai`/`4090688118` 維持 ReadOnly/open exclusions。未列 path/thread、source、tests、dataflow、architecture、README、
  PR、merge、release、post-merge 都不在 scope。

## C25 lfQl9 bounded static-attribute remediation successor

C25 僅處理 C24 對 `PRRT_kwDOUJTij86lfQl9`/`4091213935` 的靜態 scanner 缺口：
`(loader := importlib).import_module(...)`。它不處理 C24 的另一 pair `lfQmF`/`4091213944`，也不重新分類、回覆或
resolve 任何 thread。scanner 的唯一新辨識是：direct `ast.Attribute` 的 base 為 `ast.NamedExpr`，其 target 是直接
simple-name，value 解析為既有已知 `importlib` module alias，且 attribute 為 `import_module`。此為靜態語法判定，
不得遞迴處理 target 或 expression、執行 fixture／AST、dynamic import 或 runtime introspection。

- C25 candidate 只可修改本 requirements、`technical-spec.md`、topic plan、topic spec 與 step tracker；不得預填
  candidate SHA、Plan-Reviewer verdict、RED/green SHA、Tester/Reviewer outcome、PR head、classification outcome、reply
  或 resolution。獨立 Plan-Reviewer 必須先寫標準 SHA-bound approved receipt，且僅 Implementer 可原樣 sole
  receipt-only commit。
- approved receipt 後，RED 與 distinct green implementation subject 都只可修改
  `tests/test_loaded_runtime_cache_bc_independence.py`。RED 必須 collection-success 並以此 attribute-base NamedExpr
  alias 的 assertion 實際失敗；Tester 如實寫 SHA-bound `failing` evidence，由 Implementer 原樣 sole commit。green
  僅修正此 static detection，Tester 寫 same-green-subject `passing` evidence，Independent Reviewer 僅可消費該已提交
  passing evidence，所有 evidence 皆由 Implementer unchanged sole commit。
- 既有 direct-name NamedExpr、mixed assignment（保留 simple-name target、忽略 attribute target）、`getattr`、
  `sys.modules` 規則都不得改變。production source、docs、dataflow、所有 predecessor candidate／receipt／evidence、
  `lfQmF`/`4091213944`、F/ACL/business/README Human-only locks、`ld9Ai` 與所有未列 path/thread 均 ReadOnly/open。
- 僅在 Planner 驗證 approved C25 green chain 與 actual current PR head 後，Independent Reviewer 可在
  `plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-<c25-green-subject-40-hex-sha>-<actual-current-pr-head-40-hex-sha>.json`
  寫一份只含 `lfQl9`/`4091213935` 的 immutable receipt；Implementer 只能原樣 sole evidence-only commit。classification
  outcome/reply 由 Reviewer 獨立決定且 candidate 不得預填；只有 committed `REPLY_AND_RESOLVE` 的 non-empty factual
  reply 才可在後續授權 exact reply/resolve，否則 `ADDRESS` 回到 Planner、`HUMAN_CHECK` 保持 open。

## C26 current-head seven-pair classification successor

C26 是 C25 classification receipt commit `8bd9460950237c48c9befb73a1c5b80d084e88ae` 後唯一的 planning-only
successor。它只建立 current-head independent classification contract，pair set 恰為
`PRRT_kwDOUJTij86ld9Ai`/`4090688118`、`PRRT_kwDOUJTij86lfYsF`/`4091265104`、
`PRRT_kwDOUJTij86lfYsH`/`4091265108`、`PRRT_kwDOUJTij86lfYsK`/`4091265115`、
`PRRT_kwDOUJTij86m8u00`/`4129370918`、`PRRT_kwDOUJTij86m8u04`/`4129370926`、及
`PRRT_kwDOUJTij86m8u09`/`4129370931`。它固定消費 C25 green subject
`13f987a41119590621671c429293cf549055672b`、passing Tester evidence commit
`e85f936505a323e6c84c02e90f4c4114e39b6505`、approved Reviewer evidence commit
`24d5141332cbc4dcf7a87dea7f134207a16ab37e` 與 current-head base
`8bd9460950237c48c9befb73a1c5b80d084e88ae`。

- Candidate 只修改五份 planning artifacts，且不得預填 candidate SHA、Plan-Reviewer verdict、classification
  outcome、reply 或 resolution。獨立 Plan-Reviewer 必須先於
  `loaded-runtime-cache.plan-review-receipt-<planning-candidate-40-hex-sha>.json` 寫標準 approved receipt；僅
  Implementer 可原樣以 sole receipt-only commit 提交。
- approved receipt 後，僅 Independent Reviewer 可寫入 immutable current-head receipt
  `plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-13f987a41119590621671c429293cf549055672b-8bd9460950237c48c9befb73a1c5b80d084e88ae.json`；
  僅 Implementer 可原樣以 sole evidence-only commit 提交。其 top-level keys 恰為 `schema_version`、`topic`、
  `implementation_subject_commit`、`tester_evidence_commit`、`implementation_review_evidence_commit`、
  `pr_head_commit`、`classifications`、`recorded_by`，固定綁定 schema `1`、本 topic、上述 C25 facts、exactly seven
  entries 與 `Independent Reviewer`。每個 entry keys 恰為 `thread`、`comment`、`outcome`、`reply`；Reviewer 獨立選擇
  `REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK`。僅 committed `REPLY_AND_RESOLVE` 可有 non-empty factual reply 並在後續
  授權該 exact pair 的 reply/resolve；其餘兩者必為 JSON `null`，分別回到 Planner/open。
- `jnBpk`/`4043480108`、`kQ95O`/`4060023123`、`kqiZ5`/`4070096561`、`lAR8T`/`4078761998` 與
  `lfQmF`/`4091213944` 維持 Human-only open exclusions。C25 `lfQl9`/`4091213935` 與所有其他未列 threads、source、
  tests、docs、dataflow、architecture、README、PR authority、merge、release、post-merge 皆 ReadOnly。任一錯誤 writer、
  path、schema、binding、pair set、enum、nullability、staleness 或 non-sole commit 一律 fail closed。

## C27 bounded architecture-document conflict-resolution successor

C27 是 C26 committed classification receipt `31ab754aae443f702fa4ccc028d53a6c687e48aa` 後唯一授權的 planning successor。它只處理 PR 顯示的五個
architecture-document merge conflicts，並只整合已提交的事實：merge base
`37d433e198a955f0710ecd5335666760aa86a20c`、Loaded Runtime Cache fact
`442cc9461854d3909345edb26d1434bfaaa1b86e`、Model Execution fact
`5f483a05e63c9dc8f3c63b04a63c8adec3ed2e28`，以及 dev head
`1501f380f20492c71275474f800fdaaffbf0a76a`。這不是新的 architecture decision。

- Candidate 只修改五份 planning artifacts，且不得預填 candidate SHA、Plan-Reviewer verdict、integration subject
  SHA、test result 或 review verdict。獨立 Plan-Reviewer 必須先寫 standard SHA-bound approved receipt；只有
  Implementer 可原樣以 sole receipt-only commit 提交。
- approved receipt 後的唯一 integration subject 只可手動解決以下五個檔案的 textual conflicts：
  `docs/architecture/business-capability/architecture-brief.md`、
  `docs/architecture/business-capability/index.html`、
  `docs/architecture/business-capability/scene.js`、`docs/business-capability-architecture.md`、
  `docs/evolution-roadmap.md`。不得修改其他檔案、刪除任一已提交事實，或藉由解衝新增架構決策。
- 整合內容必須同時保留 Runtime Cache 的 protocol-only、無 Identity BC direct import、無 mapper、backend 或 runtime
  lifecycle，與 Model Execution 的 provider-neutral coordination contracts；兩者的 wiring 均為未來工作，不能描述為已
  實作。五檔 integration subject 提交後，Tester 唯一可在
  `plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<c27-integration-subject-40-hex-sha>.json`
  寫入該 subject 的 factual verification；只有 Implementer 可原樣以 sole evidence-only commit 提交。Independent
  Reviewer 只能消費該 committed、same-subject 的 passing evidence，並唯一可在
  `plan/loaded-runtime-cache/loaded-runtime-cache.implementation-review-log-<c27-integration-subject-40-hex-sha>.json`
  寫入 review；只有 Implementer 可再原樣以獨立 sole evidence-only commit 提交。完成 approved review 與 Planner
  Phase 4.5 後，Implementer 才可 push 更新既有 draft PR。
- C26 的 classified pairs、所有 Human-only locks、所有未列 PR threads、source/tests、Runtime Registry contract 與
  非本五檔文件均 ReadOnly。C27 本身不回覆、resolve、approve、merge、release 或 post-merge。

## C28 post-C27 eight-pair repair and classification successor

C28 以已提交的 C25、C26 與 C27 facts 為唯一歷史輸入：C25 green subject
`13f987a41119590621671c429293cf549055672b`、C26 classification receipt
`31ab754aae443f702fa4ccc028d53a6c687e48aa`，以及 C27 repaired candidate
`2dac62be230fe3daf6c259389c93a6e29cfa7006`、integration subject
`21747f2a24dedc2d18eaf2fbd6c8bc0bb0670585`、passing Tester evidence
`294f7fb5ea0502236c277e545ba9e2dc311596e3`、approved Reviewer evidence
`190c41bb3480753f78bdf97c778583bee0f6ff2f`。它只處理 C26 已獨立分類為 `ADDRESS` 的
`lfYsH`/`4091265108`、`lfYsK`/`4091265115`、`m8u04`/`4129370926`、`m8u09`/`4129370931`，以及尚未分類的
`m82WL`/`4129419161`、`m82WS`/`4129419173`、`m9eUV`/`4129677944`、`m9eUY`/`4129677947`。C28 candidate 不得預填
任何 C28 candidate SHA、review verdict、RED/green SHA、Tester/Reviewer result、PR head、classification outcome、reply 或 resolution。

- Candidate 只修改五份 planning artifacts，並以 committed facts 對齊 C25/C26/C27 的 historical tracker state；它不得
  回寫 receipt、evidence 或宣稱任何 C28 thread 已處理。先由 Independent Plan-Reviewer 在
  `loaded-runtime-cache.plan-review-receipt-<c28-candidate-40-hex-sha>.json` 寫標準 approved receipt，再由
  Implementer 原樣以 sole receipt-only commit 提交。
- approved receipt 後，RED subject 只可修改 `tests/test_loaded_runtime_cache_bc_independence.py` 與
  `tests/test_loaded_runtime_cache_contracts.py`：它必須 collection-success 並實際暴露四個 static scanner gaps
  （direct `getattr(importlib, "import_module")` callable、direct `getattr(sys, "modules")` base、`import importlib.util`
  的 top-level module binding、以及 `IfExp` assignment 任一分支的 forbidden callable），並暴露 `RuntimeReuseKey`
  construction token 不得成為可讀 instance attribute。Tester 只如實寫 full-SHA-bound `failing` evidence；沒有 RED Reviewer record。
- green subject 只可修改上述兩個 tests、
  `src/deterministic_response_cache/loaded_runtime_cache/runtime_reuse/registry/runtime_reuse_key.py`，以及下列 dataflow
  artifact allowlist 中真實 byte-changed subset：`loaded-runtime-cache.dataflow.json`、`.html`、`.validation.json`、
  `.delivery.json`、`.visual-check.json`、`.visual-check.html` 與四個既有 desktop capture PNG。修正須保持純 AST、
  不遞迴執行 source、不 dynamic import／runtime introspection；保留 direct-name NamedExpr、mixed assignment
  simple-name-only rule、既有 `getattr`/`sys.modules` alias behavior，僅擴充直接 expression 與 top-level importlib
  submodule shape。`RuntimeReuseKey` 仍為 instance-identity、immutable、token-uninterpreted local type，但不得留下可讀 token
  attribute。dataflow 必須明示 `RuntimeRegistry.retain(key, runtime) -> None` 的 key/runtime inputs 與 completion，且與
  `RuntimeRetention` outcomes 分離；不得暗示 backend、mapper、lifecycle 或 BC wiring。
- green passing Tester evidence 與 approved Independent Reviewer evidence 都必須綁定新的 green subject full SHA，並各由
  Implementer unchanged sole evidence-only commit。其後 Planner 驗證 actual current PR head，只有 Independent Reviewer 可寫
  `loaded-runtime-cache.thread-classification-receipt-<c28-green-subject-40-hex-sha>-<actual-current-pr-head-40-hex-sha>.json`。
  receipt 有既定八個 top-level keys與恰好八個 `thread`、`comment`、`outcome`、`reply` entries，pair set 僅為上述八對；
  Reviewer 獨立選擇 `REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK`。只有 committed `REPLY_AND_RESOLVE` 的 non-empty factual reply
  才能在後續授權 exact reply/resolve；其餘 reply 必為 JSON `null`。
- `jnBpk`/`4043480108`、`kQ95O`/`4060023123`、`kqiZ5`/`4070096561`、`lAR8T`/`4078761998`、`lfQmF`/`4091213944` 是
  Human-only/open exclusions。每個其他 thread、所有 predecessor artifacts、未列 path、PR approval、merge、release 與 post-merge
  皆 ReadOnly；錯誤 writer/path/SHA/schema/pair/enum/nullability/staleness/non-sole commit 一律 fail closed。

## C29 三檔 architecture conflict integration 補充（current route）

- C28 八對 exact receipt replies 已由 Implementer／Planner live 核實且均 resolved；preceding tracking commit
  `2d204b070cc9701cfdce31940cbfe377403f1894` 非 action evidence。reply IDs 映射：`lfYsH`→`4140433910`、
  `lfYsK`→`4140435052`、`m8u04`→`4140436064`、`m8u09`→`4140436858`、`m82WL`→`4140437667`、
  `m82WS`→`4140438539`、`m9eUV`→`4140439397`、`m9eUY`→`4140440128`。
- Goal／In-Scope：完整整合 dev `d6ff74ddf65c615f65eeba252e648784252a2bfd` 已提交 tree，base
  `1501f380f20492c71275474f800fdaaffbf0a76a`；僅手動解衝 business-capability 的 `architecture-brief.md`、
  `index.html`、`scene.js`。其餘 committed dev tree 自動 parent integration，不授權手動改動。
- 保留 feature Runtime protocol／Model Execution 與 dev Response Reuse fixed-codec／bytes-envelope committed facts；
  不新增架構／BC wiring 決策。原 mission、scope、outcomes、reuse protocol、測試、visualization、follow-ups 延續。
- 五份 planning candidate → independent SHA-bound approved Plan-Reviewer receipt sole commit → immutable merge subject →
  factual Tester evidence sole commit → independent same-subject review sole commit → Phase 4.5 → push／PR audit。
  新 evidence 的 exact path／schema／writer／sole ordering 由 technical-spec C29 定義；future facts 不預填。
- Out-Of-Scope／Non-Goal：thread classification／reply／resolve、新架構、backend／DI／mapper／lifecycle、Human PR
  approval／merge、release／post-merge。ReadOnly：predecessor receipts、三檔外手動修改與 dev worktree。Deleted：無。
- Human-only/open 五對 `jnBpk`/`4043480108`, `kQ95O`/`4060023123`, `kqiZ5`/`4070096561`,
  `lAR8T`/`4078761998`, `lfQmF`/`4091213944`。其餘五對 `m-94E`/`4130289778`, `m-94K`/`4130289786`,
  `nXkrM`/`4140364926`, `nXrAw`/`4140406331`, `nXrA0`/`4140406337` 未分類/open，無 disposition。

## C30 Current-Head Seven-Pair Classification Intent

C29 已完成 bounded push 與 PR audit；實際 audited PR head 為
`ee2825c785aad152e5785a021acdb68e3056e84d`。C30 僅獨立分類七對未分類 comments：
`m-94E`/`4130289778`、`m-94K`/`4130289786`、`nXkrM`/`4140364926`、`nXrAw`/`4140406331`、
`nXrA0`/`4140406337`、`nXzEu`/`4140459575`、`nXzE1`/`4140459585`。
Goal／In-Scope：固定 C29 subject／passing Tester／approved Reviewer／audited head 的 immutable classification。
Modify：五份 standard planning artifacts；Written：獨立 Plan-Reviewer receipt 與 classification receipt。
Deleted：無。ReadOnly：其餘 paths、predecessor evidence、dev worktree、五個 Human-only locks。
Non-Goal／Out-Of-Scope：新實作、RED／green、source／tests／architecture 修改、PR approval／merge／release。
TestCase：exact pairs、writer／schema／SHA binding、sole evidence-only ordering 與 stale-head fail-closed。
原 mission、scope、protocol、outcomes、測試策略、Architecture Visualization 與 follow-up missions 不變。

## C31 Five-ADDRESS Bounded Repair Intent（current route）

C30 classification sole commit `005ec865f216de9f63f7dbfdd8df424d78a03afa` 已提交。C30 live actions 已完成：
`m-94E`/`4130289778` reply `4140750473`、`nXrAw`/`4140406331` reply `4140753564`，兩個 threads 已 resolved。
C31 只處理其五個 ADDRESS pairs：`m-94K`/`4130289786`、`nXkrM`/`4140364926`、`nXrA0`/`4140406337`、
`nXzEu`/`4140459575`、`nXzE1`/`4140459585`；不預填修正結果或新的 classification disposition。

- Goal／In-Scope：補齊既有 static BC-independence scanner 的 paired tuple/list destructuring、builtins getattr、
  positional／keyword-only default callable bindings，以及 call args／kwargs 傳遞 forbidden callable 偵測；將既有圖
  Response Reuse Miss edge 終點改為 future integration boundary，遵守 architecture-brief 第 6 點。
- Modify：Plan-Creator 僅五份 standard planning artifacts；Implementer RED／green 僅
  `tests/test_loaded_runtime_cache_bc_independence.py`、`docs/architecture/business-capability/scene.js`、
  `docs/architecture/business-capability/index.html`（RED 僅測試檔）。Written：SHA-bound Plan-Reviewer、Tester、
  Independent Reviewer 與 current-head classification receipts，exact contracts 見 technical-spec C31。
- TestCase：成對 destructuring 只保留 matching simple-name targets、忽略 attribute targets；builtins
  `getattr(..., '__import__')` assigned／direct invocation；function positional／kw-only defaults 的 callable alias；
  `executor.submit`／`map` 等 call positional／keyword arguments 傳遞 forbidden import callable；正常 callable
  與 attribute-only targets 不誤判。Miss route 不落在 Runtime Cache，scene 與 inline scene 相同。
- Out-Of-Scope／Non-Goal：runtime source／API／outcomes 修改、執行 source 或 imports、general-purpose Python
  interpreter／call-graph inference、新 architecture／ACL mapper／BC wiring／backend／DI／lifecycle。
- ReadOnly：dev worktree、predecessor evidence、architecture-brief 與所有未列 paths／threads。Deleted：無。
  `nYQqw`/`4140648790` 未分類/open；五個 Human-only locks `jnBpk`、`kQ95O`、`kqiZ5`、`lAR8T`、`lfQmF`
  排除/open。PR approval／Human merge／release／post-merge 未授權。
- candidate → independent approved receipt → RED／failing evidence → green／passing evidence → independent review →
  Phase 4.5／push → actual-head-bound five-pair classification → exact permitted replies／resolve，所有 evidence sole commits。
  原 mission、protocol、outcomes、Architecture Visualization 與 follow-up missions 不變。

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

C32 classification-only，不建立新的 implementation subject／Tester／implementation review chain；消費固定 C31 triple。

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

## C50 Bounded Four-ADDRESS Repair（authoritative current routing）

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
