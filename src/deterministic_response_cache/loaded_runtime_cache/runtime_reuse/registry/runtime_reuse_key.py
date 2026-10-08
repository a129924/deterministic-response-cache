# Copyright (c) 2026 deterministic-response-cache contributors
# ruff: noqa: INP001

"""Opaque local key contract for reusable runtime lookup."""

from dataclasses import FrozenInstanceError


class RuntimeReuseKey:
    """An immutable local locator with instance-identity semantics only."""

    __slots__ = ()

    def __init__(self, token: object) -> None:
        """Accept an externally decided token without retaining or interpreting it."""
        del token

    def __repr__(self) -> str:
        """Avoid exposing the externally supplied construction token."""
        return "RuntimeReuseKey()"

    def __setattr__(self, name: str, value: object) -> None:
        """Prevent later state from being added to an opaque identity-only key."""
        del name, value
        raise FrozenInstanceError
