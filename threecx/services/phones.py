from __future__ import annotations

from typing import Any, Dict, Iterator, List, Optional

from ..models.phones import Phone, PhoneTemplate
from ..odata import ODataQuery
from .base import BaseService


class PhonesService(BaseService):
    """Manage provisioned phones and phone templates.

    Reference paths:
      GET    /Phones
      GET    /Phones({Id})
      PATCH  /Phones({Id})
      DELETE /Phones({Id})
      GET    /PhoneTemplates
      GET    /PhoneTemplates({Id})
      POST   /Users/Pbx.RebootPhone
      POST   /Users/Pbx.ReprovisionPhone
    """

    _PHONES = "/Phones"
    _TEMPLATES = "/PhoneTemplates"

    # ------------------------------------------------------------------
    # Phones
    # ------------------------------------------------------------------

    def list(self, query: Optional[ODataQuery] = None) -> List[Phone]:
        data = self._list_raw(self._PHONES, query)
        return [Phone.model_validate(item) for item in data.get("value", [])]

    def iterate(self, query: Optional[ODataQuery] = None) -> Iterator[Phone]:
        yield from self._paginate(self._PHONES, Phone, query)

    def get(self, phone_id: int, query: Optional[ODataQuery] = None) -> Phone:
        data = self._get(f"{self._PHONES}({phone_id})", params=self._query_params(query))
        return Phone.model_validate(data)

    def update(self, phone_id: int, changes: Phone | Dict[str, Any]) -> None:
        payload = changes.model_dump(by_alias=True, exclude_none=True) if isinstance(changes, Phone) else changes
        self._patch(f"{self._PHONES}({phone_id})", json=payload)

    def delete(self, phone_id: int, etag: Optional[str] = None) -> None:
        self._delete(f"{self._PHONES}({phone_id})", etag=etag)

    # ------------------------------------------------------------------
    # Phone templates
    # ------------------------------------------------------------------

    def list_templates(self, query: Optional[ODataQuery] = None) -> List[PhoneTemplate]:
        data = self._list_raw(self._TEMPLATES, query)
        return [PhoneTemplate.model_validate(item) for item in data.get("value", [])]

    def get_template(self, template_id: int) -> PhoneTemplate:
        data = self._get(f"{self._TEMPLATES}({template_id})")
        return PhoneTemplate.model_validate(data)

    # ------------------------------------------------------------------
    # Phone actions (triggered via Users service path)
    # ------------------------------------------------------------------

    def reboot(self, mac: str) -> None:
        """Reboot a phone by MAC address."""
        self._post("/Users/Pbx.RebootPhone", json={"MAC": mac})

    def reprovision(self, mac: str) -> None:
        """Reprovision a phone by MAC address."""
        self._post("/Users/Pbx.ReprovisionPhone", json={"MAC": mac})
