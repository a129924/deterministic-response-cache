---
name: agent-skill-template
description: Provide the canonical structure for a review-ready, portable, single-purpose Agent Skill in this repository, including complexity-gated sections and risk-based validation guidance. Use this when asked for the standard shape of a new skill or when building a new skill manually from a template.

complexity: low

use_when:
  - a new skill needs a clean starting point
  - you want the canonical section layout for SKILL.md

do_not_use_when:
  - the task is to review a finished skill
  - the task only needs a small edit to an existing skill
---

# Purpose
Provide the reference shape for a `review-ready` skill at the canonical
authoring target while keeping output-facing path wording aligned.

# Trigger / When to use
Use this skill when:
- a new skill needs a clean starting point
- you want the canonical section layout for `SKILL.md`
- you need the minimum companion files for a stable skill

Do not use this skill when:
- the task is to review a finished skill
- the task only needs a small edit to an existing skill

# Inputs
- the skill name
- the single responsibility
- the trigger situations
- any truly local assets
- the expected risk, branching, or external-tool profile if it is already known

# Process
1. Read `template.md` and `folder-contract.md`.
2. Classify the expected validation weight and `complexity` before copying the skeleton: lightweight (low), medium-complexity (medium), or higher-risk (high).
3. Identify applicable `risk_profile` tags for medium and high complexity skills.
4. Copy the folder shape and section layout for
   `.<platform>/skills/<skill-name>/`, while authoring the canonical source
   under `skills/<skill-name>/`.
5. Replace placeholders with one clear responsibility.
6. Add concise positive and negative examples to `SKILL.md`.
7. Add `reference.md` or `examples.md`.
8. Use `references/` only as a split-reference supplement, not as a replacement for the required companion-file rule.
9. Split oversized reference material into `references/` when one `reference.md` would exceed about 1,000 tokens or more than 3 logical topics.
10. If `reference.md` is the chosen companion file and becomes too broad, keep it focused or reduce it to a short overview while moving detailed topics into `references/`.
11. Add `examples.md` when the skill is high complexity or the concise examples are not enough for about 80% of routine usage.
12. Add stronger validation signals only when the skill's risk, branching, tooling, or downstream impact justifies them.
13. If you add optional files or folders, declare each role in `Local references`.
14. If the projected entrypoint does not yet exist, mention
    `skills/<skill-name>/` only as an explicitly labeled bootstrap fallback.
15. If truthful guidance would require hardcoding `.codex/...`, `.github/...`,
    or another concrete platform root, roll back to alignment wording instead
    of choosing a default platform.
16. If downstream planning-spine skills or other consumers still assume a
    platform-specific `.<platform>/skills/` surface, record that as a
    follow-up implication instead of editing those surfaces in this phase.
17. Stop at `review-ready`.
18. Let a human or external workflow pass the draft to `agent-skill-reviewer`.

# Examples
- Positive: Use this template to draft a focused skill with concise positive and negative examples in `SKILL.md`, then add stronger verification guidance only when the topic is higher-risk.
- Negative: Use this template as if it could approve a finished skill or as if every simple skill needed the same heavyweight validation as a release gate.

# Outputs
- a copyable projected skill folder shape at `.<platform>/skills/<skill-name>/`
- canonical source guidance for `skills/<skill-name>/`
- a `SKILL.md` skeleton
- a minimal companion file set
- a `review-ready` draft target

# Boundaries
- Do not use this as a broad catch-all skill.
- Do not remove the explicit trigger section.
- Do not depend on repository-global reference files when a local file will do.
- Do not force heavyweight validation onto a lightweight skill without a clear risk-based reason.
- Do not use `skills/<skill-name>/` as the default runnable or copy-pasteable
  path.
- Do not treat any `.<platform>/skills/` compatibility/projection, promotion,
  or runtime/tooling cutover as part of this template.
- Do not hardcode `.codex/...`, `.github/...`, or another concrete platform
  root unless context explicitly injects it.
- Do not claim `approved` or `stable`.

# Local references
- `template.md`: copyable folder and section skeleton
- `folder-contract.md`: required core and optional role rules
- `reference.md`: lifecycle, split signals, promotion rules, example depth rules, and risk-based validation guidance
