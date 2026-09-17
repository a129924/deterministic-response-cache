---
topic: canonical-identity-pipeline
correction_id: canonical-identity-pipeline/pr-comment-review-and-fix-p8-p10-route-recovery
phase: complete-immutable-provenance
created: 2026-09-17
---

# PRCF1 P8–P10 route-recovery tracking

## Current status

P3 `b8c7cc6050b3c5a44333a1fde9d3ee07145966f5`, P5
`dff14f3fdc0a06bf907ea82074e02862a05a36d1`, and P7
`24ef18b835b7646e05bf0fc3f5828349eea52b1` are the completed immutable same-subject PRCF1
chain. P7 phase-repair candidate `87eb3de65d6b5a4efaef745d23e5d6cc34c70c59` / receipt
`40824056def6c9d3402e95039af6a931b67ee547`, and P7 receipt-status-sync candidate
`8ac6bd76ff85d04c16407518105dc023180871ef` / receipt
`49c0bcd197c6b9ac4fb1baba115c903060ff52cf`, are completed frozen facts.

`18d9b4751df26376c9cf47fe7968130870f07fe7` is a structurally correct historical classification
payload and superseded immutable nonrouting provenance. It is not P8 or P10 evidence and cannot
route reply/resolution work. Recovery receipt `b903cb06c2e174501228aab1325179fc1e13bc08`, P8,
and fresh P9/P10 commit `8a86e88621e00bbc10e773411cb10c6272b6fc45` are complete immutable facts.

## Fixed route

- [X] **P3/P5/P7:** The immutable same-subject evidence chain is complete and must remain exact.
- [X] **P7 receipt status sync:** Candidate `8ac6bd76ff85d04c16407518105dc023180871ef` and the
  approved one-path receipt commit `49c0bcd197c6b9ac4fb1baba115c903060ff52cf` are completed
  frozen facts.
- [X] **Historical 18d:** `18d9b4751df26376c9cf47fe7968130870f07fe7` is superseded immutable
  nonrouting provenance.
- [X] **Recovery review / receipt:** Approved receipt `b903cb06c2e174501228aab1325179fc1e13bc08`
  is complete immutable provenance.
- [X] **P8:** Planner completed Phase 4.5 after that receipt.
- [X] **Fresh P9/P10:** Fresh classification was committed unchanged as sole P10 evidence at
  `8a86e88621e00bbc10e773411cb10c6272b6fc45`.
- [ ] **P11:** Pending; no reply or resolution is asserted or performed here.

## Stop conditions

This record cannot select or self-close the recovery candidate, create/reuse a receipt, infer P8,
write classification, infer P10, mark 18d superseded early, change `uv.lock`, or act on PR #6 or
its threads. A dirty candidate/evidence tree, parent other than 18d, merge parent, unlisted path,
missing P3/P5/P7 or 49c facts, or candidate/evidence conflict fails closed and returns to Planner;
worktree or thread conflict is `human-check`.
