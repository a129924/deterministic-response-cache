# loaded-runtime-cache

## Goal / Outcome

Analysis strict mode：`analysis/loaded-runtime-cache/technical-spec.md` 是 execution-facing source of truth，
`requirements.md` 是 business-intent guardrail；本 plan 完整映射兩者及 Human 確認的 locked decisions。

建立獨立、protocol-first 的 Loaded Runtime Cache BC。完成後 repository 具備 local `RuntimeReuseKey`、generic
synchronous Runtime Registry／Retention ports，以及 reusable-runtime lookup／retention outcome contracts；它不建立
concrete backend、DI composition 或 runtime lifecycle。

本 topic 的 Git lineage label 是 Human-authorized exception `feat/andrew/runtime-reuse-protocol`。它只標示
lineage，不能建立第二 topic、替代 slug、選擇 candidate 或作為 routing evidence。

## Scope

| Field | Contract |
| --- | --- |
| In-Scope | local immutable opaque `RuntimeReuseKey`；`RuntimeRegistry[RuntimeT]`、`RuntimeRetention[RuntimeT]` Protocol；`Available`、`Missing`、`Unavailable`、`Retained`、`NotRetained` outcomes；locked module taxonomy、direct-module contract tests、BC-independence regression、五份 architecture authority 同步與 Archify dataflow evidence。 |
| Out-Of-Scope | Identity BC direct import、`ModelIdentity -> RuntimeReuseKey` mapping／mapper／ACL implementation、concrete Registry／Retention／lookup class、DI、backend、runtime initialization／download／unload／execution、provider management、Response Reuse、Model Execution、Provider Adapter、TTL、eviction、locking、concurrency、retry、timeout、metrics、tracing。 |
| Non-Goal | root re-export、package facade、dynamic import、`sys.modules` substitution、`service.py`、`utils.py`、`common.py`、README、version、release、tag、merge、post-merge。 |

## Locked Decisions

- Identity BC 與 Loaded Runtime Cache 是獨立 BC，任一方向均不得 import 對方 module。`ModelIdentity` 與
  `RuntimeReuseKey` 是語意不同的 local types，不得 re-export、duplicate 或跨 BC 假裝共用。
- integration／ACL boundary 決定 `RuntimeReuseKey` token／mapping；Loaded Runtime Cache 只 opaque pass-through，
  不讀取、拆解、序列化、字串化、hash、canonicalize、驗證、推測或重新詮釋 key。
- `RuntimeRegistry.lookup` 回傳 `RuntimeT | None`，`retain` 回傳 `None`；`RuntimeRetention.retain` 回傳
  `Retained[RuntimeT] | NotRetained[RuntimeT]`。port-owned expected signal 是
  `RuntimeRegistryLookupUnavailable`；outcome-owned `Unavailable` 與此 signal 分離，本 topic 不增加 mapper。
- module placement 固定為 `<bc>/<topic>/<child-topic>/<module>.py`。這是 non-stable-library topic，沒有 README
  row、VERSION bump、release note 或 release action。
- architecture-path overlap 僅在 Human review／merge coordination 處理；不授權改另一 topic artifacts。

## Boundaries / Exclusions

| Category | Exact contract |
| --- | --- |
| ReadOnly | `src/deterministic_response_cache/identity/**`、`response_reuse/**`、`model_execution/**`、`provider_adapter/**`、root `__init__.py`、`loaded_runtime_cache/.gitkeep`、existing source/tests、`pyproject.toml`、`README.md`、version metadata、workflow contracts、`.github/agents/**`。 |
| Written | 五個 new Python modules、`tests/test_loaded_runtime_cache_contracts.py`、`tests/test_loaded_runtime_cache_bc_independence.py`、Archify JSON／HTML／validation／delivery／visual-check receipt、contact sheet 與四張 specified PNG sidecars。 |
| Modify | `docs/business-capability-architecture.md`、`docs/evolution-roadmap.md`、`docs/architecture/business-capability/architecture-brief.md`、`scene.js`、`index.html`；只同步 protocol-only capability 與 boundaries。 |
| Deleted | 無；不得刪除 `.gitkeep`、existing tests 或既有 artifacts。 |

## Status / Allowed Transitions

- **Current**: `planned`。五份 planning artifacts 已由 Plan-Creator 撰寫但尚未形成 candidate；下一步是
  Implementer 的 planning-candidate commit。
- **Execution model**: committed planning candidate → independent Plan-Reviewer receipt → receipt-only commit →
  immutable implementation subject → Tester evidence → Tester evidence-only commit → independent Reviewer evidence
  → Reviewer evidence-only commit → Planner Phase 4.5 alignment → bounded publish／draft PR → Human review／merge。
- **Allowed transitions**: `planned` → `planning-candidate-committed` → `plan-review-in-progress` →
  `plan-review-receipt-committed` → `implementation-in-progress` → `tester-in-progress` →
  `tester-evidence-committed` → `reviewer-in-progress` → `reviewer-evidence-committed` → `approved` →
  `publish-in-progress` → `pr-open` → `merged` (Human only). A `needs-rework` verdict returns only to a new
  planning candidate or a new immutable implementation subject as applicable; no stale evidence may route.

## Artifact Paths

| Artifact | Path | Write owner | Decision authority and role |
| --- | --- | --- | --- |
| Requirements | `analysis/loaded-runtime-cache/requirements.md` | Plan-Creator | Business-intent guardrail; planning candidate only. |
| Technical specification | `analysis/loaded-runtime-cache/technical-spec.md` | Plan-Creator | Execution-facing contract; planning candidate only. |
| Topic plan | `plan/loaded-runtime-cache/loaded-runtime-cache.plan.md` | Plan-Creator | Canonical executable contract; planning candidate only. |
| Topic specification | `plan/loaded-runtime-cache/loaded-runtime-cache.spec.md` | Plan-Creator | Acceptance and TestCase contract. |
| Step tracker | `plan/loaded-runtime-cache/loaded-runtime-cache.step.md` | Plan-Creator; later Implementer only for implementation checkmarks | Topic-local progression truth. |
| Plan-review receipt | `plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<planning-candidate-40-hex-sha>.json` | Independent Plan-Reviewer writes; Implementer commits unchanged alone | SHA-bound normal-plan verdict. |
| Runtime key | `src/deterministic_response_cache/loaded_runtime_cache/runtime_reuse/registry/runtime_reuse_key.py` **Add** | Implementer | Local opaque semantic type only. |
| Registry port | `src/deterministic_response_cache/loaded_runtime_cache/runtime_reuse/registry/runtime_registry_port.py` **Add** | Implementer | Synchronous `RuntimeRegistry` Protocol and expected lookup signal owner. |
| Lookup outcomes | `src/deterministic_response_cache/loaded_runtime_cache/runtime_reuse/lookup/lookup_outcome.py` **Add** | Implementer | Lookup outcome contract owner; no mapper. |
| Retention protocol | `src/deterministic_response_cache/loaded_runtime_cache/runtime_reuse/retention/runtime_retention.py` **Add** | Implementer | `RuntimeRetention` Protocol. |
| Retention outcomes | `src/deterministic_response_cache/loaded_runtime_cache/runtime_reuse/retention/retain_outcome.py` **Add** | Implementer | Retention outcome contract owner. |
| Contract tests | `tests/test_loaded_runtime_cache_contracts.py` **Add** | Implementer | Direct-module type／outcome／opaque-handoff tests. |
| BC-independence tests | `tests/test_loaded_runtime_cache_bc_independence.py` **Add** | Implementer | Cross-BC direct-import regression. |
| BC text authority | `docs/business-capability-architecture.md` **Modify** | Implementer | Canonical BC responsibility synchronization. |
| Evolution roadmap | `docs/evolution-roadmap.md` **Modify** | Implementer | Topic order and future-boundary synchronization. |
| Architecture brief | `docs/architecture/business-capability/architecture-brief.md` **Modify** | Implementer | Protocol-only and ACL-boundary synchronization. |
| Interactive scene source | `docs/architecture/business-capability/scene.js` **Modify** | Implementer | Interactive visual authority synchronization. |
| Interactive scene mirror | `docs/architecture/business-capability/index.html` **Modify** | Implementer | Embedded scene synchronization. |
| Dataflow source | `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.json` **Add** | Implementer | Archify showcase source. |
| Standalone dataflow | `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.html` **Add** | Implementer | Trusted delivered HTML. |
| Dataflow validation receipt | `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.validation.json` **Add** | Implementer | Final showcase validation receipt. |
| Dataflow delivery receipt | `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.delivery.json` **Add** | Implementer | Final delivery receipt. |
| Visual-check receipt | `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.json` **Add** | Implementer | Desktop containment and capture receipt. |
| Visual contact sheet | `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.html` **Add** | Implementer | Generated visual evidence index. |
| PNG 1440×900 light | `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.1440x900.light.png` **Add** | Implementer | Visual evidence. |
| PNG 1440×900 dark | `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.1440x900.dark.png` **Add** | Implementer | Visual evidence. |
| PNG 2048×1320 light | `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.2048x1320.light.png` **Add** | Implementer | Visual evidence. |
| PNG 2048×1320 dark | `docs/architecture/loaded-runtime-cache/loaded-runtime-cache.dataflow.visual-check.2048x1320.dark.png` **Add** | Implementer | Visual evidence. |
| Tester evidence | `plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence.json` | Tester writes; Implementer commits unchanged alone | Same-subject factual validation. |
| Independent review evidence | `plan/loaded-runtime-cache/loaded-runtime-cache.implementation-review-log.json` | Independent Reviewer writes; Implementer commits unchanged alone | Consumes committed passing Tester evidence. |

Every unlisted path is read-only. The fixed-name legacy plan-review receipt from the abandoned lineage is historical,
frozen provenance only: it is not an artifact of candidate C, must not be created or overwritten, and has no routing
authority. Each current or successor candidate uses only the SHA-bound template above; no candidate SHA is prefilled.

### Review and evidence schemas

- SHA-bound Plan-review receipt is one JSON object with exactly `verdict`, `blocking_issues`,
  `copilot_feedback_triage`. `verdict` is `approved|needs-rework`; `blocking_issues` is an array of objects with
  exactly `issue`, `file`, `fix`; triage has exactly `ADDRESS`／`DISCUSS`／`SKIP` arrays. Only a committed approved
  receipt for the committed candidate can authorize implementation routing.
- Tester evidence has exactly `schema_version`, `topic`, `implementation_subject_commit`, `status`, `commands`,
  `recorded_by`; it records actual commands and exit codes for the same full-SHA subject.
- Independent review evidence has exactly `schema_version`, `topic`, `implementation_subject_commit`,
  `tester_evidence_commit`, `verdict`, `blocking_issues`, `recorded_by`; it consumes committed passing Tester evidence
  for that same subject.

## Implementation Steps

1. Add only the five locked Python contract modules; preserve BC separation, direct-module surface, `.gitkeep`, and
   no-concrete-implementation boundary.
2. Add only the two declared tests with typed fakes for key-instance handoff, value／missing channels, retention
   outcome runtime preservation, failure distinction and BC-independence; no mapper test or key-field assertion.
3. Synchronize only the five declared architecture authority files; declare external unimplemented ACL mapping and
   retain backend, lifecycle, execution and provider work as future.
4. Produce Archify `dataflow` with Traditional-Chinese labels, no `meta.locale`, `quality_profile: showcase`, at most
   12 primary nodes, and truthful `backend` visual classification for the contract-only Loaded Runtime Cache node.
5. After each JSON edit run validate; freeze only a 9/9, zero-error, zero-warning result; then deliver and run
   visual-check at 1440×900, 1600×1000, 1920×1080, 2048×1320. Nonzero or skipped result stops the gate.
6. Run locked format, pyright, targeted／full pytest and direct-import regression. Tester records actual results only
   after immutable implementation subject creation.

## Validation / Acceptance Checks

- All changes match Artifact Paths; no deletion or unlisted edit.
- direct-module imports work without facade／dynamic import; Identity and Loaded Runtime Cache have no direct import.
- typed fakes prove same-instance `RuntimeReuseKey` handoff; signal, `Missing`, `Unavailable`, and unexpected
  exception semantics remain distinct; retention outcomes preserve runtime identity.
- Archify artifacts truthfully show external ACL and contract-only boundaries, and complete required validation,
  delivery and visual evidence.

## Reviewer Handoff

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

## Post-merge / release actions

No repository release action is required. Human alone decides merge; this non-stable topic has no README, VERSION,
release-note, tag or post-merge action.

## Open Questions / Unresolved Items

None. Concrete `ModelIdentity -> RuntimeReuseKey` conversion and Registry／Retention implementation are deferred to
future, separately planned integration／DI topics.

## Workflow State Contract

- current_step: planning-candidate-commit
- next_step: independent-plan-review
- status: PENDING
