from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Iterator, List, Optional

from ..models.system import LicenseStatus, Parameter, SystemParameters, SystemStatus
from ..odata import ODataQuery
from .base import BaseService


def _fmt_dt(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%S") + "+00:00"


class SystemService(BaseService):
    _PARAMS = "/Parameters"

    # ------------------------------------------------------------------
    # System status
    # ------------------------------------------------------------------

    def get_status(self) -> SystemStatus:
        data = self._get("/SystemStatus")
        return SystemStatus.model_validate(data)

    def get_api_token(self) -> str:
        data = self._get("/SystemStatus/Pbx.APIToken()")
        return str(data.get("value", ""))

    def get_remote_access_status(self) -> Dict[str, Any]:
        return self._get("/SystemStatus/Pbx.GetRemoteAccessStatus()")

    def get_version_type(self) -> str:
        data = self._get("/SystemStatus/Pbx.GetVersionType()")
        return str(data.get("value", ""))

    def is_request_help_enabled(self) -> bool:
        data = self._get("/SystemStatus/Pbx.IsRequestHelpEnabled()")
        return bool(data.get("value", data))

    def get_request_help_link(self, grant_period_days: int) -> str:
        data = self._get(f"/SystemStatus/Pbx.GetRequestHelpLink(grantPeriodDays={grant_period_days})")
        return str(data.get("value", ""))

    def get_system_database_info(self) -> Dict[str, Any]:
        return self._get("/SystemStatus/Pbx.SystemDatabaseInformation()")

    def get_system_extensions(self) -> Dict[str, Any]:
        return self._get("/SystemStatus/Pbx.SystemExtensions()")

    def get_system_health(self) -> Dict[str, Any]:
        return self._get("/SystemStatus/Pbx.SystemHealthStatus()")

    def get_system_telemetry(self) -> Dict[str, Any]:
        return self._get("/SystemStatus/Pbx.SystemTelemetry()")

    def get_service_telemetry(self) -> Dict[str, Any]:
        return self._get("/SystemStatus/Pbx.ServiceTelemetry()")

    def get_network_telemetry(self) -> Dict[str, Any]:
        return self._get("/SystemStatus/Pbx.NetworkTelemetry()")

    def get_my_phone_request_id_telemetry(self, start: datetime, end: datetime) -> List[Dict[str, Any]]:
        path = f"/SystemStatus/Pbx.MyPhoneRequestIdTelemetry(startDate={_fmt_dt(start)},endDate={_fmt_dt(end)})"
        data = self._get(path)
        return self._list_values(data) if isinstance(data, dict) else data

    def request_help(self, data: Dict[str, Any]) -> None:
        self._post("/SystemStatus/Pbx.RequestHelp", json=data)

    def revoke_remote_access(self) -> None:
        self._post("/SystemStatus/Pbx.RevokeRemoteAccess")

    def set_chat_log_status(self, data: Dict[str, Any]) -> None:
        self._post("/SystemStatus/Pbx.SetChatLogStatus", json=data)

    def set_multi_company_mode(self, data: Dict[str, Any]) -> None:
        self._post("/SystemStatus/Pbx.SetMultiCompanyMode", json=data)

    def start_db_maintenance(self) -> None:
        self._post("/SystemStatus/Pbx.StartDBMaintenance")

    # ------------------------------------------------------------------
    # License status
    # ------------------------------------------------------------------

    def get_license(self) -> LicenseStatus:
        data = self._get("/LicenseStatus")
        return LicenseStatus.model_validate(data)

    def refresh_license(self) -> None:
        self._post("/LicenseStatus/Pbx.RefreshLicenseStatus")

    def unlink_partner(self) -> None:
        self._post("/LicenseStatus/Pbx.UnlinkPartner")

    def link_partner(self, data: Dict[str, Any]) -> None:
        self._post("/LicenseStatus/Pbx.LinkPartner", json=data)

    def replace_license_key(self, data: Dict[str, Any]) -> None:
        self._post("/LicenseStatus/Pbx.ReplaceLicenseKey", json=data)

    def edit_license_info(self, data: Dict[str, Any]) -> None:
        self._post("/LicenseStatus/Pbx.EditLicenseInfo", json=data)

    def get_partner_info(self, reseller_id: str) -> Dict[str, Any]:
        return self._get(f"/LicenseStatus/Pbx.PartnerInfo(resellerId='{reseller_id}')")

    # ------------------------------------------------------------------
    # Parameters (legacy + CRUD)
    # ------------------------------------------------------------------

    def get_parameters(self, query: Optional[ODataQuery] = None) -> SystemParameters:
        """Legacy: return global PBX parameters as a typed object."""
        data = self._get(self._PARAMS, params=self._query_params(query))
        return SystemParameters.model_validate(data)

    def list_parameters(self, query: Optional[ODataQuery] = None) -> List[Parameter]:
        data = self._list_raw(self._PARAMS, query)
        return [Parameter.model_validate(item) for item in data.get("value", [])]

    def iterate_parameters(self, query: Optional[ODataQuery] = None) -> Iterator[Parameter]:
        yield from self._paginate(self._PARAMS, Parameter, query)

    def create_parameter(self, param: Parameter | Dict[str, Any]) -> Parameter:
        payload = param.model_dump(by_alias=True, exclude_none=True) if isinstance(param, Parameter) else param
        data = self._post(self._PARAMS, json=payload)
        return Parameter.model_validate(data)

    def get_parameter(self, param_id: int) -> Parameter:
        data = self._get(f"{self._PARAMS}({param_id})")
        return Parameter.model_validate(data)

    def update_parameter(self, param_id: int, changes: Parameter | Dict[str, Any]) -> None:
        payload = changes.model_dump(by_alias=True, exclude_none=True) if isinstance(changes, Parameter) else changes
        self._patch(f"{self._PARAMS}({param_id})", json=payload)

    def delete_parameter(self, param_id: int) -> None:
        self._delete(f"{self._PARAMS}({param_id})")

    def get_parameter_by_name(self, name: str) -> Parameter:
        data = self._get(f"{self._PARAMS}/Pbx.GetParameterByName(name='{name}')")
        return Parameter.model_validate(data)

    # ------------------------------------------------------------------
    # Escape hatches
    # ------------------------------------------------------------------

    def get_raw(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._get(path, params=params)

    def post_raw(self, path: str, json: Any = None) -> Any:
        return self._post(path, json=json)
