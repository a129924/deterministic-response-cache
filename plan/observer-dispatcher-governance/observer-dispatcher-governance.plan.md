# Observer / Dispatcher Governance

## Goal / Outcome

以 B6R13 runtime/wrapper correction 收斂唯一可驗證路徑：`B6R13 -> R23 -> S17 -> T17 -> V17 -> Q17 -> thread-classification -> comment-resolve -> human-check`。本 topic 是 non-stable、review-ready-only；停在 Human boundary。

## Scope

- **In Scope:** B6R13 exact-eight planning baseline、R23 independent review、已宣告 S17 exact-fourteen runtime/template/test subject、T17/V17/Q17 evidence 與 passed Q17 後的 independent classification / exact-thread bounded comment-resolve。
- **Out Of Scope:** B6R12/R22/S16-Q16、B6R10/R20、所有早期 provenance、legacy migration、step-creator、產品或架構工作、unlisted paths、merge、release、post-merge。
- **ReadOnly:** README、VERSION、`.github/**`、all frozen evidence/provenance；S17 以外不得修改 runtime/skill/template surfaces。
- **Written / Modify:** B6R13 exact-eight planning paths；S17 只可修改 declared exact-fourteen allowlist；T17/V17/Q17 與 R23 只可寫 declared receipts。No path is Deleted。

## Locked Decisions

- Current correction 是 `observer-dispatcher-governance/high/b6r13`，state `R23_REVIEW_PENDING`；只有此路徑可 routing。B6R12/R22/S16-Q16、B6R10/R20 與 earlier route/evidence 均 frozen nonrouting provenance。
- B6R13/R23 都是 non-subject。B6R13 admission 為 non-merge first-parent exact-eight，pre-admission 不含 B6R13/R23 commit、tree、blob、HEAD 或 outcome。只有 independently committed approved R23 產生 active candidate，effective state `R23_COMPLETE_S17_NEXT`，next phase S17。
- S17 是唯一 implementation subject，完整 diff 僅可改 declared exact-fourteen allowlist；direct imports 必須保留，禁止 `importlib`、`__import__`、`sys.modules` substitution。Planner bootstraps exactly once and must not select Planner as next role; Plan-Creator is only planning writer; Tester is factual actual-exit-code evidence; Reviewer consumes same-subject passing Tester evidence; Explorer is bounded read-only; Implementer is bounded and never merges.
- T17/V17/Q17 使用 fresh B6R13 evidence paths、linear topology 與 actual full triple. Q17 only authorizes classification; only an independent classification can permit an exact addressed-and-resolvable thread comment/resolve by Implementer.

## Boundaries / Exclusions

Observer 只 dispatch/aggregate；Planner 唯一決定 candidate、phase、gate 與 one non-Planner next role。Plan-Creator 只寫 declared planning paths；Plan-Reviewer 只寫 R23；Implementer 只做 approved bounded work；Tester 與 Reviewer 只寫 declared evidence。Reviewer 不是 Human PR reviewer。不得 widen allowlist、directly resolve threads、merge、release 或 post-merge。

## Status / Allowed Transitions

**Current:** `R23_REVIEW_PENDING`。

R23 必須在 committed B6R13 clean checkout 驗證 exact-eight blobs/admission 與 frozen B6R12/R22/S16-Q16 receipt。只有 independently committed R23 且 `verdict: approved` 時，R23 才可令 `candidate.active:true`、`blocking_issues:[]`，並令 route authorization 精確為 `R23_COMPLETE_S17_NEXT` / `S17`；needs-rework 必須令 candidate inactive 且 route authorization `null`。S17 需要 committed approved R23；T17 需要 same-S17 factual execution；V17 需要 committed passing T17；Q17 需要 committed V17。failure 回 Planner；human actions 停在 Human boundary。

## Artifact Paths

| Artifact | Exact path | Write owner | Decision authority | Role |
| --- | --- | --- | --- | --- |
| Parent plan | `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md` | Plan-Creator | Planner | B6R13 current truth |
| Parent spec | `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md` | Plan-Creator | Planner | B6R13 acceptance |
| Parent step | `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md` | Plan-Creator | Planner | B6R13 tracker |
| B6R13 plan | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r13-plan.md` | Plan-Creator | Planner | baseline delta |
| B6R13 step | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r13-step.md` | Plan-Creator | Planner | baseline tracker |
| R23 review | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r13-review-log.md` | Plan-Reviewer | Plan-Reviewer verdict | pre-S17 gate |
| S17 subject | fourteen paths named in B6R13 correction plan | Implementer | Planner | sole subject |
| T17 evidence | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r13-tester-evidence.md` | Tester | factual test result | same-S17 descendant |
| V17 evidence | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r13-implementation-review-log.md` | Reviewer | reviewer verdict | same-S17 descendant |
| Q17 evidence | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r13-actual-gate-evidence.md` | Reviewer | actual-gate result | classification-only gate |

## Implementation Steps

1. Plan-Creator writes exactly the eight B6R13 planning paths; Independent Implementer creates the exact non-merge first-parent admission.
2. Independent Plan-Reviewer reviews committed B6R13 and writes R23, including predecessor receipt verification and strict eight-record schema; Independent Implementer commits an unchanged approved R23.
3. Planner dispatches S17 only when committed R23 is approved and `R23_COMPLETE_S17_NEXT`.
4. Implementer changes only the exact fourteen allowlisted paths. Tester writes factual T17 after execution; Reviewer writes V17 after committed same-subject passing T17; Reviewer executes Q17 only after V17 commit.
5. After active passed Q17, independent Reviewer classifies threads. Only an explicit addressed-and-resolvable classification permits Implementer to reply/resolve that exact thread; stop at human-check.

## Validation / Acceptance Checks

- B6R13 admission is non-merge, first-parent and exact-eight. R23's executable schema validates the actual eight
  path/blob records, first-parent admission and frozen B6R12/R22/S16-Q16 predecessor receipt; all revision identities
  are 40-character lowercase hexadecimal and B6R13/R23 post-commit facts are absent before admission.
- S17 changes exactly the fourteen named paths. It enforces one Planner bootstrap/no Planner self-route, Plan-Creator-only
  planning write, independent factual Tester stage, Reviewer same-subject Tester dependency, bounded no-merge Implementer,
  read-only Explorer, compatible generic/Python templates, `pr-open` Human boundary and direct-import preservation.
- T17/V17/Q17 are new B6R13-only evidence paths. Q17 verifies committed S17/T17/V17 full SHA, parents, linear topology,
  exact range/name-status and parsed same-subject factual/passing/approved claims; its sole authorization is classification.
- The following B6R12 checks are frozen provenance, not B6R13 routing authority.
- B6R12 admission is non-merge, first-parent and exactly five declared paths in lexical name-status order: B6R12 plan, B6R12 step, parent plan, parent spec, parent step.
- R22 的 full Draft 2020-12 JSON Schema machine-enforces actual `reviewed_artifacts` array 的五筆 ordered path/blob records，及 `first_parent_admission.name_status` 的同一 lexical exact-five；兩者都使用 `prefixItems`、`minItems:5`、`maxItems:5` 與 `items:false`。every blob, candidate commit/tree and first-parent SHA is lowercase hexadecimal with exactly 40 characters.
- R22 records candidate commit/tree, the exact-five first-parent admission, frozen B6R11 absent-R21 and B6R10/R20 receipt, Copilot triage, verdict and blockers.
- R20 remains `FROZEN_INVALID_NOT_ROUTING`; no S16 execution occurs before a committed approved R22.
- Retained B6R10 S16/T16/V16/Q16 paths, schemas and direct-import ban remain unmodified; Q16 never authorizes resolve, PR approval or merge.

## Frozen R22 Routing-Receipt Schema

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

## R23 Routing-Receipt Schema

R23 is written only from committed B6R13 and records post-admission facts. Its JSON schema is declared in the B6R13
correction plan: top-level keys are `schema_version`, `correction_id`, `review_kind`, `candidate`,
`reviewed_artifacts`, `first_parent_admission`, `predecessor_receipt_verification`, `review_basis`,
`copilot_feedback_triage`, `verdict`, `blocking_issues`, `route_authorization`, and `timestamp`. It machine-enforces
eight ordered exact path/blob records and the identical first-parent name-status entries. `approved` requires active
candidate, empty blockers and exact `R23_COMPLETE_S17_NEXT` / `S17`; `needs-rework` requires inactive candidate,
nonempty blockers and null route. Only an independently committed unchanged approved R23 activates S17.

## Reviewer Handoff

~~~json
{"current_route":"B6R13->R23->S17->T17->V17->Q17","correction_id":"observer-dispatcher-governance/high/b6r13","plan_review_path":"plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r13-review-log.md","implementation_subject":"S17 exact-fourteen allowlist only","range":"S17..V17","verdict":"approved|needs-rework"}
~~~

## Post-merge / release actions

No release action is authorized. Stop at the Human boundary.

## Open Questions / Unresolved Items

step-creator remains deferred. B6R12/R22/S16-Q16, B6R10/R20 and all earlier records are frozen nonrouting provenance.
