# Topic Plan Contract

## Purpose

定義 repo-visible topic plan 的 authority、required structure、planning evidence 與 preflight
contract。本文件不取代 `AGENTS.md`、`plan/agent-handoff-workflow.md` 或個別 topic plan 的 locked scope。

## Authority Ordering

1. `AGENTS.md`
2. `plan/agent-handoff-workflow.md`
3. `plan/topic-plan-contract.md`
4. `plan/<topic>/<topic>.plan.md`
5. `plan/<topic>/<topic>.step.md`
6. `plan/<topic>/<topic>.review-log.md`，或 current correction route 明定的 exact review path
7. local planning skill guidance

`GOAL.md` 是 project mission，非 topic / phase authority。chat、branch、summary、
`.github/agents/**` 不可補推 planning evidence；`.github/agents/**` 僅為 frozen provenance。

## Required Topic-Plan Sections

每個 topic plan 依 canonical order 包含：`Goal / Outcome`、`Scope`、`Locked Decisions`、
`Boundaries / Exclusions`、`Status / Allowed Transitions`、`Artifact Paths`、
`Implementation Steps`、`Validation / Acceptance Checks`、`Reviewer Handoff`、
`Post-merge / release actions`、`Open Questions / Unresolved Items`。非 stable-library topic
必須明示 non-stable intent；影響 stable-library surface 必須另列 metadata/timing。

## Planning Baseline, Evidence, and Preflight

### Ordinary planning evidence

Plan-Creator 寫 planning artifacts 但不得 commit；已有 Human authorization 時，獨立
Implementer 可作 bounded planning commit，這不表示 implementation approval。future/new ordinary
`review-log.md` 是 chronological NDJSON，最後 nonblank object 必須符合 `Reviewer Handoff`
schema 且 verdict 為 `approved`。legacy logs 保持 frozen provenance，不得遷移、重讀或以格式
不符使其失效。

### Frozen B4R7 provenance

本節僅適用 `observer-dispatcher-governance`。`b900366`、B0–B4R6、S1–S5、T1–T5、V1–V5、
normal/recovery records、`7d23e8c`、`6ede06b`、所有舊 correction artifacts，及任何 uncommitted
B4R6 review log 與其 plan、step、review、schema、blocker、checklist、pending semantics 全部是 frozen
nonrouting provenance；不得作為 candidate、gate、subject、evidence source 或 current work。兩個
`step-creator` threads 維持 deferred。

`B4R7` is frozen nonrouting provenance. Its former baseline contained the following seven planning paths:

1. `plan/agent-handoff-workflow.md`
2. `plan/topic-plan-contract.md`
3. `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md`
4. `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md`
5. `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md`
6. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r7-plan.md`
7. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r7-step.md`

An Independent Implementer first commits exactly these seven paths as non-subject `B4R7`; it may not
change `tests/test_observer_dispatcher_governance_contract.py` or any implementation/evidence path in
that baseline. That commit must be non-merge and the named first-parent `git diff --name-status` must
contain the complete exact seven-path set, each once. Pre-commit B4R7 artifacts must not embed SHA, blob
SHA, `HEAD`, or review outcome. From a clean checkout of committed B4R7, an Independent Plan-Reviewer
reviews actual seven blobs and writes only
`plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r7-review-log.md`.
An Independent Implementer separately commits that unchanged approved R7 record. Neither B4R7 commit can
establish `implementation_subject_sha`.

Only the separately committed approved R7 record permits one non-merge `S6`. S6 alone establishes
`implementation_subject_sha` and may change only the exact preserved 15-path allowlist in the parent
plan. The S6 test path must add regression assertions for actual named graph/range, exact path sets,
frozen B0–B4R6 provenance, B4R7 admission and R7 schema mutation. `T6` then `V6` are its sole linear,
non-merge, evidence-only descendants. Actual named SHA graph queries must prove `S6 -> T6 -> V6`; named
`git diff --name-status S6..V6` must list exactly the B4R7 T6/V6 evidence paths. `HEAD`, a merge, a
third descendant, or textual topology inference fails closed.

### Planner preflight

Planner reads only the current parent plan, parent step and exact current approved review record. It
selects candidate, phase, gate and next role. Missing evidence is `blocked`; multiple candidates or
conflict is `human-check`; only Planner routes bounded rework. Planning approval never sets the topic
execution status to `approved`.

## Artifact Path Rules

`Artifact Paths` 是 executable contract。每個 artifact 必須有 exact repo-visible path、write
owner、decision authority 與 role。write owner 不會取得 route、status、gate 或 lifecycle authority。
未列 path 停止並交 Planner；不得自行擴張。

## Topic-Plan Contract Rules

`Implementation Steps` 僅描述 locked implementation work，不得混入 verdict、routing、reviewer
acceptance 或 human-only action。`Reviewer Handoff` 必須嵌入 fixed machine JSON schema；special
correction evidence 必須明示 exact path、ownership 與 gate。merge、post-merge、release 留在 Human
boundary。

## Reviewer Handoff

ordinary future/new review record:

```json
{"reviewed_artifacts":[{"path":"<exact repo-visible path>","revision":"<revision>"}],"review_basis":"<independent review basis>","verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]},"timestamp":"<RFC 3339 timestamp>"}
```

### B4R7 correction evidence schemas

These B4R7 records are frozen correction evidence. Each exact evidence file contains one
complete JSON object and no trailing prose. Tester records factual results only; Tester/Reviewer
cannot route lifecycle or status.

```json
{"schema_version":"observer-dispatcher-governance.correction-b4r7-plan-review.v1","correction_id":"observer-dispatcher-governance/high/b4r7","review_kind":"correction-b4r7-plan","severity":"high","reviewed_commit_sha":"<committed B4R7 SHA>","reviewed_artifacts":[{"path":"<one exact B4R7 baseline path>","blob_sha":"<B4R7 blob SHA>"}],"review_basis":"<independent clean-checkout seven-blob review after first-parent exact-path admission>","verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]},"timestamp":"<RFC 3339 timestamp>"}
```

The B4R7 review record contains each seven B4R7 baseline paths exactly once, and no test path.
An approved record must be separately committed unchanged before S6; `needs-rework` returns only to
Planner.

```json
{"schema_version":"observer-dispatcher-governance.correction-b4r7-tester-evidence.v1","correction_id":"observer-dispatcher-governance/high/b4r7","actor":"Tester","implementation_subject_sha":"<S6 SHA>","subject_verification":{"expected_sha":"<S6 SHA>","observed_sha":"<S6 SHA>","command":"<exact command>","result":"passing|failing"},"commands":[{"command":"<exact command>","exit_code":0,"result":"passing|failing"}],"correction_test_result":"passing|failing","repository_validation_result":"passing|failing","verdict":"passing|failing","timestamp":"<RFC 3339 timestamp>"}
```

```json
{"schema_version":"observer-dispatcher-governance.correction-b4r7-implementation-review.v1","correction_id":"observer-dispatcher-governance/high/b4r7","review_kind":"correction-b4r7-implementation","severity":"high","implementation_subject_sha":"<S6 SHA>","review_target_commit_sha":"<pre-existing T6 SHA>","tester_evidence":{"path":"plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r7-tester-evidence.md","revision":"<T6 SHA>","implementation_subject_sha":"<S6 SHA>","verdict":"passing"},"reviewed_artifacts":[{"path":"<one exact S6 allowlist path>","revision":"<S6 revision>"}],"review_basis":"<independent implementation review basis including named SHA graph queries>","verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]},"timestamp":"<RFC 3339 timestamp>"}
```

V6 is authored before its own commit and cannot contain, require or infer a V6 SHA. Post-commit
validation independently identifies V6 and proves named actual-SHA non-merge `S6 -> T6 -> V6`.
`git diff --name-status S6..V6` lists exactly:

1. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r7-tester-evidence.md`
2. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r7-implementation-review-log.md`

## Blocking Semantics

Missing B4R7 admission/evidence, non-approved R7 review, a merge/non-complete/wrong-path B4R7 admission,
embedded SHA/`HEAD`, any path outside the seven-path B4R7 baseline or 15-path S6 allowlist, a frozen epoch
as current evidence, a subject other than S6, wrong T6/V6 path, merge, third descendant, `HEAD`
substitution, or a range other than named `S6..V6` is
contract-breaking. Plan-Reviewer returns `needs-rework`; Planner routes `blocked` or `human-check`
for unresolved conflict.

## Boundaries

本文件不授權修改未列 paths，也不授權 PR thread action、merge、post-merge、release、tag 或
summary。Observer only dispatches Planner; Planner is routing authority; Plan-Creator authors planning
artifacts; Implementer performs bounded implementation/commits; Tester and Reviewer independently
write only declared evidence.

## Frozen B5 provenance

All B4R7 text above, this B5 route, missing R8, and all older epochs are frozen historical nonrouting
provenance. They cannot be a candidate, gate, subject, evidence source, or pending work; `step-creator`
stays deferred.

B5 is the sole non-subject non-merge baseline. Its first-parent named diff contains exactly:

1. `plan/agent-handoff-workflow.md`
2. `plan/topic-plan-contract.md`
3. `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md`
4. `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md`
5. `plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md`
6. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b5-plan.md`
7. `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b5-step.md`

Before admission, B5 planning artifacts contain no B5 SHA/blob SHA/`HEAD`/review outcome. Independent
Plan-Reviewer clean-checkout-reviews every B5 blob and writes only B5 R8; Independent Implementer separately
commits unchanged approved R8. B5/R8 never create `implementation_subject_sha`.

Only approved R8 permits non-merge S7, whose sole changed path is
`tests/test_observer_dispatcher_governance_contract.py`. S7 uses only the complete explicit environment
triple `ODG_S7_SHA`, `ODG_T7_SHA`, `ODG_V7_SHA` and subprocess real `git rev-parse`, `git rev-list`, and
`git diff --name-status`; no env triple explicitly skips rather than passes. Missing/partial/`HEAD`/
nonexistent/merge/wrong-parent/multi-path input fails closed. Direct imports remain mandatory.

T7 and V7 are the only non-merge linear S7 descendants. Named `S7..V7` diff contains exactly
`plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b5-tester-evidence.md` and
`plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b5-implementation-review-log.md`.
After V7 commits, Q7 is read-only actual query with V7 full SHA, no artifact, no `HEAD`, and no lifecycle/
thread authority.

### B5 evidence schemas

```json
{"schema_version":"observer-dispatcher-governance.correction-b5-plan-review.v1","correction_id":"observer-dispatcher-governance/high/b5","reviewed_commit_sha":"<B5 SHA>","reviewed_artifacts":[{"path":"<B5 path>","blob_sha":"<B5 blob SHA>"}],"verdict":"approved|needs-rework","blocking_issues":[]}
```

```json
{"schema_version":"observer-dispatcher-governance.correction-b5-tester-evidence.v1","correction_id":"observer-dispatcher-governance/high/b5","implementation_subject_sha":"<S7 SHA>","verdict":"passing|failing"}
```

```json
{"schema_version":"observer-dispatcher-governance.correction-b5-implementation-review.v1","correction_id":"observer-dispatcher-governance/high/b5","implementation_subject_sha":"<S7 SHA>","review_target_commit_sha":"<T7 SHA>","verdict":"approved|needs-rework"}
```

## B5R Current Route

B5R is the sole current correction route. B5R is a non-subject, non-merge seven-path planning baseline;
its pre-commit artifacts contain neither B5R SHA/blob SHA nor `HEAD`/review outcome. Independent
Plan-Reviewer clean-checkout-reviews the committed B5R blobs and writes only R9; independent Implementer
separately commits unchanged approved R9. B5R/R9 never create `implementation_subject_sha`.

Only approved R9 permits S7, the one non-merge implementation subject, changing only
`tests/test_observer_dispatcher_governance_contract.py`. Direct imports remain required and `step-creator`
remains deferred. The actual Git assertion uses only a complete explicit
`ODG_S7_SHA`/`ODG_T7_SHA`/`ODG_V7_SHA` triple and subprocess `git rev-parse`, `git rev-list`, and
`git diff --name-status`; it may be explicitly skipped/unverified only if all three values are absent.
Partial/invalid/`HEAD`/merge/wrong-parent-or-graph/multi-path input fails closed.

T7 and V7 are the only non-merge S7 descendants. Their named `S7..V7` diff lists exactly the B5R T7 and V7
paths. T7 must record a passing non-skipped run with a complete real triple. Q7 is post-V7 full-SHA,
read-only, no-artifact and has no lifecycle or thread authority.

### B5R evidence schemas

```json
{"schema_version":"observer-dispatcher-governance.correction-b5r-plan-review.v1","correction_id":"observer-dispatcher-governance/high/b5r","reviewed_commit_sha":"<B5R SHA>","reviewed_artifacts":[{"path":"<B5R planning path>","blob_sha":"<B5R blob SHA>"}],"verdict":"approved|needs-rework","blocking_issues":[]}
```

```json
{"schema_version":"observer-dispatcher-governance.correction-b5r-tester-evidence.v1","correction_id":"observer-dispatcher-governance/high/b5r","implementation_subject_sha":"<S7 SHA>","actual_graph_assertion":{"environment":"complete-real-triple","result":"passing","skipped":false},"verdict":"passing|failing"}
```

```json
{"schema_version":"observer-dispatcher-governance.correction-b5r-implementation-review.v1","correction_id":"observer-dispatcher-governance/high/b5r","implementation_subject_sha":"<S7 SHA>","review_target_commit_sha":"<T7 SHA>","verdict":"approved|needs-rework"}
```
