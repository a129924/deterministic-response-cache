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

B2_ROUTE_PATHS = {
    "workflow": "plan/agent-handoff-workflow.md",
    "topic_contract": "plan/topic-plan-contract.md",
    "parent_plan": "plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md",
    "parent_spec": "plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md",
    "parent_step": "plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md",
    "b2_plan": (
        "plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b2-plan.md"
    ),
    "b2_step": (
        "plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b2-step.md"
    ),
}

B2_EVIDENCE_PATHS = (
    "plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b2-tester-evidence.md",
    "plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b2-implementation-review-log.md",
)


def read(path: str) -> str:
    """Read one declared repository contract surface."""
    return (ROOT / path).read_text(encoding="utf-8")


def read_b2_route() -> dict[str, str]:
    """Read every B2 routing authority used by the S3 conformance gate."""
    return {name: read(path) for name, path in B2_ROUTE_PATHS.items()}


def assert_b2_s3_route_is_fail_closed(route: dict[str, str]) -> None:
    """Reject any route that reuses frozen provenance or broadens S3 descendants."""
    assert set(route) == set(B2_ROUTE_PATHS)

    assert "B0/S1/T1/V1、B1" in route["workflow"]
    assert "frozen provenance" in route["parent_step"]
    assert "不能作為 current gate 或新 subject" in route["workflow"]
    assert "all old correction artifacts are frozen provenance only" in route["parent_step"]

    b2_subject_boundary = route["b2_plan"] + route["b2_step"] + route["parent_plan"]
    assert "B2 is a one-time verified-tree baseline, never a subject." in b2_subject_boundary
    assert "B2 is non-subject" in b2_subject_boundary
    assert "B1/B2 as subject" in b2_subject_boundary

    s3_subject_boundary = route["parent_plan"] + route["parent_spec"] + route["parent_step"]
    assert "S3 is non-merge" in s3_subject_boundary
    assert "implementation_subject_sha" in s3_subject_boundary
    assert "tests/test_observer_dispatcher_governance_contract.py" in s3_subject_boundary

    topology = (
        route["workflow"]
        + route["topic_contract"]
        + route["parent_plan"]
        + route["b2_plan"]
        + route["b2_step"]
    )
    assert "`S3..V3`" in topology
    assert "exactly T3 then V3" in route["b2_step"]
    assert "no merge, extra descendant, or `HEAD` range." in route["b2_step"]
    assert "never `HEAD`" in topology
    assert all(path in topology for path in B2_EVIDENCE_PATHS)


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


def test_b2_route_freezes_prior_epochs_and_resets_the_subject_at_s3() -> None:
    """Require B2 to stay a baseline while S3 is the sole new subject."""
    assert_b2_s3_route_is_fail_closed(read_b2_route())


@pytest.mark.parametrize(
    ("source", "required_text", "replacement"),
    [
        (
            "workflow",
            "B0/S1/T1/V1、B1",
            "B0/T1/V1、B1",
        ),
        (
            "parent_step",
            "all old correction artifacts are frozen provenance only",
            "all old correction artifacts are current routing",
        ),
        (
            "b2_plan",
            "B2 is a one-time verified-tree baseline, never a subject.",
            "B2 establishes the implementation subject.",
        ),
        (
            "b2_step",
            "exactly T3 then V3",
            "T3, V3, or another descendant may follow S3.",
        ),
    ],
)
def test_b2_s3_route_rejects_provenance_subject_and_topology_mutations(
    source: str,
    required_text: str,
    replacement: str,
) -> None:
    """Make removal of an epoch, subject, or topology invariant fail closed."""
    mutated_route = read_b2_route()
    assert required_text in mutated_route[source]
    mutated_route[source] = mutated_route[source].replace(required_text, replacement, 1)

    with pytest.raises(AssertionError):
        assert_b2_s3_route_is_fail_closed(mutated_route)


def test_s3_contract_test_preserves_direct_import_behavior() -> None:
    """Keep this conformance test free of dynamic-import substitutions."""
    source = read("tests/test_observer_dispatcher_governance_contract.py")
    for forbidden in ("import" + "lib", "__" + "import__", "sys." + "modules"):
        assert forbidden not in source
