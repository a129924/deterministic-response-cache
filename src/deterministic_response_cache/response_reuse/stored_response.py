# Copyright (c) 2026 deterministic-response-cache contributors
# ruff: noqa: INP001

"""Stored response bytes and their closed format identifier."""

from dataclasses import dataclass
from enum import StrEnum


class ResponseCodecId(StrEnum):
    """Formats supported for the lifetime of a cache instance."""

    JSON_V1 = "json/v1"
    DATAFRAME_V1 = "dataframe/v1"


@dataclass(frozen=True, slots=True)
class StoredResponse:
    """Envelope retained by the internal CacheStore."""

    codec_id: ResponseCodecId
    payload: bytes
