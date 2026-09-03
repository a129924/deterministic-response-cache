# Observer / Dispatcher Governance

## Goal / Outcome

以 B6R11 routing-receipt correction 收斂唯一可驗證路徑：`B6R11 -> R21 -> S16 -> T16 -> V16 -> Q16 -> thread-classification -> human-check`。本 topic 是 non-stable、review-ready-only；停在 Human boundary。

## Scope

- **In Scope:** B6R11 exact-five planning baseline、R21 independent review、已宣告的 S16 單一 test-path、既有 T16/V16/Q16 evidence schemas 與 passed Q16 後的 independent classification。
- **Out Of Scope:** B6R10/R20、B6R9/Q15 和所有早期 provenance、legacy migration、step-creator、產品或架構工作、unlisted paths、thread resolve、merge、release、post-merge。
- **ReadOnly:** `AGENTS.md`、README、VERSION、`.github/**`、B6R10/R20 與所有 earlier artifacts。
- **Written / Modify:** 僅 B6R11 admission 的五個 declared planning paths；No path is Deleted。

## Locked Decisions

- Current correction 是 `observer-dispatcher-governance/high/b6r11`，state `R21_REVIEW_PENDING`；只有此路徑可 routing。
- B6R10/R20 是 frozen predecessor receipt。R20 reviewed B6R10 `785eed2`，R20 commit 為 `8b5e8dad1eda02e5effa3e1cb6555efe3c8cd87c`，review blob `3d1a4941…` 的 decoded literal-backslash-`t` defect 使其 `routing_valid:false` / `FROZEN_INVALID_NOT_ROUTING`；不得 authorize S16。
- B6R11/R21 都是 non-subject。S16 是唯一 implementation subject，完整 diff 僅可改 `tests/test_observer_dispatcher_governance_contract.py`；direct imports 必須保留，禁止 `importlib`、`__import__`、`sys.modules` substitution。
- B6R10 已宣告的 S16/T16/V16/Q16 paths、exact schemas、linear topology 與 Q16 actual full-triple/classification-only boundary 原樣保留；B6R11 不重寫其 schema。
- B6R11 admission 為 non-merge first-parent exact-five；pre-admission 不含 B6R11/R21 commit、tree、blob、HEAD 或 outcome。只有 committed approved R21 產生一個 active candidate，effective state `R21_COMPLETE_S16_NEXT`，next phase S16。

## Boundaries / Exclusions

Observer 只 dispatch/aggregate；Planner 唯一決定 candidate、phase、gate 與 next role。Plan-Creator 只寫 declared planning paths；Plan-Reviewer 只寫 R21；Implementer 只做 approved bounded work；Tester 與 Reviewer 只寫 declared evidence。Reviewer 不是 Human PR reviewer。不得 widen allowlist、resolve threads、merge、release 或 post-merge。

## Status / Allowed Transitions

**Current:** `R21_REVIEW_PENDING`。

R21 必須在 committed B6R11 clean checkout 驗證 exact-five blobs/admission 與 frozen B6R10/R20 receipt。approved R21 原樣由 Independent Implementer 單獨提交後，才成為 `R21_COMPLETE_S16_NEXT` 並 dispatch S16。S16 需要 R21 approval；T16 需要 same-S16 full-suite passing；V16 需要 committed passing T16；Q16 需要 committed V16。failure 回 Planner；human actions 停在 Human boundary。

## Artifact Paths

| Artifact | Exact path | Write owner | Decision authority | Role |
| --- | --- | --- | --- | --- |
| Parent plan | `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md` | Plan-Creator | Planner | B6R11 current truth |
| Parent spec | `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md` | Plan-Creator | Planner | B6R11 acceptance |
| Parent step | `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md` | Plan-Creator | Planner | B6R11 tracker |
| B6R11 plan | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r11-plan.md` | Plan-Creator | Planner | baseline delta |
| B6R11 step | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r11-step.md` | Plan-Creator | Planner | baseline tracker |
| R21 review | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r11-review-log.md` | Plan-Reviewer | Plan-Reviewer verdict | pre-S16 gate |
| S16 subject | `tests/test_observer_dispatcher_governance_contract.py` | Implementer | Planner | sole subject |
| T16 evidence | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r10-tester-evidence.md` | Tester | factual test result | retained descendant |
| V16 evidence | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r10-implementation-review-log.md` | Reviewer | reviewer verdict | retained descendant |
| Q16 evidence | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r10-actual-gate-evidence.md` | Reviewer | actual-gate result | classification gate |

## Implementation Steps

1. Plan-Creator writes exactly the five B6R11 planning paths; Independent Implementer creates the exact non-merge first-parent admission.
2. Independent Plan-Reviewer reviews committed B6R11 and writes R21, including predecessor receipt verification; Independent Implementer commits an unchanged approved R21.
3. Planner dispatches retained S16 only when committed R21 is approved and `R21_COMPLETE_S16_NEXT`.
4. Tester writes retained T16 after full suite; Reviewer writes retained V16 after committed passing T16; Reviewer executes retained Q16 only after V16 commit.
5. After active passed Q16, independent Reviewer classifies threads; stop at human-check.

## Validation / Acceptance Checks

- B6R11 admission is non-merge, first-parent and exactly five declared paths.
- R21 machine-enforces five ordered path/blob records: the three parent paths followed by the B6R11 plan and step; each blob SHA is lowercase hexadecimal with exactly 40 characters, and that ordered file set must equal the B6R11 first-parent exact-five diff.
- R21 records candidate commit/tree, the exact-five first-parent admission, frozen B6R10/R20 receipt, Copilot triage, verdict and blockers.
- R20 remains `FROZEN_INVALID_NOT_ROUTING`; no S16 execution occurs before a committed approved R21.
- Retained B6R10 S16/T16/V16/Q16 paths, schemas and direct-import ban remain unmodified; Q16 never authorizes resolve, PR approval or merge.

## R21 Routing-Receipt Schema

R21 is written only from the committed B6R11 checkout and records post-admission facts. Its single JSON object has
`schema_version`, `correction_id`, `review_kind`, `candidate`, `reviewed_artifacts`, `first_parent_admission`,
`predecessor_receipt_verification`, `review_basis`, `copilot_feedback_triage`, `verdict`, `blocking_issues`,
`route_authorization`, and `timestamp`. `reviewed_artifacts` uses the declared B6R11 JSON Schema: it has exactly five
ordered records (not a generic pair), its path constants are the three parent paths then the B6R11 plan and step, and
every `blob_sha` matches `^[0-9a-f]{40}$`. The reviewer must fail closed unless this ordered tuple list is identical to
the first-parent exact-five diff's ordered file set; `first_parent_admission` records that comparison, candidate,
parent, non-merge result, and five name-status entries.
`predecessor_receipt_verification` must record B6R10 `785eed2`, R20
`8b5e8dad1eda02e5effa3e1cb6555efe3c8cd87c`, review blob prefix `3d1a4941`, decoded literal-backslash-`t` defect,
`routing_valid:false`, and `FROZEN_INVALID_NOT_ROUTING`. `needs-rework` requires inactive candidate and null route
authorization. Only committed unchanged `approved` R21 may set `R21_COMPLETE_S16_NEXT` / `S16`.

## Reviewer Handoff

~~~json
{"current_route":"B6R11->R21->S16->T16->V16->Q16","correction_id":"observer-dispatcher-governance/high/b6r11","plan_review_path":"plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r11-review-log.md","implementation_subject":"S16 only","range":"S16..V16","verdict":"approved|needs-rework"}
~~~

## Post-merge / release actions

No release action is authorized. Stop at the Human boundary.

## Open Questions / Unresolved Items

step-creator remains deferred. B6R10/R20 and all earlier records are frozen nonrouting provenance.
