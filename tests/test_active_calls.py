"""Tests for ActiveCallsService."""
from __future__ import annotations

import pytest
from pytest_httpx import HTTPXMock

from tests.conftest import TOKEN_URL, TOKEN_JSON, api
from threecx import ThreeCXClient


CALL_1 = {"Id": 1, "Status": "Connected", "Established": True, "Caller": "100", "Callee": "200", "Duration": 30}
CALL_2 = {"Id": 2, "Status": "Ringing", "Established": False, "Caller": "101", "Callee": "0031612345678"}


@pytest.fixture
def client(httpx_mock: HTTPXMock) -> ThreeCXClient:
    httpx_mock.add_response(url=TOKEN_URL, method="POST", json=TOKEN_JSON, is_reusable=True)
    return ThreeCXClient("https://pbx.test", "id", "secret")


def test_list_active_calls(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(url=api("/ActiveCalls"), json={"value": [CALL_1, CALL_2]})
    calls = client.active_calls.list()
    assert len(calls) == 2
    assert calls[0].id == 1
    assert calls[0].duration == 30
    assert calls[1].caller == "101"


def test_list_active_calls_empty(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(url=api("/ActiveCalls"), json={"value": []})
    assert client.active_calls.list() == []


def test_iterate_active_calls(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(url=api("/ActiveCalls"), json={"value": [CALL_1, CALL_2]})
    calls = list(client.active_calls.iterate())
    assert len(calls) == 2


def test_drop_call(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=api("/ActiveCalls(1)/Pbx.DropCall"),
        method="POST",
        status_code=204,
    )
    client.active_calls.drop(1)


def test_active_call_on_hold_field(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=api("/ActiveCalls"),
        json={"value": [{**CALL_1, "OnHold": True, "Recording": False}]},
    )
    calls = client.active_calls.list()
    assert calls[0].on_hold is True
    assert calls[0].recording is False
