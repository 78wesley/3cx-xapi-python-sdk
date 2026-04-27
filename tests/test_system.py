"""Tests for SystemService."""
from __future__ import annotations

import pytest
from pytest_httpx import HTTPXMock

from tests.conftest import TOKEN_URL, TOKEN_JSON, api
from threecx import ThreeCXClient


STATUS_PAYLOAD = {
    "HasActiveCalls": True,
    "CallsActive": 5,
    "ExtensionsRegistered": 20,
    "ExtensionsTotal": 25,
    "TrunksRegistered": 2,
    "TrunksTotal": 3,
    "CpuUsage": 15.2,
    "MemUsage": 42.0,
    "DiskUsage": 30.5,
    "Version": "20.0.0.123",
    "FQDN": "pbx.example.com",
}

LICENSE_PAYLOAD = {
    "ProductCode": "3CXPSPRO",
    "MaxSimCalls": 32,
    "MaxExtensions": 100,
    "RegisteredExtensions": 25,
}

PARAMS_PAYLOAD = {
    "FQDN": "pbx.example.com",
    "Name": "My PBX",
    "HttpPort": 5000,
    "HttpsPort": 5001,
    "SIPPort": 5060,
}


@pytest.fixture
def client(httpx_mock: HTTPXMock) -> ThreeCXClient:
    httpx_mock.add_response(url=TOKEN_URL, method="POST", json=TOKEN_JSON, is_reusable=True)
    return ThreeCXClient("https://pbx.test", "id", "secret")


def test_get_status(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(url=api("/SystemStatus"), json=STATUS_PAYLOAD)
    status = client.system.get_status()
    assert status.calls_active == 5
    assert status.pbx_version == "20.0.0.123"
    assert status.fqdn == "pbx.example.com"
    assert status.cpu_usage == pytest.approx(15.2)


def test_get_license(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(url=api("/LicenseStatus"), json=LICENSE_PAYLOAD)
    lic = client.system.get_license()
    assert lic.product_code == "3CXPSPRO"
    assert lic.max_simultaneous_calls == 32
    assert lic.max_extensions == 100


def test_get_parameters(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(url=api("/Parameters"), json=PARAMS_PAYLOAD)
    params = client.system.get_parameters()
    assert params.fqdn == "pbx.example.com"
    assert params.sip_port == 5060


def test_get_raw(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(url=api("/EventLogs"), json={"value": [{"Id": 1, "Message": "Started"}]})
    data = client.system.get_raw("/EventLogs")
    assert data["value"][0]["Message"] == "Started"


def test_post_raw(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=api("/Backups/Pbx.CreateBackup"),
        method="POST",
        status_code=204,
    )
    result = client.system.post_raw("/Backups/Pbx.CreateBackup")
    assert not result
