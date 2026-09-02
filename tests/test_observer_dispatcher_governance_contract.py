# Copyright (c) 2026 deterministic-response-cache contributors

"""Conformance checks for Observer / Dispatcher governance surfaces."""

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATHS = (
    "AGENTS.md",
    ".codex/agents/planner.toml",
    ".codex/agents/implementer.toml",
    ".agents/skills/plan-creator/SKILL.md",
    ".agents/skills/plan-creator/checklist.md",
    ".agents/skills/plan-creator/templates/topic-plan-template.md",
    ".agents/skills/plan-reviewer/SKILL.md",
    ".agents/skills/plan-reviewer/checklist.md",
    ".agents/skills/plan-reviewer/reference.md",
    ".agents/skills/plan-reviewer/examples.md",
    ".agents/skills/python-implementation-workflow/SKILL.md",
    ".agents/skills/python-plan-authoring/templates/canonical-python-topic-plan-template.md",
)


def read(path: str) -> str:
    """Read one declared repository contract surface."""
    return (ROOT / path).read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def surfaces() -> dict[str, str]:
    """Provide the contract surfaces governed by this topic."""
    return {
        "governance": read("AGENTS.md"),
        "planner": read(".codex/agents/planner.toml"),
        "implementer": read(".codex/agents/implementer.toml"),
        "creator": read(".agents/skills/plan-creator/SKILL.md"),
        "creator_checklist": read(".agents/skills/plan-creator/checklist.md"),
        "creator_template": read(".agents/skills/plan-creator/templates/topic-plan-template.md"),
        "reviewer": read(".agents/skills/plan-reviewer/SKILL.md"),
        "reviewer_checklist": read(".agents/skills/plan-reviewer/checklist.md"),
        "reviewer_reference": read(".agents/skills/plan-reviewer/reference.md"),
        "reviewer_examples": read(".agents/skills/plan-reviewer/examples.md"),
        "python_workflow": read(".agents/skills/python-implementation-workflow/SKILL.md"),
        "python_template": read(
            ".agents/skills/python-plan-authoring/templates/canonical-python-topic-plan-template.md",
        ),
    }


def test_all_declared_contract_surfaces_are_repo_visible() -> None:
    """Keep every declared contract surface at its exact path."""
    assert all((ROOT / path).is_file() for path in CONTRACT_PATHS)


def test_runtime_bootstrap_and_allowlist_belong_to_planner(
    surfaces: dict[str, str],
) -> None:
    """Keep Planner as the sole runtime bootstrap and allowlist owner."""
    assert "runtime bootstrap 的唯一入口是 Planner" in surfaces["governance"]
    assert "Planner 擁有 runtime allowlist" in surfaces["governance"]
    for role in (
        "Planner",
        "Plan-Creator",
        "Plan-Reviewer",
        "Implementer",
        "Tester",
        "Reviewer",
        "Explorer",
    ):
        assert role in surfaces["planner"]
    assert "You do not own runtime routing" in surfaces["implementer"]


def test_only_authorized_implementer_publish_is_bounded(
    surfaces: dict[str, str],
) -> None:
    """Require all Implementer publishing authority to remain bounded."""
    for content in (
        surfaces["governance"],
        surfaces["planner"],
        surfaces["implementer"],
        surfaces["python_workflow"],
    ):
        assert "Tester evidence" in content
        assert "merge" in content
    assert "bounded commit, push, and draft PR" in surfaces["implementer"]
    assert "never authorizes merge" in surfaces["implementer"]


@pytest.mark.parametrize("surface", ["creator_template", "python_template"])
def test_templates_require_tester_and_no_direct_publish_to_merged(
    surfaces: dict[str, str],
    surface: str,
) -> None:
    """Require Tester and draft-PR boundaries in authoring templates."""
    content = surfaces[surface]
    assert "tester-in-progress" in content
    assert "`publish-in-progress` -> `pr-open`" in content
    assert "\n  - `publish-in-progress` -> `merged`" not in content
    assert "`pr-open` -> `merged`" in content


def test_plan_reviewer_checks_tester_and_human_merge_boundary(surfaces: dict[str, str]) -> None:
    """Require reviewer surfaces to enforce the Tester and Human gates."""
    content = (
        surfaces["reviewer"]
        + surfaces["reviewer_checklist"]
        + surfaces["reviewer_reference"]
        + surfaces["reviewer_examples"]
    )
    assert "independent Tester" in content
    assert "cannot transition directly to `merged`" in content


@pytest.mark.parametrize(
    "surface",
    [
        "creator",
        "creator_checklist",
        "creator_template",
        "reviewer_checklist",
        "reviewer_reference",
        "reviewer_examples",
        "python_template",
    ],
)
def test_correction_extension_is_conditional_and_complete(
    surfaces: dict[str, str],
    surface: str,
) -> None:
    """Keep the correction artifact extension conditional and complete."""
    content = surfaces[surface]
    assert "conditional" in content
    for artifact in (
        "correction plan",
        "correction step",
        "correction-plan review log",
        "Tester evidence",
        "implementation-review log",
    ):
        assert artifact in content
    assert "schema authority" in content


def test_correction_review_inputs_are_allowlisted(surfaces: dict[str, str]) -> None:
    """Reject correction-review inputs that are not explicitly allowlisted."""
    content = surfaces["reviewer"] + surfaces["reviewer_reference"]
    assert "correction-review input allowlist" in content
    assert "chat, branch, summary, `GOAL.md`, or `.github/agents/**`" in content
    assert "The Plan-Reviewer may write only the declared correction-plan verdict" in content
