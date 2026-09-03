# Observer / Dispatcher Governance — B6R12 Correction Plan

## Current route

`B6R12 -> R22 -> S16 -> T16 -> V16 -> Q16 -> thread-classification -> human-check` is the only current route. B6R11/R21 and B6R10/R20 are frozen nonrouting predecessor provenance. B6R12/R22 are non-subject; S16 is the sole implementation subject.

## Exact admission paths

B6R12 is non-merge first-parent exact-five. Its lexical `git diff --name-status` entries are exactly:

1. `A\tplan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r12-plan.md`
2. `A\tplan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r12-step.md`
3. `M\tplan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md`
4. `M\tplan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md`
5. `M\tplan/observer-dispatcher-governance/observer-dispatcher-governance.step.md`

Pre-admission planning artifacts contain no B6R12/R22 commit, tree, blob, HEAD or outcome claim.

## Evidence matrix

| Phase | Exact path | Writer | Gate |
| --- | --- | --- | --- |
| R22 | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r12-review-log.md` | Plan-Reviewer | committed B6R12 |
| S16 | `tests/test_observer_dispatcher_governance_contract.py` | Implementer | committed approved R22 |
| T16 | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r10-tester-evidence.md` | Tester | same S16 full suite passing |
| V16 | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r10-implementation-review-log.md` | Reviewer | committed passing T16 |
| Q16 | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r10-actual-gate-evidence.md` | Reviewer | committed V16 / actual full triple |

## R22 declared schema

```json
{"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object","required":["schema_version","correction_id","review_kind","candidate","reviewed_artifacts","first_parent_admission","predecessor_receipt_verification","review_basis","copilot_feedback_triage","verdict","blocking_issues","route_authorization","timestamp"],"properties":{"schema_version":{"const":"observer-dispatcher-governance.correction-b6r12-plan-review.v1"},"correction_id":{"const":"observer-dispatcher-governance/high/b6r12"},"review_kind":{"const":"correction-b6r12-routing-receipt"},"candidate":{"type":"object","required":["id","commit_sha","tree_sha","active"],"properties":{"id":{"const":"observer-dispatcher-governance/high/b6r12"},"commit_sha":{"type":"string","pattern":"^[0-9a-f]{40}$"},"tree_sha":{"type":"string","pattern":"^[0-9a-f]{40}$"},"active":{"type":"boolean"}},"additionalProperties":false},"reviewed_artifacts":{"type":"array","minItems":5,"maxItems":5,"prefixItems":[{"type":"object","required":["path","blob_sha"],"properties":{"path":{"const":"plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r12-plan.md"},"blob_sha":{"type":"string","pattern":"^[0-9a-f]{40}$"}},"additionalProperties":false},{"type":"object","required":["path","blob_sha"],"properties":{"path":{"const":"plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r12-step.md"},"blob_sha":{"type":"string","pattern":"^[0-9a-f]{40}$"}},"additionalProperties":false},{"type":"object","required":["path","blob_sha"],"properties":{"path":{"const":"plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md"},"blob_sha":{"type":"string","pattern":"^[0-9a-f]{40}$"}},"additionalProperties":false},{"type":"object","required":["path","blob_sha"],"properties":{"path":{"const":"plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md"},"blob_sha":{"type":"string","pattern":"^[0-9a-f]{40}$"}},"additionalProperties":false},{"type":"object","required":["path","blob_sha"],"properties":{"path":{"const":"plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md"},"blob_sha":{"type":"string","pattern":"^[0-9a-f]{40}$"}},"additionalProperties":false}],"items":false},"first_parent_admission":{"type":"object","required":["commit_sha","tree_sha","parent_sha","non_merge","exact_declared_paths","name_status"],"properties":{"commit_sha":{"type":"string","pattern":"^[0-9a-f]{40}$"},"tree_sha":{"type":"string","pattern":"^[0-9a-f]{40}$"},"parent_sha":{"type":"string","pattern":"^[0-9a-f]{40}$"},"non_merge":{"const":true},"exact_declared_paths":{"const":true},"name_status":{"type":"array","minItems":5,"maxItems":5,"prefixItems":[{"const":"A\tplan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r12-plan.md"},{"const":"A\tplan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r12-step.md"},{"const":"M\tplan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md"},{"const":"M\tplan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md"},{"const":"M\tplan/observer-dispatcher-governance/observer-dispatcher-governance.step.md"}],"items":false}},"additionalProperties":false},"predecessor_receipt_verification":{"type":"object","required":["b6r11_admission","r21","r20"],"properties":{"b6r11_admission":{"const":"995c5a8"},"r21":{"const":"ABSENT_FROZEN_NONROUTING"},"r20":{"const":"FROZEN_INVALID_NOT_ROUTING"}},"additionalProperties":false},"review_basis":{"const":"independent clean checkout"},"copilot_feedback_triage":{"type":"object","required":["ADDRESS","DISCUSS","SKIP"],"properties":{"ADDRESS":{"type":"array"},"DISCUSS":{"type":"array"},"SKIP":{"type":"array"}},"additionalProperties":false},"verdict":{"enum":["approved","needs-rework"]},"blocking_issues":{"type":"array"},"route_authorization":{"type":["object","null"]},"timestamp":{"type":"string","format":"date-time"}},"additionalProperties":false,"allOf":[{"if":{"properties":{"verdict":{"const":"approved"}},"required":["verdict"]},"then":{"properties":{"candidate":{"properties":{"active":{"const":true}},"required":["active"]},"blocking_issues":{"maxItems":0},"route_authorization":{"type":"object","required":["effective_committed_state","next_phase","implementation_subject_sha","close_authorization"],"properties":{"effective_committed_state":{"const":"R22_COMPLETE_S16_NEXT"},"next_phase":{"const":"S16"},"implementation_subject_sha":{"const":null},"close_authorization":{"const":null}},"additionalProperties":false}},"required":["candidate","blocking_issues","route_authorization"]}},{"if":{"properties":{"verdict":{"const":"needs-rework"}},"required":["verdict"]},"then":{"properties":{"candidate":{"properties":{"active":{"const":false}},"required":["active"]},"blocking_issues":{"minItems":1},"route_authorization":{"const":null}},"required":["candidate","blocking_issues","route_authorization"]}}]}
```

此 code fence 是可執行的 Draft 2020-12 JSON Schema，不是 R22 evidence object。實際 R22 的 `reviewed_artifacts` 值必須是 array；其 exact-five records 依序為兩個 `A` correction paths、三個 `M` parent paths，`prefixItems` 配合 `items:false` 禁止第六筆或替換。每個 candidate、tree、first-parent 與 blob SHA 都必須符合 `^[0-9a-f]{40}$`；`first_parent_admission.name_status` 也以相同 lexical exact-five `prefixItems`／`items:false` machine-enforce。written R22 僅記錄 post-admission facts。

`approved` requires `candidate.active:true`, `blocking_issues:[]`, and exact `R22_COMPLETE_S16_NEXT` / `S16` route authorization. `needs-rework` requires `candidate.active:false`, nonempty blockers and `route_authorization:null`. Only an Independent Implementer committing unchanged approved R22 activates S16.

## Retained descendant contract

S16 retains direct imports and forbids `importlib`, `__import__` and `sys.modules`. The B6R10-declared T16/V16/Q16 exact-key schemas, lower-case 40-hex requirements, same-S16 topology, V16 `APPROVED`, and Q16 actual full-triple/classification-only boundary are unchanged. Q16 never authorizes thread resolution, Human review, merge, release or post-merge.
