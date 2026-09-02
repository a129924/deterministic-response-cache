# Observer / Dispatcher Governance

> **Frozen provenance:** `b900366` and B0–B4R5, S1–S5, T1–T5, V1–V5, normal/recovery evidence,
> and every older correction artifact are nonrouting history. They create no current status, gate,
> pending work, subject, schema, checklist, or candidate.

## Goal / Outcome

完成 B4R6 correction baseline，讓唯一 current route 以 clean seven-blob planning review 後的
S6 subject、T6 factual test evidence、V6 independent review evidence 收斂，並保留 Human boundary。

## Scope

- **In scope:** B4R6 seven planning paths、B4R6 clean seven-blob review record、S6 exact 15-path
  allowlist，以及 exact T6/V6 evidence paths。
- **Out of scope:** frozen epoch 修改或重讀、legacy migration、`step-creator` threads、任何未列
  path、產品/architecture work、PR thread action、merge、release、post-merge。

## Locked Decisions

- B4R6 is the unique current pre-subject baseline; its baseline and separately committed review record
  are both non-subject. Only S6 can establish `implementation_subject_sha`.
- B4R6 baseline has no bootstrap-test exception: it is exactly seven planning paths and no test,
  implementation, evidence, routing, status, or eighth path.
- Direct imports remain mandatory; `importlib`, `__import__` and `sys.modules` substitutions are
  forbidden.
- Actual named Git graph queries—not `HEAD` or textual inference—must prove exactly
  `S6 -> T6 -> V6` and named `S6..V6`.
- This is non-stable, review-ready-only work: README, VERSION, release and tag are excluded.

## Boundaries / Exclusions

Observer bootstrap-dispatches Planner only; Planner is the sole routing authority. Plan-Creator writes
the seven planning artifacts only; Independent Implementer commits B4R6 and later S6; Tester and
Reviewer independently write only declared evidence. The two `step-creator` threads remain deferred.

## Status / Allowed Transitions

Current status is `needs-rework` / `PLANNER_REPLAN`. The sole executable route is:
`B4R6 seven-blob review -> S6 -> T6 -> V6 -> human-check`. Any contract failure returns to Planner; no prior
epoch is a fallback.

## Artifact Paths

| Artifact | Exact path | Write owner | Decision authority | Role |
| --- | --- | --- | --- | --- |
| Shared workflow | `plan/agent-handoff-workflow.md` | Plan-Creator | Planner | B4R6 contract |
| Shared contract | `plan/topic-plan-contract.md` | Plan-Creator | Planner | B4R6 contract |
| Parent plan | `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md` | Plan-Creator | Planner | Current execution truth |
| Parent spec | `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md` | Plan-Creator | Planner | Acceptance contract |
| Parent step | `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md` | Plan-Creator | Planner | Current tracker |
| B4R6 plan | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r6-plan.md` | Plan-Creator | Planner | B4R6 delta |
| B4R6 step | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r6-step.md` | Plan-Creator | Planner | B4R6 tracker |
| B4R6 review | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r6-review-log.md` | Plan-Reviewer | Plan-Reviewer verdict | Pre-S6 gate |
| T6 evidence | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r6-tester-evidence.md` | Tester | Factual test result | First descendant |
| V6 evidence | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r6-implementation-review-log.md` | Reviewer | Reviewer verdict; Planner route | Final descendant |

After separately committed approved B4R6 review, S6 may modify exactly:

1. `AGENTS.md`
2. `.codex/agents/planner.toml`
3. `.codex/agents/implementer.toml`
4. `.codex/agents/reviewer.toml`
5. `.agents/skills/plan-creator/SKILL.md`
6. `.agents/skills/plan-creator/checklist.md`
7. `.agents/skills/plan-creator/templates/topic-plan-template.md`
8. `.agents/skills/plan-reviewer/SKILL.md`
9. `.agents/skills/plan-reviewer/checklist.md`
10. `.agents/skills/plan-reviewer/reference.md`
11. `.agents/skills/plan-reviewer/examples.md`
12. `.agents/skills/python-implementation-workflow/SKILL.md`
13. `.agents/skills/python-implementation-workflow/reference.md`
14. `.agents/skills/python-plan-authoring/templates/canonical-python-topic-plan-template.md`
15. `tests/test_observer_dispatcher_governance_contract.py`

## Implementation Steps

1. Independent Implementer commits exactly the seven B4R6 baseline paths as non-subject and reports
   `git diff --name-status b900366..<B4R6-SHA>`.
2. Independently review actual seven B4R6 blobs from a clean checkout and separately commit approved
   B4R6 review evidence.
3. Planner verifies the B4R6 record before dispatching one non-merge S6 over the exact allowlist.
4. Write T6 then V6 as the two evidence-only descendants, with actual named-SHA topology/range
   verification.

## Validation / Acceptance Checks

- B4R6 baseline diff from `b900366` lists exactly the seven declared planning paths, without a test,
  implementation, evidence, eighth path, merge, or `implementation_subject_sha`.
- B4R6 review covers exactly its seven committed blobs once and is approved before S6.
- S6 is the only implementation subject and has no path outside the preserved 15-path allowlist.
- T6 and V6 attest the same S6; V6 requires passing T6; each evidence path is exact.
- Actual Git commands prove non-merge `S6 -> T6 -> V6` and `git diff --name-status S6..V6` lists
  exactly the two B4R6 evidence paths.
- Tests fail closed for frozen provenance as route/subject, changed S6 allowlist, dynamic import
  substitution, B4R6 review-schema mutation, incorrect evidence topology/range, merge, or third descendant.

## Reviewer Handoff

```json
{"current_route":"B4R6-seven-blob-review->S6->T6->V6","b4r6_review_path":"plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r6-review-log.md","implementation_subject":"S6 only","range":"S6..V6","verdict":"approved|needs-rework"}
```

The B4R6 review schema and T6/V6 evidence schemas are defined by
`plan/topic-plan-contract.md#b4r6-correction-evidence-schemas`.

## Post-merge / release actions

Stop at the Human boundary; none are authorized.

## Open Questions / Unresolved Items

Only the B4R6 review and successor S6/T6/V6 gates remain; frozen history creates none.
