# Workflow Concurrency Supersession — Requirements

## Human override and authority

本文件依 Human 的明確指示建立：不得讓既有治理 topic 對不相衝突的新功能 topic
造成全域阻擋。此指示只授權本 `workflow-concurrency-supersession` bootstrap topic
開始規劃；它不把任何聊天內容視為 Git evidence，也不追認、取消或補建 R23。

## Required outcome

- 將 repository workflow 改為 topic-local routing：每個 topic 只由自己的 committed
  plan、step、Plan-Reviewer receipt、implementation subject、Tester evidence 與
  independent Reviewer evidence 決定其 phase 與 gate。
- 多個互不衝突 topic 可在不同 branch/worktree 並行至各自的 independent Reviewer。
- path allowlist 或 evidence subject 衝突必須交回 Human `human-check`；不得自動選擇
  贏家、合併 evidence 或擴大 scope。
- B6R13/R23 保持既有 subject-local obligations。未提交的 R23 聊天結果無效，不補建，且
  B6R13 的矛盾或 pending state 只阻擋 B6R13。
- 每個 topic 的 publish 仍需同 subject 的 passing Tester evidence、independent
  Reviewer approval、Planner Phase 4.5 alignment 與既有 human authorization。可同時有
  多個 draft PR；僅 Human 可 merge、release、tag 或 post-merge。

## Boundaries

- 本 topic 不規劃或建立 `src-implementation` 的 folders、命名、模組責任或產品行為。
- 本 topic 不執行 R23、S17、任何舊治理 topic 的 repair，亦不修改 frozen provenance。
- 不可更動 stable-library surface：`README.md`、`VERSION` 與 release material 都不在 scope。

## Acceptance intent

完成後，已提交且 approved 的 `workflow-concurrency-supersession` 契約會讓 Planner
以 topic-local evidence routing；一個缺失、未提交或 needs-rework 的 B6R13/R23 record 不得
再阻擋另一個已具備自身 committed planning evidence、且無衝突的新 topic。
