# Loaded Runtime Cache Specification

## Acceptance Criteria

1. Loaded Runtime Cache 有自己的 nominal immutable opaque `RuntimeReuseKey`；其 responsibility 是 local
   reusable-runtime locator，且不等同或引用 `ModelIdentity`。
2. `RuntimeRegistry[RuntimeT]` 的 `lookup(key: RuntimeReuseKey) -> RuntimeT | None` 與
   `retain(key: RuntimeReuseKey, runtime: RuntimeT) -> None` 是 synchronous Protocol contract。
3. `RuntimeRetention[RuntimeT].retain(key, runtime)` 回傳 `Retained[RuntimeT] | NotRetained[RuntimeT]`；兩者都
   保留同一 runtime instance。
4. `runtime_registry_port.py` 擁有 `RuntimeRegistryLookupUnavailable` expected signal；Registry 原樣 raise；
   hit／missing 仍只有 `RuntimeT | None`。`lookup_outcome.py` 擁有 `Available`／`Missing`／`Unavailable`
   semantic contracts；本 topic 沒有 signal-to-`Unavailable()` mapper。unexpected exceptions 原樣 propagate。
5. 新增 Python modules 位於 locked three-level taxonomy，沒有 child `__init__.py`、root re-export、facade、
   dynamic import、`sys.modules` substitution 或 generic module names。
6. Identity BC 與 Loaded Runtime Cache 無任一方向 direct module import、re-export 或 duplicate type。
7. Architecture authority 和 Archify dataflow 只宣告 protocol capability；ACL mapping、backend、lifecycle,
   Model Execution、Provider Adapter 均為 external／future／out of scope。

## Behavioral Scenarios

### Scenario 1 — local key handoff

Given local `RuntimeReuseKey` fixture，When typed Registry／Retention fake 接收 lookup／retain，Then 接收同一
key instance，且 test 不檢查 token 或內部欄位。

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
保持不變。

### Scenario 6 — visualization evidence

Given frozen Archify JSON candidate，When validate、deliver、`visual-check --repo-root` 依序執行，Then validate
為 showcase 9/9、0 errors、0 warnings，四個 desktop viewports containment 均通過；否則保留 truthful failure／skipped
receipt 並停止 gate。圖使用 `backend` visual type 時必須以 contract-only label 和「僅 Protocol；無 concrete backend、
DI、runtime lifecycle」說明消除實作暗示。

## Error / Edge Cases

1. **Unexpected exception:** Given a Registry fake raises an exception other than
   `RuntimeRegistryLookupUnavailable`, When the port contract is used, Then the exception propagates unchanged; it is
   not classified as `None`, `Missing()` or `Unavailable()`.
2. **Expected operational failure:** Given Registry raises `RuntimeRegistryLookupUnavailable`, When a direct-module
   contract test invokes lookup, Then that exact signal remains distinguishable from a `None` miss and the separate
   `Unavailable()` outcome type; no signal-to-outcome consumer is implemented.
3. **Retention failure:** Given a `NotRetained` outcome, When the caller receives it, Then it retains the exact input
   runtime instance for caller-side handling.
4. **Import boundary:** Given either BC attempts a direct import of the other, re-export, duplicate semantic type, or
   dynamic-import workaround, When the BC-independence regression runs, Then it fails.
5. **Visual gate failure:** Given Archify validate, deliver, or visual-check is non-zero or visual-check is skipped,
   When evidence is recorded, Then the failure／skipped result is retained truthfully and the delivery gate stops.
