from __future__ import annotations

from typing import Any, Dict, Iterator, List, Optional

from ..models.receptionists import Receptionist
from ..odata import ODataQuery
from .base import BaseService


class ReceptionistsService(BaseService):
    _PATH = "/Receptionists"

    def list(self, query: Optional[ODataQuery] = None) -> List[Receptionist]:
        data = self._list_raw(self._PATH, query)
        return [Receptionist.model_validate(item) for item in data.get("value", [])]

    def iterate(self, query: Optional[ODataQuery] = None) -> Iterator[Receptionist]:
        yield from self._paginate(self._PATH, Receptionist, query)

    def create(self, rec: Receptionist | Dict[str, Any]) -> Receptionist:
        payload = rec.model_dump(by_alias=True, exclude_none=True) if isinstance(rec, Receptionist) else rec
        data = self._post(self._PATH, json=payload)
        return Receptionist.model_validate(data)

    def get(self, rec_id: int, query: Optional[ODataQuery] = None) -> Receptionist:
        data = self._get(f"{self._PATH}({rec_id})", params=self._query_params(query))
        return Receptionist.model_validate(data)

    def get_by_number(self, number: str, query: Optional[ODataQuery] = None) -> Receptionist:
        data = self._get(f"{self._PATH}(Number='{number}')", params=self._query_params(query))
        return Receptionist.model_validate(data)

    def update(self, rec_id: int, changes: Receptionist | Dict[str, Any]) -> None:
        payload = changes.model_dump(by_alias=True, exclude_none=True) if isinstance(changes, Receptionist) else changes
        self._patch(f"{self._PATH}({rec_id})", json=payload)

    def delete(self, rec_id: int) -> None:
        self._delete(f"{self._PATH}({rec_id})")

    def get_forwards(self, rec_id: int) -> List[Dict[str, Any]]:
        data = self._get(f"{self._PATH}({rec_id})/Forwards")
        return self._list_values(data)

    def get_first_available_number(self) -> str:
        data = self._get(f"{self._PATH}/Pbx.GetFirstAvailableReceptionistNumber()")
        return str(data.get("value", ""))
