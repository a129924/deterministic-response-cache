# Canonical skill template

Use this as the default output-facing starting point for a `review-ready`
skill.

```text
.<platform>/skills/<skill-name>/
├── SKILL.md
├── reference.md            # required unless examples.md already covers local detail
├── references/             # optional, for split topic-specific reference files
├── examples.md             # required for high-complexity or clearly higher-risk skills
├── checklist.md            # optional, useful for repeatable higher-risk validation
├── run-task.sh            # optional
└── assets/                # optional
```

- Use `reference.md` or `examples.md` as the required companion file.
- Use `references/` only as a split-reference supplement, not as a replacement
  for the required companion file.
- Add `references/` when one `reference.md` would exceed about 1,000 tokens or
  more than 3 logical topics.
- Add `examples.md` when the skill is high complexity or the `SKILL.md`
  examples are not enough.
- Add stronger validation guidance only when the skill's risk warrants it.

## Path-role rule

- Author canonical source content under `skills/<skill-name>/`.
- Use `.<platform>/skills/<skill-name>/` as the default runnable,
  copy-pasteable, and output-facing path form.
- If the projected entrypoint does not yet exist, you may mention
  `skills/<skill-name>/` only as an explicitly labeled bootstrap fallback.
- Do not hardcode `.codex/...`, `.github/...`, or another concrete platform
  root unless context explicitly injects it.
- Do not interpret this template as projection promotion, cutover, or runtime
  path design.

## `SKILL.md` skeleton

```md
---
name: <skill-name>
description: <what the skill does and when to use it>
complexity: low | medium | high

risk_profile:
  - ambiguity_sensitive       # missing/ambiguous input may change output meaningfully
  - multi_agent_handoff       # output consumed by another agent or workflow step
  - destructive_action        # may delete, overwrite, migrate, or irreversibly change
  - external_tooling          # calls CLI tools, APIs, networked services, package managers
  - code_modification         # directly edits source code, tests, configuration, or artifacts

inputs:
  - <input-1>

outputs:
  - <artifact-1>

use_when:
  - <trigger scenario>

do_not_use_when:
  - <exclusion scenario>
---

# Purpose
<one clear job>

# Trigger / When to use
Use this skill when:
- ...

Do not use this skill when:
- ...

# Inputs
- ...

# Process
1. ...
2. ...
3. ...

# Examples
- Positive: ...
- Negative: ...

# Outputs
- ...

# Validation
<!-- Required for complexity: high. Required for complexity: medium when ambiguity
     would materially change output. -->

## Required Checks
- <hard condition that must be true>

## Quality Checks (best effort)
- <soft condition — improves output but not blocking>

## On Soft Fail
- mark status as INCOMPLETE
- continue with best-effort output
- list missing information explicitly

## On Blocked
- mark status as BLOCKED
- stop when proceeding would materially change the output or create misleading results
- state exactly what blocker prevents safe completion

# Failure Handling
<!-- Required for complexity: high. Required for complexity: medium when ambiguity
     would materially change output. -->

## Missing Context
- mark output as INCOMPLETE
- list required additional inputs explicitly

## Ambiguous Requirement
- if blocking: stop and ask the user before proceeding
- if non-blocking: proceed with stated assumptions, list them explicitly

## Execution Limitation
- state the limitation explicitly in output
- do not fabricate data to fill gaps

# Workflow State Contract (Optional)
<!-- Recommended for complexity: high when participating in multi-agent handoff. -->

When participating in multi-agent workflows, include:
- current_step: <step name from Process>
- next_step: <next step or DONE>
- status: IN_PROGRESS | COMPLETE | INCOMPLETE | BLOCKED

Omit this section if the skill is not part of a multi-agent handoff workflow.

# Verification
- ...                       <!-- optional for higher-risk or easier-to-misuse skills -->

# Red Flags
- ...                       <!-- optional for higher-risk skills -->

# Common Rationalizations
- ...                       <!-- optional for higher-risk skills -->

# Boundaries
- ...

# Local references
- `reference.md`: local examples, constraints, or edge cases
- `references/topic-a.md`: split reference file with one clear topic and role
- `checklist.md`: repeatable verification steps (optional)
- `assets/`: local-only material used by this skill (optional)
```

## Companion file guidance
- Use `reference.md` or `examples.md` for reusable detail.
- Split oversized reference material into `references/` when one file becomes too broad.
- If `reference.md` is the chosen companion file and becomes too broad, keep it
  focused or reduce it to a short overview while moving detailed topics into
  `references/`.
- Add `checklist.md` only when the skill has repeatable review steps.
- Keep scripts local to the skill that needs them.
- Optional files or folders must declare their role in `Local references`.
- Add `examples.md` when the skill is high complexity or when the concise
  examples in `SKILL.md` are not enough.
- Add `Validation` for medium complexity skills when ambiguity would materially
  change output; require it for high complexity skills.
- Add `Failure Handling` when ambiguity would materially change output.
- Add `Workflow State Contract` only when the skill joins multi-agent handoff.
- Use `SOFT FAIL` for recoverable gaps and `BLOCKED` only when proceeding would
  materially change the output or create misleading results, instead of hard
  `FAIL -> stop`.
- Add stronger validation signals only when risk, branching, tooling, or
  downstream impact justify them.
- If truthful guidance would require a concrete platform root, roll back to
  alignment wording instead of choosing a default platform here.
