from __future__ import annotations

from typing import Any, Dict, Optional
from urllib.parse import urljoin

import httpx

from .auth import OAuth2Auth
from .services.active_calls import ActiveCallsService
from .services.call_history import CallHistoryService
from .services.contacts import ContactsService
from .services.phones import PhonesService
from .services.queues import QueuesService
from .services.reports import ReportsService
from .services.ring_groups import RingGroupsService
from .services.system import SystemService
from .services.trunks import TrunksService
from .services.users import UsersService

_DEFAULT_API_PATH = "/xapi/v1"


class ThreeCXClient:
    """Entry point for the 3CX XAPI Python SDK.

    Usage::

        client = ThreeCXClient(
            base_url="https://pbx.example.com",
            client_id="my-service-principal-id",
            client_secret="my-secret",
        )

        # List active calls
        for call in client.active_calls.list():
            print(call.caller, "→", call.callee)

        # Find a user by extension number
        users = client.users.list(
            ODataQuery().filter("Number eq '100'")
        )

        # Pull 7 days of call history
        from datetime import datetime, timedelta
        end = datetime.utcnow()
        start = end - timedelta(days=7)
        entries = client.reports.get_call_log(start, end)

    Args:
        base_url: Root URL of the 3CX instance, e.g. ``https://pbx.example.com``.
        client_id: Service-principal client ID (Admin → Integrations → API).
        client_secret: Service-principal client secret.
        api_path: API prefix; defaults to ``/xapi/v1``.
        timeout: HTTP request timeout in seconds (default 30).
        verify_ssl: Set to ``False`` to skip TLS verification (not recommended in production).
        httpx_kwargs: Additional keyword arguments forwarded to :class:`httpx.Client`.
    """

    def __init__(
        self,
        base_url: str,
        client_id: str,
        client_secret: str,
        *,
        api_path: str = _DEFAULT_API_PATH,
        timeout: float = 30.0,
        verify_ssl: bool = True,
        **httpx_kwargs: Any,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._auth = OAuth2Auth(
            base_url=self._base_url,
            client_id=client_id,
            client_secret=client_secret,
        )
        self._http = httpx.Client(
            base_url=self._base_url + api_path,
            auth=self._auth,
            timeout=timeout,
            verify=verify_ssl,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            **httpx_kwargs,
        )

        # --- service registry ---
        self.active_calls = ActiveCallsService(self._http)
        self.users = UsersService(self._http)
        self.queues = QueuesService(self._http)
        self.ring_groups = RingGroupsService(self._http)
        self.call_history = CallHistoryService(self._http)
        self.trunks = TrunksService(self._http)
        self.contacts = ContactsService(self._http)
        self.phones = PhonesService(self._http)
        self.system = SystemService(self._http)
        self.reports = ReportsService(self._http)

    # ------------------------------------------------------------------
    # Context-manager support
    # ------------------------------------------------------------------

    def __enter__(self) -> ThreeCXClient:
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()

    def close(self) -> None:
        """Close the underlying HTTP session."""
        self._http.close()

    # ------------------------------------------------------------------
    # Convenience / escape hatches
    # ------------------------------------------------------------------

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Perform a raw GET against any XAPI path."""
        return self.system.get_raw(path, params=params)

    def post(self, path: str, json: Any = None) -> Any:
        """Perform a raw POST against any XAPI path."""
        return self.system.post_raw(path, json=json)

    def invalidate_token(self) -> None:
        """Force re-authentication on the next request."""
        self._auth.invalidate()

    def __repr__(self) -> str:
        return f"ThreeCXClient(base_url={self._base_url!r})"
