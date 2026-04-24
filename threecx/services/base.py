from __future__ import annotations

from typing import Any, Dict, Iterator, List, Optional, Type, TypeVar

import httpx

from ..exceptions import raise_for_status
from ..odata import ODataQuery

T = TypeVar("T")

_SENTINEL = object()


class BaseService:
    """Shared HTTP helpers used by every resource service."""

    def __init__(self, http: httpx.Client) -> None:
        self._http = http

    # ------------------------------------------------------------------
    # Low-level request helpers
    # ------------------------------------------------------------------

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        response = self._http.get(path, params=params)
        self._raise(response)
        if response.status_code == 204:
            return None
        return response.json()

    def _post(self, path: str, json: Any = None, params: Optional[Dict[str, Any]] = None) -> Any:
        response = self._http.post(path, json=json, params=params)
        self._raise(response)
        if response.status_code == 204:
            return None
        return response.json()

    def _patch(self, path: str, json: Any) -> None:
        response = self._http.patch(path, json=json)
        self._raise(response)

    def _delete(self, path: str, etag: Optional[str] = None) -> None:
        headers = {"If-Match": etag} if etag else {}
        response = self._http.delete(path, headers=headers)
        self._raise(response)

    @staticmethod
    def _raise(response: httpx.Response) -> None:
        if response.is_error:
            try:
                body = response.json()
            except Exception:
                body = response.text
            raise_for_status(response.status_code, body)

    # ------------------------------------------------------------------
    # OData helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _query_params(query: Optional[ODataQuery]) -> Dict[str, Any]:
        return query.to_params() if query else {}

    def _list_raw(self, path: str, query: Optional[ODataQuery] = None) -> Dict[str, Any]:
        return self._get(path, params=self._query_params(query))

    def _paginate(
        self,
        path: str,
        model: Type[T],
        query: Optional[ODataQuery] = None,
    ) -> Iterator[T]:
        """Yield all items across OData pages."""
        params: Optional[Dict[str, Any]] = self._query_params(query) or None
        while path:
            data = self._get(path, params=params)
            for item in data.get("value", []):
                yield model.model_validate(item)
            path = data.get("@odata.nextLink")
            # nextLink is a full URL with query string already embedded;
            # passing params={} to httpx strips the query string, so use None.
            params = None
