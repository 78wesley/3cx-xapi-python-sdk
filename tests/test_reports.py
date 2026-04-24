"""Tests for ReportsService — URL construction and response parsing."""
from __future__ import annotations

import re
from datetime import datetime, timezone

import pytest
from pytest_httpx import HTTPXMock

from tests.conftest import TOKEN_URL, TOKEN_JSON, API_BASE
from threecx import ThreeCXClient
from threecx.services.reports import _fmt_dt


START = datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
END = datetime(2026, 1, 7, 23, 59, 59, tzinfo=timezone.utc)

START_STR = "2026-01-01T00:00:00+00:00"
END_STR = "2026-01-07T23:59:59+00:00"


@pytest.fixture
def client(httpx_mock: HTTPXMock) -> ThreeCXClient:
    httpx_mock.add_response(url=TOKEN_URL, method="POST", json=TOKEN_JSON, is_reusable=True)
    return ThreeCXClient("https://pbx.test", "id", "secret")


# --- _fmt_dt helper -----------------------------------------------------------

def test_fmt_dt_formats_correctly() -> None:
    dt = datetime(2026, 3, 15, 9, 5, 30, tzinfo=timezone.utc)
    assert _fmt_dt(dt) == "2026-03-15T09:05:30+00:00"


# --- get_call_log -------------------------------------------------------------

def test_get_call_log(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    expected_path = (
        f"/ReportCallLogData/Pbx.GetCallLogData("
        f"periodFrom={START_STR},periodTo={END_STR})"
    )
    httpx_mock.add_response(
        url=API_BASE + expected_path,
        json={"value": [{"Id": "cdr-1", "Caller": "100", "TalkDuration": 60}]},
    )
    rows = client.reports.get_call_log(START, END)
    assert len(rows) == 1
    assert rows[0]["Caller"] == "100"


def test_get_call_log_empty(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    expected_path = (
        f"/ReportCallLogData/Pbx.GetCallLogData("
        f"periodFrom={START_STR},periodTo={END_STR})"
    )
    httpx_mock.add_response(url=API_BASE + expected_path, json={"value": []})
    rows = client.reports.get_call_log(START, END)
    assert rows == []


# --- get_extension_statistics -------------------------------------------------

def test_get_extension_statistics(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    path = (
        f"/ReportExtensionStatistics/Pbx.GetExtensionStatistics("
        f"periodFrom={START_STR},periodTo={END_STR})"
    )
    httpx_mock.add_response(
        url=API_BASE + path,
        json={"value": [{"Extension": "100", "TotalCalls": 15}]},
    )
    rows = client.reports.get_extension_statistics(START, END)
    assert rows[0]["TotalCalls"] == 15


# --- get_queue_performance_overview ------------------------------------------

def test_get_queue_performance_overview(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    path = (
        f"/ReportQueuePerformanceOverview/Pbx.GetQueuePerformanceOverview("
        f"periodFrom={START_STR},periodTo={END_STR})"
    )
    httpx_mock.add_response(
        url=API_BASE + path,
        json={"value": [{"QueueName": "Support", "AnsweredCalls": 50}]},
    )
    rows = client.reports.get_queue_performance_overview(START, END)
    assert rows[0]["QueueName"] == "Support"


# --- get_agent_login_history --------------------------------------------------

def test_get_agent_login_history(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    path = (
        f"/ReportAgentLoginHistory/Pbx.GetAgentLoginHistory("
        f"periodFrom={START_STR},periodTo={END_STR})"
    )
    httpx_mock.add_response(
        url=API_BASE + path,
        json={"value": [{"Agent": "100", "LoginTime": "2026-01-02T08:00:00Z"}]},
    )
    rows = client.reports.get_agent_login_history(START, END)
    assert rows[0]["Agent"] == "100"


# --- activity log -------------------------------------------------------------

def test_get_activity_log_filter(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=API_BASE + "/ActivityLog/Pbx.GetFilter()",
        json={"Extensions": ["100", "101"], "Severities": ["Info", "Warning"]},
    )
    result = client.reports.get_activity_log_filter()
    assert "Extensions" in result


def test_get_activity_logs_no_filters(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    path = (
        f"/ActivityLog/Pbx.GetLogs("
        f"startDate={START_STR},endDate={END_STR},"
        f"extension=null,call=null,severity=null)"
    )
    httpx_mock.add_response(
        url=API_BASE + path,
        json={"value": [{"Message": "System started", "Severity": "Info"}]},
    )
    rows = client.reports.get_activity_logs(START, END)
    assert rows[0]["Message"] == "System started"


def test_get_activity_logs_with_filters(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    path = (
        f"/ActivityLog/Pbx.GetLogs("
        f"startDate={START_STR},endDate={END_STR},"
        f"extension='100',call=null,severity='Warning')"
    )
    httpx_mock.add_response(
        url=API_BASE + path,
        json={"value": [{"Message": "Missed call", "Extension": "100"}]},
    )
    rows = client.reports.get_activity_logs(START, END, extension="100", severity="Warning")
    assert rows[0]["Extension"] == "100"


def test_purge_activity_logs(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=API_BASE + "/ActivityLog/Pbx.PurgeLogs",
        method="POST",
        status_code=204,
    )
    client.reports.purge_activity_logs()


# --- get_abandoned_queue_calls ------------------------------------------------

def test_get_abandoned_queue_calls(client: ThreeCXClient, httpx_mock: HTTPXMock) -> None:
    path = (
        f"/ReportAbandonedQueueCalls/Pbx.GetAbandonedQueueCalls("
        f"periodFrom={START_STR},periodTo={END_STR})"
    )
    httpx_mock.add_response(
        url=API_BASE + path,
        json={"value": [{"Caller": "0031612345678", "QueueName": "Support"}]},
    )
    rows = client.reports.get_abandoned_queue_calls(START, END)
    assert rows[0]["QueueName"] == "Support"
