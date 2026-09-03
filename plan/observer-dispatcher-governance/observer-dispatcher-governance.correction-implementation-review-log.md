{
  "schema_version": "observer-dispatcher-governance.correction-implementation-review.v1",
  "correction_id": "observer-dispatcher-governance/high",
  "review_kind": "correction-implementation",
  "severity": "high",
  "implementation_subject_sha": "f1a2ae1334b03ea0c5eea7612909ef77c089f38c",
  "reviewed_commit_sha": "uncommitted V1 review artifact; Reviewer is not authorized to create the V1 commit",
  "reviewed_commit_status": "V1 does not yet exist. The verified committed chain is S1=f1a2ae1334b03ea0c5eea7612909ef77c089f38c -> T1=b96c484e78bdc1ea004c7629616f216657e64e07; T1 has S1 as its sole parent and both commits are non-merge.",
  "tester_evidence": {
    "path": "plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-tester-evidence.md",
    "revision": "b96c484e78bdc1ea004c7629616f216657e64e07",
    "implementation_subject_sha": "f1a2ae1334b03ea0c5eea7612909ef77c089f38c",
    "verdict": "passing"
  },
  "reviewed_artifacts": [
    {
      "path": ".agents/skills/plan-creator/SKILL.md",
      "revision": "S1 f1a2ae1334b03ea0c5eea7612909ef77c089f38c; blob 96ebec610c7cbc2156792b38a69baa52a94c7d6b"
    },
    {
      "path": ".agents/skills/plan-creator/checklist.md",
      "revision": "S1 f1a2ae1334b03ea0c5eea7612909ef77c089f38c; blob b5609a7bcb03fb0494e1da46d974f6ce857b8057"
    },
    {
      "path": ".agents/skills/plan-creator/templates/topic-plan-template.md",
      "revision": "S1 f1a2ae1334b03ea0c5eea7612909ef77c089f38c; blob 3a59d986c7e3d3b32ddb34f849adeaf5959df082"
    },
    {
      "path": ".agents/skills/plan-reviewer/SKILL.md",
      "revision": "S1 f1a2ae1334b03ea0c5eea7612909ef77c089f38c; blob 396abee0b1fb074f003b0edd1141a4bca2e84723"
    },
    {
      "path": ".agents/skills/plan-reviewer/checklist.md",
      "revision": "S1 f1a2ae1334b03ea0c5eea7612909ef77c089f38c; blob d3e0e358630812449ecec7e6bb43231e5dcd7ffd"
    },
    {
      "path": ".agents/skills/plan-reviewer/examples.md",
      "revision": "S1 f1a2ae1334b03ea0c5eea7612909ef77c089f38c; blob 08118f6f0aa208423ea3433a60c5893c896da469"
    },
    {
      "path": ".agents/skills/plan-reviewer/reference.md",
      "revision": "S1 f1a2ae1334b03ea0c5eea7612909ef77c089f38c; blob 71948cad32c632d5c27ee291c208403aaa79c134"
    },
    {
      "path": ".agents/skills/python-implementation-workflow/SKILL.md",
      "revision": "S1 f1a2ae1334b03ea0c5eea7612909ef77c089f38c; blob 5c0abef533b9cf84720233b893f20ee234e56cb3"
    },
    {
      "path": ".agents/skills/python-plan-authoring/templates/canonical-python-topic-plan-template.md",
      "revision": "S1 f1a2ae1334b03ea0c5eea7612909ef77c089f38c; blob 1ec4daaa2afda6e8fd9a894d24caa4a6bfd1f092"
    },
    {
      "path": ".codex/agents/implementer.toml",
      "revision": "S1 f1a2ae1334b03ea0c5eea7612909ef77c089f38c; blob fa8d9cc362d281d8a80f9cb0da5e1ef89417cea5"
    },
    {
      "path": ".codex/agents/planner.toml",
      "revision": "S1 f1a2ae1334b03ea0c5eea7612909ef77c089f38c; blob 4e7808f65c568a7bfb2cc39f4dd12b24db480439"
    },
    {
      "path": "AGENTS.md",
      "revision": "S1 f1a2ae1334b03ea0c5eea7612909ef77c089f38c; blob 0e22778eee70833d418dfd681030285328597dfb"
    },
    {
      "path": "GOAL.md",
      "revision": "S1 f1a2ae1334b03ea0c5eea7612909ef77c089f38c; blob 299cc70e319d2fb130987670e94a6687750a6dc4; unchanged from B0 and T1"
    },
    {
      "path": "tests/test_observer_dispatcher_governance_contract.py",
      "revision": "S1 f1a2ae1334b03ea0c5eea7612909ef77c089f38c; blob 52871465b76fb0ba75d13846244b48a87d924d4b"
    }
  ],
  "review_basis": "Independent review of the direct non-merge S1/T1 chain, S1's complete declared 13-path implementation diff, S1 AGENTS.md and GOAL.md blobs, the approved correction plan/spec/step, and T1's exact same-subject passing evidence. T1 records passing targeted governance, tracker, repository pytest, pyright, tach, pre-commit, diff-check, path-count, and non-merge commands.",
  "traceability": [
    {
      "implementation_step": "1. Align exact declared governance, custom-agent, workflow-skill and Python-template surfaces on the expanded correction contract.",
      "status": "done",
      "evidence": "S1 modifies exactly the declared AGENTS.md, two allowed .codex agents, nine declared workflow/template surfaces, and no .github/agents/** path."
    },
    {
      "implementation_step": "2. Add declared governance contract test and preserve existing direct-import behavior.",
      "status": "partial",
      "evidence": "S1 adds tests/test_observer_dispatcher_governance_contract.py and T1 records it passing, but the test has no assertions for frozen normal/recovery provenance, the S1 subject reset, or the exact ordered T1/V1 two-descendant invariant required by the plan/spec."
    },
    {
      "implementation_step": "3. Begin declared implementation only after the approved correction review was committed unchanged as non-subject B0.",
      "status": "done",
      "evidence": "S1's sole parent is B0=8556d41282eb2388ff22e45623dd20052a2bf70f; B0 contains the approved correction-review record and no S1 implementation path is introduced before S1."
    }
  ],
  "contract_check": [
    {
      "item": "S1/T1 immutable-subject chain",
      "status": "matches",
      "detail": "T1=b96c484e78bdc1ea004c7629616f216657e64e07 directly parents S1 and its JSON attests the same full S1 SHA with verdict passing."
    },
    {
      "item": "Declared path boundary and frozen provenance",
      "status": "matches",
      "detail": "S1 changes the 13 declared implementation paths only; AGENTS.md and GOAL.md blobs are pinned above, GOAL.md remains unchanged, and no .github/agents/** path changed."
    },
    {
      "item": "Executable drift detection for all declared correction invariants",
      "status": "deviation",
      "detail": "The added test checks selected wording and artifact names only. It does not fail closed for frozen normal/recovery provenance, S1-only subject reset, or exact T1 then V1 evidence-only descendant topology."
    }
  ],
  "test_plan_check": [
    {
      "case_type": "Declared governance contract test",
      "status": "present-but-incomplete",
      "location": "tests/test_observer_dispatcher_governance_contract.py; T1 b96c484e78bdc1ea004c7629616f216657e64e07 records uv run pytest tests/test_observer_dispatcher_governance_contract.py passing."
    },
    {
      "case_type": "Frozen-provenance exclusion, immutable subject reset, and exact T1/V1 ordering",
      "status": "missing",
      "location": "not found in tests/test_observer_dispatcher_governance_contract.py"
    }
  ],
  "blocking_issues": [
    {
      "issue": "The declared governance contract test does not verify three mandatory drift conditions.",
      "file": "tests/test_observer_dispatcher_governance_contract.py",
      "fix": "Add direct file-content assertions that fail for normal/recovery provenance being current, an implementation descendant being treated as the subject instead of S1, and any topology other than linear evidence-only T1 then V1. A new correction route is required before another implementation subject because this needs-rework verdict invalidates the current chain."
    }
  ],
  "copilot_feedback_triage": {
    "ADDRESS": [],
    "DISCUSS": [],
    "SKIP": []
  },
  "verdict": "needs-rework",
  "timestamp": "2026-09-02T03:41:21Z"
}
