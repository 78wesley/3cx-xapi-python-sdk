from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import Field

from .base import _Base


class ActiveCall(_Base):
    """Represents a currently active call (Pbx.ActiveCall)."""

    id: Optional[int] = Field(None, alias="Id")
    status: Optional[str] = Field(None, alias="Status")
    established: Optional[bool] = Field(None, alias="Established")
    start_time: Optional[datetime] = Field(None, alias="StartTime")
    caller: Optional[str] = Field(None, alias="Caller")
    callee: Optional[str] = Field(None, alias="Callee")
    caller_display_name: Optional[str] = Field(None, alias="CallerDisplayName")
    callee_display_name: Optional[str] = Field(None, alias="CalleeDisplayName")
    duration: Optional[int] = Field(None, alias="Duration")
    on_hold: Optional[bool] = Field(None, alias="OnHold")
    recording: Optional[bool] = Field(None, alias="Recording")
    is_internal: Optional[bool] = Field(None, alias="IsInternal")


class CallHistoryEntry(_Base):
    """Represents an entry in the call history log (Pbx.CallLogData)."""

    id: Optional[str] = Field(None, alias="Id")
    caller: Optional[str] = Field(None, alias="Caller")
    callee: Optional[str] = Field(None, alias="Callee")
    caller_display_name: Optional[str] = Field(None, alias="CallerDisplayName")
    callee_display_name: Optional[str] = Field(None, alias="CalleeDisplayName")
    start_time: Optional[datetime] = Field(None, alias="StartTime")
    talk_duration: Optional[int] = Field(None, alias="TalkDuration")
    ring_duration: Optional[int] = Field(None, alias="RingDuration")
    status: Optional[str] = Field(None, alias="Status")
    direction: Optional[str] = Field(None, alias="CallDirection")
    recording_file: Optional[str] = Field(None, alias="RecordingFile")
    from_display_name: Optional[str] = Field(None, alias="From")
    to_display_name: Optional[str] = Field(None, alias="To")


class OutboundCall(_Base):
    """Body for initiating an outbound call (Pbx.OutboundCall)."""

    number: Optional[str] = Field(None, alias="Number")
    extension: Optional[str] = Field(None, alias="Extension")
