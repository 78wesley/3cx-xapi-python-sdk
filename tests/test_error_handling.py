"""Integration-style tests: verify that HTTP error codes become the right exceptions."""
from __future__ import annotations

import pytest
from pytest_httpx import HTTPXMock

from tests.conftest import TOKEN_URL, TOKEN_JSON, api
from threecx import ThreeCXClient
from threecx.exceptions import (
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)

ERROR_BODY = {"error": {"message": "Something went wrong", "code": "GeneralException"}}


@pytest.fixture
def client(httpx_mock: HTTPXMock) -> ThreeCXClient:
    httpx_mock.add_response(url=TOKEN_URL, method="POST", json=TOKEN_JSON, is_reusable=True)
    return ThreeCXClient("https://pbx.test", "id", "secret")


@pytest.mark.parametrize("status_code,exc_type", [
    (400, ValidationError),
    (401, AuthenticationError),
    (404, NotFoundError),
    (422, ValidationError),
    (429, RateLimitError),
    (500, ServerError),
    (503, ServerError),
])
def test_error_status_raises_correct_exception(
    client: ThreeCXClient,
    httpx_mock: HTTPXMock,
    status_code: int,
    exc_type: type,
) -> None:
    httpx_mock.add_response(url=api("/Users"), status_code=status_code, json=ERROR_BODY)
    with pytest.raises(exc_type) as exc_info:
        client.users.list()
    assert exc_info.value.status_code == status_code


def test_not_found_on_get_user(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=api("/Users(9999)"),
        status_code=404,
        json={"error": {"message": "User 9999 not found"}},
    )
    with pytest.raises(NotFoundError, match="User 9999 not found"):
        client.users.get(9999)


def test_validation_error_on_create(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=api("/Users"),
        method="POST",
        status_code=400,
        json={"error": {"message": "Number is already in use"}},
    )
    with pytest.raises(ValidationError, match="Number is already in use"):
        client.users.create({"Number": "100"})


def test_server_error_carries_status_code(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(url=api("/SystemStatus"), status_code=503, json=ERROR_BODY)
    with pytest.raises(ServerError) as exc_info:
        client.system.get_status()
    assert exc_info.value.status_code == 503


def test_plain_text_error_body(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=api("/Users"),
        status_code=500,
        text="Internal Server Error",
    )
    with pytest.raises(ServerError):
        client.users.list()
