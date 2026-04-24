from __future__ import annotations

from typing import Any, List, Optional

from pydantic import Field

from .base import _Base


class SystemStatus(_Base):
    """Represents the system status (Pbx.SystemStatus)."""

    has_active_calls: Optional[bool] = Field(None, alias="HasActiveCalls")
    calls_active: Optional[int] = Field(None, alias="CallsActive")
    extensions_registered: Optional[int] = Field(None, alias="ExtensionsRegistered")
    extensions_total: Optional[int] = Field(None, alias="ExtensionsTotal")
    trunks_registered: Optional[int] = Field(None, alias="TrunksRegistered")
    trunks_total: Optional[int] = Field(None, alias="TrunksTotal")
    disk_usage: Optional[float] = Field(None, alias="DiskUsage")
    memory_usage: Optional[float] = Field(None, alias="MemUsage")
    cpu_usage: Optional[float] = Field(None, alias="CpuUsage")
    free_space: Optional[int] = Field(None, alias="FreeSpace")
    ip: Optional[str] = Field(None, alias="Ip")
    fqdn: Optional[str] = Field(None, alias="FQDN")
    pbx_version: Optional[str] = Field(None, alias="Version")
    up_since: Optional[str] = Field(None, alias="UpSince")


class LicenseStatus(_Base):
    """Represents the license / subscription status (Pbx.LicenseStatus)."""

    product_code: Optional[str] = Field(None, alias="ProductCode")
    max_simultaneous_calls: Optional[int] = Field(None, alias="MaxSimCalls")
    max_extensions: Optional[int] = Field(None, alias="MaxExtensions")
    registered_extensions: Optional[int] = Field(None, alias="RegisteredExtensions")
    subscription_valid_until: Optional[str] = Field(None, alias="SubscriptionValidUntil")
    maintenance_expires: Optional[str] = Field(None, alias="MaintenanceExpires")


class SystemParameters(_Base):
    """Represents global PBX parameters (Pbx.Parameters)."""

    fqdn: Optional[str] = Field(None, alias="FQDN")
    name: Optional[str] = Field(None, alias="Name")
    ip: Optional[str] = Field(None, alias="Ip")
    http_port: Optional[int] = Field(None, alias="HttpPort")
    https_port: Optional[int] = Field(None, alias="HttpsPort")
    sip_port: Optional[int] = Field(None, alias="SIPPort")
    tunnel_port: Optional[int] = Field(None, alias="TunnelPort")
    local_ip_address: Optional[str] = Field(None, alias="LocalIpAddress")
    supported_timezones: Optional[List[Any]] = Field(None, alias="SupportedTimezones")
