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
Q14_REAL_COMMIT_REQUIRED = "named Q14 SHA must resolve to a real commit"

B6R8_BASELINE_PATHS = (
    "plan/agent-handoff-workflow.md",
    "plan/topic-plan-contract.md",
    "plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md",
    "plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md",
    "plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md",
    "plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r8-plan.md",
    "plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r8-step.md",
)
B6R8_REVIEW_PATH = (
    "plan/observer-dispatcher-governance/"
    "observer-dispatcher-governance.correction-b6r8-review-log.md"
)
B6R8_T14_PATH = (
    "plan/observer-dispatcher-governance/"
    "observer-dispatcher-governance.correction-b6r8-tester-evidence.md"
)
B6R8_V14_PATH = (
    "plan/observer-dispatcher-governance/"
    "observer-dispatcher-governance.correction-b6r8-implementation-review-log.md"
)
B6R8_EVIDENCE_PATHS = (B6R8_T14_PATH, B6R8_V14_PATH)
B6R7_REVIEW_PATH = (
    "plan/observer-dispatcher-governance/"
    "observer-dispatcher-governance.correction-b6r7-review-log.md"
)
B6R7_BASELINE_SHA = "03d90755b378063a312e62f9eefbe31caa081981"
R17_RECEIPT_SHA = "a7770348222049f1c8bb6a0ee67e3136f2f47c3f"
S14_ENV_KEYS = ("ODG_S14_SHA", "ODG_T14_SHA", "ODG_V14_SHA")

CURRENT_ROUTE_PATHS = {
    "workflow": "plan/agent-handoff-workflow.md",
    "topic_contract": "plan/topic-plan-contract.md",
    "parent_plan": "plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md",
    "parent_spec": "plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md",
    "parent_step": "plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md",
    "b6r8_plan": (
        "plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r8-plan.md"
    ),
    "b6r8_step": (
        "plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r8-step.md"
    ),
}
JsonObject = dict[str, Any]
RecordMutation = Callable[[JsonObject], None]


@dataclass(frozen=True)
class EvidenceGraph:
    """Named post-V14 values required for the actual Q14 Git gate."""

    s14_sha: str
    s14_parents: tuple[str, ...]
    t14_sha: str
    t14_parents: tuple[str, ...]
    v14_sha: str
    v14_parents: tuple[str, ...]
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
    """Read only the B6R8 current authority surfaces."""
    return {name: read(path) for name, path in CURRENT_ROUTE_PATHS.items()}


def numbered_paths(content: str, start: str, end: str) -> tuple[str, ...]:
    """Extract one bounded numbered exact-path list without broad text matching."""
    block = content.split(start, 1)[1].split(end, 1)[0]
    paths: list[str] = []
    for line in block.splitlines():
        match = re.match(r"\d+\. `([^`]+)`$", line.strip())
        if match is not None:
            paths.append(match.group(1))
    return tuple(paths)


def assert_direct_import_behavior(source: str) -> None:
    """Keep this conformance test free of dynamic-import substitutions."""
    for forbidden in ("import" + "lib", "__" + "import__", "sys." + "modules"):
        assert forbidden not in source


def assert_b6r8_r18_schema(record: object) -> None:
    """Reject an incomplete, widened, or substituted committed R18 review."""
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
        "predecessor_receipt_verification",
        "next_phase",
        "effective_committed_state",
        "review_basis",
        "copilot_feedback_triage",
        "verdict",
        "blocking_issues",
        "timestamp",
    }
    assert payload["schema_version"] == (
        "observer-dispatcher-governance.correction-b6r8-plan-review.v1"
    )
    assert payload["correction_id"] == "observer-dispatcher-governance/high/b6r8"
    assert payload["review_kind"] == "correction-b6r8-plan"
    assert payload["next_phase"] == "S14"
    assert payload["effective_committed_state"] == "R17_COMPLETE_S14_NEXT"
    assert payload["verdict"] == "approved"
    assert payload["blocking_issues"] == []
    assert payload["copilot_feedback_triage"] == {"ADDRESS": [], "DISCUSS": [], "SKIP": []}
    for key in ("reviewed_commit_sha", "reviewed_tree_sha"):
        assert isinstance(payload[key], str)
        assert SHA_PATTERN.fullmatch(payload[key])

    artifacts = cast("list[JsonObject]", payload["reviewed_artifacts"])
    assert tuple(artifact.get("path") for artifact in artifacts) == B6R8_BASELINE_PATHS
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

    receipt = cast("JsonObject", payload["predecessor_receipt_verification"])
    assert receipt == {
        "review_log_path": B6R7_REVIEW_PATH,
        "reviewed_commit_sha": B6R7_BASELINE_SHA,
        "receipt_commit_sha": R17_RECEIPT_SHA,
        "verdict": "approved",
        "non_merge": True,
        "first_parent": True,
    }


def remove_next_phase(record: JsonObject) -> None:
    """Remove one required R18 schema key."""
    record.pop("next_phase")


def replace_effective_state(record: JsonObject) -> None:
    """Substitute an invalid effective state."""
    record["effective_committed_state"] = "R18_PENDING"


def remove_reviewed_artifact(record: JsonObject) -> None:
    """Remove one required reviewed-artifact entry."""
    artifacts = cast("list[JsonObject]", record["reviewed_artifacts"])
    artifacts.pop()


def replace_receipt_commit_sha(record: JsonObject) -> None:
    """Substitute an invalid predecessor receipt SHA."""
    receipt = cast("JsonObject", record["predecessor_receipt_verification"])
    receipt["receipt_commit_sha"] = "0" * 40


def replace_verdict(record: JsonObject) -> None:
    """Substitute an unapproved R18 verdict."""
    record["verdict"] = "needs-rework"


def assert_b6r8_route_is_fail_closed(route: Mapping[str, str]) -> None:
    """Reject stale routing, subject drift, or altered B6R8 topology."""
    assert tuple(route) == tuple(CURRENT_ROUTE_PATHS)
    authority = "".join(route.values())
    assert "B6R8 -> R18 -> S14 -> T14 -> V14 -> Q14" in route["workflow"]
    assert "sole current route" in authority
    assert "R18_REVIEW_PENDING" in authority
    assert "frozen nonrouting provenance" in authority
    assert "step-creator" in authority
    assert "deferred" in authority
    assert "S1\u2013S13" in authority
    assert B6R7_BASELINE_SHA in authority
    assert R17_RECEIPT_SHA in authority
    assert "B6R8/R18 are non-subject" in authority
    assert "S14 alone changes" in route["b6r8_plan"]
    assert "S14 -> T14 -> V14" in route["b6r8_plan"]
    assert "S14..V14" in authority
    assert "Q14" in authority
    assert "read-only" in authority
    assert "no artifact" in authority
    assert "no thread authority" in authority
    assert "addressed-and-resolvable" in authority
    assert all(path in authority for path in B6R8_EVIDENCE_PATHS)
    assert all(key in route["parent_spec"] for key in S14_ENV_KEYS)

    baseline_paths = numbered_paths(
        route["workflow"],
        "admission 的 named diff 必須恰好各一次\n包含以下七個 paths\uff1a",
        "R18 只在 committed B6R8 clean checkout",
    )
    assert baseline_paths == B6R8_BASELINE_PATHS
    assert "B6R8 admission is a non-merge first-parent exact-seven baseline" in route["b6r8_plan"]
    assert "B6R8/R18 never write\n`implementation_subject_sha`" in route["b6r8_plan"]
    assert "effective state `R17_COMPLETE_S14_NEXT`" in route["b6r8_plan"]
    assert "all earlier routes are frozen" in route["parent_spec"]


def explicit_s14_triple(environment: Mapping[str, str]) -> tuple[str, str, str] | None:
    """Return only a complete explicit triple; absence is the sole skip condition."""
    values = tuple(environment.get(key) for key in S14_ENV_KEYS)
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


def assert_named_s14_evidence_graph(graph: EvidenceGraph) -> None:
    """Validate named topology values without any inference from the checkout tip."""
    for sha in (graph.s14_sha, graph.t14_sha, graph.v14_sha):
        assert SHA_PATTERN.fullmatch(sha)
        assert sha != "HEAD"
    assert len({graph.s14_sha, graph.t14_sha, graph.v14_sha}) == EVIDENCE_GRAPH_SHA_COUNT
    assert len(graph.s14_parents) == len(graph.t14_parents) == len(graph.v14_parents) == 1
    assert graph.t14_parents == (graph.s14_sha,)
    assert graph.v14_parents == (graph.t14_sha,)
    assert graph.named_range == f"{graph.s14_sha}..{graph.v14_sha}"
    assert "HEAD" not in graph.named_range
    assert graph.range_paths == B6R8_EVIDENCE_PATHS


def assert_actual_s14_graph(s14_sha: str, t14_sha: str, v14_sha: str) -> None:
    """Use real Git objects for the post-V14 Q14 read-only actual proof."""
    for sha in (s14_sha, t14_sha, v14_sha):
        try:
            assert run_git("rev-parse", "--verify", f"{sha}^{{commit}}") == sha
        except subprocess.CalledProcessError as error:
            raise AssertionError(Q14_REAL_COMMIT_REQUIRED) from error

    graph = EvidenceGraph(
        s14_sha=s14_sha,
        s14_parents=(single_parent(s14_sha),),
        t14_sha=t14_sha,
        t14_parents=(single_parent(t14_sha),),
        v14_sha=v14_sha,
        v14_parents=(single_parent(v14_sha),),
        named_range=f"{s14_sha}..{v14_sha}",
        range_paths=tuple(
            line.split("\t", 1)[1]
            for line in run_git("diff", "--name-status", f"{s14_sha}..{v14_sha}").splitlines()
        ),
    )
    assert_named_s14_evidence_graph(graph)

    subject_lines = run_git("diff", "--name-status", f"{s14_sha}^..{s14_sha}").splitlines()
    assert subject_lines == [f"M\t{TEST_PATH}"]
    assert run_git("rev-list", "--reverse", graph.named_range).splitlines() == [t14_sha, v14_sha]
    assert run_git("diff", "--name-status", graph.named_range).splitlines() == [
        f"A\t{B6R8_T14_PATH}",
        f"A\t{B6R8_V14_PATH}",
    ]


def test_b6r8_route_uses_only_current_artifacts_and_s14_subject() -> None:
    """Require B6R8/R18 gates while S14 remains the sole implementation subject."""
    assert_b6r8_route_is_fail_closed(read_current_route())


def test_actual_b6r8_admission_and_r18_match_named_git_objects() -> None:
    """Check B6R8's committed seven-path baseline, blobs, and sole R18 evidence diff."""
    record = json.loads(read(B6R8_REVIEW_PATH))
    assert_b6r8_r18_schema(record)
    payload = cast("JsonObject", record)
    b6r8_sha = cast("str", payload["reviewed_commit_sha"])
    admission = cast("JsonObject", payload["first_parent_admission"])

    assert run_git("rev-parse", f"{b6r8_sha}^{{tree}}") == payload["reviewed_tree_sha"]
    assert single_parent(b6r8_sha) == admission["parent_sha"]
    observed_lines = run_git("diff", "--name-status", f"{b6r8_sha}^..{b6r8_sha}").splitlines()
    observed_name_status = [line.replace("\t", "\\t") for line in observed_lines]
    assert observed_name_status == admission["name_status"]
    observed_paths = tuple(line.split("\t", 1)[1] for line in observed_lines)
    assert len(observed_paths) == len(B6R8_BASELINE_PATHS)
    assert set(observed_paths) == set(B6R8_BASELINE_PATHS)
    for artifact in cast("list[JsonObject]", payload["reviewed_artifacts"]):
        path = cast("str", artifact["path"])
        assert run_git("rev-parse", f"{b6r8_sha}:{path}") == artifact["blob_sha"]

    r18_sha = run_git("log", "-1", "--format=%H", "--", B6R8_REVIEW_PATH)
    assert single_parent(r18_sha) == b6r8_sha
    assert run_git("diff", "--name-status", f"{b6r8_sha}..{r18_sha}").splitlines() == [
        f"A\t{B6R8_REVIEW_PATH}",
    ]
    assert single_parent(R17_RECEIPT_SHA) == B6R7_BASELINE_SHA


@pytest.mark.parametrize(
    ("source", "required_text", "replacement"),
    [
        ("workflow", "B6R8 -> R18 -> S14 -> T14 -> V14 -> Q14", "B6R7 -> R17 -> S13"),
        ("b6r8_plan", "S14 alone changes", "B6R8 alone changes"),
        ("b6r8_plan", "S14 -> T14 -> V14", "S14 -> V14 -> T14"),
        ("parent_spec", "ODG_T14_SHA", "ODG_T14_ALIAS"),
    ],
)
def test_b6r8_route_rejects_frozen_subject_and_topology_mutations(
    source: str,
    required_text: str,
    replacement: str,
) -> None:
    """Make current-route, subject, topology, and input substitutions fail closed."""
    route = read_current_route()
    assert required_text in route[source]
    route[source] = route[source].replace(required_text, replacement)
    with pytest.raises(AssertionError):
        assert_b6r8_route_is_fail_closed(route)


@pytest.mark.parametrize(
    "mutation",
    [
        remove_next_phase,
        replace_effective_state,
        remove_reviewed_artifact,
        replace_receipt_commit_sha,
        replace_verdict,
    ],
)
def test_r18_schema_rejects_structural_and_value_mutations(mutation: RecordMutation) -> None:
    """Reject missing R18 fields and substitutions in receipt or effective state."""
    record = cast("JsonObject", json.loads(read(B6R8_REVIEW_PATH)))
    mutation(record)
    with pytest.raises(AssertionError):
        assert_b6r8_r18_schema(record)


def test_named_s14_t14_v14_graph_rejects_head_merge_and_range_mutations() -> None:
    """Keep Q14's actual graph linear, named, and confined to two evidence paths."""
    s14_sha, t14_sha, v14_sha = "1" * 40, "2" * 40, "3" * 40
    graph = EvidenceGraph(
        s14_sha=s14_sha,
        s14_parents=("0" * 40,),
        t14_sha=t14_sha,
        t14_parents=(s14_sha,),
        v14_sha=v14_sha,
        v14_parents=(t14_sha,),
        named_range=f"{s14_sha}..{v14_sha}",
        range_paths=B6R8_EVIDENCE_PATHS,
    )
    assert_named_s14_evidence_graph(graph)
    for mutation in (
        {"t14_parents": (s14_sha, "4" * 40)},
        {"v14_parents": (s14_sha,)},
        {"named_range": f"{s14_sha}..HEAD"},
        {"range_paths": (*B6R8_EVIDENCE_PATHS, "plan/extra.md")},
    ):
        with pytest.raises(AssertionError):
            assert_named_s14_evidence_graph(replace(graph, **mutation))


def test_all_absent_s14_environment_is_an_explicit_skip_condition() -> None:
    """Allow no actual-Q14 graph claim until all three post-commit identities exist."""
    assert explicit_s14_triple({}) is None


@pytest.mark.parametrize(
    "environment",
    [
        {"ODG_S14_SHA": "1" * 40},
        {"ODG_S14_SHA": "1" * 40, "ODG_T14_SHA": "2" * 40},
        {"ODG_S14_SHA": "", "ODG_T14_SHA": "2" * 40, "ODG_V14_SHA": "3" * 40},
        {"ODG_S14_SHA": "HEAD", "ODG_T14_SHA": "2" * 40, "ODG_V14_SHA": "3" * 40},
        {"ODG_S14_SHA": "1" * 39, "ODG_T14_SHA": "2" * 40, "ODG_V14_SHA": "3" * 40},
        {"ODG_S14_SHA": "1" * 40, "ODG_T14_SHA": "1" * 40, "ODG_V14_SHA": "3" * 40},
    ],
)
def test_partial_or_invalid_s14_environment_fails_closed(environment: dict[str, str]) -> None:
    """Reject every supplied environment that is not a complete named triple."""
    with pytest.raises(AssertionError):
        explicit_s14_triple(environment)


def test_nonexistent_s14_triple_fails_closed() -> None:
    """Reject real-looking but nonexistent commits rather than treating them as unverified."""
    with pytest.raises(AssertionError):
        assert_actual_s14_graph("0" * 40, "1" * 40, "2" * 40)


def test_actual_s14_t14_v14_graph_requires_a_complete_real_triple() -> None:
    """Run Q14 only with explicit post-V14 SHAs; it writes no artifact or thread state."""
    triple = explicit_s14_triple(os.environ)
    if triple is None:
        pytest.skip("explicit skip/unverified: all ODG S14/T14/V14 SHAs are absent")
    assert_actual_s14_graph(*triple)


def test_b6r8_contract_test_preserves_direct_import_behavior() -> None:
    """Keep this conformance test free of dynamic-import substitutions."""
    assert_direct_import_behavior(read(TEST_PATH))


def test_contract_test_rejects_dynamic_import_mutation() -> None:
    """Make a dynamic-import substitution fail closed instead of replacing behavior."""
    mutated_source = read(TEST_PATH) + "\nimport " + "import" + "lib\n"
    with pytest.raises(AssertionError):
        assert_direct_import_behavior(mutated_source)
