from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Iterator, List, Optional

from ..odata import ODataQuery
from .base import BaseService


def _fmt_dt(dt: datetime) -> str:
    """Format a datetime to the ISO-8601 pattern expected by 3CX path parameters."""
    return dt.strftime("%Y-%m-%dT%H:%M:%S") + "+00:00"


class ReportsService(BaseService):
    """Access 3CX reporting endpoints.

    All report methods return raw dicts — the raw API JSON is returned because
    the report schemas are highly specialised.  Pass the result to a Pydantic
    model of your choice or consume the dict directly.

    Reference paths (selection):
      GET /ReportCallLogData/Pbx.GetCallLogData(...)
      GET /ReportExtensionStatistics/Pbx.GetExtensionStatistics(...)
      GET /ReportQueuePerformanceOverview/Pbx.GetQueuePerformanceOverview(...)
      GET /ReportAgentLoginHistory/Pbx.GetAgentLoginHistory(...)
      GET /ActivityLog/Pbx.GetLogs(...)
      GET /ActivityLog/Pbx.GetFilter()
    """

    # ------------------------------------------------------------------
    # Call log
    # ------------------------------------------------------------------

    def get_call_log(
        self,
        start: datetime,
        end: datetime,
        *,
        query: Optional[ODataQuery] = None,
    ) -> List[Dict[str, Any]]:
        """Return call log entries between *start* and *end* (UTC)."""
        path = (
            f"/ReportCallLogData/Pbx.GetCallLogData("
            f"periodFrom={_fmt_dt(start)},periodTo={_fmt_dt(end)})"
        )
        data = self._get(path, params=self._query_params(query))
        return data.get("value", data)

    # ------------------------------------------------------------------
    # Extension statistics
    # ------------------------------------------------------------------

    def get_extension_statistics(
        self,
        start: datetime,
        end: datetime,
        *,
        query: Optional[ODataQuery] = None,
    ) -> List[Dict[str, Any]]:
        path = (
            f"/ReportExtensionStatistics/Pbx.GetExtensionStatistics("
            f"periodFrom={_fmt_dt(start)},periodTo={_fmt_dt(end)})"
        )
        data = self._get(path, params=self._query_params(query))
        return data.get("value", data)

    # ------------------------------------------------------------------
    # Queue performance
    # ------------------------------------------------------------------

    def get_queue_performance_overview(
        self,
        start: datetime,
        end: datetime,
        *,
        query: Optional[ODataQuery] = None,
    ) -> List[Dict[str, Any]]:
        path = (
            f"/ReportQueuePerformanceOverview/Pbx.GetQueuePerformanceOverview("
            f"periodFrom={_fmt_dt(start)},periodTo={_fmt_dt(end)})"
        )
        data = self._get(path, params=self._query_params(query))
        return data.get("value", data)

    def get_queue_performance_totals(
        self,
        start: datetime,
        end: datetime,
        *,
        query: Optional[ODataQuery] = None,
    ) -> List[Dict[str, Any]]:
        path = (
            f"/ReportQueuePerformanceTotals/Pbx.GetQueuePerformanceTotals("
            f"periodFrom={_fmt_dt(start)},periodTo={_fmt_dt(end)})"
        )
        data = self._get(path, params=self._query_params(query))
        return data.get("value", data)

    # ------------------------------------------------------------------
    # Agent login history
    # ------------------------------------------------------------------

    def get_agent_login_history(
        self,
        start: datetime,
        end: datetime,
        *,
        query: Optional[ODataQuery] = None,
    ) -> List[Dict[str, Any]]:
        path = (
            f"/ReportAgentLoginHistory/Pbx.GetAgentLoginHistory("
            f"periodFrom={_fmt_dt(start)},periodTo={_fmt_dt(end)})"
        )
        data = self._get(path, params=self._query_params(query))
        return data.get("value", data)

    # ------------------------------------------------------------------
    # Activity log
    # ------------------------------------------------------------------

    def get_activity_log_filter(self) -> Dict[str, Any]:
        return self._get("/ActivityLog/Pbx.GetFilter()")

    def get_activity_logs(
        self,
        start: datetime,
        end: datetime,
        *,
        extension: Optional[str] = None,
        call: Optional[str] = None,
        severity: Optional[str] = None,
        query: Optional[ODataQuery] = None,
    ) -> List[Dict[str, Any]]:
        ext = f"'{extension}'" if extension else "null"
        cal = f"'{call}'" if call else "null"
        sev = f"'{severity}'" if severity else "null"
        path = (
            f"/ActivityLog/Pbx.GetLogs("
            f"startDate={_fmt_dt(start)},endDate={_fmt_dt(end)},"
            f"extension={ext},call={cal},severity={sev})"
        )
        data = self._get(path, params=self._query_params(query))
        return data.get("value", data)

    def purge_activity_logs(self) -> None:
        self._post("/ActivityLog/Pbx.PurgeLogs")

    # ------------------------------------------------------------------
    # Abandoned queue calls
    # ------------------------------------------------------------------

    def get_abandoned_queue_calls(
        self,
        start: datetime,
        end: datetime,
        *,
        query: Optional[ODataQuery] = None,
    ) -> List[Dict[str, Any]]:
        path = (
            f"/ReportAbandonedQueueCalls/Pbx.GetAbandonedQueueCalls("
            f"periodFrom={_fmt_dt(start)},periodTo={_fmt_dt(end)})"
        )
        data = self._get(path, params=self._query_params(query))
        return data.get("value", data)
