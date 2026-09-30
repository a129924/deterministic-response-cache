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

## C34 Current-Head Three-Pair Classification Successor（authoritative current routing）

### Goal / Outcome / Scope

Current：`c34-planning-draft`。Goal／In-Scope：僅獨立分類三個新 pairs
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
