from __future__ import annotations

from typing import Any, Dict, Iterator, List, Optional

from ..models.holidays import Holiday
from ..odata import ODataQuery
from .base import BaseService


class HolidaysService(BaseService):
    _PATH = "/Holidays"

    def list(self, query: Optional[ODataQuery] = None) -> List[Holiday]:
        data = self._list_raw(self._PATH, query)
        return [Holiday.model_validate(item) for item in data.get("value", [])]

    def iterate(self, query: Optional[ODataQuery] = None) -> Iterator[Holiday]:
        yield from self._paginate(self._PATH, Holiday, query)

    def create(self, holiday: Holiday | Dict[str, Any]) -> Holiday:
        payload = holiday.model_dump(by_alias=True, exclude_none=True) if isinstance(holiday, Holiday) else holiday
        data = self._post(self._PATH, json=payload)
        return Holiday.model_validate(data)

    def get(self, holiday_id: int, query: Optional[ODataQuery] = None) -> Holiday:
        data = self._get(f"{self._PATH}({holiday_id})", params=self._query_params(query))
        return Holiday.model_validate(data)

    def update(self, holiday_id: int, changes: Holiday | Dict[str, Any]) -> None:
        payload = changes.model_dump(by_alias=True, exclude_none=True) if isinstance(changes, Holiday) else changes
        self._patch(f"{self._PATH}({holiday_id})", json=payload)

    def delete(self, holiday_id: int) -> None:
        self._delete(f"{self._PATH}({holiday_id})")

    def get_office_hours(self) -> Dict[str, Any]:
        return self._get("/OfficeHours")

    def update_office_hours(self, data: Dict[str, Any]) -> None:
        self._patch("/OfficeHours", json=data)
