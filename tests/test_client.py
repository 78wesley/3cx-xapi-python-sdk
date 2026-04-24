"""Tests for ThreeCXClient construction, context manager, and escape hatches."""
from __future__ import annotations

import pytest
from pytest_httpx import HTTPXMock

from threecx import ThreeCXClient
from threecx.services.active_calls import ActiveCallsService
from threecx.services.call_history import CallHistoryService
from threecx.services.contacts import ContactsService
from threecx.services.phones import PhonesService
from threecx.services.queues import QueuesService
from threecx.services.reports import ReportsService
from threecx.services.ring_groups import RingGroupsService
from threecx.services.system import SystemService
from threecx.services.trunks import TrunksService
from threecx.services.users import UsersService

TOKEN_URL = "https://pbx.test/connect/token"
TOKEN_JSON = {"access_token": "tok", "expires_in": 3600}


@pytest.fixture
def c(httpx_mock: HTTPXMock) -> ThreeCXClient:
    # is_optional=True because some tests don't trigger an HTTP request at all
    # (e.g. repr, attribute checks) so the token endpoint may not be called.
    httpx_mock.add_response(url=TOKEN_URL, method="POST", json=TOKEN_JSON, is_reusable=True, is_optional=True)
    return ThreeCXClient("https://pbx.test", "id", "secret")


def test_all_services_registered(c: ThreeCXClient) -> None:
    assert isinstance(c.active_calls, ActiveCallsService)
    assert isinstance(c.users, UsersService)
    assert isinstance(c.queues, QueuesService)
    assert isinstance(c.ring_groups, RingGroupsService)
    assert isinstance(c.call_history, CallHistoryService)
    assert isinstance(c.trunks, TrunksService)
    assert isinstance(c.contacts, ContactsService)
    assert isinstance(c.phones, PhonesService)
    assert isinstance(c.system, SystemService)
    assert isinstance(c.reports, ReportsService)


def test_repr(c: ThreeCXClient) -> None:
    assert "https://pbx.test" in repr(c)


def test_context_manager(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(url=TOKEN_URL, method="POST", json=TOKEN_JSON, is_optional=True)
    with ThreeCXClient("https://pbx.test", "id", "secret") as c:
        assert isinstance(c, ThreeCXClient)
    # __exit__ calls close(); if the client is already closed a second close
    # would raise — we just check it didn't raise here.


def test_escape_hatch_get(c: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url="https://pbx.test/xapi/v1/InboundRules",
        json={"value": [{"Id": 1}]},
    )
    data = c.get("/InboundRules")
    assert data["value"][0]["Id"] == 1


def test_escape_hatch_post(c: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url="https://pbx.test/xapi/v1/Backups/Pbx.CreateBackup",
        method="POST",
        status_code=204,
    )
    result = c.post("/Backups/Pbx.CreateBackup")
    assert result is None


def test_invalidate_token(c: ThreeCXClient) -> None:
    c.invalidate_token()
    assert c._auth._token is None
