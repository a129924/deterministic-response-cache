# Observer / Dispatcher Governance Specification

## Acceptance Criteria

1. `GOAL.md` 只陳述 provider-agnostic Python response-reuse library 的長期
   mission 與成功方向，且不含 active topic、current phase、workflow status、
   dispatcher routing 或 release state。
2. `AGENTS.md` 將 Observer / Dispatcher 限為唯讀盤點、單一專責派遣、結果彙整與
   triage，並禁止它實作、改檔、git publish、PR / release、gate 推測、review-comment
   handling 及 locked-decision reinterpretation。
3. workflow 與 shared topic-plan contract 將 Planner 設為 candidate、phase、gate
   和 next-role 判定 authority；active routing 僅接受 planning artifact commit 後的
   plan、required step tracker，以及 Plan-Reviewer 寫入 review log 最後一筆
   `"verdict": "approved"` JSON record，且 plan 無 self-authored approval marker。
4. `.github/agents/**` 維持 frozen provenance，沒有 diff，且不被視為 runtime 或
   routing dependency。
5. 既有測試保留 direct import、fixture、mock 和 assertion 行為；本 topic 不修改
   `tests/**`，也不以 `importlib`、`__import__` 或 `sys.modules` 取代 direct import。
6. 所有實際 diff 僅位於 plan 的 `Written` 或 `Modify` exact paths；此 topic 不影響
   stable-library surfaces、README、VERSION 或 release。commit / push / draft PR 僅由
   Implementer 在 required evidence 與既有 human authorization 下執行；Reviewer 處理
   PR comment routing，merge / release / post-merge 為 human boundary。

## Behavioral Scenarios

### Scenario 1: 唯一有效 candidate 可派遣

- **Given**: 獨立 Implementer 已建立 planning artifact commit；Planner 找到唯一
  candidate，其 plan、required step tracker 與 review log 都可讀，且 review log 最後
  一筆 NDJSON record 是 Plan-Reviewer 寫入的 `"verdict": "approved"`。
- **When**: Observer 取得 Planner 的 phase / gate / next-role 判定。
- **Then**: Observer 只派遣該單一角色，彙整 bounded result，並依結果回報可前進、
  `needs-rework`、`blocked` 或 `human-check`。

### Scenario 2: candidate 不足或衝突

- **Given**: 沒有 candidate、存在多個 candidate、plan 與 step 指向不同 topic，或同
  topic 的 state / scope 相互矛盾。
- **When**: Planner 判定 routing readiness。
- **Then**: 無 candidate 為 `blocked`；多 candidate 或 topic 不一致為 `human-check`；
  state / scope 矛盾為 `blocked`，除非 Planner 明定 Plan-Creator 可進行 bounded repair。

### Scenario 3: import preservation

- **Given**: `tests/test_package_import.py` 已以直接 import 驗證 package import。
- **When**: Implementer 完成本 topic bounded change。
- **Then**: 測試檔零 diff，且沒有 `importlib`、`__import__` 或 `sys.modules` 被用來
  取代該 direct-import regression 行為。

### Scenario 4: draft PR 後停止

- **Given**: independent review 與 Planner contract alignment 均通過，且使用者已
  明示授權 commit、push 和開啟 draft PR。
- **When**: draft PR 已建立。
- **Then**: topic 停在 human review boundary；沒有 actor 自行 merge、release、
  post-merge sync 或宣告 human check 完成。

### Scenario 5: 未提交 baseline 不可開始

- **Given**: Plan-Creator 已寫入 plan、spec、step 或 shared planning contract，但
  尚未由獨立 Implementer 建立 planning artifact commit。
- **When**: Planner 準備進行 execution preflight。
- **Then**: topic 尚未為 `planned` repo-visible contract；不得進入 implementation。
  planning artifact commit 不表示 implementation approval；仍須 Plan-Reviewer
  之後寫入 latest `approved` review-log record。

## Error / Edge Cases

- 缺少 planning artifact commit、required step tracker 或 latest approved review-log
  evidence 時，不得由 branch、chat、summary、`GOAL.md` 或 frozen provenance 補推；
  回報 `blocked`。
- 若新增的測試需求本身是 import 行為，只有 approved topic 明定時才可新增專用測試；
  原有 regression test 仍必須保持 direct import。
- 如果 implementation 需要 `Written` / `Modify` 以外檔案，先停止，由 Planner 決定
  是否需 bounded plan repair；不得自行擴張。
