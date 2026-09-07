# Workflow Concurrency Supersession — Technical Specification

## Analysis-layer routing

`requirements.md` 是業務與範圍 guardrail；本 technical specification 是 execution-facing
source of truth。Human 已明確 override，授權以對話中的 supersession direction 建立本兩份
analysis artifacts；此 override 不使聊天內容成為任何 topic 的 Git routing evidence。

## Contract model

1. Planner 在 bootstrap 完成後，從各 topic 自己已提交且明確 approved 的 planning evidence
   判定 candidate、phase、gate 與一個 allowlisted next role。它不得以另一 topic 的 pending、
   missing、stale 或 `needs-rework` evidence 阻擋此 topic。
2. 每個 topic 的 committed plan、step、Plan-Reviewer receipt、implementation subject、Tester
   evidence 與 independent Reviewer evidence 必須同 topic、同 immutable subject；不可跨 topic
   轉用、覆蓋或由聊天、branch、summary 或 frozen provenance 補推。
3. 多 topic 只可在隔離 branch/worktree 並行。任兩 active topic 的 declared write paths 重疊，
   或其 candidate/evidence/subject 指向衝突時，Planner 回報 `human-check`，不派遣 writer。
4. subject-local lifecycle 保持：Plan-Creator -> independent Plan-Reviewer -> Implementer ->
   Tester -> independent Reviewer -> Planner Phase 4.5 alignment -> Implementer bounded publish ->
   `pr-open` -> Human boundary。Tester 與 Reviewer evidence 都必須對同一 immutable subject。
5. `publish-in-progress` 只能成為 `pr-open`。human authorization 僅允許該 topic 的 bounded
   commit、push、draft PR；不得授權 merge、release、tag、post-merge 或其他 topic 的動作。

## Bootstrap transition

本 topic 是唯一 bootstrap exception。它可以在 B6R13/R23 未完成時建立並提交本 topic 的
planning artifacts，然後交由 independent Plan-Reviewer 審核。本 exception 的效力只限建立
新契約；不改變 B6R13/R23 的 historical 或 subject-local status，也不授權任何
`src-implementation` planning 或 implementation。

獨立審核 approved 並完成此 topic 所需 committed receipt 後，Planner 必須重新 preflight，
再決定是否可派 Implementer 更新下列三個 workflow contract files。contract update 只可修改
`AGENTS.md`、`plan/agent-handoff-workflow.md`、`plan/topic-plan-contract.md`；不含任何產品路徑。

## Rejection and failure behavior

- 缺少 topic-local committed required evidence：僅該 topic `blocked`。
- 同一 topic 的 plan、step、receipt 或 subject 自相矛盾：該 topic `blocked`；僅 Planner
  可宣告 bounded Plan-Creator repair。
- 多 candidate、跨 topic evidence，或 declared paths / subject conflict：`human-check`。
- 未取得 same-subject Tester/Reviewer/Planner/human requirements：不得 publish。
