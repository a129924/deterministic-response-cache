# Observer / Dispatcher Governance Specification

## B6R13 Acceptance Criteria

1. `B6R13 -> R23 -> S17 -> T17 -> V17 -> Q17 -> thread-classification -> comment-resolve -> human-check` is the sole current route.
2. B6R13 is a non-subject, non-merge, first-parent exact-eight planning baseline: `AGENTS.md`, the two shared contracts,
   parent plan/spec/step and B6R13 plan/step. Pre-admission B6R13/R23 commit, tree, blob, HEAD and outcome claims are prohibited.
3. R23 validates exactly eight path/blob and identical first-parent name-status facts, one candidate commit/tree, frozen
   B6R12/R22/S16-Q16 receipt, Copilot triage, verdict and blockers. Only independently committed unchanged approved R23
   gives active candidate `R23_COMPLETE_S17_NEXT` / `S17`; needs-rework is inactive with nonempty blockers and null route.
4. S17 changes exactly fourteen paths: four `.codex/agents` wrappers, plan-creator SKILL/checklist/template,
   plan-reviewer SKILL/checklist/reference/examples, Python workflow/template, and governance test. It enforces one Planner
   bootstrap/no self-route, Plan-Creator-only planning write, independent factual Tester, same-subject Tester-consuming
   Reviewer, bounded no-merge Implementer, read-only Explorer and templates consistent with `pr-open` Human boundary.
5. Direct imports are preserved. `importlib`, `__import__`, and `sys.modules` substitution is prohibited.
6. T17/V17/Q17 are fresh B6R13 evidence paths. V17 requires committed same-S17 passing T17; Q17 validates committed
   S17/T17/V17 actual full SHA triple, parents, topology/range/name-status and only permits classification. Q17 neither
   resolves threads nor authorizes Human review, merge, release or post-merge.
7. Only an independent explicit per-thread `addressed-and-resolvable` classification permits an Implementer to leave a
   bounded reply and resolve that exact thread. The route stops at human-check.

## Frozen B6R12 Acceptance Criteria

1. `B6R12 -> R22 -> S16 -> T16 -> V16 -> Q16 -> thread-classification -> human-check` is frozen predecessor provenance.
2. B6R12 is a non-subject, non-merge, first-parent exact-five planning baseline: B6R12 plan, B6R12 step, parent plan,
   parent spec and parent step, in lexical name-status order. Pre-admission B6R12/R22 commit, tree, blob, HEAD and
   outcome claims are prohibited.
3. R22 is validated by the B6R12 correction plan's executable full Draft 2020-12 JSON Schema. Its actual
   `reviewed_artifacts` value is an exact five-record array in lexical `A`, `A`, `M`, `M`, `M` path order and its
   `first_parent_admission.name_status` is the identical exact-five lexical array; both use `prefixItems`,
   `minItems:5`, `maxItems:5`, and `items:false`. Every candidate/tree/parent/blob is lowercase 40-hex.
4. R22 records B6R11 `995c5a8` with absent R21 as frozen nonrouting provenance, and preserves R20 as
   `FROZEN_INVALID_NOT_ROUTING`.
5. Only a separately committed unchanged R22 with `verdict: approved`, active candidate, empty blockers, and
   `effective_committed_state:R22_COMPLETE_S16_NEXT` authorizes S16. needs-rework must be inactive with nonempty
   blockers and null route authorization.
6. S16 remains the sole test-path change and retains direct imports. `importlib`, `__import__`, and `sys.modules`
   substitution are prohibited.
7. The B6R10 T16/V16/Q16 exact semantic schemas, evidence paths, S16->T16->V16 topology, actual Git full-triple
   validation, and classification-only Q16 boundary remain the descendant contract.
8. Q16 never authorizes thread resolution, Human review, merge, release, or post-merge.

## Failure Conditions

The B6R13 contract fails closed if a stale route is current; B6R13 is merge/not-exact-eight; R23 has precommit facts,
missing candidate/tree/blob/admission/receipt/triage/verdict/blocker fields or inconsistent conditional values; S17
widens its fourteen paths, omits a runtime role boundary, turns Explorer writable, sends Planner to itself, allows a
Reviewer without same-subject passing Tester evidence, permits Implementer merge, or lets a template bypass `pr-open`.
It also fails if direct imports are replaced, T17/V17/Q17 use frozen paths, Q17 is before committed V17, or Q17 grants
resolution or merge authority.

The contract fails closed if B6R11/R21 or B6R10/R20 is routed; B6R12 is merge/not-exact-five; R22 lacks required
candidate/tree/blob/admission/receipt/triage/verdict/blocker fields; the executable schema or actual `reviewed_artifacts`
value lacks exact five `prefixItems`, permits additional items, has any other order/path, a non-40-lowercase-hex blob,
or `first_parent_admission.name_status` differs from the B6R12 lexical first-parent diff; pre-admission artifacts claim
post-commit facts; conditional verdict fields are inconsistent; S16 runs
before committed approved R22; S16 widens the path or
replaces direct imports; a descendant changes the retained B6R10 schema; or Q16 gains lifecycle, resolution, PR, or
merge authority.

## Non-goals

No B6R12/R22/S16-Q16 or B6R10/R20 recovery/amendment, earlier-provenance migration, step-creator work, merge, release,
post-merge action, architecture work, or unlisted implementation path belongs to B6R13. Q17 itself does not resolve threads.
