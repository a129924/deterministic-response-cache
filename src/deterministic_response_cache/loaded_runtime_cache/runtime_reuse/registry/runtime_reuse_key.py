# Copyright (c) 2026 deterministic-response-cache contributors
# ruff: noqa: INP001

"""Local opaque key contract for locating reusable runtimes."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RuntimeReuseKey:
    """Identify one reusable runtime using an externally decided opaque token."""

    _opaque_token: str
