# Observer / Dispatcher Governance — B4 Correction Plan

## B4 Baseline

B0–B3, S1–S4, T1–T4, V1–V4, normal/recovery and old corrections are frozen nonrouting provenance. The two `step-creator` PR threads are deferred. B4 comprises exactly `plan/agent-handoff-workflow.md`, `plan/topic-plan-contract.md`, parent plan/spec/step, and this B4 plan/step. Independent Implementer commits those seven paths as non-subject B4; independent Plan-Reviewer reviews actual committed B4 blobs from a clean checkout and writes separately committed B4 review evidence.

## S5 Exact Allowlist

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

S5 alone is immutable non-merge subject. Existing direct imports remain; `importlib`, `__import__`, and `sys.modules` substitutions are forbidden.

## Roles / Evidence

Observer bootstrap-dispatches Planner only. Planner selects candidate/phase/gate/next role and may dispatch Tester or Explorer; wrappers are descriptive, never orchestration. T5 writes only `correction-b4-tester-evidence.md` with factual `passing|failing` results and no `next_gate`/routing. V5 writes only `correction-b4-implementation-review-log.md`, after passing same-S5 T5. Actual SHA graph verification and named `git diff --name-status S5..V5` must prove linear non-merge S5 -> T5 -> V5; no HEAD, merge, third descendant or text heuristic.
