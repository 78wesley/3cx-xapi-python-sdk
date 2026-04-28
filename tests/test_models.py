"""Unit tests for Pydantic model validation, alias mapping, and serialisation."""
from __future__ import annotations

import pytest

from threecx.models.calls import ActiveCall, CallHistoryEntry
from threecx.models.contacts import Contact
from threecx.models.phones import Phone, PhoneTemplate
from threecx.models.queues import Queue, QueueAgent, RingGroup, RingGroupMember
from threecx.models.system import LicenseStatus, SystemStatus
from threecx.models.trunks import Peer, Sbc, Trunk
from threecx.models.users import ForwardingProfile, Greeting, Group, User


# --- User ---------------------------------------------------------------------

def test_user_validates_from_api_payload():
    payload = {
        "Id": 101,
        "Number": "100",
        "FirstName": "Alice",
        "LastName": "Smith",
        "EmailAddress": "alice@example.com",
        "Enabled": True,
    }
    user = User.model_validate(payload)
    assert user.id == 101
    assert user.number == "100"
    assert user.first_name == "Alice"
    assert user.last_name == "Smith"
    assert user.email_address == "alice@example.com"
    assert user.enabled is True


def test_user_full_name():
    user = User.model_validate({"FirstName": "Bob", "LastName": "Jones"})
    assert user.full_name == "Bob Jones"


def test_user_full_name_only_first():
    user = User.model_validate({"FirstName": "Bob"})
    assert user.full_name == "Bob"


def test_user_serialises_with_aliases():
    user = User(Number="200", FirstName="Carol", Email="carol@x.com")
    payload = user.model_dump(by_alias=True, exclude_none=True)
    assert payload["Number"] == "200"
    assert payload["FirstName"] == "Carol"
    assert "Id" not in payload  # excluded because None


def test_user_extra_fields_allowed():
    user = User.model_validate({"Id": 1, "Number": "100", "UnknownField": "ignored"})
    assert user.id == 1


def test_user_nested_groups():
    payload = {
        "Id": 1,
        "Number": "100",
        "Groups": [{"Id": 5, "Name": "Sales"}],
    }
    user = User.model_validate(payload)
    assert len(user.groups) == 1
    assert user.groups[0].name == "Sales"


# --- Group / ForwardingProfile / Greeting ------------------------------------

def test_group_validates():
    g = Group.model_validate({"Id": 3, "Name": "Support"})
    assert g.id == 3
    assert g.name == "Support"


def test_forwarding_profile_validates():
    fp = ForwardingProfile.model_validate({"Id": 1, "Name": "Away", "NoAnswerTimeout": 30})
    assert fp.name == "Away"
    assert fp.no_answer_timeout == 30


def test_greeting_validates():
    gr = Greeting.model_validate({"Filename": "greeting.wav", "DisplayName": "Voicemail"})
    assert gr.filename == "greeting.wav"
    assert gr.display_name == "Voicemail"


# --- ActiveCall ---------------------------------------------------------------

def test_active_call_validates():
    payload = {
        "Id": 42,
        "Status": "Connected",
        "EstablishedAt": "2024-01-01T12:00:00Z",
        "Caller": "100",
        "Callee": "200",
    }
    call = ActiveCall.model_validate(payload)
    assert call.id == 42
    assert call.caller == "100"
    assert call.callee == "200"
    assert call.status == "Connected"
    assert call.established_at is not None


def test_active_call_optional_fields_default_none():
    call = ActiveCall.model_validate({"Id": 1})
    assert call.established_at is None
    assert call.last_change_status is None
    assert call.server_now is None


# --- CallHistoryEntry ---------------------------------------------------------

def test_call_history_entry_validates():
    payload = {
        "SegmentId": 123,
        "SrcDn": "100",
        "DstDn": "0031612345678",
        "SrcCallerNumber": "100",
        "DstCallerNumber": "0031612345678",
        "CallAnswered": True,
        "SrcInternal": True,
        "DstExternal": True,
    }
    entry = CallHistoryEntry.model_validate(payload)
    assert entry.segment_id == 123
    assert entry.src_dn == "100"
    assert entry.dst_dn == "0031612345678"
    assert entry.call_answered is True


# --- Queue --------------------------------------------------------------------

def test_queue_validates():
    payload = {
        "Id": 10,
        "Number": "800",
        "Name": "Support Queue",
        "RingTimeout": 30,
        "SLATime": 20,
    }
    q = Queue.model_validate(payload)
    assert q.name == "Support Queue"
    assert q.ring_timeout == 30


def test_queue_agent_validates():
    agent = QueueAgent.model_validate({"Id": 5, "Number": "101", "Name": "Alice", "SkillGroup": "Tier 1"})
    assert agent.id == 5
    assert agent.number == "101"
    assert agent.name == "Alice"
    assert agent.skill_group == "Tier 1"


# --- RingGroup ----------------------------------------------------------------

def test_ring_group_validates():
    payload = {
        "Id": 20,
        "Number": "700",
        "Name": "Sales Ring",
        "RingStrategy": "Hunt",
        "RingTime": 15,
    }
    rg = RingGroup.model_validate(payload)
    assert rg.ring_strategy.value == "Hunt"
    assert rg.ring_time == 15


def test_ring_group_member_validates():
    m = RingGroupMember.model_validate({"Id": 7, "Number": "102", "Name": "Bob"})
    assert m.id == 7
    assert m.number == "102"
    assert m.name == "Bob"


# --- Trunk / Peer / Sbc -------------------------------------------------------

def test_trunk_validates():
    trunk = Trunk.model_validate({"Id": 1, "Number": "100", "AuthID": "trunkauth", "SimultaneousCalls": 8})
    assert trunk.id == 1
    assert trunk.number == "100"
    assert trunk.auth_id == "trunkauth"
    assert trunk.simultaneous_calls == 8


def test_peer_validates():
    peer = Peer.model_validate({"Id": 2, "Name": "Gateway", "Number": "200"})
    assert peer.id == 2
    assert peer.name == "Gateway"
    assert peer.number == "200"


def test_sbc_validates():
    sbc = Sbc.model_validate({"Name": "SBC-1", "DisplayName": "Edge SBC", "LocalIPv4": "10.0.0.1"})
    assert sbc.name == "SBC-1"
    assert sbc.display_name == "Edge SBC"
    assert sbc.local_i_pv4 == "10.0.0.1"


# --- Contact ------------------------------------------------------------------

def test_contact_validates():
    payload = {
        "Id": 99,
        "FirstName": "Dave",
        "LastName": "Brown",
        "Email": "dave@example.com",
        "PhoneNumber": "+31612345678",
        "ContactType": "3CX",
    }
    c = Contact.model_validate(payload)
    assert c.full_name == "Dave Brown"
    assert c.phone_number == "+31612345678"


# --- Phone / PhoneTemplate ----------------------------------------------------

def test_phone_validates():
    phone = Phone.model_validate({
        "Id": 5,
        "MacAddress": "AA:BB:CC:DD:EE:FF",
        "Name": "Reception phone",
        "TemplateName": "Yealink T48S",
    })
    assert phone.id == 5
    assert phone.mac_address == "AA:BB:CC:DD:EE:FF"
    assert phone.name == "Reception phone"
    assert phone.template_name == "Yealink T48S"


def test_phone_template_validates():
    tmpl = PhoneTemplate.model_validate({"Id": "yealink-t48s", "AddAllowed": True, "Codecs": ["g711a", "g711u"]})
    assert tmpl.id == "yealink-t48s"
    assert tmpl.add_allowed is True
    assert tmpl.codecs == ["g711a", "g711u"]


# --- SystemStatus / LicenseStatus ---------------------------------------------

def test_system_status_validates():
    payload = {
        "Activated": True,
        "CallsActive": 3,
        "ExtensionsRegistered": 25,
        "ExtensionsTotal": 30,
        "DiskUsage": 12,
        "Version": "20.0.0.123",
    }
    s = SystemStatus.model_validate(payload)
    assert s.calls_active == 3
    assert s.version == "20.0.0.123"
    assert s.activated is True


def test_license_status_validates():
    lic = LicenseStatus.model_validate({
        "ProductCode": "3CXPSPROF",
        "MaxSimCalls": 32,
    })
    assert lic.max_sim_calls == 32
    assert lic.product_code == "3CXPSPROF"
