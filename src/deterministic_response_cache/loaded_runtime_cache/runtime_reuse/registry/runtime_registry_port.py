# Copyright (c) 2026 deterministic-response-cache contributors
# ruff: noqa: INP001

"""Internal Registry port for the Loaded Runtime Cache bounded context."""

from typing import Protocol

from .runtime_reuse_key import RuntimeReuseKey


class RuntimeRegistryLookupUnavailable(Exception):  # noqa: N818
    """Signal an expected operational failure while looking up a runtime."""


class RuntimeRegistry[RuntimeT](Protocol):
    """Synchronously locate or retain runtimes by an opaque local key."""

    def lookup(self, key: RuntimeReuseKey) -> RuntimeT | None:
        """Return a runtime hit or ``None`` for a missing runtime."""
        ...

    def retain(self, key: RuntimeReuseKey, runtime: RuntimeT) -> None:
        """Retain the supplied initialized runtime for the local key."""
        ...
