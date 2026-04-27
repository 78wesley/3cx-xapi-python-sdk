from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..odata import ODataQuery
from .base import BaseService


class DefsService(BaseService):

    def get_defs(self) -> Dict[str, Any]:
        return self._get("/Defs")

    def list_codecs(self, query: Optional[ODataQuery] = None) -> List[Dict[str, Any]]:
        data = self._get("/Defs/Codecs", params=self._query_params(query))
        return self._list_values(data) if isinstance(data, dict) else data

    def list_gateway_parameters(self, query: Optional[ODataQuery] = None) -> List[Dict[str, Any]]:
        data = self._get("/Defs/GatewayParameters", params=self._query_params(query))
        return self._list_values(data) if isinstance(data, dict) else data

    def list_gateway_parameter_values(self, query: Optional[ODataQuery] = None) -> List[Dict[str, Any]]:
        data = self._get("/Defs/GatewayParameterValues", params=self._query_params(query))
        return self._list_values(data) if isinstance(data, dict) else data

    def list_timezones(self, query: Optional[ODataQuery] = None) -> List[Dict[str, Any]]:
        data = self._get("/Defs/TimeZones", params=self._query_params(query))
        return self._list_values(data) if isinstance(data, dict) else data

    def get_system_parameters(self) -> Dict[str, Any]:
        return self._get("/Defs/Pbx.GetSystemParameters()")

    def get_license_parameters(self) -> Dict[str, Any]:
        return self._get("/Defs/Pbx.GetLicenseParameters()")

    def has_system_owner(self) -> bool:
        data = self._get("/Defs/Pbx.HasSystemOwner()")
        return bool(data.get("value", data))

    def get_routes(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        result = self._post("/Defs/Pbx.GetRoutes", json=data)
        return self._list_values(result) if isinstance(result, dict) else result

    def send_email(self, data: Dict[str, Any]) -> None:
        self._post("/Defs/Pbx.SendEmail", json=data)

    def list_countries(self, query: Optional[ODataQuery] = None) -> List[Dict[str, Any]]:
        data = self._get("/Countries", params=self._query_params(query))
        return self._list_values(data) if isinstance(data, dict) else data

    def list_did_numbers(self, query: Optional[ODataQuery] = None) -> List[Dict[str, Any]]:
        data = self._get("/DidNumbers", params=self._query_params(query))
        return self._list_values(data) if isinstance(data, dict) else data
