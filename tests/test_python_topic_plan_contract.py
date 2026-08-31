# Copyright (c) 2026 deterministic-response-cache contributors

"""Conformance checks for the canonical Python topic-plan profile."""

from pathlib import Path

import pytest

FIXTURE_ROOT = Path(__file__).parent / "fixtures" / "python-topic-plan-contract"
REPOSITORY_ROOT = Path(__file__).parents[1]
PLAN_PATH = FIXTURE_ROOT / "python-topic-plan-contract.plan.md"
SPEC_PATH = FIXTURE_ROOT / "python-topic-plan-contract.spec.md"
STEP_PATH = FIXTURE_ROOT / "python-topic-plan-contract.step.md"
CANONICAL_TEMPLATE_PATH = (
    REPOSITORY_ROOT
    / ".agents"
    / "skills"
    / "python-plan-authoring"
    / "templates"
    / "canonical-python-topic-plan-template.md"
)
CANONICAL_STEP_TEMPLATE_PATH = (
    REPOSITORY_ROOT
    / ".agents"
    / "skills"
    / "python-plan-authoring"
    / "templates"
    / "canonical-step-template.md"
)

PROFILE_CONSUMERS = (
    ".agents/skills/python-plan-authoring/SKILL.md",
    ".agents/skills/python-plan-review/SKILL.md",
    ".agents/skills/python-tdd-test-authoring/SKILL.md",
    ".agents/skills/python-implementation-review/SKILL.md",
    ".agents/skills/step-creator/references/python-plan-authoring-adapter.md",
)

CANONICAL_HEADINGS = (
    "## Goal / Outcome",
    "## Scope",
    "## Locked Decisions",
    "## Boundaries / Exclusions",
    "## Status / Allowed Transitions",
    "## Artifact Paths",
    "## Implementation Steps",
    "## Validation / Acceptance Checks",
    "## Reviewer Handoff",
    "## Post-merge / release actions",
    "## Open Questions / Unresolved Items",
)

PYTHON_METADATA_HEADINGS = (
    "## Python implementation metadata",
    "### Non-goals",
    "### Current Context",
    "### Requirements",
    "### Decisions",
    "### Public Contract / API Changes",
    "### Affected Files / Modules",
    "### Test Plan",
    "### Risks",
    "### Rollback Plan",
)

STEP_HEADINGS = (
    "## Workflow Stages",
    "## Actionable Steps",
    "## Implementation Steps",
    "## Main Agent Actionable Steps — Fixed Tail",
    "## Handoff / Gate Notes",
)


def _missing_headings(document: str, headings: tuple[str, ...]) -> list[str]:
    return [heading for heading in headings if heading not in document]


def test_complete_fixture_uses_the_canonical_python_profile() -> None:
    """Accept the complete canonical plan profile."""
    plan = PLAN_PATH.read_text(encoding="utf-8")

    assert _missing_headings(plan, CANONICAL_HEADINGS) == []
    assert _missing_headings(plan, PYTHON_METADATA_HEADINGS) == []
    assert plan.index("## Artifact Paths") < plan.index("## Python implementation metadata")
    assert "Async-planning status: exempt — cite exemption evidence:" in plan


def test_missing_python_metadata_heading_is_rejected() -> None:
    """Detect missing required Python metadata."""
    plan = PLAN_PATH.read_text(encoding="utf-8")
    incomplete_plan = plan.replace("### Rollback Plan", "### Reversal", 1)

    assert _missing_headings(incomplete_plan, PYTHON_METADATA_HEADINGS) == ["### Rollback Plan"]


def test_fixture_spec_and_step_have_required_sections() -> None:
    """Require the companion specification and step layout."""
    spec = SPEC_PATH.read_text(encoding="utf-8")
    step = STEP_PATH.read_text(encoding="utf-8")

    assert (
        _missing_headings(
            spec,
            ("## Acceptance Criteria", "## Behavioral Scenarios", "## Error / Edge Cases"),
        )
        == []
    )
    assert _missing_headings(step, STEP_HEADINGS) == []


def test_canonical_templates_match_the_fixture_profile() -> None:
    """Keep canonical plan and step templates structurally valid."""
    plan_template = CANONICAL_TEMPLATE_PATH.read_text(encoding="utf-8")
    step_template = CANONICAL_STEP_TEMPLATE_PATH.read_text(encoding="utf-8")

    assert _missing_headings(plan_template, CANONICAL_HEADINGS) == []
    assert _missing_headings(plan_template, PYTHON_METADATA_HEADINGS) == []
    assert _missing_headings(step_template, STEP_HEADINGS) == []


def test_lowercase_implementation_marker_remains_pending() -> None:
    """Keep lowercase checkbox markers pending."""
    step = STEP_PATH.read_text(encoding="utf-8")
    implementation_section = step.split("## Implementation Steps", maxsplit=1)[1].split(
        "## Main Agent Actionable Steps — Fixed Tail",
        maxsplit=1,
    )[0]

    assert "- [X] 1. Read the fixture plan." in implementation_section
    assert "- [x]" not in implementation_section

    pending_step = implementation_section.replace("- [X]", "- [x]", 1)
    assert "- [x]" in pending_step
    assert "- [X]" not in pending_step


@pytest.mark.parametrize("heading", CANONICAL_HEADINGS)
def test_canonical_headings_are_not_python_metadata(heading: str) -> None:
    """Keep shared and Python-specific headings distinct."""
    assert heading not in PYTHON_METADATA_HEADINGS


@pytest.mark.parametrize("relative_path", PROFILE_CONSUMERS)
def test_python_workflow_consumers_reference_the_shared_profile(relative_path: str) -> None:
    """Keep every Python workflow consumer tied to the same schema authority."""
    skill = (REPOSITORY_ROOT / relative_path).read_text(encoding="utf-8")

    assert "canonical-topic-plan-profile.md" in skill
