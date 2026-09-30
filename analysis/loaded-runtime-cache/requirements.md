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

## C39 Current-Head Single-Pair Classification（authoritative current routing）

### Goal / Outcome / Scope / Locked Decisions

Current：`c39-planning-draft`。僅獨立分類 `ncxdC`/`4142518115`，
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
僅 `ncxdC` 待獨立分類；七 Human-only threads 保持 open。No release/post-merge actions。
