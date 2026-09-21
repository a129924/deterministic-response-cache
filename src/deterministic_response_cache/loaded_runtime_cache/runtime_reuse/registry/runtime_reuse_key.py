# Copyright (c) 2026 deterministic-response-cache contributors
# ruff: noqa: INP001

"""Opaque local key contract for reusable runtime lookup."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True, eq=False, repr=False, init=False)
class RuntimeReuseKey:
    """An immutable local locator with instance-identity semantics only."""

    _token: object

    def __init__(self, token: object) -> None:
        """Store an externally decided construction token without interpreting it."""
        object.__setattr__(self, "_token", token)

    def __repr__(self) -> str:
        """Avoid exposing the externally supplied construction token."""
        return "RuntimeReuseKey()"
