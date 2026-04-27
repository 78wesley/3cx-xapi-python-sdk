from __future__ import annotations

from typing import Any, Dict, Iterator, List, Optional

from ..models.website_links import Weblink
from ..odata import ODataQuery
from .base import BaseService


class WebsiteLinksService(BaseService):
    _PATH = "/WebsiteLinks"

    def list(self, query: Optional[ODataQuery] = None) -> List[Weblink]:
        data = self._list_raw(self._PATH, query)
        return [Weblink(**item) for item in data.get("value", [])]

    def iterate(self, query: Optional[ODataQuery] = None) -> Iterator[Weblink]:
        yield from self._paginate(self._PATH, Weblink, query)

    def create(self, data: Dict[str, Any]) -> Weblink:
        return Weblink(**self._post(self._PATH, json=data))

    def get(self, link: str) -> Weblink:
        return Weblink(**self._get(f"{self._PATH}('{link}')"))

    def update(self, link: str, changes: Dict[str, Any]) -> None:
        self._patch(f"{self._PATH}('{link}')", json=changes)

    def delete(self, link: str) -> None:
        self._delete(f"{self._PATH}('{link}')")

    def bulk_delete(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.BulkLinksDelete", json=data)

    def validate_link(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._post(f"{self._PATH}/Pbx.ValidateLink", json=data)
