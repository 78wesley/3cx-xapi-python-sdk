from __future__ import annotations

from typing import Any, Dict, Iterator, List, Optional

from ..odata import ODataQuery
from .base import BaseService


class EventLogsService(BaseService):
    _PATH = "/EventLogs"

    def list(self, query: Optional[ODataQuery] = None) -> List[Dict[str, Any]]:
        data = self._list_raw(self._PATH, query)
        return self._list_values(data)

    def iterate(self, query: Optional[ODataQuery] = None) -> Iterator[Dict[str, Any]]:
        params = self._query_params(query) or None
        path: Optional[str] = self._PATH
        while path:
            data = self._get(path, params=params)
            yield from data.get("value", [])
            path = data.get("@odata.nextLink")
            params = None

    def download(self) -> bytes:
        return self._get_bytes(f"{self._PATH}/Pbx.DownloadEventLogs()")

    def purge(self) -> None:
        self._post(f"{self._PATH}/Pbx.PurgeEventLog")
