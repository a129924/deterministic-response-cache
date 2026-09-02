# Copyright (c) 2026 deterministic-response-cache contributors

"""Conformance checks for the current Observer / Dispatcher governance route."""

import json
import os
import re
import subprocess
from collections.abc import Callable, Mapping
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, cast

import pytest

ROOT = Path(__file__).resolve().parents[1]
TEST_PATH = "tests/test_observer_dispatcher_governance_contract.py"
COMMIT_AND_PARENT_SIZE = 2

S6_ALLOWLIST = (
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

CONTRACT_PATHS = S6_ALLOWLIST[:-1]

B4R7_BASELINE_PATHS = (
    "plan/agent-handoff-workflow.md",
    "plan/topic-plan-contract.md",
    "plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md",
    "plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md",
    "plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md",
    "plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r7-plan.md",
    "plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r7-step.md",
)

B4R7_R7_PATH = (
    "plan/observer-dispatcher-governance/"
    "observer-dispatcher-governance.correction-b4r7-review-log.md"
)

B4R7_EVIDENCE_PATHS = (
    (
        "plan/observer-dispatcher-governance/"
        "observer-dispatcher-governance.correction-b4r7-tester-evidence.md"
    ),
    (
        "plan/observer-dispatcher-governance/"
        "observer-dispatcher-governance.correction-b4r7-implementation-review-log.md"
    ),
)

B4R7_ROUTE_PATHS = {
    "workflow": "plan/agent-handoff-workflow.md",
    "topic_contract": "plan/topic-plan-contract.md",
    "parent_plan": "plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md",
    "parent_spec": "plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md",
    "parent_step": "plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md",
    "b4r7_plan": (
        "plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r7-plan.md"
    ),
    "b4r7_step": (
        "plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b4r7-step.md"
    ),
    "r7_review": B4R7_R7_PATH,
}

B6R4_BASELINE_PATHS = (
    "plan/agent-handoff-workflow.md",
    "plan/topic-plan-contract.md",
    "plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md",
    "plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md",
    "plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md",
    "plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r4-plan.md",
    "plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r4-step.md",
)
B6R4_REVIEW_PATH = (
    "plan/observer-dispatcher-governance/"
    "observer-dispatcher-governance.correction-b6r4-review-log.md"
)
B6R4_EVIDENCE_PATHS = (
    (
        "plan/observer-dispatcher-governance/"
        "observer-dispatcher-governance.correction-b6r4-tester-evidence.md"
    ),
    (
        "plan/observer-dispatcher-governance/"
        "observer-dispatcher-governance.correction-b6r4-implementation-review-log.md"
    ),
)
B6R4_ROUTE_PATHS = {
    "workflow": "plan/agent-handoff-workflow.md",
    "topic_contract": "plan/topic-plan-contract.md",
    "parent_plan": "plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md",
    "parent_spec": "plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md",
    "parent_step": "plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md",
    "b6r4_plan": (
        "plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r4-plan.md"
    ),
    "b6r4_step": (
        "plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r4-step.md"
    ),
    "r14_review": B6R4_REVIEW_PATH,
}
S12_ENV_KEYS = ("ODG_S12_SHA", "ODG_T12_SHA", "ODG_V12_SHA")

SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")
S6_ALLOWLIST_SIZE = 15
JsonObject = dict[str, Any]
RecordMutation = Callable[[JsonObject], None]


@dataclass(frozen=True)
class EvidenceGraph:
    """Named actual-query values required for the S6 evidence topology."""

    s6_sha: str
    s6_parents: tuple[str, ...]
    t6_sha: str
    t6_parents: tuple[str, ...]
    v6_sha: str
    v6_parents: tuple[str, ...]
    named_range: str
    range_paths: tuple[str, ...]


def read(path: str) -> str:
    """Read one declared repository contract surface."""
    return (ROOT / path).read_text(encoding="utf-8")


def run_git(*args: str) -> str:
    """Run one named Git query against this repository."""
    result = subprocess.run(  # noqa: S603
        ["git", *args],  # noqa: S607
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def read_b4r7_route() -> dict[str, str]:
    """Read only the current B4R7 route and its approved R7 record."""
    return {name: read(path) for name, path in B4R7_ROUTE_PATHS.items()}


def numbered_paths(content: str, start: str, end: str) -> tuple[str, ...]:
    """Extract one bounded numbered exact-path list without broad text matching."""
    block = content.split(start, 1)[1].split(end, 1)[0]
    paths: list[str] = []
    for line in block.splitlines():
        match = re.match(r"\d+\. `([^`]+)`$", line.strip())
        if match is not None:
            paths.append(match.group(1))
    return tuple(paths)


def assert_b4r7_r7_schema(record: object) -> None:
    """Reject a structurally incomplete, widened, or substituted R7 review record."""
    assert isinstance(record, dict)
    payload = cast("JsonObject", record)
    assert set(payload) == {
        "schema_version",
        "correction_id",
        "review_kind",
        "severity",
        "reviewed_commit_sha",
        "reviewed_artifacts",
        "review_basis",
        "verdict",
        "blocking_issues",
        "copilot_feedback_triage",
        "timestamp",
    }
    assert (
        payload["schema_version"] == "observer-dispatcher-governance.correction-b4r7-plan-review.v1"
    )
    assert payload["correction_id"] == "observer-dispatcher-governance/high/b4r7"
    assert payload["review_kind"] == "correction-b4r7-plan"
    assert payload["severity"] == "high"
    assert payload["verdict"] == "approved"
    assert isinstance(payload["reviewed_commit_sha"], str)
    assert SHA_PATTERN.fullmatch(payload["reviewed_commit_sha"])
    assert isinstance(payload["reviewed_artifacts"], list)
    artifacts = cast("list[JsonObject]", payload["reviewed_artifacts"])
    assert len(artifacts) == len(B4R7_BASELINE_PATHS)

    reviewed_paths: list[str] = []
    for artifact in artifacts:
        assert set(artifact) == {"path", "blob_sha"}
        assert isinstance(artifact["path"], str)
        assert isinstance(artifact["blob_sha"], str)
        assert SHA_PATTERN.fullmatch(artifact["blob_sha"])
        reviewed_paths.append(artifact["path"])
    assert tuple(reviewed_paths) == B4R7_BASELINE_PATHS

    assert payload["blocking_issues"] == []
    assert payload["copilot_feedback_triage"] == {"ADDRESS": [], "DISCUSS": [], "SKIP": []}


def assert_named_s6_evidence_graph(graph: EvidenceGraph) -> None:
    """Validate actual-query shaped S6/T6/V6 values, never a HEAD-based inference."""
    for sha in (graph.s6_sha, graph.t6_sha, graph.v6_sha):
        assert SHA_PATTERN.fullmatch(sha)
    assert graph.s6_sha not in {graph.t6_sha, graph.v6_sha}
    assert graph.t6_sha != graph.v6_sha
    assert len(graph.s6_parents) == len(graph.t6_parents) == len(graph.v6_parents) == 1
    assert graph.t6_parents == (graph.s6_sha,)
    assert graph.v6_parents == (graph.t6_sha,)
    assert graph.named_range == f"{graph.s6_sha}..{graph.v6_sha}"
    assert "HEAD" not in graph.named_range
    assert graph.range_paths == B4R7_EVIDENCE_PATHS


def assert_b4r7_s6_route_is_fail_closed(route: dict[str, str]) -> None:
    """Reject stale routing, altered admission, subject drift, and deferred-work activation."""
    assert tuple(route) == tuple(B4R7_ROUTE_PATHS)
    assert "b4r4_plan" not in route
    assert "b4r6_plan" not in route

    authority = "".join(route.values())
    assert "B0" + "\u2013" + "B4R6" in authority
    assert "S1" + "\u2013" + "S5" in authority
    assert "T1" + "\u2013" + "T5" in authority
    assert "V1" + "\u2013" + "V5" in authority
    for frozen_sha in ("b900366", "7d23e8c", "6ede06b"):
        assert frozen_sha in authority
    assert "frozen nonrouting provenance" in authority
    assert "normal/recovery" in authority
    assert "step-creator" in authority
    assert "deferred" in authority

    baseline_paths = numbered_paths(
        route["b4r7_plan"],
        "complete exact B4R7\nbaseline set:",
        "Commit admission is commit-time truth:",
    )
    assert baseline_paths == B4R7_BASELINE_PATHS
    assert "B4R7 is the\nsole current non-subject baseline." in route["b4r7_plan"]
    assert "B4R7 never establishes\n`implementation_subject_sha`." in route["b4r7_plan"]
    assert "exactly these seven paths" in route["topic_contract"]
    assert "actual seven blobs" in route["topic_contract"]

    assert_b4r7_r7_schema(json.loads(route["r7_review"]))
    assert (
        "Only the separately committed approved R7 record permits one non-merge `S6`."
        in route["topic_contract"]
    )
    assert "S6 alone establishes\n`implementation_subject_sha`" in route["topic_contract"]
    assert "B4R7 與 R7 都不能建立 `implementation_subject_sha`。" in route["parent_plan"]
    assert "step-creator` threads 持續 deferred" in route["parent_plan"]

    allowlist = numbered_paths(
        route["parent_plan"],
        "After separately committed approved R7 review, S6 may modify exactly:",
        "## Implementation Steps",
    )
    assert allowlist == S6_ALLOWLIST

    topology = route["workflow"] + route["topic_contract"] + route["parent_plan"]
    assert "S6 -> T6 -> V6" in topology
    assert "S6..V6" in topology
    assert "`git diff --name-status S6..V6`" in route["topic_contract"]
    assert "S6..HEAD" not in route["topic_contract"]
    assert "non-merge" in topology
    assert "third descendant" in topology
    assert "HEAD" in topology
    assert all(path in topology for path in B4R7_EVIDENCE_PATHS)
    assert (
        "candidate selector 只讀 parent plan、parent step 與 B4R7 R7 review evidence"
        in route["workflow"]
    )


def assert_direct_import_behavior(source: str) -> None:
    """Keep this conformance test free of dynamic-import substitutions."""
    for forbidden in ("import" + "lib", "__" + "import__", "sys." + "modules"):
        assert forbidden not in source


def read_b6r4_route() -> dict[str, str]:
    """Read only the current B6R4 route and its approved R14 record."""
    return {name: read(path) for name, path in B6R4_ROUTE_PATHS.items()}


def assert_b6r4_r14_schema(record: object) -> None:
    """Reject an incomplete, widened, or substituted committed R14 review."""
    assert isinstance(record, dict)
    payload = cast("JsonObject", record)
    assert set(payload) == {
        "schema_version",
        "correction_id",
        "review_kind",
        "reviewed_commit_sha",
        "reviewed_tree_sha",
        "reviewed_artifacts",
        "first_parent_admission",
        "review_basis",
        "verdict",
        "blocking_issues",
        "copilot_feedback_triage",
        "timestamp",
    }
    assert (
        payload["schema_version"] == "observer-dispatcher-governance.correction-b6r4-plan-review.v1"
    )
    assert payload["correction_id"] == "observer-dispatcher-governance/high/b6r4"
    assert payload["review_kind"] == "correction-b6r4-plan-review"
    assert payload["verdict"] == "approved"
    assert payload["blocking_issues"] == []
    assert payload["copilot_feedback_triage"] == {"ADDRESS": [], "DISCUSS": [], "SKIP": []}
    for key in ("reviewed_commit_sha", "reviewed_tree_sha"):
        assert isinstance(payload[key], str)
        assert SHA_PATTERN.fullmatch(payload[key])

    artifacts = cast("list[JsonObject]", payload["reviewed_artifacts"])
    assert tuple(artifact.get("path") for artifact in artifacts) == B6R4_BASELINE_PATHS
    for artifact in artifacts:
        assert set(artifact) == {"path", "blob_sha"}
        assert SHA_PATTERN.fullmatch(cast("str", artifact["blob_sha"]))

    admission = cast("JsonObject", payload["first_parent_admission"])
    assert set(admission) == {
        "candidate_parent_sha",
        "observed_parent_sha",
        "non_merge",
        "exact_declared_paths",
        "name_status",
    }
    assert admission["candidate_parent_sha"] == admission["observed_parent_sha"]
    assert SHA_PATTERN.fullmatch(cast("str", admission["candidate_parent_sha"]))
    assert admission["non_merge"] is True
    assert admission["exact_declared_paths"] is True
    assert isinstance(admission["name_status"], str)


def assert_b6r4_route_is_fail_closed(route: Mapping[str, str]) -> None:
    """Reject frozen-route activation, subject drift, or topology substitution."""
    assert tuple(route) == tuple(B6R4_ROUTE_PATHS)
    authority = "".join(route.values())
    assert "B6R4 -> R14 -> S12 -> T12 -> V12 -> Q12" in authority
    assert "sole current route" in authority
    assert "frozen nonrouting provenance" in authority
    assert "normal/recovery" in authority
    assert "step-creator" in authority
    assert "deferred" in authority
    for frozen_marker in (
        "b900366",
        "B0" + "\u2013" + "B6",
        "S1" + "\u2013" + "S10",
        "T1" + "\u2013" + "T10",
        "V1" + "\u2013" + "V10",
        "Q7" + "\u2013" + "Q11",
    ):
        assert frozen_marker in authority

    baseline_paths = numbered_paths(
        route["b6r4_plan"],
        "The B6R4 admission changed exactly once each:",
        "Before admission",
    )
    assert baseline_paths == B6R4_BASELINE_PATHS
    assert "B6R4 -> R14 -> S12 -> T12 -> V12 -> Q12" in route["b6r4_plan"]
    assert "frozen nonrouting provenance" in route["b6r4_plan"]
    assert "B6R4 is a non-subject" in route["b6r4_plan"]
    assert "neither B6R4 nor R14 creates `implementation_subject_sha`" in route["b6r4_plan"]
    assert "S12 is one non-merge subject modifying only" in route["b6r4_plan"]
    assert TEST_PATH in route["b6r4_plan"]
    assert "complete explicit" in route["b6r4_plan"]
    assert all(key in route["parent_spec"] for key in S12_ENV_KEYS)
    assert "S12 -> T12 -> V12" in route["b6r4_plan"]
    assert "S12..V12" in route["b6r4_plan"]
    assert all(path in authority for path in B6R4_EVIDENCE_PATHS)
    assert "read-only" in authority
    assert "addressed-and-resolvable" in authority
    assert_b6r4_r14_schema(json.loads(route["r14_review"]))


def explicit_s12_triple(environment: Mapping[str, str]) -> tuple[str, str, str] | None:
    """Return only a complete explicit triple; absence is the sole skip condition."""
    values = tuple(environment.get(key) for key in S12_ENV_KEYS)
    if all(value is None for value in values):
        return None
    assert all(value is not None for value in values)
    triple = cast("tuple[str, str, str]", values)
    for value in triple:
        assert SHA_PATTERN.fullmatch(value)
        assert value != "HEAD"
    assert len(set(triple)) == len(triple)
    return triple


def single_parent(sha: str) -> str:
    """Resolve exactly one real commit parent and reject root or merge commits."""
    parents = run_git("rev-list", "--parents", "-n", "1", sha).split()
    assert parents[0] == sha
    assert len(parents) == COMMIT_AND_PARENT_SIZE
    return parents[1]


def assert_actual_s12_graph(s12_sha: str, t12_sha: str, v12_sha: str) -> None:
    """Use real Git objects to prove the complete S12/T12/V12 contract."""
    for sha in (s12_sha, t12_sha, v12_sha):
        assert run_git("rev-parse", "--verify", f"{sha}^{{commit}}") == sha
    assert single_parent(t12_sha) == s12_sha
    assert single_parent(v12_sha) == t12_sha
    single_parent(s12_sha)

    subject_lines = run_git("diff", "--name-status", f"{s12_sha}^..{s12_sha}").splitlines()
    assert len(subject_lines) == 1
    assert tuple(line.split("\t", 1)[1] for line in subject_lines) == (TEST_PATH,)

    named_range = f"{s12_sha}..{v12_sha}"
    assert "HEAD" not in named_range
    assert run_git("rev-list", "--reverse", named_range).splitlines() == [t12_sha, v12_sha]
    assert run_git("diff", "--name-status", named_range).splitlines() == [
        f"A\t{B6R4_EVIDENCE_PATHS[0]}",
        f"A\t{B6R4_EVIDENCE_PATHS[1]}",
    ]


@pytest.fixture(scope="module")
def surfaces() -> dict[str, str]:
    """Provide the declared S6-governed surfaces without replacing their imports."""
    return {
        "governance": read("AGENTS.md"),
        "planner": read(".codex/agents/planner.toml"),
        "implementer": read(".codex/agents/implementer.toml"),
        "reviewer_config": read(".codex/agents/reviewer.toml"),
        "creator": read(".agents/skills/plan-creator/SKILL.md"),
        "creator_checklist": read(".agents/skills/plan-creator/checklist.md"),
        "creator_template": read(".agents/skills/plan-creator/templates/topic-plan-template.md"),
        "reviewer": read(".agents/skills/plan-reviewer/SKILL.md"),
        "reviewer_checklist": read(".agents/skills/plan-reviewer/checklist.md"),
        "reviewer_reference": read(".agents/skills/plan-reviewer/reference.md"),
        "reviewer_examples": read(".agents/skills/plan-reviewer/examples.md"),
        "python_workflow": read(".agents/skills/python-implementation-workflow/SKILL.md"),
        "python_workflow_reference": read(
            ".agents/skills/python-implementation-workflow/reference.md",
        ),
        "python_template": read(
            ".agents/skills/python-plan-authoring/templates/canonical-python-topic-plan-template.md",
        ),
    }


def test_all_declared_s6_contract_surfaces_are_repo_visible() -> None:
    """Keep every declared non-test S6 surface at its exact path."""
    assert len(S6_ALLOWLIST) == S6_ALLOWLIST_SIZE
    assert len(set(S6_ALLOWLIST)) == S6_ALLOWLIST_SIZE
    assert all((ROOT / path).is_file() for path in CONTRACT_PATHS)


def test_role_configs_and_wrappers_keep_the_locked_boundaries(surfaces: dict[str, str]) -> None:
    """Keep Planner routing, bounded implementer work, review, and wrappers distinct."""
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
    assert "never authorizes merge" in surfaces["implementer"]
    assert (
        "Do not create commits, push branches, or open pull requests" in surfaces["reviewer_config"]
    )
    assert "wrapper recipe" in surfaces["python_workflow"]
    assert "不會建立對 legacy" in surfaces["python_workflow"]
    assert "must not require the legacy file at runtime" in surfaces["python_workflow_reference"]


def test_b6r4_route_uses_only_current_artifacts_and_s12_subject() -> None:
    """Require B6R4/R14 gates while S12 is the only implementation subject."""
    assert_b6r4_route_is_fail_closed(read_b6r4_route())


def test_actual_b4r7_admission_and_r7_review_match_their_named_git_objects() -> None:
    """Check current B4R7 admission and R7 against named commits, paths, and blobs."""
    record = json.loads(read(B4R7_R7_PATH))
    assert_b4r7_r7_schema(record)
    b4r7_sha = record["reviewed_commit_sha"]
    assert isinstance(b4r7_sha, str)
    assert run_git("rev-list", "--parents", "-n", "1", b4r7_sha).split() == [
        b4r7_sha,
        run_git("rev-parse", f"{b4r7_sha}^"),
    ]

    diff_lines = run_git("diff", "--name-status", f"{b4r7_sha}^..{b4r7_sha}").splitlines()
    admission_paths = tuple(line.split("\t", 1)[1] for line in diff_lines)
    assert len(admission_paths) == len(B4R7_BASELINE_PATHS)
    assert set(admission_paths) == set(B4R7_BASELINE_PATHS)
    assert all(line.split("\t", 1)[0] in {"A", "M"} for line in diff_lines)
    for artifact in record["reviewed_artifacts"]:
        assert isinstance(artifact, dict)
        assert run_git("rev-parse", f"{b4r7_sha}:{artifact['path']}") == artifact["blob_sha"]

    r7_sha = run_git("log", "-1", "--format=%H", "--", B4R7_R7_PATH)
    assert run_git("rev-parse", f"{r7_sha}^") == b4r7_sha
    assert run_git("diff", "--name-status", f"{b4r7_sha}..{r7_sha}").splitlines() == [
        f"A\t{B4R7_R7_PATH}",
    ]


@pytest.mark.parametrize(
    ("source", "required_text", "replacement"),
    [
        ("b6r4_plan", "frozen nonrouting provenance", "current routing provenance"),
        ("b6r4_plan", "B6R4 is a non-subject", "B6R4 is the subject"),
        (
            "b6r4_plan",
            "B6R4 -> R14 -> S12 -> T12 -> V12 -> Q12",
            "B6R4 -> R14 -> S12 -> V12 -> T12 -> Q12",
        ),
        ("parent_spec", "ODG_T12_SHA", "ODG_T12_ALIAS"),
    ],
)
def test_b6r4_route_rejects_frozen_subject_and_topology_mutations(
    source: str,
    required_text: str,
    replacement: str,
) -> None:
    """Make required provenance, subject, and topology removals fail closed."""
    route = read_b6r4_route()
    assert required_text in route[source]
    route[source] = route[source].replace(required_text, replacement)
    with pytest.raises(AssertionError):
        assert_b6r4_route_is_fail_closed(route)


def remove_review_kind(record: JsonObject) -> None:
    """Remove one required R7 schema field."""
    record.pop("review_kind")


def replace_schema_version(record: JsonObject) -> None:
    """Substitute the locked R7 schema identifier."""
    record["schema_version"] = "wrong.schema.v1"


def remove_reviewed_artifact(record: JsonObject) -> None:
    """Remove one required reviewed B4R7 artifact."""
    artifacts = cast("list[JsonObject]", record["reviewed_artifacts"])
    artifacts.pop()


def replace_reviewed_artifact_path(record: JsonObject) -> None:
    """Substitute an undeclared reviewed artifact path."""
    artifacts = cast("list[JsonObject]", record["reviewed_artifacts"])
    artifacts[0]["path"] = "plan/unlisted.md"


def replace_r7_verdict(record: JsonObject) -> None:
    """Replace the required approved R7 verdict."""
    record["verdict"] = "needs-rework"


@pytest.mark.parametrize(
    "mutation",
    [
        remove_review_kind,
        replace_schema_version,
        remove_reviewed_artifact,
        replace_reviewed_artifact_path,
        replace_r7_verdict,
    ],
)
def test_r7_schema_rejects_structural_and_value_mutations(mutation: RecordMutation) -> None:
    """Reject both missing R7 fields and value/path substitutions."""
    record = json.loads(read(B4R7_R7_PATH))
    mutation(record)
    with pytest.raises(AssertionError):
        assert_b4r7_r7_schema(record)


def test_named_s6_t6_v6_graph_rejects_head_merge_and_range_mutations() -> None:
    """Keep the actual-query graph contract linear and named rather than inferred."""
    s6_sha, t6_sha, v6_sha = "1" * 40, "2" * 40, "3" * 40
    graph = EvidenceGraph(
        s6_sha=s6_sha,
        s6_parents=("0" * 40,),
        t6_sha=t6_sha,
        t6_parents=(s6_sha,),
        v6_sha=v6_sha,
        v6_parents=(t6_sha,),
        named_range=f"{s6_sha}..{v6_sha}",
        range_paths=B4R7_EVIDENCE_PATHS,
    )
    assert_named_s6_evidence_graph(graph)
    for mutation in (
        {"t6_parents": (s6_sha, "4" * 40)},
        {"v6_parents": (s6_sha,)},
        {"named_range": f"{s6_sha}..HEAD"},
        {"range_paths": (*B4R7_EVIDENCE_PATHS, "plan/extra.md")},
    ):
        with pytest.raises(AssertionError):
            assert_named_s6_evidence_graph(replace(graph, **mutation))


def test_actual_b6r4_admission_and_r14_match_named_git_objects() -> None:
    """Check the committed B6R4 baseline, every blob, and R14's sole evidence diff."""
    record = json.loads(read(B6R4_REVIEW_PATH))
    assert_b6r4_r14_schema(record)
    b6r4_sha = cast("str", record["reviewed_commit_sha"])
    reviewed_tree_sha = cast("str", record["reviewed_tree_sha"])
    admission = cast("JsonObject", record["first_parent_admission"])

    assert run_git("rev-parse", f"{b6r4_sha}^{{tree}}") == reviewed_tree_sha
    assert single_parent(b6r4_sha) == admission["observed_parent_sha"]
    observed_lines = run_git("diff", "--name-status", f"{b6r4_sha}^..{b6r4_sha}").splitlines()
    observed_name_status = "\\n".join(line.replace("\t", "\\t") for line in observed_lines)
    assert observed_name_status == admission["name_status"]
    observed_paths = tuple(line.split("\t", 1)[1] for line in observed_lines)
    assert len(observed_paths) == len(B6R4_BASELINE_PATHS)
    assert set(observed_paths) == set(B6R4_BASELINE_PATHS)
    for artifact in cast("list[JsonObject]", record["reviewed_artifacts"]):
        path = cast("str", artifact["path"])
        assert run_git("rev-parse", f"{b6r4_sha}:{path}") == artifact["blob_sha"]

    r14_sha = run_git("log", "-1", "--format=%H", "--", B6R4_REVIEW_PATH)
    assert single_parent(r14_sha) == b6r4_sha
    assert run_git("diff", "--name-status", f"{b6r4_sha}..{r14_sha}").splitlines() == [
        f"A\t{B6R4_REVIEW_PATH}",
    ]


def test_all_absent_s12_environment_is_an_explicit_skip_condition() -> None:
    """Allow no graph claim until all three post-commit identities exist."""
    assert explicit_s12_triple({}) is None


@pytest.mark.parametrize(
    "environment",
    [
        {"ODG_S12_SHA": "1" * 40},
        {"ODG_S12_SHA": "1" * 40, "ODG_T12_SHA": "2" * 40},
        {"ODG_S12_SHA": "", "ODG_T12_SHA": "2" * 40, "ODG_V12_SHA": "3" * 40},
        {"ODG_S12_SHA": "HEAD", "ODG_T12_SHA": "2" * 40, "ODG_V12_SHA": "3" * 40},
        {"ODG_S12_SHA": "1" * 39, "ODG_T12_SHA": "2" * 40, "ODG_V12_SHA": "3" * 40},
        {"ODG_S12_SHA": "1" * 40, "ODG_T12_SHA": "1" * 40, "ODG_V12_SHA": "3" * 40},
    ],
)
def test_partial_or_invalid_s12_environment_fails_closed(environment: dict[str, str]) -> None:
    """Reject every supplied environment that is not a complete named triple."""
    with pytest.raises(AssertionError):
        explicit_s12_triple(environment)


def test_actual_s12_t12_v12_graph_requires_a_complete_real_triple() -> None:
    """Run the actual Git proof only with explicit complete post-commit SHAs."""
    triple = explicit_s12_triple(os.environ)
    if triple is None:
        pytest.skip("explicit skip/unverified: all ODG S12/T12/V12 SHAs are absent")
    assert_actual_s12_graph(*triple)


def test_b4r7_contract_test_preserves_direct_import_behavior() -> None:
    """Keep this conformance test free of dynamic-import substitutions."""
    assert_direct_import_behavior(read("tests/test_observer_dispatcher_governance_contract.py"))


def test_contract_test_rejects_dynamic_import_mutation() -> None:
    """Make a dynamic-import substitution fail closed instead of replacing test behavior."""
    mutated_source = (
        read("tests/test_observer_dispatcher_governance_contract.py")
        + "\nimport "
        + "import"
        + "lib\n"
    )
    with pytest.raises(AssertionError):
        assert_direct_import_behavior(mutated_source)
