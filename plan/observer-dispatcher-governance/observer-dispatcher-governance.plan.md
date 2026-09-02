# Observer / Dispatcher Governance

> **B4R5 supersession:** `8190dbb` B4R4 and its bootstrap-test route are frozen nonrouting
> provenance. B4R5 is the sole current seven-blob pre-subject route: its separately committed
> approved clean-checkout review record is required before S5. The exact B4R5 contract, seven-path
> baseline, preserved 15-path S5 allowlist, direct-import rule, deferred `step-creator` threads, and
> S5's three future regression groups are authoritative in `correction-b4r5-plan.md`.

> **B4R4 current execution truth:** `8b87aab` B4R3 clean-checkout review failed. B0–B4R3,
> S1–S4, T1–T4, V1–V4, normal/recovery records and their active, pending, schema, blocker and
> checklist semantics are frozen nonrouting history. The two `step-creator` threads remain
> deferred. B4R4 is the sole current pre-subject route: clean review of committed eight-blob B4R4,
> then S5, T5 and V5 only.

## Goal / Outcome

完成 current-topic governance correction：以一次性明定的 bootstrap test adaptation 讓 B4R4 成為可由
獨立 Plan-Reviewer clean-checkout 審查的八 blob 非 subject baseline，之後只允許 immutable S5 與
fresh B4R4 T5/V5 evidence chain，並保持 Human boundary。

## Scope

- **In scope:** B4R4 的七個 planning paths；唯一一次把 declared conformance test 作為第八 baseline
  path 的 fixed bootstrap adaptation；approved B4R4 review 後，S5 的 exact preserved 15-path
  allowlist；以及 B4R4 exact T5/V5 evidence paths。
- **Out of scope:** frozen epoch 修改或重讀、legacy migration、`step-creator` threads、任何未列
  path、產品/architecture work、PR thread action、merge、release、post-merge。

## Locked Decisions

- B4R3 failed review and all prior epochs are frozen non-subject provenance; B4R4 and its separately
  committed review record are also non-subject; only S5 can establish `implementation_subject_sha`.
- B4R4 bootstrap exception only permits Independent Implementer, before Plan-Reviewer, to adapt
  `tests/test_observer_dispatcher_governance_contract.py` to fixed B4R4 acceptance assertions and
  commit it with the seven planning paths. It cannot create subject, evidence, routing, status, or a
  ninth path.
- Direct imports remain mandatory; `importlib`, `__import__` and `sys.modules` substitutions are
  forbidden.
- Actual named Git graph queries—not `HEAD` or textual inference—must prove exactly
  `S5 -> T5 -> V5` and named `S5..V5`.
- This is non-stable, review-ready-only work: README, VERSION, release and tag are excluded.

## Boundaries / Exclusions

Observer bootstrap-dispatches Planner only; Planner is the sole routing authority. Plan-Creator writes
the seven planning artifacts only; Independent Implementer performs the bounded B4R4 bootstrap test
adaptation/commits and later S5; Tester and Reviewer independently write only declared evidence.
Frozen B2/B3/B4/B4R/B4R2/B4R3 records have no
current route, status, gate or pending meaning.

## Status / Allowed Transitions

Current status is `needs-rework` / `PLANNER_REPLAN`. The sole executable route is:
`B4R4 eight-blob review -> S5 -> T5 -> V5 -> human-check`. Any contract failure returns to Planner; no prior
epoch is a fallback.

## Artifact Paths

| Artifact | Exact path | Write owner | Decision authority | Role |
| --- | --- | --- | --- | --- |
| Shared workflow | `plan/agent-handoff-workflow.md` | Plan-Creator | Planner | B4R4 contract |
| Shared contract | `plan/topic-plan-contract.md` | Plan-Creator | Planner | B4R4 contract |
| Parent plan | `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md` | Plan-Creator | Planner | Current execution truth |
| Parent spec | `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md` | Plan-Creator | Planner | Acceptance contract |
| Parent step | `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md` | Plan-Creator | Planner | Current tracker |
| B4R4 plan | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r4-plan.md` | Plan-Creator | Planner | B4R4 delta |
| B4R4 step | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r4-step.md` | Plan-Creator | Planner | B4R4 tracker |
| Bootstrap test | `tests/test_observer_dispatcher_governance_contract.py` | Independent Implementer | Planner | B4R4 eighth baseline blob only |
| B4R4 review | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r4-review-log.md` | Plan-Reviewer | Plan-Reviewer verdict; Planner route | Pre-S5 gate |
| T5 evidence | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r4-tester-evidence.md` | Tester | Factual test result only | First descendant |
| V5 evidence | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r4-implementation-review-log.md` | Reviewer | Reviewer verdict; Planner route | Final descendant |

After separately committed approved B4R4 review, S5 may modify exactly:

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

1. Independent Implementer applies only B4R4 fixed test adaptation and commits exactly the eight
   baseline paths; B4R4 remains non-subject.
2. Independently review actual eight B4R4 blobs from a clean checkout and separately commit approved
   B4R4 review evidence.
3. Make one non-merge S5 changing only the exact allowlist above.
4. Write fresh B4R4 T5 then V5 as the two evidence-only descendants, with actual named-SHA
   topology/range verification.

## Validation / Acceptance Checks

- B4R4 baseline diff from `8b87aab` is reported with `git diff --name-status 8b87aab..<B4R4-SHA>`
  and lists exactly the eight Artifact Paths through `Bootstrap test`, with no extra path.
- B4R4 test adaptation reads shared workflow/contract, parent plan/spec/step and B4R4 plan/step; it
  fails closed if B4R3/prior epochs are not frozen, B4R4 is subject, eight baseline paths or clean
  eight-blob review changes, S5 allowlist changes, direct imports are replaced, `step-creator` is not
  deferred, or B4R4 evidence/topology/range is wrong.
- B4R4 review covers exactly its eight committed paths and is approved before S5.
- S5 is the only implementation subject and has no path outside the preserved 15-path allowlist.
- T5 and V5 attest the same S5; V5 requires passing T5; each evidence path is exact.
- Actual Git commands prove non-merge `S5 -> T5 -> V5` and `git diff --name-status S5..V5` lists
  exactly the two B4R4 evidence paths.
- Tests fail closed for prior epochs as route/subject, changed S5 allowlist, dynamic import
  substitution, incorrect evidence topology, range, merge or third descendant.

## Reviewer Handoff

```json
{"current_route":"B4R4-eight-blob-review->S5->T5->V5","b4r4_review_path":"plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r4-review-log.md","implementation_subject":"S5 only","range":"S5..V5","verdict":"approved|needs-rework"}
```

The B4R4 review schema and T5/V5 evidence schemas are defined by
`plan/topic-plan-contract.md#b4r4-correction-evidence-schemas`.

## Post-merge / release actions

Stop at the Human boundary; none are authorized.

## Open Questions / Unresolved Items

Only the current B4R4 review and successor S5/T5/V5 gates remain; frozen history creates none.
