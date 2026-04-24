from __future__ import annotations

from typing import Iterator, List, Optional

from ..models.calls import ActiveCall
from ..odata import ODataQuery
from .base import BaseService


class ActiveCallsService(BaseService):
    """Manage and inspect currently active calls.

    Reference paths:
      GET  /ActiveCalls
      POST /ActiveCalls({Id})/Pbx.DropCall
    """

    _PATH = "/ActiveCalls"

    def list(self, query: Optional[ODataQuery] = None) -> List[ActiveCall]:
        """Return all active calls (single page)."""
        data = self._list_raw(self._PATH, query)
        return [ActiveCall.model_validate(item) for item in data.get("value", [])]

    def iterate(self, query: Optional[ODataQuery] = None) -> Iterator[ActiveCall]:
        """Yield active calls across all OData pages."""
        yield from self._paginate(self._PATH, ActiveCall, query)

    def drop(self, call_id: int) -> None:
        """Forcefully drop an active call by its ID."""
        self._post(f"{self._PATH}({call_id})/Pbx.DropCall")
