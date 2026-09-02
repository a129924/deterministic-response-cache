# Observer / Dispatcher Governance

## Goal / Outcome

- 完成 B2 high-severity corrective baseline：以可驗證 Git tree object 取代已失效 B1 review
  record，並只補強 governance contract test 對 frozen provenance、subject reset 與 exact
  two-evidence topology 的 fail-closed assertions。
- topic 保持 `needs-rework`，直到 B2 chain 通過；B0/S1/T1/V1、B1 及其 invalid review record
  均是 frozen provenance。narrow `B2` exception 之後，只有 test-only `S3 -> T3 -> V3`；驗證使用
  `S3..V3`，絕不以 `HEAD` 代替。

> **Analysis-layer warning:** `analysis/observer-dispatcher-governance/requirements.md`
> 與 `analysis/observer-dispatcher-governance/technical-spec.md` 不存在。本 plan 依
> Planner 已核准的 B2 corrective direction author；此 warning 不授權重新開啟
> architecture、BC、identity 或未列 path。

## Scope

- **In scope**: two shared contracts、parent plan/spec/step、B2 correction plan/step；B2 approval
  後唯一 implementation path 為 `tests/test_observer_dispatcher_governance_contract.py`。
- **Out of scope**: `AGENTS.md`、`.codex/**`、`.agents/**`、產品 library、public API、BC、Identity、
  runtime、architecture docs、README、VERSION、release、tag、push、PR / thread、merge、post-merge、
  summary、legacy evidence migration / reader / compatibility layer，以及未列 path。

## Locked Decisions

- 這是 Planner-confirmed `high` B2 correction，routing state 為 `PLANNER_REPLAN`；B0/S1/T1/V1、
  B1 及其 invalid review record 都是 frozen provenance，不能作為 B2 gate 或 subject，且不可修改。
- Human 的此 scope expansion authorization 為 `2. 授權擴張 current topic。`；current
  correction route 的 authoritative source 是兩份 shared contracts、parent plan/spec/step、
  `correction-b2-plan.md` / `correction-b2-step.md`，及其 exact B2 pre-subject review evidence。
- Parent plan、spec 與 step 在 Plan-Creator backfill 後仍是 current execution truth；
  `correction-b2-plan.md` / `correction-b2-step.md` 是 retained correction delta，不取代 parent。
  `correction-b2-review-log.md` 僅在其 pre-subject gate 尚未完成時是 current routing
  evidence；completed 後仍保留為 evidence，不成為 parent execution truth。
- B0=8556d41282eb2388ff22e45623dd20052a2bf70f、S1=f1a2ae1334b03ea0c5eea7612909ef77c089f38c、
  T1=b96c484e78bdc1ea004c7629616f216657e64e07、V1=2b0e6fa653bb58537523ae4010945dadbab7b34e，
  normal / `recovery-*` evidence 與其 SHA / verdict 都是 frozen provenance，不得修改、遷移、
  重讀為 current gate 或推導新 subject。
- Old epoch terminal 是 `R0=cb3f66c60e95e5580cb2b30632d0d5ed9f0d0ee9`，唯一 predicate 為
  `ecc5b6f61bacc5493ca3a9f1012d1bfdd43a810c..cb3f66c60e95e5580cb2b30632d0d5ed9f0d0ee9`。
  narrow `B2` exception 僅容許 Plan-Reviewer 以 temporary index seeded from `HEAD`，只納入
  七個未提交 B2 planning artifacts，以 `git write-tree` 產生並以 `git rev-parse` / `git cat-file`
  驗證 actual Git tree object，再寫入 `correction-b2-review-log.md`。Independent Implementer
  將 unchanged log 與七個 reviewed artifacts 提交為 `B2` 後，必須驗證 record tree/blob 與 B2
  tree 對七個 paths 相同，且 diff 只新增 review log；`B2` 絕非 subject。
- 只有 `B2` 後唯一 test-path 的 non-merge `S3` commit 建立 replacement immutable
  `implementation_subject_sha`。新 subject 後嚴格只允許 `T3`（Tester evidence）再 `V3`
  （Reviewer evidence）兩個 linear、non-merge、evidence-only commits。第三個 path、merge、
  lifecycle action 或以 `HEAD` 取代 `S3..V3` 驗證使 chain 無效並回交 Planner。
- 這是 non-stable、review-ready-only topic：README / VERSION 不修改，無 release / tag；
  standalone correction skill 只可在另開 topic 且 repeated instability 或
  cross-workflow reuse 已證實時再考慮。

## Boundaries / Exclusions

- Observer 只讀 state、依 Planner 決定派遣一個角色、彙整 bounded result 並回報
  `可直接前進`、`needs-rework`、`blocked` 或 `human-check`；不得實作、改檔、git、
  gate inference、comment handling 或重解 locked decisions。
- Planner 是 candidate、phase、gate、severity、correction routing 與 next role 的唯一
  authority。Plan-Creator 只 author / sync planning artifacts；Implementer 只實作及
  原樣固化已授權 evidence；Tester 與 Reviewer 必須真實獨立。
- `.github/agents/**` 僅為 frozen provenance，絕非 runtime dependency；唯一可修改的
  `.codex` paths 是 `.codex/agents/planner.toml` 與 `.codex/agents/implementer.toml`。Identity BC、
  CacheStore 與其餘 deferred BC boundaries 維持不變。任何未列 path 或 direction change
  都停止並回交 Planner，chat、branch、PR Ready、summary 或舊 evidence 不得補推 gate。

## Status / Allowed Transitions

- **Current**: `needs-rework`；correction routing state 為 `PLANNER_REPLAN`。
- **Execution model**: narrow `B2` exception 下 Plan-Reviewer 先以 temporary-index verified
  Git tree/blob review 七個未提交 B2 planning artifacts 並寫 correction-b2 review record；
  Independent Implementer 原樣將 record 加七個 reviewed artifacts commit 成 `B2` 並驗證 retained
  tree/blob，其非 subject。只有其後 test-only non-merge `S3` 建立 immutable subject；Tester `T3`、
  再 Reviewer `V3` 各自 attest `S3`；僅以 `S3..V3`
  驗證後停止於 Human boundary。
- **Allowed transitions**:
  - `needs-rework` -> `creator-in-progress`
  - `creator-in-progress` -> `review-ready`
  - `review-ready` -> `reviewer-in-progress`
  - `reviewer-in-progress` -> `approved|needs-rework`
  - `approved` -> `creator-in-progress|publish-in-progress`
  - `publish-in-progress` -> `pr-open`
  - `pr-open` -> `needs-rework|merged`
  - `merged` -> terminal
- **Correction routing**: correction review `needs-rework` 保持 topic `needs-rework`
  並要求新的 Planner-frozen direction。final correction implementation review
  `needs-rework` 使 new chain 無效；不得用 patch、extra descendant 或 prior evidence 修復。

## Artifact Paths

| Artifact | Path | Write owner | Decision authority | Role |
| --- | --- | --- | --- | --- |
| Repo workflow | `plan/agent-handoff-workflow.md` | Plan-Creator | Planner | Canonical correction routing and Human stop boundary |
| Shared topic-plan contract | `plan/topic-plan-contract.md` | Plan-Creator | Planner | Parent/current-truth and correction-artifact contract |
| Governance contract test | `tests/test_observer_dispatcher_governance_contract.py` | Implementer | Planner | Executable expanded-schema checks |
| Topic plan | `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md` | Plan-Creator | Planner | Parent current execution contract |
| Topic specification | `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md` | Plan-Creator | Planner | Parent current execution contract |
| Step tracker | `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md` | Plan-Creator | Planner | Parent current execution contract |
| B2 correction plan | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b2-plan.md` | Plan-Creator | Planner | Retained B2 correction delta |
| B2 correction step | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b2-step.md` | Plan-Creator | Planner | Retained B2 checkpoints |
| B2 correction review log | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b2-review-log.md` | Plan-Reviewer | Plan-Reviewer verdict; Planner route | Verified-tree pre-subject review |
| B2 Tester evidence | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b2-tester-evidence.md` | Tester | Tester factual result; Planner route | T3 only, first evidence descendant |
| B2 implementation review | `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b2-implementation-review-log.md` | Reviewer | Reviewer verdict; Planner route | V3 only, final evidence descendant |
| Frozen B0/S1/T1/V1/B1 correction provenance | Existing prior correction / evidence paths | Historical (no write) | None | Never current routing, subject, Tester, or Reviewer evidence |
| Frozen normal provenance | `plan/observer-dispatcher-governance/observer-dispatcher-governance.review-log.md` | Historical (no write) | None | Never current routing, Tester or Reviewer evidence |
| Frozen normal provenance | `plan/observer-dispatcher-governance/observer-dispatcher-governance.planning-review-evidence.md` | Historical (no write) | None | Never current routing, Tester or Reviewer evidence |
| Frozen normal provenance | `plan/observer-dispatcher-governance/observer-dispatcher-governance.tester-evidence.md` | Historical (no write) | None | Never current routing, Tester or Reviewer evidence |
| Frozen normal provenance | `plan/observer-dispatcher-governance/observer-dispatcher-governance.implementation-review-log.md` | Historical (no write) | None | Never current routing, Tester or Reviewer evidence |
| Frozen recovery provenance | `plan/observer-dispatcher-governance/observer-dispatcher-governance.recovery-planning-review-evidence.md` | Historical (no write) | None | Never current routing, Tester or Reviewer evidence |
| Frozen recovery provenance | `plan/observer-dispatcher-governance/observer-dispatcher-governance.recovery-tester-evidence.md` | Historical (no write) | None | Never current routing, Tester or Reviewer evidence |
| Frozen recovery provenance | `plan/observer-dispatcher-governance/observer-dispatcher-governance.recovery-implementation-review-log.md` | Historical (no write) | None | Never current routing, Tester or Reviewer evidence |

`README.md`、`VERSION`、`.github/copilot-instructions.md`、`.github/agents/**`、`src/**`、
docs、其他 tests 與 summary 均不在 write scope。未列 path 需先由 Planner 修復 parent plan。

## Implementation Steps

1. Plan-Creator 只同步七個 B2 planning paths 並建立 B2 correction plan/step；不寫 evidence、
   不 commit、也不開始 implementation。
2. Independent Plan-Reviewer approved B2 verified-tree record 已原樣與該七個 paths commit 成
   non-subject `B2` 且 post-commit tree/blob validation 通過後，Implementer 才可在唯一 non-merge `S3` 改動
   `tests/test_observer_dispatcher_governance_contract.py`，以 direct assertions 驗證 frozen
   provenance、S3 reset 與 exact `T3 -> V3` topology，且不得替代 direct-import regressions。
3. Tester 只寫同一 S3 的 T3 factual evidence；Reviewer 僅在 passing T3 後寫 V3 verdict；兩者都
   不得改 subject、route、status 或 implementation。

## Validation / Acceptance Checks

- B2 review pins a verified Git tree object and one tree-derived path/blob revision for each exact
  seven B2 planning paths; its approved record is committed unchanged with exactly that set as
  non-subject B2, then validates the retained object/blobs and one-path tree diff post-commit.
- S3 is non-merge and changes only `tests/test_observer_dispatcher_governance_contract.py`, which
  fails for current use of frozen provenance, B2/S1 as subject, or topology other than T3 then V3.
- New Tester state is `pending` until the new subject exists. Tester then records subject
  verification, exact command/results, the new test, repository validation, timestamp and
  `passing|failing`; no prior Tester record may satisfy this gate.
- The B2 review record is the schema-complete `correction-b2-plan` object defined in the shared
  contract. Only approved and post-commit-validated B2 authorizes test-only S3.
- The final reviewer record carries the same S3 SHA and passing T3 reference. `git diff --name-status
  S3..V3` must be exactly the two B2 Tester / Reviewer evidence paths with no merge; `HEAD` is not accepted.
- Parent sync and independent reviews must pass before correction resolution. Retain all
  correction artifacts; then stop, with no publish, PR action, merge, release, tag, summary
  or self-approval.

## Reviewer Handoff

Current B2 pre-subject gate:

- The sole current correction-review record path is
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b2-review-log.md`.
  An independent Plan-Reviewer is its sole writer. All old B0/S1/T1/V1/B1 correction paths and their
  records are frozen provenance, never current routing or evidence.
- Under the one-time `B2` exception and before the test-only S3 change, the Plan-Reviewer must
  independently build a verified Git tree from a temporary index seeded by `HEAD` and containing
  only these seven **uncommitted** B2 planning artifacts: `plan/agent-handoff-workflow.md`, `plan/topic-plan-contract.md`,
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md`,
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md`,
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md`,
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b2-plan.md`, and
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b2-step.md`.
- The record must be the single schema-complete `correction-b2-plan` JSON object with
  `reviewed_tree_sha` and exactly one path/blob revision per artifact, under
  `plan/topic-plan-contract.md#current-topic-correction-evidence-schemas`, with an `approved`
  verdict. Only an independent Implementer, under existing Human commit authorization, may commit
  that approved record unchanged together with exactly the seven reviewed artifacts as non-subject
  `B2`, then independently validate retained tree/blob values. Only then may a non-merge `S3` modify
  `tests/test_observer_dispatcher_governance_contract.py` and become the immutable subject.
- Only Tester `T3` at
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b2-tester-evidence.md`
  and then Reviewer `V3` at
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b2-implementation-review-log.md`
  may be non-merge evidence-only descendants of the same S3. V3 references passing T3 and final
  verification is exactly `git diff --name-status S3..V3`, containing only those two named paths.

```json
{
  "schema_version": "observer-dispatcher-governance.correction-b2-plan-review.v1",
  "correction_id": "observer-dispatcher-governance/high/b2",
  "review_kind": "correction-b2-plan",
  "severity": "high",
  "routing_state": "PLANNER_REPLAN",
  "reviewed_tree_sha": "<verified Git tree object>",
  "reviewed_artifacts": [
    {
      "path": "<exact repo-visible path>",
      "blob_sha": "<exact reviewed working-tree blob SHA>"
    }
  ],
  "review_basis": "<independent review basis>",
  "verdict": "approved|needs-rework",
  "blocking_issues": [],
  "copilot_feedback_triage": {
    "ADDRESS": [],
    "DISCUSS": [],
    "SKIP": []
  },
  "timestamp": "<RFC 3339 timestamp>"
}
```

The B2 review, T3 Tester, and V3 final implementation-review records use the complete three-object
schemas in `plan/topic-plan-contract.md#current-topic-correction-evidence-schemas`; those schemas
are the authoritative field contract for correction review and the exact named `S3..V3` topology.

## Post-merge / release actions

- No merge, release, VERSION bump, tag, post-merge sync, PR action or summary is authorized.
  The final correction implementation-review record is a terminal Human boundary; every
  later lifecycle action needs new explicit Human direction.

## Open Questions / Unresolved Items

- Correction review, replacement subject, new Tester evidence and new independent
  implementation review are pending. Existing evidence is frozen provenance and cannot
  answer those gates.
