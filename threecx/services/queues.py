from __future__ import annotations

from typing import Any, Dict, Iterator, List, Optional

from ..models.queues import Queue, QueueAgent, QueueManager
from ..odata import ODataQuery
from .base import BaseService


class QueuesService(BaseService):
    """CRUD operations for call queues.

    Reference paths:
      GET    /Queues
      POST   /Queues
      GET    /Queues({Id})
      GET    /Queues(Number={Number})
      PATCH  /Queues({Id})
      DELETE /Queues({Id})
      GET    /Queues({Id})/Agents
      GET    /Queues({Id})/Managers
      POST   /Queues({Id})/Pbx.ResetQueueStatistics
    """

    _PATH = "/Queues"

    def list(self, query: Optional[ODataQuery] = None) -> List[Queue]:
        data = self._list_raw(self._PATH, query)
        return [Queue.model_validate(item) for item in data.get("value", [])]

    def iterate(self, query: Optional[ODataQuery] = None) -> Iterator[Queue]:
        yield from self._paginate(self._PATH, Queue, query)

    def create(self, queue: Queue | Dict[str, Any]) -> Queue:
        payload = queue.model_dump(by_alias=True, exclude_none=True) if isinstance(queue, Queue) else queue
        data = self._post(self._PATH, json=payload)
        return Queue.model_validate(data)

    def get(self, queue_id: int, query: Optional[ODataQuery] = None) -> Queue:
        data = self._get(f"{self._PATH}({queue_id})", params=self._query_params(query))
        return Queue.model_validate(data)

    def get_by_number(self, number: str, query: Optional[ODataQuery] = None) -> Queue:
        data = self._get(f"{self._PATH}(Number='{number}')", params=self._query_params(query))
        return Queue.model_validate(data)

    def update(self, queue_id: int, changes: Queue | Dict[str, Any]) -> None:
        payload = changes.model_dump(by_alias=True, exclude_none=True) if isinstance(changes, Queue) else changes
        self._patch(f"{self._PATH}({queue_id})", json=payload)

    def delete(self, queue_id: int, etag: Optional[str] = None) -> None:
        self._delete(f"{self._PATH}({queue_id})", etag=etag)

    # ------------------------------------------------------------------
    # Sub-resources
    # ------------------------------------------------------------------

    def get_agents(self, queue_id: int) -> List[QueueAgent]:
        data = self._get(f"{self._PATH}({queue_id})/Agents")
        return [QueueAgent.model_validate(item) for item in data.get("value", [])]

    def get_managers(self, queue_id: int) -> List[QueueManager]:
        data = self._get(f"{self._PATH}({queue_id})/Managers")
        return [QueueManager.model_validate(item) for item in data.get("value", [])]

    def reset_statistics(self, queue_id: int) -> None:
        self._post(f"{self._PATH}({queue_id})/Pbx.ResetQueueStatistics")
