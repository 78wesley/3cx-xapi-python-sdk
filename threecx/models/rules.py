from __future__ import annotations

from typing import Any, List, Optional

from pydantic import Field

from .base import _Base


class InboundRule(_Base):
    """Represents an inbound call routing rule (Pbx.InboundRule)."""

    id: Optional[int] = Field(None, alias="Id")
    name: Optional[str] = Field(None, alias="Name")
    did_number: Optional[str] = Field(None, alias="DIDNumber")
    number: Optional[str] = Field(None, alias="Number")
    route_calls_to: Optional[str] = Field(None, alias="RouteCallsTo")
    route_to_extension: Optional[str] = Field(None, alias="RouteToExtension")
    enabled: Optional[bool] = Field(None, alias="Enabled")


class OutboundRule(_Base):
    """Represents an outbound call routing rule (Pbx.OutboundRule)."""

    id: Optional[int] = Field(None, alias="Id")
    name: Optional[str] = Field(None, alias="Name")
    calls_from_extensions: Optional[List[Any]] = Field(None, alias="CallsFromExtensions")
    calls_from_groups: Optional[List[Any]] = Field(None, alias="CallsFromGroups")
    number_length: Optional[int] = Field(None, alias="NumberLength")
    prefix: Optional[str] = Field(None, alias="Prefix")
    strip_digits: Optional[int] = Field(None, alias="StripDigits")
    prepend: Optional[str] = Field(None, alias="Prepend")
    enabled: Optional[bool] = Field(None, alias="Enabled")
