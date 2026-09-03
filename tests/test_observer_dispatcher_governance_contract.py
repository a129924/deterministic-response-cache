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
SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")
COMMIT_AND_PARENT_SIZE = 2
EVIDENCE_GRAPH_SHA_COUNT = 3
Q16_REAL_COMMIT_REQUIRED = "named Q16 SHA must resolve to a real commit"

B6R12_BASELINE_PATHS = (
    "plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r12-plan.md",
    "plan/observer-dispatcher-governance/observer-dispatcher-governance.correction-b6r12-step.md",
    "plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md",
    "plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md",
    "plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md",
)
B6R12_NAME_STATUS = (
    f"A\t{B6R12_BASELINE_PATHS[0]}",
    f"A\t{B6R12_BASELINE_PATHS[1]}",
    f"M\t{B6R12_BASELINE_PATHS[2]}",
    f"M\t{B6R12_BASELINE_PATHS[3]}",
    f"M\t{B6R12_BASELINE_PATHS[4]}",
)
R22_REVIEW_PATH = (
    "plan/observer-dispatcher-governance/"
    "observer-dispatcher-governance.correction-b6r12-review-log.md"
)
T16_EVIDENCE_PATH = (
    "plan/observer-dispatcher-governance/"
    "observer-dispatcher-governance.correction-b6r10-tester-evidence.md"
)
V16_EVIDENCE_PATH = (
    "plan/observer-dispatcher-governance/"
    "observer-dispatcher-governance.correction-b6r10-implementation-review-log.md"
)
S16_ENV_KEYS = ("ODG_S16_SHA", "ODG_T16_SHA", "ODG_V16_SHA")

CURRENT_ROUTE_PATHS = {
    "parent_plan": "plan/observer-dispatcher-governance/observer-dispatcher-governance.plan.md",
    "parent_spec": "plan/observer-dispatcher-governance/observer-dispatcher-governance.spec.md",
    "parent_step": "plan/observer-dispatcher-governance/observer-dispatcher-governance.step.md",
    "b6r12_plan": (
        "plan/observer-dispatcher-governance/"
        "observer-dispatcher-governance.correction-b6r12-plan.md"
    ),
    "b6r12_step": (
        "plan/observer-dispatcher-governance/"
        "observer-dispatcher-governance.correction-b6r12-step.md"
    ),
}
RETAINED_DESCENDANT_PATHS = {
    "workflow": "plan/agent-handoff-workflow.md",
    "topic_contract": "plan/topic-plan-contract.md",
}
JsonObject = dict[str, Any]
RecordMutation = Callable[[JsonObject], None]


@dataclass(frozen=True)
class EvidenceGraph:
    """Named post-V16 identities required by the read-only Q16 gate."""

    s16_sha: str
    s16_parent: str
    t16_sha: str
    t16_parent: str
    v16_sha: str
    v16_parent: str
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
    """Read only the B6R12/R22 current routing surfaces."""
    return {name: read(path) for name, path in CURRENT_ROUTE_PATHS.items()}


def assert_direct_import_behavior(source: str) -> None:
    """Keep this conformance test free of dynamic-import substitutions."""
    for forbidden in ("import" + "lib", "__" + "import__", "sys." + "modules"):
        assert forbidden not in source


def assert_sha(value: object) -> str:
    """Return one full lowercase Git object identity or fail closed."""
    assert isinstance(value, str)
    assert SHA_PATTERN.fullmatch(value)
    return value


def json_object_at(commit_sha: str, path: str) -> JsonObject:
    """Load one committed evidence blob, never the working-tree version."""
    payload = json.loads(run_git("show", f"{commit_sha}:{path}"))
    assert isinstance(payload, dict)
    return cast("JsonObject", payload)


def single_parent(sha: str) -> str:
    """Resolve exactly one real commit parent and reject roots and merges."""
    parents = run_git("rev-list", "--parents", "-n", "1", sha).split()
    assert parents[0] == sha
    assert len(parents) == COMMIT_AND_PARENT_SIZE
    return parents[1]


def assert_b6r12_r22_schema(record: object) -> None:
    """Reject an incomplete, widened, or substituted approved R22 receipt."""
    assert isinstance(record, dict)
    payload = cast("JsonObject", record)
    assert set(payload) == {
        "schema_version",
        "correction_id",
        "review_kind",
        "candidate",
        "reviewed_artifacts",
        "first_parent_admission",
        "predecessor_receipt_verification",
        "review_basis",
        "copilot_feedback_triage",
        "verdict",
        "blocking_issues",
        "route_authorization",
        "timestamp",
    }
    assert (
        payload["schema_version"]
        == "observer-dispatcher-governance.correction-b6r12-plan-review.v1"
    )
    assert payload["correction_id"] == "observer-dispatcher-governance/high/b6r12"
    assert payload["review_kind"] == "correction-b6r12-routing-receipt"
    assert payload["review_basis"] == "independent clean checkout"
    assert payload["copilot_feedback_triage"] == {"ADDRESS": [], "DISCUSS": [], "SKIP": []}
    assert payload["verdict"] == "approved"
    assert payload["blocking_issues"] == []

    candidate = cast("JsonObject", payload["candidate"])
    assert set(candidate) == {"id", "commit_sha", "tree_sha", "active"}
    assert candidate["id"] == "observer-dispatcher-governance/high/b6r12"
    assert candidate["active"] is True
    assert_sha(candidate["commit_sha"])
    assert_sha(candidate["tree_sha"])

    artifacts = cast("list[JsonObject]", payload["reviewed_artifacts"])
    assert len(artifacts) == len(B6R12_BASELINE_PATHS)
    assert tuple(artifact.get("path") for artifact in artifacts) == B6R12_BASELINE_PATHS
    for artifact in artifacts:
        assert set(artifact) == {"path", "blob_sha"}
        assert_sha(artifact["blob_sha"])

    admission = cast("JsonObject", payload["first_parent_admission"])
    assert set(admission) == {
        "commit_sha",
        "tree_sha",
        "parent_sha",
        "non_merge",
        "exact_declared_paths",
        "name_status",
    }
    assert admission["commit_sha"] == candidate["commit_sha"]
    assert admission["tree_sha"] == candidate["tree_sha"]
    assert_sha(admission["parent_sha"])
    assert admission["non_merge"] is True
    assert admission["exact_declared_paths"] is True
    assert admission["name_status"] == list(B6R12_NAME_STATUS)
    assert payload["predecessor_receipt_verification"] == {
        "b6r11_admission": "995c5a8",
        "r21": "ABSENT_FROZEN_NONROUTING",
        "r20": "FROZEN_INVALID_NOT_ROUTING",
    }
    assert payload["route_authorization"] == {
        "effective_committed_state": "R22_COMPLETE_S16_NEXT",
        "next_phase": "S16",
        "implementation_subject_sha": None,
        "close_authorization": None,
    }


def assert_b6r12_admission_and_r22() -> None:
    """Verify the committed B6R12 exact-five baseline and sole R22 receipt."""
    record = cast("JsonObject", json.loads(read(R22_REVIEW_PATH)))
    assert_b6r12_r22_schema(record)
    candidate = cast("JsonObject", record["candidate"])
    admission = cast("JsonObject", record["first_parent_admission"])
    baseline_sha = cast("str", candidate["commit_sha"])
    assert run_git("rev-parse", f"{baseline_sha}^{{tree}}") == candidate["tree_sha"]
    assert single_parent(baseline_sha) == admission["parent_sha"]
    assert run_git(
        "diff",
        "--name-status",
        f"{baseline_sha}^..{baseline_sha}",
    ).splitlines() == list(B6R12_NAME_STATUS)
    for artifact in cast("list[JsonObject]", record["reviewed_artifacts"]):
        path = cast("str", artifact["path"])
        assert run_git("rev-parse", f"{baseline_sha}:{path}") == artifact["blob_sha"]
    r22_sha = run_git("log", "-1", "--format=%H", "--", R22_REVIEW_PATH)
    assert single_parent(r22_sha) == baseline_sha
    assert run_git("diff", "--name-status", f"{baseline_sha}..{r22_sha}").splitlines() == [
        f"A\t{R22_REVIEW_PATH}",
    ]


def assert_s16_route_is_fail_closed(route: Mapping[str, str]) -> None:
    """Require B6R12/R22 as the sole frozen predecessor to S16."""
    assert tuple(route) == tuple(CURRENT_ROUTE_PATHS)
    authority = "".join(route.values())
    assert "B6R12 -> R22 -> S16 -> T16 -> V16 -> Q16" in authority
    assert "B6R12 -> R22 -> S16 -> T16 -> V16 -> Q16" in route["parent_plan"]
    assert "sole current route" in authority or "only current route" in authority
    assert "R22_REVIEW_PENDING" in authority
    assert "R22_COMPLETE_S16_NEXT" in authority
    assert "S16 is the sole implementation subject" in authority
    assert "S16 retains direct imports" in route["b6r12_plan"]
    assert "Q16 actual full-triple" in route["b6r12_plan"]
    assert "R22_REVIEW_PENDING" in route["b6r12_step"]
    assert "B6R11/R21" in authority
    assert "B6R10/R20" in authority
    assert "FROZEN_INVALID_NOT_ROUTING" in authority
    assert "step-creator" in authority
    assert "deferred" in authority
    assert "thread resolve" in authority
    assert "merge" in authority
    assert all(path in authority for path in (T16_EVIDENCE_PATH, V16_EVIDENCE_PATH))
    retained = "".join(read(path) for path in RETAINED_DESCENDANT_PATHS.values())
    assert all(key in retained for key in S16_ENV_KEYS)
    assert "S16 is the sole non-merge test subject" in retained
    assert "T16 `passing`" in retained
    assert "V16 `APPROVED`" in retained
    assert "classification only" in retained or "classification-only" in retained


def explicit_s16_triple(environment: Mapping[str, str]) -> tuple[str, str, str] | None:
    """Return a full explicit triple; all absent is the sole permitted skip."""
    values = tuple(environment.get(key) for key in S16_ENV_KEYS)
    if all(value is None for value in values):
        return None
    assert all(value is not None for value in values)
    triple = cast("tuple[str, str, str]", values)
    for value in triple:
        assert_sha(value)
        assert value != "HEAD"
    assert len(set(triple)) == EVIDENCE_GRAPH_SHA_COUNT
    return triple


def assert_t16_schema(record: object, s16_sha: str) -> None:
    """Require the retained exact T16 JSON evidence semantics."""
    assert isinstance(record, dict)
    payload = cast("JsonObject", record)
    assert set(payload) == {
        "schema_version",
        "correction_id",
        "phase",
        "subject",
        "test_run",
        "timestamp",
    }
    assert (
        payload["schema_version"]
        == "observer-dispatcher-governance.correction-b6r10-tester-evidence.v1"
    )
    assert payload["correction_id"] == "observer-dispatcher-governance/high/b6r10"
    assert payload["phase"] == "T16"
    subject = cast("JsonObject", payload["subject"])
    assert set(subject) == {"phase", "commit_sha", "test_path"}
    assert subject == {"phase": "S16", "commit_sha": s16_sha, "test_path": TEST_PATH}
    test_run = cast("JsonObject", payload["test_run"])
    assert set(test_run) == {"command", "status", "exit_code"}
    assert isinstance(test_run["command"], str)
    assert test_run["command"]
    assert test_run["status"] == "passing"
    assert test_run["exit_code"] == 0


def assert_v16_schema(record: object, s16_sha: str, t16_sha: str, t16_blob: str) -> None:
    """Require the retained exact V16 JSON evidence semantics."""
    assert isinstance(record, dict)
    payload = cast("JsonObject", record)
    assert set(payload) == {
        "schema_version",
        "correction_id",
        "phase",
        "subject",
        "tester_evidence",
        "verdict",
        "blocking_issues",
        "timestamp",
    }
    assert (
        payload["schema_version"]
        == "observer-dispatcher-governance.correction-b6r10-implementation-review.v1"
    )
    assert payload["correction_id"] == "observer-dispatcher-governance/high/b6r10"
    assert payload["phase"] == "V16"
    subject = cast("JsonObject", payload["subject"])
    assert set(subject) == {"phase", "commit_sha", "test_path"}
    assert subject == {"phase": "S16", "commit_sha": s16_sha, "test_path": TEST_PATH}
    tester_evidence = cast("JsonObject", payload["tester_evidence"])
    assert set(tester_evidence) == {
        "phase",
        "commit_sha",
        "path",
        "blob_sha",
        "subject_commit_sha",
        "status",
    }
    assert tester_evidence == {
        "phase": "T16",
        "commit_sha": t16_sha,
        "path": T16_EVIDENCE_PATH,
        "blob_sha": t16_blob,
        "subject_commit_sha": s16_sha,
        "status": "passing",
    }
    assert payload["verdict"] == "APPROVED"
    assert payload["blocking_issues"] == []


def assert_named_s16_evidence_graph(graph: EvidenceGraph) -> None:
    """Validate named graph facts without inferring them from checkout HEAD."""
    for sha in (graph.s16_sha, graph.t16_sha, graph.v16_sha):
        assert_sha(sha)
        assert sha != "HEAD"
    assert len({graph.s16_sha, graph.t16_sha, graph.v16_sha}) == EVIDENCE_GRAPH_SHA_COUNT
    assert graph.t16_parent == graph.s16_sha
    assert graph.v16_parent == graph.t16_sha
    assert graph.named_range == f"{graph.s16_sha}..{graph.v16_sha}"
    assert "HEAD" not in graph.named_range
    assert graph.range_paths == (V16_EVIDENCE_PATH, T16_EVIDENCE_PATH)


def assert_actual_s16_graph(s16_sha: str, t16_sha: str, v16_sha: str) -> None:
    """Use real Git objects to validate the full committed S16/T16/V16 chain."""
    for sha in (s16_sha, t16_sha, v16_sha):
        try:
            assert run_git("rev-parse", "--verify", f"{sha}^{{commit}}") == sha
        except subprocess.CalledProcessError as error:
            raise AssertionError(Q16_REAL_COMMIT_REQUIRED) from error
    graph = EvidenceGraph(
        s16_sha=s16_sha,
        s16_parent=single_parent(s16_sha),
        t16_sha=t16_sha,
        t16_parent=single_parent(t16_sha),
        v16_sha=v16_sha,
        v16_parent=single_parent(v16_sha),
        named_range=f"{s16_sha}..{v16_sha}",
        range_paths=tuple(
            line.split("\t", 1)[1]
            for line in run_git("diff", "--name-status", f"{s16_sha}..{v16_sha}").splitlines()
        ),
    )
    assert_named_s16_evidence_graph(graph)
    assert run_git("diff", "--name-status", f"{s16_sha}^..{s16_sha}").splitlines() == [
        f"M\t{TEST_PATH}",
    ]
    assert run_git("rev-list", "--reverse", graph.named_range).splitlines() == [t16_sha, v16_sha]
    assert run_git("diff", "--name-status", f"{s16_sha}..{t16_sha}").splitlines() == [
        f"A\t{T16_EVIDENCE_PATH}",
    ]
    assert run_git("diff", "--name-status", f"{t16_sha}..{v16_sha}").splitlines() == [
        f"A\t{V16_EVIDENCE_PATH}",
    ]
    t16_blob = run_git("rev-parse", f"{t16_sha}:{T16_EVIDENCE_PATH}")
    assert_t16_schema(json_object_at(t16_sha, T16_EVIDENCE_PATH), s16_sha)
    assert_v16_schema(json_object_at(v16_sha, V16_EVIDENCE_PATH), s16_sha, t16_sha, t16_blob)


def remove_route_authorization(record: JsonObject) -> None:
    """Remove one mandatory approved R22 field."""
    record.pop("route_authorization")


def replace_candidate_state(record: JsonObject) -> None:
    """Substitute an inactive candidate into an approved R22 receipt."""
    cast("JsonObject", record["candidate"])["active"] = False


def remove_reviewed_artifact(record: JsonObject) -> None:
    """Remove one required exact-five R22 artifact."""
    cast("list[JsonObject]", record["reviewed_artifacts"]).pop()


def replace_verdict(record: JsonObject) -> None:
    """Substitute an unapproved R22 verdict."""
    record["verdict"] = "needs-rework"


def test_b6r12_r22_route_is_the_sole_s16_predecessor() -> None:
    """Require the committed approved R22 gate before the S16 implementation subject."""
    assert_s16_route_is_fail_closed(read_current_route())


def test_actual_b6r12_admission_and_r22_match_committed_git_objects() -> None:
    """Check exact-five baseline admission and its independent one-path R22 receipt."""
    assert_b6r12_admission_and_r22()


@pytest.mark.parametrize(
    ("source", "required_text", "replacement"),
    [
        ("parent_plan", "B6R12 -> R22 -> S16 -> T16 -> V16 -> Q16", "B6R11 -> R21 -> S16"),
        ("b6r12_plan", "S16 retains direct imports", "S16 permits replacement imports"),
        ("b6r12_plan", "Q16 actual full-triple", "Q16 inferred triple"),
        ("b6r12_step", "R22_REVIEW_PENDING", "R22_COMPLETE_S16_NEXT"),
    ],
)
def test_s16_route_rejects_stale_topology_and_gate_mutations(
    source: str,
    required_text: str,
    replacement: str,
) -> None:
    """Make stale route, direct-import, input, and state substitutions fail closed."""
    route = read_current_route()
    assert required_text in route[source]
    route[source] = route[source].replace(required_text, replacement)
    with pytest.raises(AssertionError):
        assert_s16_route_is_fail_closed(route)


@pytest.mark.parametrize(
    "mutation",
    [
        remove_route_authorization,
        replace_candidate_state,
        remove_reviewed_artifact,
        replace_verdict,
    ],
)
def test_r22_schema_rejects_structural_and_value_mutations(mutation: RecordMutation) -> None:
    """Reject missing R22 fields, inactive approval, and substituted receipt values."""
    record = cast("JsonObject", json.loads(read(R22_REVIEW_PATH)))
    mutation(record)
    with pytest.raises(AssertionError):
        assert_b6r12_r22_schema(record)


def test_named_s16_t16_v16_graph_rejects_merge_head_and_range_mutations() -> None:
    """Keep Q16 named, linear, and confined to two evidence paths."""
    s16_sha, t16_sha, v16_sha = "1" * 40, "2" * 40, "3" * 40
    graph = EvidenceGraph(
        s16_sha,
        "0" * 40,
        t16_sha,
        s16_sha,
        v16_sha,
        t16_sha,
        f"{s16_sha}..{v16_sha}",
        (V16_EVIDENCE_PATH, T16_EVIDENCE_PATH),
    )
    assert_named_s16_evidence_graph(graph)
    for mutation in (
        {"t16_parent": "4" * 40},
        {"v16_parent": s16_sha},
        {"named_range": f"{s16_sha}..HEAD"},
        {"range_paths": (V16_EVIDENCE_PATH, T16_EVIDENCE_PATH, "plan/extra.md")},
    ):
        with pytest.raises(AssertionError):
            assert_named_s16_evidence_graph(replace(graph, **mutation))


def test_all_absent_s16_environment_is_an_explicit_skip_condition() -> None:
    """Permit no actual-Q16 claim until all three post-commit identities exist."""
    assert explicit_s16_triple({}) is None


@pytest.mark.parametrize(
    "environment",
    [
        {"ODG_S16_SHA": "1" * 40},
        {"ODG_S16_SHA": "1" * 40, "ODG_T16_SHA": "2" * 40},
        {"ODG_S16_SHA": "", "ODG_T16_SHA": "2" * 40, "ODG_V16_SHA": "3" * 40},
        {"ODG_S16_SHA": "HEAD", "ODG_T16_SHA": "2" * 40, "ODG_V16_SHA": "3" * 40},
        {"ODG_S16_SHA": "1" * 39, "ODG_T16_SHA": "2" * 40, "ODG_V16_SHA": "3" * 40},
        {"ODG_S16_SHA": "1" * 40, "ODG_T16_SHA": "1" * 40, "ODG_V16_SHA": "3" * 40},
    ],
)
def test_partial_or_invalid_s16_environment_fails_closed(environment: dict[str, str]) -> None:
    """Reject every supplied environment that is not a complete named triple."""
    with pytest.raises(AssertionError):
        explicit_s16_triple(environment)


def test_nonexistent_s16_triple_fails_closed() -> None:
    """Reject real-looking but nonexistent commits rather than treating them as unverified."""
    with pytest.raises(AssertionError):
        assert_actual_s16_graph("0" * 40, "1" * 40, "2" * 40)


def test_actual_s16_t16_v16_graph_requires_a_complete_real_triple() -> None:
    """Run Q16 only with explicit post-V16 SHAs; it writes neither artifact nor thread state."""
    triple = explicit_s16_triple(os.environ)
    if triple is None:
        pytest.skip("explicit skip/unverified: all ODG S16/T16/V16 SHAs are absent")
    assert_actual_s16_graph(*triple)


def test_s16_contract_test_preserves_direct_import_behavior() -> None:
    """Keep this conformance test free of dynamic-import substitutions."""
    assert_direct_import_behavior(read(TEST_PATH))


def test_contract_test_rejects_dynamic_import_mutation() -> None:
    """Make a dynamic-import substitution fail closed instead of replacing behavior."""
    mutated_source = read(TEST_PATH) + "\nimport " + "import" + "lib\n"
    with pytest.raises(AssertionError):
        assert_direct_import_behavior(mutated_source)
