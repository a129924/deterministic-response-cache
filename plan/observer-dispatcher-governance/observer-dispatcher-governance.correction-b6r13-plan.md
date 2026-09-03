# Observer / Dispatcher Governance — B6R13 Correction Plan

## Current route

`B6R13 -> R23 -> S17 -> T17 -> V17 -> Q17 -> thread-classification -> comment-resolve -> human-check` is the only
current route. B6R13/R23 are non-subject. B6R12/R22/S16-Q16, B6R10/R20 and all older records are immutable frozen
nonrouting provenance. B6R13/R23 commit, tree, blob, HEAD and outcome facts are absent before admission.

## Exact B6R13 admission paths

B6R13 is non-merge, first-parent and exact-eight. Its named diff must contain exactly once, with no other path:

1. `AGENTS.md`
2. `plan/agent-handoff-workflow.md`
3. `plan/topic-plan-contract.md`
4. `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md`
5. `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md`
6. `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md`
7. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r13-plan.md`
8. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r13-step.md`

## R23 receipt contract

R23 may be written only from a committed B6R13 clean checkout, at
`plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r13-review-log.md`. It is one JSON
object with exactly `schema_version`, `correction_id`, `review_kind`, `candidate`, `reviewed_artifacts`,
`first_parent_admission`, `predecessor_receipt_verification`, `review_basis`, `copilot_feedback_triage`, `verdict`,
`blocking_issues`, `route_authorization`, `timestamp`. `candidate` has exactly id/commit_sha/tree_sha/active;
`reviewed_artifacts` has exactly the above eight ordered path/blob records; `first_parent_admission` has exactly
commit_sha/tree_sha/parent_sha/non_merge/exact_declared_paths/name_status, whose name-status records are identical to
the actual first-parent B6R13 named diff. All revision and blob values are 40-character lowercase hexadecimal.

`predecessor_receipt_verification` records B6R12 `351e381e9ae048671944255314f52cc88b00271f`, R22
`1cb0ea780b26c46c667466d6f42df28606790194`, S16 `b205d22d4b19b9a9246b2c06d448046d1dd2d2fd`, T16
`e4727883c973e315516bd6282590062c033ca26e`, V16 `51971b761ef4e8d887b2f6446a5fa834f760d987`, Q16
`cbb0f8fcd5181ff4993f9a36aa5477772b4403b3`, each as frozen nonrouting provenance. `review_basis` is independent
clean checkout. `copilot_feedback_triage` has exact ADDRESS/DISCUSS/SKIP arrays. `approved` requires active candidate,
empty blockers and route authorization exactly `R23_COMPLETE_S17_NEXT` / `S17` with null implementation subject and
close authorization. `needs-rework` requires inactive candidate, one-or-more blockers and null route authorization.
Only an independent Implementer committing unchanged approved R23 makes the route active.

## S17 exact allowlist and acceptance

S17 is non-merge and may modify only these fourteen paths:

1. `.codex/agents/planner.toml`
2. `.codex/agents/implementer.toml`
3. `.codex/agents/reviewer.toml`
4. `.codex/agents/tester.toml`
5. `.agents/skills/plan-creator/SKILL.md`
6. `.agents/skills/plan-creator/checklist.md`
7. `.agents/skills/plan-creator/templates/topic-plan-template.md`
8. `.agents/skills/plan-reviewer/SKILL.md`
9. `.agents/skills/plan-reviewer/checklist.md`
10. `.agents/skills/plan-reviewer/reference.md`
11. `.agents/skills/plan-reviewer/examples.md`
12. `.agents/skills/python-implementation-workflow/SKILL.md`
13. `.agents/skills/python-plan-authoring/templates/canonical-python-topic-plan-template.md`
14. `tests/test_observer_dispatcher_governance_contract.py`

S17 must prove: Planner bootstraps once and cannot select itself later; Plan-Creator alone writes planning artifacts;
Plan-Reviewer only writes declared review receipt; Tester is independent, factual and records actual exit code; Reviewer
only consumes same-subject passing Tester evidence; Implementer is bounded and never merges; Explorer is bounded
read-only; generic and Python templates match the shared contract and keep release conditional; `publish-in-progress`
only reaches `pr-open`, then stops at Human boundary. Existing direct imports remain direct and no `importlib`,
`__import__`, or `sys.modules` substitution is introduced.

## Descendant evidence and boundary

T17, V17 and Q17 paths are respectively
`observer-dispatcher-governance.correction-b6r13-tester-evidence.md`,
`observer-dispatcher-governance.correction-b6r13-implementation-review-log.md`, and
`observer-dispatcher-governance.correction-b6r13-actual-gate-evidence.md` under this topic directory. T17 records
same-S17 factual actual command/exit-code result; V17 binds committed passing T17 and approves the exact S17 diff; Q17
is post-V17 actual full-SHA triple/linear/range/name-status validation. Q17 authorizes classification only. A separate
independent classification must name an exact `addressed-and-resolvable` thread before an Implementer may leave the
bounded reply and resolve it. Human review, merge, release and post-merge remain forbidden.
