from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Iterator, List, Optional

from ..odata import ODataQuery
from .base import BaseService


def _fmt_dt(dt: datetime) -> str:
    """Format datetime to ISO-8601 pattern expected by 3CX path parameters."""
    return dt.strftime("%Y-%m-%dT%H:%M:%S") + "+00:00"


def _s(v: Optional[str], default: str = "null") -> str:
    return f"'{v}'" if v is not None else default


def _b(v: bool) -> str:
    return "true" if v else "false"


class ReportsService(BaseService):
    """Access 3CX reporting endpoints. All methods return raw dicts."""

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
        path = (
            f"/ReportCallLogData/Pbx.GetCallLogData("
            f"periodFrom={_fmt_dt(start)},periodTo={_fmt_dt(end)},"
            f"sourceType=0,sourceFilter='',destinationType=0,destinationFilter='',"
            f"callsType=0,callTimeFilterType=0,callTimeFilterFrom={_fmt_dt(start)},"
            f"callTimeFilterTo={_fmt_dt(end)},hidePcalls=false)"
        )
        data = self._get(path, params=self._query_params(query))
        return self._list_values(data)

    def get_call_log_full(
        self,
        start: datetime,
        end: datetime,
        source_type: int = 0,
        source_filter: str = "",
        destination_type: int = 0,
        destination_filter: str = "",
        calls_type: int = 0,
        call_time_filter_type: int = 0,
        call_time_filter_from: Optional[datetime] = None,
        call_time_filter_to: Optional[datetime] = None,
        hide_pcalls: bool = False,
        *,
        query: Optional[ODataQuery] = None,
    ) -> List[Dict[str, Any]]:
        tf_from = call_time_filter_from or start
        tf_to = call_time_filter_to or end
        path = (
            f"/ReportCallLogData/Pbx.GetCallLogData("
            f"periodFrom={_fmt_dt(start)},periodTo={_fmt_dt(end)},"
            f"sourceType={source_type},sourceFilter='{source_filter}',"
            f"destinationType={destination_type},destinationFilter='{destination_filter}',"
            f"callsType={calls_type},callTimeFilterType={call_time_filter_type},"
            f"callTimeFilterFrom={_fmt_dt(tf_from)},callTimeFilterTo={_fmt_dt(tf_to)},"
            f"hidePcalls={_b(hide_pcalls)})"
        )
        data = self._get(path, params=self._query_params(query))
        return self._list_values(data)

    # ------------------------------------------------------------------
    # Extension statistics
    # ------------------------------------------------------------------

    def get_extension_statistics(
        self,
        start: datetime,
        end: datetime,
        extension_filter: str = "",
        call_area: int = 0,
        *,
        query: Optional[ODataQuery] = None,
    ) -> List[Dict[str, Any]]:
        path = (
            f"/ReportExtensionStatistics/Pbx.GetExtensionStatisticsData("
            f"periodFrom={_fmt_dt(start)},periodTo={_fmt_dt(end)},"
            f"extensionFilter='{extension_filter}',callArea={call_area})"
        )
        data = self._get(path, params=self._query_params(query))
        return self._list_values(data)

    def get_extension_statistics_by_group(
        self,
        group_number: str,
        start: datetime,
        end: datetime,
        call_area: int = 0,
        *,
        query: Optional[ODataQuery] = None,
    ) -> List[Dict[str, Any]]:
        path = (
            f"/ReportExtensionStatisticsByGroup/Pbx.GetExtensionStatisticsByGroupData("
            f"groupNumber='{group_number}',periodFrom={_fmt_dt(start)},periodTo={_fmt_dt(end)},"
            f"callArea={call_area})"
        )
        data = self._get(path, params=self._query_params(query))
        return self._list_values(data)

    def get_extension_statistics_by_ring_groups(
        self,
        start: datetime,
        end: datetime,
        ring_group_dns: str = "",
        *,
        query: Optional[ODataQuery] = None,
    ) -> List[Dict[str, Any]]:
        path = (
            f"/ReportExtensionsStatisticsByRingGroups/Pbx.GetExtensionsStatisticsByRingGroupsData("
            f"periodFrom={_fmt_dt(start)},periodTo={_fmt_dt(end)},ringGroupDns='{ring_group_dns}')"
        )
        data = self._get(path, params=self._query_params(query))
        return self._list_values(data)

    # ------------------------------------------------------------------
    # Queue performance
    # ------------------------------------------------------------------

    def get_queue_performance_overview(
        self,
        start: datetime,
        end: datetime,
        queue_dns: str = "",
        wait_interval: int = 0,
        *,
        query: Optional[ODataQuery] = None,
    ) -> List[Dict[str, Any]]:
        path = (
            f"/ReportQueuePerformanceOverview/Pbx.GetQueuePerformanceOverviewData("
            f"periodFrom={_fmt_dt(start)},periodTo={_fmt_dt(end)},"
            f"queueDns='{queue_dns}',waitInterval={wait_interval})"
        )
        data = self._get(path, params=self._query_params(query))
        return self._list_values(data)

    def get_queue_performance_totals(
        self,
        start: datetime,
        end: datetime,
        queue_dns: str = "",
        wait_interval: int = 0,
        *,
        query: Optional[ODataQuery] = None,
    ) -> List[Dict[str, Any]]:
        path = (
            f"/ReportQueuePerformanceTotals/Pbx.GetQueuePerformanceTotalsData("
            f"periodFrom={_fmt_dt(start)},periodTo={_fmt_dt(end)},"
            f"queueDns='{queue_dns}',waitInterval={wait_interval})"
        )
        data = self._get(path, params=self._query_params(query))
        return self._list_values(data)

    def get_detailed_queue_statistics(
        self,
        queue_dns: str,
        start: datetime,
        end: datetime,
        wait_interval: int = 0,
        *,
        query: Optional[ODataQuery] = None,
    ) -> List[Dict[str, Any]]:
        path = (
            f"/ReportDetailedQueueStatistics/Pbx.GetDetailedQueueStatisticsData("
            f"queueDnStr='{queue_dns}',startDt={_fmt_dt(start)},endDt={_fmt_dt(end)},"
            f"waitInterval={wait_interval})"
        )
        data = self._get(path, params=self._query_params(query))
        return self._list_values(data)

    def get_queue_agents_statistics(
        self,
        queue_dns: str,
        start: datetime,
        end: datetime,
        wait_interval: int = 0,
        *,
        query: Optional[ODataQuery] = None,
    ) -> List[Dict[str, Any]]:
        path = (
            f"/ReportAgentsInQueueStatistics/Pbx.GetAgentsInQueueStatisticsData("
            f"queueDnStr='{queue_dns}',startDt={_fmt_dt(start)},endDt={_fmt_dt(end)},"
            f"waitInterval={wait_interval})"
        )
        data = self._get(path, params=self._query_params(query))
        return self._list_values(data)

    def get_queue_agents_chat_statistics(
        self,
        queue_dns: str,
        start: datetime,
        end: datetime,
        participant_type: int = 0,
        *,
        query: Optional[ODataQuery] = None,
    ) -> List[Dict[str, Any]]:
        path = (
            f"/ReportQueueAgentsChatStatistics/Pbx.GetQueueAgentsChatStatisticsData("
            f"queueDnStr='{queue_dns}',startDt={_fmt_dt(start)},endDt={_fmt_dt(end)},"
            f"participantType={participant_type})"
        )
        data = self._get(path, params=self._query_params(query))
        return self._list_values(data)

    def get_queue_agents_chat_statistics_totals(
        self,
        queue_dns: str,
        start: datetime,
        end: datetime,
        participant_type: int = 0,
        *,
        query: Optional[ODataQuery] = None,
    ) -> List[Dict[str, Any]]:
        path = (
            f"/ReportQueueAgentsChatStatisticsTotals/Pbx.GetQueueAgentsChatStatisticsTotalsData("
            f"queueDnStr='{queue_dns}',startDt={_fmt_dt(start)},endDt={_fmt_dt(end)},"
            f"participantType={participant_type})"
        )
        data = self._get(path, params=self._query_params(query))
        return self._list_values(data)

    def get_queue_callbacks(
        self,
        queue_dns: str,
        start: datetime,
        end: datetime,
        *,
        query: Optional[ODataQuery] = None,
    ) -> List[Dict[str, Any]]:
        path = (
            f"/ReportQueueCallbacks/Pbx.GetQueueCallbacksData("
            f"queueDnStr='{queue_dns}',startDt={_fmt_dt(start)},endDt={_fmt_dt(end)})"
        )
        data = self._get(path, params=self._query_params(query))
        return self._list_values(data)

    def get_queue_chat_performance(
        self,
        queue_dns: str,
        start: datetime,
        end: datetime,
        participant_type: int = 0,
        *,
        query: Optional[ODataQuery] = None,
    ) -> List[Dict[str, Any]]:
        path = (
            f"/ReportQueueChatPerformance/Pbx.GetQueueChatPerformanceData("
            f"queueDnStr='{queue_dns}',startDt={_fmt_dt(start)},endDt={_fmt_dt(end)},"
            f"participantType={participant_type})"
        )
        data = self._get(path, params=self._query_params(query))
        return self._list_values(data)

    def get_queue_failed_callbacks(
        self,
        queue_dns: str,
        start: datetime,
        end: datetime,
        *,
        query: Optional[ODataQuery] = None,
    ) -> List[Dict[str, Any]]:
        path = (
            f"/ReportQueueFailedCallbacks/Pbx.GetQueueFailedCallbacksData("
            f"queueDnStr='{queue_dns}',startDt={_fmt_dt(start)},endDt={_fmt_dt(end)})"
        )
        data = self._get(path, params=self._query_params(query))
        return self._list_values(data)

    def get_queue_an_un_calls(
        self,
        chart_date: datetime,
        chart_by: int,
        queue_dns: str,
        client_timezone: str = "UTC",
        wait_interval: int = 0,
        *,
        query: Optional[ODataQuery] = None,
    ) -> List[Dict[str, Any]]:
        path = (
            f"/ReportQueueAnUnCalls/Pbx.GetQueueAnUnCallsData("
            f"chartDate={_fmt_dt(chart_date)},chartBy={chart_by},"
            f"queueDnStr='{queue_dns}',clientTimeZone='{client_timezone}',"
            f"waitInterval={wait_interval})"
        )
        data = self._get(path, params=self._query_params(query))
        return self._list_values(data)

    def get_queue_answered_calls_by_wait_time(
        self,
        queue_dns: str,
        start: datetime,
        end: datetime,
        answer_interval: int = 0,
        *,
        query: Optional[ODataQuery] = None,
    ) -> List[Dict[str, Any]]:
        path = (
            f"/ReportQueueAnsweredCallsByWaitTime/Pbx.GetQueueAnsweredCallsByWaitTimeData("
            f"queueDnStr='{queue_dns}',startDt={_fmt_dt(start)},endDt={_fmt_dt(end)},"
            f"answerInterval={answer_interval})"
        )
        data = self._get(path, params=self._query_params(query))
        return self._list_values(data)

    def get_team_queue_general_statistics(
        self,
        queue_dns: str,
        start: datetime,
        end: datetime,
        wait_interval: int = 0,
        *,
        query: Optional[ODataQuery] = None,
    ) -> List[Dict[str, Any]]:
        path = (
            f"/ReportTeamQueueGeneralStatistics/Pbx.GetTeamQueueGeneralStatisticsData("
            f"queueDnStr='{queue_dns}',startDt={_fmt_dt(start)},endDt={_fmt_dt(end)},"
            f"waitInterval={wait_interval})"
        )
        data = self._get(path, params=self._query_params(query))
        return self._list_values(data)

    def get_breaches_sla(
        self,
        queue_dns: str,
        start: datetime,
        end: datetime,
        wait_interval: int = 0,
        *,
        query: Optional[ODataQuery] = None,
    ) -> List[Dict[str, Any]]:
        path = (
            f"/ReportBreachesSla/Pbx.GetBreachesSlaData("
            f"queueDnStr='{queue_dns}',startDt={_fmt_dt(start)},endDt={_fmt_dt(end)},"
            f"waitInterval={wait_interval})"
        )
        data = self._get(path, params=self._query_params(query))
        return self._list_values(data)

    def get_statistic_sla(
        self,
        queue_dns: str,
        start: datetime,
        end: datetime,
        wait_interval: int = 0,
        *,
        query: Optional[ODataQuery] = None,
    ) -> List[Dict[str, Any]]:
        path = (
            f"/ReportStatisticSla/Pbx.GetStatisticSlaData("
            f"queueDnStr='{queue_dns}',startDt={_fmt_dt(start)},endDt={_fmt_dt(end)},"
            f"waitInterval={wait_interval})"
        )
        data = self._get(path, params=self._query_params(query))
        return self._list_values(data)

    def get_average_queue_wait_time(
        self,
        chart_date: datetime,
        chart_by: int,
        queue_dns: str,
        wait_interval: int = 0,
        client_timezone: str = "UTC",
        *,
        query: Optional[ODataQuery] = None,
    ) -> List[Dict[str, Any]]:
        path = (
            f"/ReportAverageQueueWaitingTime/Pbx.GetAverageQueueWaitingTimeData("
            f"chartDate={_fmt_dt(chart_date)},chartBy={chart_by},"
            f"queueDnStr='{queue_dns}',waitInterval={wait_interval},"
            f"clientTimeZone='{client_timezone}')"
        )
        data = self._get(path, params=self._query_params(query))
        return self._list_values(data)

    def get_abandoned_chats(
        self,
        queue_dns: str,
        start: datetime,
        end: datetime,
        participant_type: int = 0,
        *,
        query: Optional[ODataQuery] = None,
    ) -> List[Dict[str, Any]]:
        path = (
            f"/ReportAbandonedChatsStatistics/Pbx.GetAbandonedChatsStatisticsData("
            f"queueDnStr='{queue_dns}',startDt={_fmt_dt(start)},endDt={_fmt_dt(end)},"
            f"participantType={participant_type})"
        )
        data = self._get(path, params=self._query_params(query))
        return self._list_values(data)

    # ------------------------------------------------------------------
    # Agent login history
    # ------------------------------------------------------------------

    def get_agent_login_history(
        self,
        start: datetime,
        end: datetime,
        queue_dns: str = "",
        agent_dns: str = "",
        client_timezone: str = "UTC",
        *,
        query: Optional[ODataQuery] = None,
    ) -> List[Dict[str, Any]]:
        path = (
            f"/ReportAgentLoginHistory/Pbx.GetAgentLoginHistoryData("
            f"clientTimeZone='{client_timezone}',startDt={_fmt_dt(start)},endDt={_fmt_dt(end)},"
            f"queueDnStr='{queue_dns}',agentDnStr='{agent_dns}')"
        )
        data = self._get(path, params=self._query_params(query))
        return self._list_values(data)

    # ------------------------------------------------------------------
    # Inbound/Outbound calls
    # ------------------------------------------------------------------

    def get_inbound_calls(
        self,
        start: datetime,
        end: datetime,
        trunk_dns: str = "",
        calls_type: int = 0,
        *,
        query: Optional[ODataQuery] = None,
    ) -> List[Dict[str, Any]]:
        path = (
            f"/ReportInboundCalls/Pbx.GetInboundCalls("
            f"periodFrom={_fmt_dt(start)},periodTo={_fmt_dt(end)},"
            f"trunkDns='{trunk_dns}',callsType={calls_type})"
        )
        data = self._get(path, params=self._query_params(query))
        return self._list_values(data)

    def get_outbound_calls(
        self,
        start: datetime,
        end: datetime,
        trunk_dns: str = "",
        calls_type: int = 0,
        *,
        query: Optional[ODataQuery] = None,
    ) -> List[Dict[str, Any]]:
        path = (
            f"/ReportOutboundCalls/Pbx.GetOutboundCalls("
            f"periodFrom={_fmt_dt(start)},periodTo={_fmt_dt(end)},"
            f"trunkDns='{trunk_dns}',callsType={calls_type})"
        )
        data = self._get(path, params=self._query_params(query))
        return self._list_values(data)

    # ------------------------------------------------------------------
    # Ring group statistics
    # ------------------------------------------------------------------

    def get_ring_group_statistics(
        self,
        start: datetime,
        end: datetime,
        ring_group_dns: str = "",
        *,
        query: Optional[ODataQuery] = None,
    ) -> List[Dict[str, Any]]:
        path = (
            f"/ReportRingGroupStatistics/Pbx.GetRingGroupStatisticsData("
            f"periodFrom={_fmt_dt(start)},periodTo={_fmt_dt(end)},"
            f"ringGroupDns='{ring_group_dns}')"
        )
        data = self._get(path, params=self._query_params(query))
        return self._list_values(data)

    # ------------------------------------------------------------------
    # Call cost / distribution
    # ------------------------------------------------------------------

    def get_call_cost_by_extension_group(
        self,
        start: datetime,
        end: datetime,
        group_filter: str = "",
        call_class: int = 0,
        *,
        query: Optional[ODataQuery] = None,
    ) -> List[Dict[str, Any]]:
        path = (
            f"/ReportCallCostByExtensionGroup/Pbx.GetCallCostByExtensionGroupData("
            f"periodFrom={_fmt_dt(start)},periodTo={_fmt_dt(end)},"
            f"groupFilter='{group_filter}',callClass={call_class})"
        )
        data = self._get(path, params=self._query_params(query))
        return self._list_values(data)

    def get_call_distribution(
        self,
        start: datetime,
        end: datetime,
        group_number: str = "",
        extension_dns: str = "",
        wait_interval: int = 0,
        include_queue_calls: bool = False,
        call_area: int = 0,
        grouping_type: int = 0,
        client_timezone: str = "UTC",
        *,
        query: Optional[ODataQuery] = None,
    ) -> List[Dict[str, Any]]:
        path = (
            f"/ReportCallDistribution/Pbx.GetCallDistribution("
            f"clientTimeZone='{client_timezone}',periodFrom={_fmt_dt(start)},periodTo={_fmt_dt(end)},"
            f"groupNumber='{group_number}',extensionDns='{extension_dns}',"
            f"waitInterval={wait_interval},includeQueueCalls={_b(include_queue_calls)},"
            f"callArea={call_area},groupingType={grouping_type})"
        )
        data = self._get(path, params=self._query_params(query))
        return self._list_values(data)

    def get_user_activity(
        self,
        start: datetime,
        end: datetime,
        group_number: str = "",
        extension_dns: str = "",
        wait_interval: int = 0,
        include_queue_calls: bool = False,
        call_area: int = 0,
        grouping_type: int = 0,
        client_timezone: str = "UTC",
        *,
        query: Optional[ODataQuery] = None,
    ) -> List[Dict[str, Any]]:
        path = (
            f"/ReportUserActivity/Pbx.GetUserActivity("
            f"clientTimeZone='{client_timezone}',periodFrom={_fmt_dt(start)},periodTo={_fmt_dt(end)},"
            f"groupNumber='{group_number}',extensionDns='{extension_dns}',"
            f"waitInterval={wait_interval},includeQueueCalls={_b(include_queue_calls)},"
            f"callArea={call_area},groupingType={grouping_type})"
        )
        data = self._get(path, params=self._query_params(query))
        return self._list_values(data)

    # ------------------------------------------------------------------
    # Chat log
    # ------------------------------------------------------------------

    def get_chat_log(
        self,
        start: datetime,
        end: datetime,
        from_type: int = 0,
        from_extension: str = "",
        from_text: str = "",
        to_type: int = 0,
        to_extension: str = "",
        to_text: str = "",
        chat_type: int = 0,
        participant_type: int = 0,
        *,
        query: Optional[ODataQuery] = None,
    ) -> List[Dict[str, Any]]:
        path = (
            f"/ReportChatLog/Pbx.GetChatLog("
            f"periodFrom={_fmt_dt(start)},periodTo={_fmt_dt(end)},"
            f"fromType={from_type},fromExtension='{from_extension}',fromText='{from_text}',"
            f"toType={to_type},toExtension='{to_extension}',toText='{to_text}',"
            f"chatType={chat_type},participantType={participant_type})"
        )
        data = self._get(path, params=self._query_params(query))
        return self._list_values(data)

    # ------------------------------------------------------------------
    # Audit log
    # ------------------------------------------------------------------

    def get_audit_log(self, *, query: Optional[ODataQuery] = None) -> List[Dict[str, Any]]:
        data = self._get("/ReportAuditLog/Pbx.GetAuditLogData()", params=self._query_params(query))
        return self._list_values(data)

    # ------------------------------------------------------------------
    # Inbound rules report
    # ------------------------------------------------------------------

    def get_inbound_rules_report(self, *, query: Optional[ODataQuery] = None) -> List[Dict[str, Any]]:
        data = self._get("/ReportInboundRules/Pbx.GetInboundRulesData()", params=self._query_params(query))
        return self._list_values(data)

    # ------------------------------------------------------------------
    # Abandoned queue calls
    # ------------------------------------------------------------------

    def get_abandoned_queue_calls(
        self,
        start: datetime,
        end: datetime,
        queue_dns: str = "",
        wait_interval: int = 0,
        *,
        query: Optional[ODataQuery] = None,
    ) -> List[Dict[str, Any]]:
        path = (
            f"/ReportAbandonedQueueCalls/Pbx.GetAbandonedQueueCallsData("
            f"periodFrom={_fmt_dt(start)},periodTo={_fmt_dt(end)},"
            f"queueDns='{queue_dns}',waitInterval={wait_interval})"
        )
        data = self._get(path, params=self._query_params(query))
        return self._list_values(data)

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
        return self._list_values(data)

    def purge_activity_logs(self) -> None:
        self._post("/ActivityLog/Pbx.PurgeLogs")

    # ------------------------------------------------------------------
    # Scheduled reports CRUD
    # ------------------------------------------------------------------

    def list_scheduled_reports(self, query: Optional[ODataQuery] = None) -> List[Dict[str, Any]]:
        data = self._list_raw("/ScheduledReports", query)
        return self._list_values(data)

    def iterate_scheduled_reports(self, query: Optional[ODataQuery] = None) -> Iterator[Dict[str, Any]]:
        params = self._query_params(query) or None
        path: Optional[str] = "/ScheduledReports"
        while path:
            data = self._get(path, params=params)
            yield from data.get("value", [])
            path = data.get("@odata.nextLink")
            params = None

    def create_scheduled_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._post("/ScheduledReports", json=data)

    def get_scheduled_report(self, report_id: int) -> Dict[str, Any]:
        return self._get(f"/ScheduledReports({report_id})")

    def update_scheduled_report(self, report_id: int, changes: Dict[str, Any]) -> None:
        self._patch(f"/ScheduledReports({report_id})", json=changes)

    def delete_scheduled_report(self, report_id: int) -> None:
        self._delete(f"/ScheduledReports({report_id})")
