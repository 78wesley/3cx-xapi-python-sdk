from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..models.groups import Group
from ..odata import ODataQuery
from .base import BaseService


class MyGroupService(BaseService):
    _PATH = "/MyGroup"

    def get(self, query: Optional[ODataQuery] = None) -> Group:
        data = self._get(self._PATH, params=self._query_params(query))
        return Group.model_validate(data)

    def update(self, changes: Group | Dict[str, Any]) -> None:
        payload = changes.model_dump(by_alias=True, exclude_none=True) if isinstance(changes, Group) else changes
        self._patch(self._PATH, json=payload)

    def get_members(self, query: Optional[ODataQuery] = None) -> List[Dict[str, Any]]:
        data = self._get(f"{self._PATH}/Members", params=self._query_params(query))
        return self._list_values(data)

    def get_rights(self, query: Optional[ODataQuery] = None) -> List[Dict[str, Any]]:
        data = self._get(f"{self._PATH}/Rights", params=self._query_params(query))
        return self._list_values(data)

    def get_restrictions(self) -> Dict[str, Any]:
        return self._get(f"{self._PATH}/Pbx.GetRestrictions()")

    def link_partner(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.LinkMyGroupPartner", json=data)

    def replace_license_key(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.ReplaceMyGroupLicenseKey", json=data)

    def unlink_partner(self) -> None:
        self._post(f"{self._PATH}/Pbx.UnlinkMyGroupPartner")

    def get_partner_info(self, reseller_id: str) -> Dict[str, Any]:
        return self._get(f"{self._PATH}/Pbx.GetMyGroupPartnerInfo(resellerId='{reseller_id}')")
