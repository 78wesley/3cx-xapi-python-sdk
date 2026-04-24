from __future__ import annotations

from typing import Any, Dict, Iterator, List, Optional

from ..models.queues import RingGroup, RingGroupMember
from ..odata import ODataQuery
from .base import BaseService


class RingGroupsService(BaseService):
    """CRUD operations for ring groups.

    Reference paths:
      GET    /RingGroups
      POST   /RingGroups
      GET    /RingGroups({Id})
      PATCH  /RingGroups({Id})
      DELETE /RingGroups({Id})
    """

    _PATH = "/RingGroups"

    def list(self, query: Optional[ODataQuery] = None) -> List[RingGroup]:
        data = self._list_raw(self._PATH, query)
        return [RingGroup.model_validate(item) for item in data.get("value", [])]

    def iterate(self, query: Optional[ODataQuery] = None) -> Iterator[RingGroup]:
        yield from self._paginate(self._PATH, RingGroup, query)

    def create(self, ring_group: RingGroup | Dict[str, Any]) -> RingGroup:
        payload = (
            ring_group.model_dump(by_alias=True, exclude_none=True)
            if isinstance(ring_group, RingGroup)
            else ring_group
        )
        data = self._post(self._PATH, json=payload)
        return RingGroup.model_validate(data)

    def get(self, group_id: int, query: Optional[ODataQuery] = None) -> RingGroup:
        data = self._get(f"{self._PATH}({group_id})", params=self._query_params(query))
        return RingGroup.model_validate(data)

    def update(self, group_id: int, changes: RingGroup | Dict[str, Any]) -> None:
        payload = (
            changes.model_dump(by_alias=True, exclude_none=True)
            if isinstance(changes, RingGroup)
            else changes
        )
        self._patch(f"{self._PATH}({group_id})", json=payload)

    def delete(self, group_id: int, etag: Optional[str] = None) -> None:
        self._delete(f"{self._PATH}({group_id})", etag=etag)
