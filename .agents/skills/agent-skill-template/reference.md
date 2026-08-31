# Template reference

A stable skill in this repository usually has:
- one trigger family
- one responsibility
- one primary output pattern
- concise positive and negative examples in `SKILL.md`
- local example or reference material
- no hidden dependency on other skill folders
- clear roles for any optional files or folders

## Example depth rule

- simple skills may rely on concise `SKILL.md` examples when they already cover
  about 80% of routine usage
- higher-complexity skills should include `examples.md`
- reviewer may still require `examples.md` when the brief examples are not enough

## Risk-based validation rule

- validation weight should match the skill's risk, branching, external-tool usage,
  and downstream impact
- lightweight skills may stay concise when trigger, boundaries, and brief examples
  already prevent routine misuse
- medium-complexity skills may add brief verification guidance when the main
  decision path would otherwise be too easy to misuse
- higher-risk or gatekeeping skills should include stronger validation signals or
  equivalent local guidance, such as explicit verification, red flags,
  rationalizations, or a checklist
- stronger validation is optional-by-need, not mandatory for every skill

## Reference split rule

- keep `reference.md` focused when one file is enough
- treat `references/` as a split-reference supplement, not as a replacement for
  the required companion-file rule
- split into `references/` when local reference detail grows beyond about 1,000
  tokens or more than 3 logical topics
- if `reference.md` is the chosen companion file and becomes too broad, keep it
  focused or reduce it to a short overview while moving detailed topics into
  `references/`
- list each split reference file in `Local references` and state its role

## Split signals

Create a second skill when:
- the trigger list keeps growing
- the outputs differ substantially
- the process branches into unrelated jobs
- the skill starts relying on too many repo-global assumptions

## Promotion rule

Do not treat a new skill as stable until `agent-skill-reviewer` returns
`approved`.

## Path-role rule

- treat `skills/<skill-name>/` as canonical source and authoring-only context
- treat `.<platform>/skills/<skill-name>/` as the default runnable,
  copy-pasteable, and output-facing path form
- treat `skills/<skill-name>/` as a projected path only when the projected
  entrypoint does not yet exist and the text explicitly labels it as a
  bootstrap fallback
- record downstream planning-spine implications as follow-up instead of editing
  those skill folders in the same phase
- if truthful guidance would require hardcoding `.codex/...`, `.github/...`, or
  another concrete platform root, roll back to alignment wording instead of
  choosing a default platform

## Ownership rule

- creator may draft or revise until the skill is `review-ready`
- reviewer may return `approved` or `needs-rework`
- creator may not self-approve
- reviewer may not author the final implementation directly
