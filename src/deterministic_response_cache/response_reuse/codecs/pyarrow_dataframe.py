# Copyright (c) 2026 deterministic-response-cache contributors
# ruff: noqa: INP001
# pyright: reportMissingTypeStubs=false, reportUnknownVariableType=false, reportUnknownMemberType=false, reportUnknownArgumentType=false

"""Pandas DataFrame response codec backed by in-memory Arrow IPC streams."""

from typing import override

import pandas as pd
import pyarrow as pa

from deterministic_response_cache.response_reuse.codecs.contract import (
    EncodeFailureError,
    InvalidPayloadError,
    ResponseCodec,
    RoundTripMismatchError,
)
from deterministic_response_cache.response_reuse.model_response import ModelResponse
from deterministic_response_cache.response_reuse.stored_response import (
    ResponseCodecId,
    StoredResponse,
)


class PyArrowDataFrameCodec(ResponseCodec[pd.DataFrame]):
    """Preserve pandas metadata and reject lossy Arrow conversion."""

    @property
    @override
    def codec_id(self) -> ResponseCodecId:
        """Return the closed DataFrame format id."""
        return ResponseCodecId.DATAFRAME_V1

    @override
    def encode(self, response: ModelResponse[pd.DataFrame]) -> StoredResponse:
        """Write a stream only if an immediate decode preserves equality."""
        try:
            table = pa.Table.from_pandas(response.value, preserve_index=True)
            sink = pa.BufferOutputStream()
            with pa.ipc.new_stream(sink, table.schema) as writer:
                writer.write_table(table)
            payload = sink.getvalue().to_pybytes()
            decoded = self.decode(payload)
        except InvalidPayloadError as exc:
            raise EncodeFailureError from exc
        except (ValueError, TypeError, pa.ArrowException) as exc:
            raise EncodeFailureError from exc
        if not response.value.equals(decoded.value):
            raise RoundTripMismatchError
        return StoredResponse(self.codec_id, payload)

    @override
    def decode(self, payload: bytes) -> ModelResponse[pd.DataFrame]:
        """Decode an Arrow IPC stream into an independent DataFrame."""
        try:
            table = pa.ipc.open_stream(payload).read_all()
            value = table.to_pandas()
        except (ValueError, TypeError, pa.ArrowException) as exc:
            raise InvalidPayloadError from exc
        return ModelResponse(value)
