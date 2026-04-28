"""Tests for QueuesService."""
from __future__ import annotations

import pytest
from pytest_httpx import HTTPXMock

from tests.conftest import TOKEN_URL, TOKEN_JSON, api
from threecx import ThreeCXClient
from threecx.models.queues import Queue


QUEUE_1 = {"Id": 10, "Number": "800", "Name": "Support", "RingTimeout": 30, "SLATime": 20}
QUEUE_2 = {"Id": 11, "Number": "801", "Name": "Sales", "RingTimeout": 20}


@pytest.fixture
def client(httpx_mock: HTTPXMock) -> ThreeCXClient:
    httpx_mock.add_response(url=TOKEN_URL, method="POST", json=TOKEN_JSON, is_reusable=True)
    return ThreeCXClient("https://pbx.test", "id", "secret")


def test_list_queues(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(url=api("/Queues"), json={"value": [QUEUE_1, QUEUE_2]})
    queues = client.queues.list()
    assert len(queues) == 2
    assert queues[0].name == "Support"


def test_get_queue_by_id(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(url=api("/Queues(10)"), json=QUEUE_1)
    q = client.queues.get(10)
    assert q.ring_timeout == 30


def test_get_queue_by_number(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(url=api("/Queues(Number='800')"), json=QUEUE_1)
    q = client.queues.get_by_number("800")
    assert q.id == 10


def test_create_queue(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=api("/Queues"),
        method="POST",
        status_code=201,
        json={**QUEUE_1, "Id": 12},
    )
    created = client.queues.create(Queue(Number="802", Name="Billing", RingTimeout=25))
    assert created.id == 12


def test_update_queue(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(url=api("/Queues(10)"), method="PATCH", status_code=204)
    client.queues.update(10, {"SLATime": 30})


def test_delete_queue(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(url=api("/Queues(10)"), method="DELETE", status_code=204)
    client.queues.delete(10)


def test_get_agents(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=api("/Queues(10)/Agents"),
        json={"value": [{"Id": 1, "Number": "100", "Name": "Alice"}, {"Id": 2, "Number": "101", "Name": "Bob"}]},
    )
    agents = client.queues.get_agents(10)
    assert len(agents) == 2
    assert agents[0].number == "100"


def test_get_managers(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=api("/Queues(10)/Managers"),
        json={"value": [{"Id": 3, "Number": "102", "Name": "Carol"}]},
    )
    managers = client.queues.get_managers(10)
    assert managers[0].number == "102"


def test_reset_statistics(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=api("/Queues(10)/Pbx.ResetQueueStatistics"),
        method="POST",
        status_code=204,
    )
    client.queues.reset_statistics(10)
