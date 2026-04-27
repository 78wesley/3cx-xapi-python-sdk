"""Tests for TrunksService (trunks, peers, SBCs)."""
from __future__ import annotations

import pytest
from pytest_httpx import HTTPXMock

from tests.conftest import TOKEN_URL, TOKEN_JSON, api
from threecx import ThreeCXClient
from threecx.models.trunks import Trunk


TRUNK_1 = {"Id": 1, "Name": "SIP Carrier", "Host": "sip.carrier.com", "Port": 5060, "Enabled": True}
PEER_1 = {"Id": 1, "Name": "PSTN GW", "Host": "192.168.1.100", "Port": 5060, "Enabled": True}
SBC_1 = {"Id": 1, "Name": "SBC Edge", "Host": "10.0.0.1", "Port": 5060, "Enabled": True}


@pytest.fixture
def client(httpx_mock: HTTPXMock) -> ThreeCXClient:
    httpx_mock.add_response(url=TOKEN_URL, method="POST", json=TOKEN_JSON, is_reusable=True)
    return ThreeCXClient("https://pbx.test", "id", "secret")


# --- Trunks -------------------------------------------------------------------

def test_list_trunks(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(url=api("/Trunks"), json={"value": [TRUNK_1]})
    trunks = client.trunks.list_trunks()
    assert trunks[0].host == "sip.carrier.com"


def test_get_trunk(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(url=api("/Trunks(1)"), json=TRUNK_1)
    t = client.trunks.get_trunk(1)
    assert t.name == "SIP Carrier"


def test_create_trunk(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=api("/Trunks"),
        method="POST",
        status_code=201,
        json={**TRUNK_1, "Id": 2},
    )
    created = client.trunks.create_trunk(Trunk(Name="New Trunk", Host="sip2.carrier.com"))
    assert created.id == 2


def test_update_trunk(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(url=api("/Trunks(1)"), method="PATCH", status_code=204)
    client.trunks.update_trunk(1, {"Enabled": False})


def test_delete_trunk(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(url=api("/Trunks(1)"), method="DELETE", status_code=204)
    client.trunks.delete_trunk(1)


# --- Peers --------------------------------------------------------------------

def test_list_peers(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(url=api("/Peers"), json={"value": [PEER_1]})
    peers = client.trunks.list_peers()
    assert peers[0].host == "192.168.1.100"


def test_get_peer(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(url=api("/Peers(1)"), json=PEER_1)
    p = client.trunks.get_peer(1)
    assert p.name == "PSTN GW"


# --- SBCs ---------------------------------------------------------------------

def test_list_sbcs(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(url=api("/Sbcs"), json={"value": [SBC_1]})
    sbcs = client.trunks.list_sbcs()
    assert sbcs[0].name == "SBC Edge"


def test_get_sbc(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(url=api("/Sbcs('SBC Edge')"), json=SBC_1)
    sbc = client.trunks.get_sbc("SBC Edge")
    assert sbc.host == "10.0.0.1"
