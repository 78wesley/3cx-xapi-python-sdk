"""Tests for CallHistoryService, including multi-page iteration and count."""
from __future__ import annotations

import pytest
from pytest_httpx import HTTPXMock

from tests.conftest import TOKEN_URL, TOKEN_JSON, api
from threecx import ThreeCXClient
from threecx.odata import ODataQuery


ENTRY_1 = {"Id": "e1", "Caller": "100", "Callee": "200", "CallDirection": "Internal", "Status": "Answered", "TalkDuration": 60}
ENTRY_2 = {"Id": "e2", "Caller": "101", "Callee": "0031612345678", "CallDirection": "Outbound", "Status": "Answered", "TalkDuration": 120}
ENTRY_3 = {"Id": "e3", "Caller": "102", "Callee": "0031698765432", "CallDirection": "Outbound", "Status": "NoAnswer", "TalkDuration": 0}


@pytest.fixture
def client(httpx_mock: HTTPXMock) -> ThreeCXClient:
    httpx_mock.add_response(url=TOKEN_URL, method="POST", json=TOKEN_JSON, is_reusable=True)
    return ThreeCXClient("https://pbx.test", "id", "secret")


def test_list_call_history(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(url=api("/CallHistoryView"), json={"value": [ENTRY_1, ENTRY_2]})
    entries = client.call_history.list()
    assert len(entries) == 2
    assert entries[0].id == "e1"
    assert entries[1].direction == "Outbound"


def test_list_with_filter(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=api("/CallHistoryView"),
        match_params={"$filter": "CallDirection eq 'Outbound'"},
        json={"value": [ENTRY_2, ENTRY_3]},
    )
    entries = client.call_history.list(ODataQuery().filter("CallDirection eq 'Outbound'"))
    assert len(entries) == 2


def test_iterate_multiple_pages(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=api("/CallHistoryView"),
        json={"value": [ENTRY_1], "@odata.nextLink": api("/CallHistoryView?$skip=1")},
    )
    httpx_mock.add_response(
        url=api("/CallHistoryView?$skip=1"),
        json={"value": [ENTRY_2], "@odata.nextLink": api("/CallHistoryView?$skip=2")},
    )
    httpx_mock.add_response(
        url=api("/CallHistoryView?$skip=2"),
        json={"value": [ENTRY_3]},
    )
    entries = list(client.call_history.iterate())
    assert len(entries) == 3
    assert [e.id for e in entries] == ["e1", "e2", "e3"]


def test_count(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=api("/CallHistoryView"),
        match_params={"$count": "true", "$top": "0"},
        json={"@odata.count": 1337, "value": []},
    )
    assert client.call_history.count() == 1337


def test_count_with_filter(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=api("/CallHistoryView"),
        match_params={"$filter": "Status eq 'Answered'", "$count": "true", "$top": "0"},
        json={"@odata.count": 42, "value": []},
    )
    assert client.call_history.count(ODataQuery().filter("Status eq 'Answered'")) == 42
