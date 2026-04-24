"""Shared fixtures for the 3CX SDK test suite."""
from __future__ import annotations

import pytest
from pytest_httpx import HTTPXMock

from threecx import ThreeCXClient

BASE_URL = "https://pbx.test"
TOKEN_URL = f"{BASE_URL}/connect/token"
API_BASE = f"{BASE_URL}/xapi/v1"

TOKEN_RESPONSE = {"access_token": "test-token-abc", "expires_in": 3600, "token_type": "Bearer"}
TOKEN_JSON = {"access_token": "tok", "expires_in": 3600}


def api(path: str) -> str:
    """Build a full API URL from a relative path."""
    return API_BASE + path


@pytest.fixture
def mock_token(httpx_mock: HTTPXMock) -> None:
    """Pre-register a successful token response for every test that needs auth."""
    httpx_mock.add_response(
        url=TOKEN_URL,
        method="POST",
        json=TOKEN_RESPONSE,
    )


@pytest.fixture
def client(mock_token: None, httpx_mock: HTTPXMock) -> ThreeCXClient:  # noqa: ARG001
    """A ThreeCXClient wired to the mock PBX base URL."""
    return ThreeCXClient(
        base_url=BASE_URL,
        client_id="test-client-id",
        client_secret="test-client-secret",
    )
