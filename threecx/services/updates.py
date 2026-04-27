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

    def get_client_crm_updates(self) -> Dict[str, Any]:
        return self._get("/GetClientCrmUpdates()")

    def install_updates(self, data: Dict[str, Any]) -> None:
        self._post("/InstallUpdates", json=data)

    def upgrade_debian(self, data: Dict[str, Any]) -> None:
        self._post("/UpgradeDebian", json=data)

    def has_debian_upgrade(self) -> bool:
        data = self._get("/HasDebianUpgrade()")
        return bool(data.get("value", data))

    def purge_calls(self, data: Dict[str, Any]) -> None:
        self._post("/PurgeCalls", json=data)

    def purge_chats(self, data: Dict[str, Any]) -> None:
        self._post("/PurgeChats", json=data)

    def purge_all_logs(self, data: Dict[str, Any]) -> None:
        self._post("/PurgeAllLogs", json=data)
