from __future__ import annotations

from typing import Any, Dict

from .base import BaseService


class UpdatesService(BaseService):

    def get_updates(self) -> Dict[str, Any]:
        return self._get("/GetUpdates()")

    def get_update_settings(self) -> Dict[str, Any]:
        return self._get("/GetUpdateSettings()")

    def set_update_settings(self, data: Dict[str, Any]) -> None:
        self._post("/SetUpdateSettings", json=data)

    def get_update_stats(self) -> Dict[str, Any]:
        return self._get("/GetUpdatesStats()")

    def get_prompt_set_updates(self) -> Dict[str, Any]:
        return self._get("/GetPromptSetUpdates()")

    def get_server_crm_updates(self) -> Dict[str, Any]:
        return self._get("/GetServerCrmUpdates()")

    def install_updates(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._post("/InstallUpdates", json=data)

    def get_update_details(self, key: str, update_id: str) -> str:
        data = self._get(f"/GetUpdateDetails(key={key},id={update_id})")
        return str(data.get("value", ""))

    def purge_calls(self, data: Dict[str, Any]) -> None:
        self._post("/PurgeCalls", json=data)

    def purge_chats(self, data: Dict[str, Any]) -> None:
        self._post("/PurgeChats", json=data)

    def purge_all_logs(self, data: Dict[str, Any]) -> None:
        self._post("/PurgeAllLogs", json=data)
