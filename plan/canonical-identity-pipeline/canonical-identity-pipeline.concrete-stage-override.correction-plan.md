---
topic: canonical-identity-pipeline
correction_id: canonical-identity-pipeline/concrete-stage-override
phase: c7-status-sync-plan-review
created: 2026-09-15
---

# CSO1 — Concrete-stage named inheritance and `@override` correction plan

## Trigger and current truth

Human requires the delivered concrete stages to declare their existing Protocol relationship
nominally and to mark their one public Protocol implementation with Python 3.12 `@override`.
This is a narrow correction to the open `canonical-identity-pipeline` draft PR #6, not a change to
the canonical grammar, Builder orchestration, public handoffs, or identity ownership.

The parent technical specification, topic plan, topic specification, and step tracker were updated
by C0. C0 is the immutable six-path candidate
`82bb4413f0f53e912b4cf30abb65b5a13c84a93a`; its approved C1 log binds tree
`e2e4c638b74205b7cb158e1c8f92e592970a03bb`. C2 is the immutable sole-evidence commit
`15c23d67856b627fa8f736eb66694cccc9e5ec89`, a non-merge direct child of C0 whose exact one-path
diff adds the unchanged approved C1 log. These facts, the log, and its recorded reviewed blobs are
frozen; no later role may rewrite, re-review, or use them as C3 Tester or Reviewer evidence.

The rejected status-only route is C0S `46b707c209839f64935beb08e4db8a1b565c8114`: its C1S JSON
schema used double-escaped tab text, preventing parsed `name_status` values from matching Git.
C0S-R1 repaired that contract, and the unchanged approved C1S receipt was committed as sole C2S
evidence `be0ce355dc777d63b7454488989452183519490a`. C1S/C2S are frozen complete facts.

 C3 is the immutable two-path subject `cbee5f23310b973d9e52e4e1c662ca1d9f9169d8`, a non-merge
 direct child of C2S. C3S candidate `0d6f46aca2acefccd64f56c3c537f50fae00bab9` and its committed
 approved receipt `2428e27ecb402efa90fd43e8ba979d615e151cd2` are complete frozen status facts.
 Tester wrote passing same-subject C4 evidence, which C5 committed unchanged as sole evidence-only
 commit `cbc53e953a257766f918a9c1f54db66c97ab5eba`. C5S candidate
 `2d042543d60a40519e174326462a6739f9b19f6c` and its committed approved receipt
 `92f7db262bec8d774f1c6f8b1b2b16aaa82b624e` are complete frozen facts. C6 wrote approved review
 evidence and C7 committed it unchanged as sole evidence-only commit
 `e4a2e67f29a4562f6244c5031498426b610d0a91`. C7S's independent approval receipt is committed at
 `1123deae24fc37f6755e3eae810d453c40552f9d`; it is completed frozen provenance and C8 Phase 4.5
 remains Planner-only pending. The prior original
 six-path subject and all CAVO1 records remain frozen provenance: they cannot be reused as a CSO1
 candidate, Tester record, or Reviewer record.

## Locked scope

- The new CSO1 immutable implementation subject changes exactly these two paths:
  1. `src/deterministic_response_cache/identity/canonical.py`
  2. `tests/test_canonical_identity_pipeline.py`
- `canonical.py` imports `override` only from Python 3.12 `typing`. It makes the five concrete
  classes directly and explicitly inherit, respectively, `Validator`, `Sorter`, `Encoder`,
  `Serializer`, and `Hasher` from the existing `contracts.py`; it does not alter that module.
- Only `PureTypeValidator.validate`, `CanonicalSorter.sort`, `CanonicalEncoder.encode`,
  `CanonicalSerializer.serialize`, and `SHA256Hasher.hash` receive `@override`. Private class
  helpers (`_validate_value`, `_validate_sequence`, `_validate_mapping`, `_sort_value`,
  `_encode_value`, `_encode_scalar`) and all module helpers/factories remain unmarked.
- The dedicated test preserves every existing direct import and pipeline regression. It adds direct
  nominal assertions for each named base (`stage.__bases__ == (expected_protocol,)`),
  `stage_method.__override__ is True` on each matching public method, and
  `getattr(private_helper, "__override__", False) is False` for every private class helper. It uses
  no `importlib`, `__import__`, or `sys.modules` substitution.
- `contracts.py`, `builders.py`, `identity/__init__.py`, every existing test other than the one
  dedicated module, both Archify artifacts, README, `pyproject.toml`, `uv.lock`, and all historic
  planning/evidence files are read-only for C3. No new API, export, dependency, diagram, version,
  publish file, or new PR is authorized.

## Completed C7S status-synchronization boundary

- C7S changed exactly eight planning paths: completed C5S plan/step, paired C7S plan/step, this
  CSO1 correction plan/step, and the parent plan/step. Its independent approval receipt is now
  committed at `1123deae24fc37f6755e3eae810d453c40552f9d`; C7S is completed provenance and C8
  remains Planner-only pending.
- C7S is a completed non-merge direct child whose sole first parent is C7
  `e4a2e67f29a4562f6244c5031498426b610d0a91`. Its first-parent name-status diff contains
  exactly once, in lexical path order, the following entries:

  ```text
  M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c5-status-sync.correction-plan.md
  M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c5-status-sync.correction-step.md
  A\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c7-status-sync.correction-plan.md
  A\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c7-status-sync.correction-step.md
  M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-plan.md
  M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-step.md
  M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md
  M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.step.md
  ```

- The receipt's completed commit is
  `1123deae24fc37f6755e3eae810d453c40552f9d`; `README.md`, `pyproject.toml`, and `uv.lock` remain
  outside C7S. No subsequent role may rewrite C7S history, claim C8 completion, or use its receipt
  as PRCF1 Plan-Reviewer, Tester, or implementation-review evidence.

## Acceptance delta

CSO1 passes only when all of the following are true:

1. Each concrete stage's direct named base is exactly its matching existing Protocol.
2. The five matching public stage methods, and only those methods among class helpers, expose
   `__override__ is True`.
3. The existing exact Encoder-string, Serializer-bytes, validation, deterministic, composition,
   direct-import, and Builder regression behavior continues unchanged.
4. The immutable C3 diff has exactly the two declared paths; no CAVO1 evidence or subject is
   referenced as CSO1 evidence.
5. Required tests and static checks complete with exit code 0, then CSO1 receives a fresh
   same-subject passing Tester record and independent approved Reviewer record.

## Exact correction artifacts and evidence order

| Order | Artifact | Exact path | Writer | Authority / condition |
| --- | --- | --- | --- | --- |
| C0 | Parent technical specification | `analysis/canonical-identity-pipeline/technical-spec.md` | Plan-Creator | Completed immutable six-path CSO1 candidate surface. |
| C0 | Parent topic plan | `plan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md` | Plan-Creator | Completed candidate's current route and path contract. |
| C0 | Parent topic specification | `plan/canonical-identity-pipeline/canonical-identity-pipeline.spec.md` | Plan-Creator | Completed testable nominal-inheritance and marker contract. |
| C0 | Parent step tracker | `plan/canonical-identity-pipeline/canonical-identity-pipeline.step.md` | Plan-Creator | CSO1 progression truth, synchronized by C5S only. |
| C0 | Correction plan | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-plan.md` | Plan-Creator | This CSO1 trigger, scope, ordering, and schema authority; synchronized by C5S only. |
| C0 | Correction step | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-step.md` | Plan-Creator | CSO1 execution/evidence tracking; synchronized by C5S only. |
| C1 | Correction Plan-Reviewer log | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-plan-review-log.json` | Independent Plan-Reviewer | Completed approved record, committed unchanged by C2; frozen provenance for all later steps. |
| C2 | Committed C1 evidence | same C1 path | Independent Implementer | Completed sole-evidence commit `15c23d67856b627fa8f736eb66694cccc9e5ec89`; frozen provenance. |
| C0S-R1/C1S/C2S | Completed status-sync route | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-status-sync.correction-plan-review-log.json` | Independent Plan-Reviewer; Independent Implementer | Approved receipt and sole evidence-only commit `be0ce355dc777d63b7454488989452183519490a`; frozen provenance. |
| C3 | Immutable implementation subject | `src/deterministic_response_cache/identity/canonical.py`, `tests/test_canonical_identity_pipeline.py` | Implementer | Complete two-path subject `cbee5f23310b973d9e52e4e1c662ca1d9f9169d8`; no evidence is in this commit. |
| C3S | Completed status-sync route | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c3-status-sync.correction-plan-review-log.json` | Plan-Creator; Independent Plan-Reviewer; Independent Implementer | Completed candidate `0d6f46aca2acefccd64f56c3c537f50fae00bab9` and committed approved receipt `2428e27ecb402efa90fd43e8ba979d615e151cd2`; frozen status provenance. |
| C4 | Correction Tester evidence | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-tester-evidence.json` | Tester | Completed passing same-subject factual evidence for C3; frozen as committed by C5. |
| C5 | Committed C4 evidence | same C4 path | Independent Implementer | Completed sole evidence-only commit `cbc53e953a257766f918a9c1f54db66c97ab5eba`. |
| C5S | Completed status-sync route | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c5-status-sync.correction-plan-review-log.json` | Plan-Creator; Independent Plan-Reviewer; Independent Implementer | Candidate `2d042543d60a40519e174326462a6739f9b19f6c` and committed approved receipt `92f7db262bec8d774f1c6f8b1b2b16aaa82b624e`; frozen status provenance. |
| C6 | Completed implementation-review log | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-implementation-review-log.json` | Independent Reviewer | Approved same-subject review evidence; frozen as committed by C7. |
| C7 | Committed C6 evidence | same C6 path | Independent Implementer | Completed sole evidence-only commit `e4a2e67f29a4562f6244c5031498426b610d0a91`. |
| C7S | Status-sync candidate | completed C5S plan/step, paired C7S plan/step, this CSO1 plan/step, and parent plan/step | Plan-Creator | Completed exact eight-path non-merge direct child of C7. |
| C7S review/receipt | Status-sync Plan-Reviewer log | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c7-status-sync.correction-plan-review-log.json` | Independent Plan-Reviewer | Completed sole C7S review artifact, committed at `1123deae24fc37f6755e3eae810d453c40552f9d`; frozen provenance. |
| C8 | Phase 4.5 alignment | no new CSO1 artifact | Planner | Pending until committed approved C7S receipt; C7S declares no C8 outcome. |

`needs-rework` in C7S review returns to Planner. An approved C7S receipt does not re-review C3 or
decide C8; it only restores Planner authority to select pending Phase 4.5. A rework starts a fresh
C3 subject and repeats C3S/C4–C7; no prior C4/C5/C6/C7 can be reused. Missing evidence is
`blocked`; competing candidate, evidence, subject, or worktree facts are `human-check`.

## Completed C7S and successor boundary

The C7S independent approval receipt is now committed at
`1123deae24fc37f6755e3eae810d453c40552f9d`; its one-path evidence commit is completed frozen
provenance. C8 remains Planner-only Phase 4.5 and is not completed or selected by this update.

PRCF1 is a separate Human-authorized correction route, declared in
`canonical-identity-pipeline.pr-comment-review-and-fix.correction-plan.md`. It cannot reuse C3/C4/
C5/C6/C7/C7S as its plan-review, Tester, or implementation-review evidence. The old CSO1 subject,
its public `@override` contract, and every historic evidence path remain read-only.

## Extended evidence schemas

These schemas supersede generic parent evidence shapes only for CSO1. Every object has exactly the
listed top-level keys. Commit and tree IDs are complete lowercase 40-hex SHA values. Every command
entry has exactly a non-empty string `command` and integer `exit_code`. Extra, missing, malformed,
cross-topic, cross-correction, or cross-subject fields fail closed.

### C1 correction Plan-Reviewer log

`reviewed_paths` contains exactly the six C0 paths in the table order; every entry has exactly
`path` and `blob_sha`. `approved` requires an empty `blocking_issues`; `needs-rework` requires at
least one issue.

```json
{
  "schema_version": "canonical-identity-pipeline.concrete-stage-override.correction-plan-review.v1",
  "topic": "canonical-identity-pipeline",
  "correction_id": "canonical-identity-pipeline/concrete-stage-override",
  "candidate_commit": "<40-hex C0 commit>",
  "candidate_tree": "<40-hex C0 tree>",
  "reviewed_paths": [
    {"path": "analysis/canonical-identity-pipeline/technical-spec.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.spec.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.step.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-plan.md", "blob_sha": "<40-hex>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-step.md", "blob_sha": "<40-hex>"}
  ],
  "review_basis": "clean committed C0 tree; explicit Human override; exact CSO1 two-path subject and fresh evidence route",
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "copilot_feedback_triage": {"ADDRESS": [], "DISCUSS": [], "SKIP": []},
  "recorded_by": "Independent Plan-Reviewer"
}
```

### C1S status-sync correction Plan-Reviewer log — frozen provenance

The C1S schema below is frozen historical provenance. The approved receipt is at the declared C1S
path and its unchanged sole-evidence C2S commit is
`be0ce355dc777d63b7454488989452183519490a`; it creates neither a C3S review outcome nor any C4
Tester, Reviewer, publish, PR, or Human-review authority.

The C1S file is committed frozen provenance. Its schema remains documented only to explain the
completed C1S/C2S binding and must not be reused as C3 Tester or Reviewer evidence.

### C3S status-sync correction Plan-Reviewer log — frozen provenance

The independent C3S Plan-Reviewer created
`plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c3-status-sync.correction-plan-review-log.json`,
after the C3S candidate was committed and from its clean checkout. It is one JSON object with
exactly twelve top-level keys: `schema_version`, `topic`, `correction_id`, `candidate_commit`,
`candidate_tree`, `reviewed_paths`, `first_parent_admission`, `review_basis`, `verdict`,
`blocking_issues`, `copilot_feedback_triage`, and `recorded_by`. The six `reviewed_paths` entries
are ordered exactly as the C3S name-status list and contain only `path` and `blob_sha`.
`first_parent_admission` contains only `candidate_commit`, `candidate_tree`, `parent_commit`,
`non_merge`, `first_parent`, `exact_declared_paths`, and `name_status`. All Git identifiers are
lowercase 40-hex values. `approved` requires empty `blocking_issues`; `needs-rework` requires at
least one non-empty issue.

```json
{
  "schema_version": "canonical-identity-pipeline.concrete-stage-override-c3-status-sync.correction-plan-review.v1",
  "topic": "canonical-identity-pipeline",
  "correction_id": "canonical-identity-pipeline/concrete-stage-override-c3-status-sync",
  "candidate_commit": "<40-hex C3S commit>",
  "candidate_tree": "<40-hex C3S tree>",
  "reviewed_paths": [
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c3-status-sync.correction-plan.md", "blob_sha": "<40-hex C3S blob>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c3-status-sync.correction-step.md", "blob_sha": "<40-hex C3S blob>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-plan.md", "blob_sha": "<40-hex C3S blob>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-step.md", "blob_sha": "<40-hex C3S blob>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md", "blob_sha": "<40-hex C3S blob>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.step.md", "blob_sha": "<40-hex C3S blob>"}
  ],
  "first_parent_admission": {
    "candidate_commit": "<same 40-hex C3S commit>",
    "candidate_tree": "<same 40-hex C3S tree>",
    "parent_commit": "cbee5f23310b973d9e52e4e1c662ca1d9f9169d8",
    "non_merge": true,
    "first_parent": true,
    "exact_declared_paths": true,
    "name_status": [
      "A\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c3-status-sync.correction-plan.md",
      "A\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c3-status-sync.correction-step.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-plan.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-step.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.step.md"
    ]
  },
  "review_basis": "clean committed C3S candidate checkout; direct non-merge first-parent admission from C3 cbee5f23310b973d9e52e4e1c662ca1d9f9169d8; C3S name_status parses to the exact two A-tab-path and four M-tab-path entries; state surfaces agree on C1S/C2S be0ce355dc777d63b7454488989452183519490a and C3 cbee5f23310b973d9e52e4e1c662ca1d9f9169d8 complete, C4 pending, C5-C8 not started; no Tester, Reviewer, Phase 4.5, push, PR, or Human review claim",
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "copilot_feedback_triage": {"ADDRESS": [], "DISCUSS": [], "SKIP": []},
  "recorded_by": "Independent Plan-Reviewer"
}
```

The C3S record is frozen provenance: it is neither C4 Tester evidence nor C6 Reviewer evidence.
It documented the clean C3 direct-child admission that preceded C4 and C5; it cannot be rewritten,
re-reviewed, or used to decide C6.

### C5S status-sync correction Plan-Reviewer log

Only the independent C5S Plan-Reviewer may create
`plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c5-status-sync.correction-plan-review-log.json`,
only after the C5S candidate is committed and from its clean checkout. It is one JSON object with
exactly twelve top-level keys: `schema_version`, `topic`, `correction_id`, `candidate_commit`,
`candidate_tree`, `reviewed_paths`, `first_parent_admission`, `review_basis`, `verdict`,
`blocking_issues`, `copilot_feedback_triage`, and `recorded_by`. The six `reviewed_paths` entries
are ordered exactly as the C5S name-status list and contain only `path` and `blob_sha`.
`first_parent_admission` contains only `candidate_commit`, `candidate_tree`, `parent_commit`,
`non_merge`, `first_parent`, `exact_declared_paths`, and `name_status`. All Git identifiers are
lowercase 40-hex values. `approved` requires empty `blocking_issues`; `needs-rework` requires at
least one non-empty issue.

```json
{
  "schema_version": "canonical-identity-pipeline.concrete-stage-override-c5-status-sync.correction-plan-review.v1",
  "topic": "canonical-identity-pipeline",
  "correction_id": "canonical-identity-pipeline/concrete-stage-override-c5-status-sync",
  "candidate_commit": "<40-hex C5S commit>",
  "candidate_tree": "<40-hex C5S tree>",
  "reviewed_paths": [
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c5-status-sync.correction-plan.md", "blob_sha": "<40-hex C5S blob>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c5-status-sync.correction-step.md", "blob_sha": "<40-hex C5S blob>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-plan.md", "blob_sha": "<40-hex C5S blob>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-step.md", "blob_sha": "<40-hex C5S blob>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md", "blob_sha": "<40-hex C5S blob>"},
    {"path": "plan/canonical-identity-pipeline/canonical-identity-pipeline.step.md", "blob_sha": "<40-hex C5S blob>"}
  ],
  "first_parent_admission": {
    "candidate_commit": "<same 40-hex C5S commit>",
    "candidate_tree": "<same 40-hex C5S tree>",
    "parent_commit": "cbc53e953a257766f918a9c1f54db66c97ab5eba",
    "non_merge": true,
    "first_parent": true,
    "exact_declared_paths": true,
    "name_status": [
      "A\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c5-status-sync.correction-plan.md",
      "A\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c5-status-sync.correction-step.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-plan.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-step.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md",
      "M\tplan/canonical-identity-pipeline/canonical-identity-pipeline.step.md"
    ]
  },
  "review_basis": "clean committed C5S candidate checkout; direct non-merge first-parent admission from C5 cbc53e953a257766f918a9c1f54db66c97ab5eba; C5S name_status parses to the exact two A-tab-path and four M-tab-path entries; state surfaces agree on committed C3S candidate/receipt, passing C4 evidence for C3 cbee5f23310b973d9e52e4e1c662ca1d9f9169d8, C5 cbc53e953a257766f918a9c1f54db66c97ab5eba, C6 pending, C7-C8 not started; no Reviewer, Phase 4.5, push, PR, or Human review claim",
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "copilot_feedback_triage": {"ADDRESS": [], "DISCUSS": [], "SKIP": []},
  "recorded_by": "Independent Plan-Reviewer"
}
```

The C5S reviewer must fail closed for an uncommitted/dirty candidate, a parent other than C5, a
merge, unlisted path, malformed or non-tab `name_status`, inconsistent C3S/C4/C5/C6–C8 state, or
any downstream completion claim. The review log is neither prewritten nor part of C5S. Only an
Independent Implementer may commit an unchanged approved receipt as the sole evidence receipt
commit; only then may Planner route Reviewer for C6.

### C4 correction Tester evidence

`implementation_subject_paths` is exactly the two C3 paths in the stated order. `passing` requires
every command exit code to be 0; `failing` requires at least one non-zero exit code. Tester verifies
the C3 commit's exact two-path name-status before running the direct-import and pipeline regressions,
format/lint/type/architecture/full-test/pre-commit checks.

```json
{
  "schema_version": "canonical-identity-pipeline.concrete-stage-override.correction-tester-evidence.v1",
  "topic": "canonical-identity-pipeline",
  "correction_id": "canonical-identity-pipeline/concrete-stage-override",
  "implementation_subject_commit": "<40-hex C3 SHA>",
  "implementation_subject_paths": [
    "src/deterministic_response_cache/identity/canonical.py",
    "tests/test_canonical_identity_pipeline.py"
  ],
  "status": "passing|failing",
  "commands": [{"command": "<exact command>", "exit_code": 0}],
  "recorded_by": "Tester"
}
```

### C6 correction implementation-review log

`reviewed_paths` is exactly the two C3 paths in the stated order. `approved` requires
`clean_worktree: true`, committed same-subject C4 `status: "passing"`, an empty
`blocking_issues`, named base/marker assertions, preserved direct imports, and no scope drift.
`needs-rework` requires at least one blocking issue.

```json
{
  "schema_version": "canonical-identity-pipeline.concrete-stage-override.correction-implementation-review.v1",
  "topic": "canonical-identity-pipeline",
  "correction_id": "canonical-identity-pipeline/concrete-stage-override",
  "implementation_subject_commit": "<same 40-hex C3 SHA>",
  "tester_evidence_commit": "<40-hex C5 SHA>",
  "reviewed_tree": "<40-hex C5 tree>",
  "clean_worktree": true,
  "reviewed_paths": [
    "src/deterministic_response_cache/identity/canonical.py",
    "tests/test_canonical_identity_pipeline.py"
  ],
  "review_basis": "clean committed C5 tree; same-subject passing C4 evidence; CSO1 nominal Protocol base, public override marker, private-helper, direct-import, and scope verification",
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "copilot_feedback_triage": {"ADDRESS": [], "DISCUSS": [], "SKIP": []},
  "recorded_by": "Independent Reviewer"
}
```

## Required CSO1 validation

Tester records the actual commands and exit codes for the following checks; exact C3 scope must be
verified before their execution:

```bash
git diff-tree --no-commit-id --name-status -r <C3-full-SHA>
uv run pytest tests/test_canonical_identity_pipeline.py tests/test_model_feature_identity_contracts.py tests/test_model_feature_identity_builders.py
uv run ruff format --check .
uv run ruff check .
uv run pyright
uv run tach check
uv run pytest
uv run pre-commit run --all-files
```

No Archify command runs for CSO1. A required non-zero result is factual `failing` evidence and
returns to Planner; it is never described as success.
