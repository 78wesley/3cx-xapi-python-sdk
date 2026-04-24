from __future__ import annotations

from typing import Iterator, List, Optional

from ..models.calls import CallHistoryEntry
from ..odata import ODataQuery
from .base import BaseService


class CallHistoryService(BaseService):
    """Query the call history log.

    Reference paths:
      GET /CallHistoryView
    """

    _PATH = "/CallHistoryView"

    def list(self, query: Optional[ODataQuery] = None) -> List[CallHistoryEntry]:
        """Return a single page of call history entries."""
        data = self._list_raw(self._PATH, query)
        return [CallHistoryEntry.model_validate(item) for item in data.get("value", [])]

    def iterate(self, query: Optional[ODataQuery] = None) -> Iterator[CallHistoryEntry]:
        """Yield call history entries across all OData pages."""
        yield from self._paginate(self._PATH, CallHistoryEntry, query)

    def count(self, query: Optional[ODataQuery] = None) -> int:
        """Return the total number of call history records matching *query*."""
        q = (query or ODataQuery()).count().top(0)
        data = self._list_raw(self._PATH, q)
        return data.get("@odata.count", 0)
