# Observer / Dispatcher Governance

## Goal / Outcome

以 B6R12 routing-receipt correction 收斂唯一可驗證路徑：`B6R12 -> R22 -> S16 -> T16 -> V16 -> Q16 -> thread-classification -> human-check`。本 topic 是 non-stable、review-ready-only；停在 Human boundary。

## Scope

- **In Scope:** B6R12 exact-five planning baseline、R22 independent review、已宣告的 S16 單一 test-path、保留的 B6R10 T16/V16/Q16 evidence schemas 與 passed Q16 後的 independent classification。
- **Out Of Scope:** B6R11/R21、B6R10/R20、所有早期 provenance、legacy migration、step-creator、產品或架構工作、unlisted paths、thread resolve、merge、release、post-merge。
- **ReadOnly:** `AGENTS.md`、README、VERSION、`.github/**`、B6R11/R21、B6R10/R20 與所有 earlier artifacts。
- **Written / Modify:** 僅 B6R12 admission 的五個 declared planning paths；No path is Deleted。

## Locked Decisions

- Current correction 是 `observer-dispatcher-governance/high/b6r12`，state `R22_REVIEW_PENDING`；只有此路徑可 routing。
- B6R11 admission `995c5a8` 是 frozen predecessor receipt；absent R21 只屬 nonrouting provenance，不能 authorize S16。R20 維持 `FROZEN_INVALID_NOT_ROUTING`。
- B6R12/R22 都是 non-subject。S16 是唯一 implementation subject，完整 diff 僅可改 `tests/test_observer_dispatcher_governance_contract.py`；direct imports 必須保留，禁止 `importlib`、`__import__`、`sys.modules` substitution。
- B6R10 已宣告的 S16/T16/V16/Q16 paths、exact schemas、linear topology 與 Q16 actual full-triple/classification-only boundary 原樣保留；B6R12 不重寫其 schema。
- B6R12 admission 為 non-merge first-parent exact-five；pre-admission 不含 B6R12/R22 commit、tree、blob、HEAD 或 outcome。只有 independently committed approved R22 產生 active candidate，effective state `R22_COMPLETE_S16_NEXT`，next phase S16。

## Boundaries / Exclusions

Observer 只 dispatch/aggregate；Planner 唯一決定 candidate、phase、gate 與 next role。Plan-Creator 只寫 declared planning paths；Plan-Reviewer 只寫 R22；Implementer 只做 approved bounded work；Tester 與 Reviewer 只寫 declared evidence。Reviewer 不是 Human PR reviewer。不得 widen allowlist、resolve threads、merge、release 或 post-merge。

## Status / Allowed Transitions

**Current:** `R22_REVIEW_PENDING`。

R22 必須在 committed B6R12 clean checkout 驗證 exact-five blobs/admission 與 frozen B6R11/R21、B6R10/R20 receipt。只有 independently committed R22 且 `verdict: approved` 時，R22 才可令 `candidate.active:true`、`blocking_issues:[]`，並令 route authorization 精確為 `R22_COMPLETE_S16_NEXT` / `S16`；needs-rework 必須令 candidate inactive 且 route authorization `null`。S16 需要 committed approved R22；T16 需要 same-S16 full-suite passing；V16 需要 committed passing T16；Q16 需要 committed V16。failure 回 Planner；human actions 停在 Human boundary。

## Artifact Paths

| Artifact | Exact path | Write owner | Decision authority | Role |
| --- | --- | --- | --- | --- |
| Parent plan | `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md` | Plan-Creator | Planner | B6R12 current truth |
| Parent spec | `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md` | Plan-Creator | Planner | B6R12 acceptance |
| Parent step | `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md` | Plan-Creator | Planner | B6R12 tracker |
| B6R12 plan | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r12-plan.md` | Plan-Creator | Planner | baseline delta |
| B6R12 step | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r12-step.md` | Plan-Creator | Planner | baseline tracker |
| R22 review | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r12-review-log.md` | Plan-Reviewer | Plan-Reviewer verdict | pre-S16 gate |
| S16 subject | `tests/test_observer_dispatcher_governance_contract.py` | Implementer | Planner | sole subject |
| T16 evidence | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r10-tester-evidence.md` | Tester | factual test result | retained descendant |
| V16 evidence | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r10-implementation-review-log.md` | Reviewer | reviewer verdict | retained descendant |
| Q16 evidence | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r10-actual-gate-evidence.md` | Reviewer | actual-gate result | classification gate |

## Implementation Steps

1. Plan-Creator writes exactly the five B6R12 planning paths; Independent Implementer creates the exact non-merge first-parent admission.
2. Independent Plan-Reviewer reviews committed B6R12 and writes R22, including predecessor receipt verification and strict five-record schema; Independent Implementer commits an unchanged approved R22.
3. Planner dispatches retained S16 only when committed R22 is approved and `R22_COMPLETE_S16_NEXT`.
4. Tester writes retained T16 after full suite; Reviewer writes retained V16 after committed passing T16; Reviewer executes retained Q16 only after V16 commit.
5. After active passed Q16, independent Reviewer classifies threads; stop at human-check.

## Validation / Acceptance Checks

- B6R12 admission is non-merge, first-parent and exactly five declared paths in lexical name-status order: B6R12 plan, B6R12 step, parent plan, parent spec, parent step.
- R22 的 full Draft 2020-12 JSON Schema machine-enforces actual `reviewed_artifacts` array 的五筆 ordered path/blob records，及 `first_parent_admission.name_status` 的同一 lexical exact-five；兩者都使用 `prefixItems`、`minItems:5`、`maxItems:5` 與 `items:false`。every blob, candidate commit/tree and first-parent SHA is lowercase hexadecimal with exactly 40 characters.
- R22 records candidate commit/tree, the exact-five first-parent admission, frozen B6R11 absent-R21 and B6R10/R20 receipt, Copilot triage, verdict and blockers.
- R20 remains `FROZEN_INVALID_NOT_ROUTING`; no S16 execution occurs before a committed approved R22.
- Retained B6R10 S16/T16/V16/Q16 paths, schemas and direct-import ban remain unmodified; Q16 never authorizes resolve, PR approval or merge.

## R22 Routing-Receipt Schema

R22 is written only from the committed B6R12 checkout and records post-admission facts. The B6R12 correction plan contains its executable full Draft 2020-12 JSON Schema; that schema—not a schema-shaped R22 example—is the authority. Its single JSON evidence object has
`schema_version`, `correction_id`, `review_kind`, `candidate`, `reviewed_artifacts`, `first_parent_admission`,
`predecessor_receipt_verification`, `review_basis`, `copilot_feedback_triage`, `verdict`, `blocking_issues`,
`route_authorization`, and `timestamp`. Its actual `reviewed_artifacts` value is constrained in this exact order—`A`
B6R12 plan, `A` B6R12 step, `M` parent plan, `M` parent spec, `M` parent step—with `minItems:5`, `maxItems:5`, and
`items:false`; every path is literal and every `blob_sha` matches `^[0-9a-f]{40}$`. `first_parent_admission.name_status`
uses the identical lexical five-entry `prefixItems` contract. The reviewer must fail closed unless the two lists and
the first-parent lexical name-status diff are identical.
`first_parent_admission` records lowercase 40-hex `commit_sha`, `tree_sha`, and `parent_sha`, non-merge result and five
name-status entries. `predecessor_receipt_verification` records B6R11 `995c5a8`, absent R21 as nonrouting and R20 as
`FROZEN_INVALID_NOT_ROUTING`. `approved` requires active candidate, empty blockers and exact
`R22_COMPLETE_S16_NEXT` / `S16` route; `needs-rework` requires inactive candidate, one-or-more blockers and null route.
Only independently committed unchanged approved R22 may activate S16.

## Reviewer Handoff

~~~json
{"current_route":"B6R12->R22->S16->T16->V16->Q16","correction_id":"observer-dispatcher-governance/high/b6r12","plan_review_path":"plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r12-review-log.md","implementation_subject":"S16 only","range":"S16..V16","verdict":"approved|needs-rework"}
~~~

## Post-merge / release actions

No release action is authorized. Stop at the Human boundary.

## Open Questions / Unresolved Items

step-creator remains deferred. B6R11/R21, B6R10/R20 and all earlier records are frozen nonrouting provenance.
