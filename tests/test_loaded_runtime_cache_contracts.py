# Copyright (c) 2026 deterministic-response-cache contributors

"""Direct-module RED contracts for the protocol-only Loaded Runtime Cache BC."""

from dataclasses import FrozenInstanceError

import pytest

from deterministic_response_cache.loaded_runtime_cache.runtime_reuse.lookup.lookup_outcome import (
    Available,
    LookupOutcome,
    Missing,
    Unavailable,
)
from deterministic_response_cache.loaded_runtime_cache.runtime_reuse.registry.runtime_registry_port import (  # noqa: E501
    RuntimeRegistry,
    RuntimeRegistryLookupUnavailable,
)
from deterministic_response_cache.loaded_runtime_cache.runtime_reuse.registry.runtime_reuse_key import (  # noqa: E501
    RuntimeReuseKey,
)
from deterministic_response_cache.loaded_runtime_cache.runtime_reuse.retention.retain_outcome import (  # noqa: E501
    NotRetained,
    Retained,
    RetentionOutcome,
)
from deterministic_response_cache.loaded_runtime_cache.runtime_reuse.retention.runtime_retention import (  # noqa: E501
    RuntimeRetention,  # noqa: TC001
)


class _OpaqueToken:
    """An externally supplied token whose representation must not leak."""

    def __repr__(self) -> str:
        """Return a recognizable representation for the no-leak assertion."""
        return "externally-decided-token"


class _HostileEqualityToken:
    """Fail if Loaded Runtime Cache delegates equality or hashing to this token."""

    def __eq__(self, other: object) -> bool:
        """Reject forbidden equality inspection by the local key."""
        del other
        message = "RuntimeReuseKey must not compare its opaque token"
        raise AssertionError(message)

    def __hash__(self) -> int:
        """Reject forbidden hashing inspection by the local key."""
        message = "RuntimeReuseKey must not hash its opaque token"
        raise AssertionError(message)


class FakeRuntimeRegistry[RuntimeT]:
    """Typed Registry double that records opaque handoffs only."""

    def __init__(self, lookup_result: RuntimeT | None) -> None:
        """Configure the typed hit or missing channel."""
        self._lookup_result = lookup_result
        self.lookup_keys: list[RuntimeReuseKey] = []
        self.retained: list[tuple[RuntimeReuseKey, RuntimeT]] = []

    def lookup(self, key: RuntimeReuseKey) -> RuntimeT | None:
        """Record the exact key instance before returning the configured result."""
        self.lookup_keys.append(key)
        return self._lookup_result

    def retain(self, key: RuntimeReuseKey, runtime: RuntimeT) -> None:
        """Record the exact opaque key and runtime instances."""
        self.retained.append((key, runtime))


class ExpectedFailureRegistry:
    """Registry double that raises only the port-owned expected signal."""

    def __init__(self, signal: RuntimeRegistryLookupUnavailable) -> None:
        """Keep the expected signal for identity-preserving propagation."""
        self._signal = signal

    def lookup(self, key: RuntimeReuseKey) -> object | None:
        """Raise the configured expected signal without classifying it."""
        del key
        raise self._signal

    def retain(self, key: RuntimeReuseKey, runtime: object) -> None:
        """Satisfy the Registry port without introducing retention behavior."""
        del key, runtime


class UnexpectedFailureRegistry:
    """Registry double that leaves an unexpected exception unchanged."""

    def __init__(self, error: ValueError) -> None:
        """Keep the unexpected error that must escape unchanged."""
        self._error = error

    def lookup(self, key: RuntimeReuseKey) -> object | None:
        """Raise the configured unexpected error without conversion."""
        del key
        raise self._error

    def retain(self, key: RuntimeReuseKey, runtime: object) -> None:
        """Satisfy the Registry port without introducing retention behavior."""
        del key, runtime


class FakeRuntimeRetention[RuntimeT]:
    """Typed Retention double that returns its configured semantic outcome."""

    def __init__(self, outcome: RetentionOutcome[RuntimeT]) -> None:
        """Configure a caller-selected retention outcome."""
        self._outcome = outcome
        self.received: list[tuple[RuntimeReuseKey, RuntimeT]] = []

    def retain(
        self,
        key: RuntimeReuseKey,
        runtime: RuntimeT,
    ) -> Retained[RuntimeT] | NotRetained[RuntimeT]:
        """Record opaque inputs and return the configured semantic outcome."""
        self.received.append((key, runtime))
        return self._outcome


def _runtime_reuse_key_fixture() -> RuntimeReuseKey:
    """Represent a key supplied by the external integration or ACL boundary."""
    return RuntimeReuseKey(_OpaqueToken())


def test_runtime_reuse_key_is_opaque_and_handed_to_registry_by_identity() -> None:
    """The local key is neither converted, inspected, nor recreated by this BC."""
    key = _runtime_reuse_key_fixture()
    runtime = object()
    registry: RuntimeRegistry[object] = FakeRuntimeRegistry(runtime)

    assert registry.lookup(key) is runtime
    registry.retain(key, runtime)

    fake_registry = registry
    assert isinstance(fake_registry, FakeRuntimeRegistry)
    assert fake_registry.lookup_keys[0] is key
    assert fake_registry.retained[0][0] is key
    assert fake_registry.retained[0][1] is runtime
    assert "externally-decided-token" not in repr(key)


def test_runtime_reuse_key_uses_instance_identity_for_hostile_and_unhashable_tokens() -> None:
    """Opaque token equality and hash are never needed for local key semantics."""
    hostile_token = _HostileEqualityToken()
    unhashable_token: list[object] = []
    hostile_key = RuntimeReuseKey(hostile_token)
    unhashable_key = RuntimeReuseKey(unhashable_token)

    same_hostile_key = hostile_key
    assert hostile_key == same_hostile_key
    assert hostile_key != RuntimeReuseKey(hostile_token)
    assert hash(hostile_key) == hash(same_hostile_key)
    same_unhashable_key = unhashable_key
    assert unhashable_key == same_unhashable_key
    assert unhashable_key != RuntimeReuseKey(unhashable_token)
    assert hash(unhashable_key) == hash(same_unhashable_key)


def test_runtime_reuse_key_rejects_reassignment_of_its_opaque_token() -> None:
    """The opaque token binding is frozen after the integration boundary supplies it."""
    key = RuntimeReuseKey(object())

    with pytest.raises(FrozenInstanceError):
        key.__setattr__("_token", object())


def test_runtime_registry_distinguishes_hit_and_missing_channels() -> None:
    """The port value channels remain distinct from lookup outcome vocabulary."""
    key = _runtime_reuse_key_fixture()
    runtime = object()
    hit_registry: RuntimeRegistry[object] = FakeRuntimeRegistry(runtime)
    missing_registry: RuntimeRegistry[object] = FakeRuntimeRegistry(None)
    outcome: LookupOutcome[object] = Available(runtime)

    assert hit_registry.lookup(key) is runtime
    assert missing_registry.lookup(key) is None
    assert outcome.runtime is runtime
    assert Missing() != Unavailable()


def test_registry_expected_and_unexpected_failures_propagate_unchanged() -> None:
    """No contract in this topic maps a Registry exception to an outcome."""
    key = _runtime_reuse_key_fixture()
    expected_signal = RuntimeRegistryLookupUnavailable("registry unavailable")
    expected_registry: RuntimeRegistry[object] = ExpectedFailureRegistry(expected_signal)
    unexpected_error = ValueError("invalid registry adapter")
    unexpected_registry: RuntimeRegistry[object] = UnexpectedFailureRegistry(unexpected_error)

    with pytest.raises(RuntimeRegistryLookupUnavailable) as expected_info:
        expected_registry.lookup(key)
    with pytest.raises(ValueError, match="invalid registry adapter") as unexpected_info:
        unexpected_registry.lookup(key)

    assert expected_info.value is expected_signal
    assert unexpected_info.value is unexpected_error
    assert Missing() != Unavailable()


@pytest.mark.parametrize("outcome_type", [Retained, NotRetained])
def test_retention_outcomes_preserve_the_same_runtime_instance(
    outcome_type: type[Retained[object]] | type[NotRetained[object]],
) -> None:
    """Both retention outcomes leave the input runtime with the caller."""
    key = _runtime_reuse_key_fixture()
    runtime = object()
    outcome: RetentionOutcome[object] = outcome_type(runtime)
    retention: RuntimeRetention[object] = FakeRuntimeRetention(outcome)

    returned = retention.retain(key, runtime)

    assert returned.runtime is runtime
    fake_retention = retention
    assert isinstance(fake_retention, FakeRuntimeRetention)
    assert fake_retention.received[0][0] is key
    assert fake_retention.received[0][1] is runtime
