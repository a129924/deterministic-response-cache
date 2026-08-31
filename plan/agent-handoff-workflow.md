# Agent handoff workflow

## Purpose
Define the canonical repo-level workflow for planning, drafting, reviewing,
publishing, and releasing work in this repository when different agents operate
in different contexts.

## Scope
- This document defines the shared process for repo-visible handoff artifacts.
- It is platform-agnostic at the process level.
- It applies to both VS Code and CLI usage.
- It does not replace the shared topic-plan contract in
  `plan/topic-plan-contract.md`.
- It does not replace task-specific skill instructions inside
  `.github/skills/<skill-name>/`.

## Workflow layering
- This document defines the repo-level phase semantics, ownership, stop points,
  and handoff rules.
- `plan/topic-plan-contract.md` defines repo-level topic-plan contract
  semantics, required plan sections, and reviewer handoff shape.
- Topic plans define execution contract for one topic within those repo-level
  governance and workflow constraints.
- Skill-local instructions may define task-specific execution detail, but they
  are consumer guidance only for topic-plan contract questions and must not
  contradict repo-level stop points, ownership, status transitions, or the
  shared topic-plan contract.
- Hidden chat context must never override repo-visible workflow artifacts.

## Core principles
- Planning decisions must be captured in repo-visible files, not left in hidden
  session context.
- Creator and reviewer are separate roles and should not rely on one shared
  conversation state.
- If real role separation cannot be established for a required handoff, stop
  and surface the execution limitation instead of simulating independent
  planner, reviewer, implementer, or final-gate completion.
- Topic execution should start from `plan/<topic>/<topic>.plan.md`.
- Stable-library updates happen only after reviewer approval.
- Topic plans that trigger stable-library or release work must declare when those
  actions occur.
- The workflow should stay reusable and independent of one exact UI or launch
  command.

## State machine rules
- Each workflow state must have a clear entry condition, allowed next status, and
  stop rule.
- If the required entry condition is not met, remain in the current state instead
  of inferring progress.
- STOP POINT 1 is a positive authorization gate:
  - it blocks commit / push / PR creation until explicit human approval exists
  - once approval exists and no blocking conflict remains, execution may continue
    directly
- STOP POINT 2 is a terminal / no-op gate:
  - after merge handoff, the current execution must stop
  - no background polling, implicit wait, or inferred transition is allowed
  - only a new explicit human resume message may re-enter the workflow
- Human confirmation gates are explicit transitions, not implied progress
  markers.

## Source of truth
- `AGENTS.md` is the governance canonical source.
- This file is the authoritative repo-level workflow contract.
- `plan/topic-plan-contract.md` is the shared repo-level topic-plan contract
  surface for required sections, fallback behavior, and contract review basis.
- Repo-visible topic plans are the authoritative execution contract for a
  single topic within those repo-level constraints.
- Skill-local instructions are authoritative only within their own skill
  boundary and do not own repo-level topic-plan contract authority.
- Parent artifacts for a topic remain the current truth:
  - the locked topic plan
  - any topic-owned parent artifacts such as `*.spec.md` that are explicitly
    listed in `Artifact paths`
- When `plan/<topic>/<topic>.step.md` is present, it is a workflow progression
  artifact:
  - it reflects current stage readiness and stage-local next work
  - it does not define topic-close or follow-up handoff truth
- When a required topic-close `summary artifact` is present, it is the current
  truth for close and handoff semantics:
  - it determines whether the topic is fully closed or explicitly closed with
    follow-up
  - it is not replaced by `step.md`, status labels, or hidden chat context
- Correction artifacts are historical truth only:
  - they explain why current truth changed
  - they do not replace the parent contract
- Hidden chat context must never override repo-visible workflow artifacts.
- If repo-level contracts and topic-local truth artifacts conflict in a way
  that changes execution meaning, stop and surface the conflict rather than
  silently choosing whichever artifact is more convenient.

## Roles
| Role | Primary responsibility | Must not do |
| --- | --- | --- |
| Planning actor | Define scope, locked decisions, boundaries, and handoff artifacts | Skip the repo-visible plan file |
| Creator | Draft or revise the implementation from the topic plan until it is `review-ready` | Approve its own output |
| Reviewer | Evaluate the latest creator output and return `approved` or `needs-rework` | Author the final implementation directly |
| Main Agent (publisher / release actor) | Handle commit, push, PR, review-comment triage, merge follow-up, and release/version actions, while stopping for explicit human confirmations where the workflow requires them | Change planning intent retroactively without updating the plan |

Role-separation execution rule:
- A valid multi-role workflow requires a real separated role surface, bounded
  handoff payload, bounded result payload, and distinct task owner.
- If those conditions cannot be established for the required stage, stop and
  report the execution limitation instead of treating one actor as if multiple
  independent gates had already been satisfied.

### Correction routing roles
- Human operator may raise a direction concern or point at drift, but chat alone
  must not override repo-visible source of truth.
- Workflow agent may make provisional routing / severity decisions to prevent
  silent advance, but must not confirm final correction severity or close a
  correction.
- Planner confirms final severity, freezes the correction direction, and closes
  correction only after required reviews pass and parent sync is complete.
- Implementer performs the repair under the frozen direction and must not
  redefine correctness criteria or skip required correction artifacts.

## Canonical artifacts
| Artifact | Path | Purpose |
| --- | --- | --- |
| Repo workflow spec | `plan/agent-handoff-workflow.md` | Shared process contract |
| Shared topic-plan contract | `plan/topic-plan-contract.md` | Repo-level topic-plan authority for required sections, fallback behavior, and contract review basis |
| Topic handoff plan | `plan/<topic>/<topic>.plan.md` | Repo-visible execution contract for one topic |
| Topic progression artifact | `plan/<topic>/<topic>.step.md` when required, or another exact repo-visible progression artifact when explicitly listed | Current-truth workflow progression status for the topic |
| Topic close summary artifact | `plan/<topic>/<topic>.summary.md` or another exact repo-visible close artifact when explicitly listed | Current-truth close outcome and handoff semantics for the topic |
| Parent topic artifacts | `plan/<topic>/<topic>.spec.md` or other topic-owned parent artifacts when explicitly listed | Current-truth execution details for the topic besides progression and close summary artifacts |
| Correction artifacts | `plan/<topic>/<topic>.correction-plan.md` and `plan/<topic>/<topic>.correction-step.md` when explicitly listed | Historical-truth correction trail for planner-confirmed drift |
| Review log / routing handoff | `plan/<topic>/<topic>.review-log.md` or another exact repo-visible path when explicitly listed | Reviewer feedback trail when feedback controls routing or multi-round rework |
| Skill draft | `.github/skills/<skill-name>/` | Creator output under repo policy |
| Stable-library summary | `README.md` | Human-facing stable skill list |
| Repo version baseline | `VERSION` | Canonical SemVer version for the repository |

## Topic plan contract
`plan/topic-plan-contract.md` owns the repo-level topic-plan contract for
required section names, reviewer handoff shape, and topic-plan authority
ordering.

Every topic handoff plan must satisfy that shared contract.

The required section meanings, fallback behavior, and contract-level review
basis are shared in `plan/topic-plan-contract.md`.

Additional contract rules:
- `Artifact paths` is an executable contract, not an informational appendix.
- If a listed artifact path is invalid, contradicts repo policy, or drifts from
  the intended output location, fix the topic plan before continuing execution.
- If a topic uses correction artifacts, each one must be listed explicitly in
  `Artifact paths` with an exact repo-visible path, owner, and role beside the
  parent artifacts they affect; they are never implied by chat history or
  workflow state.
- If reviewer feedback controls routing or multi-round rework, the topic must
  also list an exact repo-visible `review-log` or equivalent handoff artifact.
- Even when correction artifacts exist, parent artifacts remain the current
  truth and the correction files remain historical truth.
- When stable-library or release work applies, the topic plan must declare the
  timing of README / VERSION actions instead of leaving Main Agent to infer it.
- A valid repo-visible topic plan is the execution prerequisite for the rest of
  this workflow; later phases must not infer missing planning intent from chat
  history alone.
- The planning actor may be a human today and may later be a dedicated planning
  tool or skill such as a future `plan-creator`, but the authoring method for
  that planner is outside the scope of this execution workflow.
- If execution reaches Phase 2 or later without a valid topic plan, stop and
  repair the plan instead of improvising downstream git, review, or release
  decisions.

### Conditional workflow artifacts
- `plan/<topic>/<topic>.step.md` is conditionally required when either of these
  is true:
  - the topic requires two or more workflow-role handoffs
  - the topic has `required follow-up`
- Missing required `step.md` blocks workflow progression; do not advance to the
  next workflow role until the artifact exists and is usable as progression
  truth.
- When repo-level `step.md` exists, it must at minimum contain:
  - `Workflow Stages`
  - `Actionable Steps`
  - `Handoff / Gate Notes`
- `step.md` is a progression artifact only; it does not decide topic-close
  meaning.
- A topic-close `summary artifact` is conditionally required when either of
  these is true:
  - the topic closes with a handoff to another agent or human
  - the topic has `required follow-up`
- Missing required `summary artifact` blocks topic close, even if merge, sync,
  or release work is otherwise complete.
- When a required repo-level `summary artifact` exists, it must at minimum
  contain:
  - `current state`
  - `completed`
  - `not completed`
  - `required follow-up`
  - `next handoff`
- The `next handoff` section of a required `summary artifact` must include:
  - `next actor`
  - `next step`
- `required follow-up` allows explicit close with follow-up.
- The required `summary artifact` is the source of truth for close and handoff
  semantics; `step.md` only reflects progression status.

## Correction layer semantics
- Ordinary `needs-rework` stays separate from correction-triggering drift.
- Correction-triggering drift means the issue changes at least one of:
  - source-of-truth semantics
  - public contract meaning
  - architecture boundary
  - phase routing

### Severity classification
| Severity | Meaning | Required artifacts |
| --- | --- | --- |
| `low` | Local repair stays inside existing current truth | note only; no correction artifact required |
| `medium` | Planner-confirmed drift needs a repo-visible correction contract | `*.correction-plan.md`; add `*.correction-step.md` when the repair is multi-step |
| `high` | Planner-confirmed drift invalidates confidence in the current implementation | both correction artifacts are required and the current implementation is treated as suspect code |

### Routing states
| State | Meaning | Routing owner | Required artifacts |
| --- | --- | --- | --- |
| `IMPLEMENT_CONTINUE` | Ordinary `needs-rework` stays in the current execution loop | Implementer / executor | existing parent artifacts; optional note |
| `IMPLEMENT_PATCH` | Planner confirmed `low` severity and allowed a bounded patch inside current truth | Implementer / executor | repo-visible note; no correction artifact |
| `PLANNER_CLARIFY` | Drift was detected but final severity / route is not yet frozen | Planner | repo-visible deviation or equivalent routing note |
| `PLANNER_REPLAN` | Planner confirmed `medium` or `high` severity and froze the correction route | Planner -> Implementer | severity-appropriate correction artifacts |

### Closure and retention rules
- Applicable correction artifacts must be listed explicitly in `Artifact paths`
  beside the parent artifacts they affect.
- If reviewer feedback controls routing or multi-round rework, keep a
  repo-visible `review-log` or equivalent handoff artifact; do not rely on
  hidden chat history.
- Parent artifacts become the execution-facing current truth again only after
  backfill is complete; parent sync is required before correction closure.
- Required downstream reviews must pass before correction closure is accepted.
- Correction artifacts remain historical truth after closure; they may be marked
  `resolved` or `superseded`, but direct deletion is forbidden.
- Open correction work keeps the topic inside its normal execution loop; it does
  not create a new generic human STOP POINT.
- STOP POINT 1 and STOP POINT 2 semantics remain unchanged.

## Status model
| Status | Meaning | Owner | Allowed next |
| --- | --- | --- | --- |
| `planned` | Topic plan is committed and ready for execution | Planning actor / human | `creator-in-progress` |
| `creator-in-progress` | Creator is drafting or revising the work | Creator | `review-ready` |
| `review-ready` | Creator finished the latest draft and hands it off | Creator | `reviewer-in-progress` |
| `reviewer-in-progress` | Reviewer is evaluating the latest draft | Reviewer | `approved`, `needs-rework` |
| `needs-rework` | Reviewer found blocking issues and returned the work | Reviewer | `creator-in-progress` |
| `approved` | Reviewer accepted the draft and handed it to post-review routing | Reviewer -> Main Agent | `creator-in-progress`, `publish-in-progress` |
| `publish-in-progress` | Approved work is being committed, pushed, and prepared for PR / stable-surface updates | Main Agent (publisher / release actor) | `pr-open`, `merged` |
| `pr-open` | PR is open and comment triage is active | Main Agent (publisher / release actor) | `needs-rework`, `merged` |
| `merged` | Changes are merged; local sync and optional release follow-up remain | Main Agent (publisher / release actor) | `released`, terminal |
| `released` | Version and tag actions are complete when the change requires them | Main Agent (publisher / release actor) | terminal |

Notes:
- `merged` is terminal for changes that do not require a release action.
- `released` is required when a merge also performs a repository release step.
- Topic close is not complete until any required `summary artifact` exists and
  matches the final handoff outcome.
- If `required follow-up` remains at close time, the topic may reach terminal
  status only as an explicit close with follow-up; it must not be represented
  as fully done.
- Reviewer comments on an open PR may send the work back to `needs-rework`.
- `approved` means reviewer acceptance passed, but planner contract alignment may
  still route the topic back to `creator-in-progress` before publish.
- Reviewer ownership ends when it issues `approved`; Main Agent owns the
  Phase 4.5 routing decision that follows.
- Human interaction still exists at explicit stop points (for example, manual merge on
  GitHub), but those stop points do not transfer overall Phase 5-10 ownership away
  from Main Agent.
- STOP POINT 1 is intentionally not a terminal state; it is a human approval gate
  that may continue directly once approval exists and staged-scope conflicts are
  resolved.
- Once STOP POINT 2 is reached, Main Agent must fully stop and wait for a new
  explicit human resume message; it must not keep polling or waiting in the
  background for merge completion.
- If a late defect is discovered after merge but before release completes, route
  it explicitly; do not silently rewrite the original topic intent to make the
  defect disappear. Once a topic is `released`, use a follow-up repair topic
  instead of rolling the original topic back.

## Workflow phases

### Git execution view (trigger / input / output)

This table is the compact execution contract for the workflow phases that gate
git-visible execution. Some rows are not themselves git-mutating, but they
still define required trigger / input / output contracts for later git work.
The detailed phase text below explains the same phases in more depth, while
`.github/guides/MAIN-AGENT-WORKFLOW.md` turns them into executable command
patterns and recovery logic.

| Phase | Trigger | Required input | Output / transition | Owner |
| --- | --- | --- | --- | --- |
| 1. Plan the topic | New topic accepted for execution | Repo-visible planning intent; target topic name; locked scope once decided | `plan/<topic>/<topic>.plan.md` exists and topic can be marked `planned` | Planning actor / human |
| 2. Prepare the branch | Valid topic plan exists and execution is starting | Topic plan; branch naming policy; current branch/worktree state | Semantic execution branch is ready for work | Main Agent |
| 3. Creator implementation | Execution branch is ready and the topic plan is locked for drafting | Topic plan; repo instructions; target output paths | Draft stays within locked scope and reaches `review-ready`, or remains in creator rework | Creator |
| 4. Reviewer pass | Creator returns a `review-ready` draft | Skill folder; topic plan; Copilot feedback for context | Independent JSON verdict returns `approved` or `needs-rework` | Reviewer |
| 4.5 Planner contract alignment | Reviewer returned `approved` and required fixes are applied | Latest draft; latest topic plan; locked decisions; artifact paths | Either route back to `creator-in-progress` or move to `publish-in-progress` | Main Agent |
| 5. Stable library handling | Planner alignment passed and topic may affect stable-library surfaces | Stable library metadata; approved draft; current README / VERSION baseline | Stable-library timing decision is resolved: stage now, defer to release, or skip | Main Agent |
| 6. Commit, push, and PR | Pre-commit validation passed and Stop Point 1 is approved | Staged changes; execution branch; commit scope; PR target branch | Commits are created, pushed, and PR opens with status `pr-open` | Main Agent |
| 7-8. PR loop + bounded observation | PR is open and checks or comments may require action | PR reviews / review state; review comments; issue comments; check results; direct-apply rules; reviewer re-entry rule | Either new patch commit, reroute to reviewer, or a bounded clean-window report that is eligible for human merge-readiness confirmation | Main Agent |
| 9. Post-merge local sync | Human explicitly resumes after merge is confirmed on GitHub | Merged PR reference; current local worktree; preserved local state; human resume signal | Local repo is synchronized and topic reaches `merged`, but topic close still waits on any required `summary artifact` | Main Agent |
| 10. Release | Topic plan declares a release action and post-merge execution was explicitly resumed | Release timing instructions; stable library metadata when deferred; release readiness state | Tag and release actions complete, or topic stays terminal at `merged`; topic close still waits on any required `summary artifact` | Main Agent |

### 1. Plan the topic
1. Planning actor captures the topic in `plan/<topic>/<topic>.plan.md`.
2. Lock scope, decisions, and boundaries before execution.
3. Keep the plan repo-visible before any downstream git / review work starts.
4. Mark the topic as `planned`.

Execution boundary:
- Phase 1 defines the prerequisite execution contract: later phases consume a
  valid topic plan, but they do not define the full authoring methodology for a
  planning-specific tool or skill.
- This workflow does not define a separate numbered Phase 0; planning is the
  formal Phase 1 prerequisite in this repository.
- A future `plan-creator` may satisfy this prerequisite, but this workflow
  remains focused on execution after a valid topic plan exists.

### 2. Prepare the branch
1. Create or repair the execution branch using the repository branch policy.
2. Verify branch readiness before creator work begins:
   - current branch matches the topic intent, or a clear repair path is chosen
   - branch naming policy has been applied
   - current worktree state is understood and safe for this topic
   - unrelated dirty or untracked state is either intentionally preserved,
     explicitly approved, or treated as a stop condition
3. Keep the branch scoped to one topic or one tightly related change family.
4. Stop if branch readiness cannot be proven; do not begin creator work
   speculatively.
5. Do not start creator work from uncommitted chat-only planning notes.

Execution guardrail:
- Phase 3 must not start until Main Agent has verified the semantic execution
  branch and the current worktree state for this topic.

### 3. Creator implementation
1. Hand the topic plan plus relevant repo instructions to the creator.
2. The creator drafts or revises the work until it is `review-ready`.
3. The creator must keep the output within the locked boundaries from the topic plan.
4. Stable-library files such as `README.md` and `VERSION` stay untouched until
   reviewer approval unless the topic plan explicitly says otherwise.

Execution note:
- Phase 3 uses the creator skill as a normal drafting step (`@file:agent-skill-creator`
  in VS Code or `copilot skill agent-skill-creator` in CLI).
- Phase 3 is **not** the independent reviewer-style SubAgent handoff used in Phase 4.
- The explicit SubAgent boundary starts at reviewer pass, where independence from
  the creator context is required.

### 4. Reviewer pass (Two-Layer Independent Review)

The reviewer role is independent from the creator and ensures quality gate before publishing.

#### **New: Two-Layer Review Architecture** (as of v2.0)

This phase now includes **two complementary review layers**:

**Layer 1: Copilot PR Review Agent** (automatic)
- Scans code quality, formatting, style, links, typos
- Produces PR-like comments
- Single scan per phase (not continuous)

**Layer 2: Agent-Skill-Reviewer (SubAgent)** (independent)
- Evaluates SKILL design against `review-checklist.md`
- Reads topic plan to verify scope alignment
- Assesses Copilot feedback for reasonableness
- Returns structured verdict

#### **Three-Step Process**

**Step 4a: Creator Ready**
- SKILL draft complete (all required files present)
- Ready for independent review

**Step 4b: Copilot Scans**
- Copilot Review Agent scans commits one time
- Produces: code quality, formatting, link, typo comments
- Main Agent collects comments

**Step 4c: Reviewer Evaluates**
- SubAgent reads:
  - SKILL folder: `.github/skills/<skill-name>/`
  - Topic plan: `plan/<topic>/<topic>.plan.md`
  - Copilot feedback (for context)
- Produces: JSON verdict with detailed triage
- Confirms that actual draft locations still match the locked `Artifact paths`
  from the topic plan

#### In VS Code
- Open a SubAgent directly (within the same Copilot context)
- SubAgent reads the skill folder and topic plan
- Returns: JSON verdict with `approved` or `needs-rework`

#### In Copilot CLI
- Use the `/fleet` orchestrator for independent parallel review
- Command pattern:
  ```
  /fleet 根據 review-checklist.md 與 plan 評審 .github/skills/<skill-name>/

  路徑：
    - Skill folder: .github/skills/<skill-name>/
    - Topic plan: plan/<topic>/<topic>.plan.md

   評審內容：
     1. 符合 plan 的 Implementation steps？
     2. 例子和參考資料足夠深入？
     3. Copilot 的評論是否都妥當？(address/discuss/skip)
     4. `Artifact paths` 是否有效且與實際輸出位置一致？

  回傳 JSON：
  {
    "verdict": "approved|needs-rework",
    "blocking_issues": [...],
    "copilot_feedback_triage": {
      "ADDRESS": [...],
      "DISCUSS": [...],
      "SKIP": [...]
    }
  }
  ```
- This ensures reviewer logic is separate from creator's session context

#### **Reviewer Report Format (JSON)**

```json
{
  "verdict": "approved|needs-rework",
  "blocking_issues": [
    {
      "issue": "Missing Boundaries section",
      "file": "SKILL.md",
      "fix": "Add Boundaries section per SKILL.md template"
    }
  ],
  "copilot_feedback_triage": {
    "ADDRESS": [
      {
        "comment": "H1 title should use Title Case",
        "location": "SKILL.md line 6",
        "why": "Matches repo standard for consistency"
      }
    ],
    "DISCUSS": [
      {
        "comment": "Consider adding more edge-case examples",
        "optional": true,
        "why": "Would help readers, but not required"
      }
    ],
    "SKIP": [
      {
        "comment": "Use Markdown tables instead of ASCII",
        "why": "Not applicable; already using tables in examples.md"
      }
    ]
  }
}
```

#### Decision routing
1. If verdict is `needs-rework`:
   - Extract blocking issues
   - Route to creator; move topic to `creator-in-progress`
   - Creator fixes and loops back to Step 4a
2. If verdict is `approved`:
   - Creator applies `ADDRESS` feedback (required)
   - Creator optionally applies `DISCUSS` feedback
   - Creator skips `SKIP` feedback
   - Commit fixes with appropriate message
   - Continue to planner contract alignment before moving topic to
     `publish-in-progress`

**Note**: Reviewer is not creator. Reviewer does not approve own work.

#### Main Agent Implementation Detail

See `.github/guides/MAIN-AGENT-WORKFLOW.md` → Section "Phase 4: Two-Layer Review" for full orchestration logic including:
- How to invoke SubAgent with correct context
- How to parse JSON reviewer report
- How to route feedback back to creator
- Retry logic and error handling

### 4.5 Planner contract alignment checkpoint

This checkpoint runs after reviewer approval and after required reviewer feedback
is applied, but before publish work begins.

Owner:
- Main Agent runs this checkpoint and owns the routing decision that follows
  reviewer approval.

Purpose:
- verify that locked decisions in the topic plan still match the current draft
- verify that contract / schema / record-shape semantics did not drift during the
  creator + reviewer loop
- catch planner-level contract mismatches that are not ordinary code-quality or
  formatting feedback

Routing:
1. If planner contract alignment fails:
   - route the topic back to `creator-in-progress`
   - update the topic plan status accordingly
   - fix the drift before re-entering reviewer / planner gates per the status model
2. If planner contract alignment passes:
   - move topic to `publish-in-progress`

Notes:
- This is an independent checkpoint, not a rewrite of reviewer ownership.
- It exists because reviewer approval alone does not guarantee that plan-level
  contract semantics stayed aligned.

### 5. Stable library handling (if applicable)

Only applies when the skill is entering the stable library (per topic plan).

Execution contract:
- Trigger: planner contract alignment passed and the topic may update stable
  library surfaces.
- Input: approved draft, topic plan `Stable library metadata`, and current
  README / VERSION baseline.
- Output: a resolved timing decision for README / VERSION changes: stage now in
  `publish-in-progress`, defer to Phase 10 release, or skip because the topic is
  not entering the stable library.

1. Read the topic plan's `Stable library metadata` section for:
   - README row format (exact table entry to add)
   - VERSION bump direction (MAJOR | MINOR | PATCH)
   - Rationale (why this bump)
   - Timing (when README / VERSION actions occur)
2. If the section is absent, treat the topic as not entering the stable library.
3. If the section exists but timing is missing, stop and fix the topic plan before
   continuing.
4. If timing places README / VERSION updates at `publish-in-progress` timing,
   prepare them during Phase 5-6.
5. If timing places README / VERSION updates at `release` timing, the topic plan
   MUST also declare a release action that executes Phase 10.
6. If timing is `release` but no release action is declared, treat the topic plan
   as invalid, stop, and fix the plan before continuing.
7. If timing places README / VERSION updates at `release` timing and a release
   action is declared, defer them to Phase 10.

**Note**: Topic plan MUST include the `Stable library metadata` section before this phase.
If topic plan lacks this section, the skill is not intended for stable library.

### 6. Commit, push, and PR (with Pre-Commit Gate)

Execution contract:
- Trigger: Pre-commit validation passed and the human approves Stop Point 1.
- Input: validated staged changes, execution branch, commit scope, and PR target
  branch.
- Output: git history advances with the publish commits, remote branch is
  updated, PR is opened, and topic status moves to `pr-open`.

#### Staging Phase (Phase 5-6: Pre-Commit Checks)

Before committing, validate and stage changes:

1. **Validation** (Phase 5):
   - Verify all required files exist (SKILL.md, examples or reference)
   - Check SKILL.md structure (all 8 required sections)
   - Verify examples have positive and negative cases
   - Run lint/type checks if applicable

2. **Staging** (Phase 6):
    - Stage only the allowed file set for this topic:
      1. artifact paths locked in the topic plan
      2. direct-apply PR-fix files for the current loop
      3. extra files explicitly approved by a human
    - `README.md` and `VERSION` are **not** automatic exceptions; each file is
      allowed only when it is explicitly listed in the topic plan `Artifact paths`
    - Do not use broad staging defaults such as `git add -A` or `git add .`
      for publish work
    - If topic plan specifies stable-library update with `publish-in-progress` timing:
      - Stage README.md updates only if `README.md` is explicitly listed in
        `Artifact paths`
      - Stage VERSION bump only if `VERSION` is explicitly listed in
        `Artifact paths`
    - Display final preview of all staged changes; if unrelated files appear in
      the staged set, unstage and repair before STOP POINT 1

#### **[STOP POINT 1]** Before Commit

STOP POINT 1 is a positive authorization gate, not a terminal pause. Its job is
to prevent unsafe commit / push / PR creation, not to force an artificial halt
after the staged set is already valid.

README / VERSION appear in the staged set only when the topic plan schedules them
before PR creation.

Main Agent displays:
```
✅ VALIDATION COMPLETE

Staged changes:
  - .github/skills/<skill-name>/SKILL.md
  - .github/skills/<skill-name>/examples.md
  - README.md (new row added, if publish timing)
  - VERSION (bumped: 0.11.0 → 0.12.0, if publish timing)

Ready to commit + push + open PR on GitHub?
[Y] Proceed
[N] Back to Phase 5 (make more changes)
```

**If [N]**: Discard all staged changes; creator can modify further; ask again when ready

**If [Y]**:
- Proceed directly to commit.
- Do not add a second artificial waiting phase if the staged set is already valid
  and no blocking scope conflict remains.

#### Commit and Push (Phase 6)

1. Commit all approved changes:
   ```bash
   git commit -m "feat: add <skill-name> skill to stable library

   - Implements [topic-name] plan
   - SKILL.md with all required sections
   - examples.md with positive/negative cases
   - README.md updated (new row per stable-library metadata)
   - VERSION bumped: [old] → [new]

   Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
   ```

2. Commit plan status update:
   ```bash
   git commit -m "chore: mark plan status as pr-open

   Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
   ```

3. Push the branch to remote:
   ```bash
   git push
   ```

4. Open a PR using GitHub CLI:
   ```bash
   gh pr create \
     --title "Add <skill-name> skill to stable library" \
     --body "Implements plan/<topic>/<topic>.plan.md

   See detailed spec in `.github/guides/MAIN-AGENT-WORKFLOW.md`" \
     --base main
   ```

5. Move topic to `pr-open`

### 7. Creator patches on PR with Termination Logic (Phase 7-8: MAX 3 ITERATIONS)

After PR is open, comments may arrive (Copilot reviewer, CI checks, or human review).

Execution contract:
- Trigger: topic status is `pr-open` and new comments or failed checks require
  action.
- Input: latest PR reviews / current review state, latest review comments,
  latest issue comments, current check state, direct-apply rules, and the
  reroute rule for reviewer-required changes.
- Output: either a new patch commit on the same PR, a route back to Phase 4 for
  reviewer re-check, or a bounded clean-window report that is eligible for
  human merge-readiness confirmation.

#### Direct-apply (no reviewer loop needed)
Creator may directly commit fixes for:
- **Style**: H1 Title Case, code fence type (` ```py `), imports formatting, whitespace
- **Typo**: spelling, grammar, punctuation errors in text
- **Meta**: link corrections, file path updates, example titles, numbering
- **Formatting**: indentation, blank lines, table alignment, list structure

#### Do NOT directly apply (requires reviewer re-check)
- **Trigger logic**: changes to when the skill should be used
- **Core examples**: changes to example's decision flow, assumption set, or logic
- **Missing requirements**: adding imports, dependencies, or prerequisites to examples
- **Process or Boundaries**: changes to skill definition or scope
- **Scope expansion**: new sections, new features, or changed responsibilities
- **Example behavior**: changes that affect whether example code is runnable

#### Blocking signal definition
A PR snapshot is blocking when any newly observed signal indicates the branch is
not yet safe for merge handoff. Blocking signals include:
- a PR review with a blocking review state, especially `CHANGES_REQUESTED`
- an unresolved blocking review thread
- a review comment that still requires action
- an issue comment that still requires action
- a check run that is not yet clean:
  - status is not `completed`, or
  - conclusion is not a success-like state such as `success`, `neutral`, or
    `skipped`

#### PR Observation States (before handoff)
- **Clean snapshot**: one fetch found no blocking signal, but the observation
  window is not yet complete.
- **Observation window active**: the agent is still inside the bounded
  `consecutive-empty-checks` window.
- **Observation window exhausted**: three consecutive clean snapshots were seen
  using waits of `30s -> 60s -> 120s`.
- **Eligible for human merge-readiness confirmation**: the bounded window ended
  without a new blocking signal, but the agent still may not claim the PR is
  merge-ready on its own.
- **STOP POINT 2**: reached only after the human explicitly chooses merge
  handoff.

#### PR Comment Loop Logic (Phase 7-8)

```
iteration = 0
max_iterations = 3
empty_checks = 0
observation_waits_seconds = [30, 60, 120]

LOOP:
  1. Fetch latest PR reviews / current review state, latest review comments,
     latest issue comments, and current check runs

  2. If any blocking signal exists:
     - Reset empty_checks = 0
     - Treat blocking PR review state, unresolved blocking review thread,
       blocking comment state, failed or non-complete checks, or other newly
       blocking PR state as NOT clean
     - Classify comments and review outcomes (direct-apply? / needs-reviewer?)
     - If ALL actionable items are direct-apply:
        - Creator applies fixes
        - Commit: git commit -m "fix: address PR feedback on [specific items]"
        - Push: git push
        - iteration += 1
        - Loop back to step 1
     - If ANY actionable item requires reviewer re-check:
        - Route back to Phase 4 (invoke reviewer again)
        - Reviewer evaluates new issues
        - If approved: continue Phase 7-8 loop
        - If needs-rework: back to creator Phase 3

  3. If no blocking signal exists in the current snapshot:
     - empty_checks += 1
     - If empty_checks < 3:
        - Sleep observation_waits_seconds[empty_checks - 1]
        - Loop back to step 1
     - If empty_checks == 3:
        - Exit the bounded observation window
        - Report only:
          1. no new blocking signal was observed within the bounded window
             across PR reviews, comments, and check runs
          2. this is not a guarantee that later feedback will not arrive
          3. a human must decide whether to inspect the PR and hand off merge
        - Continue to the human merge-readiness confirmation gate

  4. If iteration >= max_iterations:
     - Display: "Reached max PR iterations (3)"
     - Stop direct-apply looping
     - Remain in `pr-open` until a human decides the next step
```

**Iteration Limit**: After 3 loops of direct-apply fixes, Main Agent stops the
direct-apply loop (prevents infinite looping), but that limit does not by
itself prove merge readiness or skip the observation / human gate.

**Reviewer Re-routing**: If any comment falls outside direct-apply, immediately route back to Phase 4 for re-evaluation.

#### **[STOP POINT 2]** Before Manual Merge

STOP POINT 2 is a terminal / no-op gate. After human merge handoff, the current
execution must stop completely. It is not a "wait here and keep checking"
boundary.

Main Agent displays:
```
✅ BOUNDED PR OBSERVATION COMPLETE

PR: #<number> <github.com/.../pull/<number>>
Branch: <type>/<username>/<short-description>
Observation: 3 consecutive clean checks (`30s -> 60s -> 120s`)
Signals checked: PR reviews / review state, review comments, issue comments,
check runs
Result: No new blocking signal observed within the bounded window

Important:
  - This is not a guarantee that later feedback will not arrive
  - Main Agent is not declaring the PR merge-ready on its own
  - A human must inspect the PR and decide whether to hand off merge

Next step: Human decides whether to inspect the PR and proceed to manual merge handoff

After handoff, Main Agent will:
  - Stop here completely immediately after handoff
  - Resume only after a human sends a new explicit merge-confirmation message
  - After that resume, run git-post-merge-workflow
  - After that resume, run git-release-management (if plan specifies)
  - After that resume, update local branches

Ready to hand off to human merge and stop here?
[Y] Hand off to human merge and stop here
[N] Stop here; a human may resume later with a new explicit message
```

**If [N]**:
- Stop the current execution.
- Do not poll, wait in the background, or ask again automatically.
- A human may later resume from this stop point with a new explicit message.

**If [Y]**:
- Instruct user: "Go to [PR link] and click Merge"
- Stop the current execution immediately after handoff.
- Do not poll GitHub for merge detection.
- Resume at Phase 9 only when a human sends a new explicit message confirming
  merge and telling the workflow to continue.

#### Each direct-apply fix gets a new commit

- Commits are atomic (one logical fix per commit)
- Commit message uses `git-commit-convention`
- Messages must reference the PR comment being fixed

### 8. Merge

Human merges the PR when ready.

### 9. Post-merge local sync

After a human explicitly resumes the workflow and the merge is confirmed, Main Agent continues the workflow and runs
`git-post-merge-workflow` as a normal post-merge skill step to synchronize local
branches and clean up. This is not a new reviewer-style independent SubAgent
handoff.

Execution contract:
- Trigger: a human explicitly resumes the workflow after merge and merge is
  confirmed on GitHub.
- Input: merged PR state, local worktree state, untracked files, any local
  state that still needs preservation, and the human resume signal.
- Output: local repository is safely synchronized, branch cleanup is complete,
  and topic status reaches `merged`.

Required guardrails and sequence:
1. Confirm that the referenced PR or merge path actually merged before cleanup
   starts.
2. Inspect the current worktree, including untracked files and any preserved local
   state, before syncing.
3. Distinguish repo-history changes from local-only state so users do not mistake
   local loss or drift for an upstream rollback.
4. If local state still needs preservation, capture it safely before cleanup or
   sync steps proceed.
5. Only then run the normal post-merge cleanup / sync actions.
6. Do not treat local sync completion as topic close when a required
   `summary artifact` is still missing.

### 10. Release (if applicable)

Execution contract:
- Trigger: the topic plan declares a release action after merge.
- Input: release timing instructions, stable-library metadata when deferred to
  release timing, and release-readiness checks.
- Output: annotated tag is created and pushed with topic status `released`, or
  the topic remains terminal at `merged` when no release action applies.

If topic plan specified a release action:
1. Read the topic plan's release timing instructions.
2. If stable-library metadata scheduled README / VERSION changes at `release`
   timing, apply them now before release completion.
3. Main Agent continues and runs `git-release-management` as a normal release
   skill step to validate release readiness.
4. If a late defect is discovered during Phase 10:
   - stop release work immediately
   - do not silently rewrite the original topic's locked intent
   - if the topic is already `merged` but not yet `released`, route the next step
     explicitly with human judgment (for example, limited rollback or a follow-up
     repair topic)
   - if the topic is already `released`, use a new repair topic instead of
     rolling the original topic back
5. Create annotated tag with semantic version.
6. Push tag to remote.
7. Move topic to `released`.
8. If topic-close handoff or `required follow-up` applies, create or validate
   the required `summary artifact` before treating the topic as closed.

If no release action: topic is terminal at `merged`.

Close semantics:
- A required `summary artifact` may be created after Phase 9 for non-release
  topics or after Phase 10 for release topics, but topic close is incomplete
  until that artifact exists.
- If the final artifact declares `required follow-up`, the close result is
  explicitly close with follow-up rather than fully done.

## Topic plan template

Every skill topic plan must include these fixed sections (11 required):

1. **Goal / outcome**
2. **Scope**
3. **Locked decisions**
4. **Boundaries / exclusions**
5. **Status / allowed transitions**
6. **Artifact paths**
7. **Implementation steps**
8. **Validation / acceptance checks**
9. **Reviewer handoff**
10. **Post-merge / release actions**
11. **Open questions / unresolved items**

When correction artifacts apply to a topic, list them explicitly under
**Artifact paths** beside the parent artifacts they are correcting.

If the topic requires two or more workflow-role handoffs or declares
`required follow-up`, also list the exact `step.md` path under
**Artifact paths**. If the topic will close with a handoff or with
`required follow-up`, list the exact repo-visible `summary artifact` path there
as well.

### New: Stable library metadata (if applicable)

If the skill is intended to enter the stable library, add this section before Phase 5 (Stable library handling):

```markdown
## Stable library metadata

When this skill is approved, it enters the stable library. Specify:

### README update
- Table/section name: Current Skills (or other location per repo policy)
- New row format (exact):
  ```
  | skill-name | Brief description of skill purpose | .github/skills/skill-name/ |
  ```
- Position: Alphabetical order by skill name (or other rule)

### VERSION bump
- Current version: (read from root `VERSION` file)
- Bump direction: MAJOR | MINOR | PATCH
- New version: (calculated)
- Reason: (e.g., "New stable skill" or "Backward-compatible feature addition")

### Timing
- README/VERSION timing: (choose one: `publish-in-progress` | `release`)
- Why this timing is correct for the topic
- If timing is `release`, `Post-merge / release actions` must declare the release
  action that executes Phase 10

**Example from python-context-management:**
```
### README update
- Table: Current Skills
- New row:
  ```
  | python-context-management | Synchronous context-manager design guidance | .github/skills/python-context-management/ |
  ```
- Position: Between python-class-design and python-error-handling (alphabetical)

### VERSION bump
- Current: 0.11.0
- Direction: MINOR (new stable skill)
- New: 0.12.0
- Reason: New stable skill (non-breaking capability)

### Timing
- README/VERSION timing: `release`
- Reason: stable-library row and version bump are part of the post-merge release step for this topic
- Release action: declared in `Post-merge / release actions`
```
```

**Note**: Reviewer will validate this section exists, is complete, and declares timing before approving.

## New: Main Agent Orchestration Specification

For detailed Main Agent implementation logic, including phase transitions, checkpoint-based resumability, error handling patterns, and SubAgent communication formats, see:

**`.github/guides/MAIN-AGENT-WORKFLOW.md`** (NEW in v2.0)

Responsibility split:
- `plan/agent-handoff-workflow.md` owns the canonical phase semantics,
  trigger/input/output contract, role boundaries, and stop-point meaning.
- `.github/guides/MAIN-AGENT-WORKFLOW.md` owns executable orchestration detail:
  command patterns, retries, checkpoints, and environment-specific execution
  notes.

This guide covers:
- All 10 phases with executable logic
- Two-layer review architecture (Copilot + Reviewer)
- Pre-commit stop points (avoid fake git state)
- PR loop with max 3 iterations (prevent infinite loops)
- JSON-formatted SubAgent reports (structured communication)
- Checkpoint-based crash recovery
- Ask-user-only error handling (maximum transparency)

**When to use**:
- Main Agent developers: Reference for orchestration logic
- Skill creators: Understand phase flow and human stop points
- Reviewers: Understand what Main Agent expects from SubAgent
- Testers: Use for workflow verification and debugging

## Version History

### v2.0 (2026-04-22)
- **New**: `.github/guides/MAIN-AGENT-WORKFLOW.md` with full 10-phase executable spec
- **New**: Two-layer review architecture (Copilot + agent-skill-reviewer with JSON reports)
- **New**: Pre-commit stop points (Phase 6, BEFORE commit)
- **New**: PR loop max 3 iterations + termination logic
- **New**: Checkpoint-based resumability for crash recovery
- **Enhanced**: Phase 4 section with detailed three-step review process
- **Enhanced**: Phase 6-7 sections with stop points and loop termination
- **Updated**: Reviewer report format (JSON + Markdown)

### v1.0 (earlier)
- Initial workflow definition (single-review model)

## VS Code and CLI Workflow Examples

### VS Code Complete Workflow

Use this pattern in VS Code Copilot with `@file` and `@runSubagent` syntax:

```markdown
# Agent Skill Release Workflow (VS Code)

開發分支命名
  ↓ [User or auto-detect]
@file:git-branch-naming <skill_name>
  ↓
@file:agent-skill-creator <path/to/topic_plan.md>
  → Normal creator skill invocation (not `@runSubagent`)
  → Creator drafts skill files
  → Creator outputs: "This skill is review-ready"
  ↓
@runSubagent run @file:agent-skill-reviewer
  → Reviewer evaluates against review-checklist.md
  → Returns: approved or needs-rework
  ↓ [if approved, continue; if needs-rework, loop back to creator]
交互確認: 讀 topic plan 的 Stable library metadata
  → Confirm README row format
  → Confirm VERSION bump direction
  ↓ [User manual step]
手動或自動化:
  - 更新 README.md 按照 metadata 指定的 row format
  - 更新 VERSION 按照 metadata 指定的 bump direction
  ↓
@file:git-commit-convention
  → Draft or review commit message
  → Stage only the allowed file set (artifact paths + approved extras)
  → Commit after staged preview is confirmed
  ↓
提交 commit + 開 PR
  → git push
  → gh pr create --base dev
  ↓ [Human review + merge via GitHub]
  → Main Agent stops completely at STOP POINT 2
  → Human returns later with explicit merge confirmation
  ↓
@file:git-post-merge-workflow
  → Main Agent resumes after explicit human message
  → Clean up local branches
  → Sync with remote
  ↓
@file:git-release-management
  → Main Agent continues with release checks
  → Validate release readiness
  → Create annotated tag
  → Push tag to remote
```

**Key interaction points:**
- After Phase 3 (Creator): User or automation triggers Reviewer
- After Phase 4 (Reviewer): User confirms metadata + manually updates README/VERSION (or automation)
- After Phase 5 (Publish): User decides commit scope (direct-apply rules from Phase 7 apply)
- At STOP POINT 2: Main Agent fully stops; user later resumes with an explicit merge-confirmation message before post-merge and release steps continue

### CLI Complete Workflow

Use this pattern in Copilot CLI with `/fleet` and `copilot skill` syntax:

```bash
#!/bin/bash
# Agent Skill Release Workflow (CLI)

SKILL_NAME="my-skill"
SKILL_PATH=".github/skills/${SKILL_NAME}"
TOPIC_PLAN="plan/${SKILL_NAME}/${SKILL_NAME}.plan.md"

# Phase 1: Plan (user-created; not automated)
# Expected: $TOPIC_PLAN exists with all 11 sections + Stable library metadata

# Phase 2: Branch
git checkout -b feat/a129924/${SKILL_NAME}

# Phase 3: Creator draft
# Normal skill invocation, not an independent /fleet SubAgent
copilot skill agent-skill-creator ${TOPIC_PLAN}
# Creator outputs: "This skill is review-ready"

# Phase 4: Reviewer (independent SubAgent via /fleet)
/fleet 根據 .github/skills/agent-skill-reviewer/review-checklist.md 評審 ${SKILL_PATH}
# Outputs: approved or needs-rework
# If needs-rework, loop back to Phase 3

# Phase 5: Stable library metadata confirmation (user manual)
echo "Confirm from $TOPIC_PLAN:"
grep -A 10 "## Stable library metadata" ${TOPIC_PLAN}
read -p "Press enter to confirm metadata, then manually update README.md and VERSION"

# Manual steps (or automation if parsing metadata):
# - Update README.md per metadata format
# - Update VERSION per metadata direction

# Phase 6: Commit + Push + PR
# Stage only the allowed file set for this topic; do not use git add -A / git add .
git add <locked-artifact-paths> [approved-extra-files]
copilot skill git-commit-convention
# Review commit message, then:
git push origin feat/a129924/${SKILL_NAME}
gh pr create --base dev

# Phase 8: Merge (human via GitHub)
# STOP here completely; no background polling
# Human returns later with explicit merge confirmation, then continue:

# Phase 9: Post-merge workflow (Main Agent resumes after explicit human message)
# Normal skill invocation under Main Agent control, not a separate operator-owned handoff
copilot skill git-post-merge-workflow

# Phase 10: Release (if applicable; still Main Agent-controlled)
# Normal skill invocation under Main Agent control
copilot skill git-release-management
# Tag and push
```

**Key differences from VS Code:**
- `/fleet` launches independent SubAgent (vs `@runSubagent` in VS Code)
- Metadata confirmation is user manual (could be automated with parsing)
- Uses `copilot skill` command instead of `@file:` syntax
- Phase 9-10 remain Main Agent phases even when the CLI surface uses
  `copilot skill ...` syntax for the concrete skill invocation

### Tool Mapping

| VS Code | CLI | Purpose |
|---|---|---|
| `@file:<skill>` | `copilot skill <skill>` | Invoke skill |
| `@runSubagent` | `/fleet` (+ natural language) | Independent SubAgent |
| `@file:` file reference | shell variable + path | Pass context |
| Inline @runSubagent | Separate command | Sequence steps |

---

## Implementation Notes

1. **Topic plan metadata is mandatory** when skill enters stable library
   - Must include README row format, VERSION direction, rationale
   - Both VSCode and CLI workflows expect this section

2. **Direct-apply boundary** (Phase 7) applies to both environments
   - VSCode and CLI handle PR comments the same way
   - Only style/typo/meta fixes directly applied; others route back to reviewer

3. **Status model** is repo-visible (not session-specific)
   - topic plan status field updated consistently across environments
   - Both environments read the same review-checklist.md
4. **Phase 9-10 ownership** stays with Main Agent
   - post-merge and release are follow-up phases in the same workflow
   - they resume only after an explicit human message following STOP POINT 2
   - command syntax does not change the actor model

## VS Code and CLI Notes

- VS Code may orchestrate multiple main/sub-agents from one broad task, but the
  workflow still depends on repo-visible artifacts rather than hidden tab state.
- CLI may launch separate agents more explicitly via `/fleet`, but the workflow should read
  the same topic plan and use the same status model.
- In both environments, Phase 9-10 are Main Agent continuation steps after an
  explicit human resume following STOP POINT 2; only the reviewer pass requires
  the explicit independent SubAgent boundary.
- Worktrees are optional execution mechanics, not part of the canonical contract.

## Boundaries
- This document does not define one mandatory shell command sequence.
- It does not replace `.github/copilot-instructions.md` or skill-local rules.
- It does not let creator and reviewer collapse into one role.
- It does not treat PR comments as a replacement for the reviewer verdict.
