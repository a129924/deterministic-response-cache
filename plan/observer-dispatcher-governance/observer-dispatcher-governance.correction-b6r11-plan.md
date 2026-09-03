# Observer / Dispatcher Governance — B6R11 Routing-Receipt Correction

## Current route

`B6R11 -> R21 -> S16 -> T16 -> V16 -> Q16 -> thread-classification -> human-check` is the sole current route.
B6R11/R21 are non-subject; S16 alone may change
`tests/test_observer_dispatcher_governance_contract.py`. B6R10/R20 and all earlier records are frozen nonrouting
provenance.

## Exact admission paths

1. `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md`
2. `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md`
3. `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md`
4. this file
5. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r11-step.md`

B6R11 admission is non-merge, first-parent exact-five. This pre-admission artifact contains no B6R11/R21 commit,
tree, blob, HEAD, or review outcome.

## Frozen predecessor receipt

R20 reviewed B6R10 `785eed2`; R20 was committed as `8b5e8dad1eda02e5effa3e1cb6555efe3c8cd87c`. Its review blob
`3d1a4941…` has a decoded literal-backslash-`t` defect. R21 must record this immutable fact as
`routing_valid:false` and `FROZEN_INVALID_NOT_ROUTING`; it cannot select, repair, or route R20.

## Retained descendant contract

B6R10's declared S16/T16/V16/Q16 paths and exact semantic schemas remain authoritative for descendants. S16 retains
direct imports and rejects `importlib`, `__import__`, and `sys.modules` substitution. Q16 remains a real-Git
full-triple, classification-only boundary and never resolves threads or authorizes Human review, merge, release, or
post-merge.

## R21 declared schema

~~~json
{"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object","required":["schema_version","correction_id","review_kind","candidate","reviewed_artifacts","first_parent_admission","predecessor_receipt_verification","review_basis","copilot_feedback_triage","verdict","blocking_issues","route_authorization","timestamp"],"properties":{"schema_version":{"const":"observer-dispatcher-governance.correction-b6r11-plan-review.v1"},"correction_id":{"const":"observer-dispatcher-governance/high/b6r11"},"review_kind":{"const":"correction-b6r11-routing-receipt"},"candidate":{"type":"object","required":["id","commit_sha","tree_sha","active"],"properties":{"id":{"const":"observer-dispatcher-governance/high/b6r11"},"commit_sha":{"type":"string","pattern":"^[0-9a-f]{40}$"},"tree_sha":{"type":"string","pattern":"^[0-9a-f]{40}$"},"active":{"type":"boolean"}},"additionalProperties":false},"reviewed_artifacts":{"type":"array","minItems":5,"maxItems":5,"prefixItems":[{"type":"object","required":["path","blob_sha"],"properties":{"path":{"const":"plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md"},"blob_sha":{"type":"string","pattern":"^[0-9a-f]{40}$"}},"additionalProperties":false},{"type":"object","required":["path","blob_sha"],"properties":{"path":{"const":"plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md"},"blob_sha":{"type":"string","pattern":"^[0-9a-f]{40}$"}},"additionalProperties":false},{"type":"object","required":["path","blob_sha"],"properties":{"path":{"const":"plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md"},"blob_sha":{"type":"string","pattern":"^[0-9a-f]{40}$"}},"additionalProperties":false},{"type":"object","required":["path","blob_sha"],"properties":{"path":{"const":"plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r11-plan.md"},"blob_sha":{"type":"string","pattern":"^[0-9a-f]{40}$"}},"additionalProperties":false},{"type":"object","required":["path","blob_sha"],"properties":{"path":{"const":"plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r11-step.md"},"blob_sha":{"type":"string","pattern":"^[0-9a-f]{40}$"}},"additionalProperties":false}],"items":false},"first_parent_admission":{"type":"object","required":["commit_sha","parent_sha","non_merge","exact_declared_paths","name_status"],"properties":{"commit_sha":{"type":"string","pattern":"^[0-9a-f]{40}$"},"parent_sha":{"type":"string","pattern":"^[0-9a-f]{40}$"},"non_merge":{"const":true},"exact_declared_paths":{"const":true},"name_status":{"type":"array","minItems":5,"maxItems":5,"items":{"type":"string"}}},"additionalProperties":false},"predecessor_receipt_verification":{"type":"object","required":["b6r10_commit_sha","r20_commit_sha","r20_review_blob_prefix","defect","routing_valid","status"],"properties":{"b6r10_commit_sha":{"const":"785eed2"},"r20_commit_sha":{"const":"8b5e8dad1eda02e5effa3e1cb6555efe3c8cd87c"},"r20_review_blob_prefix":{"const":"3d1a4941"},"defect":{"const":"decoded literal-backslash-t"},"routing_valid":{"const":false},"status":{"const":"FROZEN_INVALID_NOT_ROUTING"}},"additionalProperties":false},"review_basis":{"const":"independent clean checkout"},"copilot_feedback_triage":{"type":"object","required":["ADDRESS","DISCUSS","SKIP"],"properties":{"ADDRESS":{"type":"array"},"DISCUSS":{"type":"array"},"SKIP":{"type":"array"}},"additionalProperties":false},"verdict":{"enum":["approved","needs-rework"]},"blocking_issues":{"type":"array"},"route_authorization":{"type":["object","null"]},"timestamp":{"type":"string","format":"date-time"}},"additionalProperties":false}
~~~

`reviewed_artifacts` is an ordered tuple list, not a representative pair: its five `prefixItems` are the complete
allowlist and `items:false` rejects a sixth or substituted entry. R21 must fail closed unless this ordered path list is
identical to the B6R11 first-parent `exact-five` diff's ordered file set; each paired `blob_sha` must be read from the
committed candidate tree. `first_parent_admission.name_status` must likewise contain exactly the five diff entries.

R21 writes post-admission facts only. `needs-rework` requires `candidate.active:false` and
`route_authorization:null`. Only an independently committed unchanged approved R21 can set
`R21_COMPLETE_S16_NEXT` and next phase `S16`.
