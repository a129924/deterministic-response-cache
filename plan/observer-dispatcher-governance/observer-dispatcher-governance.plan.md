# Observer / Dispatcher Governance

> **B4R2 current execution truth:** B0, B1, B2, B3, B4, B4R, S1–S4, T1–T4, V1–V4,
> normal/recovery records and their active, pending, schema, blocker and checklist semantics are
> frozen nonrouting history. The two `step-creator` threads remain deferred. B4R2 is the sole
> current pre-subject route: independent review of committed B4R2, then S5, T5 and V5 only.

## Goal / Outcome

完成 current-topic governance correction：以 B4R2 的獨立 clean-checkout planning review 建立唯一
pre-subject gate，之後只允許 immutable S5 與 T5/V5 evidence chain，並保持 Human boundary。

## Scope

- **In scope:** B4R2 的六個 planning paths；approved B4R2 review 後，S5 的 exact 15-path
  allowlist；以及 B4R2 exact T5/V5 evidence paths。
- **Out of scope:** frozen epoch 修改或重讀、legacy migration、`step-creator` threads、任何未列
  path、產品/architecture work、PR thread action、merge、release、post-merge。

## Locked Decisions

- B4R2 and its separately committed review record are non-subject; only S5 can establish
  `implementation_subject_sha`.
- Direct imports remain mandatory; `importlib`, `__import__` and `sys.modules` substitutions are
  forbidden.
- Actual named Git graph queries—not `HEAD` or textual inference—must prove exactly
  `S5 -> T5 -> V5` and named `S5..V5`.
- This is non-stable, review-ready-only work: README, VERSION, release and tag are excluded.

## Boundaries / Exclusions

Observer bootstrap-dispatches Planner only; Planner is the sole routing authority. Plan-Creator
writes planning artifacts only; Implementer performs bounded commits/implementation; Tester and
Reviewer independently write only declared evidence. Frozen B2/B3/B4/B4R records have no current
route, status, gate or pending meaning.

## Status / Allowed Transitions

Current status is `needs-rework` / `PLANNER_REPLAN`. The sole executable route is:
`B4R2 review -> S5 -> T5 -> V5 -> human-check`. Any contract failure returns to Planner; no prior
epoch is a fallback.

## Artifact Paths

| Artifact | Exact path | Write owner | Decision authority | Role |
| --- | --- | --- | --- | --- |
| Shared contract | `plan/topic-plan-contract.md` | Plan-Creator | Planner | B4R2 contract |
| Parent plan | `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md` | Plan-Creator | Planner | Current execution truth |
| Parent spec | `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md` | Plan-Creator | Planner | Acceptance contract |
| Parent step | `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md` | Plan-Creator | Planner | Current tracker |
| B4R2 plan | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r2-plan.md` | Plan-Creator | Planner | B4R2 delta |
| B4R2 step | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r2-step.md` | Plan-Creator | Planner | B4R2 tracker |
| B4R2 review | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r2-review-log.md` | Plan-Reviewer | Plan-Reviewer verdict; Planner route | Pre-S5 gate |
| T5 evidence | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r2-tester-evidence.md` | Tester | Factual test result only | First descendant |
| V5 evidence | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r2-implementation-review-log.md` | Reviewer | Reviewer verdict; Planner route | Final descendant |

After separately committed approved B4R2 review, S5 may modify exactly:

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

1. Independently review and separately commit B4R2 planning evidence; B4R2 remains non-subject.
2. Make one non-merge S5 changing only the exact allowlist above.
3. Write T5 then V5 as the two evidence-only descendants, with actual named-SHA topology/range verification.

## Validation / Acceptance Checks

- B4R2 review covers exactly its six committed paths and is approved before S5.
- S5 is the only implementation subject and has no path outside the preserved 15-path allowlist.
- T5 and V5 attest the same S5; V5 requires passing T5; each evidence path is exact.
- Actual Git commands prove non-merge `S5 -> T5 -> V5` and `git diff --name-status S5..V5` lists
  exactly the two B4R2 evidence paths.
- Tests fail closed for prior epochs as route/subject, changed S5 allowlist, dynamic import
  substitution, incorrect evidence topology, range, merge or third descendant.

## Reviewer Handoff

```json
{"current_route":"B4R2-review->S5->T5->V5","b4r2_review_path":"plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r2-review-log.md","implementation_subject":"S5 only","range":"S5..V5","verdict":"approved|needs-rework"}
```

The B4R2 review schema and T5/V5 evidence schemas are defined by
`plan/topic-plan-contract.md#b4r2-correction-evidence-schemas`.

## Post-merge / release actions

Stop at the Human boundary; none are authorized.

## Open Questions / Unresolved Items

Only the current B4R2 review and successor S5/T5/V5 gates remain; frozen history creates none.
