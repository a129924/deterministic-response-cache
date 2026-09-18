# Copyright (c) 2026 deterministic-response-cache contributors

"""Direct-module contracts for the protocol-only Loaded Runtime Cache BC."""

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
from deterministic_response_cache.loaded_runtime_cache.runtime_reuse.retention.runtime_retention import (  # noqa: E501, TC001
    RuntimeRetention,
)


class FakeRuntimeRegistry[RuntimeT]:
    """Typed Registry double that records only opaque handoffs."""

    def __init__(self, lookup_result: RuntimeT | None) -> None:
        """Configure the Registry hit or missing channel."""
        self._lookup_result = lookup_result
        self.lookup_keys: list[RuntimeReuseKey] = []
        self.retained: list[tuple[RuntimeReuseKey, RuntimeT]] = []

    def lookup(self, key: RuntimeReuseKey) -> RuntimeT | None:
        """Return the configured channel after retaining the same key instance."""
        self.lookup_keys.append(key)
        return self._lookup_result

    def retain(self, key: RuntimeReuseKey, runtime: RuntimeT) -> None:
        """Record the opaque key and runtime without interpreting either value."""
        self.retained.append((key, runtime))


class ExpectedFailureRegistry:
    """Registry double that raises the port-owned expected failure signal."""

    def __init__(self, signal: RuntimeRegistryLookupUnavailable) -> None:
        """Keep the exact signal that must propagate unchanged."""
        self._signal = signal
        self.lookup_keys: list[RuntimeReuseKey] = []

    def lookup(self, key: RuntimeReuseKey) -> object | None:
        """Raise the configured expected signal after one opaque handoff."""
        self.lookup_keys.append(key)
        raise self._signal

    def retain(self, key: RuntimeReuseKey, runtime: object) -> None:
        """Provide the Registry port's retention member for structural typing."""
        del key, runtime


class UnexpectedFailureRegistry:
    """Registry double that exposes a non-expected failure unchanged."""

    def __init__(self, error: ValueError) -> None:
        """Keep the exact unexpected error that must propagate."""
        self._error = error

    def lookup(self, key: RuntimeReuseKey) -> object | None:
        """Raise the configured unexpected error without conversion."""
        del key
        raise self._error

    def retain(self, key: RuntimeReuseKey, runtime: object) -> None:
        """Provide the Registry port's retention member for structural typing."""
        del key, runtime


class FakeRuntimeRetention[RuntimeT]:
    """Typed Retention double with a caller-selected semantic outcome."""

    def __init__(self, outcome: RetentionOutcome[RuntimeT]) -> None:
        """Configure a success or failure outcome."""
        self._outcome = outcome
        self.received: list[tuple[RuntimeReuseKey, RuntimeT]] = []

    def retain(
        self,
        key: RuntimeReuseKey,
        runtime: RuntimeT,
    ) -> Retained[RuntimeT] | NotRetained[RuntimeT]:
        """Return the configured outcome after recording opaque arguments."""
        self.received.append((key, runtime))
        return self._outcome


def test_runtime_registry_handoff_keeps_the_same_local_key_instance() -> None:
    """Lookup and retain forward an opaque local key without interpreting it."""
    key = RuntimeReuseKey("externally-decided-token")
    runtime = object()
    registry: RuntimeRegistry[object] = FakeRuntimeRegistry(runtime)

    assert registry.lookup(key) is runtime
    registry.retain(key, runtime)

    fake_registry = registry
    assert isinstance(fake_registry, FakeRuntimeRegistry)
    assert len(fake_registry.lookup_keys) == 1
    assert fake_registry.lookup_keys[0] is key
    assert len(fake_registry.retained) == 1
    assert fake_registry.retained[0][0] is key
    assert fake_registry.retained[0][1] is runtime


def test_runtime_registry_distinguishes_hit_and_missing_channels() -> None:
    """The port's value channels remain separate from semantic outcome vocabulary."""
    key = RuntimeReuseKey("externally-decided-token")
    runtime = object()
    hit_registry: RuntimeRegistry[object] = FakeRuntimeRegistry(runtime)
    missing_registry: RuntimeRegistry[object] = FakeRuntimeRegistry(None)
    outcome: LookupOutcome[object] = Available(runtime)

    assert hit_registry.lookup(key) is runtime
    assert missing_registry.lookup(key) is None
    assert outcome.runtime is runtime
    assert Missing() != Unavailable()


def test_expected_lookup_signal_and_unexpected_error_propagate_unchanged() -> None:
    """No protocol implementation maps either exception into a lookup outcome."""
    key = RuntimeReuseKey("externally-decided-token")
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
    """Both outcome channels keep ownership of the exact caller runtime."""
    key = RuntimeReuseKey("externally-decided-token")
    runtime = object()
    outcome: RetentionOutcome[object] = outcome_type(runtime)
    retention: RuntimeRetention[object] = FakeRuntimeRetention(outcome)

    returned = retention.retain(key, runtime)

    assert returned.runtime is runtime
    fake_retention = retention
    assert isinstance(fake_retention, FakeRuntimeRetention)
    assert len(fake_retention.received) == 1
    assert fake_retention.received[0][0] is key
    assert fake_retention.received[0][1] is runtime
