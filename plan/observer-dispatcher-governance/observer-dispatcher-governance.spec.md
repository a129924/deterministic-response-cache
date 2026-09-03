# Observer / Dispatcher Governance Specification

## B6R11 Acceptance Criteria

1. `B6R11 -> R21 -> S16 -> T16 -> V16 -> Q16 -> thread-classification -> human-check` is the sole current route.
2. B6R11 is a non-subject, non-merge, first-parent exact-five planning baseline: the three parent artifacts and the
   B6R11 plan/step. Pre-admission B6R11/R21 commit, tree, blob, HEAD, and outcome claims are prohibited.
3. R21 independently records the committed B6R11 candidate/tree and a machine-enforced `reviewed_artifacts` tuple
   list of exactly five ordered named path/blob records: the three parent paths, then the B6R11 plan and step. Every
   blob is a lowercase 40-hex SHA, and the ordered tuple path list must equal the B6R11 first-parent exact-five diff;
   it also records admission, Copilot triage, verdict/blockers, and B6R10/R20 frozen receipt verification.
4. B6R10 `785eed2` and R20 `8b5e8dad1eda02e5effa3e1cb6555efe3c8cd87c` are frozen provenance; R20 review blob
   `3d1a4941…` has the decoded literal-backslash-`t` defect and is `routing_valid:false`,
   `FROZEN_INVALID_NOT_ROUTING`.
5. Only a separately committed unchanged R21 with `verdict: approved`, one active candidate, and
   `effective_committed_state:R21_COMPLETE_S16_NEXT` authorizes S16. A needs-rework R21 has no route authorization.
6. S16 remains the sole test-path change and retains direct imports. `importlib`, `__import__`, and `sys.modules`
   substitution are prohibited.
7. The B6R10 T16/V16/Q16 exact semantic schemas, evidence paths, S16->T16->V16 topology, actual Git full-triple
   validation, and classification-only Q16 boundary remain the descendant contract.
8. Q16 never authorizes thread resolution, Human review, merge, release, or post-merge.

## Failure Conditions

The contract fails closed if B6R10/R20 is routed; B6R11 is merge/not-exact-five; R21 lacks required
candidate/tree/blob/admission/receipt/triage/verdict fields; `reviewed_artifacts` has any cardinality other than five,
any other order or path name, a non-40-lowercase-hex blob, or does not equal the B6R11 first-parent exact-five diff;
pre-admission artifacts claim post-commit facts; S16 runs before committed approved R21; S16 widens the path or
replaces direct imports; a descendant changes the retained B6R10 schema; or Q16 gains lifecycle, resolution, PR, or
merge authority.

## Non-goals

No B6R10/R20 recovery or amendment, earlier-provenance migration, step-creator work, thread resolution, merge,
release, post-merge action, architecture work, or unlisted implementation path belongs to B6R11.
