from __future__ import annotations

from typing import Any, Dict, List

from .base import BaseService


class SettingsService(BaseService):
    """Access to all PBX settings domains."""

    # ------------------------------------------------------------------
    # General settings
    # ------------------------------------------------------------------

    def get_general_pbx_settings(self) -> Dict[str, Any]:
        return self._get("/GeneralSettingsForPbx")

    def update_general_pbx_settings(self, data: Dict[str, Any]) -> None:
        self._patch("/GeneralSettingsForPbx", json=data)

    def get_general_app_settings(self) -> Dict[str, Any]:
        return self._get("/GeneralSettingsForApps")

    def update_general_app_settings(self, data: Dict[str, Any]) -> None:
        self._patch("/GeneralSettingsForApps", json=data)

    # ------------------------------------------------------------------
    # Mail settings
    # ------------------------------------------------------------------

    def get_mail_settings(self) -> Dict[str, Any]:
        return self._get("/MailSettings")

    def update_mail_settings(self, data: Dict[str, Any]) -> None:
        self._patch("/MailSettings", json=data)

    def test_email(self, data: Dict[str, Any]) -> None:
        self._post("/MailSettings/Pbx.TestEmail", json=data)

    # ------------------------------------------------------------------
    # CDR / call costs
    # ------------------------------------------------------------------

    def get_cdr_settings(self) -> Dict[str, Any]:
        return self._get("/CDRSettings")

    def update_cdr_settings(self, data: Dict[str, Any]) -> None:
        self._patch("/CDRSettings", json=data)

    def get_call_cost_settings(self) -> Dict[str, Any]:
        data = self._get("/CallCostSettings")
        result: Dict[str, Any] = data.get("value", data) if isinstance(data, dict) else data
        return result

    def export_call_costs(self) -> bytes:
        return self._get_bytes("/CallCostSettings/Pbx.ExportCallCosts()")

    def update_call_cost(self, data: Dict[str, Any]) -> None:
        self._post("/CallCostSettings/Pbx.UpdateCost", json=data)

    def get_call_types_settings(self) -> Dict[str, Any]:
        return self._get("/CallTypesSettings")

    def update_call_types_settings(self, data: Dict[str, Any]) -> None:
        self._patch("/CallTypesSettings", json=data)

    # ------------------------------------------------------------------
    # Chat log settings
    # ------------------------------------------------------------------

    def get_chat_log_settings(self) -> Dict[str, Any]:
        return self._get("/ChatLogSettings")

    def update_chat_log_settings(self, data: Dict[str, Any]) -> None:
        self._patch("/ChatLogSettings", json=data)

    # ------------------------------------------------------------------
    # Codecs settings
    # ------------------------------------------------------------------

    def get_codecs_settings(self) -> Dict[str, Any]:
        return self._get("/CodecsSettings")

    def update_codecs_settings(self, data: Dict[str, Any]) -> None:
        self._patch("/CodecsSettings", json=data)

    # ------------------------------------------------------------------
    # Conference settings
    # ------------------------------------------------------------------

    def get_conference_settings(self) -> Dict[str, Any]:
        return self._get("/ConferenceSettings")

    def update_conference_settings(self, data: Dict[str, Any]) -> None:
        self._patch("/ConferenceSettings", json=data)

    def get_web_meeting_zones(self) -> List[Dict[str, Any]]:
        data = self._get("/ConferenceSettings/Pbx.GetWebMeetingZones()")
        return self._list_values(data) if isinstance(data, dict) else data

    def generate_api_key(self) -> str:
        data = self._get("/ConferenceSettings/Pbx.GenerateApiKey()")
        return str(data.get("value", ""))

    def delete_api_key(self, data: Dict[str, Any]) -> None:
        self._post("/ConferenceSettings/Pbx.DeleteApiKey", json=data)

    def get_mcu_request_status(self) -> Dict[str, Any]:
        return self._get("/ConferenceSettings/Pbx.GetMCURequestStatus()")

    def get_onboard_mcu_data(self) -> Dict[str, Any]:
        return self._get("/ConferenceSettings/Pbx.GetOnboardMcuData()")

    def get_onboard_meetings(self) -> Dict[str, Any]:
        return self._get("/ConferenceSettings/Pbx.GetOnboardMeetings()")

    def get_mcu_rows(self) -> List[Dict[str, Any]]:
        data = self._get("/ConferenceSettings/Pbx.GetMCURows()")
        return self._list_values(data) if isinstance(data, dict) else data

    def update_mcu_request_status(self, data: Dict[str, Any]) -> None:
        self._post("/ConferenceSettings/Pbx.UpdateMCURequestStatus", json=data)

    # ------------------------------------------------------------------
    # Console restrictions
    # ------------------------------------------------------------------

    def get_console_restrictions(self) -> Dict[str, Any]:
        return self._get("/ConsoleRestrictions")

    def update_console_restrictions(self, data: Dict[str, Any]) -> None:
        self._patch("/ConsoleRestrictions", json=data)

    # ------------------------------------------------------------------
    # Dial code / E164 / secure SIP
    # ------------------------------------------------------------------

    def get_dial_code_settings(self) -> Dict[str, Any]:
        return self._get("/DialCodeSettings")

    def update_dial_code_settings(self, data: Dict[str, Any]) -> None:
        self._patch("/DialCodeSettings", json=data)

    def get_e164_settings(self) -> Dict[str, Any]:
        return self._get("/E164Settings")

    def update_e164_settings(self, data: Dict[str, Any]) -> None:
        self._patch("/E164Settings", json=data)

    def get_secure_sip_settings(self) -> Dict[str, Any]:
        return self._get("/SecureSipSettings")

    def update_secure_sip_settings(self, data: Dict[str, Any]) -> None:
        self._patch("/SecureSipSettings", json=data)

    # ------------------------------------------------------------------
    # Logging / syslog settings
    # ------------------------------------------------------------------

    def get_logging_settings(self) -> Dict[str, Any]:
        return self._get("/LoggingSettings")

    def update_logging_settings(self, data: Dict[str, Any]) -> None:
        self._patch("/LoggingSettings", json=data)

    def get_syslog_settings(self) -> Dict[str, Any]:
        return self._get("/SyslogSettings")

    def update_syslog_settings(self, data: Dict[str, Any]) -> None:
        self._patch("/SyslogSettings", json=data)

    def test_syslog_connection(self) -> None:
        self._post("/SyslogSettings/Pbx.TestConnection")

    # ------------------------------------------------------------------
    # Notification / phone book settings
    # ------------------------------------------------------------------

    def get_notification_settings(self) -> Dict[str, Any]:
        return self._get("/NotificationSettings")

    def update_notification_settings(self, data: Dict[str, Any]) -> None:
        self._patch("/NotificationSettings", json=data)

    def get_phone_book_settings(self) -> Dict[str, Any]:
        return self._get("/PhoneBookSettings")

    def update_phone_book_settings(self, data: Dict[str, Any]) -> None:
        self._patch("/PhoneBookSettings", json=data)

    def get_phones_settings(self) -> Dict[str, Any]:
        return self._get("/PhonesSettings")

    def update_phones_settings(self, data: Dict[str, Any]) -> None:
        self._patch("/PhonesSettings", json=data)

    # ------------------------------------------------------------------
    # Country codes / hotel services
    # ------------------------------------------------------------------

    def get_country_codes(self) -> Dict[str, Any]:
        return self._get("/CountryCodes")

    def update_country_codes(self, data: Dict[str, Any]) -> None:
        self._patch("/CountryCodes", json=data)

    def get_hotel_services(self) -> Dict[str, Any]:
        return self._get("/HotelServices")

    def update_hotel_services(self, data: Dict[str, Any]) -> None:
        self._patch("/HotelServices", json=data)

    # ------------------------------------------------------------------
    # Network settings
    # ------------------------------------------------------------------

    def get_network_settings(self) -> Dict[str, Any]:
        return self._get("/NetworkSettings")

    def update_network_settings(self, data: Dict[str, Any]) -> None:
        self._patch("/NetworkSettings", json=data)

    def get_network_interfaces(self) -> List[Dict[str, Any]]:
        data = self._get("/NetworkInterfaces")
        return self._list_values(data) if isinstance(data, dict) else data

    def get_ifaces(self) -> List[Dict[str, Any]]:
        data = self._get("/NetworkSettings/Pbx.GetIfaces()")
        return self._list_values(data) if isinstance(data, dict) else data
