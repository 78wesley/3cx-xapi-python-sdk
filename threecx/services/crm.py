from __future__ import annotations

from typing import Any, Dict, List

from .base import BaseService


class CrmService(BaseService):
    _PATH = "/CrmIntegration"

    def get_integration(self) -> Dict[str, Any]:
        return self._get(self._PATH)

    def update_integration(self, data: Dict[str, Any]) -> None:
        self._patch(self._PATH, json=data)

    def delete_crm_contacts(self) -> None:
        self._post(f"{self._PATH}/Pbx.DeleteCrmContacts")

    def get_crm_template_source(self, name: str) -> str:
        data = self._get(f"{self._PATH}/Pbx.GetCrmTemplateSource(name='{name}')")
        return str(data.get("value", ""))

    def get_oauth(self, variable: str) -> Dict[str, Any]:
        return self._get(f"{self._PATH}/Pbx.GetOAuth(variable='{variable}')")

    def set_oauth_state(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.SetOAuthState", json=data)

    def test_integration(self) -> Dict[str, Any]:
        return self._post(f"{self._PATH}/Pbx.Test")

    # ------------------------------------------------------------------
    # CRM templates
    # ------------------------------------------------------------------

    def list_templates(self) -> List[Dict[str, Any]]:
        data = self._get("/CrmTemplates/Pbx.GeCrmtTemplates()")
        return self._list_values(data) if isinstance(data, dict) else data

    def get_template(self, name: str) -> Dict[str, Any]:
        return self._get(f"/CrmTemplates('{name}')")

    def delete_template(self, name: str) -> None:
        self._delete(f"/CrmTemplates('{name}')")
