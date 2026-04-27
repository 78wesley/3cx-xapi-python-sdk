from __future__ import annotations

from typing import Any, Dict, Iterator, List, Optional

from ..models.groups import Group
from ..odata import ODataQuery
from .base import BaseService


class GroupsService(BaseService):
    _PATH = "/Groups"

    def list(self, query: Optional[ODataQuery] = None) -> List[Group]:
        data = self._list_raw(self._PATH, query)
        return [Group.model_validate(item) for item in data.get("value", [])]

    def iterate(self, query: Optional[ODataQuery] = None) -> Iterator[Group]:
        yield from self._paginate(self._PATH, Group, query)

    def create(self, group: Group | Dict[str, Any]) -> Group:
        payload = group.model_dump(by_alias=True, exclude_none=True) if isinstance(group, Group) else group
        data = self._post(self._PATH, json=payload)
        return Group.model_validate(data)

    def get(self, group_id: int, query: Optional[ODataQuery] = None) -> Group:
        data = self._get(f"{self._PATH}({group_id})", params=self._query_params(query))
        return Group.model_validate(data)

    def update(self, group_id: int, changes: Group | Dict[str, Any]) -> None:
        payload = changes.model_dump(by_alias=True, exclude_none=True) if isinstance(changes, Group) else changes
        self._patch(f"{self._PATH}({group_id})", json=payload)

    def delete(self, group_id: int) -> None:
        self._delete(f"{self._PATH}({group_id})")

    def get_members(self, group_id: int, query: Optional[ODataQuery] = None) -> List[Dict[str, Any]]:
        data = self._get(f"{self._PATH}({group_id})/Members", params=self._query_params(query))
        return self._list_values(data)

    def get_rights(self, group_id: int, query: Optional[ODataQuery] = None) -> List[Dict[str, Any]]:
        data = self._get(f"{self._PATH}({group_id})/Rights", params=self._query_params(query))
        return self._list_values(data)

    def get_restrictions(self, group_id: int) -> Dict[str, Any]:
        return self._get(f"{self._PATH}({group_id})/Pbx.GetRestrictions()")

    def delete_company_by_number(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.DeleteCompanyByNumber", json=data)

    def delete_company_by_id(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.DeleteCompanyById", json=data)

    def replace_license_key(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.ReplaceGroupLicenseKey", json=data)

    def link_partner(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.LinkGroupPartner", json=data)

    def unlink_partner(self) -> None:
        self._post(f"{self._PATH}/Pbx.UnlinkGroupPartner")
