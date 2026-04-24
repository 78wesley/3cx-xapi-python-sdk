from __future__ import annotations

from typing import Any, Dict, Optional

from ..models.system import LicenseStatus, SystemParameters, SystemStatus
from ..odata import ODataQuery
from .base import BaseService


class SystemService(BaseService):
    """Read-only access to system status, license, and global PBX parameters.

    Reference paths:
      GET /SystemStatus
      GET /LicenseStatus
      GET /Parameters
      GET /Parameters/Pbx.GetSystemStatus()
    """

    def get_status(self) -> SystemStatus:
        """Return current PBX system status (CPU, memory, call counts, etc.)."""
        data = self._get("/SystemStatus")
        return SystemStatus.model_validate(data)

    def get_license(self) -> LicenseStatus:
        """Return the current license / subscription status."""
        data = self._get("/LicenseStatus")
        return LicenseStatus.model_validate(data)

    def get_parameters(self, query: Optional[ODataQuery] = None) -> SystemParameters:
        """Return global PBX parameters (FQDN, ports, IPs, etc.)."""
        data = self._get("/Parameters", params=self._query_params(query))
        return SystemParameters.model_validate(data)

    def get_raw(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Escape hatch: perform an arbitrary GET against the XAPI."""
        return self._get(path, params=params)

    def post_raw(self, path: str, json: Any = None) -> Any:
        """Escape hatch: perform an arbitrary POST against the XAPI."""
        return self._post(path, json=json)
