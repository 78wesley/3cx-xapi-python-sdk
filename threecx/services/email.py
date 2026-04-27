from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..odata import ODataQuery
from .base import BaseService


class EmailService(BaseService):
    _PATH = "/EmailTemplate"

    def list_templates(self, query: Optional[ODataQuery] = None) -> List[Dict[str, Any]]:
        data = self._list_raw(self._PATH, query)
        return self._list_values(data)

    def get_template(self, path: str) -> Dict[str, Any]:
        return self._get(f"{self._PATH}('{path}')")

    def update_template(self, path: str, data: Dict[str, Any]) -> None:
        self._patch(f"{self._PATH}('{path}')", json=data)

    def set_template_default(self, path: str) -> None:
        self._post(f"{self._PATH}('{path}')/Pbx.SetDefault")
