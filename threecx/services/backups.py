from __future__ import annotations

from typing import Any, Dict, List

from ..models.backups import BackupEntry
from .base import BaseService


class BackupsService(BaseService):
    _PATH = "/Backups"

    def list(self) -> List[BackupEntry]:
        data = self._get(self._PATH)
        return [BackupEntry.model_validate(item) for item in data.get("value", [])]

    def delete(self, filename: str) -> None:
        self._delete(f"{self._PATH}('{filename}')")

    def backup(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.Backup", json=data)

    def can_create_backup(self) -> bool:
        data = self._get(f"{self._PATH}/Pbx.GetCanCreateBackup()")
        return bool(data.get("value", data))

    def get_settings(self) -> Dict[str, Any]:
        return self._get(f"{self._PATH}/Pbx.GetBackupSettings()")

    def get_failover_settings(self) -> Dict[str, Any]:
        return self._get(f"{self._PATH}/Pbx.GetBackupFailoverSettings()")

    def set_failover_settings(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.SetBackupFailoverSettings", json=data)

    def get_failover_scripts(self) -> List[Dict[str, Any]]:
        data = self._get(f"{self._PATH}/Pbx.GetFailoverScripts()")
        return self._list_values(data) if isinstance(data, dict) else data

    def set_settings(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.SetBackupSettings", json=data)

    def get_repository_settings(self) -> Dict[str, Any]:
        return self._get(f"{self._PATH}/Pbx.GetBackupRepositorySettings()")

    def set_repository_settings(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.SetBackupRepositorySettings", json=data)

    def get_restore_settings(self) -> Dict[str, Any]:
        return self._get(f"{self._PATH}/Pbx.GetRestoreSettings()")

    def set_restore_settings(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.SetRestoreSettings", json=data)

    def get_local_backup_size(self) -> Dict[str, Any]:
        return self._get(f"{self._PATH}/Pbx.GetLocalBackupSize()")

    def purge_local(self) -> None:
        self._post(f"{self._PATH}/Pbx.PurgeLocalBackups")

    def get_backup_extras(self, filename: str) -> Dict[str, Any]:
        return self._get(f"{self._PATH}('{filename}')/Pbx.GetBackupExtras()")

    def restore(self, filename: str, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}('{filename}')/Pbx.Restore", json=data)
