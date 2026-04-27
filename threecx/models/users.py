from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from .base import _Base


class UserGroupRef(_Base):
    """A user group reference (Pbx.UserGroup) — lightweight Id+Name pair."""

    id: Optional[int] = Field(None, alias="Id")
    name: Optional[str] = Field(None, alias="Name")


Group = UserGroupRef


class ForwardingProfile(_Base):
    """A forwarding profile entry (Pbx.ForwardingProfile)."""

    id: Optional[int] = Field(None, alias="Id")
    name: Optional[str] = Field(None, alias="Name")
    enabled: Optional[bool] = Field(None, alias="Enabled")


class Greeting(_Base):
    """A voicemail/IVR greeting file (Pbx.Greeting)."""

    id: Optional[int] = Field(None, alias="Id")
    filename: Optional[str] = Field(None, alias="GreetingFile")
    type: Optional[str] = Field(None, alias="GreetingType")
    name: Optional[str] = Field(None, alias="Name")


class User(_Base):
    """Represents a 3CX PBX user/extension (Pbx.User)."""

    id: Optional[int] = Field(None, alias="Id")
    number: Optional[str] = Field(None, alias="Number")
    first_name: Optional[str] = Field(None, alias="FirstName")
    last_name: Optional[str] = Field(None, alias="LastName")
    email: Optional[str] = Field(None, alias="Email")
    mobile: Optional[str] = Field(None, alias="Mobile")
    external_caller_id: Optional[str] = Field(None, alias="ExternalCallerID")
    internal_caller_id: Optional[str] = Field(None, alias="InternalCallerID")
    enabled: Optional[bool] = Field(None, alias="Enabled")
    is_registered: Optional[bool] = Field(None, alias="IsRegistered")
    status: Optional[str] = Field(None, alias="PresenceStatus")
    web_meeting_friendly_name: Optional[str] = Field(None, alias="WebMeetingFriendlyName")
    groups: Optional[List[UserGroupRef]] = Field(None, alias="Groups")
    forwarding_profiles: Optional[List[ForwardingProfile]] = Field(None, alias="ForwardingProfiles")
    greetings: Optional[List[Greeting]] = Field(None, alias="Greetings")
    out_of_office_message: Optional[str] = Field(None, alias="OutOfOfficeMessage")
    language: Optional[str] = Field(None, alias="Language")
    primary_group_id: Optional[int] = Field(None, alias="PrimaryGroupId")
    transcription_mode: Optional[str] = Field(None, alias="TranscriptionMode")

    @property
    def full_name(self) -> str:
        parts = filter(None, [self.first_name, self.last_name])
        return " ".join(parts)
