# canonical-identity-pipeline

## Goal / Outcome

Deliver the Identity BC's official v1 concrete canonical pipeline. A Python consumer can use
exported stages or a default existing Builder to turn valid model/feature sources into stable
`ModelIdentity`, `FeatureIdentity`, and `CompleteRequestIdentity` hashes without changing the
current injected-Builder contract.

## Scope

| Field | Contract |
| --- | --- |
| In-Scope | Historical delivery: five concrete stages, two default-builder factories, the cycle-safe private snapshot adjustment, exports, dedicated tests, a delivered Archify dataflow diagram, and publish-time README/version promotion. Completed CSO1 C3 adds only nominal Protocol inheritance and `@override` markers in the five concrete stages plus their direct regression assertions. C7S is completed frozen status provenance; PRCF1 adds exact-string/surrogate/snapshot-type corrections, dedicated regressions, and bounded nine-thread classification/reply routing. The P8–P10 recovery is planning-only: it restores a valid route without changing code, tests, `uv.lock`, or PR threads. |
| Out-Of-Scope | Provider extraction, Response Reuse, CacheStore, runtime retention, model execution, provider adapters, persistence, telemetry, configurable/profile-versioned formats, migration, and cache-key policy. |
| ReadOnly | Existing Protocol signatures, value-object fields, keyword-only Builder injection signatures, existing direct-import tests, root package surface, `identity/.gitkeep`, BC ownership/source-of-truth architecture files, `builders.py`, `identity/__init__.py`, both Archify artifacts, `README.md`, `pyproject.toml`, and `uv.lock` during CSO1. C0–C7, rejected C0S, C0S-R1/C1S/C2S, C3S, C5S, C7S's committed receipt, and all historical evidence are frozen. |
| Written | `identity/canonical.py`, dedicated pipeline tests, Archify source/HTML, planning artifacts, and later role-owned CAVO1 evidence files. |
| Modify | Historical subject: `identity/builders.py` private snapshot traversal and `identity/__init__.py` exports; `README.md` and `pyproject.toml` only at `publish-in-progress`. Completed CSO1 C3 subject: only `identity/canonical.py` and `tests/test_canonical_identity_pipeline.py`; active C7S changes only its declared eight planning paths. |
| Deleted | No tracked file. Untracked Archify visual-check sidecars are removed before the subject commit. |
| TestCase | Valid/invalid PureType; issue aggregation; short-circuit; mapping order; type/list-tuple distinction; exact Encoder strings; Serializer bytes; `-0.0`; independent processes; factories; composition; direct imports; diagram receipts. |

The analysis layer is complete: `analysis/canonical-identity-pipeline/requirements.md` is the
business-intent guardrail and `analysis/canonical-identity-pipeline/technical-spec.md` is the
execution-facing authority. This plan maps to that technical specification without adding
alternative work.

## Locked Decisions

- This is an Identity BC-only, stable-library-affecting topic. Identity remains the unique authority
  for model and complete-request identity; no adjacent BC may reimplement the rules.
- v1 is a public type-tagged canonical JSON-like grammar. It accepts only `None`, `bool`, `int`,
  finite `float`, `str`, recursive list/tuple, and string-keyed mappings; `-0.0` normalizes to
  `0.0`; mapping/field ordering is Unicode code-point order; Unicode text is not normalized.
- Existing `Validator`, `Sorter`, `Encoder`, `Serializer`, `Hasher`, value objects, and the
  two Builder injection signatures remain unchanged. On `Failure`, later stages do not run.
- `CanonicalEncoder.encode(SortedIdentity) -> EncodedIdentity` always hands off a canonical
  JSON-like `str` in `EncodedIdentity.value`, never a Python list/dictionary/intermediate object.
  `CanonicalSerializer` alone converts that string to ASCII `bytes`.
- Required value-grammar examples are exactly `1 → '["int","1"]'`,
  `True → '["bool",true]'`, and
  `[1, "x"] → '["list",[["int","1"],["str","x"]]]'`.
- SHA-256 produces the 64-character lowercase hexadecimal `Hash`.
- Public additions are `PureTypeValidator`, `CanonicalSorter`, `CanonicalEncoder`,
  `CanonicalSerializer`, `SHA256Hasher`, `default_model_identity_builder()`, and
  `default_feature_identity_builder()`.
- CSO1 uses Python 3.12 `from typing import override`. `PureTypeValidator`,
  `CanonicalSorter`, `CanonicalEncoder`, `CanonicalSerializer`, and `SHA256Hasher` explicitly
  inherit `Validator`, `Sorter`, `Encoder`, `Serializer`, and `Hasher`, respectively. Only
  `validate`, `sort`, `encode`, `serialize`, and `hash`, respectively, receive `@override`.
  Private helpers, factories, Protocols, value objects, and Builder injection are not changed or
  decorated.
- The concrete profile is v1 only: no negotiation, configurable policy, migration, or silent future
  change is authorized.
- The implementation includes a static Archify dataflow diagram after Python code/test work; it
  explains only this Identity pipeline and its `Failure` short-circuit.
- PRCF1 preserves the public API and every Protocol/value-object/Builder signature. It tightens
  canonical strings to exact built-in `str`, rejects Unicode surrogate code points at field-name,
  mapping-key, and scalar-string positions with `surrogate-code-point`, preserves valid non-BMP
  Unicode, and recognizes only the exact private `_SnapshotList` type as a snapshotted source list.
  `uv.lock` is read-only under an explicit Human decision.

## Boundaries / Exclusions

- `builders.py` may change only its private snapshot traversal, solely to ensure a cyclic invalid
  runtime input reaches Validator as `Failure`; its public methods, valid-data snapshots, aggregate
  composition, and injection behavior remain unchanged.
- `contracts.py` is read-only; new classes structurally satisfy its existing Protocols rather than
  changing those Protocols or their value objects.
- Existing direct imports, fixtures, mocks, and assertions remain direct and unchanged. No
  `importlib`, `__import__`, or `sys.modules` substitution is permitted.
- Diagram files are a topic-local flow visualization, not a revision to the repository's BC
  architecture authority. CacheStore, response reuse, runtime, execution, and provider paths are
  excluded from both code and diagram.
- CAVO1 is completed historical provenance. Its diagrams and all CAVO1 Plan-Reviewer, Tester, and
  Reviewer evidence are not CSO1 routing authority and cannot be reused.
- CSO1 C0 is the immutable six-path candidate `82bb4413f0f53e912b4cf30abb65b5a13c84a93a`.
  Its C1 log is an approved record that binds that exact commit, tree, and reviewed blobs. CSO1 C2
  is the immutable sole-evidence commit `15c23d67856b627fa8f736eb66694cccc9e5ec89`: it is a
  non-merge direct child of C0 and adds only the unchanged C1 log. These facts are frozen.
- C0S `46b707c209839f64935beb08e4db8a1b565c8114` remains rejected frozen provenance because its
  C1S schema double-escaped each tab. Its direct child C0S-R1 was independently reviewed, and the
  unchanged approved C1S receipt was committed as sole evidence C2S
  `be0ce355dc777d63b7454488989452183519490a`. C1S/C2S are frozen complete facts.
- CSO1 C3 is the immutable two-path implementation subject
  `cbee5f23310b973d9e52e4e1c662ca1d9f9169d8`. C3S candidate
  `0d6f46aca2acefccd64f56c3c537f50fae00bab9` and its one-path committed approved receipt
  `2428e27ecb402efa90fd43e8ba979d615e151cd2` are complete frozen status facts. C4 factual
  passing Tester evidence for C3 was committed unchanged by C5
  `cbc53e953a257766f918a9c1f54db66c97ab5eba`; C5 is the sole evidence-only commit and is frozen.
  C5S candidate `2d042543d60a40519e174326462a6739f9b19f6c` and its committed approved receipt
  `92f7db262bec8d774f1c6f8b1b2b16aaa82b624e` are complete frozen status facts. C6 wrote the
  approved same-subject review log and C7 committed it unchanged as the sole evidence-only commit
  `e4a2e67f29a4562f6244c5031498426b610d0a91`. C7S's direct-child status candidate was reviewed
  and its independent approval receipt is committed at
  `1123deae24fc37f6755e3eae810d453c40552f9d`. C7S is complete frozen provenance; C8 Phase 4.5
  remains pending and Planner-only without a claimed outcome.
- A path not listed below is a plan-alignment stop and returns to Planner.

## Status / Allowed Transitions

- **Current**: `pr-comment-review-and-fix-p8-p10-route-recovery-review-pending`; CSO1 C0/C1/C2,
  C1S/C2S `be0ce355dc777d63b7454488989452183519490a`, C3
  `cbee5f23310b973d9e52e4e1c662ca1d9f9169d8`, committed C3S receipt
  `2428e27ecb402efa90fd43e8ba979d615e151cd2`, C5
  `cbc53e953a257766f918a9c1f54db66c97ab5eba`, C5S receipt
  `92f7db262bec8d774f1c6f8b1b2b16aaa82b624e`, and C7
  `e4a2e67f29a4562f6244c5031498426b610d0a91`, and C7S receipt
  `1123deae24fc37f6755e3eae810d453c40552f9d` are complete historical facts. C8 Phase 4.5 is
  pending and Planner-only. PRCF1 P0 candidate `bbf3bde597b1adbf074ef832802a6151c330752a`,
  its approved P1 receipt, and its sole P2 receipt-evidence commit
  `618be901c8313447b88e9fec513dea6beb59e534` are complete facts. The P2 status-sync candidate
  `fbdbe901a84630089e07792f15b79fb0e67b0861` and its committed approved sole receipt
  `4a4a99165cdc37a3bae6931e0fb2249ad5f0ab3a` are complete facts. P3 is the committed exact
  two-path implementation subject `b8c7cc6050b3c5a44333a1fde9d3ee07145966f5`. The original P3
  status-sync candidate `2e8fc3230805bf6a09239f8225585cb59d1d22a3` is superseded nonrouting
  provenance: its untracked receipt was discarded before review, commit, or reuse. The P3
  status-alignment candidate `d430493b068608171043a7794d86c549bfc8b6fc` is rejected immutable
  nonrouting provenance: its independent review found only that the PRCF1 correction-plan
  frontmatter still declared `p2-status-sync-review-pending`. The phase-repair candidate
  `90fc41117b6ff9969c2ea9161d0952b2814b597d` and its committed approved receipt
  `c1751ac832c6b08f2173e1d51627f70cad0e0ca3` are complete frozen facts. P4 factual passing
  evidence and P5's sole one-path evidence-only commit are both
  `dff14f3fdc0a06bf907ea82074e02862a05a36d1`, binding the P3 subject. The P5 status-sync
  candidate `7a604e27d5fc00089b9c00ebeec3a142bb5ea861` and its unchanged approved sole receipt
  commit `ff19d0aeda3305e6bc743930827408122d18a55a` are complete frozen facts. P6's approved
  same-subject implementation-review log is committed unchanged by P7 at
  `24ef18b835b7646e05bf0fc3f5828349eea52b1d`. P7 status-sync candidate
  `850c1e66f2d2dc339620ca86e03660f1faef9331` is rejected immutable nonrouting provenance: its
  uncommitted review outcome is not a receipt and is neither committed, consumed, nor reusable.
  P7 status-alignment phase-repair candidate `87eb3de65d6b5a4efaef745d23e5d6cc34c70c59` and its
  unchanged approved sole receipt commit `40824056def6c9d3402e95039af6a931b67ee547` are complete
  frozen facts. P7 receipt-status-sync candidate `8ac6bd76ff85d04c16407518105dc023180871ef` and
  its approved sole receipt commit `49c0bcd197c6b9ac4fb1baba115c903060ff52cf` are complete
  frozen facts. They preserve the same P3 `b8c7cc6050b3c5a44333a1fde9d3ee07145966f5` → P5
  `dff14f3fdc0a06bf907ea82074e02862a05a36d1` → P7
  `24ef18b835b7646e05bf0fc3f5828349eea52b1` evidence chain and made only Planner P8 the next
  action. The direct child `18d9b4751df26376c9cf47fe7968130870f07fe7` is structurally correct
  but pre-P8 immutable nonrouting provenance; it neither completes P8/P10 nor is yet superseded.
  The active P8–P10 route-recovery candidate awaits its sole independent Plan-Reviewer receipt.
  After its one-path receipt commit, Planner redoes P8, then fresh P9 writes the declared recovery
  classification and P10 commits it alone. Draft PR #6 remains open and CAVO1 is completed
  historical provenance.
- **Execution model**: CSO1 C0 → approved C1 log → sole-evidence C2 commit → rejected C0S →
  C0S-R1 → approved C1S receipt / sole-evidence C2S commit → immutable C3 subject → C3S six-path
  direct-child candidate → committed approved C3S receipt → C4 Tester evidence → sole-evidence C5
  commit → C5S six-path direct-child candidate → independent C5S Plan-Reviewer receipt →
  sole-evidence C5S receipt commit → Planner route to CSO1 C6 Reviewer → sole-evidence C7 review
  commit → C7S eight-path direct-child candidate → independent C7S Plan-Reviewer receipt →
  committed C7S receipt `1123deae24fc37f6755e3eae810d453c40552f9d` → Planner C8 Phase 4.5
  alignment → PRCF1 P0 → approved P1 receipt → sole P2 receipt-evidence commit → independent
  review and sole evidence-only P2 status-sync receipt commit → immutable P3 subject →
  superseded P3 status-sync provenance → rejected P3 status-alignment provenance → phase-repair
  candidate `90fc41117b6ff9969c2ea9161d0952b2814b597d` / sole receipt
  `c1751ac832c6b08f2173e1d51627f70cad0e0ca3` → passing P4 / sole P5 evidence
  `dff14f3fdc0a06bf907ea82074e02862a05a36d1` → P5 status-sync candidate
  `7a604e27d5fc00089b9c00ebeec3a142bb5ea861` / sole receipt
  `ff19d0aeda3305e6bc743930827408122d18a55a` → approved P6 / sole P7 receipt commit
  `24ef18b835b7646e05bf0fc3f5828349eea52b1d` → rejected P7 status-sync candidate
  `850c1e66f2d2dc339620ca86e03660f1faef9331` / uncommitted nonreceipt review outcome → P7
  status-alignment phase-repair candidate `87eb3de65d6b5a4efaef745d23e5d6cc34c70c59` / sole
  approved repair receipt commit `40824056def6c9d3402e95039af6a931b67ee547` → P7
  status-alignment receipt status-sync candidate `8ac6bd76ff85d04c16407518105dc023180871ef` /
  approved sole receipt commit `49c0bcd197c6b9ac4fb1baba115c903060ff52cf` → pre-P8 structural
  but immutable nonrouting `18d9b4751df26376c9cf47fe7968130870f07fe7` → P8–P10 route-recovery
  ten-path candidate / independent receipt / sole receipt commit → Planner redoes P8 → fresh P9
  classification → sole P10 commit → P11 route. Only a later authorized Implementer may update
  existing draft PR #6; Human reviews and merges.
- **Allowed transitions**:
  - `planned` → `creator-in-progress`
  - `creator-in-progress` → `tester-in-progress`
  - `tester-in-progress` → `review-ready`
  - `review-ready` → `reviewer-in-progress`
  - `reviewer-in-progress` → `approved`
  - `reviewer-in-progress` → `needs-rework`
  - `needs-rework` → `creator-in-progress`
  - `approved` → `creator-in-progress`
  - `approved` → `publish-in-progress`
  - `publish-in-progress` → `pr-open`
  - `pr-open` → `needs-rework`
  - `pr-open` → `merged`
  - `merged` → terminal
- CSO1 Tester evidence must bind the same full immutable two-path implementation subject consumed by
  CSO1 Reviewer. The CSO1 correction Plan defines the extended correction evidence schemas; CAVO1
  and generic parent Tester/Reviewer evidence paths are inactive for this route.
  `publish-in-progress` can only become `pr-open`; only Human can merge from `pr-open`. Human
  also exclusively owns release, tag, post-merge, and final summary.

## Artifact Paths

| Artifact | Path | Write owner | Decision authority and role |
| --- | --- | --- | --- |
| Requirements analysis | `analysis/canonical-identity-pipeline/requirements.md` | Plan-Creator | Business-intent guardrail for this planning candidate. |
| Technical specification | `analysis/canonical-identity-pipeline/technical-spec.md` | Plan-Creator | Execution-facing source of truth for this candidate. |
| Topic plan | `plan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md` | Plan-Creator | Canonical execution contract. |
| Topic specification | `plan/canonical-identity-pipeline/canonical-identity-pipeline.spec.md` | Plan-Creator | Testable behavior and edge-case contract. |
| Step tracker | `plan/canonical-identity-pipeline/canonical-identity-pipeline.step.md` | Plan-Creator; later Implementer only for implementation markers | Progression truth; only its implementation section is the completion gate. |
| Plan-review receipt | `plan/canonical-identity-pipeline/canonical-identity-pipeline.plan-review-receipt.json` | Independent Plan-Reviewer | Committed approved candidate evidence before Planner may route implementation. |
| CAVO1 correction plan | `plan/canonical-identity-pipeline/canonical-identity-pipeline.archify-visual-overflow.correction-plan.md` | Plan-Creator | Historical trigger, locked two-path scope, round cap, and extended evidence-schema authority. |
| CAVO1 correction step | `plan/canonical-identity-pipeline/canonical-identity-pipeline.archify-visual-overflow.correction-step.md` | Plan-Creator | Historical correction execution/evidence sequence. |
| CAVO1 correction Plan-Reviewer log | `plan/canonical-identity-pipeline/canonical-identity-pipeline.archify-visual-overflow.correction-plan-review-log.json` | Independent Plan-Reviewer | Independent clean-tree review of the committed CAVO1 candidate; an Implementer separately commits unchanged approved evidence. |
| Concrete stages/factories | `src/deterministic_response_cache/identity/canonical.py` | Implementer | Public first-party v1 stage implementations and default existing-Builder factories. |
| Snapshot adapter | `src/deterministic_response_cache/identity/builders.py` | Implementer | Private cycle-safe invalid-input handoff; no public API/orchestration change. |
| Identity exports | `src/deterministic_response_cache/identity/__init__.py` | Implementer | Bounded re-export of the seven declared public additions. |
| Pipeline tests | `tests/test_canonical_identity_pipeline.py` | Implementer | Dedicated direct-import behavior, determinism, invalid-input, and composition coverage. |
| Archify dataflow source | `docs/architecture/canonical-identity-pipeline.dataflow.json` | Implementer | Showcase-quality Identity pipeline diagram specification. |
| Delivered dataflow viewer | `docs/architecture/canonical-identity-pipeline.html` | Implementer | Delivered static interactive diagram. |
| README API promotion | `README.md` | Implementer, only at `publish-in-progress` | Public API table row and current-stage wording after all prerequisite gates. |
| Version promotion | `pyproject.toml` | Implementer, only at `publish-in-progress` | `[project].version` minor bump from `0.0.0` to `0.1.0`. |
| CAVO1 Tester evidence | `plan/canonical-identity-pipeline/canonical-identity-pipeline.archify-visual-overflow.correction-tester-evidence.json` | Tester | Factual same-subject CAVO1 validation; an independent Implementer commits unchanged passing evidence as the sole evidence-only commit. |
| CAVO1 implementation review log | `plan/canonical-identity-pipeline/canonical-identity-pipeline.archify-visual-overflow.correction-implementation-review-log.json` | Independent Reviewer | Same-subject CAVO1 review after committed passing Tester evidence, from a clean committed tree; an independent Implementer commits unchanged approved evidence as the sole evidence-only commit. |
| CSO1 correction plan | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-plan.md` | Plan-Creator | Active correction trigger, exact two-path subject, and CSO1 extended evidence-schema authority. |
| CSO1 correction step | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-step.md` | Plan-Creator | Active CSO1 execution and evidence sequence. |
| CSO1 correction Plan-Reviewer log | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-plan-review-log.json` | Independent Plan-Reviewer | Clean-tree review of this committed six-path candidate; an independent Implementer commits unchanged approved evidence as its sole evidence-only commit. |
| C0S-R1 correction plan | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-status-sync.correction-plan.md` | Plan-Creator | Status-only C0S-R1 admission, four-surface synchronization, and its v2 actual-tab review-log schema. |
| C0S-R1 correction step | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-status-sync.correction-step.md` | Plan-Creator | Rejected C0S, C0S-R1 candidate, review, evidence-only commit, and return-to-C3 tracker. |
| C0S-R1 correction Plan-Reviewer log | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-status-sync.correction-plan-review-log.json` | Independent Plan-Reviewer | The sole C0S-R1 review artifact; it is written only from a clean committed C0S-R1 checkout and then separately committed unchanged by an Independent Implementer. |
| C3S correction plan | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c3-status-sync.correction-plan.md` | Plan-Creator | Direct-child C3 status synchronization, six-path admission, and C3S review-receipt schema. |
| C3S correction step | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c3-status-sync.correction-step.md` | Plan-Creator | C3S candidate, review-receipt commit, and only then return to C4 Tester routing. |
| C3S correction Plan-Reviewer log | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c3-status-sync.correction-plan-review-log.json` | Independent Plan-Reviewer | Sole C3S review artifact, written from the clean committed six-path candidate and separately committed unchanged by an Independent Implementer. |
| C5S correction plan | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c5-status-sync.correction-plan.md` | Plan-Creator | Direct-child C5 status synchronization, six-path admission, and C5S review-receipt schema. |
| C5S correction step | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c5-status-sync.correction-step.md` | Plan-Creator | C5S candidate, review-receipt commit, and only then return to C6 Reviewer routing. |
| C5S correction Plan-Reviewer log | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c5-status-sync.correction-plan-review-log.json` | Independent Plan-Reviewer | Sole C5S review artifact, written from the clean committed six-path candidate and separately committed unchanged by an Independent Implementer. |
| C7S correction plan | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c7-status-sync.correction-plan.md` | Plan-Creator | Completed direct-child C7 status synchronization; frozen historical admission/schema record. |
| C7S correction step | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c7-status-sync.correction-step.md` | Plan-Creator | Completed C7S record; C8 remains Planner-only. |
| C7S correction Plan-Reviewer log | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c7-status-sync.correction-plan-review-log.json` | Independent Plan-Reviewer | Completed sole C7S review artifact, committed at `1123deae24fc37f6755e3eae810d453c40552f9d`; frozen provenance. |
| CSO1 concrete stage subject | `src/deterministic_response_cache/identity/canonical.py` | Implementer | Sole production-code path for named Protocol bases and the five public `@override` markers. |
| CSO1 concrete stage regression | `tests/test_canonical_identity_pipeline.py` | Implementer | Sole test path; keeps direct-import/pipeline regressions and proves named bases, public markers, and unmarked private helpers. |
| CSO1 Tester evidence | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-tester-evidence.json` | Tester | Factual same-subject validation only; an independent Implementer commits unchanged passing evidence as its sole evidence-only commit. |
| CSO1 implementation review log | `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-implementation-review-log.json` | Independent Reviewer | Same-subject CSO1 review after committed passing Tester evidence, from a clean committed tree; an independent Implementer commits unchanged approved evidence as its sole evidence-only commit. |
| PRCF1 correction plan | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-plan.md` | Plan-Creator | Exact ten-path candidate authority, PRCF1 scope, evidence schemas, and nine-thread route. |
| PRCF1 correction step | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-step.md` | Plan-Creator | P0–P11 state tracking; no route may skip a fresh same-subject gate. |
| PRCF1 Plan-Reviewer log | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-plan-review-log.json` | Independent Plan-Reviewer | Written only from clean committed P0; Independent Implementer separately commits unchanged approved evidence. |
| PRCF1 P2 status-sync correction plan | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p2-status-sync.correction-plan.md` | Plan-Creator | Completed six-path direct-child status synchronization for committed P0/P1/P2 facts; it introduced no implementation work. |
| PRCF1 P2 status-sync correction step | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p2-status-sync.correction-step.md` | Plan-Creator | Completed P2 status synchronization record; it restored routing to P3 only. |
| PRCF1 P2 status-sync Plan-Reviewer log | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p2-status-sync.correction-plan-review-log.json` | Independent Plan-Reviewer | Completed sole P2 status-sync review artifact, committed unchanged by an Independent Implementer at `4a4a99165cdc37a3bae6931e0fb2249ad5f0ab3a`. |
| PRCF1 P3 status-sync correction plan | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-sync.correction-plan.md` | Plan-Creator | Superseded eight-path candidate provenance; it created no committed receipt and cannot route P4. |
| PRCF1 P3 status-sync correction step | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-sync.correction-step.md` | Plan-Creator | Superseded tracking provenance; its untracked receipt was discarded and is nonrouting. |
| PRCF1 P3 status-sync Plan-Reviewer log | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-sync.correction-plan-review-log.json` | None | Discarded untracked file; it was never committed, consumed, or reusable evidence. |
| PRCF1 P3 status-alignment correction plan | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-alignment.correction-plan.md` | Plan-Creator | Rejected immutable nonrouting provenance at `d430493b068608171043a7794d86c549bfc8b6fc`; it cannot route P4. |
| PRCF1 P3 status-alignment correction step | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-alignment.correction-step.md` | Plan-Creator | Rejected alignment tracking provenance; its `needs-rework` result is not routing evidence. |
| PRCF1 P3 status-alignment Plan-Reviewer log | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-alignment.correction-plan-review-log.json` | None | No committed receipt is usable from rejected alignment provenance. |
| PRCF1 P3 status-alignment phase-repair correction plan | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-alignment-phase-repair.correction-plan.md` | Plan-Creator | Completed frozen eight-path phase-repair candidate `90fc41117b6ff9969c2ea9161d0952b2814b597d`. |
| PRCF1 P3 status-alignment phase-repair correction step | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-alignment-phase-repair.correction-step.md` | Plan-Creator | Completed frozen phase-repair tracking; its receipt commit restored routing only to P4. |
| PRCF1 P3 status-alignment phase-repair Plan-Reviewer log | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p3-status-alignment-phase-repair.correction-plan-review-log.json` | Independent Plan-Reviewer | Completed sole phase-repair receipt, committed unchanged at `c1751ac832c6b08f2173e1d51627f70cad0e0ca3`. |
| PRCF1 P5 status-sync correction plan | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p5-status-sync.correction-plan.md` | Plan-Creator | Completed frozen eight-path candidate `7a604e27d5fc00089b9c00ebeec3a142bb5ea861`; it introduced no implementation work. |
| PRCF1 P5 status-sync correction step | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p5-status-sync.correction-step.md` | Plan-Creator | Completed P5 state synchronization; its committed receipt restored routing to P6 only. |
| PRCF1 P5 status-sync Plan-Reviewer log | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p5-status-sync.correction-plan-review-log.json` | Independent Plan-Reviewer | Completed sole P5 status-sync receipt, committed unchanged at `ff19d0aeda3305e6bc743930827408122d18a55a`. |
| PRCF1 Tester evidence | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-tester-evidence.json` | Tester | Factual P3 evidence only; Independent Implementer separately commits unchanged passing evidence. |
| PRCF1 implementation-review log | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-implementation-review-log.json` | Independent Reviewer | Approved same-subject P6 evidence, committed unchanged by P7 at `24ef18b835b7646e05bf0fc3f5828349eea52b1d`. |
| PRCF1 P7 status-sync correction plan | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-sync.correction-plan.md` | Plan-Creator | Rejected immutable nonrouting provenance at `850c1e66f2d2dc339620ca86e03660f1faef9331`; its uncommitted review outcome is not reusable evidence. |
| PRCF1 P7 status-sync correction step | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-sync.correction-step.md` | Plan-Creator | Rejected P7 status-sync tracking provenance; it cannot route P8. |
| PRCF1 P7 status-sync Plan-Reviewer log | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-sync.correction-plan-review-log.json` | None | No committed receipt exists or is usable from rejected P7 status-sync provenance. |
| PRCF1 P7 status-alignment phase-repair correction plan | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-alignment-phase-repair.correction-plan.md` | Plan-Creator | Completed frozen eight-path phase repair at `87eb3de65d6b5a4efaef745d23e5d6cc34c70c59`. |
| PRCF1 P7 status-alignment phase-repair correction step | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-alignment-phase-repair.correction-step.md` | Plan-Creator | Completed frozen repair tracking; its receipt commit is `40824056def6c9d3402e95039af6a931b67ee547`. |
| PRCF1 P7 status-alignment phase-repair Plan-Reviewer log | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-alignment-phase-repair.correction-plan-review-log.json` | Independent Plan-Reviewer | Completed approved repair receipt, committed unchanged at `40824056def6c9d3402e95039af6a931b67ee547`. |
| PRCF1 P7 status-alignment receipt status-sync correction plan | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-alignment-receipt-status-sync.correction-plan.md` | Plan-Creator | Completed frozen eight-path status synchronization at `8ac6bd76ff85d04c16407518105dc023180871ef`; it creates no P8 result. |
| PRCF1 P7 status-alignment receipt status-sync correction step | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-alignment-receipt-status-sync.correction-step.md` | Plan-Creator | Completed tracking; approved sole receipt commit is `49c0bcd197c6b9ac4fb1baba115c903060ff52cf`. |
| PRCF1 P7 status-alignment receipt status-sync Plan-Reviewer log | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p7-status-alignment-receipt-status-sync.correction-plan-review-log.json` | Independent Plan-Reviewer | Completed sole status-sync receipt, committed unchanged at `49c0bcd197c6b9ac4fb1baba115c903060ff52cf`. |
| PRCF1 historical pre-P8 classification | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.thread-classification.json` | Independent Reviewer | Structurally correct immutable nonrouting provenance at `18d9b4751df26376c9cf47fe7968130870f07fe7`; it is not yet superseded and cannot route P10 or replies. |
| PRCF1 P8–P10 route-recovery correction plan | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p8-p10-route-recovery.correction-plan.md` | Plan-Creator | Exact ten-path direct-child recovery admission and sole receipt/classification contract. |
| PRCF1 P8–P10 route-recovery correction step | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p8-p10-route-recovery.correction-step.md` | Plan-Creator | Recovery state tracking; it cannot self-complete P8, P9, or P10. |
| PRCF1 P8–P10 route-recovery Plan-Reviewer log | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p8-p10-route-recovery.correction-plan-review-log.json` | Independent Plan-Reviewer | Sole future receipt, written only from the clean committed ten-path recovery candidate and then separately committed unchanged. |
| PRCF1 fresh P9 classification | `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix-p8-p10-route-recovery.thread-classification.json` | Independent Reviewer | Written only after redone Planner P8; Independent Implementer commits it unchanged as P10 before replies/resolutions. |

`README.md` and `pyproject.toml` are not part of the immutable implementation subject; they are
the stable-library promotion after Phase 4.5 and Human authorization. Archify visual-check contact
sheets and JSON sidecars are temporary untracked verification artifacts, not commit paths. Any
unlisted path, including a repository `VERSION` file that does not exist, requires Planner
alignment before modification.

## Stable library metadata

- **README row**: at `publish-in-progress`, add an Identity API table row identifying
  `deterministic_response_cache.identity`, its v1 concrete stages, and two default builder
  factories; revise the no-implementation baseline wording only enough to stay truthful.
- **VERSION bump**: minor, `0.0.0` → `0.1.0` in `[project].version` of `pyproject.toml`; this is
  the repository's version source because no `VERSION` file exists.
- **Timing**: `publish-in-progress`, only after same-subject passing Tester evidence, independent
  Reviewer approval, Planner Phase 4.5 alignment, and existing Human authorization.
- **Rationale**: the topic adds a new stable public identity API and canonical-format compatibility
  boundary.
- **Release notes**: no release-note file is created. Human decides any release publication, tag,
  and release notes after merge.

## Python implementation metadata

### Non-goals

- Do not modify existing Protocols, value-object fields, Builder signatures, or the root package API.
- Do not build provider-specific `IdentitySource` extraction, response reuse, CacheStore, runtime,
  model execution, provider integration, persistence, telemetry, or cache-key policy.
- Do not add dependencies, configurable/negotiated canonical profiles, profile migrations, or a
  separate versioned profile API.
- Do not alter existing direct-import tests or use dynamic import techniques.

### Current Context

`identity/contracts.py` defines all handoff values and five Protocols; `identity/builders.py`
provides injected model/feature orchestration and recursive valid-input snapshots;
`identity/__init__.py` exports the current public Identity API. Existing contract and Builder tests
directly import those symbols and must remain unchanged. `pyproject.toml` is the version source and
currently declares `0.0.0`.

### Requirements

1. Supply the seven declared public additions while structurally satisfying all existing Protocols.
2. Validate every discoverable invalid input and short-circuit all downstream stages on `Failure`.
3. Canonically sort fields/mappings, preserve scalar/container type distinctions and sequence order,
   normalize signed zero, encode ASCII canonical strings, and hash exact ASCII bytes with SHA-256.
4. Preserve existing Builder semantics while enabling cyclic invalid inputs to reach validation.
5. Prove deterministic outputs across fresh Python processes and complete-request composition.
6. Deliver and visually check the bounded dataflow diagram without changing architecture ownership.

### Decisions

- Async-planning status: exempt — cited exemption evidence: the declared paths implement synchronous
  in-memory traversal, encoding, hashing, static documentation, and a static diagram; no async
  boundary, resource lifecycle, concurrency, timeout, cancellation, or external I/O policy exists.
- Module/package placement: `src/deterministic_response_cache/identity/canonical.py` contains all
  concrete stages and default existing-Builder factories; the only existing source edit is the
  private snapshot helper in `identity/builders.py`.
- New public API: yes — five concrete stage classes plus
  `default_model_identity_builder() -> ModelIdentityBuilder` and
  `default_feature_identity_builder() -> FeatureIdentityBuilder`, re-exported by Identity.
- Interface changes: no — existing Protocol/value-object signatures and existing Builder
  constructors/methods remain byte-for-byte compatible in public shape.
- Breaking changes allowed: no — new API is additive; explicit injection continues to work.
- New dependencies: no — use only standard-library `hashlib`, `json`, `math`, and existing tools.
- Error-handling strategy: validator returns existing `Failure` with all discoverable
  `ValidationIssue` values; only invalid raw input yields `Failure`; no stage raises a new public
  domain exception.
- Typing strategy: Python 3.12 strict types using existing `PureType`, handoff values, and
  structural Protocol conformance; CSO1 adds direct nominal Protocol bases and `typing.override`
  only on their public contract methods; no `Any`, runtime type mutation, or public generic.

### Public Contract / API Changes

The seven public additions and exact signatures are in the technical specification. `Encoder` keeps
`encode(self, identity: SortedIdentity) -> EncodedIdentity`; `EncodedIdentity.value` remains
`str`; no list/dict handoff API is added. All existing public symbols and Builder signatures remain
compatible.

### Affected Files / Modules

**Written implementation paths:**

- `src/deterministic_response_cache/identity/canonical.py`
- `tests/test_canonical_identity_pipeline.py`
- `docs/architecture/canonical-identity-pipeline.dataflow.json`
- `docs/architecture/canonical-identity-pipeline.html`

**Modified implementation paths:**

- `src/deterministic_response_cache/identity/builders.py`
- `src/deterministic_response_cache/identity/__init__.py`

**Publish-only modified paths:**

- `README.md`
- `pyproject.toml`

**Read-only verification paths:**

- `src/deterministic_response_cache/identity/contracts.py`
- `tests/test_model_feature_identity_contracts.py`
- `tests/test_model_feature_identity_builders.py`
- `src/deterministic_response_cache/__init__.py`
- `src/deterministic_response_cache/identity/.gitkeep`
- `docs/business-capability-architecture.md`
- `docs/evolution-roadmap.md`
- `docs/architecture/business-capability/architecture-brief.md`
- `docs/architecture/business-capability/index.html`

**Active CSO1 correction subject:**

- `src/deterministic_response_cache/identity/canonical.py`
- `tests/test_canonical_identity_pipeline.py`

CSO1 must not modify any historical implementation/publish/diagram path, including `contracts.py`,
`builders.py`, `identity/__init__.py`, `README.md`, `pyproject.toml`, or `uv.lock`.

### Test Plan

- **Happy path:** assert each stage and both default factories yield the documented model, feature,
  and complete identities from valid nested input.
- **Invalid input:** assert all discoverable unsupported values, non-string keys/field names,
  non-finite floats, and cycles produce every corresponding `ValidationIssue` and no downstream
  calls.
- **Edge case:** assert mapping order is irrelevant; list/tuple and scalar types are distinct; nested
  structures preserve order; `-0.0 == 0.0`; non-ASCII strings become deterministic ASCII escapes;
  `EncodedIdentity.value` and `SerializedIdentity.value` match v1 grammar exactly.
- **Regression:** run both existing direct-import test modules unchanged; assert factories retain
  existing Builders' pipeline/aggregate behavior and cyclic invalid input no longer recurses before
  Validator.
- **Backward compatibility:** assert existing Protocol/VO/Builder signatures and every old export
  remain unchanged, while seven additions are direct imports; subprocess Python invocations prove
  the same hash in independent processes.
- **CSO1 nominal override regression:** assert each concrete class has its one exact named Protocol
  base; assert `validate`, `sort`, `encode`, `serialize`, and `hash` have the runtime
  `__override__` marker; assert every private helper in these classes lacks that marker; retain every
  direct-import and pipeline regression assertion.
- **Diagram TestCase:** require Archify source to describe every stage handoff and only the permitted
  failure branch, a showcase `validate`/successful `deliver`/visual-check receipt, and truthful
  manual contact-sheet review before cleanup.

### Risks

- Canonical bytes are public compatibility data; a grammar or float-format mistake would make later
  cache-key interoperability unsafe.
- A private snapshot-cycle change could regress existing immutable snapshots if valid containers leak.
- The viewer has a generated source JSON; post-delivery edits or committed visual-check sidecars would
  violate Archify handoff rules.

### Rollback Plan

Before merge, revert the immutable subject containing `canonical.py`, `builders.py`,
`__init__.py`, its dedicated test, and the two diagram artifacts together; delete only untracked
visual-check sidecars. If promotion is committed but not merged, separately revert `README.md` and
`pyproject.toml` to restore the former public description and `0.0.0`.

## Implementation Steps

1. Modify `src/deterministic_response_cache/identity/builders.py` only in the private recursive
   source-snapshot helper so valid data remains immutable and a repeated active container reference
   reaches Validator as invalid input; preserve every public Builder method and stage order.
2. Create `src/deterministic_response_cache/identity/canonical.py` with `PureTypeValidator`,
   `CanonicalSorter`, `CanonicalEncoder`, `CanonicalSerializer`, `SHA256Hasher`, and the two
   default existing-Builder factories, using the exact v1 grammar and validation behavior from the
   technical specification.
3. Modify `src/deterministic_response_cache/identity/__init__.py` to re-export only the seven
   declared public additions while retaining every existing export.
4. Create `tests/test_canonical_identity_pipeline.py` using direct imports to test exact stage
   handoffs, valid/invalid behavior, short-circuit, ordering/type boundaries, signed zero,
   subprocess determinism, default factories, composition, and existing API compatibility.
5. Historical CAVO1 implementation step (complete): after committed approved CAVO1 Plan-Reviewer evidence and Planner route, use the Archify skill
   for at most two focused geometry/content rounds. Modify only
   `docs/architecture/canonical-identity-pipeline.dataflow.json`, re-deliver only
   `docs/architecture/canonical-identity-pipeline.html`, preserve all pipeline semantics/nodes and
   the `Failure` boundary, run showcase validation/delivery/desktop visual-check per round, and
   remove all untracked visual-check sidecars before the immutable subject commit.
6. Rejected C0S remains frozen provenance. C0S-R1 repaired its double-escaped C1S tab schema;
   C1S/C2S are complete in `be0ce355dc777d63b7454488989452183519490a`. These historical records
   create no C3 Tester, Reviewer, push, or PR authority.
7. After committed approved CSO1 Plan-Reviewer evidence, committed approved C0S-R1 status-sync
   review evidence, and a Planner route, C3 modified only
   `src/deterministic_response_cache/identity/canonical.py`: import `override` from `typing`, use
   the five exact named Protocol bases, and decorate only the matching public stage method. Preserve
   all private helpers and existing pipeline behavior.
8. C3 modified only `tests/test_canonical_identity_pipeline.py` to preserve direct imports and all
   pipeline regression coverage while asserting the exact direct base and `__override__` marker for
   each public stage method and no marker on private helpers, then committed the immutable two-path
   subject `cbee5f23310b973d9e52e4e1c662ca1d9f9169d8`.
9. C3S/C4/C5, C5S receipt, C6/C7, and C7S's committed independent approval receipt
   `1123deae24fc37f6755e3eae810d453c40552f9d` are completed frozen facts. C8 stays Planner-only
   Phase 4.5 pending. PRCF1 has a fresh exact two-path subject and evidence sequence; it cannot
   reuse CSO1 evidence or derive a C8 outcome.

## Validation / Acceptance Checks

- `uv run pytest tests/test_canonical_identity_pipeline.py tests/test_model_feature_identity_contracts.py tests/test_model_feature_identity_builders.py`
  passes without modifying the two existing test files.
- `uv run ruff format --check .`, `uv run ruff check .`, `uv run pyright`, `uv run tach check`,
  `uv run pytest`, and `uv run pre-commit run --all-files` pass.
- The concrete test proves exact JSON strings `["int","1"]`, `["bool",true]`, and
  `["list",[["int","1"],["str","x"]]]`, plus exact `EncodedIdentity.value` /
  `SerializedIdentity.value` handoffs. It never asserts or implies list/dict Encoder output.
- A clean-process subprocess test proves a fixed valid source produces the same lowercase
  64-character SHA-256 hex output in at least two independent Python processes.
- The historical original implementation subject is six non-publish paths. The new CSO1 immutable
  subject diff is exactly two paths: `canonical.py` and `tests/test_canonical_identity_pipeline.py`.
  No CAVO1 evidence, historical subject, or publish file is reused or amended.
- CAVO1 accepts only Archify validation with all 9 showcase checks and zero errors/warnings,
  delivery exit 0, and visual-check exit 0 with containment at all four desktop viewports. At most
  two focused rounds are allowed; no improvement across both or remaining second-round overflow is
  `human-check`. No sidecar remains before commit.
- CAVO1 Tester records actual commands, integer exit codes, delivery SHA-256 values, showcase
  counts, and failing viewport count in declared JSON evidence. CAVO1 Reviewer consumes only
  committed same-subject passing evidence and a clean committed tree, then verifies the exact
  two-path correction scope, direct imports, canonical boundaries, and diagram scope.
- CSO1 tests prove direct named bases (`Validator`, `Sorter`, `Encoder`, `Serializer`, `Hasher`),
  `__override__ is True` for exactly `validate`, `sort`, `encode`, `serialize`, and `hash`, and no
  private helper marker. `uv run pytest tests/test_canonical_identity_pipeline.py
  tests/test_model_feature_identity_contracts.py tests/test_model_feature_identity_builders.py`,
  `uv run ruff format --check .`, `uv run ruff check .`, `uv run pyright`, `uv run tach check`,
  `uv run pytest`, and `uv run pre-commit run --all-files` must pass.
- At `publish-in-progress` only, verify the README API row and `pyproject.toml` `0.1.0` change;
  bounded push/draft PR still require existing Human authorization. No auto-merge/release/tag.

## Reviewer Handoff

The independent Plan-Reviewer produces exactly this JSON object (no Markdown prose) at the declared
plan-review receipt path. Only a committed `approved` verdict permits Planner routing; this
candidate itself neither selects nor closes an active candidate.

```json
{
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "copilot_feedback_triage": {
    "ADDRESS": [],
    "DISCUSS": [],
    "SKIP": []
  }
}
```

CAVO1's correction Plan-Reviewer, Tester, and Reviewer evidence use the exact extended JSON
schemas in `canonical-identity-pipeline.archify-visual-overflow.correction-plan.md`. Their writers,
same-subject binding, clean-tree review condition, and separate evidence-only commit order are
mandatory. This correction candidate itself neither selects nor closes an active candidate.

CSO1's correction Plan-Reviewer, Tester, and Reviewer evidence use the exact extended JSON schemas
in `canonical-identity-pipeline.concrete-stage-override.correction-plan.md`. CAVO1 evidence cannot
substitute for any CSO1 gate. This candidate itself neither selects nor closes an active candidate.

PRCF1's correction Plan-Reviewer, Tester, independent Reviewer, and later nine-thread
classification evidence use the exact schemas in
`canonical-identity-pipeline.pr-comment-review-and-fix.correction-plan.md`. The recovery receipt
and fresh classification use the separate exact schemas in
`canonical-identity-pipeline.pr-comment-review-and-fix-p8-p10-route-recovery.correction-plan.md`.
The sole PRCF1 subject is `canonical.py` plus its dedicated test. Its P3/P5/P7 same-subject
evidence is new and cannot reuse CAVO1 or CSO1 records. `uv.lock` is neither an implementation nor
a resolution path.

## PRCF1 correction route

C7S's independent approval receipt was committed at
`1123deae24fc37f6755e3eae810d453c40552f9d`; it is completed historical provenance. C8 remains a
Planner-only Phase 4.5 gate. PRCF1 is a separate, Human-authorized candidate that is a clean,
non-merge direct child of that receipt. It does not declare C8 complete or derive merge, release,
or thread-resolution authority from it.

### Candidate admission

The Plan-Creator candidate changes exactly these ten paths and creates no receipt or execution
evidence:

1. `analysis/canonical-identity-pipeline/technical-spec.md`
2. `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c7-status-sync.correction-plan.md`
3. `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override-c7-status-sync.correction-step.md`
4. `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-plan.md`
5. `plan/canonical-identity-pipeline/canonical-identity-pipeline.concrete-stage-override.correction-step.md`
6. `plan/canonical-identity-pipeline/canonical-identity-pipeline.plan.md`
7. `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-plan.md`
8. `plan/canonical-identity-pipeline/canonical-identity-pipeline.pr-comment-review-and-fix.correction-step.md`
9. `plan/canonical-identity-pipeline/canonical-identity-pipeline.spec.md`
10. `plan/canonical-identity-pipeline/canonical-identity-pipeline.step.md`

The first-parent diff must contain only those paths. `uv.lock` was restored to the parent and is not
a candidate, subject, evidence, or publish path.

### Fixed route

1. Independent Plan-Reviewer writes only PRCF1's declared plan-review log from the clean committed
   candidate; Independent Implementer separately commits unchanged approved content.
2. The immutable implementation subject then changes only
   `src/deterministic_response_cache/identity/canonical.py` and
   `tests/test_canonical_identity_pipeline.py`: exact built-in string acceptance before sorting,
   all surrogate rejection, fixed non-BMP ASCII bytes/hash proof, and exact `_SnapshotList` type
   identity.
3. Tester writes factual same-subject evidence, then Independent Implementer commits it alone.
   Independent Reviewer writes same-subject review evidence, then Independent Implementer commits
   it alone. No evidence shares a commit with code, tests, planning, or the other evidence.
4. P7 receipt-status-sync completed at `49c0bcd197c6b9ac4fb1baba115c903060ff52cf`, but the
   structurally correct `18d9b4751df26376c9cf47fe7968130870f07fe7` classification is pre-P8
   immutable nonrouting provenance. Only after the separate recovery receipt is committed may
   Planner redo Phase 4.5; only then may Independent Reviewer write fresh P9 classification and
   Independent Implementer commit it as sole P10 evidence. Seven are resolvable only when that
   fresh P9/P10 evidence proves their correction; the two `uv.lock` threads remain
   `skip-not-resolvable` under the explicit Human decision. Implementer may reply and resolve only
   exact `addressed-and-resolvable` threads after P10. No skipped thread may be resolved; no role
   may approve, merge, release, tag, or post-merge.

A dirty worktree, parent mismatch, unlisted path, failed/missing/cross-subject evidence, altered
`uv.lock`, or attempt to resolve a skip is `blocked`; candidate/evidence/thread conflict is
`human-check`.

## Post-merge / release actions

No automatic release, tag, post-merge, or final summary action is authorized. After the draft PR
opens, Human alone performs review, merge, and any decision to publish `0.1.0` or create release
notes/tags.

## Open Questions / Unresolved Items

None. The absent repository `VERSION` file was resolved by the discovered `[project].version`
source in `pyproject.toml`; the exact minor bump and timing are locked above.
