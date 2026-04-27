from __future__ import annotations

from typing import Any, Dict, Optional

import httpx

from .auth import OAuth2Auth
from .services.active_calls import ActiveCallsService
from .services.backups import BackupsService
from .services.call_flow import CallFlowService
from .services.call_history import CallHistoryService
from .services.chat import ChatService
from .services.contacts import ContactsService
from .services.crm import CrmService
from .services.defs import DefsService
from .services.email import EmailService
from .services.emergency import EmergencyService
from .services.event_logs import EventLogsService
from .services.fax import FaxService
from .services.groups import GroupsService
from .services.holidays import HolidaysService
from .services.inbound_rules import InboundRulesService
from .services.integrations import IntegrationsService
from .services.my_group import MyGroupService
from .services.my_user import MyUserService
from .services.outbound_rules import OutboundRulesService
from .services.parameters import ParametersService
from .services.parkings import ParkingsService
from .services.pbx_services import PbxServicesService
from .services.phones import PhonesService
from .services.prompts import PromptsService
from .services.queues import QueuesService
from .services.receptionists import ReceptionistsService
from .services.recordings import RecordingsService
from .services.reports import ReportsService
from .services.ring_groups import RingGroupsService
from .services.security import SecurityService
from .services.settings import SettingsService
from .services.system import SystemService
from .services.trunks import TrunksService
from .services.updates import UpdatesService
from .services.users import UsersService
from .services.voicemail import VoicemailService
from .services.website_links import WebsiteLinksService

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
        self.backups = BackupsService(self._http)
        self.call_flow = CallFlowService(self._http)
        self.call_history = CallHistoryService(self._http)
        self.chat = ChatService(self._http)
        self.contacts = ContactsService(self._http)
        self.crm = CrmService(self._http)
        self.defs = DefsService(self._http)
        self.email = EmailService(self._http)
        self.emergency = EmergencyService(self._http)
        self.event_logs = EventLogsService(self._http)
        self.fax = FaxService(self._http)
        self.groups = GroupsService(self._http)
        self.holidays = HolidaysService(self._http)
        self.inbound_rules = InboundRulesService(self._http)
        self.integrations = IntegrationsService(self._http)
        self.my_group = MyGroupService(self._http)
        self.my_user = MyUserService(self._http)
        self.outbound_rules = OutboundRulesService(self._http)
        self.parameters = ParametersService(self._http)
        self.parkings = ParkingsService(self._http)
        self.pbx_services = PbxServicesService(self._http)
        self.phones = PhonesService(self._http)
        self.prompts = PromptsService(self._http)
        self.queues = QueuesService(self._http)
        self.receptionists = ReceptionistsService(self._http)
        self.recordings = RecordingsService(self._http)
        self.reports = ReportsService(self._http)
        self.ring_groups = RingGroupsService(self._http)
        self.security = SecurityService(self._http)
        self.settings = SettingsService(self._http)
        self.system = SystemService(self._http)
        self.trunks = TrunksService(self._http)
        self.updates = UpdatesService(self._http)
        self.users = UsersService(self._http)
        self.voicemail = VoicemailService(self._http)
        self.website_links = WebsiteLinksService(self._http)

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
