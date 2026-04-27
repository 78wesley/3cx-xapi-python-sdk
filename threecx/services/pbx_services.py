from __future__ import annotations

from typing import Any, Dict, List

from .base import BaseService


class PbxServicesService(BaseService):
    _PATH = "/Services"

    def list(self) -> List[Dict[str, Any]]:
        data = self._get(self._PATH)
        return self._list_values(data) if isinstance(data, dict) else data

    def start(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.Start", json=data)

    def stop(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.Stop", json=data)

    def enable(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.Enable", json=data)

    def disable(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.Disable", json=data)

    def restart(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.Restart", json=data)

    def restart_os(self) -> None:
        self._post(f"{self._PATH}/Pbx.RestartOperatingSystem")

    def garbage_collect(self) -> None:
        self._post(f"{self._PATH}/Pbx.GarbageCollect")
