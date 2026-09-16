---
topic: canonical-identity-pipeline
correction_id: canonical-identity-pipeline/pr-comment-review-and-fix
phase: p7-status-alignment-review-pending
created: 2026-09-16
---

# PRCF1 — canonical PR comment review and fix correction plan

## Trigger and current truth

PR #6 has nine independently inspected review threads. Seven require a bounded correction to the
canonical pipeline or its routing-state documentation; two concern the `pyproject.toml`/`uv.lock`
version mismatch. Human explicitly directed that `uv.lock` be restored to HEAD and neither modified
nor committed. It is restored cleanly to
`1123deae24fc37f6755e3eae810d453c40552f9d` and is read-only throughout PRCF1.

C7S's independent approval receipt is committed at
`1123deae24fc37f6755e3eae810d453c40552f9d`. That receipt and C0–C7 are frozen completed
provenance; C8 remains Planner-only Phase 4.5. PRCF1 is a new, Human-authorized correction route
and cannot reuse any CAVO1, CSO1, or C7S Plan-Reviewer, Tester, or independent Reviewer evidence.

PRCF1 P0 is the clean ten-path candidate `bbf3bde597b1adbf074ef832802a6151c330752a`. Independent
Plan-Reviewer wrote its approved P1 receipt, and Independent Implementer committed that unchanged
receipt as sole P2 evidence at `618be901c8313447b88e9fec513dea6beb59e534`, a non-merge direct
child of P0. The P2 status-sync candidate `fbdbe901a84630089e07792f15b79fb0e67b0861` and its
committed approved one-path receipt `4a4a99165cdc37a3bae6931e0fb2249ad5f0ab3a` are complete
frozen facts. P3 is the completed exact two-path subject
`b8c7cc6050b3c5a44333a1fde9d3ee07145966f5`. The committed P3 status-sync candidate
`2e8fc3230805bf6a09239f8225585cb59d1d22a3` and its discarded untracked receipt are superseded
nonrouting provenance. P3 status-alignment candidate
`d430493b068608171043a7794d86c549bfc8b6fc` is rejected immutable nonrouting provenance: its
independent review found only this stale frontmatter phase, formerly
`p2-status-sync-review-pending`. Phase-repair candidate
`90fc41117b6ff9969c2ea9161d0952b2814b597d` and its committed approved receipt
`c1751ac832c6b08f2173e1d51627f70cad0e0ca3` are complete frozen facts. P4 factual passing
evidence and P5's sole evidence-only commit are both
`dff14f3fdc0a06bf907ea82074e02862a05a36d1`, binding P3. The P5 status-sync candidate
`7a604e27d5fc00089b9c00ebeec3a142bb5ea861` and its unchanged approved sole receipt commit
`ff19d0aeda3305e6bc743930827408122d18a55a` are complete frozen facts. P6's approved review log
is committed unchanged by P7 at `24ef18b835b7646e05bf0fc3f5828349eea52b1d`. P7 status-sync
candidate `850c1e66f2d2dc339620ca86e03660f1faef9331` is rejected immutable nonrouting
provenance: its uncommitted review outcome is not a receipt and is neither committed, consumed,
nor reusable. The active P7 status-alignment phase-repair route corrects only that state; P8 Phase
4.5 is pending and Planner-only. P9–P11 have not started. This route establishes no alignment
result, classification, reply, resolution, publish, or merge authority.

## Locked implementation scope

After a committed approved PRCF1 plan-review receipt, the immutable implementation subject modifies
exactly these paths:

1. `src/deterministic_response_cache/identity/canonical.py`
2. `tests/test_canonical_identity_pipeline.py`

The implementation must:

- Require `type(name) is str` for every top-level `IdentityField.name` and mapping key before
  sorting; a `str` subclass is rejected with the existing non-string field/key issue and its
  comparator must not run.
- Reject `U+D800` through `U+DFFF` in all exact built-in canonical-string positions—field name,
  mapping key, and scalar string—using `surrogate-code-point`, while retaining deterministic issue
  aggregation and Validator short-circuit.
- Keep valid non-BMP Unicode. For `{"value": "\U0001f600"}`, assert the exact ASCII Encoder
  output `["identity",[[["str","value"],["str","\ud83d\ude00"]]]]`, the identical strict-ASCII
  Serializer bytes, and SHA-256
  `02c41d0e0019f532fef8e908145a6fdde13c471e23d3a64c2d70a8ef6b3372a6`.
- Recognize a Builder list snapshot only through exact private type identity
  `type(value) is _SnapshotList`; no attribute/sentinel name lookup or subtype acceptance is
  permitted. A tuple subclass spoofing `_canonical_identity_list = True` must retain the `tuple`
  grammar tag.
- Preserve direct imports, nominal Protocol bases, public `@override` markers, all existing public
  contracts, Builder injection, valid map order, list/tuple boundary, and the public Encoder string
  / Serializer bytes handoff.

Every other tracked path is read-only, including `contracts.py`, `builders.py`, exports, all
non-dedicated tests, diagrams, `README.md`, `pyproject.toml`, and `uv.lock`. No dependency,
version, API, profile, diagram, publish, new PR, merge, release, tag, or post-merge change is
authorized.

## Candidate admission

The Plan-Creator candidate is a clean non-merge direct child of
`1123deae24fc37f6755e3eae810d453c40552f9d` and changes exactly these ten paths:

```text
M\tanalysis/canonical-identity-pipeline/technical-spec.md
M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c7-status-sync.correction-plan.md
M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c7-status-sync.correction-step.md
M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-plan.md
M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-step.md
M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md
A\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-plan.md
A\tplan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-step.md
M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.spec.md
M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.step.md
```

The candidate creates no JSON receipt, implementation subject, test evidence, implementation
review, classification record, reply, resolution, push, or PR action. An unlisted path, non-direct
or merge parent, dirty candidate, altered `uv.lock`, or prefilled outcome fails closed.

## Five correction artifacts and evidence order

| Order | Artifact | Exact path | Sole writer | Commit rule |
| --- | --- | --- | --- | --- |
| P0 | Correction plan | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-plan.md` | Plan-Creator | In the ten-path candidate only. |
| P0 | Correction step | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-step.md` | Plan-Creator | In the ten-path candidate only. |
| P1/P2 | Plan-review receipt | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-plan-review-log.json` | Independent Plan-Reviewer | Completed: written from clean P0 and committed unchanged as sole one-path P2 evidence at `618be901c8313447b88e9fec513dea6beb59e534`. |
| P4/P5 | Tester evidence | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-tester-evidence.json` | Tester | Completed factual P3 evidence, committed unchanged as the sole one-path P5 commit `dff14f3fdc0a06bf907ea82074e02862a05a36d1`. |
| P6/P7 | Implementation-review log | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-implementation-review-log.json` | Independent Reviewer | Completed approved P6 evidence, committed unchanged as sole one-path P7 evidence at `24ef18b835b7646e05bf0fc3f5828349eea52b1d`. |

P3 is completed at `b8c7cc6050b3c5a44333a1fde9d3ee07145966f5`. P3 status sync is superseded
nonrouting provenance: its receipt was untracked and discarded before review, commit, or reuse.
P3 status alignment at `d430493b068608171043a7794d86c549bfc8b6fc` is rejected immutable
nonrouting provenance because its review found the stale phase corrected by the separate
phase-repair route. Its candidate `90fc41117b6ff9969c2ea9161d0952b2814b597d` and receipt
`c1751ac832c6b08f2173e1d51627f70cad0e0ca3`, then P4/P5
`dff14f3fdc0a06bf907ea82074e02862a05a36d1`, P5 status-sync candidate
`7a604e27d5fc00089b9c00ebeec3a142bb5ea861` / receipt
`ff19d0aeda3305e6bc743930827408122d18a55a`, and P7 receipt commit
`24ef18b835b7646e05bf0fc3f5828349eea52b1d` are completed frozen facts. P7 status-sync candidate
`850c1e66f2d2dc339620ca86e03660f1faef9331` is rejected immutable nonrouting provenance; its
uncommitted review outcome cannot be reused. P8 is Planner-only Phase 4.5 after the committed
approved P7 status-alignment phase-repair receipt restores routing, using the PRCF1 same-subject
full SHA chain and existing Human authorization. It permits classification only; it never
authorizes approval, merge, release, tag, or post-merge.

## Evidence schemas

Each JSON object admits no extra or missing top-level key. SHA values are lowercase 40-hex values;
`approved` and `passing` require an empty `blocking_issues` where present, and any failing command
requires `status: "failing"`.

### P1 Plan-Reviewer receipt

```json
{
  "schema_version": "canonical-identity-pipeline.pr-comment-review-and-fix.correction-plan-review.v1",
  "topic": "canonical-identity-pipeline",
  "correction_id": "canonical-identity-pipeline/pr-comment-review-and-fix",
  "candidate_commit": "<40-hex P0>",
  "candidate_tree": "<40-hex P0 tree>",
  "reviewed_paths": [{"path": "<one of exact P0 paths>", "blob_sha": "<40-hex>"}],
  "first_parent_admission": {
    "candidate_commit": "<40-hex P0>",
    "candidate_tree": "<40-hex P0 tree>",
    "parent_commit": "1123deae24fc37f6755e3eae810d453c40552f9d",
    "non_merge": true,
    "first_parent": "1123deae24fc37f6755e3eae810d453c40552f9d",
    "exact_declared_paths": ["<ten exact P0 paths>"],
    "name_status": ["<ten exact P0 M/A tab-path entries>"]
  },
  "review_basis": "clean committed P0 tree; exact ten-path admission; locked PRCF1 scope and nine-thread triage",
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "copilot_feedback_triage": {"ADDRESS": ["<seven node IDs>"], "DISCUSS": [], "SKIP": ["<two node IDs>"]},
  "recorded_by": "Independent Plan-Reviewer"
}
```

`reviewed_paths` has exactly the ten paths in P0 order. `approved` requires all seven ADDRESS and
both SKIP IDs listed below, no DISCUSS IDs, the clean `uv.lock` restore, and no C8/publish/merge
claim.

### P4 Tester evidence

```json
{
  "schema_version": "canonical-identity-pipeline.pr-comment-review-and-fix.correction-tester.v1",
  "topic": "canonical-identity-pipeline",
  "correction_id": "canonical-identity-pipeline/pr-comment-review-and-fix",
  "implementation_subject_commit": "<40-hex P3>",
  "implementation_subject_paths": [
    "src/deterministic_response_cache/identity/canonical.py",
    "tests/test_canonical_identity_pipeline.py"
  ],
  "commands": [{"command": "<non-empty command>", "exit_code": 0}],
  "status": "passing|failing",
  "recorded_by": "Tester"
}
```

Commands must include the dedicated pipeline tests, existing direct-import Builder/contract tests,
Ruff format/check, Pyright, Tach, full pytest, and pre-commit. It records actual command strings and
integer exit codes; it is factual only and cannot classify or resolve comments.

### P6 independent implementation-review log

```json
{
  "schema_version": "canonical-identity-pipeline.pr-comment-review-and-fix.correction-implementation-review.v1",
  "topic": "canonical-identity-pipeline",
  "correction_id": "canonical-identity-pipeline/pr-comment-review-and-fix",
  "implementation_subject_commit": "<same 40-hex P3>",
  "tester_evidence_commit": "<40-hex P5>",
  "reviewed_tree": "<40-hex P5 tree>",
  "clean_worktree": true,
  "reviewed_paths": [
    "src/deterministic_response_cache/identity/canonical.py",
    "tests/test_canonical_identity_pipeline.py"
  ],
  "review_basis": "clean committed P5 tree; same-subject passing P4 evidence; exact-string, surrogate, non-BMP, snapshot-type, direct-import, and no-uv-lock-drift review",
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "copilot_feedback_triage": {"ADDRESS": ["<seven node IDs>"], "DISCUSS": [], "SKIP": ["<two node IDs>"]},
  "recorded_by": "Independent Reviewer"
}
```

## Nine-thread classification, reply, and resolution route

Only after P8, Independent Reviewer may write
`plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.thread-classification.json`.
It binds P3, P5, P7, PR #6, and every exact node/comment identifier below. Its exact schema is:

```json
{
  "schema_version": "canonical-identity-pipeline.pr-comment-review-and-fix.thread-classification.v1",
  "topic": "canonical-identity-pipeline",
  "correction_id": "canonical-identity-pipeline/pr-comment-review-and-fix",
  "pull_request": 6,
  "implementation_subject_commit": "<40-hex P3>",
  "tester_evidence_commit": "<40-hex P5>",
  "implementation_review_commit": "<40-hex P7>",
  "threads": [
    {"node_id": "<PRRC node ID>", "comment_id": 0, "classification": "addressed-and-resolvable|skip-not-resolvable", "reason": "<non-empty factual reason>"}
  ],
  "recorded_by": "Independent Reviewer"
}
```

It contains exactly nine thread entries, in the table order. Independent Implementer commits the
unchanged record as a sole one-path classification-evidence commit before any reply or resolve API
action. Then, and only then, Implementer posts the fixed bounded reply appropriate to each exact
thread and resolves only `addressed-and-resolvable` entries. A `skip-not-resolvable` entry receives
the Human-decision reply but remains unresolved.

| Node ID | Comment ID | Disposition | Bounded final reply |
| --- | ---: | --- | --- |
| `PRRC_kwDOUJTij87vvFvj` | 4022098915 | ADDRESS | `Addressed by PRCF1: exact built-in str validation now rejects subclass field names and mapping keys before sorting; regression proves the comparator is not invoked.` |
| `PRRC_kwDOUJTij87vvFvo` | 4022098920 | ADDRESS | `Addressed by PRCF1: surrogate code points are rejected in every canonical-string position, while valid non-BMP Unicode has an exact ASCII encoding/bytes/hash regression.` |
| `PRRC_kwDOUJTij87vvFvu` | 4022098926 | ADDRESS | `Addressed by PRCF1 planning state: C7S receipt is recorded as completed historical provenance and C8 remains Planner-only.` |
| `PRRC_kwDOUJTij87vvF0O` | 4022099214 | ADDRESS | `Addressed by PRCF1: only exact private _SnapshotList type identity denotes a snapshotted list; attribute-spoofing tuple subclasses remain tuples.` |
| `PRRC_kwDOUJTij87vvF0q` | 4022099242 | ADDRESS | `Addressed by PRCF1 planning state: all C7S surfaces now record the committed receipt consistently; PRCF1 uses fresh evidence.` |
| `PRRC_kwDOUJTij87vvF0_` | 4022099263 | ADDRESS | `Addressed by PRCF1 planning state: the parent tracker records the committed C7S receipt and keeps C8 Planner-only.` |
| `PRRC_kwDOUJTij87vvF1r` | 4022099307 | ADDRESS | `Addressed by PRCF1: the dedicated suite proves valid non-BMP input's exact ASCII Encoder string, Serializer bytes, and literal SHA-256.` |
| `PRRC_kwDOUJTij87vvFve` | 4022098910 | SKIP | `Per explicit Human decision, uv.lock remains restored to HEAD and is neither modified nor committed in this topic.` |
| `PRRC_kwDOUJTij87vvF1V` | 4022099285 | SKIP | `Per explicit Human decision, uv.lock remains restored to HEAD and is neither modified nor committed in this topic.` |

The first seven may be resolved only if the P9 classification says
`addressed-and-resolvable`. The two SKIP rows are never resolvable under this route. Classification,
reply, and resolution do not grant PR approval, merge, release, tag, post-merge, or final summary.

## Stop conditions

Return to Planner for an unclear thread mapping, code/test scope beyond P3, changed public contract,
dynamic import, missing all-position surrogate coverage, wrong non-BMP literal hash, spoofable list
recognition, or an attempt to change/commit `uv.lock`. Missing or non-passing same-subject evidence
is `blocked`; conflicting candidate, subject, evidence, or thread identity is `human-check`.
