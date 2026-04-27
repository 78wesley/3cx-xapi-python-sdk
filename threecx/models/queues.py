from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from .base import _Base


class QueueAgent(_Base):
    """An agent assigned to a queue (Pbx.QueueAgent)."""

    dn_number: Optional[str] = Field(None, alias="DnNumber")
    position: Optional[int] = Field(None, alias="Position")
    wrap_up_time: Optional[int] = Field(None, alias="WrapUpTime")


class QueueManager(_Base):
    """A manager assigned to a queue (Pbx.QueueManager)."""

    dn_number: Optional[str] = Field(None, alias="DnNumber")


class Queue(_Base):
    """Represents a 3CX call queue (Pbx.Queue)."""

    id: Optional[int] = Field(None, alias="Id")
    number: Optional[str] = Field(None, alias="Number")
    name: Optional[str] = Field(None, alias="Name")
    is_registered: Optional[bool] = Field(None, alias="IsRegistered")
    polling_strategy: Optional[str] = Field(None, alias="PollingStrategy")
    ring_timeout: Optional[int] = Field(None, alias="RingTimeout")
    master_timeout: Optional[int] = Field(None, alias="MasterTimeout")
    sla_time: Optional[int] = Field(None, alias="SLATime")
    announce_queue_position: Optional[bool] = Field(None, alias="AnnounceQueuePosition")
    announce_estimated_wait_time: Optional[bool] = Field(None, alias="AnnounceEstimatedWaitTime")
    agents: Optional[List[QueueAgent]] = Field(None, alias="Agents")
    managers: Optional[List[QueueManager]] = Field(None, alias="Managers")


class RingGroupMember(_Base):
    """A member of a ring group (Pbx.RingGroupMember)."""

    dn_number: Optional[str] = Field(None, alias="DnNumber")
    timeout: Optional[int] = Field(None, alias="Timeout")


class RingGroup(_Base):
    """Represents a 3CX ring group (Pbx.RingGroup)."""

    id: Optional[int] = Field(None, alias="Id")
    number: Optional[str] = Field(None, alias="Number")
    name: Optional[str] = Field(None, alias="Name")
    is_registered: Optional[bool] = Field(None, alias="IsRegistered")
    ring_strategy: Optional[str] = Field(None, alias="RingStrategy")
    ring_time: Optional[int] = Field(None, alias="RingTime")
    members: Optional[List[RingGroupMember]] = Field(None, alias="Members")
    greeting_file: Optional[str] = Field(None, alias="GreetingFile")
