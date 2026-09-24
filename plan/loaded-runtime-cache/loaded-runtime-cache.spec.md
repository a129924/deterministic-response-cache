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
