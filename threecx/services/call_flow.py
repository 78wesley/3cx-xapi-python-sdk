from __future__ import annotations

from typing import Any, Dict, Iterator, List, Optional

from ..models.call_flow import CallFlowApp
from ..odata import ODataQuery
from .base import BaseService


class CallFlowService(BaseService):
    _PATH = "/CallFlowApps"

    def list(self, query: Optional[ODataQuery] = None) -> List[CallFlowApp]:
        data = self._list_raw(self._PATH, query)
        return [CallFlowApp.model_validate(item) for item in data.get("value", [])]

    def iterate(self, query: Optional[ODataQuery] = None) -> Iterator[CallFlowApp]:
        yield from self._paginate(self._PATH, CallFlowApp, query)

    def create(self, app: CallFlowApp | Dict[str, Any]) -> CallFlowApp:
        payload = app.model_dump(by_alias=True, exclude_none=True) if isinstance(app, CallFlowApp) else app
        data = self._post(self._PATH, json=payload)
        return CallFlowApp.model_validate(data)

    def get(self, app_id: int, query: Optional[ODataQuery] = None) -> CallFlowApp:
        data = self._get(f"{self._PATH}({app_id})", params=self._query_params(query))
        return CallFlowApp.model_validate(data)

    def update(self, app_id: int, changes: CallFlowApp | Dict[str, Any]) -> None:
        payload = changes.model_dump(by_alias=True, exclude_none=True) if isinstance(changes, CallFlowApp) else changes
        self._patch(f"{self._PATH}({app_id})", json=payload)

    def delete(self, app_id: int) -> None:
        self._delete(f"{self._PATH}({app_id})")

    def get_files(self, app_id: int) -> List[Dict[str, Any]]:
        data = self._get(f"{self._PATH}({app_id})/Pbx.GetFiles()")
        return self._list_values(data) if isinstance(data, dict) else data

    def delete_file(self, app_id: int, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}({app_id})/Pbx.DeleteFile", json=data)

    def list_scripts(self, query: Optional[ODataQuery] = None) -> List[Dict[str, Any]]:
        data = self._list_raw("/CallFlowScripts", query)
        return self._list_values(data)
