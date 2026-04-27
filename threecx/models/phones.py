from __future__ import annotations

from typing import Optional

from pydantic import Field

from .base import _Base


class Phone(_Base):
    """Represents a provisioned IP phone (Pbx.Phone)."""

    id: Optional[int] = Field(None, alias="Id")
    mac: Optional[str] = Field(None, alias="MAC")
    model: Optional[str] = Field(None, alias="Model")
    ip_address: Optional[str] = Field(None, alias="IPAddress")
    firmware_version: Optional[str] = Field(None, alias="FirmwareVersion")
    assigned_extension: Optional[str] = Field(None, alias="AssignedExtension")
    last_registration: Optional[str] = Field(None, alias="LastRegistration")
    active: Optional[bool] = Field(None, alias="Active")


class PhoneTemplate(_Base):
    """Represents a phone provisioning template (Pbx.PhoneTemplate)."""

    id: Optional[int] = Field(None, alias="Id")
    name: Optional[str] = Field(None, alias="Name")
    model: Optional[str] = Field(None, alias="Model")
    manufacturer: Optional[str] = Field(None, alias="Manufacturer")


class SipDevice(_Base):
    """Represents a registered SIP device (Pbx.SipDevice)."""

    id: Optional[int] = Field(None, alias="Id")
    mac: Optional[str] = Field(None, alias="MAC")
    model: Optional[str] = Field(None, alias="Model")
    ip_address: Optional[str] = Field(None, alias="IPAddress")
    firmware_version: Optional[str] = Field(None, alias="FirmwareVersion")


class Fxs(_Base):
    """Represents an FXS (analog) gateway device (Pbx.Fxs)."""

    mac_address: Optional[str] = Field(None, alias="MacAddress")
    name: Optional[str] = Field(None, alias="Name")
    type: Optional[str] = Field(None, alias="Type")
    host: Optional[str] = Field(None, alias="Host")
    enabled: Optional[bool] = Field(None, alias="Enabled")


class FxsTemplate(_Base):
    """Represents an FXS gateway template (Pbx.FxsTemplate)."""

    id: Optional[int] = Field(None, alias="Id")
    name: Optional[str] = Field(None, alias="Name")
    model: Optional[str] = Field(None, alias="Model")
    manufacturer: Optional[str] = Field(None, alias="Manufacturer")


class DeviceInfo(_Base):
    """Represents provisioning device info (Pbx.DeviceInfo)."""

    id: Optional[str] = Field(None, alias="Id")
    mac: Optional[str] = Field(None, alias="MAC")
    model: Optional[str] = Field(None, alias="Model")
    ip_address: Optional[str] = Field(None, alias="IPAddress")


class Firmware(_Base):
    """Represents a firmware package (Pbx.Firmware)."""

    id: Optional[str] = Field(None, alias="Id")
    model: Optional[str] = Field(None, alias="Model")
    version: Optional[str] = Field(None, alias="Version")
    manufacturer: Optional[str] = Field(None, alias="Manufacturer")
