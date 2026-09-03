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
EVIDENCE_GRAPH_SHA_COUNT = 3
SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")
Q15_REAL_COMMIT_REQUIRED = "named Q15 SHA must resolve to a real commit"

B6R9_BASELINE_PATHS = (
    "plan/agent-handoff-workflow.md",
    "plan/topic-plan-contract.md",
    "plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md",
    "plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md",
    "plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md",
    "plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r9-plan.md",
    "plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r9-step.md",
)
B6R9_REVIEW_PATH = (
    "plan/observer-dispatcher-governance/"
    "observer-dispatcher-governance.correction-b6r9-review-log.md"
)
B6R9_T15_PATH = (
    "plan/observer-dispatcher-governance/"
    "observer-dispatcher-governance.correction-b6r9-tester-evidence.md"
)
B6R9_V15_PATH = (
    "plan/observer-dispatcher-governance/"
    "observer-dispatcher-governance.correction-b6r9-implementation-review-log.md"
)
B6R9_EVIDENCE_PATHS = (B6R9_V15_PATH, B6R9_T15_PATH)
S15_ENV_KEYS = ("ODG_S15_SHA", "ODG_T15_SHA", "ODG_V15_SHA")

CURRENT_ROUTE_PATHS = {
    "workflow": "plan/agent-handoff-workflow.md",
    "topic_contract": "plan/topic-plan-contract.md",
    "parent_plan": "plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md",
    "parent_spec": "plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md",
    "parent_step": "plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md",
    "b6r9_plan": (
        "plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r9-plan.md"
    ),
    "b6r9_step": (
        "plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r9-step.md"
    ),
}
JsonObject = dict[str, Any]
RecordMutation = Callable[[JsonObject], None]


@dataclass(frozen=True)
class EvidenceGraph:
    """Named post-V15 values required for the actual Q15 Git gate."""

    s15_sha: str
    s15_parents: tuple[str, ...]
    t15_sha: str
    t15_parents: tuple[str, ...]
    v15_sha: str
    v15_parents: tuple[str, ...]
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


def read_current_route() -> dict[str, str]:
    """Read only the B6R9 current authority surfaces."""
    return {name: read(path) for name, path in CURRENT_ROUTE_PATHS.items()}


def numbered_paths(content: str, start: str, end: str) -> tuple[str, ...]:
    """Extract one bounded numbered exact-path list without broad text matching."""
    block = content.split(start, 1)[1].split(end, 1)[0]
    paths: list[str] = []
    for line in block.splitlines():
        match = re.match(r"\d+\. (?:`([^`]+)`|(.+))$", line.strip())
        if match is not None:
            paths.append(match.group(1) or match.group(2))
    return tuple(paths)


def assert_direct_import_behavior(source: str) -> None:
    """Keep this conformance test free of dynamic-import substitutions."""
    for forbidden in ("import" + "lib", "__" + "import__", "sys." + "modules"):
        assert forbidden not in source


def assert_b6r9_r19_schema(record: object) -> None:
    """Reject an incomplete, widened, or substituted committed R19 review."""
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
        "next_phase",
        "effective_committed_state",
        "review_basis",
        "copilot_feedback_triage",
        "verdict",
        "blocking_issues",
        "timestamp",
    }
    assert payload["schema_version"] == (
        "observer-dispatcher-governance.correction-b6r9-plan-review.v1"
    )
    assert payload["correction_id"] == "observer-dispatcher-governance/high/b6r9"
    assert payload["review_kind"] == "correction-b6r9-plan"
    assert payload["next_phase"] == "S15"
    assert payload["effective_committed_state"] == "R19_COMPLETE_S15_NEXT"
    assert payload["verdict"] == "approved"
    assert payload["blocking_issues"] == []
    assert payload["copilot_feedback_triage"] == {"ADDRESS": [], "DISCUSS": [], "SKIP": []}
    for key in ("reviewed_commit_sha", "reviewed_tree_sha"):
        assert isinstance(payload[key], str)
        assert SHA_PATTERN.fullmatch(payload[key])

    artifacts = cast("list[JsonObject]", payload["reviewed_artifacts"])
    assert tuple(artifact.get("path") for artifact in artifacts) == B6R9_BASELINE_PATHS
    for artifact in artifacts:
        assert set(artifact) == {"path", "blob_sha"}
        assert SHA_PATTERN.fullmatch(cast("str", artifact["blob_sha"]))

    admission = cast("JsonObject", payload["first_parent_admission"])
    assert set(admission) == {
        "commit_sha",
        "parent_sha",
        "non_merge",
        "exact_declared_paths",
        "name_status",
    }
    assert admission["commit_sha"] == payload["reviewed_commit_sha"]
    assert SHA_PATTERN.fullmatch(cast("str", admission["parent_sha"]))
    assert admission["non_merge"] is True
    assert admission["exact_declared_paths"] is True
    assert isinstance(admission["name_status"], list)


def remove_next_phase(record: JsonObject) -> None:
    """Remove one required R19 schema key."""
    record.pop("next_phase")


def replace_effective_state(record: JsonObject) -> None:
    """Substitute an invalid effective state."""
    record["effective_committed_state"] = "R19_PENDING"


def remove_reviewed_artifact(record: JsonObject) -> None:
    """Remove one required reviewed-artifact entry."""
    artifacts = cast("list[JsonObject]", record["reviewed_artifacts"])
    artifacts.pop()


def replace_verdict(record: JsonObject) -> None:
    """Substitute an unapproved R19 verdict."""
    record["verdict"] = "needs-rework"


def assert_b6r9_route_is_fail_closed(route: Mapping[str, str]) -> None:
    """Reject stale routing, subject drift, or altered B6R9 topology."""
    assert tuple(route) == tuple(CURRENT_ROUTE_PATHS)
    authority = "".join(route.values())
    assert "B6R9 -> R19 -> S15 -> T15 -> V15 -> Q15" in route["workflow"]
    assert "sole current route" in authority
    assert "R19_REVIEW_PENDING" in authority
    assert "frozen nonrouting provenance" in authority
    assert "step-creator" in authority
    assert "deferred" in authority
    assert "S1\u2013S14" in authority
    assert "B6R9/R19 are non-subject" in authority
    assert "S15 alone changes" in route["b6r9_plan"]
    assert "S15 -> T15 -> V15" in route["b6r9_plan"]
    assert "S15..V15" in authority
    assert "Q15" in authority
    assert "read-only" in authority
    assert "no artifact" in authority
    assert "no-thread-authority" in authority
    assert "addressed-and-resolvable" in authority
    assert all(path in authority for path in B6R9_EVIDENCE_PATHS)
    assert all(key in route["parent_spec"] for key in S15_ENV_KEYS)

    baseline_paths = numbered_paths(
        route["workflow"],
        "admission 的 named diff 必須恰好各一次包含以下\n七個 paths\uff1a",
        "R19 只在 committed B6R9 clean checkout",
    )
    assert baseline_paths == B6R9_BASELINE_PATHS
    assert "B6R9 admission is a non-merge first-parent exact-seven baseline" in route["b6r9_plan"]
    assert "B6R9/R19 never write implementation_subject_sha" in route["b6r9_plan"]
    assert "R19_COMPLETE_S15_NEXT" in route["b6r9_plan"]
    assert "all earlier routes are frozen" in route["parent_spec"]


def explicit_s15_triple(environment: Mapping[str, str]) -> tuple[str, str, str] | None:
    """Return only a complete explicit triple; absence is the sole skip condition."""
    values = tuple(environment.get(key) for key in S15_ENV_KEYS)
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


def assert_named_s15_evidence_graph(graph: EvidenceGraph) -> None:
    """Validate named topology values without any inference from the checkout tip."""
    for sha in (graph.s15_sha, graph.t15_sha, graph.v15_sha):
        assert SHA_PATTERN.fullmatch(sha)
        assert sha != "HEAD"
    assert len({graph.s15_sha, graph.t15_sha, graph.v15_sha}) == EVIDENCE_GRAPH_SHA_COUNT
    assert len(graph.s15_parents) == len(graph.t15_parents) == len(graph.v15_parents) == 1
    assert graph.t15_parents == (graph.s15_sha,)
    assert graph.v15_parents == (graph.t15_sha,)
    assert graph.named_range == f"{graph.s15_sha}..{graph.v15_sha}"
    assert "HEAD" not in graph.named_range
    assert graph.range_paths == B6R9_EVIDENCE_PATHS


def assert_actual_s15_graph(s15_sha: str, t15_sha: str, v15_sha: str) -> None:
    """Use real Git objects for the post-V15 Q15 read-only actual proof."""
    for sha in (s15_sha, t15_sha, v15_sha):
        try:
            assert run_git("rev-parse", "--verify", f"{sha}^{{commit}}") == sha
        except subprocess.CalledProcessError as error:
            raise AssertionError(Q15_REAL_COMMIT_REQUIRED) from error

    graph = EvidenceGraph(
        s15_sha=s15_sha,
        s15_parents=(single_parent(s15_sha),),
        t15_sha=t15_sha,
        t15_parents=(single_parent(t15_sha),),
        v15_sha=v15_sha,
        v15_parents=(single_parent(v15_sha),),
        named_range=f"{s15_sha}..{v15_sha}",
        range_paths=tuple(
            line.split("\t", 1)[1]
            for line in run_git("diff", "--name-status", f"{s15_sha}..{v15_sha}").splitlines()
        ),
    )
    assert_named_s15_evidence_graph(graph)

    subject_lines = run_git("diff", "--name-status", f"{s15_sha}^..{s15_sha}").splitlines()
    assert subject_lines == [f"M\t{TEST_PATH}"]
    assert run_git("rev-list", "--reverse", graph.named_range).splitlines() == [t15_sha, v15_sha]
    assert run_git("diff", "--name-status", graph.named_range).splitlines() == [
        f"A\t{B6R9_V15_PATH}",
        f"A\t{B6R9_T15_PATH}",
    ]


def test_b6r9_route_uses_only_current_artifacts_and_s15_subject() -> None:
    """Require B6R9/R19 gates while S15 remains the sole implementation subject."""
    assert_b6r9_route_is_fail_closed(read_current_route())


def test_actual_b6r9_admission_and_r19_match_named_git_objects() -> None:
    """Check B6R9's committed seven-path baseline, blobs, and sole R19 evidence diff."""
    record = json.loads(read(B6R9_REVIEW_PATH))
    assert_b6r9_r19_schema(record)
    payload = cast("JsonObject", record)
    b6r9_sha = cast("str", payload["reviewed_commit_sha"])
    admission = cast("JsonObject", payload["first_parent_admission"])

    assert run_git("rev-parse", f"{b6r9_sha}^{{tree}}") == payload["reviewed_tree_sha"]
    assert single_parent(b6r9_sha) == admission["parent_sha"]
    observed_lines = run_git("diff", "--name-status", f"{b6r9_sha}^..{b6r9_sha}").splitlines()
    assert observed_lines == admission["name_status"]
    observed_paths = tuple(line.split("\t", 1)[1] for line in observed_lines)
    assert len(observed_paths) == len(B6R9_BASELINE_PATHS)
    assert set(observed_paths) == set(B6R9_BASELINE_PATHS)
    for artifact in cast("list[JsonObject]", payload["reviewed_artifacts"]):
        path = cast("str", artifact["path"])
        assert run_git("rev-parse", f"{b6r9_sha}:{path}") == artifact["blob_sha"]

    r19_sha = run_git("log", "-1", "--format=%H", "--", B6R9_REVIEW_PATH)
    assert single_parent(r19_sha) == b6r9_sha
    assert run_git("diff", "--name-status", f"{b6r9_sha}..{r19_sha}").splitlines() == [
        f"A\t{B6R9_REVIEW_PATH}",
    ]


@pytest.mark.parametrize(
    ("source", "required_text", "replacement"),
    [
        ("workflow", "B6R9 -> R19 -> S15 -> T15 -> V15 -> Q15", "B6R8 -> R18 -> S14"),
        ("b6r9_plan", "S15 alone changes", "B6R9 alone changes"),
        ("b6r9_plan", "S15 -> T15 -> V15", "S15 -> V15 -> T15"),
        ("parent_spec", "ODG_T15_SHA", "ODG_T15_ALIAS"),
    ],
)
def test_b6r9_route_rejects_frozen_subject_and_topology_mutations(
    source: str,
    required_text: str,
    replacement: str,
) -> None:
    """Make current-route, subject, topology, and input substitutions fail closed."""
    route = read_current_route()
    assert required_text in route[source]
    route[source] = route[source].replace(required_text, replacement)
    with pytest.raises(AssertionError):
        assert_b6r9_route_is_fail_closed(route)


@pytest.mark.parametrize(
    "mutation",
    [
        remove_next_phase,
        replace_effective_state,
        remove_reviewed_artifact,
        replace_verdict,
    ],
)
def test_r19_schema_rejects_structural_and_value_mutations(mutation: RecordMutation) -> None:
    """Reject missing R19 fields and substitutions in effective state."""
    record = cast("JsonObject", json.loads(read(B6R9_REVIEW_PATH)))
    mutation(record)
    with pytest.raises(AssertionError):
        assert_b6r9_r19_schema(record)


def test_named_s15_t15_v15_graph_rejects_head_merge_and_range_mutations() -> None:
    """Keep Q15's actual graph linear, named, and confined to two evidence paths."""
    s15_sha, t15_sha, v15_sha = "1" * 40, "2" * 40, "3" * 40
    graph = EvidenceGraph(
        s15_sha=s15_sha,
        s15_parents=("0" * 40,),
        t15_sha=t15_sha,
        t15_parents=(s15_sha,),
        v15_sha=v15_sha,
        v15_parents=(t15_sha,),
        named_range=f"{s15_sha}..{v15_sha}",
        range_paths=B6R9_EVIDENCE_PATHS,
    )
    assert_named_s15_evidence_graph(graph)
    for mutation in (
        {"t15_parents": (s15_sha, "4" * 40)},
        {"v15_parents": (s15_sha,)},
        {"named_range": f"{s15_sha}..HEAD"},
        {"range_paths": (*B6R9_EVIDENCE_PATHS, "plan/extra.md")},
    ):
        with pytest.raises(AssertionError):
            assert_named_s15_evidence_graph(replace(graph, **mutation))


def test_all_absent_s15_environment_is_an_explicit_skip_condition() -> None:
    """Allow no actual-Q15 graph claim until all three post-commit identities exist."""
    assert explicit_s15_triple({}) is None


@pytest.mark.parametrize(
    "environment",
    [
        {"ODG_S15_SHA": "1" * 40},
        {"ODG_S15_SHA": "1" * 40, "ODG_T15_SHA": "2" * 40},
        {"ODG_S15_SHA": "", "ODG_T15_SHA": "2" * 40, "ODG_V15_SHA": "3" * 40},
        {"ODG_S15_SHA": "HEAD", "ODG_T15_SHA": "2" * 40, "ODG_V15_SHA": "3" * 40},
        {"ODG_S15_SHA": "1" * 39, "ODG_T15_SHA": "2" * 40, "ODG_V15_SHA": "3" * 40},
        {"ODG_S15_SHA": "1" * 40, "ODG_T15_SHA": "1" * 40, "ODG_V15_SHA": "3" * 40},
    ],
)
def test_partial_or_invalid_s15_environment_fails_closed(environment: dict[str, str]) -> None:
    """Reject every supplied environment that is not a complete named triple."""
    with pytest.raises(AssertionError):
        explicit_s15_triple(environment)


def test_nonexistent_s15_triple_fails_closed() -> None:
    """Reject real-looking but nonexistent commits rather than treating them as unverified."""
    with pytest.raises(AssertionError):
        assert_actual_s15_graph("0" * 40, "1" * 40, "2" * 40)


def test_actual_s15_t15_v15_graph_requires_a_complete_real_triple() -> None:
    """Run Q15 only with explicit post-V15 SHAs; it writes no artifact or thread state."""
    triple = explicit_s15_triple(os.environ)
    if triple is None:
        pytest.skip("explicit skip/unverified: all ODG S15/T15/V15 SHAs are absent")
    assert_actual_s15_graph(*triple)


def test_b6r9_contract_test_preserves_direct_import_behavior() -> None:
    """Keep this conformance test free of dynamic-import substitutions."""
    assert_direct_import_behavior(read(TEST_PATH))


def test_contract_test_rejects_dynamic_import_mutation() -> None:
    """Make a dynamic-import substitution fail closed instead of replacing behavior."""
    mutated_source = read(TEST_PATH) + "\nimport " + "import" + "lib\n"
    with pytest.raises(AssertionError):
        assert_direct_import_behavior(mutated_source)
