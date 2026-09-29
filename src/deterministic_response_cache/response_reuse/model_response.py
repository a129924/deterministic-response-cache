# Copyright (c) 2026 deterministic-response-cache contributors
# ruff: noqa: INP001

"""Caller-facing native model response value object."""

from dataclasses import dataclass
from typing import cast


@dataclass(frozen=True, slots=True)
class ModelResponse[PayloadT]:
    """Hold a native payload without changing its representation."""

    value: PayloadT

    def __hash__(self) -> int:
        """Preserve dataclass hashing for payloads that already support it."""
        return hash((self.value,))

    def __eq__(self, other: object) -> bool:
        """Compare native payloads, using DataFrame value equality when present."""
        if not isinstance(other, ModelResponse):
            return NotImplemented
        left: object = self.value
        right: object = cast("ModelResponse[object]", other).value
        if isinstance(left, (dict, list)) and isinstance(right, (dict, list)):
            return left == right
        try:
            import pandas as pd  # noqa: PLC0415  # pyright: ignore[reportMissingTypeStubs]
        except ImportError:
            return left == right
        if isinstance(left, pd.DataFrame):
            return isinstance(right, pd.DataFrame) and bool(left.equals(right))
        if isinstance(right, pd.DataFrame):
            return False
        return left == right
