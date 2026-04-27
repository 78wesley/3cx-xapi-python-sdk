from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..odata import ODataQuery
from .base import BaseService


class ParametersService(BaseService):
    """Tenant properties, DN properties, and directory info."""

    # ------------------------------------------------------------------
    # Tenant properties
    # ------------------------------------------------------------------

    def list_tenant_properties(self, query: Optional[ODataQuery] = None) -> List[Dict[str, Any]]:
        data = self._list_raw("/TenantProperties", query)
        return self._list_values(data)

    def create_tenant_property(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._post("/TenantProperties", json=data)

    def get_tenant_property(self, name: str) -> Dict[str, Any]:
        return self._get(f"/TenantProperties('{name}')")

    def update_tenant_property(self, name: str, data: Dict[str, Any]) -> None:
        self._patch(f"/TenantProperties('{name}')", json=data)

    def delete_tenant_property(self, name: str) -> None:
        self._delete(f"/TenantProperties('{name}')")

    # ------------------------------------------------------------------
    # DN properties
    # ------------------------------------------------------------------

    def create_dn_property(self, data: Dict[str, Any]) -> None:
        self._post("/DNProperties/Pbx.CreateDNProperty", json=data)

    def update_dn_property(self, data: Dict[str, Any]) -> None:
        self._post("/DNProperties/Pbx.UpdateDNProperty", json=data)

    def delete_dn_property(self, data: Dict[str, Any]) -> None:
        self._post("/DNProperties/Pbx.DeleteDNProperty", json=data)

    def get_dn_property_by_name(self, dn_number: str, name: str) -> Dict[str, Any]:
        return self._get(f"/DNProperties/Pbx.GetDNPropertyByName(dnNumber='{dn_number}',name='{name}')")

    def get_dn_properties_by_dn(self, dn_number: str) -> List[Dict[str, Any]]:
        data = self._get(f"/DNProperties/Pbx.GetPropertiesByDn(dnNumber='{dn_number}')")
        return self._list_values(data) if isinstance(data, dict) else data

    # ------------------------------------------------------------------
    # Directory info
    # ------------------------------------------------------------------

    def get_directory_info(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._post("/GetDirectoryInfo", json=data)
