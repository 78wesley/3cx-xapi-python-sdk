from __future__ import annotations

from typing import Any, Dict, Iterator, List, Optional

from ..odata import ODataQuery
from .base import BaseService


class ChatService(BaseService):
    _HISTORY = "/ChatHistoryView"
    _MESSAGES = "/ChatMessagesHistoryView"

    def list_history(self, query: Optional[ODataQuery] = None) -> List[Dict[str, Any]]:
        data = self._list_raw(self._HISTORY, query)
        return self._list_values(data)

    def iterate_history(self, query: Optional[ODataQuery] = None) -> Iterator[Dict[str, Any]]:
        params = self._query_params(query) or None
        path: Optional[str] = self._HISTORY
        while path:
            data = self._get(path, params=params)
            yield from data.get("value", [])
            path = data.get("@odata.nextLink")
            params = None

    def download_history(self, client_timezone: str = "UTC") -> List[Dict[str, Any]]:
        data = self._get(f"{self._HISTORY}/Pbx.DownloadChatHistory(clientTimeZone='{client_timezone}')")
        return self._list_values(data) if isinstance(data, dict) else data

    def list_messages_history(self, query: Optional[ODataQuery] = None) -> List[Dict[str, Any]]:
        data = self._list_raw(self._MESSAGES, query)
        return self._list_values(data)

    def iterate_messages_history(self, query: Optional[ODataQuery] = None) -> Iterator[Dict[str, Any]]:
        params = self._query_params(query) or None
        path: Optional[str] = self._MESSAGES
        while path:
            data = self._get(path, params=params)
            yield from data.get("value", [])
            path = data.get("@odata.nextLink")
            params = None

    def download_messages_history(self, client_timezone: str = "UTC") -> List[Dict[str, Any]]:
        data = self._get(f"{self._MESSAGES}/Pbx.DownloadChatMessagesHistory(clientTimeZone='{client_timezone}')")
        return self._list_values(data) if isinstance(data, dict) else data

    def get_last_cdr_timestamp(self) -> Dict[str, Any]:
        return self._get("/LastCdrAndChatMessageTimestamp")
