# Agent handoff workflow

## Purpose

定義本 repository 的 repo-visible topic workflow、角色權責、status transition 與
human boundary。本文件不取代 `AGENTS.md`、`plan/topic-plan-contract.md` 或個別
topic plan。

## Authority and source of truth

Authority ordering 為：

1. `AGENTS.md`：repo governance 與 Observer boundary。
2. 本文件：workflow phase、role ownership、stop point 與 status transition。
3. `plan/topic-plan-contract.md`：topic-plan structure、evidence 與 preflight。
4. `plan/<topic>/<topic>.plan.md`：單一 topic 的 locked execution contract。
5. `plan/<topic>/<topic>.step.md`：該 topic 當前 stage / next action truth。
6. `plan/<topic>/<topic>.review-log.md`：Plan-Reviewer / Reviewer 的已記錄 verdict
   truth；不取代 plan 或 step。僅當個別已授權 replan 明定 exact special evidence path
   時，該 path 才在該 replan gate 內作 routing evidence；它不會一般化取代 review log。

`GOAL.md` 只描述 repository mission；chat、branch、summary 與
`.github/agents/**` 不可作 active-topic、phase 或 routing authority。
`.github/agents/**` 是 frozen provenance，不得修改，也不可作 runtime / routing
dependency。

## Roles

| Role | May do | Must not do |
| --- | --- | --- |
| Observer / Dispatcher | 唯讀盤點；派遣一個合適角色；彙整 `可直接前進`、`needs-rework`、`blocked`、`human-check` | 實作、改檔、commit、push、PR、release、手算 gate、comment triage 或重解 locked decision |
| Planner | candidate / phase / gate / next-role preflight；Phase 4.5 contract alignment；bounded repair routing | 改 planning artifact、實作、review own work、git publish 或 release |
| Plan-Creator | 建立或 bounded repair plan、spec、step 與 shared planning contract | commit、Plan-Reviewer verdict、implementation、publish |
| Plan-Reviewer | 獨立審核 planning artifacts；依 shared contract 寫入 exact review-log path，或僅在 human-authorized current-topic replan 已明定時寫入其 exact special evidence path | 修改被審 plan/spec/step、commit、implementation 或 publish |
| Implementer | 在 approved scope 內實作；在既有 human authorization 下 commit by topic、push、開 draft PR | 自行核准、處理 PR comments、merge、release 或 post-merge |
| Tester | 執行 declared checks 並回報證據 | 改 tests 以迴避既有行為、核准或 publish |
| Reviewer | 獨立審核 implementation、處理 PR comments 的 classification / review routing、寫入 reviewer verdict | author own implementation、commit、push、merge、release 或 post-merge |
| Human | 授權 commit、push、draft PR；執行 human review、merge、post-merge、release、tagging 與 final summary | 將 merge、post-merge、release、tagging 或 final-summary action 以重新授權委派給任何非 Human actor |

所有 planner、creator、reviewer、implementer gate 必須由獨立 actor 真實執行；不得以
同一 actor 宣稱多重 gate 已完成。

## Planning baseline and preflight

1. Plan-Creator 建立或修正 topic plan、spec、step，以及 topic 必要的 shared planning
   contract 變更；它不得 commit。
2. 在 human 已對該 topic 授權 commit 的前提下，獨立 Implementer 建立 **planning
   artifact commit**。該 commit 必須包含 topic plan、spec、step 與此 topic 所需的
   workflow / shared-contract 變更；此 commit 使 topic 成為 `planned` 的
   repo-visible execution contract。它不代表 implementation approval。
3. Plan-Reviewer 對該已提交 baseline 做獨立 review，並在
   `plan/<topic>/<topic>.review-log.md` 追加一筆固定 reviewer-handoff JSON record。
   該 record 的 `verdict` 為 `approved` 時，才可作為 planning approval evidence。
4. 在 Planner preflight 前，獨立 Implementer 必須在既有 human topic authorization
   下提交 review-log-only evidence commit；此 commit 不得夾帶 implementation diff。
5. Planner 的 preflight **只讀取** candidate 的 plan、required step tracker 與
   review log；它不使用 chat、branch、summary、`GOAL.md` 或 frozen provenance
   補推 task。

planning approval evidence 固定為：

- exact path `plan/<topic>/<topic>.review-log.md` 存在；
- 最後一筆 JSON record 完整符合 shared `Reviewer Handoff` shape，且
  `"verdict": "approved"`；
- 該 record 由 Plan-Reviewer 在完成獨立 planning review 時寫入。

topic plan 不得包含、要求或依賴任何 self-authored approval marker。缺少 planning
artifact commit、required step 或上述 evidence 時，implementation 不可開始。

### Human-authorized current-topic replan exception

一般 planning baseline 與 future / new review-log NDJSON 規則維持不變。唯一已授權的
例外是 current topic `observer-dispatcher-governance` 的目前 `needs-rework` replan：
在任何 replan commit 前，independent Plan-Reviewer 必須且只能寫入
`plan/observer-dispatcher-governance/observer-dispatcher-governance.recovery-planning-review-evidence.md`。
該單一 machine-JSON record 是此次 latest replan 的 routing evidence；它必須依 shared
`Reviewer Handoff` schema 記錄 replan 的五個 reviewed artifact revisions / head。只有
`"verdict": "approved"` 才允許獨立 Implementer 建立唯一的 planning-evidence commit；
該 commit 固化五個 replan artifacts 與 recovery planning-review record，並在 commit 建立
後成為 immutable `implementation_subject_sha`。

此 subject 之後只允許兩個線性、evidence-only commits：先由 Tester 寫入 declared
recovery Tester evidence，再由 Reviewer 寫入 declared recovery implementation-review
record。兩個 record 必須 attest 相同 `implementation_subject_sha`，Reviewer 必須 reference
passing Tester evidence。最終 descendant 無 merge，且
`git diff --name-status <implementation_subject_sha>..HEAD` 恰好只列出兩個 declared
recovery implementation-evidence paths；不得有其他 path。這個狹義 recovery sequence
不授權 push、PR thread action、merge、post-merge、release、tagging 或 final summary。

此 exception 是 Human-authorized、current-topic、latest-replan-only 的 gate，不遷移、
改寫、重讀或一般化任何 existing legacy `review-log.md`。`df137326363cce4f68e43124156731a50cf29a03`
中的 planning-review、Tester 與 implementation-review evidence 均保持 frozen, superseded
provenance，並非此 replan 的 routing authority。`needs-rework` evidence 維持 topic
`needs-rework`；後續 bounded replan 必須再有 Human 明示授權。special evidence 不改變
PR #1 Ready 的 `pr-open` external fact，也不構成 merge、implementation approval 或
same-subject Tester / Reviewer completion。

Planner preflight 的 routing 為：無 candidate 為 `blocked`；多 candidate 或 plan / step
指向不同 topic 為 `human-check`；同 topic 的 status 或 scope conflict 為 `blocked`，除非
Planner 明定 Plan-Creator 可進行 bounded repair。

## Status model

下列 canonical transitions 保持不變；`planned` 的前提是上節定義的 planning artifact
commit 已存在。plan review 是從 `planned` 進入 creator work 前的 required evidence gate，
不另創 status。

| Status | Meaning | Owner | Allowed next |
| --- | --- | --- | --- |
| `planned` | Topic planning artifact commit 已存在，等待 required planning evidence / execution preflight | Plan-Creator -> Plan-Reviewer -> Planner | `creator-in-progress` |
| `creator-in-progress` | Implementer 正在依 locked plan 完成 bounded work | Implementer | `review-ready` |
| `review-ready` | Implementer 已完成最新 draft 並交 reviewer | Implementer | `reviewer-in-progress` |
| `reviewer-in-progress` | Reviewer 正在審核 implementation 或 comment routing | Reviewer | `approved`, `needs-rework` |
| `needs-rework` | Reviewer 發現 blocking issue 並退回 work | Reviewer -> Planner | `creator-in-progress` |
| `approved` | Reviewer 接受 latest draft，等待 Planner Phase 4.5 | Reviewer -> Planner | `creator-in-progress`, `publish-in-progress` |
| `publish-in-progress` | required evidence、validation 與 human authorization 齊備；Implementer commit / push / 開 draft PR | Implementer | `pr-open`, `merged` |
| `pr-open` | draft PR 等待 human review；Reviewer 處理 comments 的 classification / routing | Human / Reviewer | `needs-rework`, `merged` |
| `merged` | Human 已 merge；post-merge 與 optional release 皆為 human boundary | Human | `released`, terminal |
| `released` | Human 已完成版本與 tag action（若 topic 要求） | Human | terminal |

`merged` 對無 release topic 是 terminal；有 release action 時只有 human 能從
`merged` 推進至 `released`。

## Phases and gates

| Phase | Trigger / required input | Output | Owner |
| --- | --- | --- | --- |
| 1. Plan the topic | scope 已鎖定；Plan-Creator output | planning artifact commit 後為 `planned` | Plan-Creator -> Implementer（human 授權 commit） |
| 2. Prepare feature worktree | `planned` baseline、approved planning evidence、Planner preflight | feature branch / worktree ready | Planner -> Implementer |
| 3. Bounded implementation | approved plan、allowed path set | `review-ready` implementation | Implementer |
| 4. Independent review | review-ready output、Tester evidence | `approved` 或 `needs-rework` JSON verdict | Reviewer |
| 4.5 Planner contract alignment | independent `approved` verdict、locked plan、artifact paths | `creator-in-progress` 或 `publish-in-progress` | Planner |
| 5. Stable library handling | topic stable-library metadata（若有） | stage / defer / skip decision | Planner；release action 停在 Human |
| 6. Commit, push, draft PR | Planner permits publish、validation evidence、existing human authorization | `pr-open` | Implementer |
| 7-8. PR review loop | human review comments / failed checks | Reviewer routes `needs-rework`；human 決定 merge | Reviewer -> Human |
| 9. Post-merge | human confirms merged | local sync / summary handoff（若 required） | Human |
| 10. Release | topic declares release action | `released` 或 terminal `merged` | Human |

Phase 4.5 是 Planner 專責。它只可依 plan、latest verdict、locked decisions 與 artifact
paths 作 contract alignment：有 drift 則回 `creator-in-progress` 並明定 bounded repair；無
drift 才可進入 `publish-in-progress`。Observer 不得執行或推測 Phase 4.5。

## Rework and comment routing

- Reviewer 的 `needs-rework` 必須說明 blocking issue 與回修 target；Planner 決定是否
  屬 current-plan bounded repair 或需 Plan-Creator 修正 contract。
- draft PR comments、check failures 與 review feedback 一律先交 Reviewer；Reviewer 可
  route to `needs-rework`，不得由 Observer 或 Implementer 自行 triage。
- scope drift、contract drift 或 workflow drift 一律保守收斂：停止 publish，交 Planner，
  必要時由 Plan-Creator bounded repair 後重新走 required planning review；若已明定
  human-authorized special replan evidence path，該次 replan 依其 exact path 與 schema
  進入 Plan-Reviewer gate，不得推廣為 generic migration。

## Human boundaries

- commit、push、draft PR 只在既有明示 human authorization、required evidence、Tester
  evidence 及 Planner publish route 都存在時由 Implementer 執行。
- draft PR 開啟後即停於 human review boundary；Ready 只表示可供 Human review，絕不
  等同 merge approval 或已 merge；不得自動 merge、release、post-merge sync 或寫
  final summary。
- merge、post-merge、release、tagging 與 final summary 是不可委派的 Human-only
  action。重新授權只可涵蓋本節第一點的 commit、push、draft PR，絕不會把前述
  Human-only action 交給任何非 Human actor；Observer 不得自行恢復或輪詢。
