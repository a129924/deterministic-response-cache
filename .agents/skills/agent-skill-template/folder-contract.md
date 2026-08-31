# Skill folder contract

This document defines the folder contract for canonical source authoring,
output-facing projection wording, and bootstrap fallback.

## Path-role taxonomy

- canonical source / authoring-only: `skills/<skill-name>/`
- output-facing / runnable / copy-pasteable: `.<platform>/skills/<skill-name>/`
- bootstrap fallback: `skills/<skill-name>/` only when the projected entrypoint
  does not yet exist and the text labels it as fallback

Do not hardcode `.codex/...`, `.github/...`, or another concrete platform root
as the default. If a concrete platform root is required to keep the contract
truthful, roll back to alignment wording instead of choosing a platform here.

## Required core
- `SKILL.md`: the executable instruction contract for the skill
- `reference.md` or `examples.md`: local detail, examples, or edge cases needed
  to use the skill well

## Optional additions
- `checklist.md`: repeatable verification or operation steps
- scripts: local automation used by this skill
- `references/`: split topic-specific reference files when one `reference.md`
  would become too broad
- local subfolders such as `assets/`: fixtures, templates, or resources used only
  by this skill

## Responsibility matrix
- `SKILL.md`: executable instruction contract with concise positive and negative examples
- `reference.md`: stable local knowledge, constraints, and edge cases
- `references/`: topic-specific reference files with one clear role per file
- `examples.md`: detailed inputs, outputs, anti-patterns, and usage patterns
- `checklist.md`: repeatable verification steps
- scripts: one explicit local automation job
- `assets/`, `templates/`, `fixtures/`: local-only supporting resources with a
  fixed role

## Example policy
- `SKILL.md` must contain one concise correct example and one concise incorrect example
- `examples.md` may stay optional when the concise `SKILL.md` examples already cover about 80% of routine usage
- `examples.md` is required for:
  - code refactoring
  - branching or multi-path decisions
  - script or external-tool usage
  - higher-risk outputs
- reviewer may still require `examples.md` when the concise examples are not enough

## Risk-based validation
- validation weight should match the skill's risk, branching, external-tool usage,
  and downstream impact
- lightweight skills may stay concise when trigger, boundaries, and brief examples
  already prevent routine misuse
- medium-complexity skills should make the main decision path explicit and may add
  brief verification guidance when needed
- higher-risk or gatekeeping skills should include stronger validation signals or
  equivalent local guidance, such as explicit verification guidance, red flags,
  rationalizations, or a checklist
- stronger validation may live in `SKILL.md` or in local companion files, but the
  reviewer must be able to see that misuse prevention is intentional and sufficient
- do not force heavyweight validation onto simple low-risk skills without a clear
  reason

## Reference policy
- keep `reference.md` focused when one file is enough
- `references/` is a split-reference supplement, not by itself a replacement for
  the required companion-file rule
- split into `references/` when `reference.md` grows beyond about 1,000 tokens
  or more than 3 logical topics
- if `reference.md` is the chosen companion file and becomes too broad, keep it
  focused or reduce it to a short overview while moving detailed topics into
  `references/`
- list each split file in `Local references` and state its role

## Role declaration rule
- every optional file or folder must have one clear job
- list local files and folders in `Local references`
- state what each local file or folder is for
- reviewer should reject optional additions with no declared role
- avoid vague catch-all names such as `docs/`, `misc/`, or `helpers/`

## Lifecycle note
- creator stops at `review-ready`
- reviewer returns `approved` or `needs-rework`

## Transition boundary

- scaffold new or materially transitioned canonical source content under
  `skills/<skill-name>/`
- use `.<platform>/skills/<skill-name>/` as the default output-facing,
  runnable, or copy-pasteable path
- use `skills/<skill-name>/` as a projected path only when the projected
  entrypoint does not yet exist and the text explicitly labels it as a
  bootstrap fallback
- do not treat this contract as authorization to rewrite compatibility,
  projection, or platform-consumption surfaces
- do not rewrite runtime/tooling, installer, or projection surfaces here
- if downstream planning-spine skills still assume a `.<platform>/skills/`
  surface, record a follow-up implication instead of editing those skills in
  this phase

## YAML Metadata Policy

Only `name` and `description` are treated as portable runtime discovery fields.

The following fields are repository governance metadata:
- `inputs`
- `outputs`
- `use_when`
- `do_not_use_when`
- `complexity`
- `risk_profile`

These fields are authoritative only for repository consistency review, not for
platform-level routing behavior. The Markdown body remains the authoritative
execution contract. YAML and body must not contradict each other; contradiction
between YAML and body is a reject signal.

## Complexity Policy

`complexity` determines which body sections are required.

complexity: low
- Validation: optional
- Failure Handling: optional
- Workflow State Contract: not required

complexity: medium
- Validation: recommended; required when ambiguity would materially change output
- Failure Handling: required when ambiguity would materially change output
- Workflow State Contract: optional

complexity: high
- Validation: required
- Failure Handling: required
- Workflow State Contract: recommended when participating in multi-agent handoff

## Risk Profile Policy

`risk_profile` is repository governance metadata used to help the creator and
reviewer classify skill risk.

Allowed values:
- `ambiguity_sensitive`: use when missing or ambiguous input may change the
  output meaningfully
- `multi_agent_handoff`: use when the skill output is consumed by another agent,
  workflow step, or resume engine
- `destructive_action`: use when the skill may delete, overwrite, migrate, or
  irreversibly change files, data, or configuration
- `external_tooling`: use when the skill calls CLI tools, APIs, networked
  services, package managers, or other external systems
- `code_modification`: use when the skill directly edits source code, tests,
  configuration, or generated artifacts

Rules:
- `risk_profile` may be empty for low-complexity documentation-only skills
- any skill with `multi_agent_handoff`, `destructive_action`, or
  `code_modification` should be at least `medium` complexity
- any skill with both `code_modification` and `external_tooling` should usually
  be `high` complexity
- reviewer may escalate complexity when risk tags understate actual behavior

## Validation Policy

Validation must define both recoverable and non-recoverable outcomes.

Use `SOFT FAIL` for recoverable quality gaps:
- mark status as INCOMPLETE
- continue with best-effort output
- list missing information or limitations explicitly

Use `BLOCKED` only when proceeding would materially change the output or create
misleading results.

Do not use hard `FAIL -> stop` unless the skill cannot safely produce any useful
output.

A missing input or ambiguity is considered to "materially change output" if a
reasonable alternative interpretation would change any of the following:
- selected workflow path
- target files or artifacts
- approval or rejection verdict
- implementation order
- risk classification
- generated code behavior
- whether the result is safe to use downstream

## Legacy Skill Policy

Existing skills without `complexity` are classified as `unclassified` and must
not be automatically rejected.

Classification is required when:
- the skill is materially edited
- the skill causes workflow ambiguity
- the skill is used in a multi-agent handoff workflow

Do not reject a legacy skill solely for missing `complexity`, `risk_profile`, or
the governance body sections.

## Governance Decision Record

### Decision 1 — YAML metadata is governance metadata, not guaranteed runtime routing

Only `name` and `description` are treated as portable skill discovery fields.
Additional fields such as `inputs`, `outputs`, `use_when`, `do_not_use_when`,
`complexity`, and `risk_profile` are repository governance metadata.

### Decision 2 — Body is the execution contract

The Markdown body remains authoritative for actual skill behavior. YAML must
summarize the body and must not contradict it.

### Decision 3 — Validation must be recoverable

Validation should define PASS, SOFT FAIL, and BLOCKED conditions. Avoid hard
`FAIL -> stop` except when no safe output can be produced.

### Decision 4 — Complexity is proposed by creator and verified by reviewer

Creator proposes `complexity`; reviewer may escalate it based on workflow risk.
Existing skills without complexity are treated as `unclassified`, not
automatically invalid.

### Decision 5 — Migration is phased

This change applies immediately to creator, reviewer, and template. Existing
skills are migrated by priority and are not rejected solely for missing new
metadata.

### Decision 6 — Risk profile is a review aid, not platform behavior

`risk_profile` is used to guide creator and reviewer judgment. It does not imply
that Copilot or another agent runtime will parse or enforce these values. Risk
tags must not contradict the Markdown body.
