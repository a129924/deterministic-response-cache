---
topic: observer-dispatcher-governance
phase: needs-rework
created: 2026-09-01
---

# observer-dispatcher-governance — Step Tracking

> **B4 current route:** B0–B3/S1–S4/T1–T4/V1–V4 and normal/recovery are frozen; `step-creator` threads are deferred. Only B4 -> S5 -> T5 -> V5 routes current work.

## B4 Actionable Steps

- [X] Plan-Creator: synchronize exactly seven B4 planning paths and create B4 plan/step.
- [ ] Independent Implementer: commit the seven paths as non-subject B4.
- [ ] Independent Plan-Reviewer: clean-checkout review committed B4; write only B4 review log.
- [ ] Independent Implementer: separately commit unchanged B4 review log.
- [ ] Planner: run exact candidate selector; dispatch S5 only when B4 review is approved.
- [ ] Independent Implementer: make one non-merge S5 using exact 15-path allowlist.
- [ ] Tester: write factual same-S5 T5 evidence only.
- [ ] Reviewer: require same-S5 passing exact T5, write V5, and verify named actual-SHA `S5..V5`.
- [ ] Human boundary: no PR-thread, merge, release or post-merge action.

> **B3 correction override — current stage:** B0/B1/B2/S1/S3/T1/T3/V1/V3 and normal/recovery
> artifacts are frozen, nonrouting provenance; V3's frozen needs-rework outcome has no log. The
> current route is verified-tree non-subject B3, then test-only S4, T4, and pre-commit V4 targeting
> T4 via `review_target_commit_sha`. Exact final verification is named `S4..V4`, never HEAD.

## B3 Actionable Steps

- [X] **Plan-Creator:** synchronize only the seven B3 planning paths and create B3 plan/step.
- [ ] **Independent Plan-Reviewer:** review tree/blob state of exactly those seven paths and write B3 record.
- [ ] **Independent Implementer:** commit unchanged approved record and reviewed set as non-subject B3.
- [ ] **Independent Implementer:** create S4 changing only the governance contract test.
- [ ] **Tester:** create T4 evidence for same S4.
- [ ] **Reviewer:** create V4 pre-commit record targeting T4; validate V4 post-commit and `S4..V4`.

## B3 Current Gate Notes

- Only B3 -> S4 -> T4 -> V4 is current. B0/B1/B2/S1/S3/T1/T3/V1/V3 and normal/recovery artifacts
  are frozen, nonrouting provenance; V3 has no review-log file.
- S4 direct tests must fail closed for every frozen-marker removal, B3/prior subject substitution,
  topology/range/evidence mutation, HEAD range, or dynamic-import substitution.
- B3 is non-subject; V4 targets existing T4 via `review_target_commit_sha`, never its own SHA.

## Historical B2 Record (frozen provenance)

> **B2 correction override:** B0/S1/T1/V1、B1 and its invalid review record are frozen provenance.
> The current route is a temporary-index verified Git tree/blob review of seven B2 planning artifacts,
> non-subject B2 with post-commit validation, test-only S3, then T3 and V3;
> no evidence, commit, or thread is created in this Plan-Creator step.

### Historical B2 Workflow Stages

- [X] original-plan-authoring
- [X] original-planning-review
- [X] original-implementation-and-evidence
- [X] high-correction-planning
- [ ] b2-correction-review-and-baseline
- [ ] b2-test-only-implementation
- [ ] b2-tester-evidence
- [ ] b2-implementation-review
- [ ] human-boundary

### Historical B2 Actionable Steps

- [X] **Actor:** Plan-Creator — **Action:** synchronized the seven B2 planning artifacts only:
  `plan/agent-handoff-workflow.md`, `plan/topic-plan-contract.md`,
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md`,
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md`, this step tracker,
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b2-plan.md`, and
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b2-step.md`; do not
  alter frozen provenance, write evidence, commit, push, or act on threads.
- [ ] **Actor:** Independent Plan-Reviewer — **Action:** under the one-time `B2` exception, as sole
  writer of
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b2-review-log.md`,
  use a temporary index seeded from `HEAD`, stage only the seven uncommitted B2 planning paths,
  verify the `git write-tree` object with `git rev-parse` and `git cat-file`, then write the
  schema-complete `correction-b2-plan` JSON with tree-derived path/blob revisions.
- [ ] **Actor:** Independent Implementer — **Action:** only on that schema-complete `approved`
  verdict and existing Human commit authorization, commit the unchanged B2 review record plus the
  exact seven reviewed artifacts as non-subject `B2`, then validate retained tree/blob values and
  one-path tree-to-B2 diff; it never establishes an implementation subject.
- [ ] **Actor:** Independent Implementer — **Action:** only after committed/validated B2, make one non-merge
  immutable `S3` subject commit that modifies only
  `tests/test_observer_dispatcher_governance_contract.py`.
- [ ] **Actor:** Tester — **Action:** only against same-S3, write
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b2-tester-evidence.md`
  as non-merge `T3`; no frozen record may satisfy this gate.
- [ ] **Actor:** Reviewer — **Action:** only with same-S3 passing T3, write
  `plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b2-implementation-review-log.md`
  as non-merge `V3`, verify exact `S3..V3`, then stop at the Human boundary.

### Historical B2 Implementation Steps

- [ ] 1. Before implementation, hand the synchronized seven B2 planning artifacts to the independent
  Plan-Reviewer. Stop unless its temporary-index verified-tree review is `approved`, committed
  unchanged with exactly that reviewed set as non-subject B2, and validates post-commit.
- [ ] 2. In S3 only, add direct fail-closed assertions to
  `tests/test_observer_dispatcher_governance_contract.py` for frozen provenance, S3 as the only
  replacement subject, and the exact T3-then-V3 evidence topology; preserve existing
  direct-import behavior.
- [ ] 3. Require T3 then V3 as the only evidence-only descendants. Verify the named
  `git diff --name-status S3..V3` range contains exactly their two declared evidence paths; never
  substitute `HEAD`, a merge, or an extra descendant.

### Historical B2 Main Agent Actionable Steps — Fixed Tail

- [ ] After final new Reviewer evidence, stop. Do not publish, push, act on PR threads,
  merge, sync, release, tag or create summary without new explicit Human direction.

### Historical B2 Handoff / Gate Notes

- State is `needs-rework` / `PLANNER_REPLAN`. B0/S1/T1/V1, B1 and its invalid review record, every
  normal/recovery record, and all old correction artifacts are frozen provenance only: they are never
  current routing, a B2 gate, a subject, Tester evidence, or Reviewer evidence. B2 is a one-time
  verified-tree planning baseline and is explicitly non-subject.
- Tester state remains pending until non-merge S3 exists. S3 alone establishes the replacement
  immutable `implementation_subject_sha`; final evidence must be linear, non-merge `S3 -> T3 -> V3`,
  contain exactly the two new B2 Tester and Reviewer paths, and be verified as named `S3..V3`, never
  `HEAD`. Any other topology, merge, extra descendant, or range returns to Planner.
