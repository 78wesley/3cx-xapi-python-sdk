from __future__ import annotations

from typing import Any, Dict, Iterator, List, Optional

from ..models.rules import InboundRule
from ..odata import ODataQuery
from .base import BaseService


class InboundRulesService(BaseService):
    _PATH = "/InboundRules"

    def list(self, query: Optional[ODataQuery] = None) -> List[InboundRule]:
        data = self._list_raw(self._PATH, query)
        return [InboundRule.model_validate(item) for item in data.get("value", [])]

    def iterate(self, query: Optional[ODataQuery] = None) -> Iterator[InboundRule]:
        yield from self._paginate(self._PATH, InboundRule, query)

    def create(self, rule: InboundRule | Dict[str, Any]) -> InboundRule:
        payload = rule.model_dump(by_alias=True, exclude_none=True) if isinstance(rule, InboundRule) else rule
        data = self._post(self._PATH, json=payload)
        return InboundRule.model_validate(data)

    def get(self, rule_id: int, query: Optional[ODataQuery] = None) -> InboundRule:
        data = self._get(f"{self._PATH}({rule_id})", params=self._query_params(query))
        return InboundRule.model_validate(data)

    def update(self, rule_id: int, changes: InboundRule | Dict[str, Any]) -> None:
        payload = changes.model_dump(by_alias=True, exclude_none=True) if isinstance(changes, InboundRule) else changes
        self._patch(f"{self._PATH}({rule_id})", json=payload)

    def delete(self, rule_id: int) -> None:
        self._delete(f"{self._PATH}({rule_id})")

    def bulk_delete(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.BulkInboundRulesDelete", json=data)

    def export_caller_id_rules(self) -> List[Dict[str, Any]]:
        data = self._get(f"{self._PATH}/Pbx.ExportCallerIdRules()")
        return self._list_values(data) if isinstance(data, dict) else data
