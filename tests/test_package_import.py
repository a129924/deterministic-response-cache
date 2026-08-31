# Copyright (c) 2026 deterministic-response-cache contributors

"""Smoke coverage for the empty public package surface."""

import deterministic_response_cache


def test_package_imports() -> None:
    """Ensure the installable package can be imported."""
    assert deterministic_response_cache.__name__ == "deterministic_response_cache"
