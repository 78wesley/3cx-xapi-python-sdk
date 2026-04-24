"""Tests for OAuth2Auth token acquisition, caching, and invalidation."""
from __future__ import annotations

import time

import pytest
from pytest_httpx import HTTPXMock

from threecx.auth import OAuth2Auth, _Token
from threecx.exceptions import AuthenticationError

TOKEN_URL = "https://pbx.test/connect/token"


def _make_auth() -> OAuth2Auth:
    return OAuth2Auth(
        base_url="https://pbx.test",
        client_id="client-id",
        client_secret="client-secret",
    )


def test_fetches_token_on_first_use(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=TOKEN_URL,
        method="POST",
        json={"access_token": "tok-abc", "expires_in": 3600},
    )
    auth = _make_auth()
    token = auth._get_token()
    assert token == "tok-abc"


def test_token_is_cached_after_first_fetch(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=TOKEN_URL,
        method="POST",
        json={"access_token": "tok-xyz", "expires_in": 3600},
        is_reusable=False,
    )
    auth = _make_auth()
    auth._get_token()
    # Second call must NOT trigger another HTTP request
    token2 = auth._get_token()
    assert token2 == "tok-xyz"


def test_token_is_refreshed_when_expired(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=TOKEN_URL,
        method="POST",
        json={"access_token": "tok-old", "expires_in": 3600},
    )
    auth = _make_auth()
    auth._get_token()

    # Force expiry
    auth._token = _Token(access_token="tok-old", expires_at=time.monotonic() - 1)

    httpx_mock.add_response(
        url=TOKEN_URL,
        method="POST",
        json={"access_token": "tok-new", "expires_in": 3600},
    )
    token = auth._get_token()
    assert token == "tok-new"


def test_invalidate_forces_refetch(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=TOKEN_URL,
        method="POST",
        json={"access_token": "tok-1", "expires_in": 3600},
    )
    auth = _make_auth()
    auth._get_token()
    auth.invalidate()
    assert auth._token is None

    httpx_mock.add_response(
        url=TOKEN_URL,
        method="POST",
        json={"access_token": "tok-2", "expires_in": 3600},
    )
    token = auth._get_token()
    assert token == "tok-2"


def test_raises_authentication_error_on_non_200(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=TOKEN_URL,
        method="POST",
        status_code=401,
        text="Unauthorized",
    )
    auth = _make_auth()
    with pytest.raises(AuthenticationError) as exc_info:
        auth._get_token()
    assert exc_info.value.status_code == 401


def test_raises_authentication_error_when_no_access_token(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=TOKEN_URL,
        method="POST",
        json={"error": "invalid_client"},
    )
    auth = _make_auth()
    with pytest.raises(AuthenticationError, match="No access_token"):
        auth._get_token()


def test_auth_flow_sets_bearer_header(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=TOKEN_URL,
        method="POST",
        json={"access_token": "bearer-tok", "expires_in": 3600},
    )
    import httpx as _httpx

    auth = _make_auth()
    request = _httpx.Request("GET", "https://pbx.test/xapi/v1/Users")
    # Consume the auth_flow generator
    gen = auth.auth_flow(request)
    next(gen)
    try:
        next(gen)
    except StopIteration:
        pass
    assert request.headers["Authorization"] == "Bearer bearer-tok"


def test_token_expiry_set_30s_before_actual_expiry(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=TOKEN_URL,
        method="POST",
        json={"access_token": "tok", "expires_in": 3600},
    )
    auth = _make_auth()
    before = time.monotonic()
    auth._get_token()
    after = time.monotonic()
    # expires_at should be ~3570s from now (3600 - 30)
    assert before + 3570 - 1 <= auth._token.expires_at <= after + 3570 + 1
