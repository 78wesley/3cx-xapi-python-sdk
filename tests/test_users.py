"""Tests for UsersService — CRUD, sub-resources, actions, and OData queries."""
from __future__ import annotations

import pytest
from pytest_httpx import HTTPXMock

from tests.conftest import TOKEN_URL, TOKEN_JSON, api
from threecx import ThreeCXClient
from threecx.models.users import User
from threecx.odata import ODataQuery

USER_1 = {"Id": 101, "Number": "100", "FirstName": "Alice", "LastName": "Smith", "EmailAddress": "alice@x.com", "Enabled": True}
USER_2 = {"Id": 102, "Number": "101", "FirstName": "Bob", "LastName": "Jones", "Enabled": True}



@pytest.fixture
def client(httpx_mock: HTTPXMock) -> ThreeCXClient:
    httpx_mock.add_response(url=TOKEN_URL, method="POST", json=TOKEN_JSON, is_reusable=True)
    return ThreeCXClient("https://pbx.test", "id", "secret")


# --- list ---------------------------------------------------------------------

def test_list_returns_users(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=api("/Users"),
        json={"value": [USER_1, USER_2]},
    )
    users = client.users.list()
    assert len(users) == 2
    assert users[0].first_name == "Alice"
    assert users[1].number == "101"


def test_list_empty_collection(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(url=api("/Users"), json={"value": []})
    assert client.users.list() == []


def test_list_with_odata_query(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=api("/Users"),
        match_params={"$filter": "Enabled eq true", "$top": "5"},
        json={"value": [USER_1]},
    )
    q = ODataQuery().filter("Enabled eq true").top(5)
    users = client.users.list(q)
    assert len(users) == 1


# --- iterate (pagination) -----------------------------------------------------

def test_iterate_follows_next_link(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=api("/Users"),
        json={"value": [USER_1], "@odata.nextLink": api("/Users?$skip=1")},
    )
    httpx_mock.add_response(
        url=api("/Users?$skip=1"),
        json={"value": [USER_2]},
    )
    users = list(client.users.iterate())
    assert len(users) == 2
    assert users[0].id == 101
    assert users[1].id == 102


# --- get ----------------------------------------------------------------------

def test_get_user_by_id(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(url=api("/Users(101)"), json=USER_1)
    user = client.users.get(101)
    assert user.id == 101
    assert user.email_address == "alice@x.com"


def test_get_user_with_expand(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=api("/Users(101)"),
        match_params={"$expand": "Groups"},
        json={**USER_1, "Groups": [{"Id": 5, "Name": "Sales"}]},
    )
    user = client.users.get(101, query=ODataQuery().expand("Groups"))
    assert user.groups[0].name == "Sales"


# --- create -------------------------------------------------------------------

def test_create_user(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    new_payload = {"Number": "200", "FirstName": "Carol", "Email": "carol@x.com"}
    created_payload = {**new_payload, "Id": 103}
    httpx_mock.add_response(
        url=api("/Users"),
        method="POST",
        status_code=201,
        json=created_payload,
    )
    created = client.users.create(User(Number="200", FirstName="Carol", Email="carol@x.com"))
    assert created.id == 103
    assert created.number == "200"


def test_create_user_from_dict(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=api("/Users"),
        method="POST",
        status_code=201,
        json={"Id": 104, "Number": "201"},
    )
    created = client.users.create({"Number": "201", "FirstName": "Dave"})
    assert created.id == 104


# --- update -------------------------------------------------------------------

def test_update_user(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=api("/Users(101)"),
        method="PATCH",
        status_code=204,
    )
    client.users.update(101, {"Email": "newalice@x.com"})  # must not raise


# --- delete -------------------------------------------------------------------

def test_delete_user(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=api("/Users(101)"),
        method="DELETE",
        status_code=204,
    )
    client.users.delete(101)


def test_delete_user_with_etag(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=api("/Users(101)"),
        method="DELETE",
        status_code=204,
        match_headers={"If-Match": '"abc123"'},
    )
    client.users.delete(101, etag='"abc123"')


# --- sub-resources ------------------------------------------------------------

def test_get_groups(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=api("/Users(101)/Groups"),
        json={"value": [{"Id": 5, "Name": "Sales"}, {"Id": 6, "Name": "Support"}]},
    )
    groups = client.users.get_groups(101)
    assert len(groups) == 2
    assert groups[0].name == "Sales"


def test_get_forwarding_profiles(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=api("/Users(101)/ForwardingProfiles"),
        json={"value": [{"Id": 1, "Name": "Away", "Enabled": True}]},
    )
    profiles = client.users.get_forwarding_profiles(101)
    assert profiles[0].name == "Away"


def test_get_greetings(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=api("/Users(101)/Greetings"),
        json={"value": [{"Filename": "voicemail.wav", "DisplayName": "Voicemail"}]},
    )
    greetings = client.users.get_greetings(101)
    assert greetings[0].filename == "voicemail.wav"


# --- actions ------------------------------------------------------------------

def test_send_welcome_email(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=api("/Users(101)/Pbx.SendWelcomeEmail"),
        method="POST",
        status_code=204,
    )
    client.users.send_welcome_email(101)


def test_make_call(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=api("/Users(101)/Pbx.MakeCall"),
        method="POST",
        match_json={"Destination": "0031612345678"},
        status_code=204,
    )
    client.users.make_call(101, "0031612345678")


def test_batch_delete(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=api("/Users/Pbx.BatchDelete"),
        method="POST",
        match_json={"userIds": [101, 102]},
        status_code=204,
    )
    client.users.batch_delete([101, 102])


def test_get_first_available_extension(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=api("/Users/Pbx.GetFirstAvailableExtensionNumber()"),
        json={"value": "205"},
    )
    ext = client.users.get_first_available_extension()
    assert ext == "205"
