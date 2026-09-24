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
