---
topic: loaded-runtime-cache
phase: c28-plan-authoring
created: 2026-09-17
---

# loaded-runtime-cache — Step Tracking

## Workflow Stages

C11/C12/C13/C14 stages below are frozen provenance. C15 is the active successor and must not inherit them.

- [x] C14 plan-authoring
- [x] C14 planning-candidate-commit
- [x] C14 plan-review
- [x] C14 RED test-authoring
- [x] C14 RED factual-test-evidence
- [x] C14 green implementation
- [x] C14 green Tester evidence
- [x] C14 independent implementation review
- [ ] C14 Phase 4.5 / thread classification (frozen historical state; nonrouting)

## Actionable Steps

- [x] **Actor:** Implementer — **Action:** C11/R11/S11/T11/V11 completed as immutable provenance:
  `55ad5d48c8e638bc5a81f3d0fecfc5a5f35e963c` →
  `01da31b11dcc8013f03a773ad9e9042c8bb527bf` →
  `e9934dc7bb7b4f81098e635b5f0257c56da659a0` →
  `86a5cd54bec9d687d8d7f1738e9376435d3d1abf` →
  `73644c2b88257832e1b4d8bedaf516b803c2ee3a`.
- [x] **Actor:** Implementer — **Action:** Committed C12 `41d51072901cfd205ebc91644036e6695b1fe81c` as exactly the
  five planning artifacts; its diff excludes source, tests, architecture, Archify artifacts, receipts and evidence.
- [x] **Actor:** Independent Plan-Reviewer — **Action:** Reviewed committed C12 and wrote approved immutable R12
  `plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-41d51072901cfd205ebc91644036e6695b1fe81c.json`.
  Its triage non-emptily and factually covers the fixed snapshot in the topic plan.
- [x] **Actor:** Implementer — **Action:** Committed unchanged R12 receipt as sole evidence-only commit
  `d738e91eb20869709d605fe7f879b340c9614b6a`. Its committed `approved` verdict routes Planner Phase 4.5 thread
  classification only.
- [x] **Actor:** Planner — **Action:** Classified
  `9aa656b13fdc36492273c97a62eb9d422a1b64b5` as unapproved `needs-rework` planning provenance. It is frozen,
  nonrouting context only and cannot be reused as C13 candidate, receipt, subject, Tester evidence, or review evidence.
- [x] **Actor:** Planner — **Action:** C13 `a623981989f3363a4b225319a432c3a9d8e28b96`、R13 `cf91b55f80f1764e040c95c822ae55b290e3699c`、RED `3ba583bed8c367b756e2cb450e468f1274d04193`、failing evidence `c4f229f14d3c4c38d40cdda8ad0429712e0ae189` and
  `ade584e7eb63a7846a23c073c06a802ff99ff6cf` are frozen provenance. `ade584e7…` is `needs-rework`; none may route C14.
- [x] **Actor:** Implementer — **Action:** Committed C14 candidate `4d78eaf997847eb3b872c4c609ba23f19c6e5dc5` as exactly the
  five declared planning artifacts; it predeclared no candidate SHA, receipt, subject, evidence, test outcome or approval.
- [x] **Actor:** Independent Plan-Reviewer / Implementer — **Action:** Independent Plan-Reviewer wrote the approved
  SHA-bound C14 receipt and Implementer committed it unchanged alone in
  `033fa34ca27a9c924c7fc95b9aa9c87c33b24217` before any C14 subject.
- [x] **Actor:** Implementer / Tester — **Action:** Created RED test-only subject
  `6acbbe6d3f9b98566def9448afa760e095833a0b` containing only
  `tests/test_loaded_runtime_cache_bc_independence.py`; it must collect successfully and actually fail its chained
  assignment alias assertion. Tester records the actual failing result only at
  `loaded-runtime-cache.tester-evidence-<red-subject-40-hex-sha>.json`; Implementer commits it unchanged alone; no
  Reviewer evidence is allowed for this failing subject. The factual failing evidence was committed alone in
  `287781cee3b7f5603d6ea58059ab3b9782d7e806`.
- [x] **Actor:** Implementer — **Action:** Created distinct green subject
  `5201c30e604c8fd9cc84bd6d05c00c6b61575612` containing the BC-independence test plus
  only the truthful byte-changed subset of the sole ten-path C14 dataflow allowlist. Repair all-simple-name chained
  assignment targets and retain dataflow inputs/returns/geometry/containment without touching Human-owned architecture
  authority paths; byte-identical `.validation.json`／`.visual-check.html` remain ReadOnly.
- [x] **Actor:** Tester / Independent Reviewer — **Action:** Tester recorded passing evidence for the green subject;
  Implementer commits `loaded-runtime-cache.tester-evidence-<green-subject-40-hex-sha>.json` unchanged alone.
  Independent Reviewer consumes only that committed same-subject passing evidence, writes
  `loaded-runtime-cache.implementation-review-log-<green-subject-40-hex-sha>.json`, and Implementer commits it alone.
  These sole evidence-only commits are `6a9a543b1fb4c1389c1c5474e50995440a046dcd` and
  `4632380fa1b254046d04a6b92c9d9912836e7ee1` respectively.
- [ ] **Actor:** Planner / Independent Reviewer — **Action:** After green Phase 4.5, independently classify current
  PR threads. F and ACL remain open Human-only `human-check`; no classification or C14 evidence directly resolves a
  thread.

## Implementation Steps

- [x] 1. **Completed C11 route:** Preserve C11/R11/S11/T11/V11 and C5→V3 as ReadOnly frozen provenance. Do not modify,
  regenerate or reclassify them as C12 evidence.
- [x] 2. **C12 planning candidate:** Modified exactly the five declared planning artifacts to state C12 as sole active
  candidate and define the R12 fixed-snapshot triage contract; committed as `41d51072901cfd205ebc91644036e6695b1fe81c`.
- [x] 3. **R12 factual triage:** Independent Plan-Reviewer verified all ten current snapshot entries each have
  thread/comment/finding/commit/basis/disposition; F and architecture/ACL are `DISCUSS` Human-check, the other eight
  are `SKIP` factual entries. The approved receipt is committed in `d738e91eb20869709d605fe7f879b340c9614b6a`.
- [x] 4. **Phase 4.5:** Planner aligned C12 after the approved R12 receipt. This authorizes only independent PR-thread
  classification. No C12 step comments, resolves, publishes or merges.
- [x] 5. **C14 candidate and receipt:** Committed only five planning artifacts in
  `4d78eaf997847eb3b872c4c609ba23f19c6e5dc5`, then separately committed the SHA-bound approved Plan-Reviewer receipt
  in `033fa34ca27a9c924c7fc95b9aa9c87c33b24217`.
- [x] 6. **C14 RED:** Established the collection-success, assertion-failing chained-assignment test-only subject
  `6acbbe6d3f9b98566def9448afa760e095833a0b` and committed factual failing Tester evidence only in
  `287781cee3b7f5603d6ea58059ab3b9782d7e806`; historical `e2e125` remains preserved.
- [x] 7. **C14 green:** Established green immutable subject `5201c30e604c8fd9cc84bd6d05c00c6b61575612` with
  all-simple-name target coverage and only the
  truthful byte-changed subset of the sole ten named dataflow artifacts; record passing Tester and approved Reviewer
  evidence in separate sole commits `6a9a543b1fb4c1389c1c5474e50995440a046dcd` and
  `4632380fa1b254046d04a6b92c9d9912836e7ee1`.
- [ ] 8. **C14 classification:** Planner Phase 4.5 then independent thread classification; retain F/ACL Human-only
  boundary and stop before Human review/merge.

## Main Agent Actionable Steps — Fixed Tail

- [x] **Actor:** Planner — **Action:** 已對 committed C12→R12 evidence chain 執行 Phase 4.5 alignment。其通過只可
  派遣獨立 Reviewer 分類 fixed-snapshot PR threads；不代表 thread reply／resolution、F／architecture-ACL human-check、
  publish 或 Human action 已完成。
- [ ] **Actor:** Independent Reviewer — **Action:** C12 fixed-snapshot classification is superseded by the
  C14 green-subject Phase 4.5 classification. F／ACL remain Human-only `human-check`; no tracker entry may claim a
  reply／resolve before a fresh independent classification permits that exact thread.

## Handoff / Gate Notes

- This tracker and plan name one `loaded-runtime-cache` topic. The feature branch is lineage only, not routing
  authority.
- C5→V3, C8/C9/C10 and C11/R11/S11/T11/V11 plus C12/R12 and C13 `a623981989f3363a4b225319a432c3a9d8e28b96`→`ade584e7eb63a7846a23c073c06a802ff99ff6cf` are frozen nonrouting
  provenance. C14 does not replay a clean base, recreate historical evidence, or reuse a predecessor receipt/subject.
- `9aa656b13fdc36492273c97a62eb9d422a1b64b5` is additionally frozen unapproved `needs-rework` provenance. It is not
  the pending C14 candidate and cannot be used to infer a receipt, test outcome, approval, or next role.
- The fixed-name legacy plan-review receipt is historical frozen provenance only; it cannot be overwritten, consumed
  or used to route C5 or any successor. A `needs-rework` receipt creates no implementation subject.
- Architecture-only `442cc94`, historical RED/green subjects, T3/V3 and C11/R11/S11/T11/V11 are frozen provenance
  only. C14 creates new evidence only on its prescribed RED→green route.
- Architecture-path overlap is Human review／merge coordination only; it never relaxes declared paths or evidence
  gates.
- C12 `41d51072901cfd205ebc91644036e6695b1fe81c` and approved R12 receipt commit
  `d738e91eb20869709d605fe7f879b340c9614b6a` are committed routing facts. Under the Human-authorized post-receipt
  state-alignment rule, this alignment did not create a new candidate or Plan-Reviewer gate. It is completed frozen
  provenance for C14.
- C14 is at Phase 4.5: its committed candidate/receipt/RED/failing-evidence/green/passing-evidence/approved-review
  chain is factual in `4d78eaf…` → `033fa34…` → `6acbbe6…` → `287781…` → `5201c30…` → `6a9a543…` → `4632380…`.
  This post-receipt state alignment is explicitly Human-authorized tracking only: it creates no new candidate or
  Plan-Reviewer receipt and claims no code review, publish, comment, resolve, F／architecture-ACL ownership, or Human
  action. Independent thread classification remains pending.

## C15 Active Successor Stages (authoritative)

C14 and `37d7233e7231151c0dac6aaa1a7820bff746ffdc` are frozen nonrouting provenance. The C15 stages below supersede
all earlier tracker entries for current routing and inherit no predecessor candidate, receipt, subject, result,
evidence, approval, or next role.

- [x] C15 plan-authoring
- [x] C15 planning-candidate-commit
- [x] C15 independent Plan-Reviewer receipt
- [x] C15 receipt-only commit
- [x] C15 RED test-only subject
- [x] C15 RED factual failing Tester evidence
- [x] C15 RED evidence-only commit
- [x] C15 green test-only subject
- [x] C15 green factual passing Tester evidence
- [x] C15 green evidence-only commit
- [x] C15 independent green review evidence
- [x] C15 review-evidence-only commit
- [ ] C15 Planner Phase 4.5
- [ ] C15 independent thread classification

### C15 actionable steps

- [x] **Actor: Implementer.** Committed only the five C15 planning artifacts in
  `eadd406409a02dc1c283e7ff9740815f4c9e4596`, with no prefilled future SHA/outcome.
- [x] **Actor: Independent Plan-Reviewer / Implementer.** Wrote and unchanged-sole-committed the approved receipt in
  `d8e759ea0bdd70ca7d6eca4dc030f11879c59c25`, at the candidate-SHA-bound receipt path.
- [x] **Actor: Implementer / Tester.** Created the collection-success/assertion-failing RED subject
  `2e9cabd5d21c0ef4c9a9929efedf8efc2a776e6a`, then recorded and unchanged-sole-committed its factual failing
  evidence in `94e6d6f73b85efa5a5895e7eadb4aa9aa24089ee`. No Reviewer record was created for RED.
- [x] **Actor: Implementer.** Created distinct green subject `7dab2b9742bd19f962bef99be83b40b978f87f0f` changing
  only the declared test file. It preserves direct `ast.Name`, ignores direct `ast.Attribute`/other non-simple
  targets without recursion, and retains only `load` in `load = holder.loader = importlib.import_module`.
- [x] **Actor: Tester / Independent Reviewer / Implementer.** Committed same-subject passing Tester evidence alone in
  `475e3c953f6551bef5834d0bf350d5c79449a43e`, then approved matching independent Reviewer evidence alone in
  `cee5097c176b4321a0d9bc2e810caf7d3425d0f1`.
- [ ] **Actor: Planner / Independent Reviewer.** Run Phase 4.5, then fresh independent classification. F／ACL/business
  architecture remain Human-only `human-check`; no C15 action replies, resolves, merges, releases or post-merges.

### C15 current state

The full committed C15 chain is
`eadd406409a02dc1c283e7ff9740815f4c9e4596` →
`d8e759ea0bdd70ca7d6eca4dc030f11879c59c25` →
`2e9cabd5d21c0ef4c9a9929efedf8efc2a776e6a` →
`94e6d6f73b85efa5a5895e7eadb4aa9aa24089ee` →
`7dab2b9742bd19f962bef99be83b40b978f87f0f` →
`475e3c953f6551bef5834d0bf350d5c79449a43e` →
`cee5097c176b4321a0d9bc2e810caf7d3425d0f1`.
It is **Phase 4.5 alignment pending**. This authorized post-receipt state tracking does not create C16, a new
candidate, a new receipt, or new Tester/Reviewer evidence, and it does not reply to, resolve, or otherwise process
any PR thread.

### C15 guardrails

- No recursive destructuring, AST execution, dynamic import (`importlib`, `__import__`, `sys.modules`), runtime
  introspection, cross-BC import, production-source, Archify, workflow, or architecture modification.
- The only C15 implementation path is `tests/test_loaded_runtime_cache_bc_independence.py`; every other unlisted path
  is ReadOnly.

## C16 Thread-Classification Receipt Successor Stages (authoritative)

C15's completed chain is frozen C16 input only. C16 supersedes C15's pending Phase 4.5/classification state; it adds
no implementation, Tester, or green-review subject.

- [x] C15 immutable subject / passing Tester / approved Reviewer inputs exist
- [ ] C16 plan-authoring
- [ ] C16 planning-candidate-commit
- [ ] C16 independent Plan-Reviewer receipt
- [ ] C16 receipt-only commit
- [ ] C16 independent classification receipt
- [ ] C16 classification-receipt-only commit
- [ ] C16 Planner routing for exact classified pairs

### C16 actionable steps

- [ ] **Actor: Implementer.** Commit exactly the five C16 planning artifacts; no source, test, docs/architecture,
  Archify, PR, or evidence file may share this candidate commit.
- [ ] **Actor: Independent Plan-Reviewer / Implementer.** Write fresh approved C16 candidate-SHA-bound Plan-Reviewer
  receipt, then commit it unchanged alone. A `needs-rework` receipt cannot route classification.
- [ ] **Actor: Independent Reviewer / Implementer.** After the committed approved C16 planning receipt, Independent
  Reviewer alone writes
  `plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-7dab2b9742bd19f962bef99be83b40b978f87f0f.json`;
  Implementer commits it unchanged alone. It binds subject `7dab2b9742bd19f962bef99be83b40b978f87f0f`, Tester commit
  `475e3c953f6551bef5834d0bf350d5c79449a43e`, Reviewer commit
  `cee5097c176b4321a0d9bc2e810caf7d3425d0f1`, snapshot `7e525b1ad8dc77c25b0b11a467f6b1f24884ecd3`, and exactly
  seven listed pairs.
- [ ] **Actor: Planner / Implementer.** Only an exact committed `REPLY_AND_RESOLVE` pair may receive its factual
  reply and resolution. `ADDRESS` returns to Planner. ACL `4060023123` and business architecture `4070096561` remain
  `HUMAN_CHECK` with no reply/resolve.

### C16 receipt schema / fixed pair set

The receipt's exact top-level keys are `schema_version`, `topic`, `implementation_subject_commit`,
`tester_evidence_commit`, `implementation_review_evidence_commit`, `pr_head_commit`, `classifications`,
`recorded_by`; values are `1`, `loaded-runtime-cache`, the four fixed C15/Snapshot SHAs above, an exact seven-entry
array, and `Independent Reviewer`. Each entry has exactly `thread`, `comment`, `outcome`, `reply`; outcomes are only
`REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK`, with a non-empty reply only for `REPLY_AND_RESOLVE` and JSON `null` otherwise.

The exact pair set is `PRRT_kwDOUJTij86kQ95O`/`4060023123`, `PRRT_kwDOUJTij86kqiZu`/`4070096548`,
`PRRT_kwDOUJTij86kqiZ5`/`4070096561`, `PRRT_kwDOUJTij86lAR8J`/`4078761983`,
`PRRT_kwDOUJTij86lAR8P`/`4078761993`, `PRRT_kwDOUJTij86lAR8T`/`4078761998`, and
`PRRT_kwDOUJTij86lAR8Y`/`4078762005`. ACL `4060023123` and business architecture `4070096561` are locked
`HUMAN_CHECK`/`null`; C16 does not prefill the other five independent outcomes or replies.

## C17 ADDRESS Remediation Successor Stages (authoritative)

C15/C16 are frozen input. C17 covers only `4078761993` and `4078762005`; `4078761998` remains the separate
Human-only README/public-surface boundary. Its completed commit chain is
`dc55f1a6a32ceabf48490e952af2b9fd71b9efd3` → `35ccbd6` → `7ec3b57` → `3c9c9b8` → `708091b` →
`7ceb340` → `b58cb1` → `edbae51`.

- [x] C17 plan-authoring
- [x] C17 planning-candidate-commit
- [x] C17 independent Plan-Reviewer receipt
- [x] C17 receipt-only commit
- [x] C17 RED test-only subject
- [x] C17 RED factual failing Tester evidence
- [x] C17 RED evidence-only commit
- [x] C17 green test/dataflow subject
- [x] C17 green factual passing Tester evidence
- [x] C17 green evidence-only commit
- [x] C17 independent green review evidence
- [x] C17 review-evidence-only commit
- [x] C17 Planner Phase 4.5 (Human-authorized post-receipt alignment only)
- [ ] C17 independent thread classification

### C17 actionable steps

- [x] **Actor: Implementer / Plan-Reviewer / Tester / Independent Reviewer.** Completed the immutable C17
  candidate → approved receipt → RED/failing evidence → green/dataflow → delivery receipt → passing evidence →
  approved review chain in `dc55f1a6a32ceabf48490e952af2b9fd71b9efd3` → `35ccbd6` → `7ec3b57` → `3c9c9b8` →
  `708091b` → `7ceb340` → `b58cb1` → `edbae51`.
- [ ] **Actor: Independent Reviewer.** Independently classify the two C17 pairs after Phase 4.5. Do not reply or
  resolve before that receipt; retain `4078761998`/README, ACL, and business-architecture threads Human-only/open.

### C17 post-receipt alignment

This alignment is frozen provenance. C18 supersedes its pending classification routing; it creates no C17 candidate,
receipt, Tester/Reviewer evidence, PR reply, or thread resolution.

## C18 C17 Current-Head Classification Successor Stages (authoritative)

C18 is planning-only. It binds completed C17 subject `7ceb3409d6d8b9ff3dc51485c3588f502bdff882`, passing Tester
evidence commit `b58cb1e330fe12ccc80a8f39b875a61ea6024067`, approved Reviewer evidence commit
`edbae51a0ee86cff498d6caf4e6aa78b58962a82`, and PR head `bf63a3c6a0533ad0f367305deff029eddc2b18be`. It changes no
source/test/docs/Archify/README or PR state.

- [x] C18 plan-authoring
- [x] C18 planning-candidate-commit
- [x] C18 independent Plan-Reviewer receipt
- [x] C18 receipt-only commit
- [x] C18 independent classification receipt
- [x] C18 classification-receipt-only commit
- [x] C18 Planner routing for exact classified pairs (post-receipt state alignment only)

### C18 actionable steps

- [x] **Actor: Implementer.** Committed exactly the five C18 planning artifacts in
  `f4f27899eb34976776d4cd6baeb4fd971715edd3`; it prefilled no future candidate SHA, receipt verdict,
  classification disposition, reply, or resolution.
- [x] **Actor: Independent Plan-Reviewer / Implementer.** Wrote and unchanged-sole-committed the approved
  candidate-SHA-bound receipt in `4cd60b2794493b54c8cb9b5b1b4b48b2c04261a0`.
- [x] **Actor: Independent Reviewer / Implementer.** Wrote only
  `plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-7ceb3409d6d8b9ff3dc51485c3588f502bdff882.json`
  and unchanged-sole-committed it in `a4054d23823dd446a0d5ee6ad1cd52ac8430c80c`. Its exact eight keys bind
  C17 subject/T17/V17/PR-head facts and its classifications are exactly eleven pairs.
- [ ] **Actor: Implementer.** Leave the exact committed receipt reply and resolve only these seven pairs:
  `PRRT_kwDOUJTij86jqdPV`/`4044836129`, `PRRT_kwDOUJTij86jqdPZ`/`4044836136`,
  `PRRT_kwDOUJTij86kOjjo`/`4059094458`, `PRRT_kwDOUJTij86kqiZu`/`4070096548`,
  `PRRT_kwDOUJTij86lAR8J`/`4078761983`, `PRRT_kwDOUJTij86lAR8P`/`4078761993`, and
  `PRRT_kwDOUJTij86lAR8Y`/`4078762005`. Do not act on the four `HUMAN_CHECK` pairs or on new unclassified threads
  `PRRT_kwDOUJTij86lCkFr` and `PRRT_kwDOUJTij86lCkFu`.

### C18 exact classification set

`PRRT_kwDOUJTij86jnBpk`/`4043480108`, `PRRT_kwDOUJTij86jqdPV`/`4044836129`,
`PRRT_kwDOUJTij86jqdPZ`/`4044836136`, `PRRT_kwDOUJTij86kOjjo`/`4059094458`,
`PRRT_kwDOUJTij86kQ95O`/`4060023123`, `PRRT_kwDOUJTij86kqiZu`/`4070096548`,
`PRRT_kwDOUJTij86kqiZ5`/`4070096561`, `PRRT_kwDOUJTij86lAR8J`/`4078761983`,
`PRRT_kwDOUJTij86lAR8P`/`4078761993`, `PRRT_kwDOUJTij86lAR8T`/`4078761998`,
`PRRT_kwDOUJTij86lAR8Y`/`4078762005`. Each entry uses exactly `thread`, `comment`, `outcome`, `reply`.
F, ACL, business and README are the fixed Human-only entries; the committed receipt classifies each of the other
seven as `REPLY_AND_RESOLVE` with its exact factual reply.

### C18 post-receipt state alignment

The committed C18 chain is `f4f27899eb34976776d4cd6baeb4fd971715edd3` →
`4cd60b2794493b54c8cb9b5b1b4b48b2c04261a0` → `a4054d23823dd446a0d5ee6ad1cd52ac8430c80c`.
Its exact seven `REPLY_AND_RESOLVE` pairs are pending Implementer action. F
`PRRT_kwDOUJTij86jnBpk`/`4043480108`, ACL `PRRT_kwDOUJTij86kQ95O`/`4060023123`, business
`PRRT_kwDOUJTij86kqiZ5`/`4070096561`, and README `PRRT_kwDOUJTij86lAR8T`/`4078761998` remain open
`HUMAN_CHECK`. New `PRRT_kwDOUJTij86lCkFr` and `PRRT_kwDOUJTij86lCkFu` are open/unclassified and outside C18.
This state alignment creates no C19, candidate, receipt, new evidence, actual reply, or resolution.

## C19 Current-Head Reconciliation Classification Successor Stages (authoritative)

C19 supersedes C18 only for fresh current-head classification. It binds C17 subject
`7ceb3409d6d8b9ff3dc51485c3588f502bdff882`, passing Tester evidence commit
`b58cb1e330fe12ccc80a8f39b875a61ea6024067`, approved Reviewer evidence commit
`edbae51a0ee86cff498d6caf4e6aa78b58962a82`, and current PR head
`3e803a507b2dfa74efdf71164c260da172aadb81`. It changes no source/test/docs/Archify/README or PR state.

- [x] C19 plan-authoring
- [ ] C19 planning-candidate-commit
- [ ] C19 independent Plan-Reviewer receipt
- [ ] C19 receipt-only commit
- [ ] C19 independent classification/reconciliation receipt
- [ ] C19 classification-receipt-only commit
- [ ] C19 Planner routing for exact classified pairs

### C19 actionable steps

- [ ] **Actor: Implementer.** Commit exactly the five C19 planning artifacts; prefill no candidate SHA, receipt
  verdict, classification disposition, reply or resolution.
- [ ] **Actor: Independent Plan-Reviewer / Implementer.** Write an approved standard candidate-SHA-bound receipt,
  then unchanged-sole-commit it.
- [ ] **Actor: Independent Reviewer / Implementer.** Write and unchanged-sole-commit only
  `plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-7ceb3409d6d8b9ff3dc51485c3588f502bdff882-3e803a507b2dfa74efdf71164c260da172aadb81.json`.
  It has exactly eight top-level keys and exactly five pairs: `lCkFr`/`4079664571`, `lCkFu`/`4079664575`,
  `lDH2-`/`4079885261`, `lDH3C`/`4079885267`, and `lAR8Y`/`4078762005`.
- [ ] **Actor: Planner.** Route only exact committed `REPLY_AND_RESOLVE` entries. For `lAR8Y`, an
  `ALREADY_RESOLVED`/`null` entry is valid only when current GitHub state was independently verified; it never
  authorizes action. Do not act on F, ACL, business or README Human-only locks.

## C20 C19 ADDRESS Remediation Successor Stages (authoritative)

C20 supersedes C19 only for `lCkFu`/`4079664575` and `lDH2-`/`4079885261`. It does not prefill a candidate SHA,
verdict, subject, test result, PR head, classification outcome, reply or resolution. All locks and every unlisted path
are ReadOnly.

- [x] C20 plan-authoring
- [x] C20 planning-candidate-commit (`77835c29b90304cff9b0c3193bde4c297ec96612`)
- [x] C20 independent Plan-Reviewer receipt
- [x] C20 receipt-only commit (`8a31db2d9ccccaf46363d714be457a0cd4700a3e`)
- [x] C20 test-only RED subject (`f87bb1a9580a08196989374e069a82cccafd6c72`)
- [x] C20 failing Tester evidence-only commit (`55e91c9ff3a785af3279d8ebd9e3dfd3d69bc2a3`)
- [x] C20 green subject plus truthful dataflow outputs (`fa1468301af1906a05ee31ba0d267d2270d7af5f`)
- [x] C20 passing Tester evidence-only commit (`6423f55b6dbcde5bee190ef86dc8c31f5c27c94e`)
- [x] C20 approved independent Reviewer evidence-only commit (`3d0dc9fbb0e9da6d742ac20856b8aac6b0a3035e`)
- [ ] C20 Planner Phase 4.5 alignment
- [ ] C20 independent two-pair classification receipt
- [ ] C20 classification-receipt-only commit
- [ ] C20 Planner routing for exact classified pairs

**C20 post-review state:** the seven commits above are the complete committed chain. Phase 4.5 remains pending until
Planner verifies the actual pushed PR head contains it. That alignment alone may route the already-defined independent
two-pair classification receipt for `lCkFu`/`4079664575` and `lDH2-`/`4079885261`; it creates neither C21 nor a new
contract and authorizes no reply or resolution.

### C20 actionable steps

- [ ] **Actor: Implementer.** Commit exactly the five C20 planning artifacts, then only an unchanged standard
  candidate-SHA-bound approved Plan-Reviewer receipt in its sole receipt-only commit.
- [ ] **Actor: Implementer / Tester.** Make a test-only RED subject in
  `tests/test_loaded_runtime_cache_bc_independence.py` that collects and fails for the separate expected-failure
  dataflow signal and `ModelIdentity as LocalModelIdentity` foreign `ImportFrom` alias; Tester writes factual failing
  evidence and Implementer commits only that evidence unchanged.
- [ ] **Actor: Implementer / Tester / Independent Reviewer.** Make a distinct green subject in that test and only
  byte-truthfully changed paths in the ten-path C20 dataflow allowlist; validate → deliver → non-skipped visual-check
  must pass (including 1440×900, 1600×1000, 1920×1080, 2048×1320). Tester then records passing evidence; Independent
  Reviewer may review only that committed passing evidence; each evidence is committed by Implementer unchanged and
  alone.
- [ ] **Actor: Independent Reviewer / Implementer.** After Phase 4.5, write then unchanged-sole-commit only the
  C20 green-subject-SHA-bound classification receipt. It has exactly two pairs: `lCkFu`/`4079664575` and
  `lDH2-`/`4079885261`; it preselects neither outcome nor reply. Only its exact committed
  `REPLY_AND_RESOLVE` entry can later authorize the corresponding reply and resolve action.

## C21 Current-Head Single-Pair Classification Successor Stages (authoritative)

C21 supersedes C20 only for `PRRT_kwDOUJTij86ldYVf`/`4090457782`. It binds C20 subject
`fa1468301af1906a05ee31ba0d267d2270d7af5f`, passing Tester evidence commit
`6423f55b6dbcde5bee190ef86dc8c31f5c27c94e`, approved Reviewer evidence commit
`3d0dc9fbb0e9da6d742ac20856b8aac6b0a3035e`, and current PR head
`a1aae44897c0f0b0ac52f1ca1697554c2f79cdb5`. It changes no source, tests, docs, Archify, README or PR state.

- [x] C21 plan-authoring
- [ ] C21 planning-candidate-commit
- [ ] C21 independent Plan-Reviewer receipt
- [ ] C21 receipt-only commit
- [ ] C21 independent single-pair classification receipt
- [ ] C21 classification-receipt-only commit
- [ ] C21 Planner routing for the exact classified pair

### C21 actionable steps

- [ ] **Actor: Implementer.** Commit exactly the five C21 planning artifacts; prefill no candidate SHA, receipt
  verdict, classification outcome, reply or resolution.
- [ ] **Actor: Independent Plan-Reviewer / Implementer.** Write an approved standard candidate-SHA-bound receipt,
  then unchanged-sole-commit it.
- [ ] **Actor: Independent Reviewer / Implementer.** Write and unchanged-sole-commit only
  `plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-fa1468301af1906a05ee31ba0d267d2270d7af5f-a1aae44897c0f0b0ac52f1ca1697554c2f79cdb5.json`.
  It has exactly eight top-level keys and exactly one pair: `PRRT_kwDOUJTij86ldYVf`/`4090457782`.
- [ ] **Actor: Planner.** Route only an exact committed `REPLY_AND_RESOLVE` entry. Do not act on every other
  thread, including all existing Human-only locks; `ADDRESS` returns to planning and `HUMAN_CHECK` remains open.

## C22 Current-Head Dual-Pair Classification Successor Stages (authoritative)

C22 supersedes C21 only for `PRRT_kwDOUJTij86ldeVI`/`4090495760` and
`PRRT_kwDOUJTij86ldeVO`/`4090495770`. It binds C20 subject
`fa1468301af1906a05ee31ba0d267d2270d7af5f`, passing Tester evidence commit
`6423f55b6dbcde5bee190ef86dc8c31f5c27c94e`, approved Reviewer evidence commit
`3d0dc9fbb0e9da6d742ac20856b8aac6b0a3035e`, and current PR head
`0991c56ec7e562ea512449bda1a41118dbc48203`. It changes no source, tests, docs, Archify, README or PR state.

- [x] C22 plan-authoring
- [ ] C22 planning-candidate-commit
- [ ] C22 independent Plan-Reviewer receipt
- [ ] C22 receipt-only commit
- [ ] C22 independent dual-pair classification receipt
- [ ] C22 classification-receipt-only commit
- [ ] C22 Planner routing for the exact classified pairs

### C22 actionable steps

- [ ] **Actor: Implementer.** Commit exactly the five C22 planning artifacts; prefill no candidate SHA, receipt
  verdict, classification outcome, reply or resolution.
- [ ] **Actor: Independent Plan-Reviewer / Implementer.** Write an approved standard candidate-SHA-bound receipt,
  then unchanged-sole-commit it.
- [ ] **Actor: Independent Reviewer / Implementer.** Write and unchanged-sole-commit only
  `plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-fa1468301af1906a05ee31ba0d267d2270d7af5f-0991c56ec7e562ea512449bda1a41118dbc48203.json`.
  It has exactly eight top-level keys and exactly two pairs: `ldeVI`/`4090495760` and `ldeVO`/`4090495770`.
- [ ] **Actor: Planner.** Route only exact committed `REPLY_AND_RESOLVE` entries. F, ACL, business architecture and
  README remain Human-only open locks. `PRRT_kwDOUJTij86ld9Ai` is excluded, unclassified and open; do not act on it.

## C23 C22 ADDRESS Remediation Successor Stages (authoritative)

C23 supersedes C22 only for `PRRT_kwDOUJTij86ldeVI`/`4090495760` and
`PRRT_kwDOUJTij86ldeVO`/`4090495770`. It consumes only C22 classification receipt commit
`a9065a8332119930347214f07f2980d655d8d314`, at
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-fa1468301af1906a05ee31ba0d267d2270d7af5f-0991c56ec7e562ea512449bda1a41118dbc48203.json`,
which binds C20 subject `fa1468301af1906a05ee31ba0d267d2270d7af5f`, passing Tester evidence
`6423f55b6dbcde5bee190ef86dc8c31f5c27c94e`, approved Reviewer evidence
`3d0dc9fbb0e9da6d742ac20856b8aac6b0a3035e`, and C22 PR head `0991c56ec7e562ea512449bda1a41118dbc48203`.
It leaves source behavior, Human-only locks and `ld9Ai`/`4090688118` ReadOnly unless an exact declared C23 step
permits otherwise.

- [x] C23 plan-authoring
- [ ] C23 planning-candidate-commit
- [ ] C23 independent Plan-Reviewer receipt
- [ ] C23 receipt-only commit
- [ ] C23 RED scanner/dataflow subject
- [ ] C23 RED factual failing Tester evidence
- [ ] C23 RED evidence-only commit
- [ ] C23 green scanner/dataflow subject
- [ ] C23 green factual passing Tester evidence
- [ ] C23 green evidence-only commit
- [ ] C23 independent green review evidence
- [ ] C23 review-evidence-only commit
- [ ] C23 Planner Phase 4.5/current-head verification
- [ ] C23 independent dual-pair classification receipt
- [ ] C23 classification-receipt-only commit
- [ ] C23 Planner routing for exact classified pairs

### C23 actionable steps

- [ ] **Actor: Implementer.** Commit exactly the five C23 planning artifacts; do not prefill a future SHA, verdict,
  outcome, reply, resolution or current head.
- [ ] **Actor: Independent Plan-Reviewer / Implementer.** Write fresh approved standard candidate-SHA-bound receipt,
  then commit it unchanged alone.
- [ ] **Actor: Implementer / Tester.** Create a collection-success/assertion-failing RED subject limited to the
  scanner test. It must expose the NamedExpr alias bypass and dataflow fidelity defect without fixture execution or
  dynamic import; Tester writes factual failing SHA-bound evidence and Implementer commits that evidence alone.
- [ ] **Actor: Implementer / Tester / Independent Reviewer.** Create a distinct green subject changing only the
  scanner test and the dataflow JSON/HTML plus byte-truthfully changed existing validation/delivery/visual-check
  evidence. Preserve `lookup(...) -> RuntimeT | None` and the sole signal edge. Commit passing Tester evidence alone;
  Independent Reviewer consumes it and Implementer commits only that review record.
- [ ] **Actor: Planner / Independent Reviewer / Implementer.** After actual-current-head verification, Independent
  Reviewer writes only
  `plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-<c23-green-subject-40-hex-sha>-<current-pr-head-40-hex-sha>.json`;
  Implementer commits it unchanged alone. Its top-level keys are exactly `schema_version`, `topic`,
  `implementation_subject_commit`, `tester_evidence_commit`, `implementation_review_evidence_commit`,
  `pr_head_commit`, `classifications`, `recorded_by`; entries have exactly `thread`, `comment`, `outcome`, `reply` for
  only `ldeVI`/`4090495760` and `ldeVO`/`4090495770`; outcome is only
  `REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK`, with non-empty factual reply only for `REPLY_AND_RESOLVE` and JSON `null`
  otherwise. Only exact committed `REPLY_AND_RESOLVE` entries may receive their factual reply and resolution.
  F/ACL/business/README Human-only locks and `ld9Ai` stay open/unclassified.

## C24 C23 Current-Head Dual-Pair Classification Successor Stages (authoritative)

C24 supersedes C23 only for `PRRT_kwDOUJTij86lfQl9`/`4091213935` and
`PRRT_kwDOUJTij86lfQmF`/`4091213944`. It consumes subject `240c694fa5078dc1d35f154f7a85b06381db2e47`, passing Tester
`dabce082058805281990c52b12352b87c2b46801`, approved Reviewer `489752c727aa86cfaf49038cc2ed6dfddf33ba2d`, and C23
classification provenance/current head `e5872d5dfb2018743b1f7e319551d52f25f5ef02`. It changes no source, tests,
docs, architecture, README or PR state.

- [x] C24 plan-authoring
- [ ] C24 planning-candidate-commit
- [ ] C24 independent Plan-Reviewer receipt
- [ ] C24 receipt-only commit
- [ ] C24 independent dual-pair classification receipt
- [ ] C24 classification-receipt-only commit
- [ ] C24 Planner routing for exact classified pairs

### C24 actionable steps

- [ ] **Actor: Implementer.** Commit exactly the five C24 planning artifacts; do not prefill candidate SHA, receipt
  verdict, classification outcome, reply or resolution.
- [ ] **Actor: Independent Plan-Reviewer / Implementer.** Write approved standard candidate-SHA-bound receipt, then
  commit it unchanged alone.
- [ ] **Actor: Independent Reviewer / Implementer.** Write and unchanged-sole-commit only
  `plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-240c694fa5078dc1d35f154f7a85b06381db2e47-e5872d5dfb2018743b1f7e319551d52f25f5ef02.json`.
  It has exactly eight top-level keys and exactly two pairs: `lfQl9`/`4091213935`, `lfQmF`/`4091213944`.
- [ ] **Actor: Planner.** Route only exact committed `REPLY_AND_RESOLVE` entries. C23 resolved pairs remain frozen;
  F/ACL/business/README remain Human-only open locks and `ld9Ai` is excluded, open and unclassified.

## C25 lfQl9 Static Attribute-base NamedExpr Remediation Stages (authoritative)

C25 supersedes C24 only for `PRRT_kwDOUJTij86lfQl9`/`4091213935`. It adds no outcome, reply, current-head or SHA fact
to its candidate. `lfQmF`/`4091213944`, F/ACL/business/README Human-only locks, `ld9Ai`, all predecessor evidence,
production source, docs and dataflow are ReadOnly.

- [x] C25 plan-authoring
- [x] C25 planning-candidate-commit
- [x] C25 independent Plan-Reviewer receipt
- [x] C25 receipt-only commit
- [x] C25 test-only RED subject
- [x] C25 factual failing Tester evidence
- [x] C25 RED evidence-only commit
- [x] C25 test-only green subject
- [x] C25 factual passing Tester evidence
- [x] C25 green evidence-only commit
- [x] C25 independent green review evidence
- [x] C25 review-evidence-only commit
- [x] C25 Planner actual-current-head verification
- [x] C25 independent one-pair classification receipt
- [x] C25 classification-receipt-only commit
- [x] C25 Planner routing for exact classified pair

### C25 actionable steps

- [x] **Actor: Implementer.** Commit exactly the five C25 planning artifacts. Do not prefill candidate SHA, receipt
  verdict, implementation/evidence SHA, PR head, classification outcome, reply or resolution.
- [x] **Actor: Independent Plan-Reviewer / Implementer.** Write fresh approved standard candidate-SHA-bound receipt,
  then commit it unchanged alone.
- [x] **Actor: Implementer / Tester.** Create a collection-success/assertion-failing RED subject changing only
  `tests/test_loaded_runtime_cache_bc_independence.py`, exposing static
  `(loader := importlib).import_module(...)` attribute-base NamedExpr alias detection. Tester writes factual failing
  evidence; Implementer commits only that evidence unchanged.
- [x] **Actor: Implementer / Tester / Independent Reviewer.** Create a distinct green subject changing only the same
  test. Detect only direct `ast.Attribute`/`ast.NamedExpr`/simple-name-target/known-`importlib`-alias/`import_module`
  shape; do not recurse, execute, dynamically import or introspect. Preserve direct-name NamedExpr, mixed assignment,
  `getattr` and `sys.modules`. Commit passing Tester evidence alone; Independent Reviewer consumes it and Implementer
  commits only that review record.
- [x] **Actor: Planner / Independent Reviewer / Implementer.** After actual-current-head verification, Independent
  Reviewer writes only
  `plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-<c25-green-subject-40-hex-sha>-<actual-current-pr-head-40-hex-sha>.json`;
  Implementer commits it unchanged alone. It has exact eight top-level keys and exactly one `thread`, `comment`,
  `outcome`, `reply` entry for `lfQl9`/`4091213935`. Only committed `REPLY_AND_RESOLVE` with non-empty factual reply
  can later route exact reply/resolve; `ADDRESS` returns to Planner and `HUMAN_CHECK` remains open.

## C26 Current-Head Seven-Pair Classification Successor Stages (authoritative)

C26 is the current planning-only successor. It binds C25 green subject
`13f987a41119590621671c429293cf549055672b`, passing Tester evidence commit
`e85f936505a323e6c84c02e90f4c4114e39b6505`, approved Reviewer evidence commit
`24d5141332cbc4dcf7a87dea7f134207a16ab37e`, and current-head base
`8bd9460950237c48c9befb73a1c5b80d084e88ae`. It changes no source, test, docs, dataflow, architecture, README or PR
state before a committed exact C26 classification receipt authorizes later routing.

- [x] C26 plan-authoring
- [x] C26 planning-candidate-commit
- [x] C26 independent Plan-Reviewer receipt
- [x] C26 receipt-only commit
- [x] C26 independent seven-pair classification receipt
- [x] C26 classification-receipt-only commit
- [x] C26 Planner routing for exact classified pairs

### C26 actionable steps

- [x] **Actor: Implementer.** Commit exactly the five C26 planning artifacts; do not prefill candidate SHA, receipt
  verdict, classification outcome, reply or resolution.
- [x] **Actor: Independent Plan-Reviewer / Implementer.** Write approved standard candidate-SHA-bound receipt, then
  commit it unchanged alone.
- [x] **Actor: Independent Reviewer / Implementer.** Write and unchanged-sole-commit only
  `plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-13f987a41119590621671c429293cf549055672b-8bd9460950237c48c9befb73a1c5b80d084e88ae.json`.
  It has exactly eight top-level keys and exactly seven `thread`, `comment`, `outcome`, `reply` entries for
  `ld9Ai`/`4090688118`, `lfYsF`/`4091265104`, `lfYsH`/`4091265108`, `lfYsK`/`4091265115`, `m8u00`/`4129370918`,
  `m8u04`/`4129370926`, `m8u09`/`4129370931`. Only committed `REPLY_AND_RESOLVE` with non-empty factual reply may
  later receive the matching exact reply/resolve; `ADDRESS` returns to Planner and `HUMAN_CHECK` remains open.
- [x] **Actor: Planner.** Route only exact committed C26 entries. `jnBpk`, `kQ95O`, `kqiZ5`, `lAR8T`, and `lfQmF`
  remain Human-only open exclusions; C25 `lfQl9` and every other unlisted thread remain ReadOnly.

## C27 Bounded Architecture-Document Conflict-Resolution Stages (authoritative)

C27 follows committed C26 classification receipt `31ab754aae443f702fa4ccc028d53a6c687e48aa`. It is limited to the factual three-way integration of merge
base `37d433e198a955f0710ecd5335666760aa86a20c`, Runtime Cache fact
`442cc9461854d3909345edb26d1434bfaaa1b86e`, Model Execution fact
`5f483a05e63c9dc8f3c63b04a63c8adec3ed2e28`, and dev head
`1501f380f20492c71275474f800fdaaffbf0a76a`; it adds no architecture decision.

- [x] C27 plan-authoring
- [x] C27 planning-candidate-commit
- [x] C27 independent Plan-Reviewer receipt
- [x] C27 receipt-only commit
- [x] C27 five-file integration subject
- [x] C27 factual Tester evidence
- [x] C27 Tester-evidence-only commit
- [x] C27 independent implementation review evidence
- [x] C27 review-evidence-only commit
- [x] C27 Planner Phase 4.5 alignment
- [x] C27 bounded push updating existing draft PR

### C27 actionable steps

- [x] **Actor: Implementer.** Commit exactly the five C27 planning artifacts; do not prefill candidate SHA, receipt
  verdict, integration subject SHA, test result, or review verdict.
- [x] **Actor: Plan-Reviewer.** Write a standard candidate-SHA-bound approved receipt.
- [x] **Actor: Implementer.** Commit that Plan-Reviewer receipt unchanged in its own sole receipt-only commit.
- [x] **Actor: Implementer.** Create one immutable integration subject that manually resolves only
  `docs/architecture/business-capability/architecture-brief.md`,
  `docs/architecture/business-capability/index.html`, `docs/architecture/business-capability/scene.js`,
  `docs/business-capability-architecture.md`, and `docs/evolution-roadmap.md`; retain only the listed committed facts,
  no new architecture decision.
- [x] **Actor: Tester.** Only after the five-file integration subject is committed, write factual evidence at
  `plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<c27-integration-subject-40-hex-sha>.json`, bound
  to that exact full subject SHA.
- [x] **Actor: Implementer.** Commit that Tester evidence unchanged in its own sole evidence-only commit.
- [x] **Actor: Independent Reviewer.** Consume only the committed passing Tester evidence for that same full subject
  SHA and write review evidence at
  `plan/loaded-runtime-cache/loaded-runtime-cache.implementation-review-log-<c27-integration-subject-40-hex-sha>.json`.
- [x] **Actor: Implementer.** Commit that Independent Reviewer evidence unchanged in its own later, separate sole
  evidence-only commit.
- [x] **Actor: Planner.** After the committed approved review evidence, perform C27 Phase 4.5 alignment.
- [x] **Actor: Implementer.** After Planner Phase 4.5, push only the bounded update to the existing draft PR.
  All PR threads—including C26 outcomes and Human-only locks—remain ReadOnly; no reply or resolution is authorized.

## C28 Post-C27 Eight-Pair Repair and Classification Stages (authoritative)

C25 and C26 tracker states above are aligned to their committed receipts and routes; C27 is aligned to candidate
`2dac62be230fe3daf6c259389c93a6e29cfa7006`, integration subject
`21747f2a24dedc2d18eaf2fbd6c8bc0bb0670585`, Tester evidence
`294f7fb5ea0502236c277e545ba9e2dc311596e3`, and approved review
`190c41bb3480753f78bdf97c778583bee0f6ff2f`. All are frozen C28 inputs. C28 covers only `lfYsH`/`4091265108`,
`lfYsK`/`4091265115`, `m8u04`/`4129370926`, `m8u09`/`4129370931`, `m82WL`/`4129419161`,
`m82WS`/`4129419173`, `m9eUV`/`4129677944`, and `m9eUY`/`4129677947`.

- [x] C28 plan-authoring
- [x] C28 planning-candidate-commit
- [x] C28 independent Plan-Reviewer receipt
- [x] C28 receipt-only commit
- [x] C28 RED test subject
- [x] C28 RED factual failing Tester evidence
- [x] C28 RED evidence-only commit
- [x] C28 green bounded repair subject
- [x] C28 green factual passing Tester evidence
- [x] C28 green Tester-evidence-only commit
- [x] C28 independent green review evidence
- [x] C28 green review-evidence-only commit
- [x] C28 Planner Phase 4.5 alignment
- [x] C28 bounded push update
- [x] C28 Planner actual-current-head verification
- [x] C28 independent eight-pair classification receipt
- [x] C28 classification-receipt-only commit
- [x] C28 Planner routing for exact classified pairs
- [x] C28 exact eight-pair reply and resolution

### C28 actionable steps

**Historical C28 state:** `pr-open / exact eight-pair reply-and-resolve completed`。已提交 final green subject
`e4734aaa7d630542e13c37920593602fe8eb64cd`、passing Tester evidence
`b310dd12666aba754b55b0e1d6af5d9520696582` 與 approved Independent Reviewer evidence
`79b8095864ec8ed54db4ef107dbd06a33cdfab87`；Planner 已完成 Phase 4.5 alignment、bounded push 及 actual-current-head
`d9d851df9d5a17503f5503bb8f400f7fbc3137f4` verification。Independent Reviewer 的 exact eight-pair
`REPLY_AND_RESOLVE` receipt 已原樣以 sole evidence-only commit
`e41235af9eee729b151a06dfeaa36137c58e156b` 提交並推送，Planner 已據此 routing。preceding tracking commit
`2d204b070cc9701cfdce31940cbfe377403f1894` 非 PR action evidence；其後 Implementer／Planner live 核實 exact receipt
replies：`lfYsH`→`4140433910`、`lfYsK`→`4140435052`、`m8u04`→`4140436064`、`m8u09`→`4140436858`、
`m82WL`→`4140437667`、`m82WS`→`4140438539`、`m9eUV`→`4140439397`、`m9eUY`→`4140440128`，八個均 `isResolved: true`。

- [x] **Actor: Implementer.** Commit exactly the five C28 planning artifacts; do not prefill future SHA, verdict,
  test result, classification outcome, reply or resolution.
- [x] **Actor: Independent Plan-Reviewer / Implementer.** Write an approved standard candidate-SHA-bound receipt and
  commit it unchanged alone.
- [x] **Actor: Implementer / Tester.** Create RED only in `tests/test_loaded_runtime_cache_bc_independence.py` and
  `tests/test_loaded_runtime_cache_contracts.py`; record factual failure unchanged and alone. No RED review evidence.
- [x] **Actor: Implementer / Tester / Independent Reviewer.** Create distinct green only in those tests,
  `runtime_reuse_key.py`, and the truthful changed subset of the ten existing dataflow artifacts. Record passing Tester
  and approved same-subject Independent Reviewer evidence in separate sole commits.
- [x] **Actor: Planner / Independent Reviewer / Implementer.** After actual-current-head verification, Independent
  Reviewer writes only the SHA-bound C28 eight-pair classification receipt. Implementer commits it unchanged alone;
  only exact committed `REPLY_AND_RESOLVE` entries may later receive their factual reply and resolution.
- [x] **Actor: Implementer.** Leave the exact committed receipt reply and resolve each of the eight C28 pairs only;
  receipt commit `e41235af9eee729b151a06dfeaa36137c58e156b` records their classification, not completed PR actions.
- [x] **Actor: Planner.** Keep `jnBpk`, `kQ95O`, `kqiZ5`, `lAR8T`, and `lfQmF` Human-only/open; all unlisted threads
  and paths remain ReadOnly.

## C29 Three-File Architecture Conflict Integration Stages (authoritative current routing)

Historical C29: `pr-open / bounded publish and audit completed`。candidate `bd465e53614594ce2d4739cac19d28d17927986c`；
approved plan receipt sole commit `b3e9b0f242632be4280553f0bed64214020e167f`；integration subject
`9c6ec737e9a900e2bcd1a02f2a6808bcb91e73aa`；passing Tester sole commit
`31e727d96d4e0843714dca1c7898ac93da9c33ef`；approved independent review sole commit
`fc12dea6be989aaecfdfc71a86fa1b330256fffe`。bounded push／PR audit completed，audited head
`ee2825c785aad152e5785a021acdb68e3056e84d`。
dev `d6ff74ddf65c615f65eeba252e648784252a2bfd`，已整合 base
`1501f380f20492c71275474f800fdaaffbf0a76a`。完整 committed dev tree 自動整合，手動解衝僅
`docs/architecture/business-capability/architecture-brief.md`、`docs/architecture/business-capability/index.html`、
`docs/architecture/business-capability/scene.js`；保留 Runtime protocol／Model Execution 與 fixed-codec／bytes-envelope
committed facts，不作新決策。三檔外不可手動修改；dev worktree 不寫入。

- [x] **Actor: Plan-Creator.** 五份 C29 planning artifacts drafting；不預填未來 SHA／result／verdict。
- [x] **Actor: Implementer.** 五份 artifacts candidate-only commit。
- [x] **Actor: Independent Plan-Reviewer.** standard three-key verdict receipt 寫入
  `plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<c29-candidate-40-hex-sha>.json`。
- [x] **Actor: Implementer.** approved receipt 原樣 sole evidence-only commit。
- [x] **Actor: Implementer.** fixed-dev full-tree immutable integration merge subject，記錄實際 first parent feature HEAD
  full SHA，second parent 為固定 dev SHA；僅三檔手動解衝，no marker／extra manual delta／new architecture decision。
- [x] **Actor: Tester.** 實際 subject topology、manual bounds、facts、document/scene consistency／regressions evidence；
  唯一寫入 `plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<c29-integration-subject-40-hex-sha>.json`。
  exact six-key schema／actual exit-code／passing-failing semantics 依 technical-spec C29。
- [x] **Actor: Implementer.** 原樣 Tester evidence sole commit，不混 planning／source／另一 evidence。
- [x] **Actor: Independent Reviewer.** 僅消費 committed passing same-subject Tester；唯一寫入
  `plan/loaded-runtime-cache/loaded-runtime-cache.implementation-review-log-<c29-integration-subject-40-hex-sha>.json`，
  exact seven-key schema／same subject／Tester sole commit binding 依 technical-spec C29。
- [x] **Actor: Implementer.** 原樣 review evidence later separate sole commit；needs-rework 回新 subject 完整 sequence。
- [x] **Actor: Planner / Plan-Creator.** committed approved evidence 後 Phase 4.5 factual plan／step alignment。
- [x] **Actor: Implementer.** bounded push 更新既有 PR。
- [x] **Actor: Planner.** actual head／mergeability／thread audit；C29 無 thread actions。

Human-only `jnBpk`/`4043480108`, `kQ95O`/`4060023123`, `kqiZ5`/`4070096561`, `lAR8T`/`4078761998`,
`lfQmF`/`4091213944` 維持 open。未分類/open `m-94E`/`4130289778`, `m-94K`/`4130289786`, `nXkrM`/`4140364926`,
`nXrAw`/`4140406331`, `nXrA0`/`4140406337` 無 disposition。C29 不授權 classification／reply／resolve、Human PR
approval／merge、release／post-merge。

## C30 Current-Head Seven-Pair Classification Stages (authoritative current routing)

Historical C30：`classification committed / exact permitted replies completed`。Fixed C29 S `9c6ec737e9a900e2bcd1a02f2a6808bcb91e73aa`、
T `31e727d96d4e0843714dca1c7898ac93da9c33ef`、V `fc12dea6be989aaecfdfc71a86fa1b330256fffe`、
audited head `ee2825c785aad152e5785a021acdb68e3056e84d`。Pairs 恰為 `m-94E`/`4130289778`、
`m-94K`/`4130289786`、`nXkrM`/`4140364926`、`nXrAw`/`4140406331`、`nXrA0`/`4140406337`、
`nXzEu`/`4140459575`、`nXzE1`/`4140459585`。No new implementation／RED／green。

- [x] **Actor: Plan-Creator.** Five-artifact C30 draft, C29 factual publish／audit alignment only.
- [x] **Actor: Implementer.** Exact-five non-merge planning-candidate-only commit `1293b6ed80c0a5018b4eb6a2cbb2099c04415ac0`.
- [x] **Actor: Independent Plan-Reviewer.** Standard three-key SHA-bound C30 candidate receipt.
- [x] **Actor: Implementer.** Approved receipt unchanged sole evidence-only commit `4c313fbdbd819dcddcf5bc880c3cb5d2e419fdaf`.
- [x] **Actor: Planner.** Verify committed C29 S/T/V and fixed actual PR head.
- [x] **Actor: Independent Reviewer.** Write only fixed immutable C30 seven-pair classification receipt:
  `plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-9c6ec737e9a900e2bcd1a02f2a6808bcb91e73aa-ee2825c785aad152e5785a021acdb68e3056e84d.json`;
  exact eight-key／four-key entries／writer／enums／nullability per technical-spec C30, no preclassified disposition.
- [x] **Actor: Implementer.** Receipt unchanged separate sole evidence-only commit `005ec865f216de9f63f7dbfdd8df424d78a03afa`.
- [x] **Actor: Planner.** Route individually from committed receipt; five ADDRESS pairs passed to C31 repair.
- [x] **Actor: Implementer.** Exact replies `m-94E`→`4140750473`, `nXrAw`→`4140753564`; both live resolved.

Five Human-only locks `jnBpk`, `kQ95O`, `kqiZ5`, `lAR8T`, `lfQmF` excluded/open. All unlisted paths／threads
ReadOnly; no Human approval／merge／release／post-merge. Invalid head／pair／schema／writer／SHA／sole ordering fails closed.

## C31 Five-ADDRESS Bounded Repair Stages（completed predecessor routing）

Historical C31：`pr-open / five exact thread actions completed`。Exact pairs: `m-94K`/`4130289786`, `nXkrM`/`4140364926`,
`nXrA0`/`4140406337`, `nXzEu`/`4140459575`, `nXzE1`/`4140459585`. RED only independence test file;
green only that file and business-capability `scene.js`, `index.html`. Detailed locked cases/path/schema authority is
technical-spec C31. No future subject/head/result/verdict/classification/reply/resolution is prefilled.

- [x] **Actor: Plan-Creator.** Five standard planning artifacts draft and verified C30 historical alignment only.
- [x] **Actor: Implementer.** Non-merge exact-five candidate-only commit; schema-aligned candidate `6604b7a41a679d6c85fc90bcc5d4ca6ab621e3c7`.
- [x] **Actor: Independent Plan-Reviewer.** Write standard three-key candidate-SHA-bound approved receipt.
- [x] **Actor: Implementer.** Approved receipt unchanged sole evidence-only commit `854878afd7dd0ea1ba8866c07a616bdeac7a5785`.
- [x] **Actor: Implementer.** Test-only immutable RED subject `d84ea7b410ff4811806bdeebba568c5ee88fc399` covering all declared cases, including bounded scene assertions.
- [x] **Actor: Tester.** Write subject-SHA-bound factual failing six-key evidence after actual collect/failure checks.
- [x] **Actor: Implementer.** RED Tester evidence unchanged sole commit `d68196a308b2f2fd333f0838cdb29fe8ce7a260e`; no RED approval.
- [x] **Actor: Implementer.** Distinct bounded three-path green subject `4448c9d144db74787f8c1947b51064e291552a6a`; paired aliases/defaults/arguments and truthful Miss endpoint.
- [x] **Actor: Tester.** Actual scoped pytest/regressions, JS syntax, scene/inline agreement, endpoint and diff-bound checks;
  write only `plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<c31-green-subject-40-hex-sha>.json`.
- [x] **Actor: Implementer.** Passing Tester evidence unchanged sole commit `7787c8b8edb760df6f81f44182bb146f8730c69d`.
- [x] **Actor: Independent Reviewer.** Consume committed passing same-subject evidence; write only
  `plan/loaded-runtime-cache/loaded-runtime-cache.implementation-review-log-<c31-green-subject-40-hex-sha>.json`.
- [x] **Actor: Implementer.** Approved review evidence unchanged separate sole commit `b75242afc8fcf211c4b0e1aebe20fc410f567d6f`.
- [x] **Actor: Planner / Plan-Creator.** Phase 4.5 factual plan/step alignment after committed approved review.
- [x] **Actor: Implementer / Planner.** Tracking commit `851dedef3aa4e0f1bdfdb34ed39f2c6518fd8892`, bounded push, live audit。
- [x] **Actor: Independent Reviewer.** Write immutable eight-key exact-five-pair classification only at
  `plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-<c31-green-subject-40-hex-sha>-<actual-current-pr-head-40-hex-sha>.json`.
- [x] **Actor: Implementer.** Classification unchanged sole commit `9bdea139d9c3d79a8ae413333c9e15e877c42a30`。
- [x] **Actor: Planner / Implementer.** Route each committed REPLY_AND_RESOLVE entry; leave exact factual reply and resolve
  only that pair. ADDRESS returns bounded repair; HUMAN_CHECK stays open. Push/audit actual actions.

`nYQqw`/`4140648790` unclassified/open; five Human-only pairs `jnBpk`/`4043480108`, `kQ95O`/`4060023123`,
`kqiZ5`/`4070096561`, `lAR8T`/`4078761998`, `lfQmF`/`4091213944` excluded/open. Other paths, dev worktree and
predecessor evidence ReadOnly; Deleted none. No PR approval/Human merge/release/post-merge. Invalid scope/evidence fails closed.

## C32 Current-Head Three-Pair Classification Successor（completed predecessor routing）

C31 已完成 committed S `4448c9d144db74787f8c1947b51064e291552a6a`、
passing T `7787c8b8edb760df6f81f44182bb146f8730c69d`、
approved V `b75242afc8fcf211c4b0e1aebe20fc410f567d6f`；C31 classification sole commit／audited PR head
`9bdea139d9c3d79a8ae413333c9e15e877c42a30`。C31 五個已回覆且 resolved 的事實：
`m-94K`→`4141037841`、`nXkrM`→`4141038098`、`nXrA0`→`4141038268`、
`nXzEu`→`4141038483`、`nXzE1`→`4141038696`。

C32 exact pairs 僅 `nYQqw`/`4140648790`、`nZI5l`/`4141010658`、
`nZI5n`/`4141010661`。Committed candidate `42ec2293d306546df06529996bc63adb058b3eee`、
approved receipt commit `6a3271af13443c1b794c28038a68d4c158163071`、classification sole commit
`83ffddf831da3f4ecb26656a96bc6aeb28ef98d5` 為 completed predecessor facts。
`nYQqw` 已回覆 `4141149003` 並 resolved；另外兩 pairs 為 ADDRESS，後续權限僅見 C33。
五個 Human-only pairs `jnBpk`/`4043480108`、`kQ95O`/`4060023123`、
`kqiZ5`/`4070096561`、`lAR8T`/`4078761998`、`lfQmF`/`4091213944` 排除/open。
舊 rejected receipt `loaded-runtime-cache.plan-review-receipt-a46241e4245957cd820eae13fd2bf22ab0a9226d.json`
是 frozen nonrouting provenance，不能覆寫、提交作本輪 approval 或重新使用。
### Goal／Scope／Boundaries／Acceptance

Goal／In-Scope：僅依 C31 verified facts 分類三個新 pairs，再執行 individually authorized exact actions。
Modify：Plan-Creator 僅上述五份 planning artifacts。Written：獨立 Plan-Reviewer standard receipt 與
Independent Reviewer fixed classification receipt；只有 Implementer 可原樣分別 sole-commit。
ReadOnly：dev worktree、predecessor evidence、其他 paths／threads、Human-only locks。
Deleted：無。Out-Of-Scope／Non-Goal：新 implementation、RED/green、source/tests/diagram/runtime/API、
architecture/ACL/backend/DI/lifecycle 決策、README/VERSION、PR approval／Human merge／release／post-merge。
TestCase：full SHA/committed evidence/live head/exact pair/schema/writer/order/sole commit/immutability checks；
invalid evidence fails closed。No stable-library surface or release changes。原 mission、scope、outcomes、
Runtime Registry protocol、測試策略、Architecture Visualization 與 follow-up missions 全部保留。

Historical state：`c32-completed`。Schema/path authority：technical-spec C32。

- [x] **Actor: Plan-Creator.** C32 五份標準 planning artifacts draft、C31 completed factual alignment。
- [x] **Actor: Implementer.** Exact-five non-merge planning candidate-only commit。
- [x] **Actor: Independent Plan-Reviewer.** Candidate-SHA-bound standard approved receipt。
- [x] **Actor: Implementer.** Approved receipt unchanged separate sole evidence-only commit。
- [x] **Actor: Planner.** Verify fixed committed C31 S/T/V and actual live fixed PR head。
- [x] **Actor: Independent Reviewer.** Exact immutable eight-key three-pair classification receipt per technical-spec C32。
- [x] **Actor: Implementer.** Classification unchanged separate sole evidence-only commit；bounded push。
- [x] **Actor: Planner / Implementer.** Route exact committed REPLY_AND_RESOLVE entry；nYQqw reply 4141149003／resolved。
- [x] **Actor: Planner.** ADDRESS qualified getattr to C33；starred argument and Human-only five human-check/open。

## C33 Qualified Builtins getattr Repair Successor（completed predecessor routing）

C32 classification 已由 committed receipt 將 `nZI5l`/`4141010658` 分為 ADDRESS；
`nYQqw`/`4140648790` 已回覆 `4141149003` 並 resolved。C32 為 completed predecessor routing。
C33 僅修正 `nZI5l`/`4141010658`；`nZI5n`/`4141010661` 的 starred argument
問題留在 human-check/open，與五個既有 Human-only pairs `jnBpk`/`4043480108`、
`kQ95O`/`4060023123`、`kqiZ5`/`4070096561`、`lAR8T`/`4078761998`、
`lfQmF`/`4091213944` 一律排除。舊 rejected receipt
`plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-a46241e4245957cd820eae13fd2bf22ab0a9226d.json`
保持 frozen nonrouting provenance；不可覆寫或作 approval。

### Goal / Outcome / Scope

Goal／In-Scope：既有 static BC-independence scanner 識別 known builtins module 的 qualified
`getattr` 與其 module alias，在既有 forbidden attribute lookup 範圍內拒絕 direct invocation
及 assignment-retained callable bypass。Historical state：`c33-completed`。
Modify：Plan-Creator 僅五份標準 planning artifacts；Implementer RED 與 green 均僅
`tests/test_loaded_runtime_cache_bc_independence.py`。Written：獨立 Plan-Reviewer／Tester／
Independent Reviewer evidence at C33 immutable SHA-bound paths below，僅 Implementer 原樣 sole-commit。
ReadOnly：dev worktree、所有 predecessor evidence、source、architecture／visualization、其他 paths／threads。
Deleted：無。Out-Of-Scope／Non-Goal：starred arguments／任意 iterable inference、general callable inference、
source/import execution、新 architecture／ACL／mapper／wiring／backend／DI／lifecycle、production API、
README／VERSION、PR approval／merge／release／post-merge。無 stable-library surface 或 release change。
TestCase：qualified direct／module-alias／assignment callable regressions、bare getattr preservation、
benign len／unknown-receiver controls、exact path／writer／schema／SHA／sole evidence ordering。

### Locked Decisions / Boundaries

Execution authority 是 technical-spec 本 C33 section。維持既有 bare `getattr` 行為；
額外只接受 `ast.Attribute` callee，其 attribute 是 `getattr`、receiver 是 simple-name 且
existing module alias map 明確解析為 `builtins`。例如 `builtins.getattr`、
`bi.getattr`（`import builtins as bi`）與既有 alias map 已知的 module assignment alias。
不將未知 receiver 或任意同名方法視為 builtins。延續 exactly two positional arguments、
no keyword arguments、simple-name module target、literal string attribute 與既有 forbidden set：
`builtins.__import__`、`importlib.import_module`、`sys.modules`。不增加第三/default argument、
star／iterable expansion、general-purpose interpretation、callable getattr alias inference 或動態 execution。
維持 existing direct imports、fixtures、mocks、assertions 與所有先前 scanner regressions。
原 mission、scope、outcomes、Runtime Registry reuse protocol、測試策略、Architecture Visualization
與 follow-up missions 不變。

### Artifact Paths / Implementation Steps / Allowed Transitions

Plan-Creator 在 feature worktree 只修改：
`analysis/loaded-runtime-cache/requirements.md`、
`analysis/loaded-runtime-cache/technical-spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.plan.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.step.md`。
Implementer 獨立 non-merge exact-five candidate-only commit 後，Independent Plan-Reviewer 唯一寫
`plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<c33-candidate-40-hex-sha>.json`。
Exact keys：`verdict`、`blocking_issues`、`copilot_feedback_triage`。
Verdict `approved|needs-rework`；blockers 是 exact `issue`／`file`／`fix` nonempty string objects
array，approved 空、needs-rework 非空；triage exact `ADDRESS`／`DISCUSS`／`SKIP` arrays。
Implementer 原樣 separate sole evidence-only commit approved receipt；Planner 才可 route RED。

Implementer only test-file non-merge RED subject → Tester actual collection-success／declared-behavior failure →
failing evidence → Implementer unchanged sole evidence-only commit → distinct test-file-only green subject →
Tester actual scoped pytest and existing runtime contract regressions → passing evidence → Implementer unchanged
sole evidence-only commit → Independent Reviewer same-subject review → Implementer unchanged sole approved
review commit → Planner Phase 4.5 → Plan-Creator factual plan／step alignment → Implementer separate tracking
commit／bounded push → actual PR-head audit → Independent Reviewer single-pair classification → Implementer
sole receipt commit／bounded push → Planner exact action route → Implementer factual reply／resolve／live audit。
creator-in-progress → tester-in-progress → review-ready → reviewer-in-progress → approved or needs-rework；
approved → publish-in-progress → pr-open。Needs-rework 必須新的 green subject 與完整 Tester／Reviewer chain。
Planning approval 不授權 thread actions。Human alone PR approval／merge／release／post-merge。

Tester 唯一寫
`plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<c33-red-subject-40-hex-sha>.json` 或
`plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<c33-green-subject-40-hex-sha>.json`，
對應各自實際 immutable subject。Exact six keys `schema_version`、`topic`、
`implementation_subject_commit`、`status`、`commands`、`recorded_by`：
integer `1`、string `loaded-runtime-cache`、actual full lowercase 40-hex SHA、
`passing|failing`、nonempty array of exact `command` nonempty string／`exit_code` integer objects、`Tester`。
passing 要求全部實際 exit codes 為 0；failing 至少一個 nonzero，RED 需確認為新增指定行為失敗，
不可用 syntax／dependency／無關 failure 代替。Tester 不 commit；Implementer 原樣分別 sole-commit。

Independent Reviewer 只消費 committed passing same-green-subject Tester evidence，唯一寫
`plan/loaded-runtime-cache/loaded-runtime-cache.implementation-review-log-<c33-green-subject-40-hex-sha>.json`。
Exact seven keys `schema_version` integer `1`、`topic` string `loaded-runtime-cache`、
`implementation_subject_commit` same actual full green SHA、`tester_evidence_commit` actual full sole passing
Tester commit SHA、`verdict` `approved|needs-rework`、`blocking_issues` string array
(approved 空／needs-rework 非空)、`recorded_by` string `Independent Reviewer`。
Reviewer 不 commit；Implementer 原樣 separate sole evidence-only commit。

### Validation / Acceptance / Current-Head Classification

RED covers qualified known builtins direct calls、imported module alias、module-assignment alias、retrieved callable
assignment，目標覆蓋既有 forbidden set；benign `len` 與 unknown receiver 不誤判。
Green scoped independence pytest 與既有 loaded-runtime-cache contract regressions passing，確認 bare getattr、
原 tests direct-import behavior、one-file subject bounds。Evidence 必須實際 command facts；不預填任何 future
candidate／subject／commit／verdict／result／PR head／reply／resolution。

已提交 approved review 與 Phase 4.5／push／actual-head audit 後 Independent Reviewer 唯一可寫：
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-<c33-green-subject-40-hex-sha>-<actual-current-pr-head-40-hex-sha>.json`。
Exact eight top-level keys `schema_version`、`topic`、`implementation_subject_commit`、
`tester_evidence_commit`、`implementation_review_evidence_commit`、`pr_head_commit`、
`classifications`、`recorded_by`。Values integer `1`、string `loaded-runtime-cache`、
actual full lowercase 40-hex S／sole passing T commit／sole approved V commit／audited PR head、
exact one-entry array、`Independent Reviewer`。Entry exact `thread`、`comment`、
`outcome`、`reply`；string IDs `nZI5l`／`4141010658`；
outcome `REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK`，只有 REPLY_AND_RESOLVE reply 為 nonempty factual
string，其餘為 JSON null。Implementer 原樣 separate sole evidence-only commit，Planner 方可 route
exact committed REPLY_AND_RESOLVE entry 的指定 reply／resolve；ADDRESS 要 bounded repair，
HUMAN_CHECK 保持 open。所有 receipts immutable；wrong/stale head、binding、path、key、writer、SHA、
pair、enum、nullability、order、non-sole commit 或 overwritten evidence fail closed。

### Reviewer Handoff / Post-merge / Unresolved Items

```json
{"verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]}}
```

No release／post-merge actions。C33 qualified known-builtins getattr implementation 與獨立 verification 已提交：
candidate `05a37198c667a845f3370c4d25b859337edf6548`；
approved Plan-Reviewer receipt commit `d9092bedad9794f968b69dbbfe6412c11bdc0cbf`；
RED subject `3e1b05f72508f856e68ba61bd9669496309d811a`；
failing Tester evidence commit `21185456b8d6afed0832fc6c78dd547dad1e9f72`；
green subject `82e3dc7efa04d7a432568e254ffca82bc3337ecd`；
passing Tester evidence commit `eff8eb2f5f554d6eb01f57fcf5755cddcab4adfe`；
approved Independent Reviewer evidence commit `d29da7b8a855b3887c9bcbb7183b1db0cd744043`。
Planner 已 route Phase 4.5；本次 Plan-Creator factual plan／step alignment 完成。
Separate tracking commit `be7f374efdda4eb8ce4fe945108ab8399a903a13`、bounded push／actual PR-head audit、single-pair classification
與 sole commit `e17956b4d83ba81129cc7787d145436e7f73fd95`／push 已完成；
`nZI5l` 已留 reply `4141461698` 並 resolved。
starred `nZI5n` 與上述 Human-only five 留在 human-check/open，unlisted threads 不可回覆／resolve。

### C33 Step Tracker

- [x] **Actor: Plan-Creator.** Five-file C33 bounded draft and C32 resolved factual alignment。
- [x] **Actor: Implementer.** Exact-five non-merge candidate-only commit。
- [x] **Actor: Independent Plan-Reviewer.** Write candidate-SHA-bound standard receipt。
- [x] **Actor: Implementer.** Approved receipt unchanged sole evidence-only commit。
- [x] **Actor: Implementer.** Test-file-only RED subject。
- [x] **Actor: Tester.** Collection／declared assertion failure factual RED evidence。
- [x] **Actor: Implementer.** Failing Tester evidence unchanged sole commit。
- [x] **Actor: Implementer.** Distinct test-file-only green subject。
- [x] **Actor: Tester.** Scoped tests／preservation／bounds factual passing evidence。
- [x] **Actor: Implementer.** Passing Tester evidence unchanged sole commit。
- [x] **Actor: Independent Reviewer.** Same-subject committed passing evidence review。
- [x] **Actor: Implementer.** Approved review unchanged sole commit。
- [x] **Actor: Planner / Plan-Creator.** Phase 4.5 factual plan／step alignment。
- [x] **Actor: Implementer.** Separate tracking commit／bounded push。
- [x] **Actor: Planner.** Actual PR head／mergeability／threads audit。
- [x] **Actor: Independent Reviewer.** Immutable actual-head-bound single-pair classification。
- [x] **Actor: Implementer.** Classification unchanged sole commit／bounded push。
- [x] **Actor: Planner / Implementer.** Route exact permitted reply／resolve and verify live state。

## C34 Current-Head Three-Pair Classification Successor（completed predecessor routing）

### Goal / Outcome / Scope

Historical state：`c34-completed`。Goal／In-Scope：僅獨立分類三個新 pairs
`nZm9b`/`4141203131`、`nZm9d`/`4141203134`、`nZm9h`/`4141203139`；
不預填分類結果、reply 或 resolution。本輪固定使用同 topic committed C33
S `82e3dc7efa04d7a432568e254ffca82bc3337ecd`、
passing T commit `eff8eb2f5f554d6eb01f57fcf5755cddcab4adfe`、
approved V commit `d29da7b8a855b3887c9bcbb7183b1db0cd744043`，
與 audited PR head `e17956b4d83ba81129cc7787d145436e7f73fd95`。

C33 已提交 verification chain；其 classification sole commit 為
`e17956b4d83ba81129cc7787d145436e7f73fd95`；`nZI5l`/`4141010658`
已留 reply `4141461698` 並 resolved。C32 committed candidate
`42ec2293d306546df06529996bc63adb058b3eee`、approved receipt commit
`6a3271af13443c1b794c28038a68d4c158163071`、classification sole commit
`83ffddf831da3f4ecb26656a96bc6aeb28ef98d5` 為 completed predecessor facts；
`nYQqw` 已留 reply `4141149003` 並 resolved。C32／C33 皆為 completed
predecessor routing，本 C34 section 取代其未完成 tracking 敘述作 current routing。

### Locked Decisions / Boundaries / Exclusions

六個 Human-only pairs `jnBpk`/`4043480108`、`kQ95O`/`4060023123`、
`kqiZ5`/`4070096561`、`lAR8T`/`4078761998`、
`lfQmF`/`4091213944`、starred-argument `nZI5n`/`4141010661`
均排除，保持 human-check/open。舊 rejected receipt
`loaded-runtime-cache.plan-review-receipt-a46241e4245957cd820eae13fd2bf22ab0a9226d.json`
是 frozen nonrouting provenance，不覆寫、不提交為本輪 approval、不重新使用。

Modify：Plan-Creator 僅五份 standard planning artifacts。Written：獨立
Plan-Reviewer candidate-bound receipt 與 Independent Reviewer fixed classification receipt。
Deleted：無。ReadOnly：dev worktree、既有 source/tests/diagram、predecessor evidence、
所有未列 pairs 與六個 Human locks。Out-Of-Scope／Non-Goal：新 implementation、
RED/green、runtime/API/backend/DI/lifecycle、architecture/ACL 決策、README/VERSION、
PR approval／Human merge／release／post-merge。原 mission、scope、outcomes、
Runtime Registry protocol、測試策略、Architecture Visualization、follow-up missions
全部維持；無 stable-library surface 或 release 變更。

### Status / Allowed Transitions / Artifact Paths / Implementation Steps

Plan-Creator 僅於 feature worktree 修改：
`analysis/loaded-runtime-cache/requirements.md`、
`analysis/loaded-runtime-cache/technical-spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.plan.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.step.md`。
Implementer 建立 exact-five non-merge candidate-only commit；Independent Plan-Reviewer
只審該 committed candidate，唯一寫
`plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<c34-candidate-40-hex-sha>.json`。
單一 JSON object exact keys `verdict`、`blocking_issues`、`copilot_feedback_triage`；
verdict `approved|needs-rework`；blockers 為 exact `issue`／`file`／`fix`
nonempty string objects array，approved 空、needs-rework 非空；triage 為 exact
`ADDRESS`／`DISCUSS`／`SKIP` arrays。Implementer 原樣 separate sole
evidence-only commit approved receipt。未 approved 不可分類。

Planner 核對 committed fixed S/T/V 與 live fixed PR head 後，Independent Reviewer
唯一可寫 immutable path：
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-82e3dc7efa04d7a432568e254ffca82bc3337ecd-e17956b4d83ba81129cc7787d145436e7f73fd95.json`。

JSON object top-level keys 恰為 `schema_version`、`topic`、
`implementation_subject_commit`、`tester_evidence_commit`、
`implementation_review_evidence_commit`、`pr_head_commit`、
`classifications`、`recorded_by`。Values 分別是 integer `1`、
string `loaded-runtime-cache`、上述固定 S/T/V/head 完整 lowercase 40-hex SHA、
exact three-entry array、string `Independent Reviewer`。
Each entry exact keys `thread`、`comment`、`outcome`、`reply`；
thread/comment 是上述三個 exact pairs 的 string IDs，每 pair 恰一次。
Outcome enum `REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK`；只有
REPLY_AND_RESOLVE reply 是 nonempty factual string，其餘 reply 必為 JSON null。
Reviewer 不 commit；Implementer 原樣 separate sole evidence-only commit classification，
再 bounded push。Planning commits 保持 local 到分類完成，不先改變 fixed live PR head。

Planner 才可依 committed classification route exact REPLY_AND_RESOLVE entry；
Implementer 留該指定 factual reply 並 resolve exact thread，之後 live audit。
ADDRESS 回 bounded repair route；HUMAN_CHECK 保持 open。Planning approval 不授權
reply/resolve。Sequence：candidate → independent approved planning receipt →
sole receipt commit → fixed-triple/live-head verification → independent classification →
sole classification commit → bounded push → exact per-pair actions → human-check。
publish-in-progress 只可進 pr-open；Human alone PR approval／merge／release／post-merge。

### Validation / Acceptance / TestCase

Verify committed same-topic S/T/V、passing Tester／approved Reviewer、full SHA、live head、
exact paths/pairs/key sets/schema/writers/enum/nullability/ordering/sole commits/immutability。
Wrong/stale head、wrong binding、extra/missing key/pair、wrong writer、overwrite、非 sole commit、
跳過 actor order 或跨 topic evidence 一律 fail closed。No new implementation or RED/green；
不預填 future candidate SHA、verdict、classification outcome、reply 或 resolution。

### Reviewer Handoff / Post-merge / Unresolved Items

```json
{"verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]}}
```

本輪三個 pairs 尚待獨立分類。六個 Human-only pairs 保持 open；
unlisted threads 不可回覆／resolve。No release／post-merge actions。

### C34 Step Tracker

- [x] **Actor: Plan-Creator.** Five-artifact bounded classification draft／C32-C33 factual alignment。
- [x] **Actor: Implementer.** Exact-five non-merge candidate-only commit。
- [x] **Actor: Independent Plan-Reviewer.** Candidate-SHA-bound standard receipt。
- [x] **Actor: Implementer.** Approved receipt unchanged sole evidence-only commit。
- [x] **Actor: Planner.** Committed fixed S/T/V／live fixed PR-head verification。
- [x] **Actor: Independent Reviewer.** Immutable exact-three-pair classification receipt。
- [x] **Actor: Implementer.** Classification unchanged sole evidence-only commit／bounded push。
- [x] **Actor: Planner / Implementer.** Route exact permitted actions／reply／resolve／live audit。

## C35 Current-Head Five-Pair Classification Successor（needs-rework predecessor routing）

### Goal / Outcome / Scope

Historical state：`c35-classification-needs-rework`。Goal／In-Scope：僅獨立分類五個新 pairs
`naZCW`/`4141524912`、`naZCY`/`4141524919`、`na5mB`/`4141737461`、
`na5mE`/`4141737466`、`na5mM`/`4141737476`；
不預填分類結果、reply 或 resolution。本輪固定使用同 topic committed C33
S `82e3dc7efa04d7a432568e254ffca82bc3337ecd`、
passing T commit `eff8eb2f5f554d6eb01f57fcf5755cddcab4adfe`、
approved V commit `d29da7b8a855b3887c9bcbb7183b1db0cd744043`，
與 audited PR head `71545af8c0d6f87ea4f43bf28d380edfed75aa82`。

C33 已提交 verification chain；其 classification sole commit 為
`e17956b4d83ba81129cc7787d145436e7f73fd95`；`nZI5l`/`4141010658`
已留 reply `4141461698` 並 resolved。C32 committed candidate
`42ec2293d306546df06529996bc63adb058b3eee`、approved receipt commit
`6a3271af13443c1b794c28038a68d4c158163071`、classification sole commit
`83ffddf831da3f4ecb26656a96bc6aeb28ef98d5` 為 completed predecessor facts；
`nYQqw` 已留 reply `4141149003` 並 resolved。C32／C33 皆為 completed
predecessor routing。C34 candidate `8ef5a690669b654a16343c091ccb7617eeb04011`、
approved planning receipt commit `2ecd41b08fe91d875b3607bda45f52b1386eff85`、
classification sole commit `71545af8c0d6f87ea4f43bf28d380edfed75aa82` 已提交。
`nZm9b`/`4141203131` 已留 reply `4141853147` 並 resolved；
`nZm9d`/`4141203134`、`nZm9h`/`4141203139` 為 ADDRESS，尚未修復，
本輪不授權其 implementation 或 resolution。C34 是 completed predecessor routing。
既有 For lock 保留，不新增 For handling、alias inference 或相關 implementation。
本 C35 section 取代其未完成 tracking 敘述作 current routing。

### Locked Decisions / Boundaries / Exclusions

六個 Human-only pairs `jnBpk`/`4043480108`、`kQ95O`/`4060023123`、
`kqiZ5`/`4070096561`、`lAR8T`/`4078761998`、
`lfQmF`/`4091213944`、starred-argument `nZI5n`/`4141010661`
均排除，保持 human-check/open。舊 rejected receipt
`loaded-runtime-cache.plan-review-receipt-a46241e4245957cd820eae13fd2bf22ab0a9226d.json`
是 frozen nonrouting provenance，不覆寫、不提交為本輪 approval、不重新使用。

Modify：Plan-Creator 僅五份 standard planning artifacts。Written：獨立
Plan-Reviewer candidate-bound receipt 與 Independent Reviewer fixed classification receipt。
Deleted：無。ReadOnly：dev worktree、既有 source/tests/diagram、predecessor evidence、
所有未列 pairs 與六個 Human locks。Out-Of-Scope／Non-Goal：新 implementation、
RED/green、runtime/API/backend/DI/lifecycle、architecture/ACL 決策、README/VERSION、
PR approval／Human merge／release／post-merge。原 mission、scope、outcomes、
Runtime Registry protocol、測試策略、Architecture Visualization、follow-up missions
全部維持；無 stable-library surface 或 release 變更。

### Status / Allowed Transitions / Artifact Paths / Implementation Steps

Plan-Creator 僅於 feature worktree 修改：
`analysis/loaded-runtime-cache/requirements.md`、
`analysis/loaded-runtime-cache/technical-spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.plan.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.step.md`。
Implementer 建立 exact-five non-merge candidate-only commit；Independent Plan-Reviewer
只審該 committed candidate，唯一寫
`plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<c35-candidate-40-hex-sha>.json`。
單一 JSON object exact keys `verdict`、`blocking_issues`、`copilot_feedback_triage`；
verdict `approved|needs-rework`；blockers 為 exact `issue`／`file`／`fix`
nonempty string objects array，approved 空、needs-rework 非空；triage 為 exact
`ADDRESS`／`DISCUSS`／`SKIP` arrays。Implementer 原樣 separate sole
evidence-only commit approved receipt。未 approved 不可分類。

Planner 核對 committed fixed S/T/V 與 live fixed PR head 後，Independent Reviewer
唯一可寫 immutable path：
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-82e3dc7efa04d7a432568e254ffca82bc3337ecd-71545af8c0d6f87ea4f43bf28d380edfed75aa82.json`。

JSON object top-level keys 恰為 `schema_version`、`topic`、
`implementation_subject_commit`、`tester_evidence_commit`、
`implementation_review_evidence_commit`、`pr_head_commit`、
`classifications`、`recorded_by`。Values 分別是 integer `1`、
string `loaded-runtime-cache`、上述固定 S/T/V/head 完整 lowercase 40-hex SHA、
exact five-entry array、string `Independent Reviewer`。
Each entry exact keys `thread`、`comment`、`outcome`、`reply`；
thread/comment 是上述五個 exact pairs 的 string IDs，每 pair 恰一次。
Outcome enum `REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK`；只有
REPLY_AND_RESOLVE reply 是 nonempty factual string，其餘 reply 必為 JSON null。
Reviewer 不 commit；Implementer 原樣 separate sole evidence-only commit classification，
再 bounded push。Planning commits 保持 local 到分類完成，不先改變 fixed live PR head。

Planner 才可依 committed classification route exact REPLY_AND_RESOLVE entry；
Implementer 留該指定 factual reply 並 resolve exact thread，之後 live audit。
ADDRESS 回 bounded repair route；HUMAN_CHECK 保持 open。Planning approval 不授權
reply/resolve。Sequence：candidate → independent approved planning receipt →
sole receipt commit → fixed-triple/live-head verification → independent classification →
sole classification commit → bounded push → exact per-pair actions → human-check。
publish-in-progress 只可進 pr-open；Human alone PR approval／merge／release／post-merge。

### Validation / Acceptance / TestCase

Verify committed same-topic S/T/V、passing Tester／approved Reviewer、full SHA、live head、
exact paths/pairs/key sets/schema/writers/enum/nullability/ordering/sole commits/immutability。
Wrong/stale head、wrong binding、extra/missing key/pair、wrong writer、overwrite、非 sole commit、
跳過 actor order 或跨 topic evidence 一律 fail closed。No new implementation or RED/green；
不預填 future candidate SHA、verdict、classification outcome、reply 或 resolution。

### Reviewer Handoff / Post-merge / Unresolved Items

```json
{"verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]}}
```

本輪五個 pairs 尚待獨立分類。六個 Human-only pairs 保持 open；
unlisted threads 不可回覆／resolve。No release／post-merge actions。

### C35 Step Tracker

- [x] **Actor: Plan-Creator.** Five-artifact bounded classification draft／C34 factual alignment。
- [ ] **Actor: Implementer.** Exact-five non-merge candidate-only commit。
- [ ] **Actor: Independent Plan-Reviewer.** Candidate-SHA-bound standard receipt。
- [ ] **Actor: Implementer.** Approved receipt unchanged sole evidence-only commit。
- [ ] **Actor: Planner.** Committed fixed S/T/V／live fixed PR-head verification。
- [ ] **Actor: Independent Reviewer.** Immutable exact-five-pair classification receipt。
- [ ] **Actor: Implementer.** Classification unchanged sole evidence-only commit／bounded push。
- [ ] **Actor: Planner / Implementer.** Route exact permitted actions／reply／resolve／live audit。

## C36 Replacement Five-Pair Classification Successor（completed predecessor routing）

### Goal / Outcome / Scope / Locked Decisions

Historical state：`c36-completed`。僅為 C35 needs-rework 建立新的獨立 classification
receipt，不作 implementation。C35 candidate `0e9c84959ec602dbc117413613ce6afd371b6822`
與 approved planning receipt commit `53b19a478f23a31de6183510cc6569901f9f66f9`
是已提交事實；其未提交 classification receipt 使用 full PRRT thread IDs，
不符合 suffix ID contract，屬 rejected nonrouting provenance。原 path
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-82e3dc7efa04d7a432568e254ffca82bc3337ecd-71545af8c0d6f87ea4f43bf28d380edfed75aa82.json`
保留原樣，不覆寫、不提交作有效 evidence、不重用其 outcomes。

本輪 exact pairs 僅 `naZCW`/`4141524912`、`naZCY`/`4141524919`、
`na5mB`/`4141737461`、`na5mE`/`4141737466`、`na5mM`/`4141737476`。
thread 欄位必為這五個 suffix IDs，不是 full PRRT node IDs；comment 為上述 string IDs。
固定 S `82e3dc7efa04d7a432568e254ffca82bc3337ecd`、
passing T commit `eff8eb2f5f554d6eb01f57fcf5755cddcab4adfe`、
approved V commit `d29da7b8a855b3887c9bcbb7183b1db0cd744043`、
live audited head `71545af8c0d6f87ea4f43bf28d380edfed75aa82`。
不得预填新 candidate SHA、verdict、outcomes、replies 或 resolutions。

### Boundaries / Exclusions

In-Scope／Goal：replacement receipt contract 與 independent five-pair classification。
Modify：Plan-Creator 僅以下五個 artifacts。Written：獨立 review／classification receipts。
ReadOnly：dev、source/tests/diagram/governance、舊 receipts、unlisted pairs。Deleted：無。
Out-Of-Scope／Non-Goal：implementation、RED/green、新 architecture/runtime/API/ACL/backend/DI/lifecycle
決策、README/VERSION、PR approval／merge／release／post-merge。
六 Human-only pairs `jnBpk`/`4043480108`、`kQ95O`/`4060023123`、
`kqiZ5`/`4070096561`、`lAR8T`/`4078761998`、
`lfQmF`/`4091213944`、`nZI5n`/`4141010661` 保持 excluded/open。
`nZm9d`/`4141203134` 與 `nZm9h`/`4141203139` ADDRESS 尚未修復，
既有 For boundary/lock 保持，本輪不授權其修改或 resolve。
原 mission、scope、outcomes、Runtime Registry protocol、測試策略、
Architecture Visualization、follow-up missions 維持，無 stable-library/release 變更。

### Status / Allowed Transitions / Artifact Paths / Implementation Steps

Plan-Creator 僅 feature worktree：
`analysis/loaded-runtime-cache/requirements.md`、
`analysis/loaded-runtime-cache/technical-spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.plan.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.step.md`。
Implementer exact-five non-merge candidate-only commit；Independent Plan-Reviewer 唯一寫
`plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<c36-candidate-40-hex-sha>.json`。
單一 JSON object exact keys `verdict`、`blocking_issues`、`copilot_feedback_triage`；
verdict `approved|needs-rework`，blockers exact `issue`/`file`/`fix` nonempty
string objects array，approved 空、needs-rework 非空；triage exact `ADDRESS`/`DISCUSS`/`SKIP` arrays。
Implementer 原樣 sole evidence-only commit approved receipt；Planner 核對 fixed S/T/V/live head，
Independent Reviewer 才獨立重新分類，唯一寫全新 replacement path：

`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-82e3dc7efa04d7a432568e254ffca82bc3337ecd-71545af8c0d6f87ea4f43bf28d380edfed75aa82-c36-<c36-candidate-40-hex-sha>.json`

Template variable 必為本輪實際 committed exact-five candidate full lowercase 40-hex SHA；
同一值也綁定本輪 Plan-Reviewer receipt filename。Candidate 未提交前不預填。
此 path 不重用 C35 path，writer 寫入前確認從未存在；immutable 禁止覆寫。
Classification JSON top-level exact eight keys `schema_version`、`topic`、
`implementation_subject_commit`、`tester_evidence_commit`、
`implementation_review_evidence_commit`、`pr_head_commit`、
`classifications`、`recorded_by`；values 為 integer `1`、string `loaded-runtime-cache`、
上述 fixed full S/T/V/head、exact five-entry array、string `Independent Reviewer`。
每 entry exact `thread`、`comment`、`outcome`、`reply`，每上述 suffix pair 恰一次。
Outcome enum `REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK`；
僅 REPLY_AND_RESOLVE reply 為 nonempty factual string，其餘 JSON null。
Reviewer 不 commit；Implementer 原樣 separate sole evidence-only commit，bounded push。
Planning commits 留 local 到 fixed live-head classification 完成後才 push。

Sequence：new candidate → independent approved Plan-Reviewer receipt → sole receipt commit →
fixed-triple/live-head verification → independent NEW classification → sole classification commit →
bounded push → Planner exact-action route → Implementer 指定 factual reply/resolve/live audit。
不沿用 rejected outcomes；planning approval 不授權 thread actions。
ADDRESS 回 bounded repair，HUMAN_CHECK 保持 open；只對 committed REPLY_AND_RESOLVE entries 執行。
publish-in-progress 只可進 pr-open；Human alone PR approval／merge／release／post-merge。

### Validation / Acceptance / TestCase / Reviewer Handoff / Unresolved Items

Verify exact five suffix IDs/pairs、same-topic committed S/T/V、passing/approved evidence、
fixed live head、fresh candidate-bound path、schema/writers/enum/nullability/actor order/
sole commits/immutability。Wrong/stale binding、full PRRT IDs、extra/missing pairs/keys、
overwriting/reusing old receipt、prefilled outcomes、非 sole commit 一律 fail closed。
```json
{"verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]}}
```
五 pairs 尚待 new independent classification；六 Human locks 與 For boundary 保持 open。
No release/post-merge actions。

### C36 Step Tracker

- [x] **Actor: Plan-Creator.** Exact-five replacement contract draft。
- [ ] **Actor: Implementer.** Exact-five non-merge candidate-only commit。
- [ ] **Actor: Independent Plan-Reviewer.** New candidate-bound receipt。
- [ ] **Actor: Implementer.** Approved receipt unchanged sole commit。
- [ ] **Actor: Planner.** Fixed S/T/V/live-head verification。
- [ ] **Actor: Independent Reviewer.** New immutable candidate-bound exact-five classification。
- [ ] **Actor: Implementer.** Classification unchanged sole commit／bounded push。
- [ ] **Actor: Planner / Implementer.** Exact permitted actions／live audit。

## C37 Static BC Independence Scanner Repair（authoritative current routing）

### C37 Risks / Rollback

Risks：recursive semantic-target traversal 可能誤擴張 existing alias inference；
必須只檢查 target-side tuple/list/starred 的 local semantic names，不配對或讀取 RHS，
attribute targets 維持 non-local。直接 imported builtins getattr 可能誤判任意同名 callable；
僅接受 known-builtins import local/asname 與既有 exact-two-positional/no-keyword/
known-module/literal-attribute bounds。NamedExpr 新 semantic check 可能遮蔽既有 detectors；
保留其 regression assertions，並以 benign/attribute/non-builtins controls 排除 false positives。
Scoped tests、Ruff、strict Pyright 與 independent review 驗證上述風險。

Rollback：僅對本輪五份 planning artifacts 的尚未核准差異作 bounded planning repair，
或对 `tests/test_loaded_runtime_cache_bc_independence.py` 的本輪 immutable test subject
作新的 bounded repair commit；不得 broad reset、改 frozen C14 scope 或覆寫舊 evidence。
Implementation needs-rework／回修須建立新的 immutable subject，重新執行 Tester →
passing evidence sole commit → Independent Reviewer → review sole commit，再走後續 alignment/
classification route。已提交或 rejected receipts 原樣保留 nonrouting provenance，包括
本輪先前 needs-rework Plan-Reviewer receipt；六 Human locks／For boundary 保持。


### C37 Executable Validation Commands / Configuration

RED 新增 tests function names 必含 `c37`，指定 forbidden/foreign regressions 另含
`rejects`；benign/attribute/non-builtins controls 不含 rejects，確保 collection/control/failure
selection 可直接驗證且 nonempty。這是既有三項 bounded fixtures 的命名，不新增行為。
Tester 在各自 immutable subject 實際執行並記錄：
- RED collection：`uv run --frozen pytest -p no:tach tests/test_loaded_runtime_cache_bc_independence.py -k c37 --collect-only -q`，
  必須成功並確認三項 declared regression/control coverage。
- RED benign controls：`uv run --frozen pytest -p no:tach tests/test_loaded_runtime_cache_bc_independence.py -k 'c37 and not rejects' -q`，
  必須 passing，不能以 unrelated failure 充作 RED。
- RED declared behavior failure：`uv run --frozen pytest -p no:tach tests/test_loaded_runtime_cache_bc_independence.py -k c37 -q`，
  必須 actual assertion failure，對應新增 foreign-target／walrus／imported-getattr behavior。
- Green complete scanner/runtime regressions：
  `uv run --frozen pytest -p no:tach tests/test_loaded_runtime_cache_bc_independence.py tests/test_loaded_runtime_cache_contracts.py -q`。
- Scoped Ruff：
  `uv run --frozen ruff check tests/test_loaded_runtime_cache_bc_independence.py tests/test_loaded_runtime_cache_contracts.py`。
- Scoped strict Pyright：
  `uv run --frozen pyright tests/test_loaded_runtime_cache_bc_independence.py tests/test_loaded_runtime_cache_contracts.py`。

`-p no:tach` 明確停用 tach selection/filter，確保列出的 tests 真正執行；
沿 C33 committed passing Tester evidence 的相同 green invocation。
Config authority：`pyproject.toml` 的 `[tool.pyright]`（Python 3.12、strict、
extraPaths src）、`[tool.pytest.ini_options]`（strict config/markers 與既有 coverage）、
`[tool.ruff]`／`[tool.ruff.lint]`（py312、line-length 100、ALL）、
`[tool.ruff.lint.per-file-ignores]`（test S101）。不改 config。
Commands 是待執行 contract，不是預填結果；所有 passing evidence 需上述實際 exit code 0，
RED failing evidence 需 actual declared assertion nonzero。


### Python implementation metadata（canonical python-implementation-plan profile）

- Async-planning status：exempt — 本輪僅同步 static AST test analysis，沒有 async boundary、
  external I/O、resource lifecycle、concurrency、timeout/retry/cancellation 或 runtime ownership。
- Module/package placement：僅 `tests/test_loaded_runtime_cache_bc_independence.py`。
- New public API：no，既有 direct-module API 不變。
- Interface changes：no，既有 Protocol signatures 不變。
- Breaking changes allowed：no，保留既有 direct imports/fixtures/mocks/assertions。
- New dependencies：no，僅既有 standard-library ast 與 pytest tooling。
- Error-handling strategy：scanner 的 factual assertion failures 交 Tester；不改 production exceptions。
- Typing strategy：保留現有 Python 3.12 test typing；不用 Any/cast/dynamic import/runtime introspection。
- Non-goals：不做 RHS destructuring/alias/iterable inference；不擴張 For/star-call handling；
  不修改 production source/API；不建立 backend/DI/lifecycle；不更改 architecture 或 Human locks。
- Test categories：happy path（指定 foreign semantic target／forbidden getter 被發現）；
  edge cases（nested tuple/list/starred targets、import asname、direct walrus）；
  failure paths（RED declared assertion failures，排除 collection/dependency errors）；
  forbidden behaviors（不執行 source、不讀 RHS 推論、不把 attributes/unknown getter 視為 local imports）；
  regression preservation（direct imports/fixtures/mocks/assertions、bare/qualified getter、
  no-star alias behavior、既有 scanner/runtime contract tests）。


### Goal / Outcome / Scope / Locked Decisions

Current：`c37-planning-draft`。本輪同 static BC independence scanner mission，
僅修正三個 ADDRESS pairs：`nZm9h`/`4141203139`、
`naZCY`/`4141524919`、`na5mM`/`4141737476`。
C36 candidate `8a35890310d788d7834be035e891bb0b53baa96d`、
approved planning receipt commit `55a65a036b20ad566d8a9a9fa410f33f5393fc2c`、
classification sole commit `8306cf004eb86ac26da016a009d73da0582bc0be`
均已提交。已 reply/resolved：`naZCW`→`4142061895`、
`na5mB`→`4142062611`、`na5mE`→`4142063556`。
C36 completed predecessor routing，本 C37 取代其 current routing。

### Boundaries / In-Scope / Out-Of-Scope / Goal / Non-Goal

Implementation sole path：`tests/test_loaded_runtime_cache_bc_independence.py`。
1. Assignment-target semantic-name checks recursively inspect only syntactic
   `ast.Tuple`/`ast.List` elements and `ast.Starred.value`, including nested targets；
   each `ast.Name` target applies the existing opposite-BC semantic-name rule。
   Attribute targets 不算 local names；不讀 RHS 配對、不推論 aliases/iterables/values。
   既有 alias inference 與其 direct-name/no-star 行為維持，不因本 semantic-name check 擴張。
2. `ast.NamedExpr` 的 direct-name target 套用既有 foreign semantic-name detector；
   不移除或改寫其他已宣告 detectors，不以 RHS 推論 semantic identity。
3. 直接 `from builtins import getattr`（含 `asname`）所建立的 local callable
   可用於既有 literal attribute check。限定 import 的 known-builtins module，
   callee 為該 local simple-name，exact two positional args、no keywords，
   first arg simple-name module 且 existing map 已知、second arg literal string。
   forbidden set 維持 `builtins.__import__`、`importlib.import_module`、
   `sys.modules`。不推論任意 getter assignment/callable alias，不展開 star/iterable；
   bare/qualified known-builtins getattr 既有行為維持。

ReadOnly：dev、source/docs/governance/diagram、舊 evidence、其他 threads。
Modify：五個 planning artifacts；RED/green 僅上述 test path。Written：各 actor 的
SHA-bound immutable evidence。Deleted：無。Out-Of-Scope／Non-Goal：source/API/runtime/
registry/backend/DI/lifecycle、new architecture/ACL、README/VERSION、PR approval/merge/release/post-merge。
六 Human-only pairs `jnBpk`/`4043480108`、`kQ95O`/`4060023123`、
`kqiZ5`/`4070096561`、`lAR8T`/`4078761998`、
`lfQmF`/`4091213944`、`nZI5n`/`4141010661` 保持 excluded/open。
`nZm9d`/`4141203134` For boundary/lock 保留，不授權 repair/resolve。
兩份既有 untracked rejected receipts 保留原樣 nonrouting provenance，不覆寫、不提交。
原 mission/scope/outcomes/Runtime Registry protocol/測試策略/Architecture Visualization/
follow-up missions 維持；無 stable-library/release changes。

### Artifact Paths / Status / Allowed Transitions / Implementation Steps

Plan-Creator 只在 feature worktree 修改五個 exact artifacts：
`analysis/loaded-runtime-cache/requirements.md`、
`analysis/loaded-runtime-cache/technical-spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.plan.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.spec.md`、
`plan/loaded-runtime-cache/loaded-runtime-cache.step.md`。
Implementer exact-five non-merge candidate-only commit；Independent Plan-Reviewer 唯一寫
`plan/loaded-runtime-cache/loaded-runtime-cache.plan-review-receipt-<c37-candidate-40-hex-sha>.json`。
Single JSON exact keys `verdict`、`blocking_issues`、`copilot_feedback_triage`；
verdict approved|needs-rework，blockers exact issue/file/fix nonempty string objects array
(approved 空／needs-rework 非空)，triage exact ADDRESS/DISCUSS/SKIP arrays。
Implementer 原樣 separate sole evidence-only commit approved receipt，Planner 才 route RED。

Implementer sole-test-path RED subject（只加 isolated regression fixtures/assertions，未修 detector）→
Tester actual collection-success and declared-behavior failure evidence → Implementer sole evidence commit →
distinct sole-test-path green subject → Tester scoped scanner and existing runtime contract regression evidence →
Implementer sole passing evidence commit → Independent Reviewer same-subject committed passing-evidence review →
Implementer sole approved review commit → Planner Phase 4.5 → Plan-Creator factual plan/step alignment →
Implementer separate alignment commit/push → actual PR-head audit → Independent Reviewer new three-pair
classification → Implementer sole classification commit/push → Planner exact actions →
Implementer factual replies/resolutions/live audit。
creator-in-progress → tester-in-progress → review-ready → reviewer-in-progress → approved|needs-rework；
needs-rework 要新 subject 與完整 Tester/Reviewer chain；
approved → publish-in-progress → pr-open。Human alone approval/merge/release/post-merge。

Tester 唯一寫
`plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<c37-red-subject-40-hex-sha>.json`
或 `plan/loaded-runtime-cache/loaded-runtime-cache.tester-evidence-<c37-green-subject-40-hex-sha>.json`。
Exact six keys schema_version/topic/implementation_subject_commit/status/commands/recorded_by；
integer 1、string loaded-runtime-cache、actual subject full lowercase 40-hex SHA、
passing|failing、nonempty array of exact command(nonempty string)/exit_code(integer) objects、
string Tester。Passing 要所有 actual exit codes 0；failing 至少一個 nonzero，
RED 須新增 declared assertion failure，不可 syntax/dependency/無關 failure。
Tester 不 commit；Implementer 原樣各自 separate sole evidence-only commit。

Independent Reviewer 只消費 committed passing same-green-subject evidence，唯一寫
`plan/loaded-runtime-cache/loaded-runtime-cache.implementation-review-log-<c37-green-subject-40-hex-sha>.json`。
Exact seven keys schema_version/topic/implementation_subject_commit/tester_evidence_commit/
verdict/blocking_issues/recorded_by：integer 1、loaded-runtime-cache、same actual full green SHA、
actual full sole passing T commit SHA、approved|needs-rework、string array
(approved 空／needs-rework 非空)、Independent Reviewer。
Reviewer 不 commit；Implementer 原樣 separate sole evidence-only commit。

### Validation / Acceptance / TestCase

RED fixtures 以 original comment examples 的 isolated source strings 作靜態 AST assertions，
不 exec fixture source。兩 BC foreign/benign names、tuple/list/nested/starred targets、
attribute-only controls；walrus foreign/benign controls；
direct imported/asname getattr 對 __import__/import_module/sys.modules forbidden controls，
benign attributes/non-builtins imports controls。保留 existing direct imports、fixtures/mocks/assertions、
bare/qualified getattr、no-star iterable alias behavior 與其他 regressions。
Green 須 actual scoped independence pytest 與 existing loaded-runtime-cache contract regressions passing；
Reviewer 驗證只改 sole test path、semantic-target recursion 與 alias inference 分離、
walrus detectors preservation、getter import bounds，無動態執行。

### Current-Head Classification / Reviewer Handoff / Unresolved Items

Full chain committed/pushed 且 audit 後 Independent Reviewer 唯一寫
`plan/loaded-runtime-cache/loaded-runtime-cache.thread-classification-receipt-<c37-green-subject-40-hex-sha>-<actual-current-pr-head-40-hex-sha>.json`。
Exact eight keys schema_version/topic/implementation_subject_commit/tester_evidence_commit/
implementation_review_evidence_commit/pr_head_commit/classifications/recorded_by；
integer 1、loaded-runtime-cache、actual full same S/sole passing T/sole approved V/audited head SHA、
exact three-entry array、Independent Reviewer。Each entry exact thread/comment/outcome/reply；
上述 three pairs 各一次，thread 必為 suffix IDs、comment string IDs，
outcome REPLY_AND_RESOLVE|ADDRESS|HUMAN_CHECK；僅 REPLY_AND_RESOLVE reply nonempty factual string，
其餘 JSON null。Reviewer 不 commit；Implementer 原樣 separate sole evidence-only commit。
Planner 才可 route exact REPLY_AND_RESOLVE replies/resolutions；ADDRESS 回 bounded repair，
HUMAN_CHECK 保持 open。Planning approval 不授權 thread actions。
All paths immutable/fresh；wrong/stale SHA/head/binding/schema/pair/writer/order/non-sole commit
或 overwritten receipt fail closed。禁止預填 future SHA/verdict/result/classification/reply/resolution。

```json
{"verdict":"approved|needs-rework","blocking_issues":[],"copilot_feedback_triage":{"ADDRESS":[],"DISCUSS":[],"SKIP":[]}}
```
三 pairs 待 bounded repair/verification；六 Human-only 與 For lock 保持 open。
No release/post-merge actions。

### C37 Step Tracker

- [x] **Actor: Plan-Creator.** Five-artifact bounded three-pair repair draft／C36 facts。
- [ ] **Actor: Implementer.** Exact-five candidate-only commit。
- [ ] **Actor: Independent Plan-Reviewer.** New candidate-bound receipt。
- [ ] **Actor: Implementer.** Approved planning receipt sole commit。
- [ ] **Actor: Implementer.** Sole-test-path RED subject。
- [ ] **Actor: Tester.** Actual declared RED failure evidence。
- [ ] **Actor: Implementer.** Failing evidence sole commit。
- [ ] **Actor: Implementer.** Distinct sole-test-path green subject。
- [ ] **Actor: Tester.** Actual scoped passing evidence。
- [ ] **Actor: Implementer.** Passing evidence sole commit。
- [ ] **Actor: Independent Reviewer.** Same-subject review evidence。
- [ ] **Actor: Implementer.** Approved review sole commit。
- [ ] **Actor: Planner / Plan-Creator.** Phase 4.5 factual alignment。
- [ ] **Actor: Implementer.** Separate alignment commit／push。
- [ ] **Actor: Planner / Independent Reviewer.** Actual-head audit／new exact-three classification。
- [ ] **Actor: Implementer.** Classification sole commit／push。
- [ ] **Actor: Planner / Implementer.** Exact permitted actions／live audit。
