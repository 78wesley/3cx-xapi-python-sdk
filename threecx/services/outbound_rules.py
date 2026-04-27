from __future__ import annotations

from typing import Any, Dict, Iterator, List, Optional

from ..models.rules import OutboundRule
from ..odata import ODataQuery
from .base import BaseService


class OutboundRulesService(BaseService):
    _PATH = "/OutboundRules"

    def list(self, query: Optional[ODataQuery] = None) -> List[OutboundRule]:
        data = self._list_raw(self._PATH, query)
        return [OutboundRule.model_validate(item) for item in data.get("value", [])]

    def iterate(self, query: Optional[ODataQuery] = None) -> Iterator[OutboundRule]:
        yield from self._paginate(self._PATH, OutboundRule, query)

    def create(self, rule: OutboundRule | Dict[str, Any]) -> OutboundRule:
        payload = rule.model_dump(by_alias=True, exclude_none=True) if isinstance(rule, OutboundRule) else rule
        data = self._post(self._PATH, json=payload)
        return OutboundRule.model_validate(data)

    def get(self, rule_id: int, query: Optional[ODataQuery] = None) -> OutboundRule:
        data = self._get(f"{self._PATH}({rule_id})", params=self._query_params(query))
        return OutboundRule.model_validate(data)

    def update(self, rule_id: int, changes: OutboundRule | Dict[str, Any]) -> None:
        payload = changes.model_dump(by_alias=True, exclude_none=True) if isinstance(changes, OutboundRule) else changes
        self._patch(f"{self._PATH}({rule_id})", json=payload)

    def delete(self, rule_id: int) -> None:
        self._delete(f"{self._PATH}({rule_id})")

    def get_emergency_rules(self, query: Optional[ODataQuery] = None) -> List[OutboundRule]:
        data = self._get(f"{self._PATH}/Pbx.GetEmergencyOutboundRules()", params=self._query_params(query))
        return [OutboundRule.model_validate(item) for item in data.get("value", [])]

    def move_up_down(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.MoveUpDown", json=data)

    def purge(self) -> None:
        self._post(f"{self._PATH}/Pbx.Purge")
