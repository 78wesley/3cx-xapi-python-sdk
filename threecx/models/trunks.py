from __future__ import annotations

from typing import Any, List, Optional

from pydantic import Field

from .base import _Base


class Trunk(_Base):
    """Represents a SIP trunk (Pbx.Trunk)."""

    id: Optional[int] = Field(None, alias="Id")
    name: Optional[str] = Field(None, alias="Name")
    type: Optional[str] = Field(None, alias="Type")
    host: Optional[str] = Field(None, alias="Host")
    port: Optional[int] = Field(None, alias="Port")
    enabled: Optional[bool] = Field(None, alias="Enabled")
    simultaneous_calls: Optional[int] = Field(None, alias="SimultaneousCalls")
    registered: Optional[bool] = Field(None, alias="Registered")
    number: Optional[str] = Field(None, alias="Number")
    inbound_rules: Optional[List[Any]] = Field(None, alias="InboundRules")
    outbound_rules: Optional[List[Any]] = Field(None, alias="OutboundRules")


class Peer(_Base):
    """Represents a SIP peer / VoIP gateway (Pbx.Peer)."""

    id: Optional[int] = Field(None, alias="Id")
    name: Optional[str] = Field(None, alias="Name")
    host: Optional[str] = Field(None, alias="Host")
    port: Optional[int] = Field(None, alias="Port")
    enabled: Optional[bool] = Field(None, alias="Enabled")


class Sbc(_Base):
    """Represents a Session Border Controller (Pbx.Sbc)."""

    id: Optional[int] = Field(None, alias="Id")
    name: Optional[str] = Field(None, alias="Name")
    host: Optional[str] = Field(None, alias="Host")
    port: Optional[int] = Field(None, alias="Port")
    enabled: Optional[bool] = Field(None, alias="Enabled")
