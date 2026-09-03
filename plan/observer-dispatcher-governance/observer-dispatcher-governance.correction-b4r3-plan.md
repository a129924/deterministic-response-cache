# Observer / Dispatcher Governance — B4R3 Correction Plan

## B4R3 Baseline

`0800dc11181cdbd7d93d85e0298ea78dc33d06d3` committed B4R2, but its clean-checkout planning review
failed; B0–B4R2, S1–S4, T1–T4, V1–V4, normal/recovery records and all their active/pending/schema/
blocker/checklist semantics are frozen nonrouting history. B4R3 is the sole current pre-subject
baseline and contains exactly:

1. `plan/agent-handoff-workflow.md`
2. `plan/topic-plan-contract.md`
3. `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md`
4. `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md`
5. `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md`
6. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r3-plan.md`
7. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r3-step.md`

An Independent Implementer commits exactly these seven paths as non-subject B4R3. From a clean B4R3
checkout, an Independent Plan-Reviewer writes only the unique B4R3 review record. An Independent
Implementer separately commits that unchanged approved record. B4R3 and its review-evidence commit
can never establish `implementation_subject_sha`.

## S5 Exact Allowlist

S5 may begin only after the separately committed approved B4R3 review evidence. S5 alone is the
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
forbidden. The B4R3 scope preserves this B4R allowlist verbatim.

## Evidence and Actual-Graph Requirements

Tester writes only
`plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r3-tester-evidence.md`
for same-S5 factual `passing|failing` results, with no routing, lifecycle, status or `next_gate`
field. Reviewer writes only
`plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r3-implementation-review-log.md`
after same-S5 passing T5.

Actual named SHA graph queries must prove linear non-merge `S5 -> T5 -> V5`. Named
`git diff --name-status S5..V5` must list exactly the two B4R3 evidence paths above. `HEAD`, a
merge, a third descendant or textual topology inference fails closed. V5 is authored before its
commit and cannot self-reference or infer V5 SHA.
