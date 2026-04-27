from __future__ import annotations

from typing import Any, Dict, Iterator, List, Optional

from ..models.contacts import Contact
from ..odata import ODataQuery
from .base import BaseService


class ContactsService(BaseService):
    """CRUD operations for the PBX contact book.

    Reference paths:
      GET    /Contacts
      POST   /Contacts
      GET    /Contacts({Id})
      PATCH  /Contacts({Id})
      DELETE /Contacts({Id})
    """

    _PATH = "/Contacts"

    def list(self, query: Optional[ODataQuery] = None) -> List[Contact]:
        data = self._list_raw(self._PATH, query)
        return [Contact.model_validate(item) for item in data.get("value", [])]

    def iterate(self, query: Optional[ODataQuery] = None) -> Iterator[Contact]:
        yield from self._paginate(self._PATH, Contact, query)

    def create(self, contact: Contact | Dict[str, Any]) -> Contact:
        payload = (
            contact.model_dump(by_alias=True, exclude_none=True)
            if isinstance(contact, Contact)
            else contact
        )
        data = self._post(self._PATH, json=payload)
        return Contact.model_validate(data)

    def get(self, contact_id: int, query: Optional[ODataQuery] = None) -> Contact:
        data = self._get(f"{self._PATH}({contact_id})", params=self._query_params(query))
        return Contact.model_validate(data)

    def update(self, contact_id: int, changes: Contact | Dict[str, Any]) -> None:
        payload = (
            changes.model_dump(by_alias=True, exclude_none=True)
            if isinstance(changes, Contact)
            else changes
        )
        self._patch(f"{self._PATH}({contact_id})", json=payload)

    def delete(self, contact_id: int, etag: Optional[str] = None) -> None:
        self._delete(f"{self._PATH}({contact_id})", etag=etag)

    def get_by_number(self, number: str, query: Optional[ODataQuery] = None) -> List[Contact]:
        data = self._get(f"{self._PATH}/Pbx.GetContactsByNumber(number='{number}')", params=self._query_params(query))
        return [Contact.model_validate(item) for item in data.get("value", [])]

    def create_by_number(self, data: Dict[str, Any]) -> Contact:
        result = self._post(f"{self._PATH}/Pbx.CreateContactByNumber", json=data)
        return Contact.model_validate(result)

    def delete_by_ids(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.DeleteContactsById", json=data)

    def delete_by_type(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.DeleteContactsByType", json=data)

    def delete_department_by_type(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.DeleteDepartmentContactsByType", json=data)

    def delete_personal_by_type(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.DeletePersonalContactsByType", json=data)

    def get_dir_search_settings(self) -> Dict[str, Any]:
        return self._get(f"{self._PATH}/Pbx.GetDirSearchSettings()")

    def set_dir_search_settings(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.SetDirSearchSettings", json=data)
