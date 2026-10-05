# Loaded Runtime Cache Specification

## Acceptance Criteria

1. Loaded Runtime Cache 有自己的 nominal immutable opaque `RuntimeReuseKey`；其 responsibility 是 local
   reusable-runtime locator，且不等同或引用 `ModelIdentity`。只有本 BC 外的 integration／ACL 可建立並交入 key；
   construction token 不是 public API，不可用 `str`／hash 取代、不可被讀取，且 `repr` 不得暴露 token；key 採
   instance identity semantics，即使 token unhashable 或 custom-equality 也不呼叫其 equality／hash。
2. `RuntimeRegistry[RuntimeT]` 的 `lookup(key: RuntimeReuseKey) -> RuntimeT | None` 與
   `retain(key: RuntimeReuseKey, runtime: RuntimeT) -> None` 是 synchronous Protocol contract。
3. `RuntimeRetention[RuntimeT].retain(key, runtime)` 回傳 `Retained[RuntimeT] | NotRetained[RuntimeT]`；兩者都
   保留同一 runtime instance。
4. `runtime_registry_port.py` 擁有 `RuntimeRegistryLookupUnavailable` expected signal；Registry 原樣 raise；
   hit／missing 仍只有 `RuntimeT | None`。`lookup_outcome.py` 擁有 `Available`／`Missing`／`Unavailable`
   semantic contracts；本 topic 沒有 signal-to-`Unavailable()` mapper。unexpected exceptions 原樣 propagate。
5. 新增 Python modules 位於 locked three-level taxonomy，沒有 child `__init__.py`、root re-export、facade、
   `importlib`、`__import__`、其 alias／module-alias、`sys.modules` substitution 或 generic module names。
6. Identity BC 與 Loaded Runtime Cache 無任一方向 direct module import、re-export 或 duplicate semantic type；LRC
   不得宣告 `ModelIdentity`，Identity 不得宣告 `RuntimeReuseKey`。
7. Architecture authority 和 Archify dataflow 只宣告 protocol capability；ACL mapping、backend、lifecycle,
   Model Execution、Provider Adapter 均為 external／future／out of scope。
8. C8／C9／C10 是 frozen、unapproved predecessor planning provenance，沒有 routing authority。C11 重用 C5→V3 已提交的
   architecture/dataflow 與 source-contract provenance，不重寫其歷史順序。C11 只在既有
   source ancestor 建立兩個 isolated executable RED assertions（各一個於既有 test module）；它們不是 expected-failing
   或 green-source gate。新的同-subject T11/V11 evidence chain 才是 C11 的獨立 verification route。
9. C11 `55ad5d48c8e638bc5a81f3d0fecfc5a5f35e963c`、R11、S11、T11 與 V11
   `73644c2b88257832e1b4d8bedaf516b803c2ee3a` 是 completed frozen provenance。C12 只改五份 planning artifacts，並在
   fixed PR snapshot 建立 R12 triage contract；它不重寫 evidence、source、tests、architecture／Archify artifacts，也不
   reply 或 resolve threads。

## Behavioral Scenarios

### Scenario 1 — local key handoff

Given local `RuntimeReuseKey` fixture，When typed Registry／Retention fake 接收 lookup／retain，Then 接收同一
key instance，且 test 不檢查 token 或內部欄位、不將 `str`／hash 當作 API，也不依賴會暴露 token 的 `repr`。Given
unhashable 或 custom-equality token，When key 被比較或使用，Then token equality／hash 不被呼叫，key 只維持 instance
identity semantics。

### Scenario 2 — Registry port channels

Given typed Registry fake 回傳 runtime 或 `None`，When direct-module contract 使用 Registry，Then runtime 是 hit
channel、`None` 是 missing channel；不建立 backend 或 runtime lifecycle。

### Scenario 3 — retention outcomes

Given RuntimeRetention fake success／failure channel 和同一 runtime，When consumer 觀察 outcome，Then
`Retained`／`NotRetained` 都保留同一 runtime instance。

### Scenario 4 — expected failure semantics

Given port-owned `RuntimeRegistryLookupUnavailable`、outcome-owned `Unavailable()` 與 `Missing()`，When tests observe
the separate port／outcome contracts，Then the expected signal is raised unchanged and neither semantic outcome is
silently substituted for another; this topic neither tests nor provides a mapper.

### Scenario 5 — BC independence and import regression

Given existing direct imports and new direct-module imports，When targeted import／contract tests 和 existing package
import regression 執行，Then Identity 和 Loaded Runtime Cache 沒有 direct import，既有 fixture、mock、assertion 行為
保持不變；regression 亦拒絕直接 `importlib.import_module`、直接 `__import__`、`importlib` 或
`builtins.__import__` alias／module-alias、以及 `sys.modules` substitution 繞過邊界，且 parser 必須解析 aliases。

### Scenario 6 — visualization evidence

Given frozen Archify JSON candidate，When validate、deliver、`visual-check --repo-root` 依序執行，Then validate
為 showcase 9/9、0 errors、0 warnings，四個 desktop viewports containment 均通過；否則保留 truthful failure／skipped
receipt 並停止 gate。圖使用 `backend` visual type 時必須以 contract-only label 和「僅 Protocol；無 concrete backend、
DI、runtime lifecycle」說明消除實作暗示。

### Scenario 7 — C11 existing-source assertion route

Given C5→V3 architecture/dataflow 與 source-contract artifacts 已是 committed frozen provenance，且 C8／C9／C10 是 frozen
unapproved predecessor，When C11 開始，Then 不修改 architecture、Archify 或 production source。Given C11
Plan-Reviewer receipt 已 committed，When Implementer 建立
assertion subject，Then subject 只修改兩個 declared tests、各加入一個 isolated executable RED assertion，並在既有
source ancestor 以 zero-exit validation 執行。T11 記錄相同 subject 的事實結果；V11 只消費 committed passing T11。不得
聲稱新的 expected-nonzero red failure、RED evidence 或 green-source authorization。

### Scenario 8 — retention dataflow semantics

Given dataflow 描繪 retain path，When reader 檢視 Runtime Registry relationship，Then `RuntimeReuseKey` 明示為
retain input；synchronous `NotRetained(runtime)` failure 使用實線 outcome relationship，dashed relationship 只在
明確標示的 async flow 出現，且本圖不把 synchronous retain failure 描繪成 async。

### Scenario 9 — C11 cross-BC semantic-type regression

Given LRC 或 Identity source 嘗試自行宣告對方的 semantic type，When C11 BC-independence assertion 解析 direct 或 alias
imports 和 declarations，Then LRC `ModelIdentity` 或 Identity `RuntimeReuseKey` 的 duplicate semantic type 都使 test
失敗；C11 不改 production source、不能改為 mapper 或 shared type。

### Scenario 10 — C12 factual PR triage

Given C11/R11/S11/T11/V11 已按 commit chain 完成且 snapshot 固定為
`73644c2b88257832e1b4d8bedaf516b803c2ee3a`，When independent Plan-Reviewer 建立 R12，Then
`copilot_feedback_triage` 非空並完整列出 snapshot 的 current unresolved threads；每筆都有 `thread`、`comment`、
`finding`、`commit`、`basis`、`disposition`。F `PRRT_kwDOUJTij86jnBpk`／`4043480108` 及 architecture/ACL
`PRRT_kwDOUJTij86kQ95O`／`4060023123` 是 `DISCUSS` 且維持 Human-only `human-check`；其他 factual current entries 是
`SKIP`。C12 不把此 triage 假裝成 code fix、comment reply 或 thread resolution。

## Error / Edge Cases

1. **Unexpected exception:** Given a Registry fake raises an exception other than
   `RuntimeRegistryLookupUnavailable`, When the port contract is used, Then the exception propagates unchanged; it is
   not classified as `None`, `Missing()` or `Unavailable()`.
2. **Expected operational failure:** Given Registry raises `RuntimeRegistryLookupUnavailable`, When a direct-module
   contract test invokes lookup, Then that exact signal remains distinguishable from a `None` miss and the separate
   `Unavailable()` outcome type; no signal-to-outcome consumer is implemented.
3. **Retention failure:** Given a `NotRetained` outcome, When the caller receives it, Then it retains the exact input
   runtime instance for caller-side handling.
4. **Import boundary:** Given either BC attempts a direct import of the other, re-export, duplicate semantic type,
   direct `importlib.import_module`, direct `__import__`, `importlib`／`builtins.__import__` alias or module-alias, or
   `sys.modules` dynamic-import workaround, When the alias-aware BC-independence regression runs, Then it fails.
5. **Opaque-token equality/hash:** Given a `RuntimeReuseKey` construction token is unhashable or its custom equality
   and hash would raise／record use, When key identity is exercised, Then neither token equality nor hash is invoked.
6. **Visual gate failure:** Given Archify validate, deliver, or visual-check is non-zero or visual-check is skipped,
   When evidence is recorded, Then the failure／skipped result is retained truthfully and the delivery gate stops.
7. **C11 scope breach:** Given C11 assertion subject changes a source, architecture, Archify or evidence path, When
   Planner／Reviewer classifies it, Then it is out of scope and cannot be used for T11/V11 routing.
8. **Evidence path collision or provenance reuse:** Given T11 or V11 uses a fixed-name, C5/T3/V3, C8/C9/C10, or legacy
   `6110cb…`／`44e477…` path, or references another subject, When it is written, Then it fails closed. T11/V11 must use
   new SHA-bound non-overwritable paths and bind the C11 assertion subject only.
9. **Incomplete C12 triage:** Given R12 omits a current snapshot thread, has an empty triage, lacks any of the six
   factual fields, uses a future／abbreviated／unverifiable commit, or classifies F／architecture-ACL ownership as resolved,
   When Planner consumes it, Then it fails closed and cannot authorize comment reply or resolution.

### Scenario 11 — C14 chained-assignment RED then green route

Given a fresh C14 approved planning receipt, When Implementer creates the first immutable C14 test-only subject in
`tests/test_loaded_runtime_cache_bc_independence.py`, Then the test module collects successfully and a chained
assignment import-alias assertion actually fails. This is new factual RED evidence and neither replays nor rewrites
historical `e2e125` evidence. Given the resulting failing Tester record, When a later green subject is created, Then it
handles every all-simple-name assignment target in the chained alias and passes the direct-import regression without
dynamic-import, source, or cross-BC workaround.

### Scenario 12 — C14 truthful retention dataflow correction

Given the C14 sole ten-path dataflow allowlist, When the green subject updates the diagram and evidence, Then
the retain relationship names `RuntimeReuseKey + runtime`, both returns are labelled `Retained(runtime)` and
`NotRetained(runtime)`, edges do not obscure those labels, and receipts truthfully show showcase validation/delivery
and containment at 1440×900, 1600×1000, 1920×1080, and 2048×1320. The four existing dark/light 1440×900 and
2048×1320 PNG captures may be replaced; only paths that actually byte-change through JSON／HTML delivery／visual-check
may enter the green subject. In particular, byte-identical `.validation.json` and `.visual-check.html` remain ReadOnly;
no other architecture authority path may change.

### Scenario 13 — C14 evidence separation

Given a C14 RED subject with its own full 40-hex SHA, When Tester records the collection-success / assertion-failing
command, Then it writes only
`loaded-runtime-cache.tester-evidence-<red-subject-40-hex-sha>.json` with exact factual schema and `status: failing`;
Implementer alone commits it unchanged in a sole evidence-only commit; and no Independent Reviewer record is
permitted. Given a distinct green subject, When all factual commands pass, Then Tester uses the same SHA-bound Tester
template with the green SHA and `status: passing`; only its committed sole evidence-only commit can be consumed by an
Independent Reviewer at
`loaded-runtime-cache.implementation-review-log-<green-subject-40-hex-sha>.json`.

### Scenario 14 — C14 fail-closed provenance boundary

Given C5→V3, C11→V11, C12→R12, or
`9aa656b13fdc36492273c97a62eb9d422a1b64b5`, or C13 `a623981989f3363a4b225319a432c3a9d8e28b96`/`cf91b55f80f1764e040c95c822ae55b290e3699c`/`3ba583bed8c367b756e2cb450e468f1274d04193`/`c4f229f14d3c4c38d40cdda8ad0429712e0ae189`/`ade584e7eb63a7846a23c073c06a802ff99ff6cf`, When any actor attempts to use it as C14 candidate, receipt, subject,
Tester evidence, or review evidence, Then routing fails closed. `9aa656b13fdc36492273c97a62eb9d422a1b64b5` is unapproved
`needs-rework` planning provenance only.

## C14 Evidence Edge Cases

1. **Tester schema failure:** Given a C14 Tester record has any missing or extra top-level key, non-integer schema
   version, non-40-hex/abbreviated subject, empty commands, an invalid command item, `passing` with non-zero exit, or
   `failing` with no non-zero exit, When Planner or Reviewer consumes it, Then it fails closed.
2. **Reviewer misuse:** Given a RED failing record, an uncommitted/non-sole Tester record, or a different topic or
   subject, When Independent Reviewer attempts review, Then it must produce no review record. A green review record
   may only consume committed same-subject `passing` evidence and must itself have exactly the declared schema.

## C15 Mixed-Assignment Successor Scenarios

### Scenario 15 — direct simple target is preserved

Given a fresh C15 approved receipt, when the RED subject adds a collection-success static regression for
`load = holder.loader = importlib.import_module`, then its assertion actually fails and Tester records factual
`failing` evidence. Given the distinct green subject, when alias collection examines the assignment, then it retains
the direct `ast.Name` target `load`, ignores direct `ast.Attribute` target `holder.loader`, and detects a later direct
call through `load`.

### Scenario 16 — no recursive destructuring or runtime escape

Given tuple/list/starred/subscript/attribute or other non-simple targets, when the helper collects aliases, then it
does not recurse into them or retain nested names. It executes no AST and uses no dynamic import, runtime
introspection, cross-BC import, source change, or architecture change.

### Scenario 17 — C15 evidence and human boundary

Given C15, when a candidate or later evidence artifact is written, then it uses only its versioned SHA-bound template
after the relevant immutable subject exists; no future SHA is prefilled. C14 and
`37d7233e7231151c0dac6aaa1a7820bff746ffdc` are nonrouting provenance. After passing green Tester and approved
Reviewer evidence, Planner may perform Phase 4.5 and independent classification only; F／ACL/business architecture
remain Human-only `human-check`.

## C16 Thread-Classification Receipt Successor Scenarios

### Scenario 18 — immutable C15-bound seven-pair receipt

Given the completed C15 subject `7dab2b9742bd19f962bef99be83b40b978f87f0f`, passing Tester evidence commit
`475e3c953f6551bef5834d0bf350d5c79449a43e`, approved review evidence commit
`cee5097c176b4321a0d9bc2e810caf7d3425d0f1`, and snapshot `7e525b1ad8dc77c25b0b11a467f6b1f24884ecd3`, when C16
has a committed approved planning receipt, then only Independent Reviewer writes
`loaded-runtime-cache.thread-classification-receipt-7dab2b9742bd19f962bef99be83b40b978f87f0f.json`, and only
Implementer commits it unchanged alone. The JSON has exactly its eight declared top-level keys and exactly the seven
listed current thread/comment pairs, each with only `thread`, `comment`, `outcome`, `reply`.

### Scenario 19 — independent disposition and Human-only locks

Given the classification receipt, when Independent Reviewer examines the seven pairs, then ACL
`PRRT_kwDOUJTij86kQ95O`/`4060023123` and business-architecture
`PRRT_kwDOUJTij86kqiZ5`/`4070096561` are `HUMAN_CHECK` with `reply: null` and stay open. The other five outcomes are
not planned or prefilled: Reviewer independently selects `REPLY_AND_RESOLVE`, `ADDRESS`, or `HUMAN_CHECK`. Only an
exact committed `REPLY_AND_RESOLVE` entry permits an Implementer to leave its non-empty factual reply and resolve
that exact pair. `ADDRESS` returns to Planner; `HUMAN_CHECK` is never replied to or resolved.

## C16 Error / Edge Cases

1. Given a receipt has a missing/extra top-level or entry key, wrong role/path/full SHA, non-ancestor C15 binding,
   wrong snapshot, missing/duplicate/extra pair, invalid outcome, or an invalid reply nullability, when Planner
   consumes it, then it fails closed and no thread action is routed.
2. Given a C16 Plan-Reviewer receipt is `needs-rework`, a classification receipt is uncommitted/non-sole/altered, or
   `ADDRESS` is present, when any actor attempts a PR reply/resolve, then the action is forbidden; routing returns to
   Plan-Reviewer or Planner as applicable.

## C17 ADDRESS Remediation Scenarios

### Scenario 20 — `getattr` alias RED and green evidence

Given an approved C17 planning receipt, when the RED subject assigns a local alias from `getattr` of a known
`importlib`/`sys` alias and literal `import_module`/`modules`, then collection succeeds and its assertion fails;
Tester records factual same-subject `failing` evidence and no Reviewer record exists. Given the distinct green subject,
when that local alias is used, then the scanner rejects it while preserving direct, chained and mixed alias coverage,
without executing AST or runtime `getattr`.

### Scenario 21 — truthful protocol-only dataflow

Given the green subject, when the topic dataflow is regenerated, then it shows
`RuntimeRegistry.lookup(key: RuntimeReuseKey) -> RuntimeT | None`, not `Available`/`Missing` as lookup returns or a
mapper/concrete backend/lifecycle/ACL. When validate, deliver and visual-check succeed, only their byte-changed named
outputs join the subject; visual evidence is non-skipped and includes 1440×900, 1600×1000, 1920×1080 and 2048×1320.

### Scenario 22 — Human-only README and later classification

Given `4078761998`, when C17 remediates the other two findings, then it does not select/modify `README.md`, reply to,
or resolve that public-surface thread. After matching green passing Tester and approved Reviewer evidence, a new
independent classification—not C17 itself—decides an exact reply/resolution for C17's two pairs.

## C17 Error / Edge Cases

1. Unknown/dynamic `getattr` receivers or attributes must not trigger runtime evaluation or arbitrary-expression
   scanning.
2. A non-zero, warning/error, skipped, incomplete-viewport, or hand-edited Archify result fails closed.
3. A README or unlisted-path change is `needs-rework` and cannot authorize a PR action.

## C18 Current-Head Classification Scenarios

### Scenario 23 — immutable C17-bound eleven-pair receipt

Given committed C17 subject `7ceb3409d6d8b9ff3dc51485c3588f502bdff882`, passing Tester evidence commit
`b58cb1e330fe12ccc80a8f39b875a61ea6024067`, approved Reviewer evidence commit
`edbae51a0ee86cff498d6caf4e6aa78b58962a82`, and PR head
`bf63a3c6a0533ad0f367305deff029eddc2b18be`, when the C18 candidate has an independently committed approved
standard Plan-Reviewer receipt, then only Independent Reviewer may write
`loaded-runtime-cache.thread-classification-receipt-7ceb3409d6d8b9ff3dc51485c3588f502bdff882.json`; only
Implementer may commit that unchanged file alone. The receipt has exactly its eight top-level keys and exactly eleven
entries with only `thread`, `comment`, `outcome`, `reply`.

### Scenario 24 — fixed Human boundaries and independent remaining outcomes

Given C18's exact eleven pair set, when Independent Reviewer classifies it, then F
`PRRT_kwDOUJTij86jnBpk`/`4043480108`, ACL `PRRT_kwDOUJTij86kQ95O`/`4060023123`, business architecture
`PRRT_kwDOUJTij86kqiZ5`/`4070096561`, and README `PRRT_kwDOUJTij86lAR8T`/`4078761998` are `HUMAN_CHECK` with
`reply: null` and remain open. The other seven outcomes/replies are not preplanned; Independent Reviewer decides
them. Only an exact committed `REPLY_AND_RESOLVE` entry permits Implementer to leave that non-empty factual reply and
resolve that exact thread. `ADDRESS` returns to Planner; no Human-only pair is replied to or resolved.

## C18 Error / Edge Cases

1. A classification receipt with missing/extra keys, a wrong writer/path/full SHA, non-ancestor or non-sole
   evidence, wrong PR head, missing/duplicate/extra pair, invalid outcome, or invalid reply nullability fails closed
   and authorizes no thread action.
2. A C18 Plan-Reviewer `needs-rework` receipt, an uncommitted classification receipt, or an entry other than exact
   `REPLY_AND_RESOLVE` never authorizes reply or resolution.

## C19 Current-Head Reconciliation Classification Scenarios

### Scenario 25 — immutable five-pair C17-bound receipt

Given C17 subject `7ceb3409d6d8b9ff3dc51485c3588f502bdff882`, passing Tester evidence commit
`b58cb1e330fe12ccc80a8f39b875a61ea6024067`, approved Reviewer evidence commit
`edbae51a0ee86cff498d6caf4e6aa78b58962a82`, and current PR head
`3e803a507b2dfa74efdf71164c260da172aadb81`, when C19 has a committed approved standard Plan-Reviewer receipt,
then only Independent Reviewer may write the current-head-suffixed immutable classification receipt and only
Implementer may commit it unchanged alone. The receipt has exactly its eight top-level keys and five entries with
only `thread`, `comment`, `outcome`, `reply`.

### Scenario 26 — new-pair independence and `lAR8Y` reconciliation

Given the C19 exact pair set, when Independent Reviewer classifies it, then the four new pairs
`lCkFr`/`4079664571`, `lCkFu`/`4079664575`, `lDH2-`/`4079885261`, and `lDH3C`/`4079885267` receive no planned
outcome or reply. For `lAR8Y`/`4078762005`, `ALREADY_RESOLVED`/`null` is legal only when Reviewer verifies the
current GitHub state already resolved it; otherwise Reviewer independently applies the general outcome rules. Exact
committed `REPLY_AND_RESOLVE` alone allows the exact non-empty factual reply and resolve action. F, ACL, business
architecture and README Human-only locks are excluded and remain open.

## C19 Error / Edge Cases

1. A receipt that uses the prior C18 path, omits its current-head suffix, has other than the exact eight top-level
   keys/five pair set, or mismatches C17 subject/T17/V17/current head fails closed.
2. `ALREADY_RESOLVED` on any pair except `lAR8Y`, without current-state verification, or with a non-null reply fails
   closed. It never authorizes comment or resolution.

## C20 ADDRESS Remediation Scenarios

### Scenario 27 — separate expected lookup failure in the dataflow

Given C20's approved planning receipt and a test-only RED subject, when the topic dataflow has no separate
`RuntimeRegistryLookupUnavailable` signal, then the new assertion fails while collection succeeds. Given the green
subject and regenerated topic outputs, when the dataflow is inspected, then
`RuntimeRegistry.lookup(key: RuntimeReuseKey) -> RuntimeT | None` remains the normal lookup return and
`RuntimeRegistryLookupUnavailable` is a distinct expected-failure signal; no mapper or signal-to-outcome flow exists.

### Scenario 28 — foreign semantic ImportFrom local alias

Given a temporary Loaded Runtime Cache source that says
`from deterministic_response_cache.identity.contracts import ModelIdentity as LocalModelIdentity`, when C20 RED is
executed, then the scanner assertion fails because that import shape is not yet rejected. Given the distinct C20 green
subject, then the scanner rejects the foreign semantic import despite the local alias, without execution, dynamic
imports, module-cache access, or a rule that rejects unrelated `ImportFrom` names.

### Scenario 29 — exact evidence and two-pair classification boundary

Given the green subject, when Archify validate, deliver and visual-check succeed in order, then only byte-truthful
members of the exact ten C20 dataflow paths accompany the test change. After same-subject passing Tester evidence,
approved independent Reviewer evidence and Phase 4.5, only an immutable C20 classification receipt may classify
`lCkFu`/`4079664575` and `lDH2-`/`4079885261`; planning does not preselect either outcome or reply.

## C20 Error / Edge Cases

1. Treating `RuntimeRegistryLookupUnavailable` as `RuntimeT | None`, or adding any mapper between the signal and a
   lookup outcome, is scope/contract drift and fails closed.
2. A scanner that executes fixture source, uses `importlib`、`__import__` or `sys.modules`, misses the `as` alias, or
   rejects an unrelated foreign import is invalid.
3. An unlisted dataflow artifact, non-zero/skip/warning/error Archify result, hand-edited receipt, missing exact
   viewport, or uncommitted/non-sole/mismatched evidence fails closed and authorizes no PR action.

## C21 Current-Head Single-Pair Classification Scenarios

### Scenario 30 — immutable C20-bound one-pair receipt

Given C20 subject `fa1468301af1906a05ee31ba0d267d2270d7af5f`, passing Tester evidence commit
`6423f55b6dbcde5bee190ef86dc8c31f5c27c94e`, approved Reviewer evidence commit
`3d0dc9fbb0e9da6d742ac20856b8aac6b0a3035e`, and current PR head
`a1aae44897c0f0b0ac52f1ca1697554c2f79cdb5`, when C21 has a committed approved standard Plan-Reviewer receipt,
then only Independent Reviewer may write the current-head-suffixed immutable classification receipt and only
Implementer may commit it unchanged alone. The receipt has exactly eight top-level keys and one entry with only
`thread`, `comment`, `outcome`, `reply` for `PRRT_kwDOUJTij86ldYVf`/`4090457782`.

### Scenario 31 — independent outcome and exact action boundary

Given the C21 exact pair, Independent Reviewer independently determines its outcome and reply; planning preselects
neither. Only an exact committed `REPLY_AND_RESOLVE` entry with a non-empty factual reply permits Implementer to
leave that reply and resolve that exact thread. `ADDRESS` and `HUMAN_CHECK` require `reply: null`, return to Planner
or remain open respectively. All other threads, including existing Human-only locks, are excluded and untouched.

## C21 Error / Edge Cases

1. A receipt whose path omits either the C20 subject or current-head suffix, has any missing/extra top-level or entry
   key, binds a different subject/evidence/head, has a non-sole commit, or contains any extra/duplicate/missing pair
   fails closed and authorizes no PR action.
2. A non-null `ADDRESS`/`HUMAN_CHECK` reply, empty `REPLY_AND_RESOLVE` reply, wrong writer, or any attempt to act on
   an excluded thread fails closed.

## C22 Current-Head Dual-Pair Classification Scenarios

### Scenario 32 — immutable C20-bound two-pair receipt

Given C20 subject `fa1468301af1906a05ee31ba0d267d2270d7af5f`, passing Tester evidence commit
`6423f55b6dbcde5bee190ef86dc8c31f5c27c94e`, approved Reviewer evidence commit
`3d0dc9fbb0e9da6d742ac20856b8aac6b0a3035e`, and current PR head
`0991c56ec7e562ea512449bda1a41118dbc48203`, when C22 has a committed approved standard Plan-Reviewer receipt,
then only Independent Reviewer may write the current-head-suffixed immutable classification receipt and only
Implementer may commit it unchanged alone. The receipt has exactly eight top-level keys and two entries with only
`thread`, `comment`, `outcome`, `reply` for `PRRT_kwDOUJTij86ldeVI`/`4090495760` and
`PRRT_kwDOUJTij86ldeVO`/`4090495770`.

### Scenario 33 — independent outcome and excluded boundary

Given the C22 exact pair set, Independent Reviewer independently determines each outcome and reply; planning
preselects neither. Only an exact committed `REPLY_AND_RESOLVE` entry with a non-empty factual reply permits
Implementer to leave that reply and resolve that exact thread. `ADDRESS` and `HUMAN_CHECK` require `reply: null`,
return to Planner or remain open respectively. F, ACL, business architecture, README Human-only locks, and new
`PRRT_kwDOUJTij86ld9Ai` are excluded and untouched.

## C22 Error / Edge Cases

1. A receipt whose path omits either the C20 subject or current-head suffix, has any missing/extra top-level or entry
   key, binds a different subject/evidence/head, has a non-sole commit, or contains any extra/duplicate/missing pair
   fails closed and authorizes no PR action.
2. A non-null `ADDRESS`/`HUMAN_CHECK` reply, empty `REPLY_AND_RESOLVE` reply, wrong writer, or any attempt to act on
   a Human-only or otherwise excluded thread fails closed.

## C23 ADDRESS Remediation Scenarios

### Scenario 34 — dataflow protocol fidelity

Given the C22 `ldeVI` ADDRESS result recorded in classification receipt commit
`a9065a8332119930347214f07f2980d655d8d314`, bound to C20 subject
`fa1468301af1906a05ee31ba0d267d2270d7af5f`, passing Tester evidence
`6423f55b6dbcde5bee190ef86dc8c31f5c27c94e`, approved Reviewer evidence
`3d0dc9fbb0e9da6d742ac20856b8aac6b0a3035e`, and C22 PR head
`0991c56ec7e562ea512449bda1a41118dbc48203`, when C23 RED/green evidence is produced, then the dataflow retains exactly
`RuntimeRegistry.lookup(key: RuntimeReuseKey) -> RuntimeT | None` and only
`RuntimeRegistry -> RuntimeRegistryLookupUnavailable` as the expected-failure edge. It never connects lookup to
`Available`, `Missing`, `Unavailable` or a mapper, and never claims a concrete backend, DI, lifecycle, execution,
provider or ACL.

### Scenario 35 — NamedExpr alias is statically rejected

Given `(load := importlib.import_module)(...)`, when the BC-independence AST scanner collects aliases, then it detects
the simple-name walrus binding without executing a fixture, dynamic import or runtime module. Given
`load = holder.loader = importlib.import_module`, it retains only `load` and ignores `holder.loader`.

### Scenario 36 — evidence and only eventual exact PR action

Given a committed approved C23 Plan-Reviewer receipt, C23 RED failing Tester evidence, distinct green passing Tester
evidence and approved independent green review evidence, when Planner verifies the actual current head, then only
Independent Reviewer may create the SHA-bound two-pair classification receipt at
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-<c23-green-subject-40-hex-sha>-<current-pr-head-40-hex-sha>.json`.
Its exact top-level keys are `schema_version`, `topic`, `implementation_subject_commit`, `tester_evidence_commit`,
`implementation_review_evidence_commit`, `pr_head_commit`, `classifications`, `recorded_by`; its entries have only
`thread`, `comment`, `outcome`, `reply` for `ldeVI`/`4090495760` and `ldeVO`/`4090495770`, and outcome is only
`REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK`. Only an exact committed `REPLY_AND_RESOLVE` classification with non-empty
factual reply permits the corresponding reply/resolve; `ADDRESS` and `HUMAN_CHECK` use JSON `null`. F, ACL, business,
README and `ld9Ai` remain open and excluded; no action changes them.

## C23 Error / Edge Cases

1. Any recursive NamedExpr target parsing, fixture execution, dynamic import or runtime-module inspection fails
   closed, as does any change that alters the existing mixed-assignment semantics.
2. A dataflow connection from `RuntimeRegistry.lookup` to outcome/mapper nodes, or any non-signal expected-failure
   edge, is out of scope and fails review.
3. Missing/incorrect SHA-bound candidate, receipt, RED/green evidence, review evidence or current-head classification
   path (including either required subject/head suffix); an extra pair; wrong writer; a non-sole evidence commit;
   invalid top-level/entry keys, outcome or nullability; or action on an excluded pair fails closed.

## C24 Current-Head Dual-Pair Classification Scenarios

### Scenario 37 — C23-bound immutable two-pair receipt

Given C23 subject `240c694fa5078dc1d35f154f7a85b06381db2e47`, passing Tester evidence
`dabce082058805281990c52b12352b87c2b46801`, approved Reviewer evidence
`489752c727aa86cfaf49038cc2ed6dfddf33ba2d`, C23 classification provenance/current PR head
`e5872d5dfb2018743b1f7e319551d52f25f5ef02`, and a committed approved C24 Plan-Reviewer receipt, then only
Independent Reviewer may write the current-head-suffixed receipt and only Implementer may commit it unchanged alone.
The receipt has exactly eight top-level keys and exactly two entries with only `thread`, `comment`, `outcome`, `reply` for
`PRRT_kwDOUJTij86lfQl9`/`4091213935` and `PRRT_kwDOUJTij86lfQmF`/`4091213944`.

### Scenario 38 — independent outcome and frozen exclusions

Given the exact C24 pair set, Reviewer independently determines every outcome and reply; planning supplies neither.
Only committed `REPLY_AND_RESOLVE` plus non-empty factual reply permits the matching Implementer reply/resolve.
`ADDRESS`/`HUMAN_CHECK` require null reply and route to Planner/open state. C23 resolved pairs, F/ACL/business/README
Human-only locks and `ld9Ai` are excluded, ReadOnly and untouched.

## C24 Error / Edge Cases

1. A path without the fixed subject/head suffix, an incorrect binding, missing/extra JSON key or pair, wrong writer,
   non-sole commit, invalid enum/nullability, or stale classification fails closed and authorizes no action.
2. Any action on a C23-resolved pair, Human-only lock, `ld9Ai`, or another unclassified thread is out of scope.

## C25 Static Attribute-base NamedExpr Remediation Scenarios

### Scenario 39 — collection-success then actual static failure

Given a committed approved C25 Plan-Reviewer receipt, when the RED-only scanner test subject is created for
`(loader := importlib).import_module(...)`, then it collects successfully and its assertion actually fails. The test
does not execute a fixture or AST, import dynamically, or inspect runtime modules.

### Scenario 40 — bounded green static recognition

Given the direct `ast.Attribute` base is an `ast.NamedExpr` with direct simple-name target `loader`, value resolving to
a known `importlib` module alias and attribute `import_module`, when the green scanner subject runs, then it rejects the
alias bypass. It does not recurse through the target or expression, and it preserves direct-name NamedExpr, mixed
assignment simple-name/attribute-target behavior, `getattr`, and `sys.modules` behavior unchanged.

### Scenario 41 — immutable one-pair current-head classification

Given committed C25 passing Tester evidence and approved independent green review evidence, when Planner verifies the
actual current PR head, then only Independent Reviewer may write
`loaded-runtime-cache.thread-classification-receipt-<c25-green-subject-40-hex-sha>-<actual-current-pr-head-40-hex-sha>.json`
with exactly eight top-level keys and one `thread`, `comment`, `outcome`, `reply` entry for `lfQl9`/`4091213935`.
Only Implementer may commit it unchanged alone. Candidate supplies no SHA, outcome or reply; only committed
`REPLY_AND_RESOLVE` with non-empty factual reply can later route exact action. `lfQmF`, Human-only locks and other
open/unclassified threads remain untouched.

## C25 Error / Edge Cases

1. Any recursive target/expression walk, execution, dynamic import, runtime introspection, or modification of a
   frozen scanner path is out of scope and fails review.
2. Any C25 production/docs/dataflow/predecessor-evidence change, `lfQmF` action, or malformed/stale/non-sole
   candidate/evidence/classification record fails closed and authorizes no PR action.

## C26 Current-Head Seven-Pair Classification Scenarios

### Scenario 42 — C25-bound immutable seven-pair receipt

Given C25 green subject `13f987a41119590621671c429293cf549055672b`, passing Tester evidence commit
`e85f936505a323e6c84c02e90f4c4114e39b6505`, approved Reviewer evidence commit
`24d5141332cbc4dcf7a87dea7f134207a16ab37e`, current-head base
`8bd9460950237c48c9befb73a1c5b80d084e88ae`, and a committed approved C26 Plan-Reviewer receipt, when Independent
Reviewer creates the classification record, then only
`loaded-runtime-cache.thread-classification-receipt-13f987a41119590621671c429293cf549055672b-8bd9460950237c48c9befb73a1c5b80d084e88ae.json`
is valid and only Implementer may commit it unchanged alone. It has exactly eight top-level keys and exactly seven
entries with only `thread`, `comment`, `outcome`, `reply` for `ld9Ai`/`4090688118`, `lfYsF`/`4091265104`,
`lfYsH`/`4091265108`, `lfYsK`/`4091265115`, `m8u00`/`4129370918`, `m8u04`/`4129370926`, and
`m8u09`/`4129370931`.

### Scenario 43 — independent disposition and protected exclusions

Given the exact C26 pair set, Reviewer independently determines every outcome and reply; planning supplies neither.
Only committed `REPLY_AND_RESOLVE` with a non-empty factual reply permits the matching exact Implementer reply/resolve.
`ADDRESS` and `HUMAN_CHECK` require null reply and route to Planner/open state. `jnBpk`, `kQ95O`, `kqiZ5`, `lAR8T`,
and `lfQmF` stay Human-only/open; C25 `lfQl9` and every unlisted thread stay untouched.

## C26 Error / Edge Cases

1. A path without the fixed C25-subject/current-head suffix, incorrect C25 binding, missing/extra JSON key or pair,
   duplicate pair, wrong writer, stale head, non-sole commit, invalid enum/nullability, or preclassified candidate
   fails closed and authorizes no action.
2. Any source, test, documentation, dataflow, architecture, README, PR-authority, merge, release, post-merge, or
   Human-only thread action is out of scope.

## C27 Architecture-Document Conflict-Resolution Scenarios

### Scenario 44 — bounded factual three-way integration

Given committed facts at base `37d433e198a955f0710ecd5335666760aa86a20c`, Runtime Cache
`442cc9461854d3909345edb26d1434bfaaa1b86e`, Model Execution
`5f483a05e63c9dc8f3c63b04a63c8adec3ed2e28`, and dev head
`1501f380f20492c71275474f800fdaaffbf0a76a`, and a committed approved C27 Plan-Reviewer receipt, when Implementer
creates the integration subject, then it changes only the five declared architecture-document files and retains both
committed fact sets without making a new architecture decision.

### Scenario 45 — preserved boundaries and evidence ordering

Given the committed five-file integration subject, when the five documents are resolved, then Runtime Cache remains
protocol-only with no Identity direct import, mapper, concrete backend, or runtime lifecycle; Model Execution remains
provider-neutral coordination; and their wiring remains future work. Tester alone writes factual same-subject results
at `plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<c27-integration-subject-40-hex-sha>.json`, and
Implementer commits that unchanged record alone before Independent Reviewer may review. Independent Reviewer then
writes only `plan/loaded-runtime-cache/loaded-runtime-cache.implementation-review-log-<c27-integration-subject-40-hex-sha>.json`
for the same subject and committed passing evidence; Implementer commits it unchanged alone. Only that passing Tester
evidence followed by approved independent review permits Planner Phase 4.5 and then a bounded push updating the
existing draft PR.

## C27 Error / Edge Cases

1. A conflict marker, omitted committed fact, invented architecture or wiring decision, or a modified path outside the
   exact five-file allowlist fails closed.
2. Any PR-thread reply/resolution, approval, merge, release, post-merge, source/test change, or use of uncommitted
   facts is out of scope.

## C28 Eight-Pair Repair and Classification Scenarios

### Scenario 46 — factual historical state alignment

Given the committed C25, C26 and C27 facts, when the C28 candidate is authored, then it updates only the five planning
artifacts to mark those historical routes consistently and does not prefill any C28 candidate, evidence, outcome, reply
or resolution.

### Scenario 47 — bounded RED and green repair

Given a committed approved C28 Plan-Reviewer receipt, when RED tests cover direct `getattr` import/module-cache shapes,
an `importlib` submodule top-level binding, an `IfExp` assignment alias, and readable key token state, then they collect
and fail factually. When green runs, it rejects only those additional static bypasses, preserves prior scanner shapes,
keeps the token opaque and non-readable, and presents the Registry retain channel separately from Retention outcomes in
the truthful dataflow artifact subset.

### Scenario 48 — immutable eight-pair current-head classification

Given committed C28 green passing Tester and approved Reviewer evidence and an actual current PR head, when Independent
Reviewer writes the C28 classification receipt, then its exact eight top-level keys and exactly eight four-field entries
cover only `lfYsH`/`4091265108`, `lfYsK`/`4091265115`, `m8u04`/`4129370926`, `m8u09`/`4129370931`,
`m82WL`/`4129419161`, `m82WS`/`4129419173`, `m9eUV`/`4129677944`, and `m9eUY`/`4129677947`. Candidate planning does
not choose outcomes. Only a committed `REPLY_AND_RESOLVE` entry with a factual non-empty reply may later authorize
that exact thread action.

## C28 Error / Edge Cases

1. Any C28 change outside its declared planning, test, key-module, or truthful dataflow allowlist; recursive/runtime
   AST inspection; token interpretation; or backend/lifecycle/wiring claim fails review.
2. A missing/extra pair or key, wrong SHA/head/writer, stale or non-sole evidence, or any action on a Human-only thread
   fails closed and authorizes no reply, resolution, approval, merge, release or post-merge.

## C29 Three-File Architecture Integration Acceptance

### Scenario 49 — full committed dev tree, bounded manual resolution

Given an independently approved committed C29 candidate receipt, fixed dev
`d6ff74ddf65c615f65eeba252e648784252a2bfd` and already-integrated base `1501f380f20492c71275474f800fdaaffbf0a76a`,
when Implementer integrates dev in feature worktree, then one immutable merge subject records actual prior feature HEAD
first parent and fixed dev second parent, incorporates automatic committed dev tree changes, and limits manual conflict
resolution to `docs/architecture/business-capability/architecture-brief.md`, `docs/architecture/business-capability/index.html`,
`docs/architecture/business-capability/scene.js`. No other manual edits or conflict markers remain. Both feature Runtime
protocol／Model Execution facts and dev Response Reuse fixed-codec／bytes-envelope facts survive without new architecture
or BC wiring decisions; documentation and scene agree. Facts requiring a new decision return human-check.

### Scenario 50 — new immutable same-subject evidence and publish order

Given the committed integration subject, Tester alone records actual scoped verification at
`plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<c29-integration-subject-40-hex-sha>.json`, exact six-key
schema and factual command exit codes per technical-spec C29. Implementer unchanged-sole-commits it. Only committed
passing same-subject evidence permits Independent Reviewer to write
`plan/loaded-runtime-cache/loaded-runtime-cache.implementation-review-log-<c29-integration-subject-40-hex-sha>.json`
with exact seven-key schema, full subject and Tester-commit binding. Implementer later unchanged-sole-commits it.
Only committed approved review permits Phase 4.5 factual alignment → bounded push → actual PR head/mergeability audit.
SHA-bound paths are immutable; future subject/result/verdict facts are never prefilled. Failing evidence or needs-rework
blocks publish; repaired new subject repeats the entire Tester/Reviewer sequence.

### Scenario 51 — factual C28 closure and retained open-thread boundaries

Given live Implementer／Planner verified C28 exact receipt reply IDs `4140433910`, `4140435052`, `4140436064`,
`4140436858`, `4140437667`, `4140438539`, `4140439397`, `4140440128` and all eight threads resolved, C29 aligns
historical tracking without attributing actions to preceding commit `2d204b070cc9701cfdce31940cbfe377403f1894`.
Five Human-only locks (`jnBpk`, `kQ95O`, `kqiZ5`, `lAR8T`, `lfQmF`) stay open; `m-94E`/`4130289778`,
`m-94K`/`4130289786`, `nXkrM`/`4140364926`, `nXrAw`/`4140406331`, `nXrA0`/`4140406337` remain
unclassified/open. C29 assigns no disposition, classification, reply or resolution; original protocol／outcomes／
visualization／follow-ups persist. No PR approval／Human merge／release／post-merge authority.

## C29 Error / Edge Cases

Wrong parent/base, extra manual path, omitted committed fact, invented architecture decision, marker, schema/writer/SHA
mismatch, overwritten evidence, non-sole evidence commit, or reordered Tester/Reviewer fails closed. Automatic fixed-dev
parent changes outside three manual files are valid parent integration, not extra manual scope.

## C30 Current-Head Seven-Pair Classification Acceptance

C29 publish／audit completion 以 audited head `ee2825c785aad152e5785a021acdb68e3056e84d` 記錄。
C30 僅分類 `m-94E`/`4130289778`、`m-94K`/`4130289786`、`nXkrM`/`4140364926`、`nXrAw`/`4140406331`、
`nXrA0`/`4140406337`、`nXzEu`/`4140459575`、`nXzE1`/`4140459585`。
驗收：five-artifact candidate → independent approved SHA-bound standard receipt → sole receipt commit → Planner
C29 S/T/V/head verification → independent exact eight-key/seven-pair classification → separate sole receipt commit。
固定 S `9c6ec737e9a900e2bcd1a02f2a6808bcb91e73aa`、T `31e727d96d4e0843714dca1c7898ac93da9c33ef`、
V `fc12dea6be989aaecfdfc71a86fa1b330256fffe`；exact receipt path/schema/writer 依 technical-spec C30。
TestCase：拒絕 stale head／extra pair／wrong SHA／writer／schema／enum／reply nullability／non-sole／overwrite；
僅 committed `REPLY_AND_RESOLVE` 可 route exact factual reply／resolve，ADDRESS／HUMAN_CHECK 不 resolve。
五個 Human-only locks 與其餘未列 threads 保持 open／ReadOnly，無 implementation／test／architecture 新修改。

## C31 Five-ADDRESS Bounded Repair Acceptance（current route）

### Scenario 52 — paired destructuring, builtin getattr and default bindings

Given approved committed C31 candidate receipt, RED cases in `tests/test_loaded_runtime_cache_bc_independence.py`
collect and fail for missing static behavior. Green binds each simple-name tuple/list destructuring target only to its
matching RHS element, including nested paired forms; ignores attribute targets while retaining sibling local names.
It resolves known builtins alias `getattr(..., '__import__')` for assigned/direct calls and forbidden callable defaults
to the correct positional/keyword-only function parameters. Existing chained/mixed/walrus/conditional/getattr/import
regressions remain intact. Benign callable controls pass. No source execution or starred/arbitrary iterable inference.

### Scenario 53 — callable arguments and truthful future Miss endpoint

Given static forbidden import callable expressions or retained aliases passed as positional/keyword call arguments
(including executor.submit/map), scanner rejects them without executing source. Ordinary callable arguments remain
accepted. Given architecture-brief point 6, scene Miss edge ends at labelled future integration boundary; no edge falsely
lands on Loaded Runtime Cache. Scene and index inline scene agree, preserving independent Runtime/Execution contracts
and future wiring facts without new architecture, mapper or implemented cross-BC handoff.

### Scenario 54 — immutable C31 evidence sequence and five-pair classification

Five-file candidate → independent SHA-bound approved receipt sole commit → test-only RED subject → Tester factual
failing evidence sole commit → distinct three-path green subject → Tester passing evidence sole commit → independent
same-subject approved review sole commit → Planner Phase 4.5 alignment → bounded push/live-head audit → Independent
Reviewer current-head classification → separate sole receipt commit → Planner per-pair routing → Implementer exact
permitted reply/resolve. Full paths, exact three/six/seven/eight-key schemas, actors and no-prefill rules are in
technical-spec C31. Classification covers exactly `m-94K`/`4130289786`, `nXkrM`/`4140364926`,
`nXrA0`/`4140406337`, `nXzEu`/`4140459575`, `nXzE1`/`4140459585`; no future disposition is assumed.
REPLY_AND_RESOLVE requires factual nonempty string reply; ADDRESS/HUMAN_CHECK require null and cannot be resolved.

## C31 Error / Edge Cases

Wrong element-to-target aliasing, attribute binding, lost prior behavior, source execution, extra implementation path,
false cross-BC wiring, stale head, wrong SHA/schema/writer/pair, overwritten/non-sole evidence or actor reordering fail
closed. `nYQqw`/`4140648790` and five Human-only locks excluded/open. No dev writes or Human approval/merge/release.

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

### Scenario 55 — independent three-pair classification

Given fixed committed C31 S/T/V and actual fixed audited PR head, independently reviewed C32 candidate and sole
approved receipt commit precede independent classification at the exact immutable path in technical-spec C32.
Only the three listed pairs appear once each; exact eight-key object/four-key entries, enums and nullability apply.
Sole classification commit precedes per-pair routing/actions. ADDRESS/HUMAN_CHECK cannot be resolved.
Wrong head/binding/path/schema/writer/order/overwrite fails closed; no implementation or prechosen outcome.

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

## C48 Current-Head Twelve-Pair Human-Disposition Classification（authoritative current routing）

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
