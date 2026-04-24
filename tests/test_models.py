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
        "Email": "alice@example.com",
        "Enabled": True,
    }
    user = User.model_validate(payload)
    assert user.id == 101
    assert user.number == "100"
    assert user.first_name == "Alice"
    assert user.last_name == "Smith"
    assert user.email == "alice@example.com"
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
    fp = ForwardingProfile.model_validate({"Id": 1, "Name": "Away", "Enabled": False})
    assert fp.enabled is False


def test_greeting_validates():
    gr = Greeting.model_validate({"Id": 7, "GreetingFile": "greeting.wav", "GreetingType": "Voicemail"})
    assert gr.filename == "greeting.wav"


# --- ActiveCall ---------------------------------------------------------------

def test_active_call_validates():
    payload = {
        "Id": 42,
        "Status": "Connected",
        "Established": True,
        "Caller": "100",
        "Callee": "200",
        "Duration": 65,
        "OnHold": False,
    }
    call = ActiveCall.model_validate(payload)
    assert call.id == 42
    assert call.caller == "100"
    assert call.duration == 65
    assert call.on_hold is False


def test_active_call_optional_fields_default_none():
    call = ActiveCall.model_validate({"Id": 1})
    assert call.recording is None
    assert call.is_internal is None


# --- CallHistoryEntry ---------------------------------------------------------

def test_call_history_entry_validates():
    payload = {
        "Id": "abc-123",
        "Caller": "100",
        "Callee": "0031612345678",
        "CallDirection": "Outbound",
        "Status": "Answered",
        "TalkDuration": 120,
    }
    entry = CallHistoryEntry.model_validate(payload)
    assert entry.id == "abc-123"
    assert entry.direction == "Outbound"
    assert entry.talk_duration == 120


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
    agent = QueueAgent.model_validate({"DnNumber": "101", "Position": 1, "WrapUpTime": 10})
    assert agent.dn_number == "101"
    assert agent.wrap_up_time == 10


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
    assert rg.ring_strategy == "Hunt"


def test_ring_group_member_validates():
    m = RingGroupMember.model_validate({"DnNumber": "102", "Timeout": 20})
    assert m.dn_number == "102"


# --- Trunk / Peer / Sbc -------------------------------------------------------

def test_trunk_validates():
    trunk = Trunk.model_validate({"Id": 1, "Name": "SIP Trunk A", "Host": "sip.carrier.com", "Port": 5060})
    assert trunk.host == "sip.carrier.com"


def test_peer_validates():
    peer = Peer.model_validate({"Id": 2, "Name": "Gateway", "Host": "192.168.1.1"})
    assert peer.host == "192.168.1.1"


def test_sbc_validates():
    sbc = Sbc.model_validate({"Id": 3, "Name": "SBC-1", "Host": "10.0.0.1"})
    assert sbc.name == "SBC-1"


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
        "MAC": "AA:BB:CC:DD:EE:FF",
        "Model": "Yealink T48S",
        "IPAddress": "192.168.1.50",
    })
    assert phone.mac == "AA:BB:CC:DD:EE:FF"
    assert phone.model == "Yealink T48S"


def test_phone_template_validates():
    tmpl = PhoneTemplate.model_validate({"Id": 1, "Name": "T48S Default", "Manufacturer": "Yealink"})
    assert tmpl.manufacturer == "Yealink"


# --- SystemStatus / LicenseStatus ---------------------------------------------

def test_system_status_validates():
    payload = {
        "HasActiveCalls": True,
        "CallsActive": 3,
        "ExtensionsRegistered": 25,
        "ExtensionsTotal": 30,
        "CpuUsage": 12.5,
        "Version": "20.0.0.123",
    }
    s = SystemStatus.model_validate(payload)
    assert s.calls_active == 3
    assert s.pbx_version == "20.0.0.123"


def test_license_status_validates():
    lic = LicenseStatus.model_validate({
        "ProductCode": "3CXPSPROF",
        "MaxSimCalls": 32,
        "MaxExtensions": 100,
    })
    assert lic.max_simultaneous_calls == 32
