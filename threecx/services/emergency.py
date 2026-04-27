from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..odata import ODataQuery
from .base import BaseService


class EmergencyService(BaseService):

    def list_geo_locations(self, query: Optional[ODataQuery] = None) -> List[Dict[str, Any]]:
        data = self._list_raw("/EmergencyGeoLocations", query)
        return self._list_values(data)

    def update_geo_locations(self, data: Dict[str, Any]) -> None:
        self._post("/EmergencyGeoLocations/Pbx.Update", json=data)

    def get_notifications_settings(self) -> Dict[str, Any]:
        return self._get("/EmergencyNotificationsSettings")

    def update_notifications_settings(self, data: Dict[str, Any]) -> None:
        self._patch("/EmergencyNotificationsSettings", json=data)
