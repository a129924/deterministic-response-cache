# Copyright (c) 2026 deterministic-response-cache contributors
# ruff: noqa: INP001

"""Synchronous Registry port and its expected lookup failure signal."""

from typing import Protocol

from .runtime_reuse_key import RuntimeReuseKey


class RuntimeRegistryLookupUnavailable(Exception):  # noqa: N818
    """Signal that a Registry could not complete its lookup operation."""


class RuntimeRegistry[RuntimeT](Protocol):
    """Retain and retrieve already initialized runtimes by opaque local key."""

    def lookup(self, key: RuntimeReuseKey) -> RuntimeT | None:
        """Return the retained runtime or ``None`` when no runtime is retained."""
        ...

    def retain(self, key: RuntimeReuseKey, runtime: RuntimeT) -> None:
        """Retain an already initialized runtime without taking lifecycle ownership."""
        ...
