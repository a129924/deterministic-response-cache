# Observer / Dispatcher Governance Specification

## B6R12 Acceptance Criteria

1. `B6R12 -> R22 -> S16 -> T16 -> V16 -> Q16 -> thread-classification -> human-check` is the sole current route.
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

The contract fails closed if B6R11/R21 or B6R10/R20 is routed; B6R12 is merge/not-exact-five; R22 lacks required
candidate/tree/blob/admission/receipt/triage/verdict/blocker fields; the executable schema or actual `reviewed_artifacts`
value lacks exact five `prefixItems`, permits additional items, has any other order/path, a non-40-lowercase-hex blob,
or `first_parent_admission.name_status` differs from the B6R12 lexical first-parent diff; pre-admission artifacts claim
post-commit facts; conditional verdict fields are inconsistent; S16 runs
before committed approved R22; S16 widens the path or
replaces direct imports; a descendant changes the retained B6R10 schema; or Q16 gains lifecycle, resolution, PR, or
merge authority.

## Non-goals

No B6R11/R21 or B6R10/R20 recovery or amendment, earlier-provenance migration, step-creator work, thread resolution,
merge, release, post-merge action, architecture work, or unlisted implementation path belongs to B6R12.
