from __future__ import annotations

from typing import Any


class ODataQuery:
    """Fluent builder for OData v4 query parameters.

    Example::

        q = (
            ODataQuery()
            .filter("FirstName eq 'John'")
            .select("Id", "FirstName", "LastName", "Email")
            .expand("Groups")
            .order_by("LastName")
            .top(25)
            .skip(0)
            .count()
        )
        users = client.users.list(query=q)
    """

    def __init__(self) -> None:
        self._params: dict[str, Any] = {}

    # --- pagination -----------------------------------------------------------

    def top(self, n: int) -> ODataQuery:
        self._params["$top"] = n
        return self

    def skip(self, n: int) -> ODataQuery:
        self._params["$skip"] = n
        return self

    def count(self, include: bool = True) -> ODataQuery:
        self._params["$count"] = str(include).lower()
        return self

    # --- projection / expansion -----------------------------------------------

    def select(self, *fields: str) -> ODataQuery:
        self._params["$select"] = ",".join(fields)
        return self

    def expand(self, *relations: str) -> ODataQuery:
        self._params["$expand"] = ",".join(relations)
        return self

    # --- filtering / ordering -------------------------------------------------

    def filter(self, expression: str) -> ODataQuery:
        self._params["$filter"] = expression
        return self

    def search(self, phrase: str) -> ODataQuery:
        self._params["$search"] = phrase
        return self

    def order_by(self, *fields: str) -> ODataQuery:
        self._params["$orderby"] = ",".join(fields)
        return self

    # --- serialisation --------------------------------------------------------

    def to_params(self) -> dict[str, Any]:
        return dict(self._params)

    def __repr__(self) -> str:
        return f"ODataQuery({self._params!r})"
