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

B4R4_ROUTE_PATHS = {
    "workflow": "plan/agent-handoff-workflow.md",
    "topic_contract": "plan/topic-plan-contract.md",
    "parent_plan": "plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md",
    "parent_spec": "plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md",
    "parent_step": "plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md",
    "b4r4_plan": (
        "plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r4-plan.md"
    ),
    "b4r4_step": (
        "plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r4-step.md"
    ),
    "bootstrap_test": "tests/test_observer_dispatcher_governance_contract.py",
}

B4R4_BASELINE_PATHS = tuple(B4R4_ROUTE_PATHS.values())

S5_ALLOWLIST = (
    "AGENTS.md",
    ".codex/agents/planner.toml",
    ".codex/agents/implementer.toml",
    ".codex/agents/reviewer.toml",
    ".agents/skills/plan-creator/SKILL.md",
    ".agents/skills/plan-creator/checklist.md",
    ".agents/skills/plan-creator/templates/topic-plan-template.md",
    ".agents/skills/plan-reviewer/SKILL.md",
    ".agents/skills/plan-reviewer/checklist.md",
    ".agents/skills/plan-reviewer/reference.md",
    ".agents/skills/plan-reviewer/examples.md",
    ".agents/skills/python-implementation-workflow/SKILL.md",
    ".agents/skills/python-implementation-workflow/reference.md",
    ".agents/skills/python-plan-authoring/templates/canonical-python-topic-plan-template.md",
    "tests/test_observer_dispatcher_governance_contract.py",
)

B4R4_EVIDENCE_PATHS = (
    "plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r4-tester-evidence.md",
    "plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r4-implementation-review-log.md",
)

FROZEN_B4R4_EPOCHS = (
    "B0",
    "B1",
    "B2",
    "B3",
    "B4",
    "B4R",
    "B4R2",
    "B4R3",
    "S1",
    "S2",
    "S3",
    "S4",
    "T1",
    "T2",
    "T3",
    "T4",
    "V1",
    "V2",
    "V3",
    "V4",
)


def read(path: str) -> str:
    """Read one declared repository contract surface."""
    return (ROOT / path).read_text(encoding="utf-8")


def read_b4r4_route() -> dict[str, str]:
    """Read the eight B4R4 baseline surfaces used by the S5 conformance gate."""
    return {name: read(path) for name, path in B4R4_ROUTE_PATHS.items()}


def assert_b4r4_s5_route_is_fail_closed(route: dict[str, str]) -> None:
    """Reject a reopened epoch, non-subject baseline, or non-linear S5 evidence route."""
    assert tuple(route) == tuple(B4R4_ROUTE_PATHS)
    assert tuple(B4R4_ROUTE_PATHS.values()) == B4R4_BASELINE_PATHS

    authority = "".join(route.values())
    for epoch in FROZEN_B4R4_EPOCHS:
        assert epoch in authority
    assert "8b87aab" in authority
    assert "frozen nonrouting" in authority
    assert "normal/recovery" in authority
    assert "step-creator" in authority
    assert "deferred" in authority
    assert (
        "B4R3 and its failed clean-checkout review are frozen nonrouting provenance."
        in route["b4r4_plan"]
    )
    assert "The two\n`step-creator` threads remain deferred." in route["b4r4_plan"]

    baseline_contract = route["topic_contract"] + route["parent_plan"] + route["b4r4_plan"]
    assert all(path in baseline_contract for path in B4R4_BASELINE_PATHS)
    assert "exactly these eight paths" in route["topic_contract"]
    assert "reviews all eight actual B4R4 blobs from clean checkout" in route["b4r4_plan"]
    assert "B4R4 is non-subject." in route["b4r4_plan"]
    assert "B4R4 commit can\nestablish `implementation_subject_sha`." in route["topic_contract"]

    subject_contract = route["topic_contract"] + route["parent_plan"] + route["parent_spec"]
    assert "S5 alone\nestablishes `implementation_subject_sha`" in subject_contract
    assert (
        "Only the separately committed approved B4R4 review record permits one non-merge `S5`."
        in (route["topic_contract"])
    )
    assert all(path in route["parent_plan"] for path in S5_ALLOWLIST)
    assert "import" + "lib" in authority
    assert "__" + "import__" in authority
    assert "sys." + "modules" in authority

    topology = route["workflow"] + route["topic_contract"] + route["b4r4_plan"] + route["b4r4_step"]
    assert "S5 -> T5 -> V5" in topology
    assert "non-merge" in topology
    assert "S5..V5" in topology
    assert "HEAD" in topology
    assert "third descendant" in topology
    assert all(path in topology for path in B4R4_EVIDENCE_PATHS)
    assert (
        "Actual named SHA graph queries must prove linear non-merge `S5 -> T5 -> V5`."
        in (route["b4r4_plan"])
    )
    assert "exact `S5..V5` evidence range" in route["b4r4_plan"]


def assert_direct_import_behavior(source: str) -> None:
    """Keep this conformance test free of dynamic-import substitutions."""
    for forbidden in ("import" + "lib", "__" + "import__", "sys." + "modules"):
        assert forbidden not in source


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


def test_b4r4_route_freezes_prior_epochs_and_resets_the_subject_at_s5() -> None:
    """Require B4R4 to stay a baseline while S5 is the sole future subject."""
    assert_b4r4_s5_route_is_fail_closed(read_b4r4_route())


@pytest.mark.parametrize(
    ("source", "required_text", "replacement"),
    [
        (
            "b4r4_plan",
            "B4R3 and its failed clean-checkout review are frozen nonrouting provenance.",
            "B4R3 is current routing.",
        ),
        (
            "b4r4_plan",
            "B4R4 is non-subject.",
            "B4R4 establishes the implementation subject.",
        ),
        (
            "topic_contract",
            "exactly these eight paths",
            "one extra baseline path is allowed",
        ),
        (
            "b4r4_plan",
            "reviews all eight actual B4R4 blobs from clean checkout",
            "reviews only seven B4R4 blobs",
        ),
        (
            "topic_contract",
            "S5 alone\nestablishes `implementation_subject_sha`",
            "B4R4\nestablishes `implementation_subject_sha`",
        ),
        (
            "parent_plan",
            ".codex/agents/reviewer.toml",
            ".codex/agents/extra.toml",
        ),
        (
            "b4r4_plan",
            "The two\n`step-creator` threads remain deferred.",
            "The two\n`step-creator` threads are current work.",
        ),
        (
            "b4r4_plan",
            "Actual named SHA graph queries must prove linear non-merge `S5 -> T5 -> V5`.",
            "Actual named SHA graph queries must prove linear non-merge `S5 -> T5 -> V5 -> X5`.",
        ),
        (
            "b4r4_plan",
            "exact `S5..V5` evidence range",
            "`S5..HEAD` evidence range",
        ),
    ],
)
def test_b4r4_s5_route_rejects_all_route_and_subject_mutations(
    source: str,
    required_text: str,
    replacement: str,
) -> None:
    """Make frozen, baseline, subject, allowlist, and graph mutations fail closed."""
    mutated_route = read_b4r4_route()
    assert required_text in mutated_route[source]
    mutated_route[source] = mutated_route[source].replace(required_text, replacement, 1)

    with pytest.raises(AssertionError):
        assert_b4r4_s5_route_is_fail_closed(mutated_route)


def test_b4r4_contract_test_preserves_direct_import_behavior() -> None:
    """Keep this conformance test free of dynamic-import substitutions."""
    source = read("tests/test_observer_dispatcher_governance_contract.py")
    assert_direct_import_behavior(source)


def test_s4_contract_test_rejects_dynamic_import_mutation() -> None:
    """Make a dynamic-import substitution fail closed instead of changing test behavior."""
    source = read("tests/test_observer_dispatcher_governance_contract.py")
    mutated_source = source + "\nimport " + "import" + "lib\n"

    with pytest.raises(AssertionError):
        assert_direct_import_behavior(mutated_source)
