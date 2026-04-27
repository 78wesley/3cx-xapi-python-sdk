from __future__ import annotations

from typing import Any, Dict, Iterator, List, Optional

from ..models.fax import Fax
from ..odata import ODataQuery
from .base import BaseService


class FaxService(BaseService):
    _PATH = "/Fax"

    def list(self, query: Optional[ODataQuery] = None) -> List[Fax]:
        data = self._list_raw(self._PATH, query)
        return [Fax.model_validate(item) for item in data.get("value", [])]

    def iterate(self, query: Optional[ODataQuery] = None) -> Iterator[Fax]:
        yield from self._paginate(self._PATH, Fax, query)

    def create(self, fax: Fax | Dict[str, Any]) -> Fax:
        payload = fax.model_dump(by_alias=True, exclude_none=True) if isinstance(fax, Fax) else fax
        data = self._post(self._PATH, json=payload)
        return Fax.model_validate(data)

    def get(self, fax_id: int, query: Optional[ODataQuery] = None) -> Fax:
        data = self._get(f"{self._PATH}({fax_id})", params=self._query_params(query))
        return Fax.model_validate(data)

    def get_by_number(self, number: str, query: Optional[ODataQuery] = None) -> Fax:
        data = self._get(f"{self._PATH}(Number='{number}')", params=self._query_params(query))
        return Fax.model_validate(data)

    def update(self, fax_id: int, changes: Fax | Dict[str, Any]) -> None:
        payload = changes.model_dump(by_alias=True, exclude_none=True) if isinstance(changes, Fax) else changes
        self._patch(f"{self._PATH}({fax_id})", json=payload)

    def delete(self, fax_id: int) -> None:
        self._delete(f"{self._PATH}({fax_id})")

    def init_fax(self) -> Dict[str, Any]:
        return self._get(f"{self._PATH}/Pbx.InitFax()")

    def bulk_delete(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.BulkFaxDelete", json=data)

    # ------------------------------------------------------------------
    # Fax server settings
    # ------------------------------------------------------------------

    def get_fax_server_settings(self) -> Dict[str, Any]:
        return self._get("/FaxServerSettings")

    def update_fax_server_settings(self, data: Dict[str, Any]) -> None:
        self._patch("/FaxServerSettings", json=data)

    def get_fax_files_size(self) -> Dict[str, Any]:
        return self._get("/FaxServerSettings/Pbx.GetFaxFilesSize()")

    def cleanup_fax(self) -> None:
        self._post("/FaxServerSettings/Pbx.CleanUpFax")
