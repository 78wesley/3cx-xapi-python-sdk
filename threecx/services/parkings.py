from __future__ import annotations

from typing import Any, Dict, Iterator, List, Optional

from ..models.parkings import Parking
from ..odata import ODataQuery
from .base import BaseService


class ParkingsService(BaseService):
    _PATH = "/Parkings"

    def list(self, query: Optional[ODataQuery] = None) -> List[Parking]:
        data = self._list_raw(self._PATH, query)
        return [Parking.model_validate(item) for item in data.get("value", [])]

    def iterate(self, query: Optional[ODataQuery] = None) -> Iterator[Parking]:
        yield from self._paginate(self._PATH, Parking, query)

    def create(self, parking: Parking | Dict[str, Any]) -> Parking:
        payload = parking.model_dump(by_alias=True, exclude_none=True) if isinstance(parking, Parking) else parking
        data = self._post(self._PATH, json=payload)
        return Parking.model_validate(data)

    def get(self, parking_id: int, query: Optional[ODataQuery] = None) -> Parking:
        data = self._get(f"{self._PATH}({parking_id})", params=self._query_params(query))
        return Parking.model_validate(data)

    def get_by_number(self, number: str, query: Optional[ODataQuery] = None) -> Parking:
        data = self._get(f"{self._PATH}(Number='{number}')", params=self._query_params(query))
        return Parking.model_validate(data)

    def update(self, parking_id: int, changes: Parking | Dict[str, Any]) -> None:
        payload = changes.model_dump(by_alias=True, exclude_none=True) if isinstance(changes, Parking) else changes
        self._patch(f"{self._PATH}({parking_id})", json=payload)

    def delete(self, parking_id: int) -> None:
        self._delete(f"{self._PATH}({parking_id})")

    def get_groups(self, parking_id: int) -> List[Dict[str, Any]]:
        data = self._get(f"{self._PATH}({parking_id})/Groups")
        return self._list_values(data)

    def get_parking_settings(self) -> Dict[str, Any]:
        return self._get("/CallParkingSettings")

    def update_parking_settings(self, data: Dict[str, Any]) -> None:
        self._patch("/CallParkingSettings", json=data)
