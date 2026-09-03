# Observer / Dispatcher Governance — B4R Correction Plan

## B4R Baseline

`B4=979798e` failed before approval and is frozen, unapproved, non-subject provenance. B0–B4,
S1–S4, T1–T4, V1–V4, normal/recovery and all prior corrections are frozen nonrouting provenance;
the two `step-creator` PR threads remain deferred. B4R comprises exactly six paths:

1. `plan/topic-plan-contract.md`
2. `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md`
3. `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md`
4. `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md`
5. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r-plan.md`
6. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r-step.md`

An Independent Implementer commits only those six paths as non-subject B4R. From a clean B4R
checkout, an Independent Plan-Reviewer reviews the committed blobs and writes only
`observer-dispatcher-governance.correction-b4r-review-log.md`; an Independent Implementer separately
commits that unchanged approved record. B4R and its review-evidence commit can never establish
`implementation_subject_sha`.

## S5 Exact Allowlist

S5 may begin only after the separately committed approved B4R review evidence. S5 alone is the
immutable non-merge subject and may modify exactly:

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

Direct imports remain mandatory; `importlib`, `__import__`, and `sys.modules` substitutions are
forbidden. The B4R exception expressly includes `.codex/agents/reviewer.toml`; historical B2 path
boundaries do not constrain S5.

## Roles / Evidence

Observer bootstrap-dispatches Planner only. Planner selects candidate, phase, gate, and next role;
wrappers are descriptive, never orchestration. Tester writes only the exact B4R T5 path with factual
`passing|failing` results and no routing, lifecycle, status, or `next_gate` field. Reviewer writes
only the exact B4R V5 path after a passing T5 for the same S5.

Actual named SHA graph queries must prove linear non-merge `S5 -> T5 -> V5`. Named
`git diff --name-status S5..V5` must list exactly the B4R T5/V5 evidence paths; `HEAD`, a merge,
a third descendant, or textual topology inference fails closed.
